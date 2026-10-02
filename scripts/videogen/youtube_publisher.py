#!/usr/bin/env python3
"""
TokyoFlow YouTube Master Publishing & Scheduling Automation Engine
Automatically parses release packages, assigns schedule slots based on EST publication contract,
and uploads videos/Shorts with scheduled publishing (publishAt), custom thumbnails, and clean metadata.
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
import zoneinfo
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Import local auth
sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
LEDGER_FILE = RELEASES_DIR / "publish_ledger.json"

EST_TZ = zoneinfo.ZoneInfo("America/New_York")

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U00002B50-\U00002B55"
    "\U0000200D"
    "\U0000FE0F"
    "]+",
    flags=re.UNICODE
)

def load_ledger() -> dict:
    if LEDGER_FILE.exists():
        try:
            with open(LEDGER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"published": {}, "slots": []}

def save_ledger(ledger: dict):
    RELEASES_DIR.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

def extract_metadata_fields(md_path: Path):
    """Extracts title, description, and tags from metadata.md or short_metadata.md."""
    if not md_path.exists():
        return None
    content = md_path.read_text(encoding="utf-8")
    
    # Check for schedule kit fallback in same directory
    kit_path = md_path.parent / "youtube_schedule_kit.json"
    kit_data = None
    if kit_path.exists():
        try:
            kit_data = json.loads(kit_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # 1. Extract Title
    # Pattern A: in code block under header
    title_match = re.search(r"##\s*(?:YouTube\s+)?(?:Video|Shorts?)\s+Title[^\n]*\n+```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Pattern B: plain line under header
        plain_title_match = re.search(r"##\s*(?:YouTube\s+)?(?:Video|Shorts?)\s+Title[^\n]*\n+([^\n#]+)", content, re.IGNORECASE)
        if plain_title_match:
            title = plain_title_match.group(1).strip()
        elif kit_data:
            is_short_file = "short" in md_path.name.lower()
            if is_short_file and "shorts_package" in kit_data:
                title = kit_data["shorts_package"].get("title", "")
            elif "long_form_package" in kit_data:
                title = kit_data["long_form_package"].get("title", "")
        else:
            title = ""
    
    # 2. Extract Description
    # Pattern A: in code block
    desc_match = re.search(r"##\s*(?:YouTube\s+)?(?:Shorts?|Video)?\s*Description(?: Box)?[^\n]*\n+```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        # Pattern B: plain text until next section
        plain_desc_match = re.search(r"##\s*(?:YouTube\s+)?(?:Shorts?|Video)?\s*Description[^\n]*\n+(.*?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
        if plain_desc_match:
            description = plain_desc_match.group(1).strip()
        else:
            description = ""
    
    # 3. Extract Tags / Hashtags
    tags_match = re.findall(r"#([a-zA-Z0-9_\u3040-\u30ff\u4e00-\u9faf]+)", content)
    tags = list(dict.fromkeys(tags_match)) if tags_match else [
        "TokyoFlow", "LearnJapanese", "JapaneseSpeaking", "TokyoTravel", "JLPT", "JapaneseShadowing"
    ]
    
    # Clean fallback if title/desc missing
    # Strip ALL emojis permanently
    title = EMOJI_PATTERN.sub("", title).strip()
    title = re.sub(r" +", " ", title)
    description = EMOJI_PATTERN.sub("", description).strip()

    return {
        "title": title[:100],  # YouTube title max 100 chars
        "description": description,
        "tags": tags[:30]
    }

def generate_next_slots(start_from_dt: datetime, count: int = 30) -> list:
    """
    Generates chronological EST schedule slots adhering to the Master Contract:
    - Weekdays (Mon-Fri): 08:00 AM EST & 05:00 PM EST
    - Weekends (Sat-Sun): 05:00 PM EST
    """
    slots = []
    current_date = start_from_dt.date()
    
    while len(slots) < count:
        weekday = current_date.weekday() # 0 = Monday, 6 = Sunday
        if weekday in range(0, 5): # Mon - Fri
            t1 = datetime(current_date.year, current_date.month, current_date.day, 8, 0, 0, tzinfo=EST_TZ)
            t2 = datetime(current_date.year, current_date.month, current_date.day, 17, 0, 0, tzinfo=EST_TZ)
            if t1 > start_from_dt:
                slots.append({"time_est": t1, "slot_type": "weekday_morning", "allows_compilation": False})
            if t2 > start_from_dt:
                slots.append({"time_est": t2, "slot_type": "weekday_evening", "allows_compilation": False})
        else: # Saturday (5) or Sunday (6)
            t_weekend = datetime(current_date.year, current_date.month, current_date.day, 17, 0, 0, tzinfo=EST_TZ)
            if t_weekend > start_from_dt:
                slots.append({"time_est": t_weekend, "slot_type": "weekend_evening", "allows_compilation": True})
        current_date += timedelta(days=1)
        
    return slots

def get_next_available_slot(ledger: dict, is_compilation: bool = False, min_hours_ahead: int = 2) -> datetime:
    """Finds the next unreserved publishing slot in EST."""
    now_est = datetime.now(EST_TZ) + timedelta(hours=min_hours_ahead)
    reserved_times = {
        item["publish_at_est"] for item in ledger.get("published", {}).values() if "publish_at_est" in item
    }
    
    candidate_slots = generate_next_slots(now_est, count=60)
    for slot in candidate_slots:
        iso_str = slot["time_est"].isoformat()
        if is_compilation and not slot["allows_compilation"]:
            continue
        if not is_compilation and slot["allows_compilation"]:
            # Reserve weekend slots primarily for compilations unless configured otherwise
            continue
        if iso_str not in reserved_times:
            return slot["time_est"]
            
    # Fallback
    return candidate_slots[0]["time_est"]

def upload_video_asset(youtube, video_path: Path, thumbnail_path: Path, meta: dict, publish_at: datetime, is_short: bool = False):
    """Uploads a video to YouTube with scheduled publication (publishAt) and custom thumbnail."""
    print(f"\n Preparing upload for: {meta['title']}")
    print(f" Video file: {video_path} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
    print(f" Scheduled Publish Time: {publish_at.strftime('%Y-%m-%d %I:%M %p %Z')} ({publish_at.isoformat()})")
    
    # Append #Shorts to title and description if it's a short
    title = meta["title"]
    if is_short and "#Shorts" not in title and "#shorts" not in title:
        if len(title) + 8 <= 100:
            title = f"{title} #Shorts"
            
    body = {
        "snippet": {
            "title": title,
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "27", # 27 = Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "ja"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.isoformat(),
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(
        str(video_path),
        chunksize=8*1024*1024,
        resumable=True,
        mimetype="video/mp4"
    )
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   ⏳ Upload Progress: {int(status.progress() * 100)}%")
            
    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f" Video Uploaded Successfully! ID: {video_id} -> {video_url}")
    
    # Upload Thumbnail if present and not a Short
    if thumbnail_path and thumbnail_path.exists():
        try:
            print(f" Uploading custom thumbnail: {thumbnail_path.name}...")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
            ).execute()
            print(" Custom thumbnail applied successfully.")
        except Exception as e:
            print(f" Warning: Could not upload thumbnail: {e}")
            
    return {
        "video_id": video_id,
        "video_url": video_url,
        "title": title,
        "publish_at_est": publish_at.isoformat(),
        "uploaded_at": datetime.now(EST_TZ).isoformat(),
        "is_short": is_short
    }
# Scenario / Topic Playlists
PLAYLIST_ROUTERS = {
    "transit": "PLAUUBQzM_liE",     # Tokyo Transit & Station Japanese (E01, E05, ...)
    "kombini": "PLBhQ4N46ef1k",     # Kombini & Street Survival Japanese (E02, E06, ...)
    "dining": "PLA-JfaJhOu2E",      # Izakaya & Tokyo Foodie Japanese (E03, E07, ...)
    "shopping": "PLPigp6inTnV8",    # Anime & Tokyo Shopping Japanese (E04, E08, ...)
    "news": "PLHPFg4RJy4Po"         # NHK Daily News & Shadowing Drills
}

# Dedicated JLPT Level Playlists
JLPT_PLAYLIST_ROUTERS = {
    "N5": "PLY_ZLcqTrnU8",          # 🎯 JLPT N5 | Zero-Prerequisite Real Japanese
    "N4": "PLIiV1gnNj8Ms",          # 🎯 JLPT N4 | Practical Everyday Tokyo Japanese
    "N3": "PLFBaqxuiTcbo",          # 🎯 JLPT N3 | Intermediate News & Conversational Nuance
    "N2-N1": "PLeb_7jP3fQ2M"        # 🎯 JLPT N2-N1 | Advanced Japanese & Professional Nuance
}

def resolve_playlist_id(ep_name: str) -> str:
    ep_lower = ep_name.lower()
    if "transit" in ep_lower or "subway" in ep_lower or "yamanote" in ep_lower:
        return PLAYLIST_ROUTERS["transit"]
    elif "kombini" in ep_lower or "checkout" in ep_lower or "coffee" in ep_lower:
        return PLAYLIST_ROUTERS["kombini"]
    elif "izakaya" in ep_lower or "ramen" in ep_lower or "dining" in ep_lower:
        return PLAYLIST_ROUTERS["dining"]
    elif "akiba" in ep_lower or "shopping" in ep_lower or "ginza" in ep_lower or "anime" in ep_lower or "sauna" in ep_lower:
        return PLAYLIST_ROUTERS["shopping"]
    return None

def resolve_jlpt_playlist_id(title: str, ep_name: str = "") -> str:
    """Resolves the JLPT level playlist ID based on title badge or episode name."""
    m = re.search(r"\[JLPT\s*(N[1-5](?:-N[1-5])?)\]", title, re.IGNORECASE)
    if m:
        lvl = m.group(1).upper()
        if lvl in JLPT_PLAYLIST_ROUTERS:
            return JLPT_PLAYLIST_ROUTERS[lvl]
        elif "N2" in lvl or "N1" in lvl:
            return JLPT_PLAYLIST_ROUTERS["N2-N1"]
        elif "N4" in lvl:
            return JLPT_PLAYLIST_ROUTERS["N4"]
        elif "N5" in lvl:
            return JLPT_PLAYLIST_ROUTERS["N5"]
    return JLPT_PLAYLIST_ROUTERS["N5"]

def add_video_to_playlist(youtube, video_id: str, playlist_id: str):
    if not youtube or not playlist_id:
        return
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f" Added video {video_id} to playlist {playlist_id}")
    except Exception as e:
        print(f" Notice: Playlist add: {e}")

# Tailored Schedule Mapping (Custom Schedule Plan)
EXPLICIT_SCHEDULE_PLAN = {
    # 2026-09-30 (Wed) Shorts Blast: 2 Morning + 2 Evening
    "E01-Yamanote_Transit-v1.0_short": datetime(2026, 9, 30, 8, 0, 0, tzinfo=EST_TZ),
    "E02-Kombini_Checkout-v1.0_short": datetime(2026, 9, 30, 9, 30, 0, tzinfo=EST_TZ),
    "E03-Izakaya_Night-v1.0_short": datetime(2026, 9, 30, 17, 0, 0, tzinfo=EST_TZ),
    "E04-Akiba_Pilgrimage-v1.0_short": datetime(2026, 9, 30, 18, 30, 0, tzinfo=EST_TZ),
    
    # 2026-10-01 (Thu) E05 & E06 Launch
    "E05-Tokyo_Subway_Rush-v1.0_video": datetime(2026, 10, 1, 8, 0, 0, tzinfo=EST_TZ),
    "E05-Tokyo_Subway_Rush-v1.0_short": datetime(2026, 10, 1, 8, 0, 0, tzinfo=EST_TZ),
    "E06-Kombini_Coffee_ATM-v1.0_video": datetime(2026, 10, 1, 17, 0, 0, tzinfo=EST_TZ),
    "E06-Kombini_Coffee_ATM-v1.0_short": datetime(2026, 10, 1, 17, 0, 0, tzinfo=EST_TZ),
    
    # 2026-10-02 (Fri) E07 & E08 Launch
    "E07-Ramen_Ticket_Vending-v1.0_video": datetime(2026, 10, 2, 8, 0, 0, tzinfo=EST_TZ),
    "E07-Ramen_Ticket_Vending-v1.0_short": datetime(2026, 10, 2, 8, 0, 0, tzinfo=EST_TZ),
    "E08-Ginza_TaxFree_Shopping-v1.0_video": datetime(2026, 10, 2, 17, 0, 0, tzinfo=EST_TZ),
    "E08-Ginza_TaxFree_Shopping-v1.0_short": datetime(2026, 10, 2, 17, 0, 0, tzinfo=EST_TZ),
}

def get_slot_for_asset(asset_key: str, ledger: dict, is_compilation: bool = False) -> datetime:
    """Returns the explicit slot if configured, otherwise computes next available slot."""
    if asset_key in EXPLICIT_SCHEDULE_PLAN:
        return EXPLICIT_SCHEDULE_PLAN[asset_key]
    return get_next_available_slot(ledger, is_compilation=is_compilation)

def process_releases(dry_run: bool = False, episode_filter: str = None):
    """Scans all episode release folders and executes scheduled upload."""
    ledger = load_ledger()
    creds = None if dry_run else get_authenticated_service()
    youtube = None if dry_run else build("youtube", "v3", credentials=creds)
    
    release_dirs = sorted([d for d in RELEASES_DIR.iterdir() if d.is_dir() and d.name.startswith("E")])
    
    print(f"\n==================================================")
    print(f" TokyoFlow Master Release & Scheduler Pipeline")
    print(f"Found {len(release_dirs)} packaged episode releases in {RELEASES_DIR.name}")
    print(f"Dry Run Mode: {dry_run}")
    print(f"==================================================\n")
    
    for rel_dir in release_dirs:
        ep_name = rel_dir.name
        if episode_filter and episode_filter not in ep_name:
            continue
            
        print(f"\n Inspecting Release: {ep_name}")
        
        # 1. Check Long-form (16:9 Micro-Lesson)
        video_mp4 = rel_dir / "video.mp4"
        thumb_jpg = rel_dir / "thumbnail.jpg"
        meta_md = rel_dir / "metadata.md"
        long_key = f"{ep_name}_video"
        
        if video_mp4.exists() and meta_md.exists():
            if long_key in ledger.get("published", {}):
                pub_item = ledger["published"][long_key]
                pub_url = pub_item.get("video_url", "Public/Manual")
                pub_time = pub_item.get("publish_at_est", "Published")
                print(f"   ℹ Micro-lesson already recorded/published: {pub_url} ({pub_time})")
            else:
                meta = extract_metadata_fields(meta_md)
                slot_time = get_slot_for_asset(long_key, ledger, is_compilation=False)
                
                if dry_run:
                    print(f"   [DRY-RUN] Would upload Micro-lesson: '{meta['title']}' scheduled for {slot_time.strftime('%Y-%m-%d %I:%M %p %Z')}")
                    # Simulate reservation
                    ledger.setdefault("published", {})[long_key] = {"publish_at_est": slot_time.isoformat()}
                else:
                    record = upload_video_asset(youtube, video_mp4, thumb_jpg, meta, slot_time, is_short=False)
                    ledger.setdefault("published", {})[long_key] = record
                    save_ledger(ledger)
                    pl_id = resolve_playlist_id(ep_name)
                    if pl_id:
                        add_video_to_playlist(youtube, record["video_id"], pl_id)
                    jlpt_pl_id = resolve_jlpt_playlist_id(meta["title"], ep_name)
                    if jlpt_pl_id and jlpt_pl_id != pl_id:
                        add_video_to_playlist(youtube, record["video_id"], jlpt_pl_id)
                    
        # 2. Check Short (9:16 Vertical Short)
        short_mp4 = rel_dir / "short.mp4"
        short_thumb_jpg = rel_dir / "short_thumbnail.jpg"
        short_meta_md = rel_dir / "short_metadata.md"
        short_key = f"{ep_name}_short"
        
        if short_mp4.exists() and short_meta_md.exists():
            if short_key in ledger.get("published", {}):
                pub_item = ledger["published"][short_key]
                pub_url = pub_item.get("video_url", "Public/Manual")
                pub_time = pub_item.get("publish_at_est", "Published")
                print(f"   ℹ Short already recorded/published: {pub_url} ({pub_time})")
            else:
                short_meta = extract_metadata_fields(short_meta_md)
                short_slot_time = get_slot_for_asset(short_key, ledger, is_compilation=False)
                    
                if dry_run:
                    print(f"   [DRY-RUN] Would upload Short: '{short_meta['title']}' scheduled for {short_slot_time.strftime('%Y-%m-%d %I:%M %p %Z')}")
                    ledger.setdefault("published", {})[short_key] = {"publish_at_est": short_slot_time.isoformat()}
                else:
                    short_record = upload_video_asset(youtube, short_mp4, short_thumb_jpg, short_meta, short_slot_time, is_short=True)
                    ledger.setdefault("published", {})[short_key] = short_record
                    save_ledger(ledger)
                    pl_id = resolve_playlist_id(ep_name)
                    if pl_id:
                        add_video_to_playlist(youtube, short_record["video_id"], pl_id)
                    jlpt_pl_id = resolve_jlpt_playlist_id(short_meta["title"], ep_name)
                    if jlpt_pl_id and jlpt_pl_id != pl_id:
                        add_video_to_playlist(youtube, short_record["video_id"], jlpt_pl_id)

    if not dry_run:
        save_ledger(ledger)
    print("\n All operations completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TokyoFlow Automated YouTube Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate schedule allocation without making network calls")
    parser.add_argument("--episode", type=str, default=None, help="Filter specific episode (e.g. E01)")
    args = parser.parse_args()
    
    process_releases(dry_run=args.dry_run, episode_filter=args.episode)
