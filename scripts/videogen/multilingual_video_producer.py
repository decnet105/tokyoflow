#!/usr/bin/env python3
"""
TokyoFlow Japanese • Multilingual Video Production Engine (多母语视频生成引擎)
================================================================================
Generates high-definition, localized YouTube/Bilibili/Shorts micro-lesson video packages
supporting any learner native language (e.g. English, Chinese, Korean, Spanish, etc.).

Key Capabilities:
1. Strict Dual-Voice Separation:
   - Japanese Target Audio: 100% Native Tokyo Japanese (ja-JP-NanamiNeural / ja-JP-KeitaNeural)
   - Explainer Audio: Native Explainer Voice (en: en-US-AndrewNeural, zh: zh-CN-YunxiNeural)
2. 3-Tier Ruby Typography & Millisecond Karaoke Highlighting (with 80ms anticipatory lead)
3. Dynamic Vocabulary Card & Grammar Spotlight Audio-Visual Synchronization
4. Localized 16:9 Master Thumbnails & 9:16 Vertical Shorts Covers
5. Complete Release Directory Packaging (video.mp4, thumbnail.jpg, metadata.md, script.json)
"""

import os
import sys
import math
import json
import shutil
import asyncio
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_config import get_locale_config, LOCALES
from timing_engine import align_sentence_tokens_with_audio

PROJECT_ROOT = Path(__file__).resolve().parents[2]
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

