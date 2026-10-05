#!/usr/bin/env python3
"""
TokyoFlow Japanese • Attach Thumbnails and Add Trailers to Playlists
Run after API quota resets or to sync trailer metadata.
"""

import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAILER_EN_DIR = PROJECT_ROOT / "output" / "channel_trailer_en"
TRAILER_ZH_DIR = PROJECT_ROOT / "output" / "channel_trailer_zh"

VID_EN = "EFRVKXcv85M"
VID_ZH = "MkyFXvJrJw4"

PLAYLIST_EN = "PLHUEYGzrBe-s"
PLAYLIST_ZH = "PLVchR4TmK56E"

def sync_trailer(yt, video_id, thumb_path, playlist_id, name):
    print(f"\nProcessing {name} ({video_id})...")
    
    # Set Thumbnail
    if thumb_path.exists():
        print(f"  Setting thumbnail from: {thumb_path}")
        try:
            yt.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumb_path), mimetype="image/jpeg")
            ).execute()
            print("  [OK] Thumbnail updated successfully.")
        except HttpError as e:
            print(f"  [HttpError] Thumbnail update failed: {e}")
    
    # Add to Playlist
    if playlist_id:
        print(f"  Adding to playlist: {playlist_id}")
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
            print("  [OK] Added to playlist.")
        except HttpError as e:
            print(f"  [HttpError] Playlist insertion failed: {e}")

def main():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    sync_trailer(yt, VID_EN, TRAILER_EN_DIR / "thumbnail.jpg", PLAYLIST_EN, "English Trailer")
    sync_trailer(yt, VID_ZH, TRAILER_ZH_DIR / "thumbnail.jpg", PLAYLIST_ZH, "Chinese Trailer")

if __name__ == "__main__":
    main()
