#!/usr/bin/env python3
"""
TokyoFlow Japanese - YouTube Master Thumbnail Batch Deployment Tool
===================================================================
Connects to YouTube Data API v3 and updates custom thumbnails for all published videos in publish_ledger.json.
"""

import os
import sys
import json
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
LEDGER_FILE = RELEASES_DIR / "publish_ledger.json"

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

def upload_all_thumbnails():
    print("================================================================================")
    print("TokyoFlow YouTube Master Thumbnail Deployment")
    print("================================================================================")
    
    if not LEDGER_FILE.exists():
        print(f"Error: Ledger file not found at {LEDGER_FILE}")
        return

    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    
    success_count = 0
    fail_count = 0
    
    published_items = ledger.get("published", {})
    total_targets = len(published_items)
    print(f"Found {total_targets} published items in ledger.")

    for key, item in published_items.items():
        vid = item.get("video_id")
        title = item.get("title", key)
        is_short = item.get("is_short", False) or "_short" in key
        
        # Derive folder name from key (e.g. E01-Yamanote_Transit-v1.0-zh_video -> E01-Yamanote_Transit-v1.0-zh)
        folder_name = key.replace("_video", "").replace("_short", "")
        thumb_filename = "short_thumbnail.jpg" if is_short else "thumbnail.jpg"
        
        thumb_path = RELEASES_DIR / folder_name / thumb_filename
        if not thumb_path.exists():
            # Fallback to thumbnail.jpg if short_thumbnail missing
            thumb_path = RELEASES_DIR / folder_name / "thumbnail.jpg"

        if not thumb_path.exists() or not vid:
            print(f"Skipping {key}: Missing file ({thumb_path}) or video ID.")
            continue
            
        print(f"\nUploading Master Thumbnail for: {title}")
        print(f"   Video ID: {vid} | File: {thumb_path.name} ({thumb_path.stat().st_size/1024:.1f} KB)")
        
        try:
            media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg", resumable=True)
            req = youtube.thumbnails().set(
                videoId=vid,
                media_body=media
            )
            resp = req.execute()
            print(f"   Successfully applied custom thumbnail: https://youtu.be/{vid}")
            success_count += 1
            time.sleep(1.0)
        except Exception as e:
            print(f"   YouTube API Error for {vid}: {e}")
            fail_count += 1
            
    print("\n================================================================================")
    print(f"Deployment Finished! Successfully Updated: {success_count}/{total_targets} Thumbnails. Errors: {fail_count}")
    print("================================================================================")

if __name__ == "__main__":
    upload_all_thumbnails()
