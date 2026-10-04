#!/usr/bin/env python3
"""
TokyoFlow Japanese - Realign Chinese Releases to 08:00 PM EST (Zero Subscriber Notification)
=============================================================================================
Re-aligns both 16:9 micro-lessons and 9:16 Shorts for all Chinese releases (EP.01 ~ EP.11):
- Scheduled Release Time: 08:00 PM EST (20:00 EST)
- Subscriber Notification: notifySubscribers = False
- Cleanly replaces old scheduled items on YouTube and updates playlists and ledger.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from youtube_auth import get_authenticated_service
from youtube_publisher import (
    load_ledger, save_ledger, upload_video_asset, extract_metadata_fields,
    get_or_create_language_playlist, add_video_to_playlist, resolve_playlist_id,
    resolve_jlpt_playlist_id, get_slot_for_asset, detect_release_locale, RELEASES_DIR,
    EST_TZ
)

def realign_all_chinese_releases():
    print("==================================================")
    print("Realigning All Chinese Releases (EP.01 ~ EP.11)")
    print("Schedule: 08:00 PM EST (20:00 EST) | notifySubscribers: False")
    print("==================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    ledger = load_ledger()

    zh_dirs = sorted([d for d in RELEASES_DIR.iterdir() if d.is_dir() and d.name.endswith("-zh")])

    for rel_dir in zh_dirs:
        ep_name = rel_dir.name
        print(f"\n--------------------------------------------------")
        print(f"Processing Chinese Release: {ep_name}")
        print(f"--------------------------------------------------")

        # 1. Process 16:9 Micro-Lesson
        video_mp4 = rel_dir / "video.mp4"
        thumb_jpg = rel_dir / "thumbnail.jpg"
        meta_md = rel_dir / "metadata.md"
        long_key = f"{ep_name}_video"

        if video_mp4.exists() and meta_md.exists():
            # Delete old video on YouTube if already in ledger
            if long_key in ledger.get("published", {}):
                old_id = ledger["published"][long_key].get("video_id")
                if old_id:
                    try:
                        print(f"Deleting old 16:9 Micro-Lesson: {old_id}...")
                        youtube.videos().delete(id=old_id).execute()
                        print(f"Deleted old 16:9 Micro-Lesson: {old_id}")
                    except Exception as e:
                        print(f"Notice: Could not delete {old_id}: {e}")

            meta = extract_metadata_fields(meta_md)
            slot_time = get_slot_for_asset(long_key, ledger, locale="zh", is_compilation=False)
            
            print(f"Uploading New 16:9 Micro-Lesson for {ep_name} (20:00 EST, notifySubscribers=False)...")
            record = upload_video_asset(
                youtube, video_mp4, thumb_jpg, meta, slot_time, is_short=False, notify_subscribers=False
            )
            ledger.setdefault("published", {})[long_key] = record
            save_ledger(ledger)

            # Playlist routing
            lang_pl_id = get_or_create_language_playlist(youtube, "zh", is_short=False, ledger=ledger)
            if lang_pl_id:
                add_video_to_playlist(youtube, record["video_id"], lang_pl_id)

            pl_id = resolve_playlist_id(ep_name)
            if pl_id:
                add_video_to_playlist(youtube, record["video_id"], pl_id)

            jlpt_pl_id = resolve_jlpt_playlist_id(meta["title"], ep_name)
            if jlpt_pl_id and jlpt_pl_id != pl_id:
                add_video_to_playlist(youtube, record["video_id"], jlpt_pl_id)

        # 2. Process 9:16 Short (with First-Frame Cover)
        short_mp4 = rel_dir / "short.mp4"
        short_thumb_jpg = rel_dir / "short_thumbnail.jpg"
        short_meta_md = rel_dir / "short_metadata.md"
        short_key = f"{ep_name}_short"

        if short_mp4.exists() and short_meta_md.exists():
            # Delete old Short on YouTube if already in ledger
            if short_key in ledger.get("published", {}):
                old_id = ledger["published"][short_key].get("video_id")
                if old_id:
                    try:
                        print(f"Deleting old Short: {old_id}...")
                        youtube.videos().delete(id=old_id).execute()
                        print(f"Deleted old Short: {old_id}")
                    except Exception as e:
                        print(f"Notice: Could not delete {old_id}: {e}")

            short_meta = extract_metadata_fields(short_meta_md)
            short_slot_time = get_slot_for_asset(short_key, ledger, locale="zh", is_compilation=False)

            print(f"Uploading New 9:16 Short for {ep_name} (20:00 EST, notifySubscribers=False)...")
            short_record = upload_video_asset(
                youtube, short_mp4, short_thumb_jpg, short_meta, short_slot_time, is_short=True, notify_subscribers=False
            )
            ledger.setdefault("published", {})[short_key] = short_record
            save_ledger(ledger)

            # Playlist routing
            lang_pl_id = get_or_create_language_playlist(youtube, "zh", is_short=True, ledger=ledger)
            if lang_pl_id:
                add_video_to_playlist(youtube, short_record["video_id"], lang_pl_id)

            pl_id = resolve_playlist_id(ep_name)
            if pl_id:
                add_video_to_playlist(youtube, short_record["video_id"], pl_id)

            jlpt_pl_id = resolve_jlpt_playlist_id(short_meta["title"], ep_name)
            if jlpt_pl_id and jlpt_pl_id != pl_id:
                add_video_to_playlist(youtube, short_record["video_id"], jlpt_pl_id)

    save_ledger(ledger)
    print("\n==================================================")
    print("ALL CHINESE RELEASES REALIGNED TO 08:00 PM EST (notifySubscribers=False)!")
    print("==================================================")

if __name__ == "__main__":
    realign_all_chinese_releases()
