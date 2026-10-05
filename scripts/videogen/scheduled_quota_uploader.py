#!/usr/bin/env python3
"""
TokyoFlow Japanese • Scheduled Quota-Aware YouTube Uploader
===========================================================
Handles queued releases when daily YouTube Data API quota is exhausted.
Automatically triggers scheduled upload at 03:30 AM EDT upon quota reset:

1. Scans all unuploaded release packages in docs/youtube_releases/.
2. Verifies publish dates and publication parameters:
   - English releases: 08:00 AM EDT (notifySubscribers = True)
   - Chinese releases: 08:00 PM EDT (notifySubscribers = False)
3. Uploads videos, sets scheduled publish times, sets custom thumbnails, and routes to playlists.
"""

import os
import sys
import time
import argparse
from datetime import datetime, timedelta
import zoneinfo
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_publisher import process_releases
from update_youtube_metadata_and_covers import update_all_youtube_releases

EST_TZ = zoneinfo.ZoneInfo("America/New_York")

def wait_until_target_time(target_hour: int = 3, target_minute: int = 30):
    """Waits until the next specified EDT time (e.g. 03:30 AM EDT)."""
    now = datetime.now(EST_TZ)
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    
    wait_seconds = (target - now).total_seconds()
    print(f"Current Time (EDT): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Target Upload Time: {target.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Sleeping for {wait_seconds:.0f} seconds ({wait_seconds / 3600:.2f} hours)...")
    time.sleep(wait_seconds)

def main():
    parser = argparse.ArgumentParser(description="TokyoFlow Scheduled Quota-Aware YouTube Uploader")
    parser.add_argument("--wait", action="store_true", help="Wait until 03:30 AM EDT before starting upload")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without network upload")
    parser.add_argument("--target-hour", type=int, default=3, help="Target hour EDT (default: 3)")
    parser.add_argument("--target-minute", type=int, default=30, help="Target minute EDT (default: 30)")
    args = parser.parse_args()

    print("================================================================================")
    print("TokyoFlow YouTube • Scheduled Quota-Aware Uploader")
    print("Zero Emoji Discipline | Automated Scheduled Publishing Engine")
    print("================================================================================\n")

    if args.wait:
        wait_until_target_time(args.target_hour, args.target_minute)

    print("Starting YouTube Metadata & Cover Sync Process...")
    try:
        update_all_youtube_releases()
    except Exception as e:
        print(f"Metadata sync encountered: {e}")

    print("\nStarting YouTube Upload Process...")
    process_releases(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
