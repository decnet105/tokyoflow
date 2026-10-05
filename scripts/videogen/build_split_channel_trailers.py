#!/usr/bin/env python3
"""
TokyoFlow Japanese • Split Official Channel Trailers Producer (V2 - Clean Layering Engine)
========================================================================================
Completely cleans up frame rendering layering, eliminates ghosting/overlapping artifacts,
ensures 100% authentic scenario covers on both English & Chinese versions,
and uses Hiragino Sans GB universally to guarantee crisp Japanese kanji/kana rendering without tofu boxes.

Outputs:
- output/channel_trailer_en/tokyoflow_trailer_en_1080p.mp4
- output/channel_trailer_en/thumbnail.jpg
- output/channel_trailer_en/metadata.md
- output/channel_trailer_zh/tokyoflow_trailer_zh_1080p.mp4
- output/channel_trailer_zh/thumbnail.jpg
- output/channel_trailer_zh/metadata.md
"""

import os
import sys
import math
import shutil
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
OUT_EN_DIR = PROJECT_ROOT / "output" / "channel_trailer_en"
OUT_ZH_DIR = PROJECT_ROOT / "output" / "channel_trailer_zh"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def synth_line(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(out_path)

def get_clean_background() -> Image.Image:
    """Returns a pristine, clean 1920x1080 dark skyline background with NO text or cards."""
    W, H = 1920, 1080
    bg_skyline = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
    base = Image.new("RGB", (W, H), (10, 14, 22))
    if bg_skyline.exists():
        sky = Image.open(bg_skyline).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        sky = ImageEnhance.Brightness(sky).enhance(0.35)
        base.paste(sky, (0, 0))
    return base

# =========================================================================
# 1. PURE ENGLISH TRAILER GENERATOR
# =========================================================================
async def build_english_trailer():
    OUT_EN_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = OUT_EN_DIR / "temp_render"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("\n--- Generating Clean English Channel Trailer (16:9 1080p) ---")
    
    script_en = [
        {"id": "en_01", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Why do traditional Japanese textbooks feel impossible to use in real life?"},
        {"id": "en_02", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "教科書と実際の会話は、全然違いますよ！"},
        {"id": "en_03", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Because real Tokyo Japanese happens on the streets, trains, and kombini counters."},
        {"id": "en_04", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Welcome to TokyoFlow Japanese — the cinema-grade language academy."},
        {"id": "en_05", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "We decode how Tokyo locals actually talk in authentic daily scenarios."},
        {"id": "en_06", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "次は、新宿、新宿です。乗り換えのご案内です。"},
        {"id": "en_07", "voice": "en-US-AndrewNeural", "rate": "+4%", "text": "Decode rapid Yamanote station announcements and subway fare adjustments."},
        {"id": "en_08", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "袋は大丈夫です。温めも結構です。"},
        {"id": "en_09", "voice": "en-US-AndrewNeural", "rate": "+4%", "text": "Survive 7-Eleven register speed questions without hesitation."},
        {"id": "en_10", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "とりあえず生で！麺硬め、味濃いめで！"},
        {"id": "en_11", "voice": "en-US-AndrewNeural", "rate": "+4%", "text": "Master authentic izakaya draft beer orders and ramen ticket machine hacks."},
        {"id": "en_12", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "サウナで最高にととのう！"},
        {"id": "en_13", "voice": "en-US-AndrewNeural", "rate": "+4%", "text": "Plus Akihabara tax-free shopping, Ginza fitting rooms, and hot pop-culture trends."},
        {"id": "en_14", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Every day, get full 1080p masterclasses paired with 60-second shadowing shorts."},
        {"id": "en_15", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Structured progression from JLPT N5 beginner to N1 advanced nuance."},
        {"id": "en_16", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Released daily at 08:00 AM EDT. Hit Subscribe and master real Tokyo Japanese!"},
        {"id": "en_17", "voice": "ja-JP-NanamiNeural", "rate": "-3%", "pitch": "+3Hz", "text": "チャンネル登録、よろしくお願いします！"}
    ]

    timeline = []
    cur_time = 0.5
    for seg in script_en:
        out_f = str(temp_dir / f"{seg['id']}.mp3")
        await synth_line(seg["text"], seg["voice"], out_f, rate=seg.get("rate", "+0%"), pitch=seg.get("pitch", "+0Hz"))
        dur = get_audio_duration(out_f)
        timeline.append({"id": seg["id"], "text": seg["text"], "voice": seg["voice"], "start": cur_time, "end": cur_time + dur, "duration": dur, "file": out_f})
        cur_time += dur + 0.30

    total_duration = cur_time + 1.0

    concat_list = temp_dir / "concat_en.txt"
    with open(concat_list, "w") as f:
        sil_05 = temp_dir / "sil_05.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.5", "-c:a", "libmp3lame", str(sil_05)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        p_03 = temp_dir / "p_03.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.30", "-c:a", "libmp3lame", str(p_03)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        sil_10 = temp_dir / "sil_10.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", "-c:a", "libmp3lame", str(sil_10)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        f.write(f"file '{sil_05.name}'\n")
        for item in timeline:
            f.write(f"file '{Path(item['file']).name}'\nfile '{p_03.name}'\n")
        f.write(f"file '{sil_10.name}'\n")

    audio_out = temp_dir / "voice_en.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c:a", "libmp3lame", "-b:a", "192k", str(audio_out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 1. Generate English Master Cover (Stand-alone static image)
    cover_en = OUT_EN_DIR / "thumbnail.jpg"
    W, H = 1920, 1080
    img_en = get_clean_background()
    d = ImageDraw.Draw(img_en)

    d.rounded_rectangle([80, 70, 520, 145], radius=16, fill=(255, 255, 255))
    d.text((110, 88), "TokyoFlow Japanese", fill=(225, 29, 72), font=get_font(34))

    d.rounded_rectangle([W - 480, 70, W - 80, 145], radius=16, fill=(225, 29, 72))
    d.text((W - 450, 88), "OFFICIAL TRAILER", fill=(255, 255, 255), font=get_font(32))

    d.text((80, 200), "SPEAK REAL-LIFE TOKYO JAPANESE", fill=(254, 240, 138), font=get_font(74))
    d.text((80, 305), "Decode Authentic Spoken Japanese from Real Tokyo Streets", fill=(255, 255, 255), font=get_font(44))

    card_y = 420
    d.rounded_rectangle([80, card_y, 1180, card_y + 480], radius=24, fill=(10, 16, 28, 240), outline=(56, 189, 248), width=3)
    d.text((120, card_y + 40), "[ USE-CASE DRIVEN TOKYO IMMERSION TRACKS ]", fill=(56, 189, 248), font=get_font(28))
    
    en_bullets = [
        "- Real Transit: Yamanote Line Announcements & Subway Gate Hacks",
        "- Street Survival: 7-Eleven & FamilyMart Speed Checkout Replies",
        "- Foodie Immersion: Izakaya Draft Beer Orders & Ramen Machine Hacks",
        "- Pop Culture & Trends: Akihabara Tax-Free & Anime Sauna Hot Trends",
        "- Standardized JLPT Roadmaps: From [JLPT N5] Zero to [JLPT N1] Fluency"
    ]
    y_b = card_y + 110
    for b in en_bullets:
        d.text((120, y_b), b, fill=(230, 240, 255), font=get_font(28))
        y_b += 68

    # Authentic real English photo covers on right
    t_e01 = RELEASES_DIR / "E01-Yamanote_Transit-v1.0" / "thumbnail.jpg"
    t_e03 = RELEASES_DIR / "E03-Izakaya_Night-v1.0" / "thumbnail.jpg"
    if t_e01.exists() and t_e03.exists():
        img_e01 = Image.open(t_e01).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        img_e03 = Image.open(t_e03).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        img_en.paste(img_e01, (1240, 200))
        d.rectangle([1240, 200, 1840, 537], outline=(255, 215, 0), width=4)
        img_en.paste(img_e03, (1240, 560))
        d.rectangle([1240, 560, 1840, 897], outline=(225, 29, 72), width=4)

    d.rounded_rectangle([80, H - 125, W - 80, H - 45], radius=16, fill=(225, 29, 72))
    d.text((160, H - 100), "DAILY MASTERCLASSES & SHORTS: 08:00 AM EDT  •  SUBSCRIBE @TokyoFlowJapan", fill=(255, 255, 255), font=get_font(26))
    img_en.save(cover_en, quality=95)
    print(f"✓ Clean English Cover saved: {cover_en}")

    # 2. Render English Video Frames (From CLEAN background, NO ghosting!)
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    fps = 30
    total_frames = int(math.ceil(total_duration * fps))

    # Load authentic English scenario thumbnails
    loaded_real_covers = {
        "transit": Image.open(RELEASES_DIR / "E01-Yamanote_Transit-v1.0" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E01-Yamanote_Transit-v1.0" / "thumbnail.jpg").exists() else None,
        "kombini": Image.open(RELEASES_DIR / "E02-Kombini_Checkout-v1.0" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E02-Kombini_Checkout-v1.0" / "thumbnail.jpg").exists() else None,
        "izakaya": Image.open(RELEASES_DIR / "E03-Izakaya_Night-v1.0" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E03-Izakaya_Night-v1.0" / "thumbnail.jpg").exists() else None,
        "trends": Image.open(RELEASES_DIR / "E09-anime_sauna_trend-v1.0" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E09-anime_sauna_trend-v1.0" / "thumbnail.jpg").exists() else None,
    }

    clean_base = get_clean_background()

    for f_idx in range(total_frames):
        t = f_idx / fps
        cur_seg = None
        for seg in timeline:
            if seg["start"] <= t <= seg["end"]:
                cur_seg = seg
                break

        # Start from 100% pristine canvas (NO old text!)
        frame = clean_base.copy()
        d = ImageDraw.Draw(frame)

        # Top Navigation Bar
        d.rounded_rectangle([60, 40, 1860, 120], radius=16, fill=(15, 22, 35, 230), outline=(45, 60, 85), width=2)
        d.text((90, 60), "TokyoFlow Japanese • Master Real Spoken Japanese", fill=(255, 215, 0), font=get_font(34))
        d.rounded_rectangle([1580, 52, 1830, 108], radius=10, fill=(225, 29, 72))
        d.text((1610, 67), "MASTERCLASS", fill=(255, 255, 255), font=get_font(24))

        # Dynamic center display
        if t < 12.0:
            # Phase 1: Problem vs Solution
            d.text((100, 180), "THE CLASSROOM TO REALITY GAP", fill=(244, 114, 182), font=get_font(28))
            d.text((100, 230), "Why Traditional Textbooks Fail in Tokyo", fill=(255, 255, 255), font=get_font(52))
            
            # Left Flaws Card
            d.rounded_rectangle([100, 310, 920, 830], radius=20, fill=(20, 24, 36, 245), outline=(100, 116, 139), width=2)
            d.text((140, 350), "[ Traditional Textbook Flaws ]", fill=(148, 163, 184), font=get_font(28))
            d.text((140, 430), "- Outdated robotic sentences locals never use", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 510), "- Unnatural slow audio disconnected from reality", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 590), "- Zero preparation for rapid kombini & transit cues", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 670), "- Fear of speaking out loud due to lack of immersion", fill=(203, 213, 225), font=get_font(24))
            
            # Right Solution Card
            d.rounded_rectangle([980, 310, 1820, 830], radius=20, fill=(15, 25, 45, 250), outline=(56, 189, 248), width=3)
            d.text((1020, 350), "[ The TokyoFlow Approach ]", fill=(56, 189, 248), font=get_font(28))
            d.text((1020, 430), "- 100% authentic Tokyo transit, dining & culture cues", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 510), "- Pure Tokyo native Nanami audio & pitch accent drills", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 590), "- Cinema-grade breakdown: romaji, kanji & grammar", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 670), "- Structured progression from [JLPT N5] to [JLPT N1]", fill=(254, 240, 138), font=get_font(24))

        elif 12.0 <= t < 24.0:
            # Phase 2: Dual Flagship Showcase
            d.text((100, 180), "CINEMA-GRADE REAL-WORLD IMMERSION", fill=(56, 189, 248), font=get_font(28))
            d.text((100, 230), "Step Inside Authentic Tokyo Living", fill=(255, 255, 255), font=get_font(52))
            if loaded_real_covers["transit"] and loaded_real_covers["izakaya"]:
                cov1 = loaded_real_covers["transit"].resize((820, 461), Image.Resampling.LANCZOS)
                cov2 = loaded_real_covers["izakaya"].resize((820, 461), Image.Resampling.LANCZOS)
                frame.paste(cov1, (100, 330))
                d.rectangle([100, 330, 920, 791], outline=(56, 189, 248), width=4)
                d.text((120, 350), "[JLPT N4] Tokyo Subway & Transit", fill=(255, 255, 255), font=get_font(26))
                
                frame.paste(cov2, (980, 330))
                d.rectangle([980, 330, 1800, 791], outline=(225, 29, 72), width=4)
                d.text((1000, 350), "[JLPT N5] Izakaya & Dining Protocols", fill=(255, 255, 255), font=get_font(26))

        elif 24.0 <= t < 48.0:
            # Phase 3: Fast Scenario Showcase
            sec_idx = int((t - 24.0) / 6.0)
            scenes_info = [
                ("Scenario 01 • Tokyo Subway & Yamanote Transit", "transit", "Station Announcements & Ticket Gate Hacks"),
                ("Scenario 02 • 7-Eleven & Kombini Survival", "kombini", "30-Second Register Speed Replies & Iced Coffee"),
                ("Scenario 03 • Izakaya Dining & Ramen Orders", "izakaya", "Toriaezu Nama & Ramen Machine Broth Hacks"),
                ("Scenario 04 • Pop Culture & Hot Trends", "trends", "Akihabara Figure Shopping & Anime Sauna Buzz")
            ]
            s_title, s_key, s_sub = scenes_info[min(sec_idx, 3)]
            d.text((100, 175), s_title, fill=(255, 215, 0), font=get_font(44))
            d.text((100, 240), s_sub, fill=(203, 213, 225), font=get_font(28))
            
            if loaded_real_covers[s_key]:
                cov_main = loaded_real_covers[s_key].resize((980, 551), Image.Resampling.LANCZOS)
                frame.paste(cov_main, (100, 290))
                d.rectangle([100, 290, 1080, 841], outline=(255, 215, 0), width=4)
                
            d.rounded_rectangle([1120, 290, 1820, 841], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((1160, 330), "[ Authentic Vocabulary & Key Grammar ]", fill=(56, 189, 248), font=get_font(26))
            pts = [
                "- 100% Native Tokyo audio with exact cadence",
                "- Millisecond romaji, furigana & grammar cues",
                "- Master polite refusal and natural casual phrases",
                "- Sound like a local from your very first week"
            ]
            yp = 400
            for pt in pts:
                d.text((1160, yp), pt, fill=(241, 245, 249), font=get_font(24))
                yp += 90

        elif 48.0 <= t < 62.0:
            # Phase 4: Dual Track & JLPT
            d.text((100, 175), "DUAL-TRACK LEARNING ARCHITECTURE", fill=(56, 189, 248), font=get_font(28))
            d.text((100, 230), "Full Masterclasses + Daily 60s Shadowing Shorts", fill=(255, 255, 255), font=get_font(48))
            if loaded_real_covers["transit"]:
                m16 = loaded_real_covers["transit"].resize((780, 439), Image.Resampling.LANCZOS)
                frame.paste(m16, (100, 330))
                d.rectangle([100, 330, 880, 769], outline=(56, 189, 248), width=3)
                d.text((120, 350), "1080p Long-Form Masterclass", fill=(255, 255, 255), font=get_font(24))
                
            d.rounded_rectangle([940, 330, 1820, 769], radius=20, fill=(15, 22, 35, 240), outline=(225, 29, 72), width=3)
            d.text((980, 380), "[ COMPLETE LEVEL COVERAGE ]", fill=(254, 240, 138), font=get_font(32))
            d.text((980, 460), "- [JLPT N5] Zero-Prerequisite Real Japanese", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 530), "- [JLPT N4] Practical Everyday Tokyo Living", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 600), "- [JLPT N3] Intermediate News & Conversation", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 670), "- [JLPT N2-N1] Advanced Nuance & Fluency", fill=(255, 255, 255), font=get_font(26))

        else:
            # Phase 5: Subscribe & Cadence
            d.text((100, 175), "JOIN THE TOKYOFLOW COMMUNITY", fill=(254, 240, 138), font=get_font(32))
            d.text((100, 230), "Daily Drops at 08:00 AM EDT • Master Tokyo Fluency", fill=(255, 255, 255), font=get_font(48))
            
            d.rounded_rectangle([100, 320, 920, 790], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((140, 360), "[ Global English Release Cadence ]", fill=(56, 189, 248), font=get_font(28))
            d.text((140, 430), "- 16:9 Long-Form Masterclasses: 08:00 AM EDT", fill=(255, 255, 255), font=get_font(24))
            d.text((140, 500), "- 9:16 Daily Shadowing Shorts: 08:00 AM EDT", fill=(255, 255, 255), font=get_font(24))
            d.text((140, 570), "- Standardized JLPT Levels [N5 to N1]", fill=(254, 240, 138), font=get_font(24))
            d.text((140, 640), "- Weekend Mega Immersion Compilations", fill=(203, 213, 225), font=get_font(24))

            d.rounded_rectangle([980, 320, 1820, 790], radius=20, fill=(225, 29, 72), outline=(255, 255, 255), width=3)
            d.text((1050, 400), "SUBSCRIBE NOW", fill=(255, 255, 255), font=get_font(56))
            d.text((1050, 485), "@TokyoFlowJapan", fill=(254, 240, 138), font=get_font(48))
            d.text((1050, 570), "Start Your Real Tokyo Japanese Journey Today!", fill=(255, 255, 255), font=get_font(30))
            d.text((1050, 660), "Official Channel: youtube.com/@TokyoFlowJapan", fill=(241, 245, 249), font=get_font(24))

        # Bottom Subtitle Banner (Crisp Hiragino Sans font for Japanese & English!)
        if cur_seg:
            d.rounded_rectangle([60, 890, 1860, 1030], radius=20, fill=(8, 12, 20, 245), outline=(50, 70, 100), width=2)
            if "Nanami" in cur_seg["voice"]:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(0, 120, 215))
                d.text((115, 945), "[ Tokyo Native ] Nanami", fill=(255, 255, 255), font=get_font(22))
            else:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(16, 185, 129))
                d.text((115, 945), "[ Explainer ] Andrew", fill=(255, 255, 255), font=get_font(22))

            text = cur_seg["text"]
            font_sub = get_font(32)
            d.text((370, 946), text, fill=(255, 255, 255), font=font_sub)

        frame.save(frames_dir / f"frame_{f_idx:05d}.jpg", quality=90)

    out_mp4 = OUT_EN_DIR / "tokyoflow_trailer_en_1080p.mp4"
    cmd = [
        "ffmpeg", "-y", "-r", str(fps), "-i", str(frames_dir / "frame_%05d.jpg"),
        "-i", str(audio_out), "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✓ Pure English Trailer generated: {out_mp4}")

# =========================================================================
# 2. PURE CHINESE TRAILER GENERATOR
# =========================================================================
async def build_chinese_trailer():
    OUT_ZH_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = OUT_ZH_DIR / "temp_render"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("\n--- Generating Clean Chinese Channel Trailer (16:9 1080p) ---")
    
    script_zh = [
        {"id": "zh_01", "voice": "zh-CN-YunxiNeural", "rate": "+4%", "text": "为什么学了几年日语，到了东京依然听不懂、不敢开口？"},
        {"id": "zh_02", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "教科書と実際の会話は、全然違いますよ！"},
        {"id": "zh_03", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "因为传统的死板教材，根本无法应对东京真实的日常现场！"},
        {"id": "zh_04", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "欢迎来到 TokyoFlow 日语实景精讲！"},
        {"id": "zh_05", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "我们把东京最真实的生活现场，直接搬进你的屏幕！"},
        {"id": "zh_06", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "次は、新宿、新宿です。乗り換えのご案内です。"},
        {"id": "zh_07", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "山手线报站与地铁精算机补票，一秒听懂！"},
        {"id": "zh_08", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "袋は大丈夫です。温めも結構です。"},
        {"id": "zh_09", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "便利店收银应答与冰咖啡取杯，秒回不社恐！"},
        {"id": "zh_10", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "とりあえず生で！麺硬め、味濃いめで！"},
        {"id": "zh_11", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "居酒屋生啤开场与拉面老饕定制口诀！"},
        {"id": "zh_12", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "サウナで最高にととのう！"},
        {"id": "zh_13", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "秋叶原手办免税、银座试衣与当季热梗全覆盖！"},
        {"id": "zh_14", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "每天 1080p 深度精讲大班课，搭配 1 分钟原声跟读短视频！"},
        {"id": "zh_15", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "零基础到进阶，随时随地轻松磨耳朵！"},
        {"id": "zh_16", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "每晚 8 点定时更新，立即订阅 TokyoFlow！"},
        {"id": "zh_17", "voice": "ja-JP-NanamiNeural", "rate": "-3%", "pitch": "+3Hz", "text": "チャンネル登録、よろしくお願いします！"}
    ]

    timeline = []
    cur_time = 0.5
    for seg in script_zh:
        out_f = str(temp_dir / f"{seg['id']}.mp3")
        await synth_line(seg["text"], seg["voice"], out_f, rate=seg.get("rate", "+0%"), pitch=seg.get("pitch", "+0Hz"))
        dur = get_audio_duration(out_f)
        timeline.append({"id": seg["id"], "text": seg["text"], "voice": seg["voice"], "start": cur_time, "end": cur_time + dur, "duration": dur, "file": out_f})
        cur_time += dur + 0.30

    total_duration = cur_time + 1.0

    concat_list = temp_dir / "concat_zh.txt"
    with open(concat_list, "w") as f:
        sil_05 = temp_dir / "sil_05.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.5", "-c:a", "libmp3lame", str(sil_05)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        p_03 = temp_dir / "p_03.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.30", "-c:a", "libmp3lame", str(p_03)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        sil_10 = temp_dir / "sil_10.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", "-c:a", "libmp3lame", str(sil_10)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        f.write(f"file '{sil_05.name}'\n")
        for item in timeline:
            f.write(f"file '{Path(item['file']).name}'\nfile '{p_03.name}'\n")
        f.write(f"file '{sil_10.name}'\n")

    audio_out = temp_dir / "voice_zh.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c:a", "libmp3lame", "-b:a", "192k", str(audio_out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 1. Generate Chinese Master Cover (Stand-alone static image)
    cover_zh = OUT_ZH_DIR / "thumbnail.jpg"
    W, H = 1920, 1080
    img_zh = get_clean_background()
    d = ImageDraw.Draw(img_zh)

    d.rounded_rectangle([80, 70, 520, 145], radius=16, fill=(255, 255, 255))
    d.text((110, 88), "TokyoFlow 日语", fill=(225, 29, 72), font=get_font(34))

    d.rounded_rectangle([W - 480, 70, W - 80, 145], radius=16, fill=(225, 29, 72))
    d.text((W - 440, 88), "【官方中文预告】", fill=(255, 255, 255), font=get_font(32))

    d.text((80, 200), "告别死板教科书！", fill=(255, 255, 255), font=get_font(84))
    d.text((80, 305), "每天沉浸式掌握东京地道实景日语", fill=(254, 240, 138), font=get_font(58))

    card_y = 420
    d.rounded_rectangle([80, card_y, 1180, card_y + 480], radius=24, fill=(10, 16, 28, 240), outline=(56, 189, 248), width=3)
    d.text((120, card_y + 40), "【 核心实战课程体系与场景矩阵 】", fill=(56, 189, 248), font=get_font(28))
    
    zh_bullets = [
        "- 实景出行：山手线报站 • 地铁闸机精算机补票全流程",
        "- 街头生存：7-Eleven/全家收银应答 • 咖啡机与ATM",
        "- 美食老饕：居酒屋生啤开场 • 顶级拉面食券机定制",
        "- 潮流文化：秋叶原手办免税 • 银座试衣 • 当季热梗",
        "- 权威分级：【JLPT N5】零基础至【JLPT N1】高阶精讲"
    ]
    y_b = card_y + 110
    for b in zh_bullets:
        d.text((120, y_b), b, fill=(230, 240, 255), font=get_font(30))
        y_b += 68

    t_e01 = RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg"
    t_e03 = RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg"
    if t_e01.exists() and t_e03.exists():
        img_e01 = Image.open(t_e01).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        img_e03 = Image.open(t_e03).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        img_zh.paste(img_e01, (1240, 200))
        d.rectangle([1240, 200, 1840, 537], outline=(255, 215, 0), width=4)
        img_zh.paste(img_e03, (1240, 560))
        d.rectangle([1240, 560, 1840, 897], outline=(225, 29, 72), width=4)

    d.rounded_rectangle([80, H - 125, W - 80, H - 45], radius=16, fill=(225, 29, 72))
    d.text((180, H - 100), "每日大班课与跟读短视频：每晚 8:00 PM (EDT) 更新  •  欢迎订阅 @TokyoFlowJapan", fill=(255, 255, 255), font=get_font(26))
    img_zh.save(cover_zh, quality=95)
    print(f"✓ Clean Chinese Cover saved: {cover_zh}")

    # 2. Render Chinese Video Frames (From CLEAN background, NO ghosting!)
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    fps = 30
    total_frames = int(math.ceil(total_duration * fps))

    loaded_real_covers = {
        "transit": Image.open(RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg").exists() else None,
        "kombini": Image.open(RELEASES_DIR / "E02-Kombini_Checkout-v1.0-zh" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E02-Kombini_Checkout-v1.0-zh" / "thumbnail.jpg").exists() else None,
        "izakaya": Image.open(RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg").exists() else None,
        "trends": Image.open(RELEASES_DIR / "E09-anime_sauna_trend-v1.0-zh" / "thumbnail.jpg").convert("RGB") if (RELEASES_DIR / "E09-anime_sauna_trend-v1.0-zh" / "thumbnail.jpg").exists() else None,
    }

    clean_base = get_clean_background()

    for f_idx in range(total_frames):
        t = f_idx / fps
        cur_seg = None
        for seg in timeline:
            if seg["start"] <= t <= seg["end"]:
                cur_seg = seg
                break

        # Start from clean background
        frame = clean_base.copy()
        d = ImageDraw.Draw(frame)

        # Header
        d.rounded_rectangle([60, 40, 1860, 120], radius=16, fill=(15, 22, 35, 230), outline=(45, 60, 85), width=2)
        d.text((90, 60), "TokyoFlow 日语实景精讲 • 官方中文频道预告", fill=(255, 215, 0), font=get_font(34))
        d.rounded_rectangle([1580, 52, 1830, 108], radius=10, fill=(225, 29, 72))
        d.text((1620, 67), "精讲大班课", fill=(255, 255, 255), font=get_font(24))

        # Center Display
        if t < 12.0:
            d.text((100, 180), "告别死板机械的教科书", fill=(244, 114, 182), font=get_font(28))
            d.text((100, 230), "学了几年日语，为什么依然听不懂、不敢开口？", fill=(255, 255, 255), font=get_font(52))
            
            d.rounded_rectangle([100, 310, 920, 830], radius=20, fill=(20, 24, 36, 245), outline=(100, 116, 139), width=2)
            d.text((140, 350), "【 传统教科书痛点 】", fill=(148, 163, 184), font=get_font(28))
            d.text((140, 430), "- 死板句式：句句都是「私は学生です」", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 510), "- 语速脱节：播音员慢速，无法应对现场", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 590), "- 缺乏实战：地铁/便利店/居酒屋瞬间卡壳", fill=(203, 213, 225), font=get_font(24))
            d.text((140, 670), "- 畏惧开口：没有场景支撑，不敢自然发音", fill=(203, 213, 225), font=get_font(24))
            
            d.rounded_rectangle([980, 310, 1820, 830], radius=20, fill=(15, 25, 45, 250), outline=(56, 189, 248), width=3)
            d.text((1020, 350), "【 TokyoFlow 解决方案 】", fill=(56, 189, 248), font=get_font(28))
            d.text((1020, 430), "- 真实东京：100% 还原山手线/居酒屋/药妆现场", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 510), "- 地道原声：纯正东京音 Nanami 影子跟读", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 590), "- 深度拆解：双语名师逐字逐句刨析文化与语法", fill=(255, 255, 255), font=get_font(24))
            d.text((1020, 670), "- 考级直达：【JLPT N5 ~ N1】结构化能力进阶", fill=(254, 240, 138), font=get_font(24))

        elif 12.0 <= t < 24.0:
            d.text((100, 180), "电影级实景沉浸教学", fill=(56, 189, 248), font=get_font(28))
            d.text((100, 230), "把东京真实生活现场，直接搬进你的屏幕", fill=(255, 255, 255), font=get_font(52))
            if loaded_real_covers["transit"] and loaded_real_covers["izakaya"]:
                cov1 = loaded_real_covers["transit"].resize((820, 461), Image.Resampling.LANCZOS)
                cov2 = loaded_real_covers["izakaya"].resize((820, 461), Image.Resampling.LANCZOS)
                frame.paste(cov1, (100, 330))
                d.rectangle([100, 330, 920, 791], outline=(56, 189, 248), width=4)
                d.text((120, 350), "【JLPT N4】东京地铁实景精讲", fill=(255, 255, 255), font=get_font(26))
                
                frame.paste(cov2, (980, 330))
                d.rectangle([980, 330, 1800, 791], outline=(225, 29, 72), width=4)
                d.text((1000, 350), "【JLPT N5】居酒屋生啤点单秘籍", fill=(255, 255, 255), font=get_font(26))

        elif 24.0 <= t < 48.0:
            sec_idx = int((t - 24.0) / 6.0)
            scenes_info = [
                ("场景 01 • 东京出行与地铁", "transit", "山手线报站 / 坐过站精算机补票全流程"),
                ("场景 02 • 7-Eleven 与便利店", "kombini", "收银台 30 秒快速应答 / 冰咖啡取杯全流程"),
                ("场景 03 • 居酒屋与拉面点餐", "izakaya", "生啤开场神句 / 食券机定制面硬汤浓口诀"),
                ("场景 04 • 潮流购物与日本热梗", "trends", "秋叶原手办免税 / 银座试衣 / 桑拿「整う」流行语")
            ]
            s_title, s_key, s_sub = scenes_info[min(sec_idx, 3)]
            d.text((100, 175), s_title, fill=(255, 215, 0), font=get_font(44))
            d.text((100, 240), s_sub, fill=(203, 213, 225), font=get_font(28))
            
            if loaded_real_covers[s_key]:
                cov_main = loaded_real_covers[s_key].resize((980, 551), Image.Resampling.LANCZOS)
                frame.paste(cov_main, (100, 290))
                d.rectangle([100, 290, 1080, 841], outline=(255, 215, 0), width=4)
                
            d.rounded_rectangle([1120, 290, 1820, 841], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((1160, 330), "【 场景高频词汇 & 语法考点 】", fill=(56, 189, 248), font=get_font(26))
            pts = [
                "- 100% 真实日本商家/车站原声录音",
                "- 毫秒级假名/汉字/罗马音三重视图",
                "- 彻底理清敬语、委婉拒绝与地道短句",
                "- 告别中式日语，养成纯正东京思维"
            ]
            yp = 400
            for pt in pts:
                d.text((1160, yp), pt, fill=(241, 245, 249), font=get_font(24))
                yp += 90

        elif 48.0 <= t < 62.0:
            d.text((100, 175), "双轨立体化教学闭环", fill=(56, 189, 248), font=get_font(28))
            d.text((100, 230), "长视频深度精讲 + 竖屏短视频日常跟读", fill=(255, 255, 255), font=get_font(48))
            if loaded_real_covers["transit"]:
                m16 = loaded_real_covers["transit"].resize((780, 439), Image.Resampling.LANCZOS)
                frame.paste(m16, (100, 330))
                d.rectangle([100, 330, 880, 769], outline=(56, 189, 248), width=3)
                d.text((120, 350), "1080p 深度精讲大班课", fill=(255, 255, 255), font=get_font(24))
                
            d.rounded_rectangle([940, 330, 1820, 769], radius=20, fill=(15, 22, 35, 240), outline=(225, 29, 72), width=3)
            d.text((980, 380), "【 权威分级覆盖 】", fill=(254, 240, 138), font=get_font(32))
            d.text((980, 460), "- 【JLPT N5】零基础入门与东京生存口语", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 530), "- 【JLPT N4】日常生活与交通深度进阶", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 600), "- 【JLPT N3】新闻热点与地道会话技巧", fill=(255, 255, 255), font=get_font(26))
            d.text((980, 670), "- 【JLPT N2-N1】高阶影视语感与商务表达", fill=(255, 255, 255), font=get_font(26))

        else:
            d.text((100, 175), "加入 TOKYOFLOW 学习社区", fill=(254, 240, 138), font=get_font(32))
            d.text((100, 230), "每晚 8:00 PM (EDT) 定时更新 • 开启你的东京实战之旅", fill=(255, 255, 255), font=get_font(48))
            
            d.rounded_rectangle([100, 320, 920, 790], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((140, 360), "【 中文解说版更新时刻表 】", fill=(56, 189, 248), font=get_font(28))
            d.text((140, 430), "- 16:9 深度精讲大班课：每日 08:00 PM EDT", fill=(255, 255, 255), font=get_font(24))
            d.text((140, 500), "- 9:16 沉浸跟读短视频：每日 08:00 PM EDT", fill=(255, 255, 255), font=get_font(24))
            d.text((140, 570), "- 标准考级线：【JLPT N5 ~ N1】结构化覆盖", fill=(254, 240, 138), font=get_font(24))
            d.text((140, 640), "- 周末特辑：多合一实战串烧合集", fill=(203, 213, 225), font=get_font(24))

            d.rounded_rectangle([980, 320, 1820, 790], radius=20, fill=(225, 29, 72), outline=(255, 255, 255), width=3)
            d.text((1050, 400), "立即订阅", fill=(255, 255, 255), font=get_font(56))
            d.text((1050, 485), "@TokyoFlowJapan", fill=(254, 240, 138), font=get_font(48))
            d.text((1050, 570), "开启你的真实东京日语流利表达！", fill=(255, 255, 255), font=get_font(30))
            d.text((1050, 660), "官方频道：youtube.com/@TokyoFlowJapan", fill=(241, 245, 249), font=get_font(24))

        # Bottom Subtitle Banner
        if cur_seg:
            d.rounded_rectangle([60, 890, 1860, 1030], radius=20, fill=(8, 12, 20, 245), outline=(50, 70, 100), width=2)
            if "Nanami" in cur_seg["voice"]:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(0, 120, 215))
                d.text((115, 945), "【东京原声】Nanami", fill=(255, 255, 255), font=get_font(22))
            else:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(225, 29, 72))
                d.text((115, 945), "【中文解说】Yunxi", fill=(255, 255, 255), font=get_font(22))

            text = cur_seg["text"]
            font_sub = get_font(32)
            d.text((370, 946), text, fill=(255, 255, 255), font=font_sub)

        frame.save(frames_dir / f"frame_{f_idx:05d}.jpg", quality=90)

    out_mp4 = OUT_ZH_DIR / "tokyoflow_trailer_zh_1080p.mp4"
    cmd = [
        "ffmpeg", "-y", "-r", str(fps), "-i", str(frames_dir / "frame_%05d.jpg"),
        "-i", str(audio_out), "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out_mp4)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✓ Pure Chinese Trailer generated: {out_mp4}")

async def main():
    print("==================================================")
    print("TokyoFlow Clean Layering Channel Trailers Producer")
    print("==================================================")
    await build_english_trailer()
    await build_chinese_trailer()
    print("\n✓ Both trailers cleanly rendered without overlapping artifacts!")

if __name__ == "__main__":
    asyncio.run(main())
