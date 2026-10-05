#!/usr/bin/env python3
"""
TokyoFlow Japanese • Upload Chinese Launch Teaser Video
Uploads the teaser video as a PUBLIC release immediately, sets custom cover thumbnail,
and adds it to both Chinese Masterclass and Chinese Shorts playlists.
"""

import sys
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEASER_DIR = PROJECT_ROOT / "docs" / "youtube_releases" / "E00-Chinese_Launch_Teaser-v1.0-zh"

def upload_teaser():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    video_path = TEASER_DIR / "short.mp4"
    thumb_path = TEASER_DIR / "short_thumbnail.jpg"

    if not video_path.exists():
        print(f"Error: Video file not found at {video_path}")
        return

    title = "【TokyoFlow 中文首发】告别死板教科书！每天1分钟搞定东京地道实景日语 #Shorts"
    description = """TokyoFlow 日语实景精讲【中文解说版】全网正式首发！

告别枯燥死板的教科书，带你直接潜入东京最真实的生活现场：
- 山手线/东京地铁通勤实景
- 7-Eleven/罗森便利店高频应答
- 居酒屋/拉面馆老饕点餐口诀
- 秋叶原/银座免税退税与试衣
- 日本当季热梗与流行语追踪

每晚 8:00 PM (EDT) / 每日早间 定时更新！
包含 1080p 16:9 深度精讲大班课 与 9:16 沉浸式口语跟读 Shorts！
欢迎订阅 TokyoFlow Japanese，开启你的东京实景日语之旅！

#日语学习 #JLPT #东京实景 #日语口语 #Shorts #TokyoFlow"""

    tags = [
        "TokyoFlow", "日语学习", "日本语", "JLPT", "JLPT N5", "JLPT N4",
        "东京", "场景日语", "日语口语", "日语听力", "跟读", "居酒屋日语", "便利店日语"
    ]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27", # Education
            "defaultLanguage": "zh",
            "defaultAudioLanguage": "zh"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print("==================================================")
    print("Uploading Chinese Launch Teaser to YouTube...")
    print("==================================================")
    print(f"Title: {title}")
    print(f"Privacy: PUBLIC (Immediate release)")

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = yt.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
        notifySubscribers=False
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Uploaded {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    print(f"\n[OK] Video successfully uploaded! Video ID: {video_id}")
    print(f"Video URL: https://youtu.be/{video_id}")

    # Set custom thumbnail
    if thumb_path.exists():
        print("Uploading custom thumbnail...")
        try:
            yt.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Custom thumbnail uploaded successfully.")
        except HttpError as e:
            print(f"  [Warning] Thumbnail upload failed: {e}")

    # Add to Chinese Masterclass and Chinese Shorts playlists
    playlists_to_add = [
        ("PLVchR4TmK56E", "TokyoFlow 日语实景精讲【中文解说版】"),
        ("PLTpb6FPYqYC4", "TokyoFlow 日语短视频跟读【中文解说版】")
    ]

    for pl_id, pl_name in playlists_to_add:
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": pl_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print(f"  [OK] Added to playlist: {pl_name} ({pl_id})")
        except Exception as e:
            print(f"  [Warning] Adding to playlist {pl_name} failed: {e}")

    print("\n Chinese Launch Teaser uploaded and deployed successfully!")

if __name__ == "__main__":
    upload_teaser()
