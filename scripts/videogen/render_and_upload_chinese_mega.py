#!/usr/bin/env python3
"""
TokyoFlow Japanese • Master Render and Upload Engine (WL01 & WM01 Chinese Editions)
===================================================================================
1. Renders 1080p Master Video & 9:16 Shorts for WL.01 (Last Mile Cinema Masterclass - Chinese)
2. Renders 1080p Master Video & 9:16 Shorts for WM.01 (Weekday Survival Mega Compilation - Chinese)
3. Uploads all long-form videos and shorts to YouTube with notifySubscribers = False
4. Updates YouTube playlists, publish ledger, and website mappings
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from youtube_auth import get_authenticated_service
from youtube_publisher import (
    load_ledger, save_ledger, upload_video_asset, extract_metadata_fields,
    get_or_create_language_playlist, add_video_to_playlist, resolve_playlist_id,
    resolve_jlpt_playlist_id, get_slot_for_asset, detect_release_locale, RELEASES_DIR,
    EST_TZ
)

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
    try:
        return float(res.stdout.strip())
    except Exception:
        return 5.0

# ==========================================
# 1. RENDER WL.01 CHINESE VIDEO (1080p & 9:16)
# ==========================================

def render_wl01_zh_video(release_dir: Path):
    """Renders 1080p video for WL01 Chinese."""
    out_video = release_dir / "video.mp4"
    if out_video.exists() and out_video.stat().st_size > 1000000:
        print(f"  [OK] WL.01 视频已存在: {out_video}")
        return

    print("  >> 正在渲染 WL.01《最后的里程》中文版 1080p 视频...")
    audio_dir = release_dir / "audio"
    script_file = release_dir / "script.json"
    script_data = json.loads(script_file.read_text(encoding="utf-8"))
    
    tmp_dir = PROJECT_ROOT / "tmp" / "videogen" / "wl01_zh_render"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"

    width, height = 1920, 1080
    fps = 30
    clip_files = []

    for ch in script_data["screenplay"]:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            audio_path = audio_dir / f"seg_{seg_id}.mp3"
            if not audio_path.exists():
                continue

            dur = get_audio_duration(str(audio_path))
            out_clip = tmp_dir / f"clip_{seg_id}.mp4"
            total_frames = int(dur * fps) + 1

            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{width}x{height}",
                "-pix_fmt", "rgb24",
                "-r", str(fps),
                "-i", "-",
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", str(fps),
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                "-shortest",
                str(out_clip)
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps
                    img = Image.new("RGB", (width, height), (15, 23, 42))
                    draw = ImageDraw.Draw(img)

                    # Top Banner
                    draw.rectangle([(0, 0), (width, 75)], fill=(10, 15, 28))
                    draw.text((60, 22), "TokyoFlow 日语影视大课  |  WL.01《最后的里程》影视沉浸精讲", fill=(255, 255, 255), font=get_font(26))
                    draw.text((width - 400, 24), f"【JLPT N5-N2】• {ch_title}", fill=(244, 114, 182), font=get_font(22))

                    # Center Card
                    draw.rounded_rectangle([(100, 150), (width - 100, height - 120)], radius=24, fill=(10, 15, 28), outline=(56, 189, 248), width=3)
                    draw.text((140, 190), f"章节 {ch_id} • {ch_title}", fill=(56, 189, 248), font=get_font(28))

                    char_name = seg.get("character", "云希")
                    draw.text((140, 250), f"讲解 / 台词：{char_name}", fill=(250, 204, 21), font=get_font(32))

                    content_text = seg.get("content", "")
                    if seg.get("lang") == "ja":
                        draw.text((140, 340), content_text, fill=(255, 255, 255), font=get_font(44))
                        draw.text((140, 440), f"读音：{seg.get('furi', '')}", fill=(244, 114, 182), font=get_font(28))
                        draw.text((140, 500), f"中文：{seg.get('meaning', '')}", fill=(226, 232, 240), font=get_font(32))
                        if seg.get("grammar"):
                            draw.text((140, 600), f"核心语法：{seg.get('grammar')}", fill=(52, 211, 153), font=get_font(28))
                    else:
                        # Chinese explanation
                        lines = [content_text[i:i+38] for i in range(0, len(content_text), 38)]
                        cy = 340
                        for line in lines[:8]:
                            draw.text((140, cy), line, fill=(255, 255, 255), font=get_font(34))
                            cy += 55

                    # Bottom Bar
                    draw.rectangle([(0, height - 70), (width, height)], fill=(225, 29, 72))
                    draw.text((60, height - 50), "100% 东京原声 (Nanami) + 云希全中文名师精讲  •  TokyoFlow 日语实景学院", fill=(255, 255, 255), font=get_font(22))

                    proc.stdin.write(img.tobytes())
            except Exception:
                pass
            finally:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait()

            clip_files.append(out_clip)

    concat_txt = tmp_dir / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in clip_files:
            f.write(f"file '{cf.resolve()}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(out_video)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  [OK] WL.01 1080p 视频生成完成: {out_video}")

def render_wl01_zh_short(release_dir: Path):
    """Renders 9:16 Short for WL01 Chinese."""
    out_short = release_dir / "short.mp4"
    if out_short.exists() and out_short.stat().st_size > 500000:
        print(f"  [OK] WL.01 短视频已存在: {out_short}")
        return

    print("  >> 正在渲染 WL.01 中文版 9:16 跟读短片...")
    audio_path = release_dir / "audio" / "seg_0.2.mp3"
    if not audio_path.exists():
        return

    dur = get_audio_duration(str(audio_path))
    width, height = 1080, 1920
    fps = 30
    total_frames = int((dur + 3.0) * fps)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(dur + 2.5),
        str(out_short)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            img = Image.new("RGB", (width, height), (15, 23, 42))
            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle([(40, 50), (width - 40, 140)], radius=16, fill=(15, 23, 42))
            draw.text((70, 75), "TokyoFlow 日语影视 • 【JLPT N5-N2】WS.01", fill=(244, 114, 182), font=get_font(28))

            draw.rounded_rectangle([(40, 180), (width - 40, 380)], radius=20, fill=(10, 15, 28), outline=(250, 204, 21), width=3)
            draw.text((70, 210), "电影《最后的里程》影视跟读", fill=(250, 204, 21), font=get_font(32))
            draw.text((70, 270), "2.7米/秒 绝不停运？", fill=(255, 255, 255), font=get_font(38))
            draw.text((70, 330), "满岛光 × 冈田将生 2024 现象级悬疑大片", fill=(148, 163, 184), font=get_font(24))

            draw.rounded_rectangle([(40, 430), (width - 40, 1200)], radius=24, fill=(10, 15, 28), outline=(56, 189, 248), width=3)
            draw.text((70, 470), "[ 高光台词 • 影子跟读 ]", fill=(56, 189, 248), font=get_font(26))
            draw.text((70, 550), "ベルトコンベアを", fill=(255, 255, 255), font=get_font(44))
            draw.text((70, 630), "止めるわけにはいきません。", fill=(254, 240, 138), font=get_font(42))
            draw.text((70, 750), "Beruto konbea o tomeru wake ni wa ikimasen.", fill=(244, 114, 182), font=get_font(26))
            draw.text((70, 830), "中文：「我们绝不能停下传送带。」", fill=(226, 232, 240), font=get_font(30))
            draw.text((70, 930), "• JLPT N3 语法：~わけにはいかない", fill=(52, 211, 153), font=get_font(28))
            draw.text((70, 990), "• 道德与社会契约约束下的「绝不能」", fill=(148, 163, 184), font=get_font(24))

            draw.rounded_rectangle([(40, 1260), (width - 40, 1820)], radius=20, fill=(225, 29, 72))
            draw.text((70, 1300), "观看 25分钟 完整影视大课 (WL.01)", fill=(255, 255, 255), font=get_font(34))
            draw.text((70, 1380), "• 掌握 80+ 职场高频口语句型", fill=(254, 240, 138), font=get_font(26))
            draw.text((70, 1440), "• 破解东京高语境职场潜台词", fill=(255, 255, 255), font=get_font(26))
            draw.text((70, 1520), "tokyoflow.app 官网下载完整讲义", fill=(255, 255, 255), font=get_font(26))

            proc.stdin.write(img.tobytes())
    except Exception:
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

    # Create short metadata
    short_meta_file = release_dir / "short_metadata.md"
    short_meta_content = """# YouTube Shorts 标题
