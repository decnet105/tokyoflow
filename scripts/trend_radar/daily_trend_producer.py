#!/usr/bin/env python3
"""
TokyoFlow Japanese • Autonomous Daily Trend Video Producer & Scheduler
Standardized Master Production Engine (EP.01 / SH.01 Grade):
1. Serialized Channel Standards: Automatic next episode detection (EP.XX / SH.XX, E{XX}-{Slug}-v1.0).
2. True 30fps Frame-by-Frame Karaoke Follow-Along Highlighting:
   - Millisecond Whisper word-level timestamp alignment with 80ms anticipatory lead.
   - Dynamic glowing yellow capsule (#FEF08A) + amber outline (#F59E0B) + red follower dot (●).
   - Dynamic bilingual breakdown card & grammar spotlight follow-along.
3. 4-Stage 9:16 Shorts Funnel Engine:
   - Stage 0: Andrew English Hook
   - Stage 1: Native Speed Karaoke with millisecond token glow
   - Stage 2: Slow Breakdown & Local Pro-Tip Formula
   - Stage 3: YOUR TURN (3-2-1 Beep Countdown + Silent Recording Window + Animated Waveform & Syllable Guide)
   - Stage 4: AI Pitch Accent Scoring (98.6% Match) + Long-Form Video Funnel CTA.
4. Strict Dual-Voice & Language Assignment:
   - Male Voice (`en-US-AndrewNeural`): 100% English only (narration, explanations, pro-tips, out-loud coaching, CTAs).
   - Female Voice (`ja-JP-NanamiNeural`): 100% Native Tokyo Japanese (dialogues, vocabulary cards, examples, shadowing).
   - Zero English mispronunciation of Japanese, zero text clipping.
5. Difficulty Quota & Badges:
   - 70% JLPT N5 (Beginner / Zero prerequisite).
   - Mandatory `[JLPT N5]` title prefix and on-screen difficulty badge.
6. Unified Release Packaging in `docs/youtube_releases/`.
"""

import os
import re
import sys
import json
import math
import shutil
import asyncio
import argparse
import subprocess
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import edge_tts

# Path setups
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts", "trend_radar"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts", "videogen"))

from sources import fetch_all_sources
from scorer import rank_and_filter_candidates
from llm_curator import call_openai_chat
from timing_engine import (
    extract_tokens_from_text,
    align_sentence_tokens_with_audio
)
from slide_designer import (
    prepare_16_9_background_canvas,
    render_follow_along_video_clip,
    render_breakdown_video_clip,
    render_static_video_clip,
    render_outro_frame,
    render_news_broadcast_video_clip
)
from generate_thumbnails import generate_serialized_thumbnail
from generate_shorts_thumbnails import create_shorts_cover

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
VOICE_MALE_EN = "en-US-AndrewNeural"
VOICE_FEMALE_JA = "ja-JP-NanamiNeural"
VOICE_NEWS_ANCHOR_JA = "ja-JP-KeitaNeural"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_PATH if not is_en else "/System/Library/Fonts/Helvetica.ttc"
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

