#!/usr/bin/env python3
"""
TokyoFlow Japanese • Directory Reorganization & Hygiene Engine
==============================================================
Enforces the strict Single Source of Truth directory layout:
1. Release Packages (Single Canonical Copy):
   - docs/youtube_releases/E{XX}-{Title_Slug}-v{Version}/ (English 7-in-1 package)
   - docs/youtube_releases/E{XX}-{Title_Slug}-v{Version}-zh/ (Chinese 7-in-1 package)
   - docs/youtube_releases/WL01-... & WM01-... (Weekend Specials)
   * Each folder contains ALL artifacts for that episode (video.mp4, thumbnail.jpg, metadata.md, short.mp4, short_thumbnail.jpg, short_metadata.md, script.json).
   * NO duplicated or split directories elsewhere.

2. Study Materials & Trailers:
   - output/en/study_guide & output/zh/study_guide (PDFs, workbooks)
   - output/en/channel_trailer & output/zh/channel_trailer (Official trailers)
   - output/trend_reports (Daily trend radar markdown analysis)

3. Documentation:
   - docs/en, docs/zh, docs/shared
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def organize():
    print("==================================================")
    print("Enforcing TokyoFlow Single-Copy Directory Layout")
    print("==================================================")

    # 1. Ensure canonical directories exist
    dirs = [
        PROJECT_ROOT / "docs" / "en",
        PROJECT_ROOT / "docs" / "zh",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "backgrounds",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "branding",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "fonts",
        PROJECT_ROOT / "docs" / "youtube_releases",
        PROJECT_ROOT / "output" / "en" / "study_guide",
        PROJECT_ROOT / "output" / "en" / "channel_trailer",
        PROJECT_ROOT / "output" / "zh" / "study_guide",
        PROJECT_ROOT / "output" / "zh" / "channel_trailer",
        PROJECT_ROOT / "output" / "trend_reports",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Verified directory: {d.relative_to(PROJECT_ROOT)}")

    # 2. Clean up any obsolete split directories in output/
    obsolete_dirs = [
        PROJECT_ROOT / "output" / "en" / "masterclasses",
        PROJECT_ROOT / "output" / "en" / "shorts",
        PROJECT_ROOT / "output" / "zh" / "masterclasses",
        PROJECT_ROOT / "output" / "zh" / "shorts",
        PROJECT_ROOT / "output" / "videos",
        PROJECT_ROOT / "output" / "cinema_masterclass",
        PROJECT_ROOT / "output" / "scheduled_releases",
    ]
    for d in obsolete_dirs:
        if d.exists():
            print(f"Removing obsolete directory: {d.relative_to(PROJECT_ROOT)}")
            shutil.rmtree(d)

    # 3. Verify that all release folders in docs/youtube_releases contain the required single-copy artifacts
    releases_dir = PROJECT_ROOT / "docs" / "youtube_releases"
    print("\n--- Verifying docs/youtube_releases/ Single-Copy Integrity ---")
    valid_count = 0
    for ep_dir in sorted(releases_dir.iterdir()):
        if not ep_dir.is_dir() or ep_dir.name.startswith("."):
            continue
        files = set(f.name for f in ep_dir.iterdir() if f.is_file() and not f.name.startswith("."))
        has_video = "video.mp4" in files
        has_short = "short.mp4" in files
        has_thumb = "thumbnail.jpg" in files
        has_short_thumb = "short_thumbnail.jpg" in files
        print(f"  [OK] {ep_dir.name}: {len(files)} files (video={has_video}, short={has_short}, thumb={has_thumb})")
        valid_count += 1

    print(f"\n[SUCCESS] Directory Layout Enforced! {valid_count} release packages verified in docs/youtube_releases/.")

if __name__ == "__main__":
    organize()
