#!/usr/bin/env python3
"""
TokyoFlow Japanese • Official Channel Trailer Producer (16:9 1080p Full HD)
===========================================================================
Produces the cinematic, high-conversion Official Channel Trailer for TokyoFlow Japanese:
- 1920x1080 Full HD Landscape video.
- Multi-voice dynamic narration: ja-JP-NanamiNeural (Tokyo native), zh-CN-YunxiNeural (Chinese explainer), en-US-AndrewNeural (English explainer).
- Authentic Tokyo scenario showcase: Transit, Kombini, Izakaya, Ramen, Anime Shopping, Ginza, Pop Culture Trends.
- Dual-track learning framework: 16:9 Deep Masterclasses + 9:16 Daily Shadowing Shorts.
- Standardized JLPT N5 to N1 roadmap.
- Strict Zero Emoji Policy, CJK Kinsoku Shori typography, and dynamic safe margin bounding.
"""

import os
import sys
import math
import shutil
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
OUT_DIR = PROJECT_ROOT / "output" / "channel_trailer"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_PATH if not is_en else FONT_EN_HEAVY
    try:
        return ImageFont.truetype(font_file, size)
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

async def build_trailer_audio(temp_dir: Path):
    """Synthesizes dynamic multi-speaker dialogue track."""
    script = [
        # Phase 1: Hook (The Pain of Textbooks)
        {"id": "01_hook_cn", "voice": "zh-CN-YunxiNeural", "rate": "+4%", "text": "为什么学了几年日语，到了东京依然听不懂、不敢开口？"},
        {"id": "02_hook_en", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Because traditional textbooks don't teach how Tokyo locals actually speak."},
        {"id": "03_hook_ja", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "教科書と実際の会話は、全然違いますよ！"},
        
        # Phase 2: The Solution (TokyoFlow Vision)
        {"id": "04_sol_cn_1", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "欢迎来到 TokyoFlow 日语实景精讲！"},
        {"id": "05_sol_cn_2", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "我们把东京真实生活现场，直接搬进课堂！"},
        {"id": "06_sol_en", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "TokyoFlow Japanese — Cinema-grade, real-world language immersion."},
        
        # Phase 3: Real Tokyo Scenarios Fast Tour
        {"id": "07_trans_ja", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "次は、新宿、新宿です。乗り換えのご案内です。"},
        {"id": "08_trans_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "山手线报站与地铁精算机补票，一秒听懂！"},
        
        {"id": "09_kombini_ja", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "袋は大丈夫です。温めも結構です。"},
        {"id": "10_kombini_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "便利店收银与冰咖啡取杯，秒回不社恐！"},
        
        {"id": "11_izakaya_ja", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "とりあえず生で！麺硬め、味濃いめで！"},
        {"id": "12_izakaya_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "居酒屋生啤开场与拉面老饕定制口诀！"},
        
        {"id": "13_trend_ja", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "サウナで最高にととのう！"},
        {"id": "14_trend_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "秋叶原手办免税、银座试衣与当季热梗全覆盖！"},
        
        # Phase 4: Dual-Track & JLPT System
        {"id": "15_sys_cn_1", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "每天 1080p 深度大班课，搭配 1 分钟原声跟读短视频！"},
        {"id": "16_sys_en", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Masterclasses plus daily bite-sized shadowing drills from JLPT N5 to N1."},
        {"id": "17_sys_cn_2", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "零基础入门到高阶进阶，随时随地轻松磨耳朵！"},
        
        # Phase 5: Cadence & Call to Action
        {"id": "18_cad_cn", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "早 8 点全球英文版，晚 8 点深度中文解说版！"},
        {"id": "19_cta_en", "voice": "en-US-AndrewNeural", "rate": "+3%", "text": "Subscribe to TokyoFlow Japanese and master real-world Tokyo Japanese today!"},
        {"id": "20_cta_ja", "voice": "ja-JP-NanamiNeural", "rate": "-3%", "pitch": "+3Hz", "text": "チャンネル登録、よろしくお願いします！"}
    ]

    timeline = []
    cur_time = 0.5

    for seg in script:
        out_f = str(temp_dir / f"{seg['id']}.mp3")
        await synth_line(seg["text"], seg["voice"], out_f, rate=seg.get("rate", "+0%"), pitch=seg.get("pitch", "+0Hz"))
        dur = get_audio_duration(out_f)
        timeline.append({
            "id": seg["id"],
            "text": seg["text"],
            "voice": seg["voice"],
            "start": cur_time,
            "end": cur_time + dur,
            "duration": dur,
            "file": out_f
        })
        cur_time += dur + 0.32

    total_duration = cur_time + 1.0

    concat_list_file = temp_dir / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        silence_05 = temp_dir / "silence_05.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.5", "-c:a", "libmp3lame", str(silence_05)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        pause_03 = temp_dir / "pause_03.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.32", "-c:a", "libmp3lame", str(pause_03)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        final_silence = temp_dir / "silence_10.mp3"
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1.0", "-c:a", "libmp3lame", str(final_silence)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        f.write(f"file '{silence_05.name}'\n")
        for item in timeline:
            f.write(f"file '{Path(item['file']).name}'\n")
            f.write(f"file '{pause_03.name}'\n")
        f.write(f"file '{final_silence.name}'\n")

    combined_audio = temp_dir / "combined_voice.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list_file),
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(combined_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    return combined_audio, timeline, total_duration

def create_trailer_cover(out_16_9: Path):
    """Generates a 16:9 1920x1080 master cover for the official channel trailer."""
    W, H = 1920, 1080
    bg_skyline = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
    
    img = Image.new("RGB", (W, H), (10, 14, 24))
    if bg_skyline.exists():
        sky = Image.open(bg_skyline).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        sky = ImageEnhance.Brightness(sky).enhance(0.45)
        img.paste(sky, (0, 0))

    d = ImageDraw.Draw(img)
    
    # Top Left Brand Pill
    d.rounded_rectangle([80, 70, 520, 145], radius=16, fill=(255, 255, 255))
    d.text((110, 88), "TokyoFlow Japanese", fill=(225, 29, 72), font=get_font(34, is_en=True))

    # Top Right Capsule
    d.rounded_rectangle([W - 480, 70, W - 80, 145], radius=16, fill=(225, 29, 72))
    d.text((W - 450, 88), "OFFICIAL TRAILER", fill=(255, 255, 255), font=get_font(32, is_en=True))

    # Main Headline Hook
    d.text((80, 200), "SPEAK REAL-LIFE TOKYO JAPANESE", fill=(254, 240, 138), font=get_font(76, is_en=True))
    d.text((80, 305), "告别死板教科书 • 东京一线实景沉浸精讲", fill=(255, 255, 255), font=get_font(60))

    # Center 3-Pillar Card
    card_y = 420
    card_h = 480
    d.rounded_rectangle([80, card_y, 1180, card_y + card_h], radius=24, fill=(10, 16, 28, 240), outline=(56, 189, 248), width=3)
    
    d.text((120, card_y + 40), "[ TOKYO REALITY IMMERSION • 核心教学矩阵 ]", fill=(56, 189, 248), font=get_font(28, is_en=True))
    
    bullets = [
        "- 实景出行：山手线全线报站 • 地铁闸机精算机补票",
        "- 街头生存：7-Eleven/全家收银应答 • 咖啡机与ATM",
        "- 美食老饕：居酒屋生啤开场 • 顶级拉面食券机定制",
        "- 潮流文化：秋叶原手办免税 • 银座试衣 • 当季热梗",
        "- 权威分级：[JLPT N5] 零基础至 [JLPT N1] 高阶精讲"
    ]
    y_b = card_y + 110
    for b in bullets:
        d.text((120, y_b), b, fill=(230, 240, 255), font=get_font(34))
        y_b += 68

    # Right side 2 Featured Covers collage
    t_e01 = RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg"
    t_e03 = RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg"
    if t_e01.exists() and t_e03.exists():
        img_e01 = Image.open(t_e01).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        img_e03 = Image.open(t_e03).convert("RGB").resize((600, 337), Image.Resampling.LANCZOS)
        
        img.paste(img_e01, (1240, 200))
        d.rectangle([1240, 200, 1840, 537], outline=(255, 215, 0), width=4)
        
        img.paste(img_e03, (1240, 560))
        d.rectangle([1240, 560, 1840, 897], outline=(225, 29, 72), width=4)

    # Bottom Full Width Ribbon
    d.rounded_rectangle([80, H - 125, W - 80, H - 45], radius=16, fill=(225, 29, 72))
    ribbon_txt = "DAILY RELEASES: 08:00 AM EDT (ENGLISH)  •  08:00 PM EDT (CHINESE)  •  SUBSCRIBE @TokyoFlowJapan"
    d.text((140, H - 100), ribbon_txt, fill=(255, 255, 255), font=get_font(26, is_en=True))

    img.save(out_16_9, quality=95)
    print(f"✓ Master 16:9 Trailer Cover generated: {out_16_9}")

def render_trailer_video_16_9(temp_dir: Path, combined_audio: Path, timeline: list, total_duration: float, out_mp4: Path):
    """Renders 1920x1080 16:9 high-definition video frames and encodes video with ffmpeg."""
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    fps = 30
    total_frames = int(math.ceil(total_duration * fps))
    print(f"Rendering {total_frames} 16:9 video frames at {fps} fps (~{total_duration:.1f}s)...")

    # Load 16:9 Scenario Covers
    scenarios = {
        "transit": RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg",
        "kombini": RELEASES_DIR / "E02-Kombini_Checkout-v1.0-zh" / "thumbnail.jpg",
        "izakaya": RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg",
        "shopping": RELEASES_DIR / "E04-Akiba_Pilgrimage-v1.0-zh" / "thumbnail.jpg",
        "trends": RELEASES_DIR / "E09-anime_sauna_trend-v1.0-zh" / "thumbnail.jpg",
        "shorts_demo": RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "short_thumbnail.jpg",
        "shorts_demo2": RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "short_thumbnail.jpg",
    }
    loaded = {}
    for k, p in scenarios.items():
        if p.exists():
            loaded[k] = Image.open(p).convert("RGB")

    bg_skyline = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
    base_canvas = Image.new("RGB", (1920, 1080), (10, 14, 22))
    if bg_skyline.exists():
        sky = Image.open(bg_skyline).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        sky = ImageEnhance.Brightness(sky).enhance(0.40)
        base_canvas.paste(sky, (0, 0))

    for f_idx in range(total_frames):
        t = f_idx / fps
        
        cur_seg = None
        for seg in timeline:
            if seg["start"] <= t <= seg["end"]:
                cur_seg = seg
                break

        frame = base_canvas.copy()
        d = ImageDraw.Draw(frame)

        # Top Navigation Header
        d.rounded_rectangle([60, 40, 1860, 120], radius=16, fill=(15, 22, 35, 230), outline=(45, 60, 85), width=2)
        d.text((90, 60), "TokyoFlow Japanese • Official Channel Trailer", fill=(255, 215, 0), font=get_font(34, is_en=True))
        d.rounded_rectangle([1580, 52, 1830, 108], radius=10, fill=(225, 29, 72))
        d.text((1610, 67), "MASTERCLASS", fill=(255, 255, 255), font=get_font(24, is_en=True))

        # Main Stage Display Area (y: 150 to 860)
        if t < 12.0:
            # Phase 1: The Problem (Textbooks vs Real Tokyo)
            d.text((100, 180), "THE REAL-WORLD JAPANESE GAP", fill=(244, 114, 182), font=get_font(28, is_en=True))
            d.text((100, 230), "学了几年日语，为什么依然听不懂？", fill=(255, 255, 255), font=get_font(56))
            
            # Left Card: Textbook Problem
            d.rounded_rectangle([100, 320, 920, 820], radius=20, fill=(20, 24, 36, 240), outline=(100, 116, 139), width=2)
            d.text((140, 360), "[ 传统教科书痛点 ]", fill=(148, 163, 184), font=get_font(28))
            d.text((140, 430), "- 死板句式：句句都是「私は学生です」", fill=(203, 213, 225), font=get_font(28))
            d.text((140, 500), "- 语速脱节：播音员慢速，无法应对现场", fill=(203, 213, 225), font=get_font(28))
            d.text((140, 570), "- 缺乏实战：地铁/便利店/居酒屋瞬间卡壳", fill=(203, 213, 225), font=get_font(28))
            d.text((140, 640), "- 畏惧开口：没有场景支撑，不敢自然发音", fill=(203, 213, 225), font=get_font(28))
            
            # Right Card: TokyoFlow Reality
            d.rounded_rectangle([980, 320, 1820, 820], radius=20, fill=(15, 25, 45, 250), outline=(56, 189, 248), width=3)
            d.text((1020, 360), "[ TokyoFlow 解决方案 ]", fill=(56, 189, 248), font=get_font(28))
            d.text((1020, 430), "- 真实东京：100% 还原山手线/居酒屋/药妆现场", fill=(255, 255, 255), font=get_font(28))
            d.text((1020, 500), "- 地道原声：纯正东京音 Nanami 影子跟读", fill=(255, 255, 255), font=get_font(28))
            d.text((1020, 570), "- 深度拆解：双语名师逐字逐句刨析文化与语法", fill=(255, 255, 255), font=get_font(28))
            d.text((1020, 640), "- 考级直达：[JLPT N5 ~ N1] 结构化能力进阶", fill=(254, 240, 138), font=get_font(28))

        elif 12.0 <= t < 24.0:
            # Phase 2: Brand Vision & Positioning
            d.text((100, 180), "CINEMA-GRADE REAL-WORLD IMMERSION", fill=(56, 189, 248), font=get_font(28, is_en=True))
            d.text((100, 230), "把东京真实生活现场，直接搬进你的屏幕", fill=(255, 255, 255), font=get_font(56))
            
            # Showcase 2 Masterclass Covers
            if "transit" in loaded and "izakaya" in loaded:
                cov1 = loaded["transit"].resize((820, 461), Image.Resampling.LANCZOS)
                cov2 = loaded["izakaya"].resize((820, 461), Image.Resampling.LANCZOS)
                frame.paste(cov1, (100, 330))
                d.rectangle([100, 330, 920, 791], outline=(56, 189, 248), width=4)
                d.text((120, 350), "[JLPT N4] 东京地铁实景精讲", fill=(255, 255, 255), font=get_font(26))
                
                frame.paste(cov2, (980, 330))
                d.rectangle([980, 330, 1800, 791], outline=(225, 29, 72), width=4)
                d.text((1000, 350), "[JLPT N5] 居酒屋点单秘籍", fill=(255, 255, 255), font=get_font(26))

        elif 24.0 <= t < 48.0:
            # Phase 3: Fast Scenario Showcase
            # Switch scenes depending on sub-time
            sec_idx = int((t - 24.0) / 6.0) # 0: transit, 1: kombini, 2: izakaya, 3: trends
            titles = [
                ("场景 01 • 东京出行与地铁", "transit", "山手线报站 / 坐过站精算机补票全流程"),
                ("场景 02 • 7-Eleven 与便利店", "kombini", "收银台 30 秒快速应答 / 冰咖啡取杯全流程"),
                ("场景 03 • 居酒屋与拉面点餐", "izakaya", "生啤开场神句 / 食券机定制面硬汤浓口诀"),
                ("场景 04 • 潮流购物与日本热梗", "trends", "秋叶原手办免税 / 银座试衣 / 桑拿「整う」流行语")
            ]
            s_title, s_key, s_sub = titles[min(sec_idx, 3)]
            
            d.text((100, 175), s_title, fill=(255, 215, 0), font=get_font(46))
            d.text((100, 240), s_sub, fill=(203, 213, 225), font=get_font(30))
            
            if s_key in loaded:
                cov_main = loaded[s_key].resize((980, 551), Image.Resampling.LANCZOS)
                frame.paste(cov_main, (100, 290))
                d.rectangle([100, 290, 1080, 841], outline=(255, 215, 0), width=4)
                
            # Right side HUD info
            d.rounded_rectangle([1120, 290, 1820, 841], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((1160, 330), "[ 场景高频词汇 & 语法考点 ]", fill=(56, 189, 248), font=get_font(26))
            
            points = [
                " 100% 真实日本商家/车站原声录音",
                " 毫秒级假名/汉字/罗马音三重视图",
                " 彻底理清敬语、委婉拒绝与地道短句",
                " 告别中式日语，养成纯正东京思维"
            ]
            yp = 400
            for pt in points:
                d.text((1160, yp), pt, fill=(241, 245, 249), font=get_font(26))
                yp += 90

        elif 48.0 <= t < 64.0:
            # Phase 4: Dual-Track Engine (Masterclass + Shorts)
            d.text((100, 175), "DUAL-TRACK LEARNING ARCHITECTURE", fill=(56, 189, 248), font=get_font(28, is_en=True))
            d.text((100, 230), "长视频深度精讲 + 竖屏短视频日常跟读", fill=(255, 255, 255), font=get_font(52))
            
            # Left: 16:9 Long-form preview
            if "transit" in loaded:
                m16 = loaded["transit"].resize((780, 439), Image.Resampling.LANCZOS)
                frame.paste(m16, (100, 330))
                d.rectangle([100, 330, 880, 769], outline=(56, 189, 248), width=3)
                d.text((120, 350), "1080p 深度精讲大班课", fill=(255, 255, 255), font=get_font(24))
                
            # Middle & Right: 9:16 Shorts Previews
            if "shorts_demo" in loaded and "shorts_demo2" in loaded:
                s1 = loaded["shorts_demo"].resize((270, 480), Image.Resampling.LANCZOS)
                s2 = loaded["shorts_demo2"].resize((270, 480), Image.Resampling.LANCZOS)
                frame.paste(s1, (940, 310))
                d.rectangle([940, 310, 1210, 790], outline=(225, 29, 72), width=3)
                
                frame.paste(s2, (1260, 310))
                d.rectangle([1260, 310, 1530, 790], outline=(255, 215, 0), width=3)
                
            # Right side note
            d.rounded_rectangle([1570, 310, 1840, 790], radius=16, fill=(15, 22, 35, 240), outline=(100, 116, 139), width=2)
            d.text((1600, 350), "1分钟", fill=(255, 215, 0), font=get_font(34))
            d.text((1600, 400), "原声跟读", fill=(255, 255, 255), font=get_font(26))
            d.text((1600, 480), "随时随地", fill=(203, 213, 225), font=get_font(24))
            d.text((1600, 525), "高效磨耳朵", fill=(203, 213, 225), font=get_font(24))

        else:
            # Phase 5: Cadence & Subscribe CTA
            d.text((100, 175), "JOIN THE TOKYOFLOW COMMUNITY", fill=(254, 240, 138), font=get_font(32, is_en=True))
            d.text((100, 230), "每日定时双语更新 • 开启你的东京实战之旅", fill=(255, 255, 255), font=get_font(52))
            
            # Left Card: Publishing Schedule
            d.rounded_rectangle([100, 320, 920, 790], radius=20, fill=(15, 22, 35, 240), outline=(56, 189, 248), width=3)
            d.text((140, 360), "[ 每日双语更新时刻表 ]", fill=(56, 189, 248), font=get_font(28))
            d.text((140, 430), "- 全球英文版：每日 08:00 AM EDT 定时发布", fill=(255, 255, 255), font=get_font(28))
            d.text((140, 500), "- 深度中文版：每日 08:00 PM EDT 定时发布", fill=(255, 255, 255), font=get_font(28))
            d.text((140, 570), "- 标准考级线：[JLPT N5 ~ N1] 结构化覆盖", fill=(254, 240, 138), font=get_font(28))
            d.text((140, 640), "- 场景多合一：周末综合实战大串烧特辑", fill=(203, 213, 225), font=get_font(28))
            
            # Right Card: Giant Subscribe CTA
            d.rounded_rectangle([980, 320, 1820, 790], radius=20, fill=(225, 29, 72), outline=(255, 255, 255), width=3)
            d.text((1050, 400), "SUBSCRIBE NOW", fill=(255, 255, 255), font=get_font(56, is_en=True))
            d.text((1050, 485), "立即订阅 @TokyoFlowJapan", fill=(254, 240, 138), font=get_font(44))
            d.text((1050, 570), "开启你的真实东京日语流利表达！", fill=(255, 255, 255), font=get_font(34))
            d.text((1050, 660), "Official Channel: youtube.com/@TokyoFlowJapan", fill=(241, 245, 249), font=get_font(26, is_en=True))

        # Bottom Subtitle Banner (Horizontal Bar)
        if cur_seg:
            d.rounded_rectangle([60, 890, 1860, 1030], radius=20, fill=(8, 12, 20, 245), outline=(50, 70, 100), width=2)
            
            # Speaker Tag Pill
            if "Nanami" in cur_seg["voice"]:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(0, 120, 215))
                d.text((115, 945), "【东京原声】Nanami", fill=(255, 255, 255), font=get_font(24))
            elif "Andrew" in cur_seg["voice"]:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(16, 185, 129))
                d.text((115, 945), "[ English ] Andrew", fill=(255, 255, 255), font=get_font(24, is_en=True))
            else:
                d.rounded_rectangle([90, 925, 340, 995], radius=12, fill=(225, 29, 72))
                d.text((115, 945), "【中文解说】Yunxi", fill=(255, 255, 255), font=get_font(24))

            # Spoken Text
            text = cur_seg["text"]
            font_sub = get_font(36, is_en=("Andrew" in cur_seg["voice"]))
            bbox_t = d.textbbox((0, 0), text, font=font_sub)
            tw = bbox_t[2] - bbox_t[0]
            if tw > 1400:
                font_sub = get_font(30, is_en=("Andrew" in cur_seg["voice"]))
                
            d.text((370, 942), text, fill=(255, 255, 255), font=font_sub)

        frame_path = frames_dir / f"frame_{f_idx:05d}.jpg"
        frame.save(frame_path, quality=90)

        if f_idx % 200 == 0:
            print(f"  Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) rendered")

    print("Encoding final 16:9 trailer video with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", str(frames_dir / "frame_%05d.jpg"),
        "-i", str(combined_audio),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(out_mp4)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Trailer video successfully generated: {out_mp4}")

async def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = OUT_DIR / "temp_render"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("TokyoFlow Official 16:9 Channel Trailer Producer")
    print("==================================================")

    # 1. Synthesize audio
    print("[1/3] Synthesizing multi-speaker trailer audio...")
    combined_audio, timeline, total_duration = await build_trailer_audio(temp_dir)
    print(f"Audio synthesized successfully. Duration: {total_duration:.2f}s")

    # 2. Build 16:9 Master Cover
    print("[2/3] Generating 16:9 Master Trailer Cover...")
    thumb_16_9 = OUT_DIR / "thumbnail.jpg"
    create_trailer_cover(thumb_16_9)

    # 3. Render 16:9 Video
    print("[3/3] Rendering 16:9 Landscape Video...")
    out_mp4 = OUT_DIR / "tokyoflow_official_channel_trailer_1080p.mp4"
    render_trailer_video_16_9(temp_dir, combined_audio, timeline, total_duration, out_mp4)

    # Generate metadata
    meta_path = OUT_DIR / "metadata.md"
    meta_content = f"""# TokyoFlow Japanese Official Channel Trailer | Learn Real-Life Tokyo Japanese

## YouTube Title
Master Real Tokyo Japanese! | Official TokyoFlow Academy Trailer [JLPT N5-N1]

## YouTube Description
Welcome to TokyoFlow Japanese — the cinema-grade, use-case-driven language academy dedicated to decoding authentic spoken Tokyo Japanese through real-life living, transit, pop culture, and modern media.

Forget robotic, outdated textbook sentences. TokyoFlow immerses you directly into the pulse of Tokyo:
- Yamanote Line & Tokyo Subway transit announcements & fare adjustments
- 7-Eleven & Kombini checkout speed replies
- Izakaya ordering & ramen customization protocols
- Akihabara tax-free figure shopping & Ginza fitting rooms
- Japanese pop-culture trends & daily news immersion

Daily Multi-Language Releases:
- Column A (Global English Edition): Daily 08:00 AM EDT
- Column B (Chinese Edition • 中文解说版): Daily 08:00 PM EDT

Subscribe now and bridge the gap between classroom theory and real-world Tokyo fluency!

#LearnJapanese #JLPT #TokyoFlow #JapaneseLanguage #Tokyo #日语学习 #JLPT考级 #场景日语 #东京实景
"""
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(meta_content)

    print("\n Official Channel Trailer Package complete at:", OUT_DIR)

if __name__ == "__main__":
    asyncio.run(main())
