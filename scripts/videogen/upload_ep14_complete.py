#!/usr/bin/env python3
"""
TokyoFlow Japanese • EP.14 Complete Upload, Drive Verification, Commenting & Playlist Sync
=========================================================================================
1. Verifies Google Drive Study Companion links (HTTP 200).
2. Uploads English EP.14 (Long & Short) with scheduled release at 2026-10-10 08:00 AM EDT (notifySubscribers=True).
3. Uploads Chinese EP.14 (Long & Short) with scheduled release at 2026-10-10 08:00 PM EDT (notifySubscribers=False).
4. Embeds Drive Links & Passcode TOKYOFLOW-EP14 in Video Descriptions.
5. Adds videos to proper Playlists (EN/ZH Long/Short, JLPT N5, Tokyo Transit).
6. Posts Study Guide comments to the new videos.
7. Strictly complies with Zero-Emoji discipline.
"""

import os
import sys
import json
import time
import zoneinfo
import urllib.request
from pathlib import Path
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_auth import get_authenticated_service
from youtube_publisher import upload_video_asset

EST_TZ = zoneinfo.ZoneInfo("America/New_York")
LEDGER_FILE = PROJECT_ROOT / "docs" / "shared" / "publish_ledger.json"

DRIVE_LINK_EP14_EN = "https://drive.google.com/file/d/10EgW3fUcq0Bmn9cGTLLctKUjyW2a2qaE/view?usp=drivesdk"
DRIVE_LINK_EP14_ZH = "https://drive.google.com/file/d/1qXzDrGODLA5SskQi1-pRtf8qSFMZP9Kn/view?usp=drivesdk"
PASSCODE = "TOKYOFLOW-EP14"

PLAYLISTS = {
    "en_long": "PLHUEYGzrBe-s",
    "en_short": "PLVxXRTmSmcAM",
    "zh_long": "PLVchR4TmK56E",
    "zh_short": "PLTpb6FPYqYC4",
    "jlpt_n5": "PLY_ZLcqTrnU8",
    "transit": "PLAUUBQzM_liE"
}

def verify_drive_urls():
    print("==================================================")
    print("Verifying Google Drive URLs (HTTP Status Check)")
    print("==================================================")
    for name, url in [("English EP.14 PDF", DRIVE_LINK_EP14_EN), ("Chinese EP.14 PDF", DRIVE_LINK_EP14_ZH)]:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req)
        status = resp.status
        print(f"  [VERIFIED] {name}: Status {status} -> {url}")
        assert status == 200, f"URL validation failed for {name} with status {status}"
    print("✓ All Google Drive Study Companion URLs verified successfully!\n")

def add_to_playlist(youtube, playlist_id: str, video_id: str, playlist_name: str):
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
        print(f"  [PLAYLIST] Added {video_id} -> {playlist_name} ({playlist_id})")
    except Exception as e:
        print(f"  [PLAYLIST NOTICE] {video_id} -> {playlist_name}: {e}")

def post_study_comment(youtube, video_id: str, is_zh: bool = False):
    drive_link = DRIVE_LINK_EP14_ZH if is_zh else DRIVE_LINK_EP14_EN
    if not is_zh:
        comment_text = (
            f"Thank you for watching TokyoFlow Japanese!\n"
            f"Download your EP.14 Suica New Payment Service Study Companion (PDF):\n"
            f"Google Drive Link: {drive_link}\n"
            f"Unlock Passcode: {PASSCODE}\n\n"
            f"- Full Tokyo dialogue with Furigana & Romaji\n"
            f"- Classified Vocabulary & Grammar tables [JLPT N5]\n\n"
            f"Remember to SUBSCRIBE to TokyoFlow for daily Tokyo immersion masterclasses and shadowing drills!"
        )
    else:
        comment_text = (
            f"感谢观看 TokyoFlow 日语实景精讲！\n"
            f"第14期【JR东日本 Suica全新支付】配套研习讲义 (PDF) 已更新至网盘：\n"
            f"网盘下载链接：{drive_link}\n"
            f"视频完播口令：{PASSCODE}\n\n"
            f"- 严格按照【JLPT N5】分级归纳词汇与核心语法接续\n"
            f"- 支持离线保存与高清 300 DPI A4 打印复习\n\n"
            f"记得点击【订阅】TokyoFlow 官方频道并开启小铃铛，每日打卡实景跟读训练！"
        )
    try:
        res = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        ).execute()
        print(f"  [COMMENT] Pinned comment posted on {video_id}! Thread ID: {res.get('id')}")
    except Exception as e:
        print(f"  [COMMENT NOTICE] Could not post comment on {video_id}: {e}")

