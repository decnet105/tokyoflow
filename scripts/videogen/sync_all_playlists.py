#!/usr/bin/env python3
"""
TokyoFlow Japanese • Complete Playlist Synchronization Engine
==============================================================
Audits every video uploaded to the official YouTube channel and ensures it is
accurately added to its corresponding playlists:

1. Language Column Playlists:
   - English Masterclass (16:9 Long): PLHUEYGzrBe-s
   - English Shorts (9:16 Vertical): PLVxXRTmSmcAM
   - Chinese Masterclass (16:9 Long): PLVchR4TmK56E
   - Chinese Shorts (9:16 Vertical): PLTpb6FPYqYC4

2. Dedicated JLPT Playlists (English Column):
   - JLPT N5: PLY_ZLcqTrnU8
   - JLPT N4: PLIiV1gnNj8Ms
   - JLPT N3: PLFBaqxuiTcbo
   - JLPT N2-N1: PLeb_7jP3fQ2M

3. Scenario / Theme Playlists (English Column):
   - Tokyo Transit & Station Japanese: PLAUUBQzM_liE
   - Kombini & Street Survival Japanese: PLBhQ4N46ef1k
   - Izakaya & Tokyo Foodie Japanese: PLA-JfaJhOu2E
   - Anime & Tokyo Shopping Japanese: PLPigp6inTnV8
   - NHK Daily News & Shadowing Drills: PLHPFg4RJy4Po
"""

import os
import sys
import re
from pathlib import Path
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_auth import get_authenticated_service

PLAYLIST_IDS = {
    "en_long": "PLHUEYGzrBe-s",
    "en_short": "PLVxXRTmSmcAM",
    "zh_long": "PLVchR4TmK56E",
    "zh_short": "PLTpb6FPYqYC4",
    "jlpt_n5": "PLY_ZLcqTrnU8",
    "jlpt_n4": "PLIiV1gnNj8Ms",
    "jlpt_n3": "PLFBaqxuiTcbo",
    "jlpt_n2_n1": "PLeb_7jP3fQ2M",
    "transit": "PLAUUBQzM_liE",
    "kombini": "PLBhQ4N46ef1k",
    "dining": "PLA-JfaJhOu2E",
    "shopping": "PLPigp6inTnV8",
    "news": "PLHPFg4RJy4Po"
}

def sync_playlists():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    print("==================================================")
    print("Auditing & Synchronizing YouTube Playlists")
    print("==================================================")

    # 1. Fetch current items in all playlists
    playlist_contents = {}
    res = yt.playlists().list(part="id,snippet", mine=True, maxResults=50).execute()
    for pl in res.get("items", []):
        pl_id = pl["id"]
        pl_title = pl["snippet"]["title"]
        items = set()
        page_token = None
        while True:
            it_res = yt.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=pl_id,
                maxResults=50,
                pageToken=page_token
            ).execute()
            for item in it_res.get("items", []):
                vid = item["contentDetails"].get("videoId")
                if vid:
                    items.add(vid)
            page_token = it_res.get("nextPageToken")
            if not page_token:
                break
        playlist_contents[pl_id] = {"title": pl_title, "videos": items}

    # 2. Fetch all channel uploads
    ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    all_uploads = []
    page_token = None
    while True:
        it_res = yt.playlistItems().list(
            part="snippet,contentDetails,status",
            playlistId=uploads_id,
            maxResults=50,
            pageToken=page_token
        ).execute()
        for item in it_res.get("items", []):
            snip = item["snippet"]
            all_uploads.append({
                "video_id": item["contentDetails"]["videoId"],
                "title": snip["title"],
                "description": snip.get("description", ""),
                "status": item.get("status", {}).get("privacyStatus", "")
            })
        page_token = it_res.get("nextPageToken")
        if not page_token:
            break

    print(f"Total uploaded videos found: {len(all_uploads)}")

    def add_to_playlist(vid: str, pl_id: str, label: str):
        if vid in playlist_contents.get(pl_id, {}).get("videos", set()):
            return
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
            playlist_contents[pl_id]["videos"].add(vid)
            print(f"  [ADDED] {vid} -> {label} ({pl_id})")
        except Exception as e:
            print(f"  [ERROR] Adding {vid} to {label} ({pl_id}): {e}")

    # 3. Classify and route each video
    for u in all_uploads:
        vid = u["video_id"]
        title = u["title"]
        desc = u["description"]

        is_zh = ("【" in title) or ("中文" in title) or ("精讲" in title) or ("跟读" in title) or ("指南" in title)
        is_short = ("#Shorts" in title) or ("#shorts" in title) or ("SH." in title) or ("WS." in title)

        print(f"\nEvaluating: [{vid}] {title}")

        if is_zh:
            if is_short:
                add_to_playlist(vid, PLAYLIST_IDS["zh_short"], "TokyoFlow 日语短视频跟读【中文解说版】")
            else:
                add_to_playlist(vid, PLAYLIST_IDS["zh_long"], "TokyoFlow 日语实景精讲【中文解说版】")
        else:
            # English Column
            if is_short:
                add_to_playlist(vid, PLAYLIST_IDS["en_short"], "TokyoFlow Japanese Shorts [English Edition]")
            else:
                add_to_playlist(vid, PLAYLIST_IDS["en_long"], "TokyoFlow Japanese Masterclass [English Edition]")

            # JLPT Routing
            title_upper = title.upper()
            if "N5" in title_upper:
                add_to_playlist(vid, PLAYLIST_IDS["jlpt_n5"], "JLPT N5")
            elif "N4" in title_upper:
                add_to_playlist(vid, PLAYLIST_IDS["jlpt_n4"], "JLPT N4")
            elif "N3" in title_upper:
                add_to_playlist(vid, PLAYLIST_IDS["jlpt_n3"], "JLPT N3")
            elif "N2" in title_upper or "N1" in title_upper:
                add_to_playlist(vid, PLAYLIST_IDS["jlpt_n2_n1"], "JLPT N2-N1")

            # Scenario Routing
            t_lower = title.lower() + " " + desc.lower()
            if any(k in t_lower for k in ["transit", "subway", "train", "yamanote", "station", "platform"]):
                add_to_playlist(vid, PLAYLIST_IDS["transit"], "Tokyo Transit & Station")
            if any(k in t_lower for k in ["kombini", "7-eleven", "familymart", "lawson", "checkout", "convenience"]):
                add_to_playlist(vid, PLAYLIST_IDS["kombini"], "Kombini & Street Survival")
            if any(k in t_lower for k in ["izakaya", "ramen", "foodie", "dining", "beer", "yakitori"]):
                add_to_playlist(vid, PLAYLIST_IDS["dining"], "Izakaya & Tokyo Foodie")
            if any(k in t_lower for k in ["akiba", "akihabara", "anime", "sauna", "shopping", "ginza", "figure"]):
                add_to_playlist(vid, PLAYLIST_IDS["shopping"], "Anime & Tokyo Shopping")

    print("\n==================================================")
    print("Playlist Synchronization Finished Successfully!")
    print("==================================================")

if __name__ == "__main__":
    sync_playlists()