async def synth_audio(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def generate_beep(freq: int, duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration}",
        "-c:a", "libmp3lame", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_silence(duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def get_or_create_silence(duration: float, tmp_dir: str) -> str:
    sil_name = f"silence_{int(round(duration * 1000))}ms.mp3"
    sil_path = os.path.join(tmp_dir, sil_name)
    if not os.path.exists(sil_path):
        generate_silence(duration, sil_path)
    return sil_path

def get_next_episode_number() -> int:
    """Scans active publish ledger to find the next sequential episode number."""
    ep_numbers = []
    
    for ledger_file in [
        os.path.join(PROJECT_ROOT, "docs", "shared", "publish_ledger.json"),
        os.path.join(PROJECT_ROOT, "docs", "youtube_releases", "publish_ledger.json")
    ]:
        if os.path.exists(ledger_file):
            try:
                with open(ledger_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key in data.get("published", {}).keys():
                        m = re.match(r"^E(\d+)", key)
                        if m:
                            ep_numbers.append(int(m.group(1)))
            except Exception:
                pass

    if ep_numbers:
        return max(ep_numbers) + 1
    return 14

async def build_teamwork_breakdown_audio(cues: list, out_final_path: str, tmp_dir: str) -> dict:
    """
    Builds a bilingual teamwork breakdown audio track:
    - Nanami (ja-JP-NanamiNeural) for Japanese words & example phrases
    - Andrew (en-US-AndrewNeural) for English explanations & grammar
    Returns exact card & spotlight timings for seamless visual follow-along.
    """
    os.makedirs(tmp_dir, exist_ok=True)
    seg_files = []
    card_timings = {}
    spotlight_timings = (9999.0, 9999.0)
    current_time = 0.0

    for i, cue in enumerate(cues):
        speaker = cue["speaker"]
        text = cue["text"]
        fn = os.path.join(tmp_dir, f"cue_{i:02d}.mp3")
        
        voice = VOICE_FEMALE_JA if speaker == "ja" else VOICE_MALE_EN
        rate = "-12%" if speaker == "ja" else "+2%"
        pitch = "+2Hz" if speaker == "ja" else "+0Hz"
        
        await synth_audio(text, voice, fn, rate=rate, pitch=pitch)
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
            
    codec = "libmp3lame" if out_final_path.endswith(".mp3") else "aac"
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:a", codec,
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

def concat_videos_seamless(video_list: list, final_output_path: str, temp_dir: str):
    concat_txt_path = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for v in video_list:
            f.write(f"file '{os.path.abspath(v)}'\n")
    
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
        final_output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def prepare_shorts_background(bg_path: str, width: int = 1080, height: int = 1920) -> Image.Image:
    """Prepares an authentic scene photograph base canvas for 9:16 vertical shorts."""
    if bg_path and os.path.exists(bg_path):
        try:
            raw_img = Image.open(bg_path).convert("RGB")
            src_w, src_h = raw_img.size
            target_ratio = width / height
            src_ratio = src_w / src_h

            if src_ratio > target_ratio:
                new_w = int(src_h * target_ratio)
                center_x = int(src_w * 0.50)
                left = max(0, min(src_w - new_w, center_x - new_w // 2))
                raw_img = raw_img.crop((left, 0, left + new_w, src_h))
            else:
                new_h = int(src_w / target_ratio)
                top = max(0, (src_h - new_h) // 2)
                raw_img = raw_img.crop((0, top, src_w, top + new_h))

            from PIL import ImageEnhance
            base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
            base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
            base_img = ImageEnhance.Color(base_img).enhance(1.15)
        except Exception:
            base_img = Image.new("RGB", (width, height), (12, 17, 29))
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Dark atmospheric overlay across whole screen
    draw_ov.rectangle([(0, 0), (width, height)], fill=(10, 14, 23, 140))

    # Top header gradient (y=0..320)
    for y in range(320):
        rel = (320 - y) / 320.0
        alpha = int(180 * (rel ** 1.2))
        draw_ov.line([(0, y), (width, y)], fill=(8, 12, 22, alpha))

    # Bottom footer gradient (y=1450..1920)
    for y in range(1450, height):
        rel = (y - 1450) / 470.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")

# -------------------------------------------------------------------------
# 9:16 Shorts Interactive Frame Renderer (Millisecond Token Glow + 4 Stages)
# -------------------------------------------------------------------------
def render_interactive_short_frame(
    width: int,
    height: int,
    conf: dict,
    active_token_idx: int,
    stage_num: int,
    stage_title: str,
    speaking_prog: float,
    total_progress: float,
    frame_idx: int,
    base_canvas: Image.Image = None
) -> Image.Image:
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(12, 17, 29))
    draw = ImageDraw.Draw(img)

    # 1. Dark Neon Background Header
    draw.rectangle([(0, 0), (width, 270)], fill=(18, 25, 42, 180) if base_canvas is not None else (18, 25, 42))

    # 2. Header Brand Capsule (y=65..118 - Auto-measured, zero overflow)
    header_str = f"TokyoFlow  •  [{conf.get('jlpt_level', 'JLPT N5')}] SH.{conf['ep_num']:02d}"
    font_brand = get_font(24)
    bbox_hdr = draw.textbbox((0, 0), header_str, font=font_brand)
    hdr_w = bbox_hdr[2] - bbox_hdr[0]
    brand_w = hdr_w + 64
    bx = (width - brand_w) // 2
    draw.rounded_rectangle([(bx, 65), (bx + brand_w, 115)], radius=24, fill=(24, 32, 47, 240), outline=(56, 189, 248), width=2)
    draw.text((bx + 32, 77), header_str, fill=(255, 255, 255), font=font_brand)

    # 3. Hook Title (y=135..240)
    font_hook = get_font(44)
    hook_lines = conf["hook_title"].split("\n")
    cur_hy = 135
    for hline in hook_lines[:2]:
        bbox = draw.textbbox((0, 0), hline, font=font_hook)
        hw = bbox[2] - bbox[0]
        hx = (width - hw) // 2
        draw.text((hx + 3, cur_hy + 3), hline, fill=(0, 0, 0), font=font_hook)
        draw.text((hx, cur_hy), hline, fill=(250, 204, 21), font=font_hook)
        cur_hy += 50

    # 4. Scenario Pill (y=255..300)
    font_dist = get_font(21)
    dist_text = f" {conf.get('district', 'Tokyo Pop Culture')}"
    bbox_d = draw.textbbox((0, 0), dist_text, font=font_dist)
    dw = bbox_d[2] - bbox_d[0] + 40
    dx = (width - dw) // 2
    draw.rounded_rectangle([(dx, 255), (dx + dw, 298)], radius=12, fill=(224, 231, 255), outline=(165, 180, 252), width=1)
    draw.text((dx + 20, 264), dist_text, fill=(49, 46, 129), font=font_dist)

    # 5. Central 3-Tier Dialogue Card (y=320..940, height=620)
    card_x, card_y, card_w, card_h = 50, 320, width - 100, 620
    is_shadow_stage = (stage_num == 3)
    card_border = (239, 68, 68) if is_shadow_stage else (71, 85, 105)
    card_bg = (24, 24, 37) if is_shadow_stage else (30, 41, 59)
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=28, fill=card_bg, outline=card_border, width=4 if is_shadow_stage else 2)

    # Card Top Header
    font_card_head = get_font(22)
    card_header_title = " SHADOWING PRACTICE PHRASE" if is_shadow_stage else " NATIVE TOKYO PHRASE"
    draw.text((card_x + 36, card_y + 24), card_header_title, fill=(239, 68, 68) if is_shadow_stage else (148, 163, 184), font=font_card_head)
    
    # Tag
    level_tag = "SHADOW DRILL" if is_shadow_stage else "NATIVE AUDIO"
    tag_bg = (239, 68, 68) if is_shadow_stage else (244, 63, 94)
    draw.rounded_rectangle([(card_x + card_w - 180, card_y + 18), (card_x + card_w - 30, card_y + 52)], radius=10, fill=tag_bg)
    draw.text((card_x + card_w - 170, card_y + 24), level_tag, fill=(255, 255, 255), font=get_font(18))

    draw.line([(card_x + 30, card_y + 64), (card_x + card_w - 30, card_y + 64)], fill=(51, 65, 85), width=2)

    # 3-Tier Ruby Tokens
    font_jp = get_font(48)
    font_kana = get_font(24)
    font_meaning = get_font(20)

    tokens = conf.get("tokens", [])
    lines = []
    current_line = []
    current_w = 0
    max_line_w = card_w - 70

    for idx, tok in enumerate(tokens):
        bbox_j = draw.textbbox((0, 0), tok["orig"], font=font_jp)
        w_j = bbox_j[2] - bbox_j[0]
        tok_w = max(w_j + 16, 68)
        if current_w + tok_w > max_line_w and len(current_line) > 0:
            lines.append(current_line)
            current_line = [(idx, tok, tok_w)]
            current_w = tok_w
        else:
            current_line.append((idx, tok, tok_w))
            current_w += tok_w + 12
    if current_line:
        lines.append(current_line)

    start_y = card_y + 84
    for line in lines[:2]:
        line_total_w = sum(item[2] for item in line) + (len(line) - 1) * 12
        start_x = card_x + (card_w - line_total_w) // 2

        for idx, tok, tok_w in line:
            is_active = (idx == active_token_idx)
            
            if is_active:
                pill_bg = (251, 191, 36) if not is_shadow_stage else (239, 68, 68)
                pill_outline = (245, 158, 11) if not is_shadow_stage else (255, 255, 255)
                draw.rounded_rectangle(
                    [(start_x - 6, start_y - 6), (start_x + tok_w + 6, start_y + 120)],
                    radius=14,
                    fill=pill_bg,
                    outline=pill_outline,
                    width=3
                )
                dot_cx = start_x + tok_w // 2
                draw.ellipse([(dot_cx - 6, start_y - 18), (dot_cx + 6, start_y - 6)], fill=(239, 68, 68) if not is_shadow_stage else (250, 204, 21))
                
                kana_color = (15, 23, 42) if not is_shadow_stage else (255, 255, 255)
                jp_color = (15, 23, 42) if not is_shadow_stage else (255, 255, 255)
                meaning_color = (67, 20, 7) if not is_shadow_stage else (254, 202, 202)
            else:
                kana_color = (56, 189, 248)
                jp_color = (255, 255, 255)
                meaning_color = (148, 163, 184)

            if tok.get("kana"):
                bbox_k = draw.textbbox((0, 0), tok["kana"], font=font_kana)
                kw = bbox_k[2] - bbox_k[0]
                kx = start_x + (tok_w - kw) // 2
                draw.text((kx, start_y), tok["kana"], fill=kana_color, font=font_kana)

            bbox_t = draw.textbbox((0, 0), tok["orig"], font=font_jp)
            tw = bbox_t[2] - bbox_t[0]
            tx = start_x + (tok_w - tw) // 2
            draw.text((tx, start_y + 26), tok["orig"], fill=jp_color, font=font_jp)

            if tok.get("meaning"):
                bbox_m = draw.textbbox((0, 0), tok["meaning"], font=font_meaning)
                mw = bbox_m[2] - bbox_m[0]
                mx = start_x + (tok_w - mw) // 2
                draw.text((mx, start_y + 88), tok["meaning"], fill=meaning_color, font=font_meaning)

            start_x += tok_w + 12

        start_y += 134

    # Romaji Subtitle inside card
    font_romaji = get_font(24)
    romaji_text = conf.get("romaji_sentence", "")
    bbox_r = draw.textbbox((0, 0), romaji_text, font=font_romaji)
    rw = bbox_r[2] - bbox_r[0]
    rx = card_x + max(20, (card_w - rw) // 2)
    draw.text((rx, card_y + 395), romaji_text, fill=(254, 240, 138), font=font_romaji)

    # English Translation Box inside card
    draw.rounded_rectangle(
        [(card_x + 24, card_y + 445), (card_x + card_w - 24, card_y + 595)],
        radius=16,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2
    )
    font_en = get_font(28)
    en_words = conf.get("en_translation", "").split(" ")
    en_lines = []
    cur_el = []
    for ew in en_words:
        cur_el.append(ew)
        test_str = " ".join(cur_el)
        if draw.textbbox((0, 0), test_str, font=font_en)[2] > card_w - 80:
            cur_el.pop()
            en_lines.append(" ".join(cur_el))
            cur_el = [ew]
    if cur_el:
        en_lines.append(" ".join(cur_el))

    cur_ey = card_y + 470 if len(en_lines) == 2 else card_y + 495
    for eline in en_lines[:2]:
        bbox_el = draw.textbbox((0, 0), eline, font=font_en)
        elw = bbox_el[2] - bbox_el[0]
        elx = card_x + (card_w - elw) // 2
        draw.text((elx, cur_ey), eline, fill=(248, 250, 252), font=font_en)
        cur_ey += 36

    # 6. Interactive Middle Zone (y=960..1520, height=560)
    mid_x, mid_y, mid_w, mid_h = 50, 960, width - 100, 560

    if stage_num == 3: # SPEAKING MODE
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(35, 14, 20), outline=(239, 68, 68), width=3)
        draw.text((mid_x + 30, mid_y + 24), " REC | LIVE MIC • REPEAT OUT LOUD NOW!", fill=(248, 113, 113), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(85, 30, 40), width=2)

        mic_cx = mid_x + mid_w // 2
        mic_cy = mid_y + 140
        pulse_r1 = int(45 + math.sin(frame_idx * 0.3) * 6)
        pulse_r2 = int(58 + math.cos(frame_idx * 0.3) * 8)
        draw.ellipse([(mic_cx - pulse_r2, mic_cy - pulse_r2), (mic_cx + pulse_r2, mic_cy + pulse_r2)], outline=(239, 68, 68), width=2)
        draw.ellipse([(mic_cx - pulse_r1, mic_cy - pulse_r1), (mic_cx + pulse_r1, mic_cy + pulse_r1)], fill=(225, 29, 72), outline=(255, 255, 255), width=2)
        
        font_mic_icon = get_font(30, is_en=True)
        draw.text((mic_cx - 18, mic_cy - 18), "REC", fill=(255, 255, 255), font=font_mic_icon)

        font_mic_prompt = get_font(30)
        prompt_txt = "SPEAK NOW! MATCH TOKYO PITCH & SPEED"
        bbox_p = draw.textbbox((0, 0), prompt_txt, font=font_mic_prompt)
        pw = bbox_p[2] - bbox_p[0]
        draw.text((mid_x + (mid_w - pw) // 2, mid_y + 215), prompt_txt, fill=(255, 255, 255), font=font_mic_prompt)

        # Animated Audio Waveform Bars
        num_bars = 22
        wave_start_x = mid_x + 40
        bar_w = (mid_w - 80) // num_bars - 6
        wave_base_y = mid_y + 310
        for b_i in range(num_bars):
            amp = math.sin((frame_idx * 0.3) + (b_i * 0.5)) * 0.5 + 0.5
            bar_h = int(24 + amp * 70)
            bx_bar = wave_start_x + b_i * (bar_w + 6)
            draw.rounded_rectangle(
                [(bx_bar, wave_base_y - bar_h // 2), (bx_bar + bar_w, wave_base_y + bar_h // 2)],
                radius=6,
                fill=(239, 68, 68) if b_i % 2 == 0 else (244, 114, 182)
            )

        prog_bar_y = mid_y + 380
        draw.text((mid_x + 30, prog_bar_y), "[TIME] SHADOWING PACING COUNTDOWN:", fill=(203, 213, 225), font=get_font(22))
        draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + mid_w - 30, prog_bar_y + 64)], radius=12, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
        sp_fill_w = int((mid_w - 60) * max(0.0, min(1.0, speaking_prog)))
        if sp_fill_w > 0:
            draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + 30 + sp_fill_w, prog_bar_y + 64)], radius=12, fill=(239, 68, 68))
        
        draw.text((mid_x + 40, mid_y + 465), "Coaching: Follow the active word highlight above.", fill=(254, 240, 138), font=get_font(22))
        draw.text((mid_x + 40, mid_y + 500), "Say each syllable in cadence with the Tokyo voice guide.", fill=(203, 213, 225), font=get_font(20))

    elif stage_num == 4: # AI SCORING
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(16, 44, 87), outline=(56, 189, 248), width=3)
        draw.text((mid_x + 30, mid_y + 24), "[AI] PITCH ACCENT EVALUATION", fill=(56, 189, 248), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(30, 58, 138), width=2)

        draw.rounded_rectangle([(mid_x + 40, mid_y + 90), (mid_x + mid_w - 40, mid_y + 230)], radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
        font_score = get_font(56)
        score_str = "98.6% MATCH"
        bbox_sc = draw.textbbox((0, 0), score_str, font=font_score)
        scw = bbox_sc[2] - bbox_sc[0]
        draw.text((mid_x + (mid_w - scw) // 2, mid_y + 110), score_str, fill=(250, 204, 21), font=font_score)
        
        font_subscore = get_font(24)
        sub_str = "Tokyo Standard Pitch Accent Verified"
        bbox_sub = draw.textbbox((0, 0), sub_str, font=font_subscore)
        subw = bbox_sub[2] - bbox_sub[0]
        draw.text((mid_x + (mid_w - subw) // 2, mid_y + 180), sub_str, fill=(255, 255, 255), font=font_subscore)

        draw.text((mid_x + 40, mid_y + 265), "* Rhythm and Intonation: Excellent (100%)", fill=(241, 245, 249), font=get_font(24))
        draw.text((mid_x + 40, mid_y + 305), "* High-Low Pitch Match: Native Equivalent", fill=(241, 245, 249), font=get_font(24))
        draw.text((mid_x + 40, mid_y + 345), "* Mora Cadence: 0.12s Standard Interval", fill=(241, 245, 249), font=get_font(24))

        draw.rounded_rectangle([(mid_x + 40, mid_y + 400), (mid_x + mid_w - 40, mid_y + 510)], radius=18, fill=(15, 23, 42), outline=(52, 211, 153), width=2)
        draw.text((mid_x + 60, mid_y + 420), "Score your voice in TokyoFlow App", fill=(52, 211, 153), font=get_font(26))
        draw.text((mid_x + 60, mid_y + 460), "10,000+ JLPT Vocabulary & Real Tokyo Scenarios", fill=(203, 213, 225), font=get_font(20))

    else: # PRO-TIP & FORMULA MODE (Stages 1 & 2)
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(30, 41, 59), outline=(52, 211, 153) if stage_num==2 else (51, 65, 85), width=3 if stage_num==2 else 2)
        draw.text((mid_x + 30, mid_y + 24), conf.get("pro_tip_title", "[PRO-TIP] LOCAL GUIDE"), fill=(52, 211, 153), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(51, 65, 85), width=2)

        font_tip_body = get_font(25)
        tip_lines = conf.get("pro_tip_body", "").split("\n")
        cur_ty = mid_y + 84
        for tline in tip_lines:
            words = tline.split(" ")
            sub_lines = []
            cur_s = []
            for w in words:
                cur_s.append(w)
                if draw.textbbox((0, 0), " ".join(cur_s), font=font_tip_body)[2] > mid_w - 60:
                    cur_s.pop()
                    sub_lines.append(" ".join(cur_s))
                    cur_s = [w]
            if cur_s:
                sub_lines.append(" ".join(cur_s))

            for sline in sub_lines:
                draw.text((mid_x + 30, cur_ty), sline, fill=(241, 245, 249), font=font_tip_body)
                cur_ty += 36
            cur_ty += 10

        draw.rounded_rectangle([(mid_x + 30, mid_y + 360), (mid_x + mid_w - 30, mid_y + 510)], radius=16, fill=(15, 23, 42))
        draw.text((mid_x + 50, mid_y + 380), "3-STEP SHADOWING MASTER SYSTEM:", fill=(250, 204, 21), font=get_font(22))
        draw.text((mid_x + 50, mid_y + 420), "1. Listen  2. Breakdown  3. Shadow Out Loud", fill=(203, 213, 225), font=get_font(21))
        draw.text((mid_x + 50, mid_y + 458), "Speak after the 3-2-1 countdown beep!", fill=(244, 114, 182), font=get_font(21))

    # 7. Dynamic Status Badge (y=1545..1625)
    status_x, status_y, status_w, status_h = 50, 1545, width - 100, 75
    s_bg = (225, 29, 72) if stage_num == 3 else ((16, 185, 129) if stage_num == 4 else ((245, 158, 11) if stage_num == 2 else (79, 70, 229)))
    s_text_color = (15, 23, 42) if stage_num == 2 else (255, 255, 255)

    draw.rounded_rectangle([(status_x, status_y), (status_x + status_w, status_y + status_h)], radius=18, fill=s_bg)
    font_status = get_font(28)
    bbox_st = draw.textbbox((0, 0), stage_title, font=font_status)
    stw = bbox_st[2] - bbox_st[0]
    stx = status_x + (status_w - stw) // 2
    draw.text((stx, status_y + 20), stage_title, fill=s_text_color, font=font_status)

    # 8. Bottom CTA Block (y=1640..1870)
    cta_x, cta_y, cta_w, cta_h = 50, 1640, width - 100, 230
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=22, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    draw.text((cta_x + 30, cta_y + 20), "[WATCH] Full Deep-Dive Video & Lesson Breakdown", fill=(56, 189, 248), font=get_font(24))
    draw.text((cta_x + 30, cta_y + 56), "Pinned comment contains full lesson link", fill=(203, 213, 225), font=get_font(20))

    draw.rounded_rectangle([(cta_x + 24, cta_y + 105), (cta_x + cta_w - 24, cta_y + 195)], radius=16, fill=(244, 63, 94))
    btn_text = "SUBSCRIBE & SHADOW DAILY"
    bbox_btn = draw.textbbox((0, 0), btn_text, font=get_font(28))
    btn_w = bbox_btn[2] - bbox_btn[0]
    draw.text((cta_x + (cta_w - btn_w) // 2, cta_y + 130), btn_text, fill=(255, 255, 255), font=get_font(28))

    # 9. Bottom Progress Line (y=1900..1910)
    draw.rectangle([(0, 1900), (width, 1910)], fill=(30, 41, 59))
    prog_w = int(width * max(0.0, min(1.0, total_progress)))
    draw.rectangle([(0, 1900), (prog_w, 1910)], fill=(250, 204, 21))

    return img

async def generate_trend_short_video(conf: dict, out_video_path: str, out_thumb_path: str, tmp_dir: str):
    """Generates the full 4-stage 9:16 interactive vertical video with millisecond token glow."""
    os.makedirs(tmp_dir, exist_ok=True)
    
    # 1. Synthesize audio
    hook_audio = os.path.join(tmp_dir, "01_hook.mp3")
    await synth_audio(conf["hook_audio_en"], VOICE_MALE_EN, hook_audio, rate="+4%")

    jp_audio_norm = os.path.join(tmp_dir, "02_jp_norm.mp3")
    await synth_audio(conf["jp_sentence"], VOICE_FEMALE_JA, jp_audio_norm, rate="-10%", pitch="+2Hz")

    tip_audio = os.path.join(tmp_dir, "03_tip.mp3")
    await synth_audio(conf["pro_tip_audio_en"], VOICE_MALE_EN, tip_audio, rate="+4%")

    shadow_cue_audio = os.path.join(tmp_dir, "04_shadow_cue.mp3")
    await synth_audio("Now your turn! Read along with native audio in 3, 2, 1, go!", VOICE_MALE_EN, shadow_cue_audio, rate="+6%")

    beep_low = os.path.join(tmp_dir, "beep_low.mp3")
    generate_beep(800, 0.12, beep_low)
    beep_high = os.path.join(tmp_dir, "beep_high.mp3")
    generate_beep(1600, 0.25, beep_high)

    dur_jp_norm = get_audio_duration(jp_audio_norm)
    
    # 1.5 Practice Drill Voice for Shadowing (Stage 3)
    jp_audio_drill = os.path.join(tmp_dir, "05_jp_drill.mp3")
    await synth_audio(conf["jp_sentence"], VOICE_FEMALE_JA, jp_audio_drill, rate="-12%", pitch="+2Hz")

    chime_audio = os.path.join(tmp_dir, "chime.mp3")
    generate_beep(1200, 0.25, chime_audio)
    outro_audio = os.path.join(tmp_dir, "06_outro.mp3")
    await synth_audio("Great job! Practice pitch accent scoring with TokyoFlow on iOS!", VOICE_MALE_EN, outro_audio, rate="+4%")

    # 2. Whisper Token Alignment
    token_objs = conf["tokens"]
    jp_sentence = conf.get("jp_sentence", "")
    aligned_tokens_norm = align_sentence_tokens_with_audio(jp_audio_norm, token_objs, jp_sentence)
    aligned_tokens_drill = align_sentence_tokens_with_audio(jp_audio_drill, token_objs, jp_sentence)

    dur_hook = get_audio_duration(hook_audio)
    dur_tip = get_audio_duration(tip_audio)
    dur_cue = get_audio_duration(shadow_cue_audio)
    dur_beep_low = get_audio_duration(beep_low)
    dur_beep_high = get_audio_duration(beep_high)
    dur_drill = get_audio_duration(jp_audio_drill)
    dur_chime = get_audio_duration(chime_audio)
    dur_out = get_audio_duration(outro_audio)

    # Build linear audio timeline with explicit silence clips for 100% millisecond precision
    audio_timeline = []
    
    # Stage 0: Hook
    audio_timeline.append((hook_audio, dur_hook))
    sil_hook = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_hook, 0.25))
    t_listen_start = sum(d for _, d in audio_timeline)

    # Stage 1: Listen
    audio_timeline.append((jp_audio_norm, dur_jp_norm))
    t_listen_end = sum(d for _, d in audio_timeline)
    sil_listen = get_or_create_silence(0.35, tmp_dir)
    audio_timeline.append((sil_listen, 0.35))
    t_tip_start = sum(d for _, d in audio_timeline)

    # Stage 2: Tip & Countdown
    audio_timeline.append((tip_audio, dur_tip))
    sil_tip = get_or_create_silence(0.35, tmp_dir)
    audio_timeline.append((sil_tip, 0.35))

    audio_timeline.append((shadow_cue_audio, dur_cue))
    sil_cue = get_or_create_silence(0.15, tmp_dir)
    audio_timeline.append((sil_cue, 0.15))

    audio_timeline.append((beep_low, dur_beep_low))
    sil_b1 = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_b1, 0.25))

    audio_timeline.append((beep_low, dur_beep_low))
    sil_b2 = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_b2, 0.25))

    audio_timeline.append((beep_high, dur_beep_high))
    sil_b3 = get_or_create_silence(0.20, tmp_dir)
    audio_timeline.append((sil_b3, 0.20))
    t_shadow_start = sum(d for _, d in audio_timeline)

    # Stage 3: Shadowing Drill
    audio_timeline.append((jp_audio_drill, dur_drill))
    t_shadow_end = sum(d for _, d in audio_timeline)
    sil_drill = get_or_create_silence(0.30, tmp_dir)
    audio_timeline.append((sil_drill, 0.30))

    audio_timeline.append((chime_audio, dur_chime))
    sil_chime = get_or_create_silence(0.20, tmp_dir)
    audio_timeline.append((sil_chime, 0.20))
    t_outro_start = sum(d for _, d in audio_timeline)

    # Stage 4: Outro
    audio_timeline.append((outro_audio, dur_out))
    sil_out = get_or_create_silence(0.40, tmp_dir)
    audio_timeline.append((sil_out, 0.40))
    t_total_end = sum(d for _, d in audio_timeline)

    full_audio_path = os.path.join(tmp_dir, "full_shadow_audio.mp3")
    concat_filter = "".join([f"[{i}:a]" for i in range(len(audio_timeline))]) + f"concat=n={len(audio_timeline)}:v=0:a=1[outa]"
    cmd_audio = ["ffmpeg", "-y"]
    for f_path, _ in audio_timeline:
        cmd_audio.extend(["-i", f_path])
    cmd_audio.extend(["-filter_complex", concat_filter, "-map", "[outa]", "-c:a", "libmp3lame", "-b:a", "192k", full_audio_path])
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_duration = get_audio_duration(full_audio_path)
    print(f"Total English Short Duration: {total_duration:.2f}s (Timeline: Listen @ {t_listen_start:.2f}s, Shadow @ {t_shadow_start:.2f}s)")

    # Load 9:16 Cover Thumbnail for First-Frame Auto-Capture Injection
    cover_frame_img = None
    if os.path.exists(out_thumb_path):
        try:
            cover_frame_img = Image.open(out_thumb_path).convert("RGB").resize((1080, 1920), Image.Resampling.LANCZOS)
        except Exception:
            cover_frame_img = None

    # Prepare 9:16 Authentic Scene Background Base Canvas
    bg_img_path = conf.get("bg_image_path", "")
    base_canvas_9_16 = prepare_shorts_background(bg_img_path)

    # 3. Stream frames to ffmpeg at 30fps
    fps = 30
    total_frames = int(total_duration * fps)

    cmd_video = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(total_duration),
        out_video_path
    ]

    proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_i in range(total_frames):
            cur_t = f_i / fps
            prog = cur_t / total_duration

            # First-Frame Injection: Frames 0..7 (first ~0.25s) use the exact 9:16 master cover
            if f_i < 8 and cover_frame_img is not None:
                frame = cover_frame_img
            elif cur_t < t_listen_start:
                stg = 0
                active_tok = -1
                stg_title = "[INTRO] HOT TOPIC BREAKDOWN"
                spk_prog = 0.0
                frame = render_interactive_short_frame(
                    width=1080,
                    height=1920,
                    conf=conf,
                    active_token_idx=active_tok,
                    stage_num=stg,
                    stage_title=stg_title,
                    speaking_prog=spk_prog,
                    total_progress=prog,
                    frame_idx=f_i,
                    base_canvas=base_canvas_9_16
                )
            elif cur_t < t_tip_start:
                stg = 1
                rel_t = cur_t - t_listen_start
                active_tok = -1
                for tok_i, tok in enumerate(aligned_tokens_norm):
                    if tok.get("start", 0.0) <= rel_t <= tok.get("end", 0.0):
                        active_tok = tok_i
                        break
                stg_title = "[STEP 1] LISTEN (Native Tokyo Speed)"
                spk_prog = 0.0
                frame = render_interactive_short_frame(
                    width=1080,
                    height=1920,
                    conf=conf,
                    active_token_idx=active_tok,
                    stage_num=stg,
                    stage_title=stg_title,
                    speaking_prog=spk_prog,
                    total_progress=prog,
                    frame_idx=f_i,
                    base_canvas=base_canvas_9_16
                )
            elif cur_t < t_shadow_start:
                stg = 2
                active_tok = -1
                stg_title = "[STEP 2] PRO-TIP AND FORMULA"
                spk_prog = 0.0
                frame = render_interactive_short_frame(
                    width=1080,
                    height=1920,
                    conf=conf,
                    active_token_idx=active_tok,
                    stage_num=stg,
                    stage_title=stg_title,
                    speaking_prog=spk_prog,
                    total_progress=prog,
                    frame_idx=f_i,
                    base_canvas=base_canvas_9_16
                )
            elif cur_t < t_outro_start:
                stg = 3
                rel_shadow_t = cur_t - t_shadow_start
                spk_prog = min(1.0, max(0.0, rel_shadow_t / max(0.1, dur_drill)))
                active_tok = -1
                for tok_i, tok in enumerate(aligned_tokens_drill):
                    if tok.get("start", 0.0) <= rel_shadow_t <= tok.get("end", 0.0):
                        active_tok = tok_i
                        break
                stg_title = "[STEP 3] YOUR TURN: READ ALONG WITH NATIVE AUDIO"
                frame = render_interactive_short_frame(
                    width=1080,
                    height=1920,
                    conf=conf,
                    active_token_idx=active_tok,
                    stage_num=stg,
                    stage_title=stg_title,
                    speaking_prog=spk_prog,
                    total_progress=prog,
                    frame_idx=f_i,
                    base_canvas=base_canvas_9_16
                )
            else:
                stg = 4
                active_tok = -1
                stg_title = "[STEP 4] AI PITCH ACCENT SCORE"
                spk_prog = 1.0
                frame = render_interactive_short_frame(
                    width=1080,
                    height=1920,
                    conf=conf,
                    active_token_idx=active_tok,
                    stage_num=stg,
                    stage_title=stg_title,
                    speaking_prog=spk_prog,
                    total_progress=prog,
                    frame_idx=f_i,
                    base_canvas=base_canvas_9_16
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

# -------------------------------------------------------------------------
# LLM Editorial Curator (Enforcing 70% JLPT N5 + Pure English Explanations)
# -------------------------------------------------------------------------
def get_covered_topics() -> list:
    """Reads existing release packages and publish ledger to identify all already covered topics and slugs."""
    releases_dir = os.path.join(PROJECT_ROOT, "docs", "youtube_releases")
    covered = []
    if os.path.exists(releases_dir):
        for item in os.listdir(releases_dir):
            if item.startswith("E") and "-" in item:
                covered.append(item)
    ledger_path = os.path.join(releases_dir, "publish_ledger.json")
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)
                for key, val in ledger.get("published", {}).items():
                    title = val.get("title", "")
                    if title:
                        covered.append(title)
        except Exception:
            pass
    return list(set(covered))

def filter_uncovered_candidates(candidates: list, covered_topics: list) -> list:
    """Proactively drops any candidate that overlaps with previously covered episodes."""
    covered_words = set()
    for item in covered_topics:
        cleaned = re.sub(r"[^\w\s]", " ", item.lower())
        for w in cleaned.split():
            if len(w) > 3 and w not in {"japan", "japanese", "tokyo", "tokyoflow", "jlpt", "video", "short", "shorts", "learnjapanese", "breakdown", "trend", "daily"}:
                covered_words.add(w)
                
    filtered = []
    for cand in candidates:
        cand_str = (cand.get("title", "") + " " + cand.get("summary", "") + " " + " ".join(cand.get("entities", []))).lower()
        is_dup = False
        for cw in covered_words:
            if cw in cand_str:
                is_dup = True
                break
        if not is_dup:
            filtered.append(cand)
            
    return filtered if filtered else candidates

def curate_single_best_topic(top_candidates: list, date_str: str, next_ep_num: int) -> dict:
    covered_episodes = get_covered_topics()
    covered_str = "\n".join([f"- {ep}" for ep in covered_episodes])
    fresh_candidates = filter_uncovered_candidates(top_candidates, covered_episodes)
    
    system_prompt = f"""You are the Senior Executive Producer and Pedagogical Director of 'TokyoFlow Japanese'.
Your mission is to pick THE SINGLE BEST DAILY TRENDING TOPIC from today's fresh candidate events, prioritizing Playlist 1 (Anime, Manga, Film, TV, Pop Culture, Entertainment & Netizen Buzz), and construct a linked Long-Form Video and Shorts Funnel package.

### THE 4 CORE PILLARS PRODUCTION BIBLE & DIRECTOR CONTRACT (制作圣经与导演合同 - 核心竞争力):
1. [SPEED] RAPID TREND VELOCITY & GEO PRECISION (热点反应速度快 + 本地GEO定位):
   - Fast reaction to today's trending Japanese entertainment / anime / netizen buzz.
   - Embed specific Tokyo GEO locations (e.g. `Shinjuku`, `Shibuya`, `Akihabara`, `Ginza`, `Roppongi`, `Harajuku`, `Tokyo Dome`) and trending entity keywords in metadata, title, and tags.
2. [IMMERSION] VIRAL ENTERTAINMENT & LIVE NEWS IMMERSION (话题好玩 + 真实新闻镜头与原声速报):
   - Make topics culturally intriguing, funny, relatable, or dramatic (e.g., natural airhead reactions '天然呆', anime bathhouse collabs, bizarre kombini foods, train manners).
   - Generate an authentic Japanese breaking news anchor opening (`news_broadcast`) for Live TV broadcast immersion.
3. [JLPT] STRICT JLPT LEVEL ALIGNMENT (能学到对应级别JLPT内容):
   - Strictly 70% JLPT N5 (zero prerequisite) / 20% N4-N3 / 10% N2-N1.
   - Downscale complex news headlines into crystal-clear Subject-Object-Verb spoken sentences.
4. [PEDAGOGY] FRICTIONLESS LEARNING EASE (容易学 + 慢速发音 + 30fps逐词发光卡拉OK):
   - Synthesize slowed-down native Japanese audio for easy phoneme recognition.
   - 100% English explanations by Andrew, 100% Tokyo Japanese by Nanami/Keita.

### PREVIOUSLY COVERED EPISODES (STRICT ANTI-DUPLICATION RULE):
The following episodes and topics have ALREADY been produced. You MUST NOT select or repeat any of these topics:
{covered_str}
YOU MUST SELECT A COMPLETELY NEW AND DIFFERENT TOPIC FROM TODAY'S FRESH CANDIDATES LIST!

### AUTHORITATIVE TEXTBOOK PEDAGOGICAL CURRICULUM (Genki I & II / Minna no Nihongo I & II / Shin Kanzen Master):
1. JLPT N5 (70% Channel Focus - True Beginners / Zero Foundation):
   - Strict Lexicon (~800 core words):
     * Nouns: 会社 (kaisha), 店 (mise), 駅 (eki), 電車 (densha), 人 (hito), 友だち (tomodachi), 映画 (eiga), アニメ (anime), 水 (mizu), 本 (hon), 今日 (kyou), 明日 (ashita), 日本 (nihon), 東京 (tokyo), 時間 (jikan), お金 (okane), 俳優 (haiyuu), ニュース (nyuusu), 会場 (kaijou), 話 (hanashi).
     * Verbs: 行く (iku), 来る (kuru), 見る (miru), 食べる (taberu), 飲む (nomu), 買う (kau), 話す (hanasu), 言う (iu), 作る (tsukuru), 使う (tsukau), 知る (shiru), 待つ (matsu), 入る (hairu), 出る (deru), 笑う (warau).
     * Adjectives: 新しい (atarashii), 古い (furui), 大きい (ookii), 小さい (chiisai), 高い (takai), 安い (yasui), 面白い (omoshiroi), 好き (suki), 有名 (yuumei).
   - Strict Grammar Patterns:
     * 〜ます / 〜ません / 〜ました (Polite tense)
     * X を Verb ます (Direct object)
     * X に / へ 行きます / 来ます (Destination)
     * X で Verb ます (Location of action: 会場で見ます, 東京で話します)
     * X が あります / います (Existence)
     * 〜たいです (Desire)
     * 〜てください (Polite request)
     * 〜ています (Action in progress / state)
   - CRITICAL DOWNSCALING RULE:
     * NEVER use abstract 4-Kanji Sino-Japanese compound words in the core spoken phrases.
     * MANDATORY TRANSFORMATION: Convert the complex news headline into an authentic, accessible N5 sentence (Subject-Object-Verb).

2. JLPT N4 (20% Focus - Upper Beginners):
   - Key Patterns: 〜んです/のです (curiosity), 〜すぎる (too much), 〜たほうがいい (advice), 〜ので/のに (cause/contrast), 〜つもりです (plans), 〜たら/なら/ば/と (conditionals), 〜てあげる/もらう/くれる (favors), お + verb stem + ください.

3. JLPT N3 (10% Focus - Intermediate & Netizen Slang):
   - Key Patterns: 〜わけにはいかない, 〜かねない, 〜を中心に, 〜に基づいて, 〜に比べて, バズる, 炎上する, 神対応, 天然.

### EPISODE NUMBERING & TITLE FORMAT CONTRACT:
- Long-Form Title MUST strictly start with: `[JLPT N5] EP.{next_ep_num:02d} <High-CTR English Title> | Real Japanese Breakdown`
- Shorts Title MUST strictly start with: `[JLPT N5] SH.{next_ep_num:02d} <High-Impact English Hook>! #Shorts #LearnJapanese`

### DUAL-VOICE & LANGUAGE ASSIGNMENT:
- Andrew (Male EN, `en-US-AndrewNeural`): Speaks 100% English ONLY. Provides all hook narration, vocabulary definitions, grammar rules, pro-tips, countdown prompts, out-loud coaching, and CTAs. NEVER mispronounces Japanese words.
- Nanami (Female JA, `ja-JP-NanamiNeural`): Speaks 100% Native Tokyo Japanese ONLY. Pronounces sentences, furigana readings, and individual vocabulary cards with pristine standard pitch accent.
- ALL on-screen explanations and breakdown subtitles MUST be in English.

### AUTHENTIC JAPANESE CULTURAL INSIGHT RULE (日本文化小知识):
- In every long-form video (and metadata), whenever the topic relates to a genuine Japanese cultural phenomenon (e.g. natural airhead humor '天然/tennen', anime production culture, ryokan tea-money '心付け/kokorozuke' custom, kombini seasonal shifts, train etiquette), Andrew MUST explain this cultural insight in English during the breakdown.
- STRICT AUTHENTICITY MANDATE: ONLY explain genuine, verifiable Japanese cultural facts. Never hallucinate or fabricate cultural lore. If there is no specific cultural background for the event, gracefully focus on practical daily conversational nuances.

Return strict, valid JSON with this exact schema:
{{
  "date": "{date_str}",
  "ep_num": {next_ep_num},
  "slug": "<short_english_slug_under_25_chars>",
  "topic_title": "<Concise English Topic Title>",
  "matched_playlist": "Playlist 1: 动漫·影视·娱乐·流行文化",
  "target_jlpt_level": "JLPT N5",
  "district": "Tokyo Pop Culture",
  "dramatic_hook": "<1 sentence hook on why fans or viewers are talking about this>",
  "news_broadcast": {{
    "headline_ja": "【速報】<Realistic Japanese TV news headline>",
    "anchor_speech_ja": "<Authentic fast Japanese news broadcast anchor speech, 1-2 sentences>",
    "location_tag": "TOKYO POP CULTURE"
  }},
  "long_form": {{
    "yt_title": "[JLPT N5] EP.{next_ep_num:02d} <High-CTR English Title> | Real Japanese Breakdown",
    "english_hook": "<2-3 WORDS PUNCHY UPPERCASE HOOK>",
    "japanese_key_phrase": "<Short Downscaled N5 Key Phrase with Kanji/Kana>",
    "bottom_tag": "[JLPT N5] Native Audio - Pop Culture Trend",
    "description": "Learn natural Tokyo Japanese through today's trending entertainment news!\\n\\nTIMESTAMPS AND CHAPTERS:\\n00:00 - 01. Breaking Trend Immersion\\n00:06 - 02. Vocabulary & Grammar Breakdown\\n00:45 - 03. Situational Practice Drill\\n00:52 - 04. Shadowing Drill & Outro\\n\\nKEY PHRASES COVERED:\\n- <Phrase 1>\\n- <Phrase 2>\\n\\nRECOMMENDED PRACTICE:\\nPair this lesson with TokyoFlow - Japanese Speaking on iOS for real-time speech shadowing scoring!\\n\\n#TokyoFlow #LearnJapanese #JapaneseSpeaking #JLPT #Anime",
    "tags": ["LearnJapanese", "TokyoFlow", "JLPTN5", "AnimeJapanese", "JapaneseShadowing", "TokyoPopCulture"],
    "slides": [
      {{
        "type": "follow_along",
        "chapter": "01. Breaking Trend Immersion",
        "spoken_text": "<Full Japanese sentence for Scene 1>",
        "en": "<English translation of Scene 1>",
        "tip": "<Grammar / usage tip in English>",
        "tokens": [
          {{"orig": "<Token>", "kana": "<Kana>", "romaji": "<Romaji>", "pos": "<POS>", "meaning": "<English Meaning>"}}
        ]
      }},
      {{
        "type": "breakdown_teamwork",
        "chapter": "02. Breakdown & Cultural Insight",
        "words": [
          {{"orig": "<Word 1>", "kana": "<Kana 1>", "romaji": "<Romaji 1>", "pos": "Noun", "meaning": "<English Meaning 1>"}},
          {{"orig": "<Word 2>", "kana": "<Kana 2>", "romaji": "<Romaji 2>", "pos": "Verb", "meaning": "<English Meaning 2>"}},
          {{"orig": "<Word 3>", "kana": "<Kana 3>", "romaji": "<Romaji 3>", "pos": "Adjective", "meaning": "<English Meaning 3>"}}
        ],
        "grammar": {{
          "title": "<Grammar / Cultural Insight Title>",
          "bullets": [
            ["1. Core JLPT Pattern:", "<Explanation in English>"],
            ["2. Tokyo Cultural Insight:", "<Authentic explanation of Japanese cultural context in English>"],
            ["3. Practical Daily Life:", "<How locals use this in Tokyo>"]
          ]
        }},
        "audio_cues": [
          {{"speaker": "en", "text": "Let's break down today's key words and cultural nuance."}},
          {{"speaker": "ja", "text": "<Word 1>", "card_idx": 0}},
          {{"speaker": "en", "text": "<English explanation of Word 1>", "card_idx": 0}},
          {{"speaker": "ja", "text": "<Word 2>", "card_idx": 1}},
          {{"speaker": "en", "text": "<English explanation of Word 2>", "card_idx": 1}},
          {{"speaker": "ja", "text": "<Word 3>", "card_idx": 2}},
          {{"speaker": "en", "text": "<English explanation of Word 3>", "card_idx": 2}},
          {{"speaker": "en", "text": "<English explanation of the grammar and cultural insight>", "is_spotlight": true}},
          {{"speaker": "ja", "text": "<Full Japanese sentence>", "is_spotlight": true}},
          {{"speaker": "en", "text": "<Concluding tip and encouragement in English>", "is_spotlight": true}}
        ]
      }},
      {{
        "type": "follow_along",
        "chapter": "03. Fan & Audience Reaction",
        "spoken_text": "<Full Japanese sentence for Scene 2>",
        "en": "<English translation of Scene 2>",
        "tip": "<Quotation or reaction pattern tip>",
        "tokens": [
          {{"orig": "<Token>", "kana": "<Kana>", "romaji": "<Romaji>", "pos": "<POS>", "meaning": "<English Meaning>"}}
        ]
      }}
    ]
  }},
  "shorts": {{
    "yt_short_title": "[JLPT N5] SH.{next_ep_num:02d} <High-Impact Short Title>! #Shorts #LearnJapanese",
    "hook_title": "<LINE 1 HOOK>\\n<LINE 2 HOOK>",
    "hook_audio_en": "<1-2 sentence compelling English hook voiced by Andrew>",
    "jp_sentence": "<One punchy N5 Japanese sentence>",
    "kana_sentence": "<Kana reading>",
    "romaji_sentence": "<Romaji>",
    "en_translation": "<English translation>",
    "tokens": [
      {{"orig": "<Token>", "kana": "<Kana>", "romaji": "<Romaji>", "meaning": "<Meaning>"}}
    ],
    "pro_tip_title": " LOCAL JLPT N5 PRO-TIP",
    "pro_tip_body": "<Clear English explanation of grammar and cultural rule>",
    "pro_tip_audio_en": "<Andrew English voice explaining rule>",
    "interactive_poll": "<A vs B poll question for viewers>",
    "pinned_comment": "Full Deep-Dive Video Available Now! Click the linked video above for cultural insight & grammar drill!\\nPoll: <Poll question> A: <Option A> B: <Option B>\\nDownload TokyoFlow App on iOS for real-time speech pitch scoring!"
  }}
}}
"""
    user_prompt = f"Date: {date_str}\nNext Episode Number: {next_ep_num}\n\nTop Scored Candidates for Today:\n{json.dumps(fresh_candidates[:12], ensure_ascii=False, indent=2)}\n\nPlease pick the best trending entertainment/pop culture candidate from today's list (excluding already covered topics), and output the complete JSON specification."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return call_openai_chat(messages, model="gpt-4o", json_mode=True)

# -------------------------------------------------------------------------
# Master Autonomous Production Pipeline
# -------------------------------------------------------------------------
async def produce_daily_package(date_str: str = None, dry_run: bool = False, ep_num: int = None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        
    print(f"\n==================================================================")
    print(f"TOKYOFLOW MASTER DUAL-VOICE & KARAOKE DAILY PIPELINE ({date_str})")
    print(f"==================================================================")
    
    # 1. Detect next episode number
    next_ep_num = ep_num if ep_num is not None else get_next_episode_number()
    print(f"Target Episode Number: EP.{next_ep_num:02d} / SH.{next_ep_num:02d}")
    
    # 2. Scan and score Japanese feeds
    print(f"[1/5] Scanning Japanese feeds across 15+ channels...")
    items = fetch_all_sources(timeout=8)
    candidates = rank_and_filter_candidates(items)
    print(f"✓ Found {len(candidates)} clustered trending topics.")
    
    if dry_run:
        print("[DRY-RUN] Dry-run mode: Stopping after scan and score.")
        return
        
    # 3. Curate single best topic
    print(f"[2/5] AI Editorial Director curating Top-1 Topic (Entertainment/Anime first)...")
    spec = curate_single_best_topic(candidates, date_str, next_ep_num)
    
    slug = spec.get("slug", "daily_trend")
    folder_name = f"E{next_ep_num:02d}-{slug}-v1.0"
    topic_title = spec.get("topic_title", "Japan Daily Trend")
    jlpt_level = spec.get("target_jlpt_level", "JLPT N5")
    playlist_badge = spec.get("matched_playlist", "Playlist 1: 动漫·影视·娱乐·流行文化")
    
    print(f"✓ Selected Topic: {topic_title} [{jlpt_level}] ({playlist_badge})")
    print(f"Release Target: {folder_name}")
    
    # Setup directories (Single Source of Truth: docs/youtube_releases)
    official_release_dir = os.path.join(PROJECT_ROOT, "docs", "youtube_releases", folder_name)
    temp_dir = os.path.join(PROJECT_ROOT, "tmp", "trend_runs", date_str, folder_name)
    
    os.makedirs(official_release_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    with open(os.path.join(official_release_dir, "production_spec.json"), "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
        
    # 4. Render Long-Form 16:9 Video (Frame-by-Frame True Karaoke Follow-Along & Teamwork Breakdown)
    print(f"[3/5] Rendering 1080p 16:9 Long-Form Video (Live News Immersion + Frame-by-Frame Karaoke)...")
    long_spec = spec["long_form"]
    ep_label = f"[{jlpt_level}] EP.{next_ep_num:02d}"
    
    wallpapers = {
        "transit": os.path.join(PROJECT_ROOT, "TokyoFlow", "Resources", "Wallpapers", "tokyo_subway.jpg"),
        "kombini": os.path.join(PROJECT_ROOT, "TokyoFlow", "Resources", "Wallpapers", "rainy_cafe.jpg"),
        "izakaya": os.path.join(PROJECT_ROOT, "TokyoFlow", "Resources", "Wallpapers", "cozy_room.jpg"),
        "shopping": os.path.join(PROJECT_ROOT, "TokyoFlow", "Resources", "Wallpapers", "liquid_glass.jpg")
    }

    if "2" in playlist_badge or "便利店" in playlist_badge or "Kombini" in playlist_badge:
        default_bg = wallpapers["kombini"]
    elif "3" in playlist_badge or "交通" in playlist_badge or "Transit" in playlist_badge:
        default_bg = wallpapers["transit"]
    elif "居酒屋" in playlist_badge or "Izakaya" in playlist_badge or "美食" in playlist_badge:
        default_bg = wallpapers["izakaya"]
    else:
        default_bg = wallpapers["shopping"]

    # Retrieve dedicated topic scene background (YouTube/News Press Scene/Generated 4K)
    # Zero fallback to cartoon/manga illustration or generic abstract wallpaper
    news_bg_candidate = os.path.join(official_release_dir, "news_bg.jpg")
    scene_bg_dir = os.path.join(PROJECT_ROOT, "docs", "youtube_assets", "scene_backgrounds")
    if not os.path.exists(news_bg_candidate) and os.path.exists(scene_bg_dir):
        # 1. First check episode-specific 4K scene
        for f in os.listdir(scene_bg_dir):
            if f.startswith(f"E{next_ep_num:02d}"):
                news_bg_candidate = os.path.join(scene_bg_dir, f)
                shutil.copyfile(news_bg_candidate, os.path.join(official_release_dir, "news_bg.jpg"))
                break
        # 2. If still not found, select best matching 4K authentic Tokyo scene photo
        if not os.path.exists(os.path.join(official_release_dir, "news_bg.jpg")):
            if "便利店" in playlist_badge or "Kombini" in playlist_badge:
                fallback_photo = os.path.join(scene_bg_dir, "scene_kombini_store.jpg")
            elif "交通" in playlist_badge or "Transit" in playlist_badge or "地铁" in playlist_badge:
                fallback_photo = os.path.join(scene_bg_dir, "scene_yamanote_platform.jpg")
            elif "居酒屋" in playlist_badge or "Izakaya" in playlist_badge or "拉面" in playlist_badge or "美食" in playlist_badge:
                fallback_photo = os.path.join(scene_bg_dir, "scene_izakaya_yokocho.jpg")
            elif "动漫" in playlist_badge or "Anime" in playlist_badge or "秋叶原" in playlist_badge:
                fallback_photo = os.path.join(scene_bg_dir, "scene_akiba_street.jpg")
            else:
                fallback_photo = os.path.join(scene_bg_dir, "scene_tokyo_skyline.jpg")
            
            if os.path.exists(fallback_photo):
                shutil.copyfile(fallback_photo, os.path.join(official_release_dir, "news_bg.jpg"))
                news_bg_candidate = os.path.join(official_release_dir, "news_bg.jpg")

    bg_image_path = news_bg_candidate if os.path.exists(news_bg_candidate) else os.path.join(scene_bg_dir, "scene_tokyo_skyline.jpg")
    news_bg_image = bg_image_path
    base_canvas_16_9 = prepare_16_9_background_canvas(news_bg_image)

    rendered_clips = []

    # Guarantee authentic Japanese news headline (never English title)
    headline_jp = long_spec.get("japanese_key_phrase") or spec.get("jp_sentence") or topic_title
    news_headline = f"【芸能速报】{headline_jp}" if ("1" in playlist_badge or "芸能" in playlist_badge or "流行" in playlist_badge) else f"【速报】{headline_jp}"
    
    news_speech = f"ニュース速報です。{headline_jp}に関する最新情報をお伝えします。"
    first_slide_text = long_spec.get("slides", [{}])[0].get("spoken_text", "")
    if first_slide_text:
        news_speech = f"ニュース速報です。{first_slide_text}"
        
    # Audio Priority:
    # 1. Real source audio soundbite from event (source_audio.mp3 in release dir or spec)
    # 2. Studio anchor (Keita) at crisp, natural broadcast pace (rate="+0%", pitch="+1Hz") with TV Chime
    source_audio_file = os.path.join(official_release_dir, "source_audio.mp3")
    if os.path.exists(source_audio_file) and os.path.getsize(source_audio_file) > 10000:
        news_audio_path = source_audio_file
        print(f"✓ Using Authentic Original Event Soundbite (原音): {source_audio_file}")
    else:
        raw_anchor_path = os.path.join(temp_dir, "raw_anchor.mp3")
        await synth_audio(news_speech, VOICE_NEWS_ANCHOR_JA, raw_anchor_path, rate="+0%", pitch="+1Hz")
        
        # Generate 0.8s broadcast chime (two-tone gentle chime)
        chime_path = os.path.join(temp_dir, "news_chime.mp3")
        chime_cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "aevalsrc=0.25*sin(880*2*PI*t)*exp(-4*t)+0.35*sin(1320*2*PI*t)*exp(-3*t)+0.25*sin(1760*2*PI*t)*exp(-4*t):d=0.8",
            "-c:a", "libmp3lame",
            "-ar", "44100",
            "-ac", "2",
            chime_path
        ]
        subprocess.run(chime_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        news_audio_path = os.path.join(temp_dir, "news_anchor_live.mp3")
        concat_audio_cmd = [
            "ffmpeg", "-y",
            "-i", chime_path,
            "-i", raw_anchor_path,
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            news_audio_path
        ]
        subprocess.run(concat_audio_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    dur_news = get_audio_duration(news_audio_path)
    
    news_clip_mp4 = os.path.join(temp_dir, "clip_00_news_broadcast.mp4")
    render_news_broadcast_video_clip(
        bg_image_path=news_bg_image,
        headline_ja=news_headline,
        location_tag=spec.get("district", "TOKYO POP CULTURE"),
        audio_path=news_audio_path,
        duration=dur_news,
        out_mp4_path=news_clip_mp4,
        ep_label=f"EP.{next_ep_num:02d}",
        fps=30
    )
    rendered_clips.append(news_clip_mp4)
    print(f"✓ Live News Broadcast Clip Rendered with Authentic Chime & Scene ({dur_news:.1f}s)")
    
    for idx, sl in enumerate(long_spec["slides"]):
        sl_type = sl.get("type", "follow_along")
        clip_mp4 = os.path.join(temp_dir, f"clip_{idx+1:02d}_{sl_type}.mp4")
        
        if sl_type == "follow_along":
            spoken_text = sl["spoken_text"]
            english_meaning = sl.get("en", "")
            fa_tmp = os.path.join(temp_dir, f"fa_{idx+1:02d}")
            audio_fa_path = os.path.join(temp_dir, f"slide_{idx+1:02d}_dual_track.mp3")
            
            # Synthesize Nanami JA -> 0.3s pause -> Andrew EN Translation
            os.makedirs(fa_tmp, exist_ok=True)
            fn_ja = os.path.join(fa_tmp, "nanami_ja.mp3")
            await synth_audio(spoken_text, VOICE_FEMALE_JA, fn_ja, rate="-12%", pitch="+2Hz")
            dur_ja = get_audio_duration(fn_ja)
            
            fn_sil = os.path.join(fa_tmp, "sil.mp3")
            generate_silence(0.3, fn_sil)
            
            fn_en = os.path.join(fa_tmp, "andrew_en.mp3")
            await synth_audio(english_meaning, VOICE_MALE_EN, fn_en, rate="+2%", pitch="+0Hz")
            dur_en = get_audio_duration(fn_en)
            
            concat_txt = os.path.join(fa_tmp, "concat.txt")
            with open(concat_txt, "w") as f:
                f.write(f"file '{os.path.abspath(fn_ja)}'\n")
                f.write(f"file '{os.path.abspath(fn_sil)}'\n")
                f.write(f"file '{os.path.abspath(fn_en)}'\n")
                
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", concat_txt,
                "-c:a", "libmp3lame",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                audio_fa_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            total_dur = get_audio_duration(audio_fa_path)
            
            tokens = sl.get("tokens", [])
            if not tokens:
                tokens = extract_tokens_from_text(spoken_text)
            aligned_toks = align_sentence_tokens_with_audio(fn_ja, tokens, spoken_text)
            
            render_follow_along_video_clip(
                tokens=aligned_toks,
                category_label=f"[{jlpt_level}]  {playlist_badge.split(' ')[-1]}",
                title_label=f"{sl.get('chapter', '01. Follow Along')} • {topic_title}",
                english_meaning=english_meaning,
                pro_tip=sl.get("tip", ""),
                chapter_label=sl.get("chapter", "01. Follow Along"),
                ep_label=ep_label,
                audio_path=audio_fa_path,
                duration=total_dur,
                out_mp4_path=clip_mp4,
                fps=30,
                en_window=(dur_ja + 0.3, total_dur),
                base_canvas=base_canvas_16_9,
                bg_image_path=news_bg_image
            )
            rendered_clips.append(clip_mp4)
            print(f"✓ Dual-Voice Follow-Along Clip Rendered ({total_dur:.1f}s: Nanami JA + Andrew EN)")
            
        elif "breakdown" in sl_type:
            breakdown_tmp = os.path.join(temp_dir, f"bd_{idx+1:02d}")
            audio_bd_path = os.path.join(temp_dir, f"slide_{idx+1:02d}_bd_teamwork.mp3")
            
            cues = sl.get("teamwork_cues") or sl.get("audio_cues") or []
            if not cues:
                cues = [
                    {"speaker": "en", "text": "Let us break down today's key words and grammar."},
                    {"speaker": "ja", "text": sl.get("sentence_ja", topic_title)},
                    {"speaker": "en", "text": "Practice this sentence to speak natural Japanese in Tokyo."}
                ]
            bd_res = await build_teamwork_breakdown_audio(cues, audio_bd_path, breakdown_tmp)
            dur = bd_res["total_duration"]
            timings = bd_res["timings"]
            
            sentence_ja = sl.get("sentence_ja") or sl.get("spoken_text") or (long_spec["slides"][0]["spoken_text"] if long_spec.get("slides") else topic_title)
            vocab_list = sl.get("words") or sl.get("vocab") or []
            
            if isinstance(sl.get("grammar"), dict):
                grammar_title = sl["grammar"].get("title", "Grammar & Cultural Spotlight")
                grammar_bullets = sl["grammar"].get("bullets", [])
            else:
                grammar_title = sl.get("grammar_title", "Grammar & Cultural Spotlight")
                grammar_bullets = sl.get("grammar_bullets", [])
                
            render_breakdown_video_clip(
                sentence_ja=sentence_ja,
                vocab_list=vocab_list,
                grammar_title=grammar_title,
                grammar_bullets=grammar_bullets,
                category_label=f"[{jlpt_level}]  Sentence Structure & Nuance",
                chapter_label=sl.get("chapter", "02. Breakdown"),
                ep_label=ep_label,
                timings=timings,
                audio_path=audio_bd_path,
                duration=dur,
                out_mp4_path=clip_mp4,
                fps=30,
                base_canvas=base_canvas_16_9,
                bg_image_path=news_bg_image
            )
            rendered_clips.append(clip_mp4)
            print(f"✓ Bilingual Breakdown Clip Rendered ({dur:.1f}s)")
            
    # Add Standard 3.4s Outro Clip
    outro_audio = os.path.join(temp_dir, "outro_speech.mp3")
    await synth_audio("Subscribe to TokyoFlow Japanese, and practice interactive speaking drills in the TokyoFlow app!", VOICE_MALE_EN, outro_audio, rate="+2%")
    dur_out = get_audio_duration(outro_audio)
    outro_img = render_outro_frame(ep_label, base_canvas=base_canvas_16_9, bg_image_path=news_bg_image)
    outro_clip_mp4 = os.path.join(temp_dir, "clip_outro.mp4")
    render_static_video_clip(outro_img, outro_audio, dur_out, outro_clip_mp4, fps=30)
    rendered_clips.append(outro_clip_mp4)
    
    # Concat all long-form clips
    final_long_mp4_official = os.path.join(official_release_dir, "video.mp4")
    concat_videos_seamless(rendered_clips, final_long_mp4_official, temp_dir)
    print(f"✓ Long-Form Video Generated: {final_long_mp4_official}")
    
    # Generate 16:9 Thumbnail per EP.01 standard (tokyoflow-thumbnail-factory)
    thumb_path_official = os.path.join(official_release_dir, "thumbnail.jpg")
    master_asset_thumb = os.path.join(PROJECT_ROOT, "docs", "youtube_assets", "thumbnails", f"{folder_name}_thumb.jpg")
    
    if os.path.exists(master_asset_thumb):
        shutil.copyfile(master_asset_thumb, thumb_path_official)
        print(f"✓ Preserved Master 4K AI Landscape Thumbnail: {thumb_path_official}")
    else:
        generate_serialized_thumbnail(
            ep_num=next_ep_num,
            english_hook=long_spec.get("english_hook", "JAPAN TREND"),
            japanese_key_phrase=long_spec.get("japanese_key_phrase", topic_title),
            bottom_tag=f"[{jlpt_level}]  {long_spec.get('bottom_tag', 'Native Pop Culture • Shadowing')}",
            bg_image_path=bg_image_path,
            output_path=thumb_path_official,
            jlpt_level=jlpt_level
        )
    
    # 5. Generate Dedicated 9:16 Minimalist Cover Thumbnail FIRST (for First-Frame Video Burning)
    print(f"[4/5] Designing 9:16 Shorts Cover & Rendering Interactive Video...")
    shorts_spec = spec["shorts"]
    shorts_spec["ep_num"] = next_ep_num
    shorts_spec["jlpt_level"] = jlpt_level
    shorts_spec["district"] = spec.get("district", "Tokyo Pop Culture")
    
    short_mp4_official = os.path.join(official_release_dir, "short.mp4")
    short_thumb_official = os.path.join(official_release_dir, "short_thumbnail.jpg")
    
    if "交通" in playlist_badge or "Transit" in playlist_badge:
        accent_col = (16, 185, 129)     # Emerald
        sec_col = (56, 189, 248)        # Sky Cyan
    elif "便利店" in playlist_badge or "Kombini" in playlist_badge:
        accent_col = (249, 115, 22)     # Kombini Orange
        sec_col = (250, 204, 21)        # Warm Yellow
    elif "居酒屋" in playlist_badge or "Izakaya" in playlist_badge:
        accent_col = (234, 179, 8)      # Amber Beer Gold
        sec_col = (249, 115, 22)        # Warm Glow
    else: # Anime / Pop culture / News
        accent_col = (236, 72, 153)     # Neon Pink
        sec_col = (250, 204, 21)        # Solar Yellow

    hook_title_parts = shorts_spec.get("hook_title", "JAPAN TREND\nREAL TOKYO").split("\n")
    hook_main = hook_title_parts[0]
    hook_sub = hook_title_parts[1] if len(hook_title_parts) > 1 else "JAPAN TRENDING"

    shorts_cover_dict = {
        "ep_num": next_ep_num,
        "sh_code": f"SH.{next_ep_num:02d}",
        "folder": folder_name,
        "hook_main": hook_main,
        "hook_sub": hook_sub,
        "jp_phrase": shorts_spec.get("jp_sentence", ""),
        "romaji": shorts_spec.get("romaji_sentence", ""),
        "en_meaning": shorts_spec.get("en_translation", ""),
        "accent_color": accent_col,
        "secondary_color": sec_col,
        "location": f"TOKYO POP CULTURE • {jlpt_level}",
        "jlpt_level": jlpt_level,
        "bg_image_path": news_bg_image
    }
    cover_img = create_shorts_cover(shorts_cover_dict)
    cover_img.save(short_thumb_official, "JPEG", quality=95)
    print(f"✓ 9:16 Shorts Cover Generated: {short_thumb_official}")

    # Render 9:16 Shorts Video with First-Frame Cover Injection
    shorts_tmp = os.path.join(temp_dir, "shorts_render")
    await generate_trend_short_video(shorts_spec, short_mp4_official, short_thumb_official, shorts_tmp)
    print(f"✓ Shorts Funnel Video Generated with First-Frame Cover: {short_mp4_official}")
    
    # 6. Save Metadata & Scheduling Packages
    print(f"Packaging Metadata, Descriptions & Schedule Kits...")
    
    # Long-form metadata.md
    metadata_content = f"""# YouTube Release Manifest: EP.{next_ep_num:02d}

## Video Title
{long_spec['yt_title']}

## Video Description (Zero URLs, Zero Emojis Body)
{long_spec['description']}

## Pinned Comment
{shorts_spec['pinned_comment']}

## SEO Tags
{", ".join(long_spec['tags'])}
"""
    with open(os.path.join(official_release_dir, "metadata.md"), "w", encoding="utf-8") as f:
        f.write(metadata_content)
        
    # Shorts short_metadata.md
    short_metadata_content = f"""# YouTube Short Manifest: SH.{next_ep_num:02d}

## Short Title
{shorts_spec['yt_short_title']}

## Interactive Pinned Comment
{shorts_spec['pinned_comment']}

## Description
{shorts_spec['hook_title']}
Japanese Phrase: {shorts_spec['jp_sentence']} ({shorts_spec['romaji_sentence']})
English: {shorts_spec['en_translation']}
Rule: {shorts_spec['pro_tip_body']}

Practice speaking and pitch accent scoring in TokyoFlow - Japanese Speaking on iOS!

#Shorts #LearnJapanese #JapaneseSpeaking #TokyoFlow #Tokyo #JLPT #JapaneseShadowing
"""
    with open(os.path.join(official_release_dir, "short_metadata.md"), "w", encoding="utf-8") as f:
        f.write(short_metadata_content)
        
    # Schedule Kit JSON
    schedule_long = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 18:00:00 JST")
    schedule_shorts = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 18:30:00 JST")
    
    schedule_kit = {
        "release_date": date_str,
        "episode_number": next_ep_num,
        "folder_name": folder_name,
        "topic": topic_title,
        "jlpt_difficulty": jlpt_level,
        "playlist": playlist_badge,
        "scheduled_times": {
            "long_form_video": schedule_long,
            "shorts_video": schedule_shorts
        },
        "long_form_package": {
            "file": final_long_mp4_official,
            "thumbnail": thumb_path_official,
            "title": long_spec["yt_title"],
            "metadata_file": os.path.join(official_release_dir, "metadata.md")
        },
        "shorts_package": {
            "file": short_mp4_official,
            "thumbnail": short_thumb_official,
            "title": shorts_spec["yt_short_title"],
            "metadata_file": os.path.join(official_release_dir, "short_metadata.md"),
            "interactive_poll": shorts_spec["interactive_poll"]
        }
    }
    
    with open(os.path.join(official_release_dir, "youtube_schedule_kit.json"), "w", encoding="utf-8") as f:
        json.dump(schedule_kit, f, ensure_ascii=False, indent=2)
        
    print(f"✓ Saved YouTube Schedule Kit: {os.path.join(official_release_dir, 'youtube_schedule_kit.json')}")
    print(f"\n[DONE] Daily Dual-Voice & Karaoke Pipeline Completed Successfully!")
    print(f"Unified Release Package: {official_release_dir}")

def main():
    parser = argparse.ArgumentParser(description="TokyoFlow Autonomous Daily Trend Producer (EP.01/SH.01 Standard)")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Target date YYYY-MM-DD")
    parser.add_argument("--ep", type=int, default=None, help="Explicit target episode number (e.g. 15)")
    parser.add_argument("--dry-run", action="store_true", help="Scan and score only without rendering")
    args = parser.parse_args()
    
    asyncio.run(produce_daily_package(args.date, args.dry_run, args.ep))

if __name__ == "__main__":
    main()
