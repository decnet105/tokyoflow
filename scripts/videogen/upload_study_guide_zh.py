#!/usr/bin/env python3
"""
TokyoFlow Japanese • Upload Official Chinese Study Guide & Roadmap Video
Uploads the Chinese Study Guide video as PUBLIC with custom thumbnail.
"""

import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GUIDE_ZH_DIR = PROJECT_ROOT / "output" / "study_guide_zh"

def main():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    video_path = GUIDE_ZH_DIR / "tokyoflow_study_guide_zh_1080p.mp4"
    thumb_path = GUIDE_ZH_DIR / "thumbnail.jpg"

    title = "【TokyoFlow 官方学习指南】告别死板教材！东京实景日语学习法与进阶大纲【JLPT N5-N1】"
    description = """欢迎来到 TokyoFlow 日语实景精讲【中文解说版】！

如果你学了多年死板语法，但在东京街头面对店员提问依然会瞬间卡壳，这支视频将为你提供完整的实景日语破局方案。

在本期官方指南与路线图中，你将掌握：
1. 告别哑巴日语：为什么传统教材在真实东京街头会失效
2. 三步掌握闭环：1080p 大班课沉浸、句型文化拆解、9:16 短视频声带肌肉跟读（Shadowing）
3. 五阶段 JLPT 进阶路线图：从【JLPT N5】基础生存到【JLPT N1】NHK 原声新闻解码
4. 每日 15 分钟高能闭环：小步高频重复，构建终身语言神经反射
5. 主题播单与资源索引：如何高效利用交通出行、便利店生活、居酒屋餐饮等专栏

---

### 推荐学习播单：
- 播单 01：交通出行与山手线实景（山手线报站、地铁换乘、闸机补票）
- 播单 02：便利店与街头生活（7-Eleven、全家、咖啡点单、结账秒回）
- 播单 03：居酒屋与地道美食（生啤开场、拉面食券机定制、餐桌礼仪）
- 播单 04：NHK新闻与流行文化（原声新闻听力、网络流行语、当季热点）

每日晚 08:00 PM (EDT) 定时更新！
欢迎订阅 @TokyoFlowJapan，开启你的真实东京实景日语之旅！

#日语学习 #JLPT #东京实景 #日语口语 #东京 #TokyoFlow #JLPTN5 #JLPTN4 #JLPTN3 #JLPTN2 #JLPTN1"""

    tags = ["TokyoFlow", "日语学习", "日本语", "JLPT", "JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1", "东京", "场景日语", "日语口语", "日语听力", "跟读", "居酒屋日语", "便利店日语"]

    print("==================================================")
    print(f"Uploading Chinese Study Guide Video: {title}")
    print("==================================================")

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

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    try:
        request = yt.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
            notifySubscribers=False # Column B Chinese release cadence rule
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  Progress: {int(status.progress() * 100)}%...")

        video_id = response.get("id")
        print(f"\n[OK] Chinese Study Guide Video uploaded successfully! ID: {video_id}")
        print(f"URL: https://youtu.be/{video_id}")

        # Set thumbnail
        if thumb_path.exists():
            print("  Uploading custom thumbnail...")
            try:
                yt.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
                ).execute()
                print("  [OK] Custom thumbnail uploaded successfully.")
            except HttpError as e:
                print(f"  [Warning] Thumbnail upload failed: {e}")

        # Add to Chinese masterclass playlist
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": "PLVchR4TmK56E",
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print("  [OK] Added to Chinese Masterclass Playlist (PLVchR4TmK56E).")
        except HttpError as e:
            print(f"  [Warning] Adding to playlist failed: {e}")

        return video_id

    except HttpError as e:
        print(f"\n[HTTP Error on Upload]: {e}")
        return None

if __name__ == "__main__":
    main()