```
【JLPT N3】电影《最后的里程》高光台词跟读！2.7m/s绝不停运？（WS.01） #Shorts
```

# YouTube Shorts 简介
```
【TokyoFlow 日语影视短视频跟读 • 中文解说版】
短片编号：WS.01
长视频大课：WL.01《最后的里程》影视沉浸精讲

跟着满岛光 2024 现象级悬疑电影《最后的里程》(Last Mile)，掌握 JLPT N3 核心考点：~わけにはいかない（道德与社会契约约束下的绝不能）！

完整 25 分钟长视频深度大课已同步上线，欢迎在主页观看完整精讲。
官网：https://tokyoflow.app/

#Shorts #日语学习 #最后的里程 #满岛光 #日本电影 #JLPTN3 #日语口语 #TokyoFlow
```
"""
    short_meta_file.write_text(short_meta_content, encoding="utf-8")
    print(f"  [OK] WL.01 9:16 短片生成完成: {out_short}")

# ==========================================
# 2. RENDER WM.01 CHINESE VIDEO (1080p & 9:16)
# ==========================================

def render_wm01_zh_video(release_dir: Path):
    """Renders 1080p video for WM01 Chinese."""
    out_video = release_dir / "video.mp4"
    if out_video.exists() and out_video.stat().st_size > 1000000:
        print(f"  [OK] WM.01 视频已存在: {out_video}")
        return

    print("  >> 正在渲染 WM.01 周一到周五生活大合集 中文版 1080p 视频...")
    audio_dir = release_dir / "audio"
    script_file = release_dir / "script.json"
    script_data = json.loads(script_file.read_text(encoding="utf-8"))
    
    tmp_dir = PROJECT_ROOT / "tmp" / "videogen" / "wm01_zh_render"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    width, height = 1920, 1080
    fps = 30
    clip_files = []

    for ch in script_data["screenplay"]:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            audio_path = audio_dir / f"seg_{seg_id}.mp3"
            if not audio_path.exists():
                continue

            dur = get_audio_duration(str(audio_path))
            out_clip = tmp_dir / f"clip_{seg_id}.mp4"
            total_frames = int(dur * fps) + 1

            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{width}x{height}",
                "-pix_fmt", "rgb24",
                "-r", str(fps),
                "-i", "-",
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", str(fps),
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                "-shortest",
                str(out_clip)
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f_idx in range(total_frames):
                    img = Image.new("RGB", (width, height), (15, 23, 42))
                    draw = ImageDraw.Draw(img)

                    # Top Banner
                    draw.rectangle([(0, 0), (width, 75)], fill=(10, 15, 28))
                    draw.text((60, 22), "TokyoFlow 日语实景特辑  |  WM.01 周一到周五东京生活全景大合集", fill=(255, 255, 255), font=get_font(26))
                    draw.text((width - 450, 24), f"【JLPT N5-N3】• {ch_title}", fill=(244, 114, 182), font=get_font(22))

                    # Center Card
                    draw.rounded_rectangle([(100, 150), (width - 100, height - 120)], radius=24, fill=(10, 15, 28), outline=(56, 189, 248), width=3)
                    draw.text((140, 190), f"场景 {ch_id} • {ch_title}", fill=(56, 189, 248), font=get_font(28))

                    char_name = seg.get("character", "云希")
                    draw.text((140, 250), f"讲解 / 原声：{char_name}", fill=(250, 204, 21), font=get_font(32))

                    content_text = seg.get("content", "")
                    if seg.get("lang") == "ja":
                        draw.text((140, 340), content_text, fill=(255, 255, 255), font=get_font(42))
                        draw.text((140, 440), f"假名：{seg.get('furi', '')}", fill=(244, 114, 182), font=get_font(28))
                        draw.text((140, 500), f"中文：{seg.get('meaning', '')}", fill=(226, 232, 240), font=get_font(32))
                    else:
                        lines = [content_text[i:i+38] for i in range(0, len(content_text), 38)]
                        cy = 340
                        for line in lines[:8]:
                            draw.text((140, cy), line, fill=(255, 255, 255), font=get_font(34))
                            cy += 55

                    # Bottom Bar
                    draw.rectangle([(0, height - 70), (width, height)], fill=(225, 29, 72))
                    draw.text((60, height - 50), "100% 纯正东京原声 (Nanami) + 云希全中文名师精讲  •  TokyoFlow 日语实景学院", fill=(255, 255, 255), font=get_font(22))

                    proc.stdin.write(img.tobytes())
            except Exception:
                pass
            finally:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait()

            clip_files.append(out_clip)

    concat_txt = tmp_dir / "concat_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in clip_files:
            f.write(f"file '{cf.resolve()}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt), "-c", "copy", str(out_video)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  [OK] WM.01 1080p 视频生成完成: {out_video}")

def render_wm01_zh_short(release_dir: Path):
    """Renders 9:16 Short for WM01 Chinese."""
    out_short = release_dir / "short.mp4"
    if out_short.exists() and out_short.stat().st_size > 500000:
        print(f"  [OK] WM.01 短视频已存在: {out_short}")
        return

    print("  >> 正在渲染 WM.01 中文版 9:16 跟读短片...")
    audio_path = release_dir / "audio" / "seg_1_2_quote.mp3"
    if not audio_path.exists():
        return

    dur = get_audio_duration(str(audio_path))
    width, height = 1080, 1920
    fps = 30
    total_frames = int((dur + 3.0) * fps)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(dur + 2.5),
        str(out_short)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            img = Image.new("RGB", (width, height), (15, 23, 42))
            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle([(40, 50), (width - 40, 140)], radius=16, fill=(15, 23, 42))
            draw.text((70, 75), "TokyoFlow 日语实景 • 【JLPT N5-N3】WS.01", fill=(244, 114, 182), font=get_font(28))

            draw.rounded_rectangle([(40, 180), (width - 40, 380)], radius=20, fill=(10, 15, 28), outline=(250, 204, 21), width=3)
            draw.text((70, 210), "山手线电车实景跟读", fill=(250, 204, 21), font=get_font(32))
            draw.text((70, 270), "东京日常 • 周末大合集", fill=(255, 255, 255), font=get_font(38))
            draw.text((70, 330), "电车 • 便利店 • 居酒屋 • 秋叶原 • 拉面 • 温泉", fill=(148, 163, 184), font=get_font(24))

            draw.rounded_rectangle([(40, 430), (width - 40, 1200)], radius=24, fill=(10, 15, 28), outline=(56, 189, 248), width=3)
            draw.text((70, 470), "[ 山手线站台广播 • 影子跟读 ]", fill=(56, 189, 248), font=get_font(26))
            draw.text((70, 550), "まもなく、2番線に電車がまいります。", fill=(255, 255, 255), font=get_font(38))
            draw.text((70, 630), "黄色い点字ブロックの内側までお下がりください。", fill=(254, 240, 138), font=get_font(32))
            draw.text((70, 750), "Mamonaku, nibansen ni densha ga mairimasu.", fill=(244, 114, 182), font=get_font(24))
            draw.text((70, 830), "中文：「列车即将到达2号站台，请退至盲道内侧。」", fill=(226, 232, 240), font=get_font(28))
            draw.text((70, 930), "• mairimasu: 来 (自谦敬语)", fill=(52, 211, 153), font=get_font(28))
            draw.text((70, 990), "• osagari kudasai: 请退后 (敬语祈使)", fill=(148, 163, 184), font=get_font(24))

            draw.rounded_rectangle([(40, 1260), (width - 40, 1820)], radius=20, fill=(225, 29, 72))
            draw.text((70, 1300), "观看 28分钟 完整生活大合集 (WM.01)", fill=(255, 255, 255), font=get_font(34))
            draw.text((70, 1380), "• 掌握 40+ 实用生活口语公式", fill=(254, 240, 138), font=get_font(26))
            draw.text((70, 1440), "• 深度日本文化、风俗与旅行礼仪", fill=(255, 255, 255), font=get_font(26))
            draw.text((70, 1520), "tokyoflow.app 官网下载完整讲义", fill=(255, 255, 255), font=get_font(26))

            proc.stdin.write(img.tobytes())
    except Exception:
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

    # Create short metadata
    short_meta_file = release_dir / "short_metadata.md"
    short_meta_content = """# YouTube Shorts 标题
