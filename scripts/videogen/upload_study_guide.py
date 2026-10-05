#!/usr/bin/env python3
"""
TokyoFlow Japanese • Upload Official Study Guide & Fluency Roadmap Video
Uploads the Study Guide video as PUBLIC with custom thumbnail for returning subscribers.
"""

import sys
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

sys.path.append(str(Path(__file__).resolve().parent))
from youtube_auth import get_authenticated_service

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GUIDE_DIR = PROJECT_ROOT / "output" / "study_guide_en"

def main():
    creds = get_authenticated_service()
    yt = build("youtube", "v3", credentials=creds)

    video_path = GUIDE_DIR / "tokyoflow_study_guide_en_1080p.mp4"
    thumb_path = GUIDE_DIR / "thumbnail.jpg"

    title = "How to Master Real Tokyo Japanese: Complete Study Guide & Shadowing Roadmap [JLPT N5-N1]"
    description = """Welcome to TokyoFlow Japanese — the cinema-grade, use-case-driven language academy dedicated to decoding authentic spoken Tokyo Japanese.

If you have studied traditional grammar for years but still freeze in Tokyo train stations, kombini registers, or izakaya counters, this video is your master blueprint.

In this Official Study Guide & Roadmap, you will learn:
1. The Reality Gap: Why traditional textbook Japanese fails in real-life Tokyo conversations.
2. The 3-Step Mastery Cycle: How to combine 16:9 Scenario Masterclasses with 9:16 Spoken Shadowing Shorts to build rapid vocal muscle memory.
3. The 5-Level JLPT Milestone Roadmap: Structured progression from [JLPT N5] essential survival to [JLPT N1] native news & media nuance.
4. The 15-Minute Daily Pro Routine: How 15 minutes of structured daily exposure compounds into effortless conversational fluency.
5. Curated Playlists & Resources: How to navigate our specialized playlists for transit, dining, shopping, and cultural trends.

---

### Recommended Study Playlists:
- Playlist 1: Transit & Subway Mastery (Yamanote Line, Tokyo Metro, Fare Adjustments)
- Playlist 2: Kombini & Daily Living (7-Eleven, FamilyMart, Cafes, Checkout Speed Replies)
- Playlist 3: Izakaya & Dining Protocols (Draft Beer Orders, Ramen Ticket Machines, Table Etiquette)
- Playlist 4: NHK News & Cultural Trends (Real Broadcasts, Pop Trends, Media Nuance)

Daily Masterclasses released at 08:00 AM EDT.
Subscribe to @TokyoFlowJapan and start mastering real Tokyo Japanese today!

#LearnJapanese #JLPT #TokyoFlow #StudyJapanese #JapaneseShadowing #Tokyo #JLPTN5 #JLPTN4 #JLPTN3 #JLPTN2 #JLPTN1"""

    tags = ["TokyoFlow", "Learn Japanese", "Japanese Study Guide", "Japanese Roadmap", "JLPT", "JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1", "Japanese Shadowing", "Speak Japanese", "Real Japanese", "Tokyo Japanese", "Japanese Pronunciation", "Japanese Listening Practice"]

    print("==================================================")
    print(f"Uploading Study Guide Video: {title}")
    print("==================================================")

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27", # Education
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en"
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
            notifySubscribers=True
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"  Progress: {int(status.progress() * 100)}%...")

        video_id = response.get("id")
        print(f"\n[OK] Study Guide Video uploaded successfully! ID: {video_id}")
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

        # Add to English masterclass playlist
        try:
            yt.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": "PLHUEYGzrBe-s",
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print("  [OK] Added to English Masterclass Playlist (PLHUEYGzrBe-s).")
        except HttpError as e:
            print(f"  [Warning] Adding to playlist failed: {e}")

        return video_id

    except HttpError as e:
        print(f"\n[HTTP Error on Upload]: {e}")
        return None

if __name__ == "__main__":
    main()
