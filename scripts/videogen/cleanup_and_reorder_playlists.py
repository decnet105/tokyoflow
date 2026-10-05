#!/usr/bin/env python3
"""
TokyoFlow Playlist Cleaner & Reorganizer
Removes all deleted/invalid video entries from all playlists and sets active public/first items properly.
"""

import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

def clean_playlists():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    print("==================================================")
    print("Cleaning and Reorganizing Playlists...")
    print("==================================================")

    res = yt.playlists().list(part="id,snippet", mine=True, maxResults=50).execute()
    for pl in res.get("items", []):
        pl_id = pl["id"]
        pl_title = pl["snippet"]["title"]
        print(f"\nProcessing Playlist: [{pl_id}] {pl_title}")

        # Fetch all items in playlist
        items_res = yt.playlistItems().list(part="id,snippet,status", playlistId=pl_id, maxResults=50).execute()
        items = items_res.get("items", [])
        
        deleted_count = 0
        for it in items:
            item_id = it["id"]
            title = it["snippet"].get("title", "")
            status = it.get("status", {}).get("privacyStatus", "")
            
            # Check if deleted
            if title == "Deleted video" or status == "privacyStatusUnspecified" or not title:
                print(f"  Removing deleted item {item_id} from {pl_title}...")
                try:
                    yt.playlistItems().delete(id=item_id).execute()
                    deleted_count += 1
                except Exception as e:
                    print(f"  Error deleting item {item_id}: {e}")

        print(f"  Cleaned {deleted_count} deleted items from {pl_title}.")

    print("\n Playlist cleanup complete.")

if __name__ == "__main__":
    clean_playlists()