```
【JLPT N4】听懂山手线站台广播！黄色盲道退后提示与自谦语精讲（WS.01） #Shorts
```

# YouTube Shorts 简介
```
【TokyoFlow 日语实景短视频跟读 • 中文解说版】
短片编号：WS.01
长视频大课：WM.01 周一到周五东京生活全景大合集

通过山手线原声站台广播，掌握黄色盲道提示与自谦语 mairimasu！

完整 28 分钟超长大合集已同步上线，涵盖电车、便利店、居酒屋、秋叶原、拉面、温泉钱汤等全部生活实景。
官网：https://tokyoflow.app/

#Shorts #日语学习 #山手线 #东京生活 #JLPTN4 #日语听力 #日语口语 #TokyoFlow
```
"""
    short_meta_file.write_text(short_meta_content, encoding="utf-8")
    print(f"  [OK] WM.01 9:16 短片生成完成: {out_short}")

# ==========================================
# 3. YOUTUBE UPLOAD (notifySubscribers = False)
# ==========================================

def upload_chinese_megas():
    print("\n==================================================")
    print(" 正在上传 WL.01 与 WM.01 中文版至 YouTube")
    print(" 规则：notifySubscribers = False (不通知订阅者)")
    print("==================================================")

    creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=creds)
    ledger = load_ledger()

    targets = [
        ("WL01-last-mile-masterclass-v1.0-zh", "WL01-last-mile-masterclass_zh_thumb.jpg"),
        ("WM01-weekday_survival_mega_compilation-v1.0-zh", "WM01-weekday_survival_mega_compilation_zh_thumb.jpg")
    ]

    uploaded_results = {}

    for folder_name, thumb_filename in targets:
        rel_dir = RELEASES_DIR / folder_name
        if not rel_dir.exists():
            continue

        print(f"\n--------------------------------------------------")
        print(f"处理发布包: {folder_name}")
        print(f"--------------------------------------------------")

        # 1. 16:9 Long Video
        video_mp4 = rel_dir / "video.mp4"
        thumb_jpg = rel_dir / "thumbnail.jpg"
        meta_md = rel_dir / "metadata.md"
        long_key = f"{folder_name}_video"

        if video_mp4.exists() and meta_md.exists():
            meta = extract_metadata_fields(meta_md)
            slot_time = datetime.now(EST_TZ) # Publish immediately as public or scheduled

            print(f"  >> 上传 16:9 完整大课: {meta['title']} (notifySubscribers=False)...")
            record = upload_video_asset(
                youtube, video_mp4, thumb_jpg, meta, slot_time, is_short=False, notify_subscribers=False
            )
            ledger.setdefault("published", {})[long_key] = record
            save_ledger(ledger)
            uploaded_results[long_key] = record

            # Playlist routing
            lang_pl_id = get_or_create_language_playlist(youtube, "zh", is_short=False, ledger=ledger)
            if lang_pl_id:
                add_video_to_playlist(youtube, record["video_id"], lang_pl_id)

            pl_id = resolve_playlist_id(folder_name)
            if pl_id:
                add_video_to_playlist(youtube, record["video_id"], pl_id)

        # 2. 9:16 Short
        short_mp4 = rel_dir / "short.mp4"
        short_thumb_jpg = rel_dir / "short_thumbnail.jpg"
        short_meta_md = rel_dir / "short_metadata.md"
        short_key = f"{folder_name}_short"

        if short_mp4.exists() and short_meta_md.exists():
            meta_s = extract_metadata_fields(short_meta_md)
            slot_time_s = datetime.now(EST_TZ)

            print(f"  >> 上传 9:16 跟读短片: {meta_s['title']} (notifySubscribers=False)...")
            record_s = upload_video_asset(
                youtube, short_mp4, short_thumb_jpg, meta_s, slot_time_s, is_short=True, notify_subscribers=False
            )
            ledger.setdefault("published", {})[short_key] = record_s
            save_ledger(ledger)
            uploaded_results[short_key] = record_s

            # Playlist routing
            lang_pl_short_id = get_or_create_language_playlist(youtube, "zh", is_short=True, ledger=ledger)
            if lang_pl_short_id:
                add_video_to_playlist(youtube, record_s["video_id"], lang_pl_short_id)

    print("\n==================================================")
    print(f" 全部上传完成！生成记录: {len(uploaded_results)} 个")
    print("==================================================")
    return uploaded_results

def main():
    wl_dir = RELEASES_DIR / "WL01-last-mile-masterclass-v1.0-zh"
    wm_dir = RELEASES_DIR / "WM01-weekday_survival_mega_compilation-v1.0-zh"

    # Step 1: Render videos
    render_wl01_zh_video(wl_dir)
    render_wl01_zh_short(wl_dir)
    render_wm01_zh_video(wm_dir)
    render_wm01_zh_short(wm_dir)

    # Step 2: Upload to YouTube with notifySubscribers = False
    results = upload_chinese_megas()
    print("Upload summary:", results)

if __name__ == "__main__":
    main()