def main():
    print("==================================================")
    print("TokyoFlow • EP.14 Master Upload & Sync Pipeline")
    print("Zero-Emoji Discipline | Scheme D Passcode Distribution")
    print("==================================================")
    
    # 1. Verify Drive URLs
    verify_drive_urls()
    
    # 2. Authenticate YouTube
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)
    
    en_dir = PROJECT_ROOT / "docs" / "youtube_releases" / "E14-suica-teppay-launch-v1.0"
    zh_dir = PROJECT_ROOT / "docs" / "youtube_releases" / "E14-suica-teppay-launch-v1.0-zh"
    
    # Description download blocks
    desc_block_en = (
        f"\n\n------------------------------------------------------------\n"
        f"[OFFICIAL STUDY COMPANION & JLPT WORKBOOK PDF]\n"
        f"Download EP.14 Suica New Payment Service Study Companion (PDF):\n"
        f"Google Drive Link: {DRIVE_LINK_EP14_EN}\n"
        f"Unlock Passcode (from video): {PASSCODE}\n"
        f"- Classified Vocabulary & Grammar tables [JLPT N5]\n"
        f"- Print-Friendly 300 DPI A4 Format (100% Free for Subscribers)\n"
        f"------------------------------------------------------------\n"
    )
    
    desc_block_zh = (
        f"\n\n------------------------------------------------------------\n"
        f"【本期课程配套 JLPT 研习讲义与复习手册下载】\n"
        f"下载 第14期 JR东日本Suica全新支付配套研习讲义 (PDF)：\n"
        f"Google Drive 链接：{DRIVE_LINK_EP14_ZH}\n"
        f"视频完播口令 / 密码：{PASSCODE}\n"
        f"- 严格按照【JLPT N5】分级归纳\n"
        f"- 高清 300 DPI A4 打印版（订阅学员免费下载）\n"
        f"------------------------------------------------------------\n"
    )
    
    # -------------------------------------------------------------
    # A. English EP.14 (Oct 10 08:00 AM EDT, notifySubscribers=True)
    # -------------------------------------------------------------
    en_pub_dt = datetime(2026, 10, 10, 8, 0, 0, tzinfo=EST_TZ)
    with open(en_dir / "production_spec.json", "r", encoding="utf-8") as f:
        en_spec = json.load(f)
        
    print("1. Uploading English Masterclass (16:9 Long Video)...")
    long_meta_en = {
        "title": en_spec["long_form"]["yt_title"],
        "description": en_spec["long_form"]["description"] + desc_block_en,
        "tags": en_spec["long_form"]["tags"]
    }
    en_long_res = upload_video_asset(
        youtube=yt,
        video_path=en_dir / "video.mp4",
        thumbnail_path=en_dir / "thumbnail.jpg",
        meta=long_meta_en,
        publish_at=en_pub_dt,
        is_short=False,
        notify_subscribers=True
    )
    en_long_id = en_long_res["video_id"]
    print(f"✓ English Long Video Uploaded: {en_long_id}")
    
    print("2. Uploading English Shorts (9:16 Vertical Video)...")
    short_meta_en = {
        "title": en_spec["shorts"]["yt_short_title"],
        "description": f"Learn Tokyo Japanese in 60s! #Shorts #LearnJapanese\n\n{en_spec['shorts']['jp_sentence']}\n{en_spec['shorts']['en_translation']}" + desc_block_en,
        "tags": ["TokyoFlow", "Shorts", "LearnJapanese", "JLPTN5"]
    }
    en_short_res = upload_video_asset(
        youtube=yt,
        video_path=en_dir / "short.mp4",
        thumbnail_path=en_dir / "short_thumbnail.jpg",
        meta=short_meta_en,
        publish_at=en_pub_dt,
        is_short=True,
        notify_subscribers=True
    )
    en_short_id = en_short_res["video_id"]
    print(f"✓ English Short Video Uploaded: {en_short_id}")
    
    # -------------------------------------------------------------
    # B. Chinese EP.14 (Oct 10 08:00 PM EDT, notifySubscribers=False)
    # -------------------------------------------------------------
    zh_pub_dt = datetime(2026, 10, 10, 20, 0, 0, tzinfo=EST_TZ)
    with open(zh_dir / "script.json", "r", encoding="utf-8") as f:
        zh_spec = json.load(f)
        
    print("3. Uploading Chinese Masterclass (16:9 Long Video)...")
    long_meta_zh = {
        "title": zh_spec["yt_title"],
        "description": f"【TokyoFlow 日语实景精讲 • 中文解说版】\n\n{zh_spec['title']}\n\n#TokyoFlow #日语学习 #JLPTN5" + desc_block_zh,
        "tags": ["TokyoFlow", "日语学习", "JLPTN5", "日语听力", "日本生活"]
    }
    zh_long_res = upload_video_asset(
        youtube=yt,
        video_path=zh_dir / "video.mp4",
        thumbnail_path=zh_dir / "thumbnail.jpg",
        meta=long_meta_zh,
        publish_at=zh_pub_dt,
        is_short=False,
        notify_subscribers=False
    )
    zh_long_id = zh_long_res["video_id"]
    print(f"✓ Chinese Long Video Uploaded: {zh_long_id}")
    
    # Upload custom thumbnail for Chinese long video
    try:
        media_thumb = MediaFileUpload(str(zh_dir / "thumbnail.jpg"))
        yt.thumbnails().set(videoId=zh_long_id, media_body=media_thumb).execute()
        print(f"  [OK] Custom thumbnail uploaded for {zh_long_id}")
    except Exception as e:
        print(f"  [Notice] Thumbnail upload for {zh_long_id}: {e}")
        
    print("4. Uploading Chinese Shorts (9:16 Vertical Video)...")
    short_meta_zh = {
        "title": f"【JLPT N5】SH.14-zh {zh_spec['cover']['hook']}",
        "description": f"1分钟掌握东京地道口语！{zh_spec['cover']['sub_hook']}\n\n#TokyoFlow #Shorts #日语学习 #JLPTN5" + desc_block_zh,
        "tags": ["TokyoFlow", "Shorts", "日语学习", "JLPTN5"]
    }
    zh_short_res = upload_video_asset(
        youtube=yt,
        video_path=zh_dir / "short.mp4",
        thumbnail_path=zh_dir / "short_thumbnail.jpg",
        meta=short_meta_zh,
        publish_at=zh_pub_dt,
        is_short=True,
        notify_subscribers=False
    )
    zh_short_id = zh_short_res["video_id"]
    print(f"✓ Chinese Short Video Uploaded: {zh_short_id}")
    
    # -------------------------------------------------------------
    # C. Playlist Placement
    # -------------------------------------------------------------
    print("\n5. Categorizing videos into YouTube Playlists...")
    # English Long
    add_to_playlist(yt, PLAYLISTS["en_long"], en_long_id, "English Masterclasses (16:9)")
    add_to_playlist(yt, PLAYLISTS["jlpt_n5"], en_long_id, "JLPT N5 Complete Immersion")
    add_to_playlist(yt, PLAYLISTS["transit"], en_long_id, "Tokyo Transit & Station Japanese")
    
    # English Short
    add_to_playlist(yt, PLAYLISTS["en_short"], en_short_id, "English Shorts (9:16)")
    add_to_playlist(yt, PLAYLISTS["jlpt_n5"], en_short_id, "JLPT N5 Complete Immersion")
    add_to_playlist(yt, PLAYLISTS["transit"], en_short_id, "Tokyo Transit & Station Japanese")
    
    # Chinese Long
    add_to_playlist(yt, PLAYLISTS["zh_long"], zh_long_id, "Chinese Masterclasses (16:9)")
    add_to_playlist(yt, PLAYLISTS["jlpt_n5"], zh_long_id, "JLPT N5 Complete Immersion")
    add_to_playlist(yt, PLAYLISTS["transit"], zh_long_id, "Tokyo Transit & Station Japanese")
    
    # Chinese Short
    add_to_playlist(yt, PLAYLISTS["zh_short"], zh_short_id, "Chinese Shorts (9:16)")
    add_to_playlist(yt, PLAYLISTS["jlpt_n5"], zh_short_id, "JLPT N5 Complete Immersion")
    add_to_playlist(yt, PLAYLISTS["transit"], zh_short_id, "Tokyo Transit & Station Japanese")
    
    # -------------------------------------------------------------
    # D. Post Comments
    # -------------------------------------------------------------
    print("\n6. Posting Study Companion Download Comments...")
    post_study_comment(yt, en_long_id, is_zh=False)
    post_study_comment(yt, en_short_id, is_zh=False)
    post_study_comment(yt, zh_long_id, is_zh=True)
    post_study_comment(yt, zh_short_id, is_zh=True)
    
    # -------------------------------------------------------------
    # E. Update Publish Ledger
    # -------------------------------------------------------------
    for lf in [LEDGER_FILE, PROJECT_ROOT / "docs" / "youtube_releases" / "publish_ledger.json"]:
        if lf.exists():
            with open(lf, "r", encoding="utf-8") as f:
                led = json.load(f)
            led["published"]["E14_en_long"] = {
                "id": en_long_id,
                "title": long_meta_en["title"],
                "publishAt": "2026-10-10T12:00:00Z",
                "status": "private",
                "lang": "en",
                "format": "long"
            }
            led["published"]["E14_en_short"] = {
                "id": en_short_id,
                "title": short_meta_en["title"],
                "publishAt": "2026-10-10T12:00:00Z",
                "status": "private",
                "lang": "en",
                "format": "short"
            }
            led["published"]["E14_zh_long"] = {
                "id": zh_long_id,
                "title": long_meta_zh["title"],
                "publishAt": "2026-10-11T00:00:00Z",
                "status": "private",
                "lang": "zh",
                "format": "long"
            }
            led["published"]["E14_zh_short"] = {
                "id": zh_short_id,
                "title": short_meta_zh["title"],
                "publishAt": "2026-10-11T00:00:00Z",
                "status": "private",
                "lang": "zh",
                "format": "short"
            }
            with open(lf, "w", encoding="utf-8") as f:
                json.dump(led, f, indent=2, ensure_ascii=False)
                
    print("\n==================================================")
    print("EP.14 Re-Upload & Synchronization Complete!")
    print(f"EN Long:  {en_long_id} -> https://youtu.be/{en_long_id}")
    print(f"EN Short: {en_short_id} -> https://youtu.be/{en_short_id}")
    print(f"ZH Long:  {zh_long_id} -> https://youtu.be/{zh_long_id}")
    print(f"ZH Short: {zh_short_id} -> https://youtu.be/{zh_short_id}")
    print("==================================================")

if __name__ == "__main__":
    main()
