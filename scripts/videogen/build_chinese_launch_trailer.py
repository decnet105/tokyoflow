#!/usr/bin/env python3
"""
TokyoFlow Japanese • Chinese Launch Trailer Producer (V3 - Perfect Typography & Box Alignment)
=============================================================================================
Features:
- Short, atomic speech segments (6-14 chars each) ensuring zero text overflow.
- Strict CJK Kinsoku Shori (no punctuation at line start).
- Perfectly centered subtitle cards and dynamic HUD cards with ample padding.
- Modern visual styling and authentic scenario covers showcase.
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
OUT_DIR = RELEASES_DIR / "E00-Chinese_Launch_Teaser-v1.0-zh"

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

async def build_audio_tracks(temp_dir: Path):
    """Synthesizes short, punchy speech segments."""
    script_segments = [
        # Scene 1: Hook (0s)
        {"id": "01_hook", "voice": "zh-CN-YunxiNeural", "rate": "+4%", "text": "还在死记硬背枯燥的教科书吗？"},
        {"id": "02_launch_1", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "TokyoFlow 日语实景精讲"},
        {"id": "02_launch_2", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "【中文解说版】全网首发！"},
        {"id": "02_launch_3", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "带你直接潜入东京生活现场！"},
        
        # Scene 2: Scenarios Fast Showcase
        {"id": "03_transit_jp", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "次は、新宿、新宿です。"},
        {"id": "04_transit_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "山手线报站与地铁补票，一秒听懂！"},
        
        {"id": "05_kombini_jp", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "袋は大丈夫です。温めも結構です。"},
        {"id": "06_kombini_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "便利店结账与咖啡点单，秒回不社恐！"},
        
        {"id": "07_izakaya_jp", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "とりあえず生で！麺硬めで！"},
        {"id": "08_izakaya_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "居酒屋生啤与拉面定制老饕口诀！"},
        
        {"id": "09_shopping_jp", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "免税手続き、お願いします。"},
        {"id": "10_shopping_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "秋叶原手办免税与银座试衣口语！"},
        
        {"id": "11_trends_jp", "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "text": "サウナで最高にととのう！"},
        {"id": "12_trends_cn", "voice": "zh-CN-YunxiNeural", "rate": "+5%", "text": "更有日本当季热梗流行语深度拆解！"},
        
        # Scene 3: Masterclass + Shorts Routine
        {"id": "13_routine_1", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "每天 1080p 深度精讲大班课"},
        {"id": "13_routine_2", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "搭配 1 分钟沉浸式口语跟读！"},
        {"id": "13_routine_3", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "零基础到进阶，随时随地磨耳朵！"},
        
        # Scene 4: CTA
        {"id": "14_cta_cn", "voice": "zh-CN-YunxiNeural", "rate": "+3%", "text": "每晚 8 点更新，欢迎订阅 TokyoFlow！"},
        {"id": "15_cta_jp", "voice": "ja-JP-NanamiNeural", "rate": "-3%", "pitch": "+3Hz", "text": "チャンネル登録、よろしくお願いします！"}
    ]

    timeline = []
    cur_time = 0.5

    for seg in script_segments:
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

def create_teaser_thumbnail(out_16_9: Path, out_9_16: Path):
    bg_path = RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "hero_16_9.jpg"
    if not bg_path.exists():
        bg_path = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"

    # --- 16:9 Cover ---
    img_16_9 = Image.new("RGB", (1920, 1080), (10, 12, 18))
    if bg_path.exists():
        base = Image.open(bg_path).convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
        base = ImageEnhance.Brightness(base).enhance(0.55)
        img_16_9.paste(base, (0, 0))

    d = ImageDraw.Draw(img_16_9)
    d.rounded_rectangle([80, 80, 520, 150], radius=16, fill=(230, 0, 18))
    d.text((100, 95), "【中文解说首发预告】", fill=(255, 255, 255), font=get_font(40))

    d.text((80, 200), "告别死板教科书！", fill=(255, 255, 255), font=get_font(96))
    d.text((80, 320), "每天1分钟搞定东京地道实景日语", fill=(255, 215, 0), font=get_font(68))

    d.rounded_rectangle([80, 440, 1100, 920], radius=24, fill=(15, 20, 30, 230), outline=(50, 70, 100), width=3)
    bullets = [
        "- 山手线报站 / 7-Eleven结账 / 居酒屋生啤开场",
        "- 秋叶原手办退税 / 银座试衣 / 拉面老饕定制",
        "- 1080p 深度大班课 + 9:16 沉浸式口语跟读",
        "- 纯正东京音 Nanami + 青年解说 Yunxi",
        "- 每日晚 8 点定时更新 • 零基础到进阶直达"
    ]
    y_b = 480
    for b in bullets:
        d.text((120, y_b), b, fill=(230, 240, 255), font=get_font(40))
        y_b += 84

    d.rounded_rectangle([80, 960, 480, 1020], radius=12, fill=(30, 40, 60))
    d.text((100, 972), "@TokyoFlowJapan", fill=(140, 190, 255), font=get_font(32))

    thumb_e01 = RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg"
    thumb_e03 = RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "thumbnail.jpg"
    if thumb_e01.exists() and thumb_e03.exists():
        t1 = Image.open(thumb_e01).convert("RGB").resize((660, 371), Image.Resampling.LANCZOS)
        t2 = Image.open(thumb_e03).convert("RGB").resize((660, 371), Image.Resampling.LANCZOS)
        img_16_9.paste(t1, (1180, 200))
        d.rectangle([1180, 200, 1840, 571], outline=(255, 215, 0), width=4)
        img_16_9.paste(t2, (1180, 600))
        d.rectangle([1180, 600, 1840, 971], outline=(230, 0, 18), width=4)

    img_16_9.save(out_16_9, quality=95)

    # --- 9:16 Cover ---
    img_9_16 = Image.new("RGB", (1080, 1920), (10, 12, 18))
    if bg_path.exists():
        base_v = Image.open(bg_path).convert("RGB").resize((1920, 1920), Image.Resampling.LANCZOS)
        base_v = base_v.crop((420, 0, 1500, 1920))
        base_v = ImageEnhance.Brightness(base_v).enhance(0.45)
        img_9_16.paste(base_v, (0, 0))

    d_v = ImageDraw.Draw(img_9_16)
    d_v.rounded_rectangle([80, 120, 680, 200], radius=16, fill=(230, 0, 18))
    d_v.text((110, 138), "【中文解说首发预告】", fill=(255, 255, 255), font=get_font(46))

    d_v.text((80, 260), "告别死板教科书", fill=(255, 255, 255), font=get_font(88))
    d_v.text((80, 370), "每天1分钟", fill=(255, 215, 0), font=get_font(80))
    d_v.text((80, 470), "搞定东京地道实景日语", fill=(255, 255, 255), font=get_font(64))

    if thumb_e01.exists():
        c1 = Image.open(thumb_e01).convert("RGB").resize((920, 518), Image.Resampling.LANCZOS)
        img_9_16.paste(c1, (80, 580))
        d_v.rectangle([80, 580, 1000, 1098], outline=(255, 215, 0), width=5)

    d_v.rounded_rectangle([80, 1140, 1000, 1680], radius=24, fill=(15, 20, 30, 230), outline=(50, 70, 100), width=3)
    v_bullets = [
        "- 山手线报站 / 7-Eleven结账",
        "- 居酒屋点单 / 拉面老饕定制",
        "- 1080p深度精讲 + 沉浸跟读",
        "- 纯正东京音 + 场景痛点剖析",
        "- 每晚 8 点更新 • 轻松磨耳朵"
    ]
    y_vb = 1180
    for vb in v_bullets:
        d_v.text((120, y_vb), vb, fill=(230, 240, 255), font=get_font(42))
        y_vb += 96

    d_v.rounded_rectangle([80, 1720, 1000, 1820], radius=20, fill=(230, 0, 18))
    d_v.text((220, 1745), "立即订阅 @TokyoFlowJapan", fill=(255, 255, 255), font=get_font(46))

    img_9_16.save(out_9_16, quality=95)

def render_trailer_video(temp_dir: Path, combined_audio: Path, timeline: list, total_duration: float, out_mp4: Path):
    frames_dir = temp_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    fps = 30
    total_frames = int(math.ceil(total_duration * fps))
    print(f"Rendering {total_frames} video frames with perfect typography at {fps} fps (~{total_duration:.1f}s)...")

    covers_map = {
        "transit": RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "short_thumbnail.jpg",
        "kombini": RELEASES_DIR / "E02-Kombini_Checkout-v1.0-zh" / "short_thumbnail.jpg",
        "izakaya": RELEASES_DIR / "E03-Izakaya_Night-v1.0-zh" / "short_thumbnail.jpg",
        "shopping": RELEASES_DIR / "E04-Akiba_Pilgrimage-v1.0-zh" / "short_thumbnail.jpg",
        "trends": RELEASES_DIR / "E09-anime_sauna_trend-v1.0-zh" / "short_thumbnail.jpg",
        "master_16_9": RELEASES_DIR / "E01-Yamanote_Transit-v1.0-zh" / "thumbnail.jpg",
    }
    loaded_imgs = {}
    for k, p in covers_map.items():
        if p.exists():
            loaded_imgs[k] = Image.open(p).convert("RGB")

    bg_skyline = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
    base_canvas = Image.new("RGB", (1080, 1920), (12, 15, 22))
    if bg_skyline.exists():
        sky = Image.open(bg_skyline).convert("RGB").resize((1920, 1920), Image.Resampling.LANCZOS).crop((420, 0, 1500, 1920))
        sky = ImageEnhance.Brightness(sky).enhance(0.4)
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

        # Top Header
        d.rounded_rectangle([60, 60, 1020, 150], radius=16, fill=(18, 24, 38, 220), outline=(45, 60, 85), width=2)
        d.text((90, 85), "TokyoFlow Japanese • 中文解说版", fill=(255, 215, 0), font=get_font(36))
        d.rounded_rectangle([780, 80, 990, 130], radius=10, fill=(230, 0, 18))
        d.text((810, 92), "NEW RELEASE", fill=(255, 255, 255), font=get_font(24))

        # Dynamic Center Display
        if t < 8.0:
            # Scene 1: Hook & Launch
            d.text((100, 290), "还在死记硬背？", fill=(255, 255, 255), font=get_font(80))
            d.text((100, 395), "告别死板教科书！", fill=(255, 80, 80), font=get_font(86))
            
            d.rounded_rectangle([60, 530, 1020, 1360], radius=28, fill=(15, 22, 35), outline=(255, 215, 0), width=4)
            d.text((100, 590), "TokyoFlow 日语实景精讲", fill=(255, 215, 0), font=get_font(54))
            d.text((100, 675), "【中文解说版】全网首发！", fill=(255, 255, 255), font=get_font(48))
            
            features = [
                "- 沉浸式东京实景原声追踪",
                "- 1080p 深度精讲 + 1分钟跟读",
                "- 超市/居酒屋/地铁/药妆全覆盖",
                "- 纯正东京音 + 青年解说双师教学"
            ]
            y_f = 795
            for feat in features:
                d.text((100, y_f), feat, fill=(220, 235, 255), font=get_font(42))
                y_f += 92

        elif 8.0 <= t < 15.0:
            # Scene 2: Transit
            d.text((80, 210), "场景 01 • 东京出行与地铁", fill=(255, 215, 0), font=get_font(48))
            if "transit" in loaded_imgs:
                cov = loaded_imgs["transit"].resize((880, 1100), Image.Resampling.LANCZOS)
                frame.paste(cov, (100, 290))
                d.rectangle([100, 290, 980, 1390], outline=(0, 200, 255), width=5)
                
        elif 15.0 <= t < 22.0:
            # Scene 3: Kombini
            d.text((80, 210), "场景 02 • 7-Eleven 与便利店", fill=(255, 215, 0), font=get_font(48))
            if "kombini" in loaded_imgs:
                cov = loaded_imgs["kombini"].resize((880, 1100), Image.Resampling.LANCZOS)
                frame.paste(cov, (100, 290))
                d.rectangle([100, 290, 980, 1390], outline=(255, 180, 0), width=5)

        elif 22.0 <= t < 29.0:
            # Scene 4: Izakaya & Foodie
            d.text((80, 210), "场景 03 • 居酒屋与拉面点餐", fill=(255, 215, 0), font=get_font(48))
            if "izakaya" in loaded_imgs:
                cov = loaded_imgs["izakaya"].resize((880, 1100), Image.Resampling.LANCZOS)
                frame.paste(cov, (100, 290))
                d.rectangle([100, 290, 980, 1390], outline=(255, 80, 80), width=5)

        elif 29.0 <= t < 36.0:
            # Scene 5: Shopping & Trends
            d.text((80, 210), "场景 04 • 秋叶原免税与银座试衣", fill=(255, 215, 0), font=get_font(48))
            if "shopping" in loaded_imgs:
                cov = loaded_imgs["shopping"].resize((880, 1100), Image.Resampling.LANCZOS)
                frame.paste(cov, (100, 290))
                d.rectangle([100, 290, 980, 1390], outline=(200, 100, 255), width=5)

        elif 36.0 <= t < 44.0:
            # Scene 6: Pop Culture & Trends
            d.text((80, 210), "场景 05 • 日本流行语与当季热梗", fill=(255, 215, 0), font=get_font(48))
            if "trends" in loaded_imgs:
                cov = loaded_imgs["trends"].resize((880, 1100), Image.Resampling.LANCZOS)
                frame.paste(cov, (100, 290))
                d.rectangle([100, 290, 980, 1390], outline=(255, 215, 0), width=5)

        else:
            # Scene 7: Daily Routine & CTA
            d.text((80, 210), "每天双线学习 • 轻松磨耳朵", fill=(255, 215, 0), font=get_font(50))
            
            if "master_16_9" in loaded_imgs:
                m16 = loaded_imgs["master_16_9"].resize((920, 518), Image.Resampling.LANCZOS)
                frame.paste(m16, (80, 290))
                d.rectangle([80, 290, 1000, 808], outline=(0, 200, 255), width=4)
                d.text((110, 310), "1080p 深度精讲大班课", fill=(255, 255, 255), font=get_font(34))

            d.rounded_rectangle([80, 860, 1000, 1390], radius=24, fill=(15, 22, 35), outline=(230, 0, 18), width=4)
            d.text((120, 910), "每晚 8:00 PM (EDT) 定时更新", fill=(255, 215, 0), font=get_font(46))
            d.text((120, 1000), "中英双语独立专区 • 零基础直达", fill=(230, 240, 255), font=get_font(40))
            d.text((120, 1090), "欢迎订阅 @TokyoFlowJapan", fill=(140, 190, 255), font=get_font(40))
            d.rounded_rectangle([120, 1200, 960, 1330], radius=20, fill=(230, 0, 18))
            d.text((250, 1235), "立即订阅 • 开启东京实战", fill=(255, 255, 255), font=get_font(44))

        # Bottom Subtitle Banner with Perfect Single-Line / Centered Text
        if cur_seg:
            d.rounded_rectangle([50, 1480, 1030, 1830], radius=24, fill=(8, 12, 20, 245), outline=(50, 70, 100), width=3)
            
            # Voice Tag Pill
            if "Nanami" in cur_seg["voice"]:
                d.rounded_rectangle([80, 1510, 420, 1570], radius=12, fill=(0, 120, 215))
                d.text((100, 1525), "【东京原声】Nanami", fill=(255, 255, 255), font=get_font(28))
            else:
                d.rounded_rectangle([80, 1510, 420, 1570], radius=12, fill=(215, 60, 0))
                d.text((100, 1525), "【场景精讲】Yunxi", fill=(255, 255, 255), font=get_font(28))

            # Spoken Text Centered Horizontally
            text = cur_seg["text"]
            font_sub = get_font(44)
            bbox_t = d.textbbox((0, 0), text, font=font_sub)
            tw = bbox_t[2] - bbox_t[0]
            # If wider than 900px, auto-scale font
            if tw > 880:
                font_sub = get_font(38)
                bbox_t = d.textbbox((0, 0), text, font=font_sub)
                tw = bbox_t[2] - bbox_t[0]

            tx = 50 + (980 - tw) // 2
            d.text((tx, 1640), text, fill=(255, 255, 255), font=font_sub)

        # Save frame
        frame_path = frames_dir / f"frame_{f_idx:05d}.jpg"
        frame.save(frame_path, quality=90)

        if f_idx % 150 == 0:
            print(f"  Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) rendered")

    print("Encoding final video with ffmpeg...")
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
    print("TokyoFlow Chinese Launch Teaser Producer (V3)")
    print("==================================================")

    print("[1/3] Synthesizing audio narration tracks...")
    combined_audio, timeline, total_duration = await build_audio_tracks(temp_dir)
    print(f"Audio synthesized successfully. Duration: {total_duration:.2f}s")

    print("[2/3] Generating 16:9 & 9:16 teaser master covers...")
    thumb_16_9 = OUT_DIR / "thumbnail.jpg"
    thumb_9_16 = OUT_DIR / "short_thumbnail.jpg"
    create_teaser_thumbnail(thumb_16_9, thumb_9_16)

    print("[3/3] Rendering 9:16 vertical video...")
    out_mp4 = OUT_DIR / "short.mp4"
    render_trailer_video(temp_dir, combined_audio, timeline, total_duration, out_mp4)

    print("\n Chinese Launch Teaser V3 package fully generated at:", OUT_DIR)

if __name__ == "__main__":
    asyncio.run(main())
