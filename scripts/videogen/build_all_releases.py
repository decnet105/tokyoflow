#!/usr/bin/env python3
"""
TokyoFlow Japanese • Unified YouTube Release Packager
Generates standardized release directories for all episodes under `docs/youtube_releases/`:
- ep01_yamanote_transit
- ep02_kombini_checkout
- ep03_izakaya_night
- ep04_akiba_pilgrimage

Each directory strictly contains:
1. `video.mp4` - 1080p Full HD video
2. `thumbnail.jpg` - 1920x1080 high-CTR serialized thumbnail
3. `metadata.md` - Complete YouTube Studio metadata (Title, Description, Chapters, Tags, Pinned Comment)
4. `script.json` - Bilingual slide transcript and spoken voice text
"""

import os
import sys
import json
import shutil
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

async def generate_speech_audio(text: str, voice: str, out_path: str, rate: str = "-6%", pitch: str = "+3Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

def create_slide_image(
    title_category: str,
    title_main: str,
    japanese_text: str,
    furigana_text: str,
    english_text: str,
    tip_text: str,
    chapter_label: str,
    out_img_path: str,
    is_outro: bool = False
):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 249, 252))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw.rectangle([(0, 0), (width, 80)], fill=(22, 28, 45))
    font_brand = get_font(28)
    draw.text((60, 24), "TokyoFlow Japanese  |  Real-Life Tokyo Japanese Academy", fill=(255, 255, 255), font=font_brand)
    font_badge = get_font(22)
    draw.text((width - 340, 26), f"Chapter: {chapter_label}", fill=(244, 114, 182), font=font_badge)

    if is_outro:
        draw.rectangle([(160, 160), (width - 160, height - 120)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)
        font_hero = get_font(54)
        draw.text((220, 230), "Subscribe to TokyoFlow Japanese on YouTube", fill=(220, 38, 38), font=font_hero)
        font_sub = get_font(34)
        draw.text((220, 320), "Learn Natural Tokyo Japanese Through Real-Life Scenarios", fill=(30, 41, 59), font=font_sub)
        
        font_bullets = get_font(28)
        draw.text((220, 420), "✓ 20+ Real Tokyo Life Scenarios (Transit, Kombini, Izakaya, Akiba)", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 490), "✓ Native Audio VoiceBank • Pitch Accent & Intonation Guides", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 560), "✓ 2,600+ JLPT N5-N1 Core Vocabulary & Scenario Drills", fill=(71, 85, 105), font=font_bullets)
        
        draw.rectangle([(220, 660), (width - 220, 840)], fill=(239, 246, 255), outline=(191, 219, 254), width=3)
        font_app = get_font(34)
        draw.text((260, 695), "📱 Download 'TokyoFlow' Free on the iOS App Store", fill=(37, 99, 235), font=font_app)
        font_app_sub = get_font(24)
        draw.text((260, 760), "Pair with iOS App for Voice Shadowing Scoring, Kana Practice & SRS Flashcards", fill=(100, 116, 139), font=font_app_sub)
    else:
        # Category Badge
        font_cat = get_font(24)
        draw.rectangle([(120, 120), (520, 165)], fill=(238, 242, 255))
        draw.text((135, 128), title_category, fill=(79, 70, 229), font=font_cat)

        font_title = get_font(38)
        draw.text((120, 190), title_main, fill=(15, 23, 42), font=font_title)

        draw.rectangle([(120, 270), (width - 120, 720)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)

        if furigana_text:
            font_furi = get_font(30)
            draw.text((180, 320), furigana_text, fill=(100, 116, 139), font=font_furi)

        font_jp = get_font(50)
        draw.text((180, 380), japanese_text, fill=(15, 23, 42), font=font_jp)

        draw.line([(180, 480), (width - 180, 480)], fill=(241, 245, 249), width=3)

        font_en = get_font(34)
        draw.text((180, 515), f"Meaning:  {english_text}", fill=(30, 41, 59), font=font_en)

        font_tip = get_font(26)
        draw.text((180, 595), f"💡 Pro-Tip:  {tip_text}", fill=(16, 185, 129), font=font_tip)

        draw.rectangle([(120, 770), (width - 120, 920)], fill=(241, 245, 249), outline=(226, 232, 240), width=2)
        font_shadow = get_font(28)
        draw.text((160, 805), "🗣️  Shadowing Drill: Repeat aloud with native timing and pitch accent", fill=(51, 65, 85), font=font_shadow)
        font_shadow_sub = get_font(22)
        draw.text((160, 860), "Native Audio: Nanami (Tokyo Standard) • Real-life context breakdown", fill=(100, 116, 139), font=font_shadow_sub)

    img.save(out_img_path, quality=95)

def render_scene_video(img_path: str, audio_path: str, duration: float, out_mp4_path: str):
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration + 0.5),
        "-shortest",
        out_mp4_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def concat_videos(video_list: list, final_output_path: str):
    concat_txt_path = "tmp/videogen/concat_list.txt"
    os.makedirs(os.path.dirname(concat_txt_path), exist_ok=True)
    with open(concat_txt_path, "w") as f:
        for v in video_list:
            f.write(f"file '{os.path.abspath(v)}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c", "copy",
        final_output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

from generate_thumbnails import generate_serialized_thumbnail

EPISODES = [
    {
        "episode_number": 1,
        "folder_name": "ep01_yamanote_transit",
        "slug": "yamanote_transit",
        "title": "Tokyo Metro & Yamanote Line Platform Broadcasts",
        "yt_title": "Tokyo Train Station Announcements Decoded! 🚆 Yamanote Line Immersion (EP. 01)",
        "category": "Tokyo Transit • Yamanote Line",
        "level": "JLPT N4-N3",
        "district": "Shinjuku (新宿)",
        "youtube_id": "kFhcEWNNkkc",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/tokyo_subway_metro_1790613022369.jpg",
        "cover": {
            "hook": "TOKYO METRO HACK",
            "jp": "まもなく参ります",
            "tag": "🇯🇵 Native Transit Audio • Shadowing"
        },
        "slides": [
            {
                "chapter": "01. Approaching Train Announcement",
                "spoken_text": "まもなく、2番線に山手線内回りがまいります。黄色い点字ブロックの内側までお下がりください。",
                "ja": "まもなく、2番線に山手線内回りがまいります。",
                "furi": "まもなく、にばんせんに やまのてせん うちまわりが まいります。",
                "en": "The Yamanote Line inner loop train will arrive on Platform 2.",
                "tip": "'まいります' is humble form (Kenjougo), standard JR platform phrasing."
            },
            {
                "chapter": "02. Safety & Tactile Paving",
                "spoken_text": "黄色い点字ブロックの内側までお下がりください。危ないですから、ご注意ください。",
                "ja": "黄色い点字ブロックの内側までお下がりください。",
                "furi": "きいろい てんじぶろっくの うちがわまで おさがりください。",
                "en": "Please stand behind the yellow tactile warning blocks.",
                "tip": "'お下がりください' is a polite instructional form used across all train stations."
            },
            {
                "chapter": "03. Transfer Assistance Phrase",
                "spoken_text": "すみません、中央線への乗り換えはどのホームですか？",
                "ja": "中央線への乗り換えはどのホームですか？",
                "furi": "ちゅうおうせんへの のりかえは どのほーむですか？",
                "en": "Excuse me, which platform is the transfer for the Chuo Line?",
                "tip": "Essential phrase when asking station staff. Replace '中央線' with any line."
            },
            {
                "chapter": "04. Subscribe & Download",
                "spoken_text": "ご視聴ありがとうございました！チャンネル登録と高評価をお願いします。TokyoFlowアプリでさらに深く学びましょう！",
                "is_outro": True
            }
        ]
    },
    {
        "episode_number": 2,
        "folder_name": "ep02_kombini_checkout",
        "slug": "kombini_checkout",
        "title": "Japanese 7-Eleven & FamilyMart Checkout Mastery",
        "yt_title": "Survive Tokyo 7-Eleven Checkout! 🍱 Rapid Register Japanese Decoded (EP. 02)",
        "category": "Kombini Protocol • Checkout Guide",
        "level": "JLPT N5-N4",
        "district": "Shibuya (渋谷)",
        "youtube_id": "BTKvaO25MUI",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_kombini_1790626387613.jpg",
        "cover": {
            "hook": "KOMBINI SURVIVAL",
            "jp": "温めますか？",
            "tag": "🇯🇵 1-Sec Register Reply • Shadowing"
        },
        "slides": [
            {
                "chapter": "01. Bento Heating Question",
                "spoken_text": "お弁当温めますか？少々お待ちください。",
                "ja": "お弁当温めますか？",
                "furi": "おべんとう あたためますか？",
                "en": "Would you like your bento heated up?",
                "tip": "Reply with '温めてください (Please heat it)' or '大丈夫です (No thanks)'."
            },
            {
                "chapter": "02. Declining Plastic Bags",
                "spoken_text": "レジ袋はご利用ですか？レジ袋は大丈夫です。",
                "ja": "レジ袋は大丈夫です。",
                "furi": "れじぶくろは だいじょうぶです。",
                "en": "No plastic bag needed, thank you.",
                "tip": "'大丈夫です' paired with a gentle nod is the natural way to politely decline."
            },
            {
                "chapter": "03. Contactless Payment",
                "spoken_text": "Suicaでお願いします。ポイントカードはお持ちですか？",
                "ja": "Suicaでお願いします。",
                "furi": "すいかで おねがいします。",
                "en": "I will pay with Suica, please.",
                "tip": "'[Payment method] でお願いします' works for Suica, PayPay, or Credit Card."
            },
            {
                "chapter": "04. Subscribe & Download",
                "spoken_text": "TokyoFlow Japanese 公式チャンネルを登録して、毎日の生きた日本語をマスターしましょう！",
                "is_outro": True
            }
        ]
    },
    {
        "episode_number": 3,
        "folder_name": "ep03_izakaya_night",
        "slug": "izakaya_night",
        "title": "Authentic Tokyo Izakaya Ordering & Toasting Etiquette",
        "yt_title": "Order Like a Tokyo Local at an Izakaya! 🍻 'Toriaezu Nama!' Explained (EP. 03)",
        "category": "Izakaya Culture • Dining Guide",
        "level": "JLPT N4-N3",
        "district": "Shinjuku Omoide Yokocho (思い出横丁)",
        "youtube_id": "q6P6i7nkIhU",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_izakaya_1790626403507.jpg",
        "cover": {
            "hook": "IZAKAYA MASTERY",
            "jp": "とりあえず生！",
            "tag": "🇯🇵 Showa Pub Etiquette • Shadowing"
        },
        "slides": [
            {
                "chapter": "01. The First Drink Order",
                "spoken_text": "いらっしゃい！とりあえず生ビール二つお願いします！",
                "ja": "とりあえず生ビール二つお願いします！",
                "furi": "とりあえず なまびーる ふたつ おねがいします！",
                "en": "To start, two draft beers please!",
                "tip": "'とりあえず〜' (for starters) is the quintessential Japanese izakaya opener."
            },
            {
                "chapter": "02. Yakitori Seasoning",
                "spoken_text": "焼き鳥盛り合わせを塩でお願いします。お待たせいたしました！",
                "ja": "焼き鳥盛り合わせを塩でお願いします。",
                "furi": "やきとり もりあわせを しおで おねがいします。",
                "en": "Assorted yakitori platter with salt seasoning, please.",
                "tip": "Staff will ask '塩かタレか' (salt or sweet tare sauce). '塩 (shio)' highlights the chicken flavor."
            },
            {
                "chapter": "03. The Check & Receipt",
                "spoken_text": "お会計と領収書をお願いします。毎度ありがとうございました！",
                "ja": "お会計と領収書をお願いします。",
                "furi": "おかいけいと りょうしゅうしょを おねがいします。",
                "en": "The bill and formal receipt, please.",
                "tip": "'お会計 (okaikei)' means bill, while '領収書 (ryoushuusho)' is an itemized receipt."
            },
            {
                "chapter": "04. Subscribe & Download",
                "spoken_text": "TokyoFlow Japanese チャンネルを登録して、リアルな東京の日常会話を体験しましょう！",
                "is_outro": True
            }
        ]
    },
    {
        "episode_number": 4,
        "folder_name": "ep04_akiba_pilgrimage",
        "slug": "akiba_pilgrimage",
        "title": "Akihabara Pilgrimage: Figures, Merch & Manga Tax-Free",
        "yt_title": "Akihabara Anime & Manga Shopping Japanese! 🛍️ Tax-Free & Rare Merch (EP. 04)",
        "category": "Akihabara Shopping • Anime Protocol",
        "level": "JLPT N3-N2",
        "district": "Akihabara (秋葉原)",
        "youtube_id": "g4mHPeNyQKA",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/akiba_neon_manga_1790602623116.jpg",
        "cover": {
            "hook": "AKIBA MANGA HUNT",
            "jp": "購入特典ありますか",
            "tag": "🇯🇵 Tax-Free & Figures • Shadowing"
        },
        "slides": [
            {
                "chapter": "01. Manga & Light Novel Finding",
                "spoken_text": "今期の新作アニメの原作はどこにありますか？3階の棚にございます。",
                "ja": "今期の新作アニメの原作はどこにありますか？",
                "furi": "こんきの しんさくあにめの げんさくは どこに ありますか？",
                "en": "Where are the original manga/novels for this season's new anime?",
                "tip": "Use '原作 (gensaku)' to ask for the original book source of any anime series."
            },
            {
                "chapter": "02. Pre-order Perks & Store Bonus",
                "spoken_text": "こちらの限定版、購入特典はまだ付きますか？はい、特典ポストカードが付きます。",
                "ja": "購入特典はまだ付きますか？",
                "furi": "こうにゅうとくてんは まだ つきますか？",
                "en": "Does this still come with the purchase bonus perk?",
                "tip": "'特典 (tokuten)' refers to exclusive store gifts like acrylic stands, badges, or illustrations."
            },
            {
                "chapter": "03. Tax-Free Exemption Checkout",
                "spoken_text": "免税手続きをお願いできますか？パスポートをご提示ください。",
                "ja": "免税手続きをお願いできますか？",
                "furi": "めんぜいてつづきを おねがいできますか？",
                "en": "Could you process tax-free exemption, please?",
                "tip": "Present your passport with tourist entry visa for 10% consumption tax refund over 5,000 JPY."
            },
            {
                "chapter": "04. Subscribe & Download",
                "spoken_text": "TokyoFlow Japanese チャンネルを登録して、生きたアニメ日本語をアプリで練習しましょう！",
                "is_outro": True
            }
        ]
    }
]

def generate_metadata_markdown(ep: dict, total_duration_s: float) -> str:
    ep_num = ep["episode_number"]
    yt_title = ep["yt_title"]
    
    return f"""# 🎌 YouTube Launch Package: EP. {ep_num:02d} • {ep['title']}

## 📌 Video Information
- **Episode**: `EP. {ep_num:02d}`
- **YouTube Video Title**: `{yt_title}`
- **Target Category**: `{ep['category']}`
- **JLPT Level**: `{ep['level']}`
- **District / Setting**: `{ep['district']}`
- **Standard Video File**: `video.mp4` (1080p Full HD, {total_duration_s:.1f}s)
- **Standard Thumbnail**: `thumbnail.jpg` (1920x1080 High-CTR Serialized Cover)

---

## 📝 YouTube Description Box (Copy & Paste Ready)

```markdown
{yt_title}

Learn authentic Tokyo Japanese as spoken by locals! In this episode, we dive into {ep['title']} at {ep['district']}.

Master the high-frequency phrases, pitch accent patterns, and cultural nuances without textbook fluff.

⏱️ TIMESTAMPS & CHAPTERS:
00:00 - Introduction & Real-Life Audio Immersion
00:10 - Core Formula & Pronunciation Drill
00:20 - Situational Survival Expression
00:30 - Shadowing Practice & iOS App Integration

🔑 KEY PHRASES COVERED:
{chr(10).join([f"• {s.get('ja', '')} ({s.get('furi', '')}) - {s.get('en', '')}" for s in ep['slides'] if not s.get('is_outro')])}

📱 TAKE YOUR JAPANESE TO THE NEXT LEVEL:
Practice real-time speech shadowing with instant pitch accent scoring on TokyoFlow for iOS:
👉 Download on the App Store: https://apps.apple.com/app/tokyoflow/id6740000000
👉 Official Website: https://tokyoflow.app

🔔 Subscribe to TokyoFlow Japanese for weekly real-life Tokyo Japanese scenarios!
#LearnJapanese #Tokyo #JapaneseStudy #{ep['slug'].replace('_', '')} #JLPT
```

---

## 💬 Pinned Comment (Copy & Paste)

```markdown
🇯🇵 What Tokyo scenario do you want us to cover next? Let us know in the comments below!
📲 Practice this lesson with native VoiceBank audio & speech shadowing scoring in the TokyoFlow iOS app: https://apps.apple.com/app/tokyoflow/id6740000000
```

---

## 🏷️ YouTube SEO Tags (Comma Separated)

```
learn japanese, tokyo japanese, japanese conversation, {ep['slug'].replace('_', ' ')}, tokyo travel japanese, japanese pronunciation, JLPT, JLPT {ep['level']}, japanese listening practice, japanese shadowing, tokyoflow, study japanese, anime japanese, travel tokyo
```
"""

async def package_episode(ep: dict):
    ep_num = ep["episode_number"]
    folder_name = ep["folder_name"]
    release_dir = os.path.join("docs", "youtube_releases", folder_name)
    os.makedirs(release_dir, exist_ok=True)
    
    print(f"\n==========================================")
    print(f"📦 Packaging EP. {ep_num:02d}: {folder_name}")
    print(f"==========================================")

    # 1. Render Video Segments
    workdir = f"tmp/videogen/{folder_name}"
    os.makedirs(workdir, exist_ok=True)
    
    segment_videos = []
    for idx, slide in enumerate(ep["slides"]):
        seg_prefix = f"{workdir}/seg_{idx:02d}"
        img_path = f"{seg_prefix}.jpg"
        audio_path = f"{seg_prefix}.mp3"
        video_path = f"{seg_prefix}.mp4"

        spoken_text = slide["spoken_text"]
        await generate_speech_audio(spoken_text, "ja-JP-NanamiNeural", audio_path, rate="-6%", pitch="+3Hz")
        duration = get_audio_duration(audio_path)

        create_slide_image(
            title_category=ep.get("category", "Tokyo Scenario Masterclass"),
            title_main=f"EP. {ep_num:02d} • {ep['title']}",
            japanese_text=slide.get("ja", ""),
            furigana_text=slide.get("furi", ""),
            english_text=slide.get("en", ""),
            tip_text=slide.get("tip", ""),
            chapter_label=slide.get("chapter", f"Part {idx+1}"),
            out_img_path=img_path,
            is_outro=slide.get("is_outro", False)
        )

        render_scene_video(img_path, audio_path, duration, video_path)
        segment_videos.append(video_path)
        print(f"  ✓ Segment {idx+1}/{len(ep['slides'])} rendered ({duration:.1f}s)")

    target_video = os.path.join(release_dir, "video.mp4")
    concat_videos(segment_videos, target_video)
    
    # Also mirror to output/videos/
    os.makedirs("output/videos", exist_ok=True)
    shutil.copyfile(target_video, f"output/videos/tokyoflow_v{ep_num:02d}_{ep['slug']}.mp4")
    
    total_duration = sum(get_audio_duration(f"{workdir}/seg_{i:02d}.mp3") for i in range(len(ep["slides"])))
    print(f"  ✓ Full HD video assembled: {target_video} ({total_duration:.1f}s)")

    # 2. Render Thumbnail
    target_thumb = os.path.join(release_dir, "thumbnail.jpg")
    cov = ep["cover"]
    generate_serialized_thumbnail(
        ep_num=ep_num,
        english_hook=cov["hook"],
        japanese_key_phrase=cov["jp"],
        bottom_tag=cov["tag"],
        bg_image_path=ep.get("bg_image", ""),
        output_path=target_thumb
    )
    # Also mirror to docs/youtube_assets/thumbnails/
    os.makedirs("docs/youtube_assets/thumbnails", exist_ok=True)
    shutil.copyfile(target_thumb, f"docs/youtube_assets/thumbnails/ep{ep_num:02d}_{ep['slug']}_thumb.jpg")
    print(f"  ✓ 1920x1080 Thumbnail saved: {target_thumb}")

    # 3. Write Metadata
    target_meta = os.path.join(release_dir, "metadata.md")
    with open(target_meta, "w", encoding="utf-8") as f:
        f.write(generate_metadata_markdown(ep, total_duration))
    print(f"  ✓ Launch metadata written: {target_meta}")

    # 4. Write Script JSON
    target_script = os.path.join(release_dir, "script.json")
    with open(target_script, "w", encoding="utf-8") as f:
        json.dump(ep, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Script manifest written: {target_script}")

async def main():
    for ep in EPISODES:
        await package_episode(ep)
    print("\n🎉 All 4 Episodes successfully packaged into docs/youtube_releases/!")

if __name__ == "__main__":
    asyncio.run(main())
