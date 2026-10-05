#!/usr/bin/env python3
"""
TokyoFlow Japanese • Re-upload WL.01 with Millisecond Karaoke & Full Audio
==========================================================================
Deletes previous WL.01 video and uploads the newly generated master video
featuring Whisper millisecond-precision karaoke and continuous two-stage practice audio.
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from datetime import datetime
import zoneinfo
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

EST_TZ = zoneinfo.ZoneInfo("America/New_York")

OLD_WL01_ID = "Gk-tcCnryuM"

def parse_metadata_file(md_path: Path):
    content = md_path.read_text(encoding="utf-8")
    parts = content.split("```")
    if len(parts) >= 4:
        title = parts[1].strip()
        description = parts[3].strip()
        return title, description
    raise ValueError(f"Could not parse code blocks in {md_path}")

def main():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: Re-upload WL.01 Millisecond Karaoke Cinema Masterclass")
    print("================================================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)

    # 1. Delete old WL.01 video
    print(f"[*] Deleting previous WL.01 video ({OLD_WL01_ID})...")
    try:
        youtube.videos().delete(id=OLD_WL01_ID).execute()
        print(f"  [OK] Successfully deleted old video: {OLD_WL01_ID}")
    except Exception as e:
        print(f"  [WARN] Delete warning: {e}")
    time.sleep(1.5)

    # 2. Upload new video
    wl01_dir = PROJECT_ROOT / "docs/youtube_releases/WL01-last-mile-masterclass-v1.0-zh"
    video_path = wl01_dir / "video.mp4"
    thumb_path = wl01_dir / "thumbnail.jpg"
    wl_title, wl_desc = parse_metadata_file(wl01_dir / "metadata.md")

    print(f"[*] Uploading New WL.01 Master Video: {video_path.name} ({video_path.stat().st_size / (1024*1024):.1f} MB)...")
    body = {
        "snippet": {
            "title": wl_title[:100],
            "description": wl_desc,
            "tags": [
                "最后的里程", "ラストマイル", "满岛光", "冈田将生", "日语学习",
                "JLPT N3", "JLPT N2", "日语听力", "日语口语", "日本电影",
                "TokyoFlow", "冢原亚由子", "野木亚纪子"
            ],
            "categoryId": "27",
            "defaultLanguage": "zh",
            "defaultAudioLanguage": "ja"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        str(video_path),
        chunksize=8 * 1024 * 1024,
        resumable=True,
        mimetype="video/mp4"
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
        notifySubscribers=False
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Upload Progress: {int(status.progress() * 100)}%")

    new_id = response.get("id")
    video_url = f"https://youtu.be/{new_id}"
    print(f"  [OK] WL.01 Uploaded Successfully! New ID: {new_id} -> {video_url}")

    # Set Custom 4K Thumbnail
    if thumb_path.exists():
        print(f"    Uploading Custom 4K Thumbnail: {thumb_path.name}...")
        try:
            time.sleep(1.5)
            youtube.thumbnails().set(
                videoId=new_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Custom 4K Mitsushima Hikari Thumbnail applied successfully.")
        except Exception as e:
            print(f"  [WARN] Thumbnail upload error: {e}")

    # Add to Chinese Long-form Playlist
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": "PLVchR4TmK56E",
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": new_id
                    }
                }
            }
        ).execute()
        print(f"  [OK] Added {new_id} to playlist PLVchR4TmK56E")
    except Exception as e:
        print(f"  [WARN] Playlist addition warning: {e}")

    # 3. Update ledger files
    new_record = {
        "WL01-last-mile-masterclass-v1.0-zh_video": {
            "video_id": new_id,
            "video_url": video_url,
            "title": wl_title,
            "uploaded_at": datetime.now(EST_TZ).isoformat(),
            "is_short": False,
            "notify_subscribers": False
        }
    }

    for ledger_path in [
        PROJECT_ROOT / "docs/shared/publish_ledger.json",
        PROJECT_ROOT / "docs/youtube_releases/publish_ledger.json"
    ]:
        if ledger_path.exists():
            with open(ledger_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.update(new_record)
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [OK] Updated ledger: {ledger_path}")

    # 4. Update scripts/build_website.py
    site_script = PROJECT_ROOT / "scripts/build_website.py"
    if site_script.exists():
        site_content = site_script.read_text(encoding="utf-8")
        # Replace old WL01 id
        site_content = re.sub(r'Gk-tcCnryuM', new_id, site_content)
        site_script.write_text(site_content, encoding="utf-8")
        print(f"  [OK] Updated website script: {site_script}")

    print("\n================================================================================")
    print(f" WL.01 Millisecond Karaoke Cinema Masterclass Live: {new_id} -> {video_url}")
    print("================================================================================\n")

if __name__ == "__main__":
    main()
