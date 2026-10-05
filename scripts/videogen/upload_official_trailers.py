#!/usr/bin/env python3
"""
TokyoFlow Japanese • Upload Official Channel Trailers (English & Chinese)
Uploads both trailers as PUBLIC videos with custom thumbnails and adds them to their respective masterclass playlists.
"""

import os
import sys
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAILER_EN_DIR = PROJECT_ROOT / "output" / "channel_trailer_en"
TRAILER_ZH_DIR = PROJECT_ROOT / "output" / "channel_trailer_zh"

def upload_video_package(yt, video_path, thumb_path, title, description, tags, lang, playlist_id):
    if not video_path.exists():
        print(f"Error: Video file not found at {video_path}")
        return None

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27", # Education
            "defaultLanguage": lang,
            "defaultAudioLanguage": lang
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"\nUploading: {title}")
    print(f"Privacy: PUBLIC (Immediate release)")

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
        notifySubscribers=True if lang == "en" else False
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Progress: {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    print(f"  [OK] Video uploaded successfully! ID: {video_id}")
    print(f"  URL: https://youtu.be/{video_id}")

    # Set custom thumbnail
    if thumb_path and thumb_path.exists():
        print("  Uploading custom thumbnail...")
        try:
            yt.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Custom thumbnail uploaded successfully.")
        except HttpError as e:
            print(f"  [Warning] Thumbnail upload failed: {e}")

    # Add to playlist
    if playlist_id:
        try:
            yt.playlistItems().insert(
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
            print(f"  [OK] Added to playlist: {playlist_id}")
        except Exception as e:
            print(f"  [Warning] Adding to playlist failed: {e}")

    return video_id

def main():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    print("==================================================")
    print("Uploading Official TokyoFlow Channel Trailers")
    print("==================================================")

    # 1. English Trailer
    title_en = "Master Real Tokyo Japanese! | Official TokyoFlow Academy Trailer [JLPT N5-N1]"
    desc_en = """Welcome to TokyoFlow Japanese — the cinema-grade, use-case-driven language academy dedicated to decoding authentic spoken Tokyo Japanese through real-life living, transit, pop culture, and modern media.

Forget robotic, outdated textbook sentences. TokyoFlow immerses you directly into the pulse of Tokyo:
- Yamanote Line & Tokyo Subway transit announcements & fare adjustments
- 7-Eleven & Kombini checkout speed replies
- Izakaya ordering & ramen customization protocols
- Akihabara tax-free figure shopping & Ginza fitting rooms
- Japanese pop-culture trends & daily news immersion

Daily Global Releases: 08:00 AM EDT
Subscribe now and bridge the gap between classroom theory and real-world Tokyo fluency!

#LearnJapanese #JLPT #TokyoFlow #JapaneseLanguage #Tokyo"""
    
    tags_en = ["Learn Japanese", "JLPT", "TokyoFlow", "Japanese Language", "Speak Japanese", "Tokyo", "JLPT N5", "JLPT N4", "Japanese Listening", "Shadowing"]
    
    try:
        vid_en = upload_video_package(
            yt=yt,
            video_path=TRAILER_EN_DIR / "tokyoflow_trailer_en_1080p.mp4",
            thumb_path=TRAILER_EN_DIR / "thumbnail.jpg",
            title=title_en,
            description=desc_en,
            tags=tags_en,
            lang="en",
            playlist_id="PLHUEYGzrBe-s"
        )
    except HttpError as e:
        print(f"\n[HTTP Error on English Trailer]: {e}")
        vid_en = None

    # 2. Chinese Trailer
    title_zh = "【TokyoFlow 官方中文预告】告别死板教科书！每天沉浸式掌握东京地道实景日语【JLPT N5-N1】"
    desc_zh = """欢迎来到 TokyoFlow 日语实景精讲【中文解说版】！

告别死板枯燥的传统教科书，带你直接潜入东京最真实的日常现场：
- 山手线报站与地铁闸机精算机补票全流程
- 7-Eleven/全家便利店收银台秒回应答
- 居酒屋生啤开场与顶级拉面食券机定制口诀
- 秋叶原手办免税退税与银座精品试衣口语
- 日本当季热点新闻与全网流行语深度拆解

每日晚 8:00 PM (EDT) 定时更新！
包含 1080p 深度精讲大班课 与 9:16 沉浸式口语跟读短视频！
欢迎订阅 @TokyoFlowJapan，开启你的真实东京实景日语之旅！

#日语学习 #JLPT #东京实景 #日语口语 #东京 #TokyoFlow"""

    tags_zh = ["TokyoFlow", "日语学习", "日本语", "JLPT", "JLPT N5", "JLPT N4", "东京", "场景日语", "日语口语", "日语听力", "跟读", "居酒屋日语", "便利店日语"]

    try:
        vid_zh = upload_video_package(
            yt=yt,
            video_path=TRAILER_ZH_DIR / "tokyoflow_trailer_zh_1080p.mp4",
            thumb_path=TRAILER_ZH_DIR / "thumbnail.jpg",
            title=title_zh,
            description=desc_zh,
            tags=tags_zh,
            lang="zh",
            playlist_id="PLVchR4TmK56E"
        )
    except HttpError as e:
        print(f"\n[HTTP Error on Chinese Trailer]: {e}")
        vid_zh = None

    print("\n==================================================")
    if vid_en and vid_zh:
        print("Both English & Chinese Trailers uploaded successfully!")
        print(f"EN Trailer: https://youtu.be/{vid_en}")
        print(f"ZH Trailer: https://youtu.be/{vid_zh}")
    else:
        print("Upload status summary completed.")

if __name__ == "__main__":
    main()
