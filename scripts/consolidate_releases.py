#!/usr/bin/env python3
"""
TokyoFlow Japanese • Release Artifacts Consolidation Engine
============================================================
Consolidates all scattered / duplicate daily video and short artifacts into
the single canonical release repository under `docs/youtube_releases/`.

Rule: Each episode (English and Chinese) has ONE unique package folder:
- English: docs/youtube_releases/E{XX}-{Slug}-v1.0/
- Chinese: docs/youtube_releases/E{XX}-{Slug}-v1.0-zh/
- Specials: WL01-... / WM01-...

Inside each folder, all 7 artifacts are preserved in ONE place:
1. video.mp4 (16:9 Long-form Micro-lesson)
2. thumbnail.jpg (16:9 4K Landscape Cover)
3. metadata.md (16:9 YouTube Launch Kit)
4. short.mp4 (9:16 Vertical Interactive Shadowing Short)
5. short_thumbnail.jpg (9:16 Vertical Cover)
6. short_metadata.md (9:16 Shorts Launch Kit)
7. script.json (Structured episode manifest)
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
OUTPUT_DIR = PROJECT_ROOT / "output"

def consolidate():
    print("==================================================")
    print("Consolidating TokyoFlow Release Artifacts")
    print("==================================================")
    
    RELEASES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Consolidate English Episodes
    en_master = OUTPUT_DIR / "en" / "masterclasses"
    en_shorts = OUTPUT_DIR / "en" / "shorts"
    
    if en_master.exists():
        for ep_dir in sorted(en_master.iterdir()):
            if not ep_dir.is_dir() or ep_dir.name.startswith(".") or ep_dir.name == "batch_scenarios_drafts":
                continue
            
            ep_slug = ep_dir.name
            target_name = ep_slug if ep_slug.endswith("-v1.0") else f"{ep_slug}-v1.0"
            target_dir = RELEASES_DIR / target_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all files from masterclass
            for f in ep_dir.iterdir():
                if f.is_file() and not f.name.startswith("."):
                    dst = target_dir / f.name
                    if not dst.exists() or dst.stat().st_size != f.stat().st_size:
                        shutil.copy2(f, dst)
            
            # Copy all files from shorts
            short_ep_dir = en_shorts / ep_slug
            if short_ep_dir.exists():
                for f in short_ep_dir.iterdir():
                    if f.is_file() and not f.name.startswith("."):
                        dst = target_dir / f.name
                        if not dst.exists() or dst.stat().st_size != f.stat().st_size:
                            shutil.copy2(f, dst)
            
            print(f"[EN OK] Consolidated -> docs/youtube_releases/{target_name}")

    # 2. Consolidate Chinese Episodes
    zh_master = OUTPUT_DIR / "zh" / "masterclasses"
    zh_shorts = OUTPUT_DIR / "zh" / "shorts"
    
    if zh_master.exists():
        for ep_dir in sorted(zh_master.iterdir()):
            if not ep_dir.is_dir() or ep_dir.name.startswith("."):
                continue
            
            ep_slug = ep_dir.name
            target_name = ep_slug if ep_slug.endswith("-v1.0-zh") else f"{ep_slug}-v1.0-zh"
            target_dir = RELEASES_DIR / target_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy all files from masterclass
            for f in ep_dir.iterdir():
                if f.is_file() and not f.name.startswith("."):
                    dst = target_dir / f.name
                    if not dst.exists() or dst.stat().st_size != f.stat().st_size:
                        shutil.copy2(f, dst)
            
            # Copy all files from shorts
            short_ep_dir = zh_shorts / ep_slug
            if short_ep_dir.exists():
                for f in short_ep_dir.iterdir():
                    if f.is_file() and not f.name.startswith("."):
                        dst = target_dir / f.name
                        if not dst.exists() or dst.stat().st_size != f.stat().st_size:
                            shutil.copy2(f, dst)
            
            print(f"[ZH OK] Consolidated -> docs/youtube_releases/{target_name}")

    print("\n--- Verification of Packages in docs/youtube_releases/ ---")
    for p in sorted(RELEASES_DIR.iterdir()):
        if p.is_dir() and not p.name.startswith("."):
            files = sorted([f.name for f in p.iterdir() if f.is_file() and not f.name.startswith(".")])
            has_video = "video.mp4" in files
            has_short = "short.mp4" in files
            has_thumb = "thumbnail.jpg" in files
            has_short_thumb = "short_thumbnail.jpg" in files
            print(f"  {p.name}: {len(files)} files [video: {has_video}, short: {has_short}, thumb: {has_thumb}, s_thumb: {has_short_thumb}]")

if __name__ == "__main__":
    consolidate()
