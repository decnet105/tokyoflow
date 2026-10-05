#!/usr/bin/env python3
"""
TokyoFlow Japanese - YouTube Metadata, Title & Cover Synchronization Engine
==========================================================================
Updates YouTube video titles, high-retention structured descriptions, tags,
and uploads authentic 4K master thumbnails for Chinese releases:
- WL.01 Masterclass (AaWSZ4J2fSI) + WS.01 Short (vMM1KrOG4j4)
- WL.02 Mega-Compilation (jFEtdDNpvlg) + WS.02 Short (4_95LXM4uj0)
Enforces strict Zero Emoji Discipline across all metadata.
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

EMOJI_REGEX = re.compile(
    r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff\u2b50\u2b55\u303d\u3297\u3299]"
)

def assert_zero_emoji(text: str, context: str):
    matches = EMOJI_REGEX.findall(text)
    if matches:
        raise ValueError(f"[ZERO EMOJI VIOLATION] Found emojis in {context}: {matches}")

def parse_metadata_file(md_path: Path):
    content = md_path.read_text(encoding="utf-8")
    parts = content.split("```")
    if len(parts) >= 4:
        title = parts[1].strip()
        description = parts[3].strip()
        return title, description
    raise ValueError(f"Could not parse code blocks in {md_path}")

def update_all_youtube_releases():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: YouTube Metadata, Title & 4K Cover Update Engine")
    print("================================================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)

    wl_dir = PROJECT_ROOT / "docs/youtube_releases/WL01-last-mile-masterclass-v1.0-zh"
    wm_dir = PROJECT_ROOT / "docs/youtube_releases/WM01-weekday_survival_mega_compilation-v1.0-zh"

    wl_title, wl_desc = parse_metadata_file(wl_dir / "metadata.md")
    wl_short_title, wl_short_desc = parse_metadata_file(wl_dir / "short_metadata.md")
    wm_title, wm_desc = parse_metadata_file(wm_dir / "metadata.md")
    wm_short_title, wm_short_desc = parse_metadata_file(wm_dir / "short_metadata.md")

    updates = [
        {
            "id": "AaWSZ4J2fSI",
            "name": "WL.01 Last Mile 25-Min Cinema Masterclass (Chinese Edition)",
            "title": wl_title,
            "desc": wl_desc,
            "tags": [
                "日语学习", "最后的里程", "满岛光", "冈田将生", "石原里美", "绫野刚",
                "看电影学日语", "JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2",
                "日语听力", "日语影子跟读", "日本电影", "职场日语", "日语语法", "TokyoFlow"
            ],
            "thumb": wl_dir / "thumbnail.jpg"
        },
        {
            "id": "vMM1KrOG4j4",
            "name": "WS.01 Last Mile Shadowing Short (Chinese Edition)",
            "title": wl_short_title,
            "desc": wl_short_desc,
            "tags": ["Shorts", "日语学习", "最后的里程", "满岛光", "JLPTN3", "日语口语", "TokyoFlow"],
            "thumb": wl_dir / "short_thumbnail.jpg"
        },
        {
            "id": "jFEtdDNpvlg",
            "name": "WL.02 (WM.01) Mon-Fri Tokyo Survival 28-Min Masterclass (Chinese Edition)",
            "title": wm_title,
            "desc": wm_desc,
            "tags": [
                "日语学习", "东京生活", "日本旅游日语", "JLPT N5", "JLPT N4", "JLPT N3",
                "山手线", "便利店日语", "居酒屋日语", "拉面定制", "温泉礼仪", "日本文化",
                "TokyoFlow", "日语听力", "日语口语"
            ],
            "thumb": wm_dir / "thumbnail.jpg"
        },
        {
            "id": "4_95LXM4uj0",
            "name": "WS.02 Yamanote Station Platform Announcement Short (Chinese Edition)",
            "title": wm_short_title,
            "desc": wm_short_desc,
            "tags": ["Shorts", "日语学习", "山手线", "东京生活", "JLPTN4", "日语听力", "TokyoFlow"],
            "thumb": wm_dir / "short_thumbnail.jpg"
        }
    ]

    for item in updates:
        vid = item["id"]
        title = item["title"]
        desc = item["desc"]
        tags = item["tags"]
        thumb_path = item["thumb"]

        print(f"\n--------------------------------------------------------------------------------")
        print(f"[*] Processing Video: {item['name']} ({vid})")
        print(f"[*] Target Title: {title}")

        # Zero Emoji Verification
        assert_zero_emoji(title, f"Title for {vid}")
        assert_zero_emoji(desc, f"Description for {vid}")
        for t in tags:
            assert_zero_emoji(t, f"Tag in {vid}")

        # 1. Update Video Snippet Metadata
        try:
            req = youtube.videos().update(
                part="snippet",
                body={
                    "id": vid,
                    "snippet": {
                        "title": title,
                        "description": desc,
                        "tags": tags,
                        "categoryId": "27",
                        "defaultLanguage": "zh",
                        "defaultAudioLanguage": "ja"
                    }
                }
            )
            res = req.execute()
            print(f"  [OK] Metadata Updated on YouTube: {res['snippet']['title']}")
        except Exception as e:
            print(f"  [ERROR] Updating snippet for {vid}: {e}")

        # 2. Upload Custom 4K Thumbnail
        if thumb_path.exists():
            print(f"[*] Uploading Custom Thumbnail: {thumb_path.name} ({thumb_path.stat().st_size/1024:.1f} KB)")
            try:
                media = MediaFileUpload(str(thumb_path), mimetype="image/jpeg", resumable=True)
                req_thumb = youtube.thumbnails().set(
                    videoId=vid,
                    media_body=media
                )
                req_thumb.execute()
                print(f"  [OK] Custom Thumbnail Applied Successfully: https://youtu.be/{vid}")
            except Exception as e:
                print(f"  [ERROR] Uploading thumbnail for {vid}: {e}")
        else:
            print(f"  [WARN] Thumbnail file not found: {thumb_path}")

        time.sleep(1.0)

    print("\n================================================================================")
    print(" [OK] All YouTube Titles, Descriptions, Tags and Covers updated successfully!")
    print("================================================================================")

if __name__ == "__main__":
    update_all_youtube_releases()
