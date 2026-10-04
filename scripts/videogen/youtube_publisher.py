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
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
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

    title = ""
    description = ""

    # 1. Extract Title
    # Pattern A: in code block under header
    title_match = re.search(r"##\s*(?:YouTube\s+)?(?:Video|Shorts?|Master|中文)?[^\n]*(?:Title|标题)[^\n]*\n+```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        # Pattern B: plain line under header
        plain_title_match = re.search(r"##\s*(?:YouTube\s+)?(?:Video|Shorts?|Master|中文)?[^\n]*(?:Title|标题)[^\n]*\n+([^\n#]+)", content, re.IGNORECASE)
        if plain_title_match:
            title = plain_title_match.group(1).strip()
        else:
            # Pattern C: Top H1 Header
            h1_match = re.search(r"^#\s*([^\n]+)", content)
            if h1_match:
                title = h1_match.group(1).strip()
            elif kit_data:
                is_short_file = "short" in md_path.name.lower()
                if is_short_file and "shorts_package" in kit_data:
                    title = kit_data["shorts_package"].get("title", "")
                elif "long_form_package" in kit_data:
                    title = kit_data["long_form_package"].get("title", "")
            else:
                # Pattern D: Read script.json in parent directory
                script_file = md_path.parent / "script.json"
                if script_file.exists():
                    try:
                        s_data = json.loads(script_file.read_text(encoding="utf-8"))
                        title = s_data.get("yt_title", s_data.get("title", ""))
                    except Exception:
                        pass
    
    # 2. Extract Description
    # Pattern A: in code block
    desc_match = re.search(r"##\s*(?:YouTube\s+)?(?:Shorts?|Video|Master|中文)?[^\n]*(?:Description|简介)[^\n]*\n+```[a-zA-Z]*\n(.*?)\n```", content, re.DOTALL | re.IGNORECASE)
    if desc_match:
        description = desc_match.group(1).strip()
    else:
        # Pattern B: plain text until next section
        plain_desc_match = re.search(r"##\s*(?:YouTube\s+)?(?:Shorts?|Video|Master|中文)?[^\n]*(?:Description|简介)[^\n]*\n+(.*?)(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
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

def generate_next_slots(start_from_dt: datetime, count: int = 30, locale: str = "en") -> list:
    """
    Generates chronological EST schedule slots adhering to the Multi-Language Publishing Rules:
    - English Edition (en): 08:00 AM EST (Weekdays)
    - Chinese Edition (zh): 08:00 PM EST (20:00 EST, Weekdays)
    - Compilations: 05:00 PM EST (Weekends)
    """
    slots = []
    current_date = start_from_dt.date()
    
    while len(slots) < count:
        weekday = current_date.weekday() # 0 = Monday, 6 = Sunday
        if weekday in range(0, 5): # Mon - Fri
            if locale == "zh":
                t_zh = datetime(current_date.year, current_date.month, current_date.day, 20, 0, 0, tzinfo=EST_TZ)
                if t_zh > start_from_dt:
                    slots.append({"time_est": t_zh, "slot_type": "weekday_evening_zh", "allows_compilation": False})
            else:
                t1 = datetime(current_date.year, current_date.month, current_date.day, 8, 0, 0, tzinfo=EST_TZ)
                if t1 > start_from_dt:
                    slots.append({"time_est": t1, "slot_type": "weekday_morning_en", "allows_compilation": False})
        else: # Saturday (5) or Sunday (6)
            t_weekend = datetime(current_date.year, current_date.month, current_date.day, 17, 0, 0, tzinfo=EST_TZ)
            if t_weekend > start_from_dt:
                slots.append({"time_est": t_weekend, "slot_type": "weekend_evening", "allows_compilation": True})
        current_date += timedelta(days=1)
        
    return slots

def get_next_available_slot(ledger: dict, locale: str = "en", is_compilation: bool = False, min_hours_ahead: int = 2) -> datetime:
    """Finds the next unreserved publishing slot in EST for the given locale."""
    now_est = datetime.now(EST_TZ) + timedelta(hours=min_hours_ahead)
    reserved_times = {
        item["publish_at_est"] for item in ledger.get("published", {}).values() if "publish_at_est" in item
    }
    
    candidate_slots = generate_next_slots(now_est, count=60, locale=locale)
    for slot in candidate_slots:
        iso_str = slot["time_est"].isoformat()
        if is_compilation and not slot["allows_compilation"]:
            continue
        if not is_compilation and slot["allows_compilation"]:
            continue
        if iso_str not in reserved_times:
            return slot["time_est"]
            
    # Fallback
    return candidate_slots[0]["time_est"]

def upload_video_asset(youtube, video_path: Path, thumbnail_path: Path, meta: dict, publish_at: datetime, is_short: bool = False, notify_subscribers: bool = True):
    """Uploads a video to YouTube with scheduled publication (publishAt), notifySubscribers control, and custom thumbnail."""
    print(f"\n Preparing upload for: {meta['title']}")
    print(f" Video file: {video_path} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
    print(f" Scheduled Publish Time: {publish_at.strftime('%Y-%m-%d %I:%M %p %Z')} ({publish_at.isoformat()})")
    print(f" Notify Subscribers: {notify_subscribers}")
    
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
        media_body=media,
        notifySubscribers=notify_subscribers
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   Upload Progress: {int(status.progress() * 100)}%")
            
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
        "is_short": is_short,
        "notify_subscribers": notify_subscribers
    }
# Multi-Edition Language Column Playlists (专栏 A: 英文, 专栏 B: 中文, 专栏 C: 韩文...)
LANGUAGE_COLUMN_PLAYLISTS = {
    "en": {
        "name": "专栏 A（全球英文入口）",
        "long_title": "TokyoFlow Japanese Masterclass [English Edition]",
        "long_desc": "Master natural Tokyo Japanese through real-life scenarios, JLPT breakdowns, and native shadowing drills (English Explanations).",
        "short_title": "TokyoFlow Japanese Shorts [English Edition]",
        "short_desc": "Quick 60-second native Tokyo Japanese shadowing & pitch accent drills."
    },
    "zh": {
        "name": "专栏 B（中文用户入口）",
        "long_title": "TokyoFlow 日语实景精讲【中文解说版】",
        "long_desc": "东京真实生活场景沉浸式精讲，从山手线报站到居酒屋点单，轻松掌握 JLPT 核心词汇与地道口语（中文名师深度拆解）。",
        "short_title": "TokyoFlow 日语短视频跟读【中文解说版】",
        "short_desc": "每日 60 秒东京原声跟读挑战与声调发音打分练习。"
    },
    "ko": {
        "name": "专栏 C（韩语用户入口）",
        "long_title": "TokyoFlow 일본어 실전 마스터클래스 [한국어 해설판]",
        "long_desc": "도쿄 현지 실전 일본어 및 JLPT 핵심 문법 심층 해설 강의.",
        "short_title": "TokyoFlow 일본어 숏폼 쉐도잉 [한국어판]",
        "short_desc": "매일 60초 도쿄 원어민 쉐도잉 및 억양 트레이닝."
    }
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

def detect_release_locale(ep_name: str, meta: dict = None) -> str:
    """Detects locale code from release folder name or metadata."""
    if "-zh" in ep_name.lower() or "_zh" in ep_name.lower():
        return "zh"
    if "-ko" in ep_name.lower() or "_ko" in ep_name.lower():
        return "ko"
    if meta and "语言版本" in meta.get("description", ""):
        desc = meta.get("description", "")
        if "Chinese" in desc or "中文" in desc or "(zh)" in desc:
            return "zh"
        if "Korean" in desc or "韩语" in desc or "(ko)" in desc:
            return "ko"
    return "en"

def get_or_create_language_playlist(youtube, locale_code: str, is_short: bool = False, ledger: dict = None) -> str:
    """Fetches or automatically creates dedicated Language Column Playlist on YouTube."""
    if not youtube:
        return None

    col_cfg = LANGUAGE_COLUMN_PLAYLISTS.get(locale_code, LANGUAGE_COLUMN_PLAYLISTS["en"])
    target_title = col_cfg["short_title"] if is_short else col_cfg["long_title"]
    target_desc = col_cfg["short_desc"] if is_short else col_cfg["long_desc"]

    cache_key = f"playlist_{locale_code}_{'short' if is_short else 'long'}"
    if ledger and "playlists" in ledger and cache_key in ledger["playlists"]:
        return ledger["playlists"][cache_key]

    try:
        req = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
        resp = req.execute()
        for item in resp.get("items", []):
            if item["snippet"]["title"].strip().lower() == target_title.strip().lower():
                pl_id = item["id"]
                if ledger is not None:
                    ledger.setdefault("playlists", {})[cache_key] = pl_id
                    save_ledger(ledger)
                return pl_id

        # If not found, auto-create it
        print(f"✨ Auto-Creating Channel Column Playlist: '{target_title}'...")
        create_req = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": target_title,
                    "description": target_desc,
                    "defaultLanguage": "zh" if locale_code == "zh" else "en"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        )
        created_resp = create_req.execute()
        pl_id = created_resp["id"]
        print(f"🎉 Created Language Column Playlist: {target_title} (ID: {pl_id})")
        if ledger is not None:
            ledger.setdefault("playlists", {})[cache_key] = pl_id
            save_ledger(ledger)
        return pl_id
    except Exception as e:
        print(f" Notice: Language playlist get/create: {e}")
        return None

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
    
    # 2026-10-03 (Sat) Weekend Japanese Cinema Masterclass WL.01 Launch (5:00 PM EST)
    "WL01-last-mile-masterclass-v1.0_video": datetime(2026, 10, 3, 17, 0, 0, tzinfo=EST_TZ),
    "WL01-last-mile-masterclass-v1.0_short": datetime(2026, 10, 3, 17, 0, 0, tzinfo=EST_TZ),
    
    # 2026-10-04 (Sun) Sunday Mega-Compilation WM.01 Launch (5:00 PM EST)
    "WM01-weekday_survival_mega_compilation-v1.0_video": datetime(2026, 10, 4, 17, 0, 0, tzinfo=EST_TZ),
    "WM01-weekday_survival_mega_compilation-v1.0_short": datetime(2026, 10, 4, 17, 0, 0, tzinfo=EST_TZ),

    # 2026-10-08 (Thu) EP.12 Docomo Bike & LUUP
    "E12-Docomo_Bike_LUUP-v1.0_video": datetime(2026, 10, 8, 8, 0, 0, tzinfo=EST_TZ),
    "E12-Docomo_Bike_LUUP-v1.0_short": datetime(2026, 10, 8, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-09 (Fri) EP.13 Gyudon Customization
    "E13-Gyudon_Customization-v1.0_video": datetime(2026, 10, 9, 8, 0, 0, tzinfo=EST_TZ),
    "E13-Gyudon_Customization-v1.0_short": datetime(2026, 10, 9, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-12 (Mon) EP.14 Japan Post Redelivery
    "E14-JapanPost_Redelivery-v1.0_video": datetime(2026, 10, 12, 8, 0, 0, tzinfo=EST_TZ),
    "E14-JapanPost_Redelivery-v1.0_short": datetime(2026, 10, 12, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-13 (Tue) EP.15 Supermarket Half-Price Rush
    "E15-Supermarket_HalfPrice_Rush-v1.0_video": datetime(2026, 10, 13, 8, 0, 0, tzinfo=EST_TZ),
    "E15-Supermarket_HalfPrice_Rush-v1.0_short": datetime(2026, 10, 13, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-14 (Wed) EP.16 Drugstore Medicine
    "E16-Drugstore_Medicine-v1.0_video": datetime(2026, 10, 14, 8, 0, 0, tzinfo=EST_TZ),
    "E16-Drugstore_Medicine-v1.0_short": datetime(2026, 10, 14, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-15 (Thu) EP.17 Onsen & Sento Etiquette
    "E17-Onsen_Sento_Etiquette-v1.0_video": datetime(2026, 10, 15, 8, 0, 0, tzinfo=EST_TZ),
    "E17-Onsen_Sento_Etiquette-v1.0_short": datetime(2026, 10, 15, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-16 (Fri) EP.18 Tokyo Cafe Ordering
    "E18-Tokyo_Cafe_Ordering-v1.0_video": datetime(2026, 10, 16, 8, 0, 0, tzinfo=EST_TZ),
    "E18-Tokyo_Cafe_Ordering-v1.0_short": datetime(2026, 10, 16, 8, 0, 0, tzinfo=EST_TZ),

    # 2026-10-19 (Mon) EP.19 Shinkansen Bullet Train Tickets
    "E19-Shinkansen_BulletTrain_Tickets-v1.0_video": datetime(2026, 10, 19, 8, 0, 0, tzinfo=EST_TZ),
    "E19-Shinkansen_BulletTrain_Tickets-v1.0_short": datetime(2026, 10, 19, 8, 0, 0, tzinfo=EST_TZ),
}

def get_slot_for_asset(asset_key: str, ledger: dict, locale: str = "en", is_compilation: bool = False, release_dir: Path = None) -> datetime:
    """Returns the explicit slot if configured, otherwise computes next available slot for the target locale."""
    if asset_key in EXPLICIT_SCHEDULE_PLAN:
        return EXPLICIT_SCHEDULE_PLAN[asset_key]
    
    # Check if youtube_schedule_kit.json exists in release folder
    if release_dir:
        kit_file = release_dir / "youtube_schedule_kit.json"
        if kit_file.exists():
            try:
                kit_data = json.loads(kit_file.read_text(encoding="utf-8"))
                if "scheduled_time_est" in kit_data:
                    return datetime.fromisoformat(kit_data["scheduled_time_est"])
            except Exception:
                pass

    return get_next_available_slot(ledger, locale=locale, is_compilation=is_compilation)

def process_releases(dry_run: bool = False, episode_filter: str = None):
    """Scans all episode release folders and executes scheduled upload."""
    ledger = load_ledger()
    creds = None if dry_run else get_authenticated_service()
    youtube = None if dry_run else build("youtube", "v3", credentials=creds)
    
    release_dirs = sorted([d for d in RELEASES_DIR.iterdir() if d.is_dir() and (d.name.startswith("E") or d.name.startswith("WL") or d.name.startswith("WM"))])
    
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
                print(f"   Micro-lesson already recorded/published: {pub_url} ({pub_time})")
            else:
                meta = extract_metadata_fields(meta_md)
                locale_code = detect_release_locale(ep_name, meta)
                notify_subs = (locale_code == "en")
                slot_time = get_slot_for_asset(long_key, ledger, locale=locale_code, is_compilation=False, release_dir=rel_dir)
                
                if dry_run:
                    print(f"   [DRY-RUN] Would upload Micro-lesson ({locale_code}): '{meta['title']}' scheduled for {slot_time.strftime('%Y-%m-%d %I:%M %p %Z')} (notify_subscribers={notify_subs})")
                    ledger.setdefault("published", {})[long_key] = {"publish_at_est": slot_time.isoformat()}
                else:
                    record = upload_video_asset(youtube, video_mp4, thumb_jpg, meta, slot_time, is_short=False, notify_subscribers=notify_subs)
                    ledger.setdefault("published", {})[long_key] = record
                    save_ledger(ledger)
                    
                    # 1. Add to dedicated Language Column Playlist
                    lang_pl_id = get_or_create_language_playlist(youtube, locale_code, is_short=False, ledger=ledger)
                    if lang_pl_id:
                        add_video_to_playlist(youtube, record["video_id"], lang_pl_id)
                        
                    # 2. English-only secondary playlists (keep Chinese strictly in Chinese playlists)
                    if locale_code == "en":
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
                print(f"   Short already recorded/published: {pub_url} ({pub_time})")
            else:
                short_meta = extract_metadata_fields(short_meta_md)
                short_locale_code = detect_release_locale(ep_name, short_meta)
                short_notify_subs = (short_locale_code == "en")
                short_slot_time = get_slot_for_asset(short_key, ledger, locale=short_locale_code, is_compilation=False, release_dir=rel_dir)
                    
                if dry_run:
                    print(f"   [DRY-RUN] Would upload Short ({short_locale_code}): '{short_meta['title']}' scheduled for {short_slot_time.strftime('%Y-%m-%d %I:%M %p %Z')} (notify_subscribers={short_notify_subs})")
                    ledger.setdefault("published", {})[short_key] = {"publish_at_est": short_slot_time.isoformat()}
                else:
                    short_record = upload_video_asset(youtube, short_mp4, short_thumb_jpg, short_meta, short_slot_time, is_short=True, notify_subscribers=short_notify_subs)
                    ledger.setdefault("published", {})[short_key] = short_record
                    save_ledger(ledger)
                    
                    # 1. Add to dedicated Language Shorts Column Playlist
                    lang_pl_id = get_or_create_language_playlist(youtube, short_locale_code, is_short=True, ledger=ledger)
                    if lang_pl_id:
                        add_video_to_playlist(youtube, short_record["video_id"], lang_pl_id)
                        
                    # 2. English-only secondary playlists
                    if short_locale_code == "en":
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