async def synthesize_speech(
    text: str,
    out_path: str,
    voice: str,
    rate: str = "+0%",
    pitch: str = "+0Hz"
):
    tmp_path = out_path + ".raw.mp3"
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(tmp_path)

    cmd = [
        "ffmpeg", "-y",
        "-i", tmp_path,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

async def build_teamwork_audio(cues: list, out_final_path: str, tmp_dir: str, locale_cfg: dict) -> dict:
    os.makedirs(tmp_dir, exist_ok=True)
    seg_files = []
    card_timings = {}
    spotlight_timings = (9999.0, 9999.0)
    current_time = 0.0

    for i, cue in enumerate(cues):
        speaker = cue["speaker"]
        text = cue["text"]
        fn = os.path.join(tmp_dir, f"cue_{i:02d}.mp3")

        if speaker in ("explainer", "en", "zh"):
            voice = locale_cfg["explainer_voice"]
            rate = locale_cfg["explainer_rate"]
            pitch = locale_cfg["explainer_pitch"]
        else:
            voice = "ja-JP-NanamiNeural"
            rate = "-6%"
            pitch = "+3Hz"

        await synthesize_speech(text, fn, voice, rate=rate, pitch=pitch)
        dur = get_audio_duration(fn)

        start_t = current_time
        end_t = current_time + dur

        if "card_idx" in cue:
            c_idx = cue["card_idx"]
            if c_idx not in card_timings:
                card_timings[c_idx] = (start_t, end_t)
            else:
                card_timings[c_idx] = (card_timings[c_idx][0], end_t)

        if cue.get("is_spotlight"):
            if spotlight_timings == (9999.0, 9999.0):
                spotlight_timings = (start_t, end_t)
            else:
                spotlight_timings = (spotlight_timings[0], end_t)

        seg_files.append(fn)
        current_time += dur

    list_path = os.path.join(tmp_dir, "cues.txt")
    with open(list_path, "w") as f:
        for fn in seg_files:
            f.write(f"file '{os.path.abspath(fn)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        out_final_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_dur = get_audio_duration(out_final_path)
    return {
        "total_duration": total_dur,
        "timings": {
            "active_vocab_idx": card_timings,
            "spotlight_window": spotlight_timings
        }
    }

# ==========================================
# SLIDE RENDERING ENGINES (WITH i18n)
# ==========================================
def draw_top_brand_bar(draw: ImageDraw.Draw, width: int, chapter_title: str, ep_label: str, locale_cfg: dict, jlpt_level: str = "JLPT N4"):
    # Pixel-locked top brand bar at y=0..80
    draw.rectangle([(0, 0), (width, 80)], fill=(15, 23, 42))
    font_brand = get_font(28)
    brand_text = f"{locale_cfg['brand_title']}  |  {locale_cfg['brand_subtitle']}"
    draw.text((60, 24), brand_text, fill=(255, 255, 255), font=font_brand)
    
    # 1. Standardized JLPT Level Badge Pill (Crimson #E11D48) on top right
    jlpt_clean = jlpt_level.strip()
    if not jlpt_clean.upper().startswith("JLPT"):
        jlpt_clean = f"JLPT {jlpt_clean}"
    badge_str = f"{jlpt_clean} • {ep_label}"
    
    font_badge = get_font(22, is_en=True)
    bbox_b = draw.textbbox((0, 0), badge_str, font=font_badge)
    badge_tw = bbox_b[2] - bbox_b[0]
    badge_th = bbox_b[3] - bbox_b[1]
    pill_w = max(200, badge_tw + 36)
    pill_h = 44
    pill_x = width - 60 - pill_w
    pill_y = 18
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=12, fill=(225, 29, 72))
    draw.text((pill_x + (pill_w - badge_tw) // 2, pill_y + (pill_h - badge_th) // 2 - bbox_b[1]), badge_str, fill=(255, 255, 255), font=font_badge)
    
    # 2. Chapter Title right next to JLPT pill
    font_chap = get_font(22)
    bbox_c = draw.textbbox((0, 0), chapter_title, font=font_chap)
    chap_w = bbox_c[2] - bbox_c[0]
    draw.text((pill_x - chap_w - 30, 26), chapter_title, fill=(244, 114, 182), font=font_chap)

def draw_category_pill(draw: ImageDraw.Draw, text: str, x: int = 120, y: int = 115) -> int:
    font_cat = get_font(22)
    bbox = draw.textbbox((0, 0), text, font=font_cat)
    text_w = bbox[2] - bbox[0]
    pill_w = max(260, text_w + 48)
    pill_h = 46
    draw.rounded_rectangle([(x, y), (x + pill_w, y + pill_h)], radius=12, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((x + 24, y + 10), text, fill=(79, 70, 229), font=font_cat)
    return pill_w

def render_follow_along_frame(
    tokens: list,
    category_label: str,
    title_label: str,
    meaning_text: str,
    pro_tip: str,
    current_time: float,
    chapter_label: str,
    ep_label: str,
    locale_cfg: dict,
    jlpt_level: str = "JLPT N4",
    explainer_window: tuple = (0.0, 0.0)
) -> Image.Image:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # 1. Top Ribbon with Standardized JLPT Badge
    draw_top_brand_bar(draw, width, chapter_label, ep_label, locale_cfg, jlpt_level=jlpt_level)

    # 2. Category Pill with JLPT Level Prefix & Title
    jlpt_clean = jlpt_level.strip() if jlpt_level.startswith("JLPT") else f"JLPT {jlpt_level}"
    full_cat = f"[ {jlpt_clean} ]  {category_label}"
    draw_category_pill(draw, full_cat, x=120, y=115)
    draw.text((120, 180), title_label, fill=(15, 23, 42), font=get_font(36))

    # 3. Main 3-Tier Dialogue Card
    card_x, card_y, card_w, card_h = 120, 250, width - 240, 445
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)

    font_jp = get_font(52)
    font_kana = get_font(26)
    font_romaji = get_font(28)

    token_widths = []
    for tok in tokens:
        w_jp = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        w_kana = draw.textbbox((0, 0), tok.get("kana", ""), font=font_kana)[2] if tok.get("kana") else 0
        w_ro = draw.textbbox((0, 0), tok.get("romaji", ""), font=font_romaji)[2] if tok.get("romaji") else 0
        w = max(w_jp, w_kana, w_ro) + 24
        token_widths.append(w)

    total_tokens_w = sum(token_widths)
    start_x = card_x + max(40, (card_w - total_tokens_w) // 2)
    curr_x = start_x

    y_kana = card_y + 45
    y_jp = card_y + 95
    y_romaji = card_y + 185

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        start_t = tok.get("start", 0.0)
        end_t = tok.get("end", 0.0)
        
        is_active = (start_t <= current_time <= end_t) and (end_t > start_t)
        
        if is_active:
            draw.rounded_rectangle([(curr_x + 2, y_kana - 12), (curr_x + w - 2, y_romaji + 46)], radius=16, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 26), (dot_cx + 6, y_kana - 14)], fill=(220, 38, 38))
            color_kana = (180, 83, 9)
            color_jp = (15, 23, 42)
            color_romaji = (180, 83, 9)
        else:
            color_kana = (100, 116, 139)
            color_jp = (15, 23, 42)
            color_romaji = (71, 85, 105)

        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=font_kana)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=color_kana, font=font_kana)

        jw = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=color_jp, font=font_jp)

        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=font_romaji)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=color_romaji, font=font_romaji)

        curr_x += w

    # Divider Line
    draw.line([(card_x + 50, card_y + 265), (card_x + card_w - 50, card_y + 265)], fill=(241, 245, 249), width=2)

    # Meaning Box
    is_exp_active = (explainer_window[0] <= current_time <= explainer_window[1]) and (explainer_window[1] > 0)
    font_meaning = get_font(32)
    meaning_full = f"{locale_cfg['meaning_label']}{meaning_text}"
    if is_exp_active:
        draw.rounded_rectangle([(card_x + 35, card_y + 280), (card_x + card_w - 35, card_y + 350)], radius=14, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.ellipse([(card_x + 50, card_y + 305), (card_x + 64, card_y + 319)], fill=(99, 102, 241))
        draw.text((card_x + 78, card_y + 295), meaning_full, fill=(67, 56, 202), font=font_meaning)
    else:
        draw.text((card_x + 50, card_y + 295), meaning_full, fill=(30, 41, 59), font=font_meaning)

    # Pro-Tip
    if pro_tip:
        font_tip = get_font(25)
        tip_full = f"{locale_cfg['pro_tip_label']}{pro_tip}"
        draw.text((card_x + 50, card_y + 365), tip_full, fill=(16, 185, 129), font=font_tip)

    # Bottom Shadowing Drill Banner
    draw.rounded_rectangle([(120, 735), (width - 120, 885)], radius=20, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    if is_exp_active:
        draw.text((160, 770), locale_cfg["explainer_banner_title"], fill=(67, 56, 202), font=get_font(28))
        draw.text((160, 825), locale_cfg["explainer_banner_sub"], fill=(100, 116, 139), font=get_font(22))
    else:
        draw.text((160, 770), locale_cfg["shadowing_banner_title"], fill=(51, 65, 85), font=get_font(28))
        draw.text((160, 825), locale_cfg["shadowing_banner_sub"], fill=(100, 116, 139), font=get_font(22))

    return img

def render_breakdown_frame(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    category_label: str,
    chapter_label: str,
    ep_label: str,
    locale_cfg: dict,
    jlpt_level: str = "JLPT N4",
    current_time: float = 0.0,
    timings: dict = None
) -> Image.Image:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # 1. Top Brand Ribbon with Standardized JLPT Badge
    draw_top_brand_bar(draw, width, chapter_label, ep_label, locale_cfg, jlpt_level=jlpt_level)

    # 2. Category Pill with JLPT Level
    jlpt_clean = jlpt_level.strip() if jlpt_level.startswith("JLPT") else f"JLPT {jlpt_level}"
    breakdown_cat = f"[ {jlpt_clean} ]  {locale_cfg['breakdown_category']}"
    draw_category_pill(draw, breakdown_cat, x=120, y=115)
    
    # Vocab Grid Cards
    grid_x = 120
    grid_y = 240
    num_cards = min(5, len(vocab_list))
    gap = 20
    card_w = (width - 240 - (num_cards - 1) * gap) // num_cards
    card_h = 240

    active_vocab_idx = None
    spotlight_active = False

    if timings:
        for idx, (st, et) in timings.get("active_vocab_idx", {}).items():
            if st <= current_time <= et:
                active_vocab_idx = idx
                break
        sp_start, sp_end = timings.get("spotlight_window", (9999.0, 9999.0))
        if sp_start <= current_time <= sp_end:
            spotlight_active = True

    # Sentence Bar
    sent_text = f"{locale_cfg['sentence_label']}  {sentence_ja}"
    if spotlight_active and active_vocab_idx is None:
        draw.rounded_rectangle([(110, 168), (width - 110, 222)], radius=12, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((124, 178), sent_text, fill=(67, 56, 202), font=get_font(34))
    else:
        draw.text((120, 180), sent_text, fill=(15, 23, 42), font=get_font(34))

    for i in range(num_cards):
        v = vocab_list[i]
        x = grid_x + i * (card_w + gap)
        y = grid_y
        is_active = (active_vocab_idx == i)

        if is_active:
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=18, fill=(254, 249, 195), outline=(245, 158, 11), width=3)
            draw.ellipse([(x + card_w // 2 - 7, y - 7), (x + card_w // 2 + 7, y + 7)], fill=(220, 38, 38))
            pos_fill = (254, 240, 138)
            pos_color = (180, 83, 9)
            kana_color = (180, 83, 9)
        else:
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
            pos_fill = (241, 245, 249)
            pos_color = (100, 116, 139)
            kana_color = (79, 70, 229)

        # POS Pill
        draw.rounded_rectangle([(x + 14, y + 14), (x + min(card_w - 14, 150), y + 44)], radius=8, fill=pos_fill)
        draw.text((x + 20, y + 20), v.get("pos", "词汇"), fill=pos_color, font=get_font(17))

        # Japanese Main
        draw.text((x + 14, y + 54), v.get("orig", ""), fill=(15, 23, 42), font=get_font(30))

        # Kana & Romaji
        kana_ro = f"{v.get('kana', '')} • {v.get('romaji', '')}"
        draw.text((x + 14, y + 105), kana_ro, fill=kana_color, font=get_font(19))

        # Meaning
        draw.text((x + 14, y + 145), v.get("meaning", ""), fill=(51, 65, 85), font=get_font(20))

    # Grammar Spotlight Card with JLPT Level Indicator
    spot_x = 120
    spot_y = 510
    spot_w = width - 240
    spot_h = 375

    spot_title = f"{locale_cfg['spotlight_label'].replace('【', f'【 [{jlpt_clean}] ')} {grammar_title}" if "【" in locale_cfg['spotlight_label'] else f"[{jlpt_clean}] {locale_cfg['spotlight_label']} {grammar_title}"
    if spotlight_active:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(79, 70, 229), width=4)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(224, 231, 255))
        draw.text((spot_x + 30, spot_y + 16), spot_title, fill=(67, 56, 202), font=get_font(26))
    else:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(238, 242, 255))
        draw.text((spot_x + 30, spot_y + 16), spot_title, fill=(67, 56, 202), font=get_font(26))

    b_y = spot_y + 80
    for bullet in grammar_bullets:
        if isinstance(bullet, (list, tuple)) and len(bullet) >= 2:
            title, desc = bullet[0], bullet[1]
        elif isinstance(bullet, str) and ":" in bullet:
            parts = bullet.split(":", 1)
            title, desc = parts[0].strip(), parts[1].strip()
        else:
            title, desc = locale_cfg["rule_prefix"], str(bullet)
        bullet_title_color = (220, 38, 38) if spotlight_active else (185, 28, 28)
        draw.text((spot_x + 30, b_y), title, fill=bullet_title_color, font=get_font(22))
        draw.text((spot_x + 330, b_y), desc, fill=(30, 41, 59), font=get_font(22))
        b_y += 62

    # Bottom App CTA
    draw.rounded_rectangle([(120, 915), (width - 120, 1020)], radius=18, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    draw.text((160, 945), locale_cfg["academy_cta"], fill=(51, 65, 85), font=get_font(25))

    return img

def render_outro_frame(ep_label: str, locale_cfg: dict, jlpt_level: str = "JLPT N4") -> Image.Image:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    draw_top_brand_bar(draw, width, "Outro & Practice", ep_label, locale_cfg, jlpt_level=jlpt_level)

    draw.rectangle([(160, 150), (width - 160, height - 110)], fill=(255, 255, 255), outline=(226, 232, 240), width=4)
    font_hero = get_font(50)
    draw.text((220, 205), locale_cfg["outro_hero"], fill=(220, 38, 38), font=font_hero)
    
    font_sub = get_font(32)
    draw.text((220, 290), locale_cfg["outro_sub"], fill=(30, 41, 59), font=font_sub)
    
    font_bullets = get_font(26)
    b_y = 380
    for bullet_text in locale_cfg["outro_bullets"]:
        draw.text((220, b_y), bullet_text, fill=(71, 85, 105), font=font_bullets)
        b_y += 65
    
    draw.rectangle([(220, 620), (width - 220, 825)], fill=(239, 246, 255), outline=(191, 219, 254), width=3)
    font_app = get_font(30)
    draw.text((260, 655), locale_cfg["outro_app_cta"], fill=(37, 99, 235), font=font_app)
    font_app_sub = get_font(23)
    draw.text((260, 725), locale_cfg["outro_app_sub"], fill=(100, 116, 139), font=font_app_sub)

    return img

# ==========================================
# VIDEO CLIP GENERATION HELPERS
# ==========================================
def render_follow_along_video_clip(
    tokens: list,
    category_label: str,
    title_label: str,
    meaning_text: str,
    pro_tip: str,
    chapter_label: str,
    ep_label: str,
    audio_path: str,
    duration: float,
    out_mp4_path: str,
    locale_cfg: dict,
    jlpt_level: str = "JLPT N4",
    fps: int = 30,
    explainer_window: tuple = (0.0, 0.0)
):
    total_duration = duration + 0.3
    total_frames = int(total_duration * fps)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(total_duration),
        out_mp4_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            t = f_idx / fps
            frame = render_follow_along_frame(
                tokens=tokens,
                category_label=category_label,
                title_label=title_label,
                meaning_text=meaning_text,
                pro_tip=pro_tip,
                current_time=t,
                chapter_label=chapter_label,
                ep_label=ep_label,
                locale_cfg=locale_cfg,
                jlpt_level=jlpt_level,
                explainer_window=explainer_window
            )
            proc.stdin.write(frame.tobytes())
    except (BrokenPipeError, IOError):
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

def render_breakdown_video_clip(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    category_label: str,
    chapter_label: str,
    ep_label: str,
    timings: dict,
    audio_path: str,
    duration: float,
    out_mp4_path: str,
    locale_cfg: dict,
    jlpt_level: str = "JLPT N4",
    fps: int = 30
):
    total_duration = duration + 0.3
    total_frames = int(total_duration * fps)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(total_duration),
        out_mp4_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            t = f_idx / fps
            frame = render_breakdown_frame(
                sentence_ja=sentence_ja,
                vocab_list=vocab_list,
                grammar_title=grammar_title,
                grammar_bullets=grammar_bullets,
                category_label=category_label,
                chapter_label=chapter_label,
                ep_label=ep_label,
                locale_cfg=locale_cfg,
                jlpt_level=jlpt_level,
                current_time=t,
                timings=timings
            )
            proc.stdin.write(frame.tobytes())
    except (BrokenPipeError, IOError):
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

def render_static_video_clip(
    img: Image.Image,
    audio_path: str,
    duration: float,
    out_mp4_path: str,
    fps: int = 30
):
    total_duration = duration
    total_frames = int(total_duration * fps)
    frame_bytes = img.tobytes()

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(total_duration),
        out_mp4_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for _ in range(total_frames):
            proc.stdin.write(frame_bytes)
    except (BrokenPipeError, IOError):
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

# ==========================================
# THUMBNAIL & COVER GENERATOR (WITH i18n)
# ==========================================
def generate_localized_thumbnail(
    ep_num: int,
    hook_text: str,
    sub_hook: str,
    jp_phrase: str,
    jlpt_level: str,
    bg_image_path: str,
    output_path: str,
    locale_cfg: dict,
    grammar_tag: str = "",
    translation: str = "",
    context_note: str = "",
    location_tag: str = ""
):
    width, height = 1920, 1080

    if bg_image_path and os.path.exists(bg_image_path):
        raw_img = Image.open(bg_image_path).convert("RGB")
        src_w, src_h = raw_img.size
        target_ratio = width / height
        src_ratio = src_w / src_h

        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            center_x = int(src_w * 0.60)
            left = max(0, min(src_w - new_w, center_x - new_w // 2))
            raw_img = raw_img.crop((left, 0, left + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            raw_img = raw_img.crop((0, top, src_w, top + new_h))

        base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
        base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
        base_img = ImageEnhance.Color(base_img).enhance(1.18)
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    for x in range(width):
        if x < 1200:
            rel = x / 1200.0
            alpha = int(245 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top Brand Pill
    pill_w, pill_h = 360, 60
    draw.rounded_rectangle([(60, 45), (60 + pill_w, 45 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(26, is_en=False)
    bbox_b = draw.textbbox((0, 0), locale_cfg["thumb_brand"], font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((60 + (pill_w - bw) // 2, 45 + (pill_h - bh) // 2 - bbox_b[1]), locale_cfg["thumb_brand"], fill=(225, 29, 72), font=font_brand)

    # 2. Top-Right Level & Episode Badge
    ep_str = f"EP.{ep_num:02d}"
    jlpt_badge = f"{jlpt_level} • {ep_str}"
    badge_w, badge_h = 290, 60
    badge_x = width - 60 - badge_w
    draw.rounded_rectangle([(badge_x, 45), (badge_x + badge_w, 45 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), jlpt_badge, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 45 + (badge_h - gh) // 2 - bbox_bg[1]), jlpt_badge, fill=(255, 255, 255), font=font_badge)

    # 3. Giant 3D Yellow Hook Stack
    font_hook = get_font(72, is_en=False)
    hook_lines = [h.strip() for h in hook_text.split("\n") if h.strip()]
    hook_y = 155

    for line in hook_lines:
        for dx, dy, col in [
            (8, 8, (15, 23, 42)),
            (5, 5, (69, 26, 3)),
            (0, 0, (255, 234, 0))
        ]:
            draw.text((60 + dx, hook_y + dy), line, fill=col, font=font_hook)
        hook_y += 92

    # Sub-hook Pill
    font_sub = get_font(26, is_en=False)
    sub_text = f"[ {sub_hook.upper()} ]"
    bbox_s = draw.textbbox((0, 0), sub_text, font=font_sub)
    sw, sh = bbox_s[2] - bbox_s[0], bbox_s[3] - bbox_s[1]
    draw.rounded_rectangle([(60, hook_y + 10), (60 + sw + 40, hook_y + 10 + sh + 20)], radius=10, fill=(225, 29, 72))
    draw.text((80, hook_y + 20 - bbox_s[1]), sub_text, fill=(255, 255, 255), font=font_sub)

    # 4. Center-Left Japanese Soul Phrase
    font_jp_phrase = get_font(52, is_en=False)
    jp_lines = [jp.strip() for jp in jp_phrase.split("\n") if jp.strip()]
    jp_y = hook_y + 85
    for j_line in jp_lines:
        for dx, dy in [(4, 4), (-3, 3), (3, -3), (-3, -3)]:
            draw.text((60 + dx, jp_y + dy), j_line, fill=(0, 0, 0), font=font_jp_phrase)
        draw.text((60, jp_y), j_line, fill=(255, 255, 255), font=font_jp_phrase)
        jp_y += 66

    # 5. Bottom Pedagogy Card
    card_x, card_y, card_w, card_h = 60, height - 250, 1100, 190
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=18, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    
    font_g_tag = get_font(26)
    draw.text((card_x + 28, card_y + 22), grammar_tag, fill=(255, 234, 0), font=font_g_tag)
    
    font_trans = get_font(28)
    draw.text((card_x + 28, card_y + 68), translation, fill=(255, 255, 255), font=font_trans)
    
    font_ctx = get_font(22)
    draw.text((card_x + 28, card_y + 115), f"• {context_note}", fill=(203, 213, 225), font=font_ctx)
    draw.text((card_x + 28, card_y + 148), f"• {location_tag}", fill=(148, 163, 184), font=font_ctx)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"[OK] Localized 16:9 Thumbnail saved to: {output_path}")

def generate_localized_shorts_thumbnail(
    sh_num: int,
    hook_text: str,
    sub_hook: str,
    jp_phrase: str,
    jlpt_level: str,
    bg_image_path: str,
    output_path: str,
    locale_cfg: dict,
    grammar_tag: str = "",
    translation: str = "",
    context_note: str = ""
):
    width, height = 1080, 1920
    if bg_image_path and os.path.exists(bg_image_path):
        raw_img = Image.open(bg_image_path).convert("RGB")
        src_w, src_h = raw_img.size
        target_ratio = width / height
        src_ratio = src_w / src_h

        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            left = (src_w - new_w) // 2
            raw_img = raw_img.crop((left, 0, left + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            raw_img = raw_img.crop((0, top, src_w, top + new_h))

        base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
        base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
        base_img = ImageEnhance.Color(base_img).enhance(1.18)
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Top gradient
    for y in range(400):
        alpha = int(220 * (1 - y / 400.0))
        draw_ov.line([(0, y), (width, y)], fill=(8, 12, 22, alpha))

    # Bottom gradient
    for y in range(1200, height):
        rel = (y - 1200) / 720.0
        alpha = int(250 * rel)
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top Brand Pill
    pill_w, pill_h = 320, 54
    draw.rounded_rectangle([(50, 60), (50 + pill_w, 60 + pill_h)], radius=16, fill=(255, 255, 255))
    font_brand = get_font(24)
    bbox_b = draw.textbbox((0, 0), locale_cfg["thumb_brand"], font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((50 + (pill_w - bw) // 2, 60 + (pill_h - bh) // 2 - bbox_b[1]), locale_cfg["thumb_brand"], fill=(225, 29, 72), font=font_brand)

    # Top-Right Badge
    badge_str = f"{jlpt_level} • SH.{sh_num:02d}"
    badge_w, badge_h = 280, 54
    badge_x = width - 50 - badge_w
    draw.rounded_rectangle([(badge_x, 60), (badge_x + badge_w, 60 + badge_h)], radius=16, fill=(225, 29, 72))
    font_badge = get_font(24, is_en=True)
    bbox_bg = draw.textbbox((0, 0), badge_str, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 60 + (badge_h - gh) // 2 - bbox_bg[1]), badge_str, fill=(255, 255, 255), font=font_badge)

    # Hook Stack (Top Area)
    font_hook = get_font(72)
    hook_lines = [h.strip() for h in hook_text.split("\n") if h.strip()]
    hook_y = 160
    for line in hook_lines:
        for dx, dy, col in [(6, 6, (15, 23, 42)), (0, 0, (255, 234, 0))]:
            draw.text((50 + dx, hook_y + dy), line, fill=col, font=font_hook)
        hook_y += 85

    # Bottom Pedagogy Card
    card_x, card_y, card_w, card_h = 50, height - 580, width - 100, 480
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=3)

    font_jp = get_font(44)
    draw.text((card_x + 30, card_y + 35), jp_phrase, fill=(255, 255, 255), font=font_jp)

    font_trans = get_font(30)
    draw.text((card_x + 30, card_y + 140), translation, fill=(255, 234, 0), font=font_trans)

    font_gtag = get_font(26)
    draw.text((card_x + 30, card_y + 220), grammar_tag, fill=(147, 197, 253), font=font_gtag)

    font_ctx = get_font(24)
    draw.text((card_x + 30, card_y + 280), f"• {context_note}", fill=(203, 213, 225), font=font_ctx)

    # CTA Pill
    draw.rounded_rectangle([(card_x + 30, card_y + 360), (card_x + card_w - 30, card_y + 440)], radius=16, fill=(225, 29, 72))
    font_cta = get_font(28)
    cta_text = "[ SHADOWING DRILL ]  REPEAT ALOUD"
    bbox_cta = draw.textbbox((0, 0), cta_text, font=font_cta)
    cw, ch = bbox_cta[2] - bbox_cta[0], bbox_cta[3] - bbox_cta[1]
    draw.text((card_x + (card_w - cw) // 2, card_y + 375), cta_text, fill=(255, 255, 255), font=font_cta)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"[OK] Localized 9:16 Shorts Thumbnail saved to: {output_path}")

# ==========================================
# MASTER PRODUCTION PIPELINE
# ==========================================
async def produce_multilingual_episode(script_path: str, output_dir: str, locale_code: str = "zh"):
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    locale_cfg = get_locale_config(locale_code)
    os.makedirs(output_dir, exist_ok=True)
    tmp_dir = os.path.join("tmp", "videogen", f"ep_{script_data['episode_number']:02d}_{locale_code}")
    os.makedirs(tmp_dir, exist_ok=True)

    ep_num = script_data["episode_number"]
    ep_label = f"EP.{ep_num:02d}"
    jlpt_level = script_data.get("level", "JLPT N4")
    category_label = script_data.get("category", "Tokyo Transit")

    print(f"\n>> Starting Multi-Language Production: EP.{ep_num:02d} [{locale_cfg['name']}]")
    print(f"   Target Release Folder: {output_dir}")
    print(f"   Explainer Voice: {locale_cfg['explainer_voice']} ({locale_cfg['explainer_name']})")
    print(f"   JLPT Level Standard: {jlpt_level}")

    video_segments = []

    for idx, slide in enumerate(script_data["slides"]):
        stype = slide["type"]
        chapter_label = slide.get("chapter", f"0{idx+1}")
        seg_video_path = os.path.join(tmp_dir, f"segment_{idx:02d}_{stype}.mp4")

        print(f"\n--- [Slide {idx+1}/{len(script_data['slides'])}] Type: {stype} | Chapter: {chapter_label} ---")

        if stype == "follow_along":
            spoken_text = slide["spoken_text"]
            meaning_text = slide.get("meaning", slide.get("en", ""))
            pro_tip = slide.get("tip", "")
            title_label = spoken_text

            audio_path = os.path.join(tmp_dir, f"audio_slide_{idx:02d}.mp3")
            await synthesize_speech(
                spoken_text,
                audio_path,
                voice="ja-JP-NanamiNeural",
                rate="-6%",
                pitch="+3Hz"
            )
            audio_dur = get_audio_duration(audio_path)

            raw_tokens = slide.get("tokens", [])
            aligned_tokens = align_sentence_tokens_with_audio(audio_path, raw_tokens)

            render_follow_along_video_clip(
                tokens=aligned_tokens,
                category_label=category_label,
                title_label=title_label,
                meaning_text=meaning_text,
                pro_tip=pro_tip,
                chapter_label=chapter_label,
                ep_label=ep_label,
                audio_path=audio_path,
                duration=audio_dur,
                out_mp4_path=seg_video_path,
                locale_cfg=locale_cfg,
                jlpt_level=jlpt_level,
                fps=30
            )
            video_segments.append(seg_video_path)

        elif stype == "breakdown":
            sentence_ja = slide["sentence_ja"]
            vocab_list = slide["vocab"]
            grammar_title = slide["grammar_title"]
            grammar_bullets = slide["grammar_bullets"]
            cues = slide["teamwork_cues"]

            audio_path = os.path.join(tmp_dir, f"teamwork_slide_{idx:02d}.mp3")
            teamwork_data = await build_teamwork_audio(
                cues=cues,
                out_final_path=audio_path,
                tmp_dir=os.path.join(tmp_dir, f"cues_slide_{idx:02d}"),
                locale_cfg=locale_cfg
            )

            render_breakdown_video_clip(
                sentence_ja=sentence_ja,
                vocab_list=vocab_list,
                grammar_title=grammar_title,
                grammar_bullets=grammar_bullets,
                category_label=category_label,
                chapter_label=chapter_label,
                ep_label=ep_label,
                timings=teamwork_data["timings"],
                audio_path=audio_path,
                duration=teamwork_data["total_duration"],
                out_mp4_path=seg_video_path,
                locale_cfg=locale_cfg,
                jlpt_level=jlpt_level,
                fps=30
            )
            video_segments.append(seg_video_path)

        elif stype == "outro":
            spoken_text = slide["spoken_text"]
            audio_path = os.path.join(tmp_dir, f"audio_slide_{idx:02d}_outro.mp3")
            
            # Explainer says outro in native language
            await synthesize_speech(
                spoken_text,
                audio_path,
                voice=locale_cfg["explainer_voice"],
                rate="+2%",
                pitch="+0Hz"
            )
            audio_dur = get_audio_duration(audio_path)

            outro_img = render_outro_frame(ep_label, locale_cfg, jlpt_level=jlpt_level)
            render_static_video_clip(
                img=outro_img,
                audio_path=audio_path,
                duration=audio_dur + 0.5,
                out_mp4_path=seg_video_path,
                fps=30
            )
            video_segments.append(seg_video_path)

    # 4. Concatenate Final Master Video
    print("\n--- Concatenating Master 1080p Video ---")
    final_video_path = os.path.join(output_dir, "video.mp4")
    concat_txt_path = os.path.join(tmp_dir, "concat_list.txt")
    with open(concat_txt_path, "w") as f:
        for seg in video_segments:
            f.write(f"file '{os.path.abspath(seg)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        final_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    total_dur = get_audio_duration(final_video_path)
    print(f"[OK] Master Video Rendered! Duration: {total_dur:.1f}s -> {final_video_path}")

    # 5. Generate Thumbnails & Metadata
    cover_data = script_data.get("cover", {})
    bg_img = script_data.get("bg_image", "")
    thumb_path = os.path.join(output_dir, "thumbnail.jpg")
    short_thumb_path = os.path.join(output_dir, "short_thumbnail.jpg")

    jp_full = f"{cover_data.get('jp_line1', '')}\n{cover_data.get('jp_line2', '')}".strip()
    if not jp_full:
        jp_full = cover_data.get("jp", "まもなく参ります")

    generate_localized_thumbnail(
        ep_num=ep_num,
        hook_text=cover_data.get("hook", "山手线报站秘籍"),
        sub_hook=cover_data.get("sub_hook", locale_cfg["thumb_default_sub_hook"]),
        jp_phrase=jp_full,
        jlpt_level=script_data.get("level", "JLPT N4"),
        bg_image_path=bg_img,
        output_path=thumb_path,
        locale_cfg=locale_cfg,
        grammar_tag=cover_data.get("grammar_tag", "JLPT N4 语法精讲"),
        translation=cover_data.get("translation", "「请退到黄色盲道安全线内侧。」"),
        context_note=cover_data.get("context_note", "JR 东京车站高频广播"),
        location_tag=cover_data.get("location_tag", "场景：JR 新宿站 • 山手线")
    )

    generate_localized_shorts_thumbnail(
        sh_num=ep_num,
        hook_text=cover_data.get("hook", "山手线报站秘籍"),
        sub_hook=cover_data.get("sub_hook", locale_cfg["thumb_default_sub_hook"]),
        jp_phrase=jp_full.replace("\n", " "),
        jlpt_level=script_data.get("level", "JLPT N4"),
        bg_image_path=bg_img,
        output_path=short_thumb_path,
        locale_cfg=locale_cfg,
        grammar_tag=cover_data.get("grammar_tag", "JLPT N4 语法精讲"),
        translation=cover_data.get("translation", "「请退到黄色盲道安全线内侧。」"),
        context_note=cover_data.get("context_note", "JR 东京车站高频广播")
    )

    # 6. Generate Metadata Markdown
    meta_path = os.path.join(output_dir, "metadata.md")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"# {script_data['yt_title']}\n\n")
        f.write(f"**Language Version**: {locale_cfg['name']} ({locale_cfg['code']})\n")
        f.write(f"**JLPT Level**: {script_data.get('level', 'JLPT N4')}\n")
        f.write(f"**District / Context**: {script_data.get('district', '新宿')} • {category_label}\n\n")
        f.write("## Overview\n")
        f.write(f"{script_data.get('description', 'Master authentic Tokyo Japanese with TokyoFlow.')}\n\n")
        f.write("## Interactive Practice\n")
        f.write("Download TokyoFlow - Japanese Speaking on iOS App Store for real-time speech shadowing scoring!\n")

    # Copy script.json if different
    dest_script = os.path.join(output_dir, "script.json")
    if os.path.abspath(script_path) != os.path.abspath(dest_script):
        shutil.copyfile(script_path, dest_script)

    print(f"\n[DONE] Multi-Language Episode EP.{ep_num:02d} [{locale_code}] Complete!")
    print(f"Release package ready at: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TokyoFlow Multilingual Video Producer")
    parser.add_argument("--script", type=str, default="docs/youtube_releases/E01-Yamanote_Transit-v1.0-zh/script.json", help="Path to script.json")
    parser.add_argument("--out", type=str, default="docs/youtube_releases/E01-Yamanote_Transit-v1.0-zh", help="Output directory")
    parser.add_argument("--locale", type=str, default="zh", help="Locale code (en, zh, etc.)")
    args = parser.parse_args()

    asyncio.run(produce_multilingual_episode(args.script, args.out, args.locale))
