#!/usr/bin/env python3
"""
TokyoFlow Japanese • Re-upload WL.02 with Seamless Bilingual In-Line Audio
=========================================================================
Deletes previous WL.02 video and uploads the newly generated master video
featuring the Seamless In-line Bilingual Audio Engine (Nanami JA + Yunxi ZH).
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

OLD_WL02_ID = "owPAbQVhGE0"

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
    print(" TOKYOFLOW JAPANESE: Re-upload WL.02 Seamless Bilingual Masterclass")
    print("================================================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)

    # 1. Delete old WL.02 video
    print(f"[*] Deleting previous WL.02 video ({OLD_WL02_ID})...")
    try:
        youtube.videos().delete(id=OLD_WL02_ID).execute()
        print(f"  [OK] Successfully deleted old video: {OLD_WL02_ID}")
    except Exception as e:
        print(f"  [WARN] Delete warning: {e}")
    time.sleep(1.5)

    # 2. Upload new video
    wm_dir = PROJECT_ROOT / "docs/youtube_releases/WM01-weekday_survival_mega_compilation-v1.0-zh"
    video_path = wm_dir / "video.mp4"
    thumb_path = wm_dir / "thumbnail.jpg"
    wm_title, wm_desc = parse_metadata_file(wm_dir / "metadata.md")

    print(f"[*] Uploading New WL.02 Master Video: {video_path.name} ({video_path.stat().st_size / (1024*1024):.1f} MB)...")
    body = {
        "snippet": {
            "title": wm_title[:100],
            "description": wm_desc,
            "tags": [
                "日语学习", "东京生活", "日本旅游日语", "JLPT N5", "JLPT N4", "JLPT N3",
                "山手线", "便利店日语", "居酒屋日语", "拉面定制", "温泉礼仪", "日本文化",
                "TokyoFlow", "日语听力", "日语口语"
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
    print(f"  [OK] WL.02 Uploaded Successfully! New ID: {new_id} -> {video_url}")

    # Set Custom 4K Thumbnail
    if thumb_path.exists():
        print(f"    Uploading Custom Thumbnail: {thumb_path.name}...")
        try:
            time.sleep(1.5)
            youtube.thumbnails().set(
                videoId=new_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Custom Thumbnail applied successfully.")
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
        "WM01-weekday_survival_mega_compilation-v1.0-zh_video": {
            "video_id": new_id,
            "video_url": video_url,
            "title": wm_title,
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
            data["published"].update(new_record)
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  [OK] Updated ledger: {ledger_path}")

    # 4. Update website build script
    build_script = PROJECT_ROOT / "scripts/build_website.py"
    build_content = build_script.read_text(encoding="utf-8")
    build_content = build_content.replace(f'"yt_url_zh": "https://youtu.be/{OLD_WL02_ID}"', f'"yt_url_zh": "{video_url}"')
    build_content = build_content.replace(f'"yt_id_zh": "{OLD_WL02_ID}"', f'"yt_id_zh": "{new_id}"')
    build_script.write_text(build_content, encoding="utf-8")
    print(f"  [OK] Updated website script: {build_script}")

    print("\n================================================================================")
    print(f" WL.02 Seamless Bilingual Masterclass Live: {new_id} -> {video_url}")
    print("================================================================================")

if __name__ == "__main__":
    main()
