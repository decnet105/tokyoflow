#!/usr/bin/env python3
"""
TokyoFlow YouTube Channel Layout Optimization Engine (V2 - Dual-Language Flagship Architecture)
Ensures immediate visible dual-language entry cards (English & Chinese) at the very top of the homepage,
followed by full-width single playlist feeds, JLPT roadmaps, real-world themes, and popular feeds.
"""

import sys
import json
import time
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

def setup_channel_layout():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    print("==================================================")
    print("TokyoFlow YouTube Channel Layout Automation Engine")
    print("==================================================")

    # 1. Clear old / existing sections
    print("\n[1/3] Clearing previous channel sections...")
    current_sections = yt.channelSections().list(part="id,snippet", mine=True).execute()
    for sec in current_sections.get("items", []):
        sec_id = sec["id"]
        sec_type = sec["snippet"].get("type", "unknown")
        try:
            yt.channelSections().delete(id=sec_id).execute()
            print(f"  Deleted section [{sec_id}] (type: {sec_type})")
            time.sleep(0.3)
        except Exception as e:
            print(f"  Warning deleting section {sec_id}: {e}")

    # 2. Define Tier-1 Channel Section Architecture
    # Section Layout Blueprint:
    # 0: Dual-Language Hub (4 Core Playlists: EN Masterclass, EN Shorts, CN Masterclass, CN Shorts)
    # 1: Masterclass [English Edition] (Full-width video carousel)
    # 2: Japanese Shorts [English Edition] (Full-width shorts carousel)
    # 3: 日语实景精讲【中文解说版】 (Full-width Chinese masterclass)
    # 4: 日语短视频跟读【中文解说版】 (Full-width Chinese shorts)
    # 5: JLPT Roadmaps (N5 Beginner to N1 Advanced)
    # 6: Tokyo Scenarios (Transit, Foodie, Kombini, Anime Shopping)
    # 7: Popular Uploads (Social proof & high retention)

    sections_blueprint = [
        {
            "name": "TokyoFlow Dual-Language Hub (Main Entrances)",
            "body": {
                "snippet": {
                    "type": "multiplePlaylists",
                    "title": "TokyoFlow Official Learning Tracks | 官方双语精讲与跟读专区",
                    "position": 0
                },
                "contentDetails": {
                    "playlists": [
                        "PLHUEYGzrBe-s",  # EN Masterclass
                        "PLVxXRTmSmcAM",  # EN Shorts
                        "PLVchR4TmK56E",  # CN Masterclass
                        "PLTpb6FPYqYC4"   # CN Shorts
                    ]
                }
            }
        },
        {
            "name": "Flagship English Masterclass (Full Row)",
            "body": {
                "snippet": {
                    "type": "singlePlaylist",
                    "position": 1
                },
                "contentDetails": {
                    "playlists": ["PLHUEYGzrBe-s"]
                }
            }
        },
        {
            "name": "English Daily Shorts & Shadowing (Full Row)",
            "body": {
                "snippet": {
                    "type": "singlePlaylist",
                    "position": 2
                },
                "contentDetails": {
                    "playlists": ["PLVxXRTmSmcAM"]
                }
            }
        },
        {
            "name": "Chinese Deep Masterclass (Full Row)",
            "body": {
                "snippet": {
                    "type": "singlePlaylist",
                    "position": 3
                },
                "contentDetails": {
                    "playlists": ["PLVchR4TmK56E"]
                }
            }
        },
        {
            "name": "Chinese Daily Shorts Drills (Full Row)",
            "body": {
                "snippet": {
                    "type": "singlePlaylist",
                    "position": 4
                },
                "contentDetails": {
                    "playlists": ["PLTpb6FPYqYC4"]
                }
            }
        },
        {
            "name": "JLPT Proficiency Progression [N5 - N1]",
            "body": {
                "snippet": {
                    "type": "multiplePlaylists",
                    "title": "JLPT Progression: Zero to Advanced [N5 - N1]",
                    "position": 5
                },
                "contentDetails": {
                    "playlists": [
                        "PLY_ZLcqTrnU8",  # N5
                        "PLIiV1gnNj8Ms",  # N4
                        "PLFBaqxuiTcbo",  # N3
                        "PLeb_7jP3fQ2M"   # N2-N1
                    ]
                }
            }
        },
        {
            "name": "Real-World Tokyo Living & Survival Scenarios",
            "body": {
                "snippet": {
                    "type": "multiplePlaylists",
                    "title": "Real-World Tokyo Living & Culture Scenarios",
                    "position": 6
                },
                "contentDetails": {
                    "playlists": [
                        "PLAUUBQzM_liE",  # Transit & Station
                        "PLA-JfaJhOu2E",  # Izakaya & Foodie
                        "PLBhQ4N46ef1k",  # Kombini & Street
                        "PLPigp6inTnV8"   # Anime & Shopping
                    ]
                }
            }
        },
        {
            "name": "Popular Uploads Feed",
            "body": {
                "snippet": {
                    "type": "popularUploads",
                    "position": 7
                }
            }
        }
    ]

    print("\n[2/3] Creating Tier-1 Dual-Language Channel Layout Sections...")
    for idx, sec in enumerate(sections_blueprint):
        try:
            created = yt.channelSections().insert(
                part="snippet,contentDetails",
                body=sec["body"]
            ).execute()
            print(f"  [OK] Section {idx} created: {sec['name']} (ID: {created['id']})")
            time.sleep(0.4)
        except HttpError as e:
            print(f"  [ERROR] Failed creating section {sec['name']}: {e}")

    # 3. Verify Final Channel Sections Layout
    print("\n[3/3] Verifying Final Channel Layout State...")
    final_sections = yt.channelSections().list(part="id,snippet,contentDetails", mine=True).execute()
    print(f"Total Active Homepage Sections: {len(final_sections.get('items', []))}")
    for item in final_sections.get("items", []):
        snip = item["snippet"]
        title_info = snip.get("title", "")
        pos = snip.get("position", "-")
        stype = snip.get("type", "")
        details = item.get("contentDetails", {})
        print(f"  Pos {pos}: [{stype}] {title_info} -> {details}")

    print("\n Channel Homepage Layout configuration complete.")

if __name__ == "__main__":
    setup_channel_layout()
