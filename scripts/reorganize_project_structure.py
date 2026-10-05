#!/usr/bin/env python3
"""
TokyoFlow Japanese • Complete Project Reorganization Engine
===========================================================
Reorganizes docs, outputs, and assets into a clean, scalable dual-track structure:
- docs/en, docs/zh, docs/shared
- output/en/masterclasses, output/en/shorts, output/en/study_guide, output/en/channel_trailer
- output/zh/masterclasses, output/zh/shorts, output/zh/study_guide, output/zh/channel_trailer
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def organize():
    print("==================================================")
    print("Reorganizing TokyoFlow Dual-Track Directory Structure")
    print("==================================================")

    # 1. Create target directory skeleton
    dirs = [
        # Docs
        PROJECT_ROOT / "docs" / "en",
        PROJECT_ROOT / "docs" / "zh",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "backgrounds",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "branding",
        PROJECT_ROOT / "docs" / "shared" / "assets" / "fonts",
        # Output EN
        PROJECT_ROOT / "output" / "en" / "study_guide",
        PROJECT_ROOT / "output" / "en" / "channel_trailer",
        PROJECT_ROOT / "output" / "en" / "masterclasses",
        PROJECT_ROOT / "output" / "en" / "shorts",
        # Output ZH
        PROJECT_ROOT / "output" / "zh" / "study_guide",
        PROJECT_ROOT / "output" / "zh" / "channel_trailer",
        PROJECT_ROOT / "output" / "zh" / "masterclasses",
        PROJECT_ROOT / "output" / "zh" / "shorts",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Verified directory: {d.relative_to(PROJECT_ROOT)}")

    # 2. Sync Study Guides & Trailers
    print("\n--- Syncing Study Guides & Channel Trailers ---")
    
    # Study Guide EN
    src_sg_en = PROJECT_ROOT / "output" / "study_guide_en"
    dst_sg_en = PROJECT_ROOT / "output" / "en" / "study_guide"
    if src_sg_en.exists():
        for f in src_sg_en.glob("*"):
            if f.is_file():
                shutil.copy2(f, dst_sg_en / f.name)
        print("  [OK] Synced output/en/study_guide/")

    # Study Guide ZH
    src_sg_zh = PROJECT_ROOT / "output" / "study_guide_zh"
    dst_sg_zh = PROJECT_ROOT / "output" / "zh" / "study_guide"
    if src_sg_zh.exists():
        for f in src_sg_zh.glob("*"):
            if f.is_file():
                shutil.copy2(f, dst_sg_zh / f.name)
        print("  [OK] Synced output/zh/study_guide/")

    # Trailer EN
    src_tr_en = PROJECT_ROOT / "output" / "channel_trailer_en"
    dst_tr_en = PROJECT_ROOT / "output" / "en" / "channel_trailer"
    if src_tr_en.exists():
        for f in src_tr_en.glob("*"):
            if f.is_file():
                shutil.copy2(f, dst_tr_en / f.name)
        print("  [OK] Synced output/en/channel_trailer/")

    # Trailer ZH
    src_tr_zh = PROJECT_ROOT / "output" / "channel_trailer_zh"
    dst_tr_zh = PROJECT_ROOT / "output" / "zh" / "channel_trailer"
    if src_tr_zh.exists():
        for f in src_tr_zh.glob("*"):
            if f.is_file():
                shutil.copy2(f, dst_tr_zh / f.name)
        print("  [OK] Synced output/zh/channel_trailer/")

    # 3. Categorize Episodes (Masterclasses & Shorts) from docs/youtube_releases
    print("\n--- Organizing Episodes into English & Chinese Masterclasses / Shorts ---")
    releases_dir = PROJECT_ROOT / "docs" / "youtube_releases"
    if releases_dir.exists():
        for ep_dir in sorted(releases_dir.iterdir()):
            if not ep_dir.is_dir() or ep_dir.name.startswith("."):
                continue
            
            ep_name = ep_dir.name
            is_zh = ep_name.endswith("-zh")
            lang = "zh" if is_zh else "en"
            
            # Clean episode key
            clean_ep_id = ep_name.replace("-zh", "").replace("-v1.0", "")
            
            dst_master = PROJECT_ROOT / "output" / lang / "masterclasses" / clean_ep_id
            dst_short = PROJECT_ROOT / "output" / lang / "shorts" / clean_ep_id
            dst_master.mkdir(parents=True, exist_ok=True)
            dst_short.mkdir(parents=True, exist_ok=True)
            
            # Scan files inside episode folder
            for f in ep_dir.glob("*"):
                if not f.is_file() or f.name.startswith("."):
                    continue
                
                fname = f.name.lower()
                # Categorize into masterclass vs short
                if "short" in fname:
                    shutil.copy2(f, dst_short / f.name)
                elif "thumbnail.jpg" in fname or "metadata.md" in fname or fname.endswith(".mp4") or "lesson" in fname or "scenario" in fname:
                    shutil.copy2(f, dst_master / f.name)
                else:
                    # General / shared file for this ep
                    shutil.copy2(f, dst_master / f.name)
                    
            print(f"  [OK] Organized {ep_name} -> output/{lang}/masterclasses/{clean_ep_id} & shorts/{clean_ep_id}")

    # 4. Copy shared assets into docs/shared/assets/
    print("\n--- Organizing Shared Branding & Background Assets ---")
    assets_dir = PROJECT_ROOT / "docs" / "youtube_assets"
    if assets_dir.exists():
        # Backgrounds
        bg_dir = assets_dir / "scene_backgrounds"
        if bg_dir.exists():
            for bg in bg_dir.glob("*"):
                if bg.is_file():
                    shutil.copy2(bg, PROJECT_ROOT / "docs" / "shared" / "assets" / "backgrounds" / bg.name)
            print("  [OK] Copied scene backgrounds to docs/shared/assets/backgrounds/")
            
        # Branding
        for br in assets_dir.glob("*"):
            if br.is_file() and ("banner" in br.name or "avatar" in br.name or "icon" in br.name):
                shutil.copy2(br, PROJECT_ROOT / "docs" / "shared" / "assets" / "branding" / br.name)
        print("  [OK] Copied branding assets to docs/shared/assets/branding/")

    # 5. Populate documentation into docs/en and docs/zh
    print("\n--- Organizing Core Documents into docs/en and docs/zh ---")
    
    # English docs
    if (PROJECT_ROOT / "docs" / "PEDAGOGICAL_BLUEPRINT.md").exists():
        shutil.copy2(PROJECT_ROOT / "docs" / "PEDAGOGICAL_BLUEPRINT.md", PROJECT_ROOT / "docs" / "en" / "BLUEPRINT.md")
    if (PROJECT_ROOT / "docs" / "YOUTUBE_LAUNCH_KIT.md").exists():
        shutil.copy2(PROJECT_ROOT / "docs" / "YOUTUBE_LAUNCH_KIT.md", PROJECT_ROOT / "docs" / "en" / "YOUTUBE_LAUNCH_KIT.md")
    if (PROJECT_ROOT / "output" / "study_guide_en" / "community_post.md").exists():
        shutil.copy2(PROJECT_ROOT / "output" / "study_guide_en" / "community_post.md", PROJECT_ROOT / "docs" / "en" / "COMMUNITY_POSTS_EN.md")
    if (PROJECT_ROOT / "output" / "study_guide_en" / "metadata.md").exists():
        shutil.copy2(PROJECT_ROOT / "output" / "study_guide_en" / "metadata.md", PROJECT_ROOT / "docs" / "en" / "STUDY_GUIDE_METADATA.md")
        
    # Chinese docs
    if (PROJECT_ROOT / "output" / "study_guide_zh" / "metadata.md").exists():
        shutil.copy2(PROJECT_ROOT / "output" / "study_guide_zh" / "metadata.md", PROJECT_ROOT / "docs" / "zh" / "STUDY_GUIDE_METADATA_ZH.md")
    if (PROJECT_ROOT / "output" / "channel_trailer_zh" / "metadata.md").exists():
        shutil.copy2(PROJECT_ROOT / "output" / "channel_trailer_zh" / "metadata.md", PROJECT_ROOT / "docs" / "zh" / "CHANNEL_TRAILER_METADATA_ZH.md")

    # Shared docs
    if (PROJECT_ROOT / "docs" / "APP_STORE_CONNECT_GUIDE.md").exists():
        shutil.copy2(PROJECT_ROOT / "docs" / "APP_STORE_CONNECT_GUIDE.md", PROJECT_ROOT / "docs" / "shared" / "APP_STORE_CONNECT_GUIDE.md")
    if (PROJECT_ROOT / "docs" / "YOUTUBE_PUBLISHING_SCHEDULE_CONTRACT.md").exists():
        shutil.copy2(PROJECT_ROOT / "docs" / "YOUTUBE_PUBLISHING_SCHEDULE_CONTRACT.md", PROJECT_ROOT / "docs" / "shared" / "PUBLISHING_SCHEDULE_CONTRACT.md")

    print("\n[SUCCESS] Directory Reorganization Complete!")

if __name__ == "__main__":
    organize()
