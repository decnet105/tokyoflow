#!/usr/bin/env python3
"""
TokyoFlow Japanese - Re-upload Chinese Shorts with First-Frame Master Covers
============================================================================
1. Re-renders all 11 Chinese Shorts with first-frame master cover injection.
2. Removes previous scheduled Shorts from YouTube (clean replacement).
3. Uploads newly rendered short.mp4 files with accurate schedule slots.
4. Adds new Shorts to Language Column Playlist and JLPT playlists.
5. Updates publish_ledger.json.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from youtube_auth import get_authenticated_service
from youtube_publisher import (
    load_ledger, save_ledger, upload_video_asset, extract_metadata_fields,
    get_or_create_language_playlist, add_video_to_playlist, resolve_playlist_id,
    resolve_jlpt_playlist_id, get_slot_for_asset, detect_release_locale, RELEASES_DIR
)
from build_all_chinese_shorts import generate_all_chinese_shorts

async def reupload_all_chinese_shorts():
    print("==================================================")
    print("Step 1: Re-rendering 11 Chinese Shorts with First-Frame Covers...")
    print("==================================================")
    await generate_all_chinese_shorts()

    print("\n==================================================")
    print("Step 2: Connecting to YouTube API & Replacing Shorts...")
    print("==================================================")
    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    ledger = load_ledger()

    zh_dirs = sorted([d for d in RELEASES_DIR.iterdir() if d.is_dir() and d.name.endswith("-zh")])

    for rel_dir in zh_dirs:
        ep_name = rel_dir.name
        short_key = f"{ep_name}_short"
        short_mp4 = rel_dir / "short.mp4"
        short_thumb_jpg = rel_dir / "short_thumbnail.jpg"
        short_meta_md = rel_dir / "short_metadata.md"

        if not (short_mp4.exists() and short_meta_md.exists()):
            continue

        # If previous short exists on YouTube, delete it to replace cleanly
        if short_key in ledger.get("published", {}):
            old_item = ledger["published"][short_key]
            old_id = old_item.get("video_id")
            if old_id:
                try:
                    print(f"\nDeleting old Short: {old_id} ({old_item.get('title', '')})...")
                    youtube.videos().delete(id=old_id).execute()
                    print(f"Deleted old Short: {old_id}")
                except Exception as e:
                    print(f"Notice: Could not delete old video {old_id}: {e}")

        # Extract metadata and schedule slot
        short_meta = extract_metadata_fields(short_meta_md)
        short_slot_time = get_slot_for_asset(short_key, ledger, locale="zh", is_compilation=False)

        print(f"\nUploading New Short for {ep_name} with First-Frame Cover (08:00 PM EST, notifySubscribers=False)...")
        short_record = upload_video_asset(
            youtube, short_mp4, short_thumb_jpg, short_meta, short_slot_time, is_short=True, notify_subscribers=False
        )
        ledger.setdefault("published", {})[short_key] = short_record
        save_ledger(ledger)

        locale_code = detect_release_locale(ep_name, short_meta)
        # 1. Add to dedicated Language Shorts Column Playlist (专栏 B Shorts)
        lang_pl_id = get_or_create_language_playlist(youtube, locale_code, is_short=True, ledger=ledger)
        if lang_pl_id:
            add_video_to_playlist(youtube, short_record["video_id"], lang_pl_id)

        # 2. Add to Scenario Topic Playlist
        pl_id = resolve_playlist_id(ep_name)
        if pl_id:
            add_video_to_playlist(youtube, short_record["video_id"], pl_id)

        # 3. Add to JLPT Level Playlist
        jlpt_pl_id = resolve_jlpt_playlist_id(short_meta["title"], ep_name)
        if jlpt_pl_id and jlpt_pl_id != pl_id:
            add_video_to_playlist(youtube, short_record["video_id"], jlpt_pl_id)

    save_ledger(ledger)
    print("\n==================================================")
    print("ALL 11 CHINESE SHORTS RE-UPLOADED WITH FIRST-FRAME COVERS!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(reupload_all_chinese_shorts())
