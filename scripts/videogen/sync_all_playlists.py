#!/usr/bin/env python3
"""
TokyoFlow Japanese • Dual-Language Strict Playlist Isolation & Synchronization Engine
=====================================================================================
Strict Isolation Rules:
1. Column A (English Edition - Teaching):
   - English Masterclasses (16:9 Long): PLHUEYGzrBe-s
   - English Shorts (9:16 Vertical): PLVxXRTmSmcAM
   - English JLPT Playlists:
     * JLPT N5: PLY_ZLcqTrnU8
     * JLPT N4: PLIiV1gnNj8Ms
     * JLPT N3: PLFBaqxuiTcbo
     * JLPT N2-N1: PLeb_7jP3fQ2M
   - English Scenario Playlists:
     * Tokyo Transit & Station Japanese: PLAUUBQzM_liE
     * Kombini & Street Survival Japanese: PLBhQ4N46ef1k
     * Izakaya & Tokyo Foodie Japanese: PLA-JfaJhOu2E
     * Anime & Tokyo Shopping Japanese: PLPigp6inTnV8
     * NHK Daily News & Shadowing Drills: PLHPFg4RJy4Po

2. Column B (Chinese Edition - Teaching):
   - Chinese Masterclasses (16:9 Long): PLVchR4TmK56E
   - Chinese Shorts (9:16 Vertical): PLTpb6FPYqYC4
   - Chinese JLPT Playlists:
     * 【JLPT N5】零基础东京实景日语精讲【中文解说版】: PLPBpfF_GX60Q
     * 【JLPT N4】实用东京日常口语与生活进阶【中文解说版】: PLNFRI1RlIvIU
     * 【JLPT N3】中级新闻时事与地道表达【中文解说版】: PLHeOP0in6rRg
     * 【JLPT N2-N1】高级日本职场与深度表达【中文解说版】: PLRh0i-oZUcq8
   - Chinese Scenario Playlists:
     * 【东京出行】东京交通与车站乘车实景精讲【中文解说版】: PLdc0-MFoSiCc
     * 【街头生存】便利店与生活消费实景精讲【中文解说版】: PLPDcqCSXjUWc
     * 【美食点单】居酒屋与东京美食实景精讲【中文解说版】: PLRNRaN1g4Jac
     * 【流行文化】动漫圣地与秋叶原购物实景精讲【中文解说版】: PLdgqOJf2bv54
     * 【时事新闻】每日日本热点与原声影子跟读【中文解说版】: PLMIm06SWP2NE

3. Dedicated Promotional & Preview Playlists (NO TEACHING LESSONS):
   - English Trailers: PLMsazYTqnfLA (TokyoFlow Official Trailers & Channel Previews [English Edition])
   - Chinese Trailers: PLehSqEkAOYqk (TokyoFlow 官方宣传片与频道预告【中文版】)

STRICT RULES:
- English educational videos MUST NEVER enter Chinese playlists.
- Chinese educational videos MUST NEVER enter English playlists.
- Trailers and previews MUST ONLY enter the dedicated trailer playlists, and MUST NEVER be added to any teaching playlists.
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_auth import get_authenticated_service

ENGLISH_TEACHING_PLAYLISTS = {
    "long": "PLHUEYGzrBe-s",
    "short": "PLVxXRTmSmcAM",
    "n5": "PLY_ZLcqTrnU8",
    "n4": "PLIiV1gnNj8Ms",
    "n3": "PLFBaqxuiTcbo",
    "n2_n1": "PLeb_7jP3fQ2M",
    "transit": "PLAUUBQzM_liE",
    "kombini": "PLBhQ4N46ef1k",
    "dining": "PLA-JfaJhOu2E",
    "shopping": "PLPigp6inTnV8",
    "news": "PLHPFg4RJy4Po"
}

CHINESE_TEACHING_PLAYLISTS = {
    "long": "PLVchR4TmK56E",
    "short": "PLTpb6FPYqYC4",
    "n5": "PLPBpfF_GX60Q",
    "n4": "PLNFRI1RlIvIU",
    "n3": "PLHeOP0in6rRg",
    "n2_n1": "PLRh0i-oZUcq8",
    "transit": "PLdc0-MFoSiCc",
    "kombini": "PLPDcqCSXjUWc",
    "dining": "PLRNRaN1g4Jac",
    "shopping": "PLdgqOJf2bv54",
    "news": "PLMIm06SWP2NE"
}

TRAILER_PLAYLISTS = {
    "en": "PLMsazYTqnfLA",
    "zh": "PLehSqEkAOYqk"
}

ALL_TEACHING_PL_IDS = set(ENGLISH_TEACHING_PLAYLISTS.values()) | set(CHINESE_TEACHING_PLAYLISTS.values())
ALL_TRAILER_PL_IDS = set(TRAILER_PLAYLISTS.values())
ALL_ENGLISH_PL_IDS = set(ENGLISH_TEACHING_PLAYLISTS.values()) | {TRAILER_PLAYLISTS["en"]}
ALL_CHINESE_PL_IDS = set(CHINESE_TEACHING_PLAYLISTS.values()) | {TRAILER_PLAYLISTS["zh"]}

def is_promotional_trailer(title: str) -> bool:
    """Detects if video is an official channel trailer, preview, or overarching study roadmap."""
    t_lower = title.lower()
    return any(k in t_lower for k in [
        "official tokyoflow academy trailer",
        "official channel trailer",
        "complete study guide & shadowing roadmap",
        "官方中文预告",
        "官方学习指南",
        "中文首发",
        "trailer"
    ])

def determine_video_properties(title: str, is_zh_hint: bool = False, format_hint: str = ""):
    """Classifies video language, format (long/short), JLPT level, scenario topic, and trailer status."""
    is_trailer = is_promotional_trailer(title)
    
    # 1. Language Detection
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", title))
    is_zh = is_zh_hint or ("【" in title and "】" in title and ("精讲" in title or "跟读" in title or "解说" in title or "-zh" in title or "预告" in title or "指南" in title or "首发" in title or has_cjk))
    if "English Edition" in title or "Masterclass" in title or "Real Japanese Breakdown" in title or "Academy Trailer" in title or "Study Guide & Shadowing Roadmap" in title:
        is_zh = False

    # 2. Format (Long vs Short)
    is_short = ("#SHORTS" in title.upper() or "SH." in title or format_hint == "short")
    if "#SHORTS" in title.upper() or (title.startswith("【JLPT") and "#Shorts" in title):
        is_short = True

    # 3. JLPT Level
    jlpt = "N5"
    if "N4" in title:
        jlpt = "N4"
    elif "N3" in title:
        jlpt = "N3"
    elif "N2" in title or "N1" in title:
        jlpt = "N2_N1"

    # 4. Scenario Topic
    t_lower = title.lower()
    topic = "transit"
    if any(k in t_lower for k in ["kombini", "convenience", "checkout", "coffee", "atm", "便利店", "取现"]):
        topic = "kombini"
    elif any(k in t_lower for k in ["izakaya", "ramen", "gyudon", "dining", "food", "居酒屋", "拉面", "牛丼", "美食"]):
        topic = "dining"
    elif any(k in t_lower for k in ["akiba", "anime", "shopping", "figure", "taxfree", "tax-free", "秋叶原", "手办", "免税", "动漫"]):
        topic = "shopping"
    elif any(k in t_lower for k in ["news", "broadcast", "suicide", "audible", "robot", "apple", "新闻", "苹果", "机器人", "热点", "绫濑遥"]):
        topic = "news"
    elif any(k in t_lower for k in ["transit", "suica", "station", "subway", "train", "yamanote", "shinkansen", "交通", "地铁", "西瓜卡", "乘车", "换乘", "补票"]):
        topic = "transit"

    return {
        "is_trailer": is_trailer,
        "is_zh": is_zh,
        "is_short": is_short,
        "jlpt": jlpt,
        "topic": topic
    }

def sync_and_clean_playlists():
    print("==================================================")
    print("TokyoFlow Dual-Language Playlist Audit & Separation")
    print("Zero Cross-Contamination & Strict Trailer Isolation")
    print("==================================================")

    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    # 1. Fetch all playlist items on channel
    all_pl_res = yt.playlists().list(part="id,snippet", mine=True, maxResults=50).execute()
    playlists_map = {pl["id"]: pl["snippet"]["title"] for pl in all_pl_res.get("items", [])}

    playlist_items = {}
    for pl_id, pl_title in playlists_map.items():
        vids = {}
        page_token = None
        while True:
            res = yt.playlistItems().list(
                part="id,snippet,contentDetails",
                playlistId=pl_id,
                maxResults=50,
                pageToken=page_token
            ).execute()
            for item in res.get("items", []):
                vid = item["contentDetails"].get("videoId")
                item_id = item["id"]
                if vid:
                    vids[vid] = item_id
            page_token = res.get("nextPageToken")
            if not page_token:
                break
        playlist_items[pl_id] = vids
        print(f"Playlist: {pl_title} ({pl_id}) -> {len(vids)} videos")

    # 2. Fetch all channel uploads
    ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    channel_videos = []
    page_token = None
    while True:
        res = yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_id,
            maxResults=50,
            pageToken=page_token
        ).execute()
        for item in res.get("items", []):
            vid = item["contentDetails"].get("videoId")
            title = item["snippet"].get("title", "")
            channel_videos.append({"id": vid, "title": title})
        page_token = res.get("nextPageToken")
        if not page_token:
            break

    print(f"\nTotal channel videos detected: {len(channel_videos)}")

    # 3. Clean up Cross-Contamination & Trailers in Teaching Playlists
    print("\n--- Auditing Cross-Contamination & Trailer Isolation ---")
    for v in channel_videos:
        vid = v["id"]
        title = v["title"]
        props = determine_video_properties(title)
        
        # Rule 1: If it is a promotional trailer, remove from ALL teaching playlists
        if props["is_trailer"]:
            for teach_pl_id in ALL_TEACHING_PL_IDS:
                if teach_pl_id in playlist_items and vid in playlist_items[teach_pl_id]:
                    item_id = playlist_items[teach_pl_id][vid]
                    print(f"  [TRAILER CLEANUP] Removing trailer [{vid}: {title[:30]}] from teaching playlist {playlists_map.get(teach_pl_id, teach_pl_id)}...")
                    try:
                        yt.playlistItems().delete(id=item_id).execute()
                        del playlist_items[teach_pl_id][vid]
                        print("    [OK] Removed successfully.")
                    except Exception as e:
                        print(f"    [Notice] {e}")
            continue

        # Rule 2: If it is a regular teaching video, remove from trailer playlists
        for trail_pl_id in ALL_TRAILER_PL_IDS:
            if trail_pl_id in playlist_items and vid in playlist_items[trail_pl_id]:
                item_id = playlist_items[trail_pl_id][vid]
                print(f"  [LESSON CLEANUP] Removing lesson [{vid}: {title[:30]}] from trailer playlist {playlists_map.get(trail_pl_id, trail_pl_id)}...")
                try:
                    yt.playlistItems().delete(id=item_id).execute()
                    del playlist_items[trail_pl_id][vid]
                    print("    [OK] Removed successfully.")
                except Exception as e:
                    print(f"    [Notice] {e}")

        # Rule 3: Chinese vs English Language Isolation
        if props["is_zh"]:
            for eng_pl_id in ALL_ENGLISH_PL_IDS:
                if eng_pl_id in playlist_items and vid in playlist_items[eng_pl_id]:
                    item_id = playlist_items[eng_pl_id][vid]
                    print(f"  [LANGUAGE CLEANUP] Removing Chinese video [{vid}: {title[:30]}] from English playlist {playlists_map.get(eng_pl_id, eng_pl_id)}...")
                    try:
                        yt.playlistItems().delete(id=item_id).execute()
                        del playlist_items[eng_pl_id][vid]
                        print("    [OK] Removed successfully.")
                    except Exception as e:
                        print(f"    [Notice] {e}")
        else:
            for zh_pl_id in ALL_CHINESE_PL_IDS:
                if zh_pl_id in playlist_items and vid in playlist_items[zh_pl_id]:
                    item_id = playlist_items[zh_pl_id][vid]
                    print(f"  [LANGUAGE CLEANUP] Removing English video [{vid}: {title[:30]}] from Chinese playlist {playlists_map.get(zh_pl_id, zh_pl_id)}...")
                    try:
                        yt.playlistItems().delete(id=item_id).execute()
                        del playlist_items[zh_pl_id][vid]
                        print("    [OK] Removed successfully.")
                    except Exception as e:
                        print(f"    [Notice] {e}")

    # 4. Categorize Videos into Matching Playlists
    print("\n--- Categorizing Videos to Proper Dedicated Playlists ---")
    for v in channel_videos:
        vid = v["id"]
        title = v["title"]
        props = determine_video_properties(title)
        
        # If it's a trailer, place ONLY into the respective trailer playlist
        if props["is_trailer"]:
            target_trail_id = TRAILER_PLAYLISTS["zh"] if props["is_zh"] else TRAILER_PLAYLISTS["en"]
            if target_trail_id not in playlist_items:
                playlist_items[target_trail_id] = {}
            if vid not in playlist_items[target_trail_id]:
                pl_name = playlists_map.get(target_trail_id, target_trail_id)
                print(f"Adding Trailer [{vid}: {title[:35]}] -> [{pl_name}]...")
                try:
                    yt.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": target_trail_id,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": vid
                                }
                            }
                        }
                    ).execute()
                    playlist_items[target_trail_id][vid] = "newly_added"
                    time.sleep(0.4)
                except Exception as e:
                    print(f"  Notice adding {vid} to {target_trail_id}: {e}")
            continue

        # Regular Teaching Lessons:
        target_pl_dict = CHINESE_TEACHING_PLAYLISTS if props["is_zh"] else ENGLISH_TEACHING_PLAYLISTS
        
        # a) Format playlist (Long or Short)
        format_pl = target_pl_dict["short"] if props["is_short"] else target_pl_dict["long"]
        
        # b) JLPT playlist
        jlpt_key = props["jlpt"].lower()
        jlpt_pl = target_pl_dict.get(jlpt_key, target_pl_dict["n5"])
        
        # c) Scenario topic playlist
        topic_key = props["topic"]
        topic_pl = target_pl_dict.get(topic_key, target_pl_dict["transit"])
        
        targets = [format_pl, jlpt_pl, topic_pl]
        
        for pl_id in targets:
            if pl_id not in playlist_items:
                playlist_items[pl_id] = {}
                
            if vid not in playlist_items[pl_id]:
                pl_name = playlists_map.get(pl_id, pl_id)
                print(f"Adding Lesson [{vid}: {title[:35]}] -> [{pl_name}]...")
                try:
                    yt.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": pl_id,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": vid
                                }
                            }
                        }
                    ).execute()
                    playlist_items[pl_id][vid] = "newly_added"
                    time.sleep(0.4)
                except Exception as e:
                    print(f"  Notice adding {vid} to {pl_id}: {e}")

    print("\n==================================================")
    print("Dual-Language Playlist Separation & Trailer Isolation Complete!")
    print("==================================================")

if __name__ == "__main__":
    sync_and_clean_playlists()
