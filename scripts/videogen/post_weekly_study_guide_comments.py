#!/usr/bin/env python3
"""
TokyoFlow Japanese • Automated Study Companion Comment Publisher
================================================================
Posts Scheme D pinned comments / download instructions to YouTube videos using the YouTube Data API.
- English Edition: Links to TokyoFlow_Week01_JLPT_Master_Workbook.pdf (Drive) + Passcode TOKYOFLOW-WEEK1
- Chinese Edition: Links to TokyoFlow_第一周_JLPT实景学习讲义与复习手册.pdf (Drive) + Passcode TOKYOFLOW-WEEK1
- 100% Zero-Emoji discipline.
"""

import os
import sys
import json
import time
from pathlib import Path
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_auth import get_authenticated_service

LEDGER_FILE = PROJECT_ROOT / "docs" / "shared" / "publish_ledger.json"

DRIVE_LINK_EN = "https://drive.google.com/file/d/1lfD3p_xXnwMmyuryRbzgn6kR232rcBs5/view?usp=drivesdk"
DRIVE_LINK_ZH = "https://drive.google.com/file/d/1QGhX4br_Vi-GugGTGmck_2-iV_2DzbDu/view?usp=drivesdk"
PASSCODE = "TOKYOFLOW-WEEK1"

COMMENT_EN = f"""Thank you for watching TokyoFlow!
You can download the complete Week 1 JLPT Study Workbook (PDF) from our Google Drive:
Link: {DRIVE_LINK_EN}
Unlock Passcode: {PASSCODE}

- Complete 42 dialogue lines with Furigana & Romaji
- Classified Vocabulary & Grammar tables [JLPT N5, N4, N3]
- 100% Free for TokyoFlow Subscribers (Print-Friendly A4)

Remember to SUBSCRIBE to the channel for daily Tokyo immersion masterclasses and shadowing drills!"""

COMMENT_ZH = f"""感谢观看 TokyoFlow 日语实景精讲！
第一周完整配套研习讲义与 JLPT 复习手册已更新至网盘：
下载链接：{DRIVE_LINK_ZH}
视频完播口令：{PASSCODE}

- 严格按照【JLPT N5】【JLPT N4】【JLPT N3】分级归纳
- 包含 7 大场景 42 组全台词、假名注音与语法接续详解
- 订阅学员免费保存与打印学习

记得点击【订阅】TokyoFlow 官方频道并开启小铃铛，每日打卡实景跟读训练！"""

def post_comment(youtube, video_id: str, text: str, video_title: str):
    print(f">> Posting comment to video: {video_id} ({video_title})...")
    try:
        req = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": text
                        }
                    }
                }
            }
        )
        res = req.execute()
        comment_id = res.get("id")
        print(f"   [SUCCESS] Comment posted! Thread ID: {comment_id}")
        return comment_id
    except Exception as e:
        print(f"   [ERROR] Failed to post comment on {video_id}: {e}")
        return None

def main():
    print("==================================================")
    print("TokyoFlow Automated YouTube Comment Publisher")
    print("Zero-Emoji Discipline | Scheme D Passcode Distribution")
    print("==================================================")
    
    if not LEDGER_FILE.exists():
        print(f"Error: Ledger file not found at {LEDGER_FILE}")
        return

    ledger_data = json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
    published = ledger_data.get("published", {})
    
    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)

    posted_count = 0
    
    # Process all published videos
    for key, item in published.items():
        video_id = item.get("video_id")
        title = item.get("title", "")
        if not video_id:
            continue
            
        # Determine language edition
        is_zh = "-zh" in key or "中文" in title or "【JLPT" in title
        comment_body = COMMENT_ZH if is_zh else COMMENT_EN
        
        # We target Week 1 masterclasses (E01-E08, WM01, WL01) and trailer
        target_keys = ["E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "WM01", "WL01", "trailer", "Teaser"]
        if any(tk in key for tk in target_keys):
            print(f"\nProcessing Key: {key}")
            c_id = post_comment(youtube, video_id, comment_body, title)
            if c_id:
                posted_count += 1
                item["study_comment_id"] = c_id
            time.sleep(1) # rate-limiting buffer

    # Save updated ledger
    LEDGER_FILE.write_text(json.dumps(ledger_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n==================================================")
    print(f"Successfully posted comments to {posted_count} videos.")
    print("Updated publish_ledger.json with comment records.")
    print("==================================================")

if __name__ == "__main__":
    main()
