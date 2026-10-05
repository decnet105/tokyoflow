#!/usr/bin/env python3
"""
TokyoFlow Japanese • Re-upload Chinese Masterclasses & Shorts Engine
====================================================================
1. Deletes previous versions of Chinese masterclass videos and shorts.
2. Uploads freshly replicated 1080p master videos with 100% authentic footage:
   - WL.01 Masterclass (25 min, Last Mile authentic movie footage & Mitsushima Hikari hero cover)
   - WS.01 Short (Last Mile high-light dialogue shadowing)
   - WL.02 / WM.01 Mega-Compilation (28 min, 4K Tokyo living scenes)
   - WS.02 Short (Yamanote Line platform announcement)
3. Applies custom 4K thumbnails.
4. Routes to official Chinese playlists.
5. Updates publish ledger and website references.
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

OLD_VIDEO_IDS = [
    ("WL.01 Masterclass (Recent)", "qVNR2duZWqQ"),
    ("WS.01 Short (Recent)", "XVbg-f8s7F0"),
    ("WL.02 Masterclass (Recent)", "D99vmCoeymc"),
    ("WS.02 Short (Recent)", "PSynUxU1zy4"),
    ("WL.01 Masterclass (Old)", "AaWSZ4J2fSI"),
    ("WS.01 Short (Old)", "vMM1KrOG4j4"),
    ("WL.02 Masterclass (Old)", "jFEtdDNpvlg"),
    ("WS.02 Short (Old)", "4_95LXM4uj0")
]

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

def delete_old_videos(youtube):
    print("\n--- 正在删除旧版测试视频 ---")
    for name, vid in OLD_VIDEO_IDS:
        print(f"[*] Deleting {name} ({vid})...")
        try:
            youtube.videos().delete(id=vid).execute()
            print(f"  [OK] Successfully deleted old video: {vid}")
        except Exception as e:
            print(f"  [WARN] Could not delete {vid} (may already be deleted): {e}")
        time.sleep(1.0)

def upload_single_video(youtube, video_path: Path, thumbnail_path: Path, title: str, description: str, tags: list, is_short: bool, notify_subscribers: bool = False):
    print(f"\n[*] Uploading: {title}")
    print(f"    File: {video_path.name} ({video_path.stat().st_size / (1024*1024):.1f} MB)")
    print(f"    Shorts Mode: {is_short} | Notify Subscribers: {notify_subscribers}")

    assert_zero_emoji(title, f"Title: {title}")
    assert_zero_emoji(description, f"Description for {title}")
    for t in tags:
        assert_zero_emoji(t, f"Tag in {title}")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags[:30],
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
        notifySubscribers=notify_subscribers
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"    Upload Progress: {int(status.progress() * 100)}%")

    new_id = response.get("id")
    video_url = f"https://youtu.be/{new_id}"
    print(f"  [OK] Upload Succeeded! Video ID: {new_id} -> {video_url}")

    # Set Custom Thumbnail
    if thumbnail_path and thumbnail_path.exists():
        print(f"    Uploading Custom Thumbnail: {thumbnail_path.name} ({thumbnail_path.stat().st_size / 1024:.1f} KB)...")
        try:
            time.sleep(1.5)
            youtube.thumbnails().set(
                videoId=new_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Custom Thumbnail applied successfully.")
        except Exception as e:
            print(f"  [WARN] Thumbnail upload error: {e}")

    return new_id, video_url

def add_to_playlist(youtube, playlist_id: str, video_id: str):
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f"  [OK] Added {video_id} to playlist {playlist_id}")
    except Exception as e:
        print(f"  [WARN] Playlist addition failed: {e}")

def main():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: Re-upload Chinese Masterclasses & 4K Covers Engine")
    print("================================================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)

    # 1. Delete old videos
    delete_old_videos(youtube)

    # 2. Upload newly replicated master releases
    wl_dir = PROJECT_ROOT / "docs/youtube_releases/WL01-last-mile-masterclass-v1.0-zh"
    wm_dir = PROJECT_ROOT / "docs/youtube_releases/WM01-weekday_survival_mega_compilation-v1.0-zh"

    wl_title, wl_desc = parse_metadata_file(wl_dir / "metadata.md")
    wl_short_title, wl_short_desc = parse_metadata_file(wl_dir / "short_metadata.md")
    wm_title, wm_desc = parse_metadata_file(wm_dir / "metadata.md")
    wm_short_title, wm_short_desc = parse_metadata_file(wm_dir / "short_metadata.md")

    # [1] WL.01 Long-form Video
    wl_vid, wl_url = upload_single_video(
        youtube=youtube,
        video_path=wl_dir / "video.mp4",
        thumbnail_path=wl_dir / "thumbnail.jpg",
        title=wl_title,
        description=wl_desc,
        tags=[
            "日语学习", "最后的里程", "满岛光", "冈田将生", "石原里美", "绫野刚",
            "看电影学日语", "JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2",
            "日语听力", "日语影子跟读", "日本电影", "职场日语", "日语语法", "TokyoFlow"
        ],
        is_short=False,
        notify_subscribers=False
    )
    add_to_playlist(youtube, "PLVchR4TmK56E", wl_vid)

    # [2] WS.01 Short
    ws01_vid, ws01_url = upload_single_video(
        youtube=youtube,
        video_path=wl_dir / "short.mp4",
        thumbnail_path=wl_dir / "short_thumbnail.jpg",
        title=wl_short_title,
        description=wl_short_desc,
        tags=["Shorts", "日语学习", "最后的里程", "满岛光", "JLPTN3", "日语口语", "TokyoFlow"],
        is_short=True,
        notify_subscribers=False
    )
    add_to_playlist(youtube, "PLTpb6FPYqYC4", ws01_vid)

    # [3] WL.02 (WM.01) Long-form Video
    wm_vid, wm_url = upload_single_video(
        youtube=youtube,
        video_path=wm_dir / "video.mp4",
        thumbnail_path=wm_dir / "thumbnail.jpg",
        title=wm_title,
        description=wm_desc,
        tags=[
            "日语学习", "东京生活", "日本旅游日语", "JLPT N5", "JLPT N4", "JLPT N3",
            "山手线", "便利店日语", "居酒屋日语", "拉面定制", "温泉礼仪", "日本文化",
            "TokyoFlow", "日语听力", "日语口语"
        ],
        is_short=False,
        notify_subscribers=False
    )
    add_to_playlist(youtube, "PLVchR4TmK56E", wm_vid)

    # [4] WS.02 Short
    ws02_vid, ws02_url = upload_single_video(
        youtube=youtube,
        video_path=wm_dir / "short.mp4",
        thumbnail_path=wm_dir / "short_thumbnail.jpg",
        title=wm_short_title,
        description=wm_short_desc,
        tags=["Shorts", "日语学习", "山手线", "东京生活", "JLPTN4", "日语听力", "TokyoFlow"],
        is_short=True,
        notify_subscribers=False
    )
    add_to_playlist(youtube, "PLTpb6FPYqYC4", ws02_vid)

    # 3. Update publish_ledger.json files
    new_ledger_records = {
        "WL01-last-mile-masterclass-v1.0-zh_video": {
            "video_id": wl_vid,
            "video_url": wl_url,
            "title": wl_title,
            "uploaded_at": datetime.now(EST_TZ).isoformat(),
            "is_short": False,
            "notify_subscribers": False
        },
        "WL01-last-mile-masterclass-v1.0-zh_short": {
            "video_id": ws01_vid,
            "video_url": ws01_url,
            "title": wl_short_title,
            "uploaded_at": datetime.now(EST_TZ).isoformat(),
            "is_short": True,
            "notify_subscribers": False
        },
        "WM01-weekday_survival_mega_compilation-v1.0-zh_video": {
            "video_id": wm_vid,
            "video_url": wm_url,
            "title": wm_title,
            "uploaded_at": datetime.now(EST_TZ).isoformat(),
            "is_short": False,
            "notify_subscribers": False
        },
        "WM01-weekday_survival_mega_compilation-v1.0-zh_short": {
            "video_id": ws02_vid,
            "video_url": ws02_url,
            "title": wm_short_title,
            "uploaded_at": datetime.now(EST_TZ).isoformat(),
            "is_short": True,
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
            data["published"].update(new_ledger_records)
            with open(ledger_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  [OK] Updated ledger: {ledger_path}")

    # Output mapping for easy update
    print("\n================================================================================")
    print(" NEW PUBLISHED CHINESE MASTERCLASSES & SHORTS:")
    print(f" WL.01 Masterclass Video : {wl_vid} -> {wl_url}")
    print(f" WS.01 Shadowing Short   : {ws01_vid} -> {ws01_url}")
    print(f" WL.02 Masterclass Video : {wm_vid} -> {wm_url}")
    print(f" WS.02 Shadowing Short   : {ws02_vid} -> {ws02_url}")
    print("================================================================================")

if __name__ == "__main__":
    main()
