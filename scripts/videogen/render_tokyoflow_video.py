#!/usr/bin/env python3
"""
TokyoFlow Japanese • YouTube Scenario Video Production Engine
Inspired by Mystory's video factory architecture.
Generates 1080p full HD videos with native edge_tts narration, stylized typography cards,
and sample-accurate audio-video synchronization for English-speaking Japanese learners.
"""

import os
import sys
import json
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

async def generate_speech_audio(text: str, voice: str, out_path: str, rate: str = "-5%", pitch: str = "+0Hz"):
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
    
    # Background: Clean Japanese Ivory & Navy Modern Theme
    img = Image.new("RGB", (width, height), color=(248, 249, 252))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw.rectangle([(0, 0), (width, 80)], fill=(22, 28, 45))
    
    font_brand = get_font(28)
    draw.text((60, 24), "TokyoFlow Japanese  |  Real-Life Tokyo Japanese Academy", fill=(255, 255, 255), font=font_brand)
    
    font_badge = get_font(22)
    draw.text((width - 340, 26), f"Chapter: {chapter_label}", fill=(244, 114, 182), font=font_badge)

    if is_outro:
        # Outro Ending Card
        draw.rectangle([(160, 160), (width - 160, height - 120)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)
        
        font_hero = get_font(54)
        draw.text((220, 230), "Subscribe to TokyoFlow Japanese on YouTube", fill=(220, 38, 38), font=font_hero)
        
        font_sub = get_font(34)
        draw.text((220, 320), "Learn Natural Tokyo Japanese Through Real-Life Scenarios", fill=(30, 41, 59), font=font_sub)
        
        font_bullets = get_font(28)
        draw.text((220, 420), " 20+ Real Tokyo Life Scenarios (Transit, Kombini, Izakaya, Akiba)", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 490), " NHK Real Audio Shadowing • Pitch Accent & Intonation Guides", fill=(71, 85, 105), font=font_bullets)
        draw.text((220, 560), " JLPT N5-N1 Core Vocabulary & Japanese Cultural Nuances", fill=(71, 85, 105), font=font_bullets)
        
        # App CTA Box
        draw.rectangle([(220, 660), (width - 220, 840)], fill=(239, 246, 255), outline=(191, 219, 254), width=3)
        font_app = get_font(34)
        draw.text((260, 695), " Download 'TokyoFlow' Free on the iOS App Store", fill=(37, 99, 235), font=font_app)
        font_app_sub = get_font(24)
        draw.text((260, 760), "Pair with iOS App for Voice Shadowing Scoring, Kana Practice & SRS Flashcards", fill=(100, 116, 139), font=font_app_sub)

    else:
        # Main Scenario Content Card
        # Left Category Badge
        font_cat = get_font(24)
        draw.rectangle([(120, 120), (520, 165)], fill=(238, 242, 255))
        draw.text((135, 128), title_category, fill=(79, 70, 229), font=font_cat)

        font_title = get_font(38)
        draw.text((120, 190), title_main, fill=(15, 23, 42), font=font_title)

        # Center Main Japanese Phrase Card
        draw.rectangle([(120, 270), (width - 120, 720)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)

        # Furigana (Top)
        if furigana_text:
            font_furi = get_font(30)
            draw.text((180, 320), furigana_text, fill=(100, 116, 139), font=font_furi)

        # Japanese Kanji Main Text
        font_jp = get_font(50)
        draw.text((180, 380), japanese_text, fill=(15, 23, 42), font=font_jp)

        # Divider line
        draw.line([(180, 480), (width - 180, 480)], fill=(241, 245, 249), width=3)

        # English Meaning
        font_en = get_font(34)
        draw.text((180, 515), f"Meaning:  {english_text}", fill=(30, 41, 59), font=font_en)

        # Bottom Tip & Tone
        font_tip = get_font(26)
        draw.text((180, 595), f" Pro-Tip:  {tip_text}", fill=(16, 185, 129), font=font_tip)

        # Bottom Call-to-action
        draw.rectangle([(120, 770), (width - 120, 920)], fill=(241, 245, 249), outline=(226, 232, 240), width=2)
        font_shadow = get_font(28)
        draw.text((160, 805), "  Shadowing Drill: Repeat aloud with native timing and pitch accent", fill=(51, 65, 85), font=font_shadow)
        font_shadow_sub = get_font(22)
        draw.text((160, 860), "Native Audio: Nanami (Tokyo Standard) • Real-life context breakdown", fill=(100, 116, 139), font=font_shadow_sub)

    # Save slide image
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

async def build_video_package(spec: dict):
    video_id = spec["id"]
    print(f" Starting production for Video: {spec['title']} ({video_id})...")
    
    workdir = f"tmp/videogen/{video_id}"
    os.makedirs(workdir, exist_ok=True)
    
    segment_videos = []
    
    for idx, slide in enumerate(spec["slides"]):
        seg_prefix = f"{workdir}/seg_{idx:02d}"
        img_path = f"{seg_prefix}.jpg"
        audio_path = f"{seg_prefix}.mp3"
        video_path = f"{seg_prefix}.mp4"
        
        # 1. Generate Voiceover
        voice = slide.get("voice", "ja-JP-NanamiNeural")
        rate = slide.get("rate", "-6%")
        pitch = slide.get("pitch", "+3Hz")
        spoken_text = slide["spoken_text"]
        
        await generate_speech_audio(spoken_text, voice, audio_path, rate=rate, pitch=pitch)
        duration = get_audio_duration(audio_path)
        
        # 2. Render Graphic Slide
        create_slide_image(
            title_category=spec.get("category", "Tokyo Scenario Masterclass"),
            title_main=spec["title"],
            japanese_text=slide.get("ja", ""),
            furigana_text=slide.get("furi", ""),
            english_text=slide.get("en", ""),
            tip_text=slide.get("tip", ""),
            chapter_label=slide.get("chapter", f"Part {idx+1}"),
            out_img_path=img_path,
            is_outro=slide.get("is_outro", False)
        )
        
        # 3. Assemble Segment Video
        render_scene_video(img_path, audio_path, duration, video_path)
        segment_videos.append(video_path)
        print(f"   Segment {idx+1}/{len(spec['slides'])} rendered ({duration:.1f}s)")
        
    final_output = f"{workdir}/{video_id}.mp4"
    concat_videos(segment_videos, final_output)
    total_duration = sum(get_audio_duration(f"{workdir}/seg_{i:02d}.mp3") for i in range(len(spec["slides"])))
    print(f" Successfully produced full HD video: {final_output} (Total Length: {total_duration:.1f}s)\n")

async def main():
    videos = [
        {
            "id": "tokyoflow_v01_yamanote_transit",
            "title": "Tokyo Metro & Yamanote Line Platform Broadcasts",
            "category": "Tokyo Transit • Yamanote Line",
            "slides": [
                {
                    "chapter": "01. Approaching Train Announcement",
                    "spoken_text": "2",
                    "ja": "2",
                    "furi": "   ",
                    "en": "The Yamanote Line inner loop train will arrive on Platform 2.",
                    "tip": "'' is humble form (Kenjougo), standard JR platform phrasing."
                },
                {
                    "chapter": "02. Safety & Tactile Paving",
                    "spoken_text": "",
                    "ja": "",
                    "furi": "   ",
                    "en": "Please stand behind the yellow tactile warning blocks.",
                    "tip": "'' is a polite instructional form used across all train stations."
                },
                {
                    "chapter": "03. Transfer Assistance Phrase",
                    "spoken_text": "",
                    "ja": "",
                    "furi": "  ",
                    "en": "Excuse me, which platform is the transfer for the Chuo Line?",
                    "tip": "Essential phrase when asking station staff. Replace '' with any line."
                },
                {
                    "chapter": "04. Subscribe & Download",
                    "spoken_text": "TokyoFlow",
                    "is_outro": True
                }
            ]
        },
        {
            "id": "tokyoflow_v02_kombini_checkout",
            "title": "Japanese 7-Eleven & FamilyMart Checkout Mastery",
            "category": "Kombini Protocol • Checkout Guide",
            "slides": [
                {
                    "chapter": "01. Bento Heating Question",
                    "spoken_text": "",
                    "ja": "",
                    "furi": " ",
                    "en": "Would you like your bento heated up?",
                    "tip": "Reply with ' (Please heat it)' or ' (No thanks)'."
                },
                {
                    "chapter": "02. Declining Plastic Bags",
                    "spoken_text": "",
                    "ja": "",
                    "furi": " ",
                    "en": "No plastic bag needed, thank you.",
                    "tip": "'' paired with a gentle nod is the natural way to politely decline."
                },
                {
                    "chapter": "03. Contactless Payment",
                    "spoken_text": "Suica",
                    "ja": "Suica",
                    "furi": " ",
                    "en": "I will pay with Suica, please.",
                    "tip": "'[Payment method] ' works for Suica, PayPay, or Credit Card."
                },
                {
                    "chapter": "04. Subscribe & Download",
                    "spoken_text": "TokyoFlow Japanese ",
                    "is_outro": True
                }
            ]
        },
        {
            "id": "tokyoflow_v03_izakaya_night",
            "title": "Authentic Tokyo Izakaya Ordering & Toasting Etiquette",
            "category": "Izakaya Culture • Dining Guide",
            "slides": [
                {
                    "chapter": "01. The First Drink Order",
                    "spoken_text": "",
                    "ja": "",
                    "furi": "   ",
                    "en": "To start, two draft beers please!",
                    "tip": "'' (for starters) is the quintessential Japanese izakaya opener."
                },
                {
                    "chapter": "02. Yakitori Seasoning",
                    "spoken_text": "",
                    "ja": "",
                    "furi": "   ",
                    "en": "Assorted yakitori platter with salt seasoning, please.",
                    "tip": "Staff will ask '' (salt or sweet tare sauce). ' (shio)' highlights the chicken flavor."
                },
                {
                    "chapter": "03. The Check & Receipt",
                    "spoken_text": "",
                    "ja": "",
                    "furi": "  ",
                    "en": "The bill and formal receipt, please.",
                    "tip": "' (okaikei)' means bill, while ' (ryoushuusho)' is an itemized receipt."
                },
                {
                    "chapter": "04. Subscribe & Download",
                    "spoken_text": "TokyoFlow Japanese ",
                    "is_outro": True
                }
            ]
        }
    ]

    for v in videos:
        await build_video_package(v)

if __name__ == "__main__":
    asyncio.run(main())
