#!/usr/bin/env python3
"""
TokyoFlow Japanese • Master English Batch Production Engine (EP.12 ~ EP.19)
===========================================================================
Produces full pedagogical video packages for EP.12 to EP.19 (Oct 8 ~ Oct 19):
1. 16:9 Long-Form Full HD Master Video (video.mp4):
   - 3-tier Ruby typography (Kana top, Kanji mid, Romaji bottom, English meaning)
   - Millisecond karaoke follow-along highlighting with 80ms anticipatory offset
   - Bilingual Teamwork: Nanami (ja-JP-NanamiNeural) & Andrew (en-US-AndrewNeural)
   - Dynamic vocabulary card & grammar spotlight audio-visual synchronization
   - Standard 3.5s Outro CTA
2. 9:16 Vertical Interactive Shadowing Short (short.mp4):
   - 4-Stage Progressive Shadowing Funnel (Hook -> Native Speed -> Slow Breakdown -> 3-2-1 Speak Now / Syllable Pacing -> AI Pitch Score)
3. 16:9 High-CTR Serialized Thumbnail (thumbnail.jpg) & 9:16 Vertical Cover (short_thumbnail.jpg)
4. Comprehensive Release Packaging (metadata.md, short_metadata.md, script.json, youtube_schedule_kit.json)
"""

import os
import sys
import json
import math
import shutil
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
ASSETS_DIR = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_config import get_locale_config
from timing_engine import align_sentence_tokens_with_audio
from multilingual_video_producer import produce_multilingual_episode
from generate_shorts_thumbnails import create_shorts_cover

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

async def synth_audio(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
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

def generate_beep(freq: int, duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration}",
        "-c:a", "libmp3lame", "-ar", "44100", "-ac", "2", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_silence(duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
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


# -------------------------------------------------------------------------
# 9:16 Shorts Interactive Frame Renderer (Zero Emoji Discipline)
# -------------------------------------------------------------------------
def render_interactive_short_frame(
    width: int,
    height: int,
    conf: dict,
    active_token_idx: int,
    stage_num: int,
    stage_title: str,
    stage_subtext: str,
    speaking_prog: float,
    total_progress: float,
    frame_idx: int
) -> Image.Image:
    img = Image.new("RGB", (width, height), color=(12, 17, 29))
    draw = ImageDraw.Draw(img)

    # 1. Dark Header Band
    draw.rectangle([(0, 0), (width, 270)], fill=(18, 25, 42))

    # 2. Header Brand Capsule
    header_str = f"TokyoFlow Japanese  •  [{conf.get('jlpt_level', 'JLPT N5')}] SH.{conf['ep_num']:02d}"
    font_brand = get_font(24, is_en=True)
    bbox_hdr = draw.textbbox((0, 0), header_str, font=font_brand)
    hdr_w = bbox_hdr[2] - bbox_hdr[0]
    brand_w = hdr_w + 64
    bx = (width - brand_w) // 2
    draw.rounded_rectangle([(bx, 65), (bx + brand_w, 115)], radius=24, fill=(24, 32, 47), outline=(56, 189, 248), width=2)
    draw.text((bx + 32, 77), header_str, fill=(255, 255, 255), font=font_brand)

    # 3. Hook Title
    font_hook = get_font(44, is_en=True)
    hook_lines = conf["hook_title"].split("\n")
    cur_hy = 135
    for hline in hook_lines[:2]:
        bbox = draw.textbbox((0, 0), hline, font=font_hook)
        hw = bbox[2] - bbox[0]
        hx = (width - hw) // 2
        draw.text((hx + 3, cur_hy + 3), hline, fill=(0, 0, 0), font=font_hook)
        draw.text((hx, cur_hy), hline, fill=(250, 204, 21), font=font_hook)
        cur_hy += 50

    # 4. Scenario Pill
    font_dist = get_font(21, is_en=True)
    dist_str = f"LOCATION: {conf.get('district', 'Tokyo')}  |  {conf.get('category', 'Daily Scenario')}"
    bbox_d = draw.textbbox((0, 0), dist_str, font=font_dist)
    dw = bbox_d[2] - bbox_d[0]
    draw.rounded_rectangle([((width - dw) // 2 - 20, 255), ((width + dw) // 2 + 20, 295)], radius=12, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text(((width - dw) // 2, 264), dist_str, fill=(203, 213, 225), font=font_dist)

    # 5. Main Japanese Learning HUD Card
    card_x, card_y, card_w, card_h = 48, 320, width - 96, 750
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=28, fill=(15, 23, 42), outline=(56, 189, 248), width=3)

    # Stage Badge Ribbon
    stage_colors = {
        0: ((79, 70, 229), (224, 231, 255)),
        1: ((14, 165, 233), (255, 255, 255)),
        2: ((234, 88, 12), (255, 255, 255)),
        3: ((225, 29, 72), (255, 255, 255)),
        4: ((16, 185, 129), (255, 255, 255))
    }
    bg_col, txt_col = stage_colors.get(stage_num, ((79, 70, 229), (255, 255, 255)))
    draw.rounded_rectangle([(card_x + 24, card_y + 24), (card_x + card_w - 24, card_y + 88)], radius=16, fill=bg_col)
    font_stg = get_font(26, is_en=True)
    draw.text((card_x + 44, card_y + 40), stage_title, fill=txt_col, font=font_stg)

    # 3-Tier Japanese Token Line
    font_jp = get_font(48)
    font_kana = get_font(24)
    font_romaji = get_font(22, is_en=True)

    tokens = conf.get("tokens", [])
    token_widths = []
    for tok in tokens:
        w_jp = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        w_ka = draw.textbbox((0, 0), tok.get("kana", ""), font=font_kana)[2] if tok.get("kana") else 0
        w_ro = draw.textbbox((0, 0), tok.get("romaji", ""), font=font_romaji)[2] if tok.get("romaji") else 0
        w = max(w_jp, w_ka, w_ro) + 20
        token_widths.append(w)

    total_tokens_w = sum(token_widths)
    start_tx = card_x + max(20, (card_w - total_tokens_w) // 2)
    curr_tx = start_tx

    y_ka = card_y + 115
    y_jp = card_y + 155
    y_ro = card_y + 235

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        is_active = (i == active_token_idx)

        if is_active:
            draw.rounded_rectangle([(curr_tx + 2, y_ka - 8), (curr_tx + w - 2, y_ro + 36)], radius=14, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            # Red follower dot
            dot_x = curr_tx + w // 2
            draw.ellipse([(dot_x - 6, y_ka - 22), (dot_x + 6, y_ka - 10)], fill=(239, 68, 68))
            col_jp = (15, 23, 42)
            col_ka = (71, 85, 105)
            col_ro = (30, 41, 59)
        else:
            col_jp = (255, 255, 255)
            col_ka = (244, 114, 182)
            col_ro = (148, 163, 184)

        if tok.get("kana"):
            draw.text((curr_tx + 10, y_ka), tok["kana"], fill=col_ka, font=font_kana)
        draw.text((curr_tx + 10, y_jp), tok["orig"], fill=col_jp, font=font_jp)
        if tok.get("romaji"):
            draw.text((curr_tx + 10, y_ro), tok["romaji"], fill=col_ro, font=font_romaji)

        curr_tx += w

    # Meaning Box
    draw.rounded_rectangle([(card_x + 24, card_y + 295), (card_x + card_w - 24, card_y + 400)], radius=16, fill=(30, 41, 59))
    font_lbl = get_font(20, is_en=True)
    draw.text((card_x + 44, card_y + 308), "MEANING", fill=(148, 163, 184), font=font_lbl)
    font_mean = get_font(26, is_en=True)
    draw.text((card_x + 44, card_y + 342), conf["en_translation"], fill=(255, 255, 255), font=font_mean)

    # Pro-Tip / Cultural Formula Box
    draw.rounded_rectangle([(card_x + 24, card_y + 420), (card_x + card_w - 24, card_y + 575)], radius=16, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((card_x + 44, card_y + 434), f"[ FORMULA & PRO-TIP ]  {conf.get('pro_tip_title', 'Tokyo Local Hack')}", fill=(250, 204, 21), font=font_lbl)
    font_tip = get_font(23, is_en=True)
    tip_body = conf.get("pro_tip_body", "")
    # Word wrap tip
    words = tip_body.split(" ")
    lines = []
    cur_line = ""
    for wrd in words:
        test_line = f"{cur_line} {wrd}".strip()
        if draw.textbbox((0, 0), test_line, font=font_tip)[2] < (card_w - 90):
            cur_line = test_line
        else:
            lines.append(cur_line)
            cur_line = wrd
    if cur_line:
        lines.append(cur_line)

    cur_ty = card_y + 472
    for l in lines[:3]:
        draw.text((card_x + 44, cur_ty), l, fill=(226, 232, 240), font=font_tip)
        cur_ty += 32

    # Stage 3 Shadowing Waveform & Speaking Guide
    if stage_num == 3:
        draw.rounded_rectangle([(card_x + 24, card_y + 595), (card_x + card_w - 24, card_y + 720)], radius=16, fill=(69, 10, 10), outline=(225, 29, 72), width=2)
        font_mic = get_font(24, is_en=True)
        draw.text((card_x + 44, card_y + 610), "[ LIVE MIC ACTIVE ]  SPEAK OUT LOUD NOW", fill=(254, 205, 211), font=font_mic)
        
        # Animated Waveform Bars
        num_bars = 24
        bar_w = (card_w - 120) // num_bars
        for b_i in range(num_bars):
            phase = (frame_idx * 0.25) + b_i * 0.6
            bar_h = int(12 + 28 * abs(math.sin(phase)))
            bx = card_x + 50 + b_i * (bar_w + 3)
            by = card_y + 695 - bar_h
            draw.rounded_rectangle([(bx, by), (bx + bar_w, card_y + 695)], radius=4, fill=(244, 63, 94))
    elif stage_num == 4:
        draw.rounded_rectangle([(card_x + 24, card_y + 595), (card_x + card_w - 24, card_y + 720)], radius=16, fill=(6, 78, 59), outline=(16, 185, 129), width=2)
        font_score = get_font(28, is_en=True)
        draw.text((card_x + 44, card_y + 615), "[ AI PITCH MATCH: 98.6% ]  EXCELLENT PITCH", fill=(167, 243, 208), font=font_score)
        font_score_sub = get_font(22, is_en=True)
        draw.text((card_x + 44, card_y + 665), "Accurate Tokyo Pitch Accent & Intonation Curve", fill=(255, 255, 255), font=font_score_sub)
    else:
        # Standard Info
        draw.rounded_rectangle([(card_x + 24, card_y + 595), (card_x + card_w - 24, card_y + 720)], radius=16, fill=(24, 32, 47))
        font_info = get_font(22, is_en=True)
        draw.text((card_x + 44, card_y + 620), "[ NATIVE AUDIO ]  ja-JP-NanamiNeural (Tokyo Standard)", fill=(147, 197, 253), font=font_info)
        draw.text((card_x + 44, card_y + 660), "[ EXPLAINER ]  en-US-AndrewNeural (100% Pure English)", fill=(203, 213, 225), font=font_info)

    # 6. Bottom App Conversion Banner
    banner_y = height - 260
    draw.rounded_rectangle([(48, banner_y), (width - 48, banner_y + 190)], radius=24, fill=(225, 29, 72))
    font_cta_h = get_font(32, is_en=True)
    draw.text((80, banner_y + 30), "TokyoFlow - Japanese Speaking", fill=(255, 255, 255), font=font_cta_h)
    font_cta_sub = get_font(22, is_en=True)
    draw.text((80, banner_y + 80), "• Real-Life Tokyo Dialogue Immersion", fill=(255, 241, 242), font=font_cta_sub)
    draw.text((80, banner_y + 115), "• 14,000+ Native VoiceBank & Pitch Accent Scoring", fill=(255, 241, 242), font=font_cta_sub)
    draw.text((80, banner_y + 148), "• Free on iOS App Store", fill=(254, 240, 138), font=font_cta_sub)

    # 7. Progress Bar at Very Bottom
    draw.rectangle([(0, height - 12), (width, height)], fill=(15, 23, 42))
    prog_w = int(width * min(1.0, max(0.0, total_progress)))
    draw.rectangle([(0, height - 12), (prog_w, height)], fill=(225, 29, 72))

    return img

# -------------------------------------------------------------------------
# Short Video Audio & Frame Pipeline
# -------------------------------------------------------------------------
async def generate_single_short_video(conf: dict, out_video_path: str, tmp_dir: str, short_thumb_path: str = None):
    os.makedirs(tmp_dir, exist_ok=True)
    frames_dir = os.path.join(tmp_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    cover_frame_img = None
    if short_thumb_path and os.path.exists(short_thumb_path):
        try:
            cover_frame_img = Image.open(short_thumb_path).convert("RGB").resize((1080, 1920), Image.Resampling.LANCZOS)
        except Exception:
            cover_frame_img = None

    # 1. Synthesize Audio Clips
    f_hook = os.path.join(tmp_dir, "01_hook.mp3")
    f_native = os.path.join(tmp_dir, "02_native.mp3")
    f_tip = os.path.join(tmp_dir, "03_tip.mp3")
    f_cue = os.path.join(tmp_dir, "04_cue.mp3")
    f_beep_low = os.path.join(tmp_dir, "beep_low.mp3")
    f_beep_high = os.path.join(tmp_dir, "beep_high.mp3")
    f_drill = os.path.join(tmp_dir, "05_jp_drill.mp3")
    f_chime = os.path.join(tmp_dir, "chime.mp3")
    f_outro = os.path.join(tmp_dir, "06_outro.mp3")

    await synth_audio(conf["hook_audio_en"], "en-US-AndrewNeural", f_hook, rate="+2%")
    await synth_audio(conf["jp_sentence"], "ja-JP-NanamiNeural", f_native, rate="-6%", pitch="+3Hz")
    await synth_audio(conf["pro_tip_audio_en"], "en-US-AndrewNeural", f_tip, rate="+2%")
    await synth_audio("Now your turn! Read along with native audio in 3, 2, 1, go!", "en-US-AndrewNeural", f_cue, rate="+6%")

    generate_beep(800, 0.12, f_beep_low)
    generate_beep(1600, 0.25, f_beep_high)

    # Nanami Native Practice Drill Voice for Shadowing (Stage 3)
    await synth_audio(conf["jp_sentence"], "ja-JP-NanamiNeural", f_drill, rate="-10%", pitch="+2Hz")

    generate_beep(1200, 0.25, f_chime)
    outro_speech = "Practice interactive speech shadowing with instant pitch accent scoring on TokyoFlow for iOS!"
    await synth_audio(outro_speech, "en-US-AndrewNeural", f_outro, rate="+2%")

    # Audio Alignment for Stage 1 & Stage 3
    jp_sentence = conf.get("jp_sentence", "")
    aligned_tokens_norm = align_sentence_tokens_with_audio(f_native, conf["tokens"], jp_sentence)
    aligned_tokens_drill = align_sentence_tokens_with_audio(f_drill, conf["tokens"], jp_sentence)

    dur_hook = get_audio_duration(f_hook)
    dur_native = get_audio_duration(f_native)
    dur_tip = get_audio_duration(f_tip)
    dur_cue = get_audio_duration(f_cue)
    dur_beep_low = get_audio_duration(f_beep_low)
    dur_beep_high = get_audio_duration(f_beep_high)
    dur_drill = get_audio_duration(f_drill)
    dur_chime = get_audio_duration(f_chime)
    dur_outro = get_audio_duration(f_outro)

    # Build linear audio timeline with explicit silence clips to ensure 100% audio-visual lock
    audio_timeline = []
    
    # Stage 0: Hook
    audio_timeline.append((f_hook, dur_hook))
    sil_hook = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_hook, 0.25))
    t_listen_start = sum(d for _, d in audio_timeline)

    # Stage 1: Listen
    audio_timeline.append((f_native, dur_native))
    t_listen_end = sum(d for _, d in audio_timeline)
    sil_listen = get_or_create_silence(0.35, tmp_dir)
    audio_timeline.append((sil_listen, 0.35))
    t_tip_start = sum(d for _, d in audio_timeline)

    # Stage 2: Tip & Countdown
    audio_timeline.append((f_tip, dur_tip))
    sil_tip = get_or_create_silence(0.35, tmp_dir)
    audio_timeline.append((sil_tip, 0.35))

    audio_timeline.append((f_cue, dur_cue))
    sil_cue = get_or_create_silence(0.15, tmp_dir)
    audio_timeline.append((sil_cue, 0.15))

    audio_timeline.append((f_beep_low, dur_beep_low))
    sil_b1 = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_b1, 0.25))

    audio_timeline.append((f_beep_low, dur_beep_low))
    sil_b2 = get_or_create_silence(0.25, tmp_dir)
    audio_timeline.append((sil_b2, 0.25))

    audio_timeline.append((f_beep_high, dur_beep_high))
    sil_b3 = get_or_create_silence(0.20, tmp_dir)
    audio_timeline.append((sil_b3, 0.20))
    t_shadow_start = sum(d for _, d in audio_timeline)

    # Stage 3: Shadowing Drill (Direct Native Japanese Audio)
    audio_timeline.append((f_drill, dur_drill))
    t_shadow_end = sum(d for _, d in audio_timeline)
    sil_drill = get_or_create_silence(0.30, tmp_dir)
    audio_timeline.append((sil_drill, 0.30))

    audio_timeline.append((f_chime, dur_chime))
    sil_chime = get_or_create_silence(0.20, tmp_dir)
    audio_timeline.append((sil_chime, 0.20))
    t_outro_start = sum(d for _, d in audio_timeline)

    # Stage 4: Outro
    audio_timeline.append((f_outro, dur_outro))
    sil_out = get_or_create_silence(0.40, tmp_dir)
    audio_timeline.append((sil_out, 0.40))

    full_audio_path = os.path.join(tmp_dir, "full_short_audio.mp3")
    concat_filter = "".join([f"[{i}:a]" for i in range(len(audio_timeline))]) + f"concat=n={len(audio_timeline)}:v=0:a=1[outa]"
    cmd_cat = ["ffmpeg", "-y"]
    for f_path, _ in audio_timeline:
        cmd_cat.extend(["-i", f_path])
    cmd_cat.extend(["-filter_complex", concat_filter, "-map", "[outa]", "-c:a", "libmp3lame", "-b:a", "192k", full_audio_path])
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    total_duration = get_audio_duration(full_audio_path)

    fps = 30
    total_frames = int(total_duration * fps)

    for frame_idx in range(total_frames):
        cur_t = frame_idx / fps
        prog = cur_t / total_duration

        # First-Frame Injection: Frames 0..7 (first ~0.26s) use the exact 9:16 master cover
        if frame_idx < 8 and cover_frame_img is not None:
            frame_img = cover_frame_img
        elif cur_t < t_listen_start:
            stg = 0
            active_tok = -1
            stg_title = "[ INTRO ]  SURVIVAL JAPANESE"
            stg_sub = "Scenario Context"
            spk_prog = 0.0
            frame_img = render_interactive_short_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx
            )
        elif cur_t < t_tip_start:
            stg = 1
            rel_t = cur_t - t_listen_start
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens_norm):
                st = tok.get("start", 0.0) - 0.06
                et = tok.get("end", 0.0)
                if st <= rel_t <= et:
                    active_tok = tok_i
                    break
            stg_title = "[ STEP 1 ]  LISTEN (Native Tokyo Speed)"
            stg_sub = "Listen carefully"
            spk_prog = 0.0
            frame_img = render_interactive_short_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx
            )
        elif cur_t < t_shadow_start:
            stg = 2
            active_tok = -1
            stg_title = "[ STEP 2 ]  FORMULA & PRO-TIP"
            stg_sub = "Grammar & Nuance"
            spk_prog = 0.0
            frame_img = render_interactive_short_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx
            )
        elif cur_t < t_outro_start:
            stg = 3
            rel_shadow_t = cur_t - t_shadow_start
            spk_prog = min(1.0, max(0.0, rel_shadow_t / max(0.1, dur_drill)))
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens_drill):
                st = tok.get("start", 0.0) - 0.06
                et = tok.get("end", 0.0)
                if st <= rel_shadow_t <= et:
                    active_tok = tok_i
                    break
            stg_title = "[ STEP 3 ]  YOUR TURN: READ ALONG WITH NATIVE AUDIO"
            stg_sub = "Speak out loud with native voice!"
            frame_img = render_interactive_short_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx
            )
        else:
            stg = 4
            active_tok = -1
            stg_title = "[ STEP 4 ]  AI PITCH MATCH SCORING"
            stg_sub = "TokyoFlow App"
            spk_prog = 1.0
            frame_img = render_interactive_short_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx
            )

        frame_file = os.path.join(frames_dir, f"frame_{frame_idx:05d}.jpg")
        frame_img.save(frame_file, "JPEG", quality=90)

    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video_path
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"[OK] 9:16 Short Rendered: {out_video_path} ({total_duration:.1f}s)")

# -------------------------------------------------------------------------
# EPISODES SPECIFICATION (EP.12 to EP.19)
# -------------------------------------------------------------------------
BATCH_ENGLISH_EPISODES = [
    # -------------------------------------------------------------------------
    # EP.12: Docomo Bike & LUUP Electric Scooter Sharing (2026-10-08 Thu 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 12,
        "folder_name": "E12-Docomo_Bike_LUUP-v1.0",
        "slug": "docomo_bike_luup",
        "release_date": "2026-10-08",
        "publish_time_est": "2026-10-08T08:00:00-04:00",
        "title": "Tokyo Electric Scooter and Bike Rental Guide",
        "yt_title": "[JLPT N5] EP.12 How to Rent LUUP and Docomo Share Bikes in Tokyo! App and Return Hacks",
        "category": "Mobility & Transport • Bike Sharing",
        "level": "JLPT N5",
        "district": "Roppongi & Akasaka (六本木・赤坂)",
        "bg_image": str(ASSETS_DIR / "scene_tokyo_skyline_wide.jpg"),
        "cover": {
            "hook": "TOKYO BIKE HACK",
            "sub_hook": "RENT LUUP IN 30 SECONDS",
            "jp_line1": "アプリでQRコードを",
            "jp_line2": "スキャンして利用開始！",
            "grammar_tag": "JLPT N5 Grammar: Verb て-form + 利用開始 (Sequential Action)",
            "translation": "'Scan the QR code in the app to start your ride.'",
            "context_note": "Roppongi & Shibuya LUUP port checkout protocol",
            "location_tag": "SCENARIO: ROPPONGI LUUP DOCK"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Scan QR Code to Start Ride",
                "spoken_text": "アプリでQRコードをスキャンして利用を開始します。",
                "meaning": "Scan the QR code with the app to start using the bike.",
                "tip": "Use the て-form (スキャンして) to connect consecutive actions smoothly.",
                "tokens": [
                    {"orig": "アプリで", "kana": "あぷりで", "romaji": "apuri de", "pos": "Noun + Part.", "meaning": "With the app"},
                    {"orig": "QRコードを", "kana": "きゅーあーるこーどを", "romaji": "kyu-a-ru koodo o", "pos": "Noun + Part.", "meaning": "QR code"},
                    {"orig": "スキャンして", "kana": "すきゃんして", "romaji": "sukyan shite", "pos": "Verb (te-form)", "meaning": "Scan and"},
                    {"orig": "利用を", "kana": "りようを", "romaji": "riyou o", "pos": "Noun + Part.", "meaning": "Usage"},
                    {"orig": "開始します。", "kana": "かいしします", "romaji": "kaishi shimasu.", "pos": "Suru Verb", "meaning": "Start"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Scooter Rental Vocabulary & Rules",
                "sentence_ja": "アプリでQRコードをスキャンして利用を開始します。",
                "vocab": [
                    {"orig": "アプリ", "kana": "あぷり", "romaji": "apuri", "pos": "Noun", "meaning": "Mobile app"},
                    {"orig": "QRコード", "kana": "きゅーあーるこーど", "romaji": "kyu-a-ru koodo", "pos": "Noun", "meaning": "QR code"},
                    {"orig": "スキャンして", "kana": "すきゃんして", "romaji": "sukyan shite", "pos": "Verb (te-form)", "meaning": "Scan (connective)"},
                    {"orig": "利用", "kana": "りよう", "romaji": "riyou", "pos": "Noun", "meaning": "Usage / Rental"},
                    {"orig": "開始します", "kana": "かいしします", "romaji": "kaishi shimasu", "pos": "Verb", "meaning": "Commence / Start"}
                ],
                "grammar_title": "Grammar Pattern: Verb て-form + Main Verb (Sequence of Actions)",
                "grammar_bullets": [
                    ["1. Sequential Actions:", "Use the て-form to list chronological actions: scan QR code -> start ride."],
                    ["2. Tokyo Mobility Culture:", "LUUP electric kickboards and Docomo red bikes are everywhere in central Tokyo."],
                    ["3. Return Requirement:", "You must reserve a return port in advance via the app before parking."],
                    ["4. Parking Caution:", "Never abandon bikes outside designated port lines to avoid heavy fines."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Let's break down how to rent a LUUP electric scooter or Docomo share bike in Tokyo."},
                    {"speaker": "ja", "text": "アプリ", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: mobile phone application.", "card_idx": 0},
                    {"speaker": "ja", "text": "QRコード", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: QR code printed on the scooter handle.", "card_idx": 1},
                    {"speaker": "ja", "text": "スキャンして", "card_idx": 2},
                    {"speaker": "explainer", "text": "Verb te-form: scan the code first.", "card_idx": 2},
                    {"speaker": "ja", "text": "利用", "card_idx": 3},
                    {"speaker": "explainer", "text": "Noun: service usage or rental.", "card_idx": 3},
                    {"speaker": "ja", "text": "開始します", "card_idx": 4},
                    {"speaker": "explainer", "text": "Verb: to begin or initiate.", "card_idx": 4},
                    {"speaker": "explainer", "text": "Grammar Spotlight: connect chronological steps with the te-form.", "is_spotlight": True},
                    {"speaker": "ja", "text": "アプリでQRコードをスキャンして利用を開始します。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "Scan the QR code on the app to unlock and start riding.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "HOW TO RENT LUUP IN TOKYO\nIN 30 SECONDS!",
            "hook_audio_en": "Here is the exact Japanese phrase you need to rent e-scooters and bikes in Tokyo!",
            "jp_sentence": "QRコードをスキャンして利用を開始します。",
            "kana_sentence": "きゅーあーるこーどをすきゃんしてりようをかいしします。",
            "romaji_sentence": "QR koodo o sukyan shite riyou o kaishi shimasu.",
            "en_translation": "Scan the QR code to start your ride.",
            "tokens": [
                {"orig": "QRコードを", "kana": "きゅーあーるこーどを", "romaji": "QR koodo o", "meaning": "QR code"},
                {"orig": "スキャンして", "kana": "すきゃんして", "romaji": "sukyan shite", "meaning": "Scan and"},
                {"orig": "利用を", "kana": "りようを", "romaji": "riyou o", "meaning": "Usage"},
                {"orig": "開始します", "kana": "かいしします", "romaji": "kaishi shimasu", "meaning": "Start"}
            ],
            "pro_tip_title": "TOKYO MOBILITY PRO-TIP",
            "pro_tip_body": "Use the te-form 'sukyan shite' to smoothly chain actions before starting your ride!",
            "pro_tip_audio_en": "Notice sukyan shite. The te-form chains actions smoothly.",
            "yt_short_title": "[JLPT N5] SH.12 How to Rent LUUP in Tokyo in 30s! #Shorts #LearnJapanese",
            "pinned_comment": "Have you tried riding a LUUP electric scooter in Tokyo? Let us know in the comments!"
        }
    },

    # -------------------------------------------------------------------------
    # EP.13: Gyudon Fast-Food Customization (2026-10-09 Fri 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 13,
        "folder_name": "E13-Gyudon_Customization-v1.0",
        "slug": "gyudon_customization",
        "release_date": "2026-10-09",
        "publish_time_est": "2026-10-09T08:00:00-04:00",
        "title": "Yoshinoya and Matsuya Gyudon Customization Hacks",
        "yt_title": "[JLPT N5] EP.13 Order Gyudon Like a Tokyo Local! Yoshinoya Tsuyudaku and Set Hacks",
        "category": "Japanese Dining • Gyudon Counter",
        "level": "JLPT N5",
        "district": "Kanda & Shimbashi (神田・新橋)",
        "bg_image": str(ASSETS_DIR / "scene_izakaya_yokocho.jpg"),
        "cover": {
            "hook": "GYUDON SECRET HACK",
            "sub_hook": "ORDER LIKE A TOKYO SALARYMAN",
            "jp_line1": "牛丼並盛り、つゆだくで",
            "jp_line2": "たまごセットお願いします！",
            "grammar_tag": "JLPT N5 Grammar: Noun + でお願いします (Ordering Formula)",
            "translation": "'Regular gyudon with extra broth and egg set, please.'",
            "context_note": "Yoshinoya & Matsuya secret counter orders",
            "location_tag": "SCENARIO: YOSHINOYA KANDA COUNTER"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Ordering Gyudon with Extra Broth",
                "spoken_text": "牛丼の並盛り、つゆだくでお願いします。",
                "meaning": "Regular beef bowl with extra beef broth, please.",
                "tip": "'つゆだく' (tsuyudaku) is the legendary insider term for extra savory broth.",
                "tokens": [
                    {"orig": "牛丼の", "kana": "ぎゅうどんの", "romaji": "gyuudon no", "pos": "Noun + Part.", "meaning": "Beef bowl's"},
                    {"orig": "並盛り、", "kana": "なみもり", "romaji": "nami-mori,", "pos": "Noun", "meaning": "Regular size,"},
                    {"orig": "つゆだくで", "kana": "つゆだくで", "romaji": "tsuyu-daku de", "pos": "Slang + Part.", "meaning": "With extra broth"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegai shimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Counter Sizing & Secret Customizations",
                "sentence_ja": "牛丼の並盛り、つゆだくでお願いします。",
                "vocab": [
                    {"orig": "牛丼", "kana": "ぎゅうどん", "romaji": "gyuudon", "pos": "Noun", "meaning": "Beef bowl"},
                    {"orig": "並盛り", "kana": "なみもり", "romaji": "nami-mori", "pos": "Noun", "meaning": "Regular portion"},
                    {"orig": "つゆだく", "kana": "つゆだく", "romaji": "tsuyu-daku", "pos": "Food Jargon", "meaning": "Extra soup/broth"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu", "pos": "Polite Phrase", "meaning": "Please / I request"}
                ],
                "grammar_title": "Ordering Formula: Item + [Customization] でお願いします",
                "grammar_bullets": [
                    ["1. Standard Sizing:", "並盛り (regular), 大盛り (large), 特盛り (extra large)."],
                    ["2. Broth Options:", "つゆだく (extra soup), つゆぬき (no soup), ねぎだく (extra onions)."],
                    ["3. Condiment Etiquette:", "Pickled red ginger (紅生姜) and shichimi pepper are free on the counter."],
                    ["4. Payment Protocol:", "Pay at the counter after eating at Yoshinoya, or buy a ticket first at Matsuya."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Here is the golden order formula for Japanese beef bowl restaurants like Yoshinoya and Sukiya."},
                    {"speaker": "ja", "text": "牛丼", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: gyudon, Japanese simmered beef over rice.", "card_idx": 0},
                    {"speaker": "ja", "text": "並盛り", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: regular standard portion size.", "card_idx": 1},
                    {"speaker": "ja", "text": "つゆだく", "card_idx": 2},
                    {"speaker": "explainer", "text": "Insider term: requesting extra delicious beef broth over your rice.", "card_idx": 2},
                    {"speaker": "ja", "text": "お願いします", "card_idx": 3},
                    {"speaker": "explainer", "text": "Polite request: please make it so.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: use de onegai shimasu to specify customizations.", "is_spotlight": True},
                    {"speaker": "ja", "text": "牛丼の並盛り、つゆだくでお願いします。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "Regular beef bowl with extra broth, please.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "ORDER GYUDON LIKE A LOCAL\nIN 30 SECONDS!",
            "hook_audio_en": "Here is the secret insider phrase Tokyo locals use at Yoshinoya and Matsuya!",
            "jp_sentence": "牛丼の並盛り、つゆだくでお願いします。",
            "kana_sentence": "ぎゅうどんのなみもり、つゆだくでおねがいします。",
            "romaji_sentence": "Gyuudon no nami-mori, tsuyu-daku de onegai shimasu.",
            "en_translation": "Regular beef bowl with extra broth, please.",
            "tokens": [
                {"orig": "牛丼の", "kana": "ぎゅうどんの", "romaji": "gyuudon no", "meaning": "Gyudon's"},
                {"orig": "並盛り、", "kana": "なみもり", "romaji": "nami-mori,", "meaning": "Regular,"},
                {"orig": "つゆだくで", "kana": "つゆだくで", "romaji": "tsuyu-daku de", "meaning": "Extra broth"},
                {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu", "meaning": "Please"}
            ],
            "pro_tip_title": "YOSHINOYA INSIDER PRO-TIP",
            "pro_tip_body": "'Tsuyu-daku' asks the chef to pour generous beef simmer broth over your rice bowl for free!",
            "pro_tip_audio_en": "Tsuyu-daku means extra simmered beef broth over your rice for free!",
            "yt_short_title": "[JLPT N5] SH.13 How to Order Gyudon at Yoshinoya Like a Pro #Shorts #LearnJapanese",
            "pinned_comment": "Do you like your Gyudon with extra broth (tsuyudaku) or extra onions (negidaku)?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.14: Japan Post Redelivery Notice (2026-10-12 Mon 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 14,
        "folder_name": "E14-JapanPost_Redelivery-v1.0",
        "slug": "japanpost_redelivery",
        "release_date": "2026-10-12",
        "publish_time_est": "2026-10-12T08:00:00-04:00",
        "title": "Japan Post Redelivery Slip and Package Recovery Hacks",
        "yt_title": "[JLPT N4] EP.14 Never Miss Japanese Mail! Japan Post Redelivery Slip and Delivery Hacks",
        "category": "Living Logistics • Japan Post",
        "level": "JLPT N4",
        "district": "Shimokitazawa (下北沢)",
        "bg_image": str(ASSETS_DIR / "scene_kombini_store.jpg"),
        "cover": {
            "hook": "JAPAN MAIL HACK",
            "sub_hook": "DECODE FUZAIHYO IN 30 SECONDS",
            "jp_line1": "不在票が入っていたので、",
            "jp_line2": "再配達をお願いします！",
            "grammar_tag": "JLPT N4 Grammar: ~ので (Polite Objective Cause / Reason)",
            "translation": "'I received a missed delivery notice, please redeliver.'",
            "context_note": "Japan Post & Yamato Transport redelivery calls",
            "location_tag": "SCENARIO: SHIMOKITAZAWA APARTMENT"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Requesting Package Redelivery",
                "spoken_text": "不在連絡票が入っていたので、再配達をお願いします。",
                "meaning": "I received a missed delivery slip, so I would like to request redelivery.",
                "tip": "Use 'ので' instead of 'から' when talking to service representatives for a polite tone.",
                "tokens": [
                    {"orig": "不在連絡票が", "kana": "ふざいれんらくひょうが", "romaji": "fuzai-renrakuhyou ga", "pos": "Noun + Part.", "meaning": "Missed delivery slip"},
                    {"orig": "入っていたので、", "kana": "はいっていたので", "romaji": "haitte ita node,", "pos": "Verb + Conjunction", "meaning": "Was in the mailbox, so"},
                    {"orig": "再配達を", "kana": "さいはいたつを", "romaji": "sai-haitatsu o", "pos": "Noun + Part.", "meaning": "Redelivery"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegai shimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Delivery Slips & Time Slot Jargon",
                "sentence_ja": "不在連絡票が入っていたので、再配達をお願いします。",
                "vocab": [
                    {"orig": "不在連絡票", "kana": "ふざいれんらくひょう", "romaji": "fuzai-renrakuhyou", "pos": "Noun", "meaning": "Missed delivery slip (不在票)"},
                    {"orig": "入っていた", "kana": "はいっていた", "romaji": "haitte ita", "pos": "Verb (past continuous)", "meaning": "Was inserted / delivered"},
                    {"orig": "ので", "kana": "ので", "romaji": "node", "pos": "Conjunction", "meaning": "Because / Since (polite)"},
                    {"orig": "再配達", "kana": "さいはいたつ", "romaji": "sai-haitatsu", "pos": "Noun", "meaning": "Redelivery"}
                ],
                "grammar_title": "Polite Reason Pattern: Verb (Plain Form) + ので (Since / Because)",
                "grammar_bullets": [
                    ["1. Polite Justification:", "'ので' sounds softer and more objective than 'から' when calling courier services."],
                    ["2. QR Code Automated Option:", "Most slips (不在票) have a QR code you can scan on Line or Safari to pick a time without speaking."],
                    ["3. Standard Delivery Slots:", "午前中 (morning), 14-16時 (early afternoon), 19-21時 (night)."],
                    ["4. Kombini Pickup:", "You can also redirect packages to your local 7-Eleven or FamilyMart."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "When you miss a package delivery in Japan, here is how to arrange redelivery like a local."},
                    {"speaker": "ja", "text": "不在連絡票", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: missed delivery notice left in your mailbox.", "card_idx": 0},
                    {"speaker": "ja", "text": "入っていた", "card_idx": 1},
                    {"speaker": "explainer", "text": "Verb: was placed inside.", "card_idx": 1},
                    {"speaker": "ja", "text": "ので", "card_idx": 2},
                    {"speaker": "explainer", "text": "Conjunction: polite because or since.", "card_idx": 2},
                    {"speaker": "ja", "text": "再配達", "card_idx": 3},
                    {"speaker": "explainer", "text": "Noun: redelivery of your parcel.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: explain reason politely with node.", "is_spotlight": True},
                    {"speaker": "ja", "text": "不在連絡票が入っていたので、再配達をお願いします。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "I got a missed delivery notice, so please redeliver my package.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "NEVER MISS JAPAN MAIL\nIN 30 SECONDS!",
            "hook_audio_en": "Here is the essential phrase to request package redelivery in Japan!",
            "jp_sentence": "不在票が入っていたので、再配達をお願いします。",
            "kana_sentence": "ふざいひょうがはいっていたので、さいはいたつをおねがいします。",
            "romaji_sentence": "Fuzaihyou ga haitte ita node, sai-haitatsu o onegai shimasu.",
            "en_translation": "I received a missed delivery slip, please redeliver.",
            "tokens": [
                {"orig": "不在票が", "kana": "ふざいひょうが", "romaji": "fuzaihyou ga", "meaning": "Missed delivery slip"},
                {"orig": "入っていたので、", "kana": "はいっていたので", "romaji": "haitte ita node,", "meaning": "Was left, so"},
                {"orig": "再配達を", "kana": "さいはいたつを", "romaji": "sai-haitatsu o", "meaning": "Redelivery"},
                {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu", "meaning": "Please"}
            ],
            "pro_tip_title": "JAPAN POST PRO-TIP",
            "pro_tip_body": "Use 'node' to give polite reasons when speaking to customer service representatives in Japan!",
            "pro_tip_audio_en": "Use node for polite reasons when speaking to Japanese delivery staff.",
            "yt_short_title": "[JLPT N4] SH.14 How to Redeliver Packages in Japan #Shorts #LearnJapanese",
            "pinned_comment": "Have you ever found a mysterious 不在票 (fuzaihyo) in your Japanese mailbox?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.15: Tokyo Supermarket 8 PM Half-Price Rush (2026-10-13 Tue 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 15,
        "folder_name": "E15-Supermarket_HalfPrice_Rush-v1.0",
        "slug": "supermarket_halfprice_rush",
        "release_date": "2026-10-13",
        "publish_time_est": "2026-10-13T08:00:00-04:00",
        "title": "Tokyo Supermarket 8 PM Half-Price Sticker Hunt Hacks",
        "yt_title": "[JLPT N5] EP.15 Tokyo Supermarket 8 PM Half-Price Hunt! Hangaku Bento and Sashimi Hacks",
        "category": "Supermarket Shopping • Daily Life",
        "level": "JLPT N5",
        "district": "Koenji (高円寺)",
        "bg_image": str(ASSETS_DIR / "scene_kombini_store.jpg"),
        "cover": {
            "hook": "SUPERMARKET HACK",
            "sub_hook": "50% OFF BENTO & SASHIMI",
            "jp_line1": "8時になるとお惣菜に",
            "jp_line2": "半額シールが貼られます！",
            "grammar_tag": "JLPT N5 Grammar: Verb (Plain Form) + と (Natural Condition / Whenever)",
            "translation": "'Whenever 8 PM comes, half-price stickers are placed on prepared food!'",
            "context_note": "Tokyo evening supermarket clearance frenzy",
            "location_tag": "SCENARIO: KOENJI SUPERMARKET AISLE"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. The 8 PM Half-Price Clearance",
                "spoken_text": "夜8時になると、お惣菜に半額シールが貼られます。",
                "meaning": "When 8 PM arrives, half-price discount stickers are placed on prepared food.",
                "tip": "The conditional 'と' indicates an automatic, predictable daily event.",
                "tokens": [
                    {"orig": "夜8時に", "kana": "よるはちじに", "romaji": "yoru hachi-ji ni", "pos": "Time Noun + Part.", "meaning": "At 8 PM"},
                    {"orig": "なると、", "kana": "なると", "romaji": "naru to,", "pos": "Verb + Part.", "meaning": "When it becomes,"},
                    {"orig": "お惣菜に", "kana": "おそうざいに", "romaji": "osouzai ni", "pos": "Noun + Part.", "meaning": "On side dishes"},
                    {"orig": "半額シールが", "kana": "はんがくしーるが", "romaji": "hangaku shiiru ga", "pos": "Noun + Part.", "meaning": "Half-price stickers"},
                    {"orig": "貼られます。", "kana": "はられます", "romaji": "hararemasu.", "pos": "Passive Verb", "meaning": "Are affixed"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Discount Percentages & Supermarket Culture",
                "sentence_ja": "夜8時になると、お惣菜に半額シールが貼られます。",
                "vocab": [
                    {"orig": "お惣菜", "kana": "おそうざい", "romaji": "osouzai", "pos": "Noun", "meaning": "Delicatessen / Prepared dishes"},
                    {"orig": "半額", "kana": "はんがく", "romaji": "hangaku", "pos": "Noun", "meaning": "Half price (50% off)"},
                    {"orig": "割引", "kana": "わりびき", "romaji": "waribiki", "pos": "Noun", "meaning": "Discount"},
                    {"orig": "貼られます", "kana": "はられます", "romaji": "hararemasu", "pos": "Passive Verb", "meaning": "Are pasted / affixed"}
                ],
                "grammar_title": "Conditional Pattern: Verb (Present) + と (Whenever / As Soon As)",
                "grammar_bullets": [
                    ["1. Automatic Result:", "Verb plain form + と expresses guaranteed consequences (e.g. at 8 PM, stickers appear)."],
                    ["2. Discount Progression:", "2割引 (20% off) at 6 PM -> 3割引 (30% off) at 7 PM -> 半額 (50% off) at 8 PM."],
                    ["3. Best Targets:", "High-grade sushi and sashimi platters, karaage fried chicken, and tonkatsu bento."],
                    ["4. Local Etiquette:", "Do not crowd the clerk with the sticker gun—wait politely until they finish applying the stickers."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Every night around 8 PM, Tokyo supermarkets start their famous half-price discount clearance."},
                    {"speaker": "ja", "text": "お惣菜", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: fresh prepared side dishes and bentos.", "card_idx": 0},
                    {"speaker": "ja", "text": "半額", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: 50% off half-price discount.", "card_idx": 1},
                    {"speaker": "ja", "text": "割引", "card_idx": 2},
                    {"speaker": "explainer", "text": "Noun: discount or price reduction.", "card_idx": 2},
                    {"speaker": "ja", "text": "貼られます", "card_idx": 3},
                    {"speaker": "explainer", "text": "Passive verb: are placed or affixed.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: use to for natural automatic timing.", "is_spotlight": True},
                    {"speaker": "ja", "text": "夜8時になると、お惣菜に半額シールが貼られます。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "When 8 PM comes, half-price stickers are placed on prepared dishes.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "TOKYO 8 PM HALF-PRICE HUNT\nIN 30 SECONDS!",
            "hook_audio_en": "Here is how to get 50% off luxury sushi and bento every night in Tokyo supermarkets!",
            "jp_sentence": "夜8時になると、お惣菜に半額シールが貼られます。",
            "kana_sentence": "よるはちじになると、おそうざいにはんがくしーるがはられます。",
            "romaji_sentence": "Yoru hachi-ji ni naru to, osouzai ni hangaku shiiru ga hararemasu.",
            "en_translation": "At 8 PM, half-price stickers are placed on prepared food.",
            "tokens": [
                {"orig": "8時に", "kana": "はちじに", "romaji": "hachi-ji ni", "meaning": "At 8 PM"},
                {"orig": "なると、", "kana": "なると", "romaji": "naru to,", "meaning": "When it turns,"},
                {"orig": "お惣菜に", "kana": "おそうざいに", "romaji": "osouzai ni", "meaning": "On food"},
                {"orig": "半額シールが", "kana": "はんがくしーるが", "romaji": "hangaku shiiru ga", "meaning": "Half-price stickers"},
                {"orig": "貼られます", "kana": "はられます", "romaji": "hararemasu", "meaning": "Are attached"}
            ],
            "pro_tip_title": "SUPERMARKET SAVINGS PRO-TIP",
            "pro_tip_body": "Look for the red '半額' (hangaku) sticker on fresh sushi and bento boxes after 8 PM!",
            "pro_tip_audio_en": "Look for the red kanji hangaku for instant 50% off deals.",
            "yt_short_title": "[JLPT N5] SH.15 How to Hunt Half-Price Bento in Tokyo #Shorts #LearnJapanese",
            "pinned_comment": "Have you scored a half-price sushi or bento feast at a Japanese supermarket?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.16: Tokyo Drugstore Medicine & Symptoms (2026-10-14 Wed 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 16,
        "folder_name": "E16-Drugstore_Medicine-v1.0",
        "slug": "drugstore_medicine",
        "release_date": "2026-10-14",
        "publish_time_est": "2026-10-14T08:00:00-04:00",
        "title": "Tokyo Drugstore Painkiller and Symptom Guide",
        "yt_title": "[JLPT N5] EP.16 Tokyo Drugstore Survival! Buying Painkillers and Explaining Symptoms",
        "category": "Healthcare & Shopping • Drugstore",
        "level": "JLPT N5",
        "district": "Shinjuku East (新宿東口)",
        "bg_image": str(ASSETS_DIR / "scene_akiba_street.jpg"),
        "cover": {
            "hook": "DRUGSTORE HACK",
            "sub_hook": "BUY PAINKILLERS IN TOKYO",
            "jp_line1": "頭痛がひどいので、",
            "jp_line2": "よく効く痛み止めありますか？",
            "grammar_tag": "JLPT N5 Grammar: Noun がする (Expressing Physical Symptoms & Sensations)",
            "translation": "'I have a bad headache, do you have effective painkillers?'",
            "context_note": "Matsumoto Kiyoshi & Sundrug pharmacist inquiries",
            "location_tag": "SCENARIO: MATSUMOTO KIYOSHI SHINJUKU"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Asking Pharmacist for Painkillers",
                "spoken_text": "頭痛がひどいので、よく効く痛み止めはありますか？",
                "meaning": "I have a severe headache, do you have an effective painkiller?",
                "tip": "Use '〜がひどい' (is severe) to clearly communicate pain intensity to pharmacy staff.",
                "tokens": [
                    {"orig": "頭痛が", "kana": "ずつうが", "romaji": "zutsuu ga", "pos": "Noun + Part.", "meaning": "Headache"},
                    {"orig": "ひどいので、", "kana": "ひどいので", "romaji": "hidoi node,", "pos": "Adjective + Conjunction", "meaning": "Is severe, so"},
                    {"orig": "よく効く", "kana": "よくきく", "romaji": "yoku kiku", "pos": "Adverb + Verb", "meaning": "Works effectively"},
                    {"orig": "痛み止めは", "kana": "いたみどめは", "romaji": "itami-dome wa", "pos": "Noun + Part.", "meaning": "Painkillers"},
                    {"orig": "ありますか？", "kana": "ありますか", "romaji": "arimasu ka?", "pos": "Verb (Question)", "meaning": "Do you have?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Common Japanese Symptoms & Dosages",
                "sentence_ja": "頭痛がひどいので、よく効く痛み止めはありますか？",
                "vocab": [
                    {"orig": "頭痛", "kana": "ずつう", "romaji": "zutsuu", "pos": "Noun", "meaning": "Headache"},
                    {"orig": "痛み止め", "kana": "いたみどめ", "romaji": "itami-dome", "pos": "Noun", "meaning": "Painkiller (Analgesic)"},
                    {"orig": "よく効く", "kana": "よくきく", "romaji": "yoku kiku", "pos": "Verb Phrase", "meaning": "Highly effective"},
                    {"orig": "食後", "kana": "しょくご", "romaji": "shokugo", "pos": "Noun", "meaning": "After meals"}
                ],
                "grammar_title": "Symptom Formula: [Body Part / Symptom] がひどい (Severe Pain)",
                "grammar_bullets": [
                    ["1. Top Painkiller Brands:", "EVE (イブ) for mild headaches, Loxonin (ロキソニン) for fast strong relief."],
                    ["2. Essential Symptom Words:", "胃痛 (stomach ache), 発熱 (fever), 喉の痛み (sore throat), 鼻水 (runny nose)."],
                    ["3. Dosage Instructions:", "食後に1回2錠 (Take 2 tablets once after meals with water)."],
                    ["4. Pharmacist Counter:", "Class 1 medications like Loxonin require a registered pharmacist (薬剤師) on duty."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Let's learn how to explain your symptoms and buy over-the-counter medicine at Japanese drugstores."},
                    {"speaker": "ja", "text": "頭痛", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: headache or head pain.", "card_idx": 0},
                    {"speaker": "ja", "text": "痛み止め", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: painkiller or pain relief medication.", "card_idx": 1},
                    {"speaker": "ja", "text": "よく効く", "card_idx": 2},
                    {"speaker": "explainer", "text": "Verb phrase: works effectively and quickly.", "card_idx": 2},
                    {"speaker": "ja", "text": "食後", "card_idx": 3},
                    {"speaker": "explainer", "text": "Noun: taking medicine after finishing meals.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: state your symptom clearly with ga hidoi.", "is_spotlight": True},
                    {"speaker": "ja", "text": "頭痛がひどいので、よく効く痛み止めはありますか？", "is_spotlight": True},
                    {"speaker": "explainer", "text": "I have a bad headache, do you have effective painkillers?", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "BUY MEDICINE IN TOKYO\nIN 30 SECONDS!",
            "hook_audio_en": "Here is how to buy painkillers and cold medicine at any Japanese drugstore!",
            "jp_sentence": "頭痛がひどいので、よく効く痛み止めはありますか？",
            "kana_sentence": "ずつうがひどいので、よくきくいたみどめはありますか？",
            "romaji_sentence": "Zutsuu ga hidoi node, yoku kiku itami-dome wa arimasu ka?",
            "en_translation": "I have a bad headache, do you have effective painkillers?",
            "tokens": [
                {"orig": "頭痛が", "kana": "ずつうが", "romaji": "zutsuu ga", "meaning": "Headache"},
                {"orig": "ひどいので、", "kana": "ひどいので", "romaji": "hidoi node,", "meaning": "Is severe, so"},
                {"orig": "よく効く", "kana": "よくきく", "romaji": "yoku kiku", "meaning": "Effective"},
                {"orig": "痛み止めは", "kana": "いたみどめは", "romaji": "itami-dome wa", "meaning": "Painkillers"},
                {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka", "meaning": "Do you have"}
            ],
            "pro_tip_title": "TOKYO DRUGSTORE PRO-TIP",
            "pro_tip_body": "Ask for 'EVE' or 'Loxonin' directly if you need fast, proven headache and fever relief!",
            "pro_tip_audio_en": "Ask for EVE or Loxonin for fast and proven headache relief.",
            "yt_short_title": "[JLPT N5] SH.16 How to Buy Painkillers in Tokyo Drugstores #Shorts #LearnJapanese",
            "pinned_comment": "What Japanese over-the-counter medicine do you always stock up on when visiting Japan?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.17: Tokyo Sento & Onsen Bath Etiquette (2026-10-15 Thu 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 17,
        "folder_name": "E17-Onsen_Sento_Etiquette-v1.0",
        "slug": "onsen_sento_etiquette",
        "release_date": "2026-10-15",
        "publish_time_est": "2026-10-15T08:00:00-04:00",
        "title": "Tokyo Public Bath and Onsen Hot Springs Etiquette Guide",
        "yt_title": "[JLPT N5] EP.17 Tokyo Public Bath and Onsen Etiquette! Washing Rules and Towel Protocol",
        "category": "Culture & Wellness • Sento & Onsen",
        "level": "JLPT N5",
        "district": "Asakusa (浅草)",
        "bg_image": str(ASSETS_DIR / "scene_onsen_sento.jpg"),
        "cover": {
            "hook": "ONSEN ETIQUETTE HACK",
            "sub_hook": "SURVIVE TOKYO PUBLIC BATHS",
            "jp_line1": "湯船に入る前に、",
            "jp_line2": "体をきれいに洗ってください！",
            "grammar_tag": "JLPT N5 Grammar: Verb (Plain Form) + 前に (Before Doing Something)",
            "translation": "'Wash your body thoroughly before entering the hot bath tub!'",
            "context_note": "Traditional Asakusa sento & onsen golden rule",
            "location_tag": "SCENARIO: ASAKUSA TRADITIONAL SENTO"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. The Golden Rule of Hot Springs",
                "spoken_text": "湯船に入る前に、かけ湯で体を洗い流してください。",
                "meaning": "Before getting into the bath, please rinse and wash your body thoroughly.",
                "tip": "Never step into the communal bath water without thoroughly rinsing first.",
                "tokens": [
                    {"orig": "湯船に", "kana": "ゆぶねに", "romaji": "yubune ni", "pos": "Noun + Part.", "meaning": "Bath tub"},
                    {"orig": "入る前に、", "kana": "はいるまえに", "romaji": "hairu mae ni,", "pos": "Verb + Noun + Part.", "meaning": "Before entering,"},
                    {"orig": "かけ湯で", "kana": "かけゆで", "romaji": "kakeyu de", "pos": "Noun + Part.", "meaning": "With rinse water"},
                    {"orig": "体を", "kana": "からだを", "romaji": "karada o", "pos": "Noun + Part.", "meaning": "Body"},
                    {"orig": "洗い流してください。", "kana": "あらいながしてください", "romaji": "arainagashite kudasai.", "pos": "Polite Command", "meaning": "Please wash and rinse"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Sento Vocabulary & Onsen Rules",
                "sentence_ja": "湯船に入る前に、かけ湯で体を洗い流してください。",
                "vocab": [
                    {"orig": "湯船", "kana": "ゆぶね", "romaji": "yubune", "pos": "Noun", "meaning": "Bathtub / Soaking pool"},
                    {"orig": "入る前に", "kana": "はいるまえに", "romaji": "hairu mae ni", "pos": "Grammar Structure", "meaning": "Before entering"},
                    {"orig": "かけ湯", "kana": "かけゆ", "romaji": "kakeyu", "pos": "Noun", "meaning": "Preliminary hot water rinse"},
                    {"orig": "洗い流す", "kana": "あらいながす", "romaji": "arainagasu", "pos": "Compound Verb", "meaning": "Wash away / Rinse off"}
                ],
                "grammar_title": "Time Sequence Pattern: Verb (Dictionary Form) + 前に (Before Doing)",
                "grammar_bullets": [
                    ["1. Wash First Rule:", "The communal bath tub (湯船) is strictly for soaking—all soaping and scrubbing happens at individual stalls."],
                    ["2. Towel Protocol:", "Small privacy towels must never touch the hot spring water—rest them on your head or edge of the tub."],
                    ["3. Dry Off Before Dressing:", "Wipe your body dry with your towel before stepping back into the changing room (脱衣所)."],
                    ["4. Hydration & Milk:", "Drinking chilled fruit milk (フルーツ牛乳) after soaking is a cherished Tokyo sento tradition."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Let's master the sacred etiquette rules of Japanese public baths and onsen hot springs."},
                    {"speaker": "ja", "text": "湯船", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: communal hot bath soaking tub.", "card_idx": 0},
                    {"speaker": "ja", "text": "入る前に", "card_idx": 1},
                    {"speaker": "explainer", "text": "Grammar: before entering or stepping inside.", "card_idx": 1},
                    {"speaker": "ja", "text": "かけ湯", "card_idx": 2},
                    {"speaker": "explainer", "text": "Noun: rinsing your body with hot water before soaking.", "card_idx": 2},
                    {"speaker": "ja", "text": "洗い流す", "card_idx": 3},
                    {"speaker": "explainer", "text": "Verb: to wash and rinse off thoroughly.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: express prior conditions with mae ni.", "is_spotlight": True},
                    {"speaker": "ja", "text": "湯船に入る前に、かけ湯で体を洗い流してください。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "Before getting into the tub, please rinse and wash your body clean.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "ONSEN SURVIVAL RULES\nIN 30 SECONDS!",
            "hook_audio_en": "Here is the number one etiquette rule you must follow in Japanese onsen and sento baths!",
            "jp_sentence": "湯船に入る前に、体をきれいに洗ってください。",
            "kana_sentence": "ゆぶねにはいるまえに、からだをきれいにとあらってください。",
            "romaji_sentence": "Yubune ni hairu mae ni, karada o kirei ni aratte kudasai.",
            "en_translation": "Wash your body clean before getting into the bath.",
            "tokens": [
                {"orig": "湯船に", "kana": "ゆぶねに", "romaji": "yubune ni", "meaning": "In the tub"},
                {"orig": "入る前に、", "kana": "はいるまえに", "romaji": "hairu mae ni,", "meaning": "Before entering,"},
                {"orig": "体を", "kana": "からだを", "romaji": "karada o", "meaning": "Body"},
                {"orig": "きれいに", "kana": "きれいに", "romaji": "kirei ni", "meaning": "Cleanly"},
                {"orig": "洗ってください", "kana": "あらってください", "romaji": "aratte kudasai", "meaning": "Please wash"}
            ],
            "pro_tip_title": "ONSEN ETIQUETTE PRO-TIP",
            "pro_tip_body": "Always wash and rinse your body thoroughly at the seated wash stalls before stepping into the tub!",
            "pro_tip_audio_en": "Wash at the sit-down stalls first before touching the bath water.",
            "yt_short_title": "[JLPT N5] SH.17 Onsen Bath Etiquette in Tokyo in 30s! #Shorts #LearnJapanese",
            "pinned_comment": "Have you experienced a traditional Tokyo neighborhood sento (public bath)?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.18: Tokyo Cafe Ordering & Customizing (2026-10-16 Fri 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 18,
        "folder_name": "E18-Tokyo_Cafe_Ordering-v1.0",
        "slug": "tokyo_cafe_ordering",
        "release_date": "2026-10-16",
        "publish_time_est": "2026-10-16T08:00:00-04:00",
        "title": "Tokyo Cafe Ordering and Drink Customization Hacks",
        "yt_title": "[JLPT N5] EP.18 Order Coffee and Custom Drinks in Tokyo! Takeout and Milk Hacks",
        "category": "Cafe & Dining • Coffee Shop",
        "level": "JLPT N5",
        "district": "Shibuya & Omotesando (渋谷・表参道)",
        "bg_image": str(ASSETS_DIR / "scene_tokyo_skyline_distant_4k.jpg"),
        "cover": {
            "hook": "TOKYO CAFE HACK",
            "sub_hook": "ORDER DRINKS LIKE A LOCAL",
            "jp_line1": "アイスラテを豆乳変更で、",
            "jp_line2": "お持ち帰りお願いします！",
            "grammar_tag": "JLPT N5 Grammar: Noun + 変更で (Customization / Substitution Formula)",
            "translation": "'Iced latte with soy milk substitution, to go please!'",
            "context_note": "Starbucks, Doutor & Omotesando specialty cafes",
            "location_tag": "SCENARIO: SHIBUYA SPECIALTY CAFE"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Ordering Custom Iced Latte To-Go",
                "spoken_text": "アイスラテを豆乳に変更で、お持ち帰りでお願いします。",
                "meaning": "An iced latte with soy milk substitution, to go please.",
                "tip": "Use '豆乳に変更' (tounyuu ni henkou) to substitute dairy with soy milk seamlessly.",
                "tokens": [
                    {"orig": "アイスラテを", "kana": "あいすらてを", "romaji": "aisu rate o", "pos": "Noun + Part.", "meaning": "Iced latte"},
                    {"orig": "豆乳に", "kana": "とうにゅうに", "romaji": "tounyuu ni", "pos": "Noun + Part.", "meaning": "To soy milk"},
                    {"orig": "変更で、", "kana": "へんこうで", "romaji": "henkou de,", "pos": "Noun + Part.", "meaning": "With substitution,"},
                    {"orig": "お持ち帰りで", "kana": "おもちかえりで", "romaji": "omochikaeri de", "pos": "Noun + Part.", "meaning": "For takeout"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegai shimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Takeout vs Eat-In Tax & Milk Customizations",
                "sentence_ja": "アイスラテを豆乳に変更で、お持ち帰りでお願いします。",
                "vocab": [
                    {"orig": "アイスラテ", "kana": "あいすらて", "romaji": "aisu rate", "pos": "Noun", "meaning": "Iced latte"},
                    {"orig": "豆乳", "kana": "とうにゅう", "romaji": "tounyuu", "pos": "Noun", "meaning": "Soy milk"},
                    {"orig": "変更", "kana": "へんこう", "romaji": "henkou", "pos": "Noun", "meaning": "Change / Substitution"},
                    {"orig": "お持ち帰り", "kana": "おもちかえり", "romaji": "omochikaeri", "pos": "Polite Noun", "meaning": "Takeout / To go"}
                ],
                "grammar_title": "Cafe Jargon: [Option] に変更 (Substitute with) & 店内 vs 持ち帰り",
                "grammar_bullets": [
                    ["1. Tax Difference:", "店内ご利用 (eat-in) is 10% tax; お持ち帰り (takeout) is 8% tax in Japan."],
                    ["2. Milk Options:", "ソイミルク / 豆乳 (soy), オーツミルク (oat), アーモンドミルク (almond)."],
                    ["3. Temperature & Ice:", "ホット (hot), アイス (iced), 氷少なめ (light ice)."],
                    ["4. Size Words:", "ショート (short), トール (tall), グランデ (grande)."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Here is how to order customized coffee drinks like a local at Tokyo cafes."},
                    {"speaker": "ja", "text": "アイスラテ", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: iced cafe latte.", "card_idx": 0},
                    {"speaker": "ja", "text": "豆乳", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: soy milk.", "card_idx": 1},
                    {"speaker": "ja", "text": "変更", "card_idx": 2},
                    {"speaker": "explainer", "text": "Noun: substitution or modification.", "card_idx": 2},
                    {"speaker": "ja", "text": "お持ち帰り", "card_idx": 3},
                    {"speaker": "explainer", "text": "Polite noun: to go or takeout order.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: customize with ni henkou de.", "is_spotlight": True},
                    {"speaker": "ja", "text": "アイスラテを豆乳に変更で、お持ち帰りでお願いします。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "Iced latte with soy milk substitution, to go please.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "ORDER COFFEE IN TOKYO\nIN 30 SECONDS!",
            "hook_audio_en": "Here is how to customize your drink and order takeout at any Tokyo cafe!",
            "jp_sentence": "アイスラテを豆乳に変更で、お持ち帰りお願いします。",
            "kana_sentence": "あいすらてをとうにゅうにへんこうで、おもちかえりおねがいします。",
            "romaji_sentence": "Aisu rate o tounyuu ni henkou de, omochikaeri onegai shimasu.",
            "en_translation": "Iced latte with soy milk substitution, to go please.",
            "tokens": [
                {"orig": "アイスラテを", "kana": "あいすらてを", "romaji": "aisu rate o", "meaning": "Iced latte"},
                {"orig": "豆乳に", "kana": "とうにゅうに", "romaji": "tounyuu ni", "meaning": "To soy milk"},
                {"orig": "変更で、", "kana": "へんこうで", "romaji": "henkou de,", "meaning": "Change,"},
                {"orig": "お持ち帰り", "kana": "おもちかえり", "romaji": "omochikaeri", "meaning": "Takeout"},
                {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu", "meaning": "Please"}
            ],
            "pro_tip_title": "TOKYO CAFE PRO-TIP",
            "pro_tip_body": "Say 'omochikaeri de' for to-go orders to get the 8% reduced food tax rate in Japan!",
            "pro_tip_audio_en": "Say omochikaeri de for to-go orders and the 8% tax rate.",
            "yt_short_title": "[JLPT N5] SH.18 How to Order Coffee at Tokyo Cafes #Shorts #LearnJapanese",
            "pinned_comment": "What is your favorite coffee order when exploring Tokyo's cafe scene?"
        }
    },

    # -------------------------------------------------------------------------
    # EP.19: Shinkansen Bullet Train Tickets (2026-10-19 Mon 08:00 EDT)
    # -------------------------------------------------------------------------
    {
        "episode_number": 19,
        "folder_name": "E19-Shinkansen_BulletTrain_Tickets-v1.0",
        "slug": "shinkansen_bullettrain_tickets",
        "release_date": "2026-10-19",
        "publish_time_est": "2026-10-19T08:00:00-04:00",
        "title": "Shinkansen Bullet Train Ticket Booking and Seat Selection Hacks",
        "yt_title": "[JLPT N4] EP.19 Book Shinkansen Bullet Train Tickets! Reserved Seats and Green Car Hacks",
        "category": "Intercity Travel • Shinkansen Bullet Train",
        "level": "JLPT N4",
        "district": "Tokyo Station (東京駅)",
        "bg_image": str(ASSETS_DIR / "scene_yamanote_platform.jpg"),
        "cover": {
            "hook": "SHINKANSEN HACK",
            "sub_hook": "BOOK BULLET TRAIN IN 30 SECONDS",
            "jp_line1": "京都までの指定席を、",
            "jp_line2": "富士山側の窓席でお願いします！",
            "grammar_tag": "JLPT N4 Grammar: Destination + までの + Noun (Tickets Bound for...)",
            "translation": "'Reserved seat to Kyoto with Mt. Fuji window view, please!'",
            "context_note": "Midori-no-Madoguchi ticket window booking",
            "location_tag": "SCENARIO: TOKYO STATION MIDORI-NO-MADOGUCHI"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Booking Shinkansen Reserved Seats",
                "spoken_text": "京都までの指定席を、富士山側の窓側でお願いします。",
                "meaning": "A reserved seat to Kyoto on the Mt. Fuji window side, please.",
                "tip": "Seat E on the Tokaido Shinkansen (2-seat row) guarantees the best view of Mt. Fuji.",
                "tokens": [
                    {"orig": "京都までの", "kana": "きょうとまでの", "romaji": "kyouto made no", "pos": "Noun + Particle", "meaning": "To Kyoto"},
                    {"orig": "指定席を、", "kana": "していせきを", "romaji": "shiteiseki o,", "pos": "Noun + Particle", "meaning": "Reserved seat,"},
                    {"orig": "富士山側の", "kana": "ふじさんかわの", "romaji": "fujisan-gawa no", "pos": "Noun + Particle", "meaning": "Mt. Fuji side's"},
                    {"orig": "窓側で", "kana": "まどがわで", "romaji": "madogawa de", "pos": "Noun + Particle", "meaning": "On window side"},
                    {"orig": "お願いします。", "kana": "おねがいします", "romaji": "onegai shimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Ticket Class & Seat Selection Jargon",
                "sentence_ja": "京都までの指定席を、富士山側の窓側でお願いします。",
                "vocab": [
                    {"orig": "指定席", "kana": "していせき", "romaji": "shiteiseki", "pos": "Noun", "meaning": "Reserved seat"},
                    {"orig": "自由席", "kana": "じゆうせき", "romaji": "jiyuuseki", "pos": "Noun", "meaning": "Non-reserved seat"},
                    {"orig": "窓側", "kana": "まどがわ", "romaji": "madogawa", "pos": "Noun", "meaning": "Window seat"},
                    {"orig": "通路側", "kana": "つうろがわ", "romaji": "tsuurogawa", "pos": "Noun", "meaning": "Aisle seat"}
                ],
                "grammar_title": "Travel Formula: [Destination] までの [Seat Type] + [Seat Position] でお願いします",
                "grammar_bullets": [
                    ["1. Destination Connector:", "Place + までの (e.g. 京都までのきっぷ) describes tickets bound for a destination."],
                    ["2. Ticket Classes:", "普通車 (standard car), グリーン車 (Green Car luxury), グランクラス (Gran Class ultra-luxury)."],
                    ["3. Mt. Fuji View Rule:", "When riding from Tokyo towards Osaka/Kyoto, request '富士山側 (Seat E)' for stunning views."],
                    ["4. Large Luggage Rule:", "Suitcases with total dimensions over 160cm require a special '特大荷物スペースつき座席' reservation."]
                ],
                "teamwork_cues": [
                    {"speaker": "explainer", "text": "Here is how to book Shinkansen bullet train tickets at JR ticket counters and vending machines."},
                    {"speaker": "ja", "text": "指定席", "card_idx": 0},
                    {"speaker": "explainer", "text": "Noun: reserved numbered seating.", "card_idx": 0},
                    {"speaker": "ja", "text": "自由席", "card_idx": 1},
                    {"speaker": "explainer", "text": "Noun: non-reserved unassigned seating.", "card_idx": 1},
                    {"speaker": "ja", "text": "窓側", "card_idx": 2},
                    {"speaker": "explainer", "text": "Noun: window seat for scenic views.", "card_idx": 2},
                    {"speaker": "ja", "text": "通路側", "card_idx": 3},
                    {"speaker": "explainer", "text": "Noun: aisle seat for easy legroom and exit.", "card_idx": 3},
                    {"speaker": "explainer", "text": "Grammar Spotlight: specify tickets bound for a destination with made no.", "is_spotlight": True},
                    {"speaker": "ja", "text": "京都までの指定席を、富士山側の窓側でお願いします。", "is_spotlight": True},
                    {"speaker": "explainer", "text": "A reserved seat to Kyoto on the Mt. Fuji window side, please.", "is_spotlight": True}
                ]
            },
            {
                "type": "outro",
                "spoken_text": "Subscribe to TokyoFlow Japanese on YouTube and practice speech shadowing in the companion iOS App."
            }
        ],
        "shorts": {
            "hook_title": "BOOK SHINKANSEN TICKETS\nIN 30 SECONDS!",
            "hook_audio_en": "Here is how to get the best window seat with Mt. Fuji views on the Shinkansen bullet train!",
            "jp_sentence": "京都までの指定席、富士山側の窓側をお願いします。",
            "kana_sentence": "きょうとまでのしていせき、ふじさんがわのまどがわをおねがいします。",
            "romaji_sentence": "Kyouto made no shiteiseki, Fujisan-gawa no madogawa o onegai shimasu.",
            "en_translation": "Reserved seat to Kyoto with Mt. Fuji window view, please.",
            "tokens": [
                {"orig": "京都までの", "kana": "きょうとまでの", "romaji": "kyouto made no", "meaning": "To Kyoto"},
                {"orig": "指定席、", "kana": "していせき", "romaji": "shiteiseki,", "meaning": "Reserved seat,"},
                {"orig": "富士山側の", "kana": "ふじさんがわの", "romaji": "fujisan-gawa no", "meaning": "Mt. Fuji side"},
                {"orig": "窓側を", "kana": "まどがわを", "romaji": "madogawa o", "meaning": "Window seat"},
                {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu", "meaning": "Please"}
            ],
            "pro_tip_title": "SHINKANSEN PRO-TIP",
            "pro_tip_body": "Always ask for 'Fujisan-gawa' (Seat E) on Tokaido Shinkansen trains for breathtaking Mt. Fuji views!",
            "pro_tip_audio_en": "Ask for Seat E on the right side for clear views of Mt. Fuji.",
            "yt_short_title": "[JLPT N4] SH.19 How to Book Shinkansen Tickets with Mt. Fuji View #Shorts #LearnJapanese",
            "pinned_comment": "Have you ever seen Mt. Fuji from the window of a Shinkansen bullet train?"
        }
    }
]

# -------------------------------------------------------------------------
# BATCH EXECUTION RUNNER
# -------------------------------------------------------------------------
async def produce_all_english_batch():
    print("================================================================================")
    print("TokyoFlow Japanese • Production Sprint: EP.12 to EP.19 (English Edition)")
    print("Zero Emoji Discipline | Full HD 1080p Master Videos | 9:16 Interactive Shorts")
    print("================================================================================\n")

    for ep in BATCH_ENGLISH_EPISODES:
        ep_num = ep["episode_number"]
        folder_name = ep["folder_name"]
        release_dir = RELEASES_DIR / folder_name
        release_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(f"PRODUCING EP.{ep_num:02d}: {ep['title']} [{ep['release_date']} 08:00 AM EDT]")
        print(f"Target Directory: {release_dir}")
        print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

        # 1. Save Structured script.json
        script_file = release_dir / "script.json"
        with open(script_file, "w", encoding="utf-8") as fp:
            json.dump(ep, fp, indent=2, ensure_ascii=False)
        print(f"[OK] Saved script manifest: {script_file}")

        # 2. Produce 16:9 Long-Form Master Video & 16:9 Thumbnail
        print(f"\n--- [1/3] Generating 16:9 Long-Form Master Video & Cover ---")
        await produce_multilingual_episode(
            script_path=str(script_file),
            output_dir=str(release_dir),
            locale_code="en"
        )

        # 3. Produce 9:16 Interactive Shadowing Short & 9:16 Cover (First-Frame Cover Injected)
        print(f"\n--- [2/3] Generating 9:16 Interactive Shadowing Short Video ---")
        shorts_spec = ep["shorts"]
        shorts_spec["ep_num"] = ep_num
        shorts_spec["jlpt_level"] = ep["level"]
        shorts_spec["district"] = ep["district"]
        shorts_spec["category"] = ep["category"]

        # Generate Dedicated 9:16 Cover FIRST for video burning
        short_thumb_path = str(release_dir / "short_thumbnail.jpg")
        cover_dict = {
            "ep_num": ep_num,
            "sh_code": f"SH.{ep_num:02d}",
            "folder": folder_name,
            "hook_main": shorts_spec["hook_title"].split("\n")[0],
            "hook_sub": shorts_spec["hook_title"].split("\n")[1] if "\n" in shorts_spec["hook_title"] else "SURVIVAL JAPANESE",
            "jp_phrase": shorts_spec["jp_sentence"],
            "romaji": shorts_spec["romaji_sentence"],
            "en_meaning": shorts_spec["en_translation"],
            "accent_color": (225, 29, 72),
            "secondary_color": (250, 204, 21),
            "location": f"{ep['district']} • {ep['level']}",
            "bg_image_path": ep["bg_image"]
        }
        cover_img = create_shorts_cover(cover_dict)
        cover_img.save(short_thumb_path, "JPEG", quality=95)
        print(f"[OK] Saved 9:16 Short Cover: {short_thumb_path}")

        short_mp4 = str(release_dir / "short.mp4")
        short_tmp = str(PROJECT_ROOT / "tmp" / f"shorts_render_ep{ep_num:02d}")
        await generate_single_short_video(shorts_spec, short_mp4, short_tmp, short_thumb_path)

        # 4. Save Clean Metadata Files
        print(f"\n--- [3/3] Packaging Clean Metadata & Schedule Kits ---")
        meta_file = release_dir / "metadata.md"
        tokens_txt = "\n".join([f"- {t['orig']} ({t['kana']}) : {t.get('meaning', '')}" for t in ep['slides'][0]['tokens']])
        
        long_metadata_content = f"""# YouTube Release Manifest: EP.{ep_num:02d}

## Video Title
{ep['yt_title']}

## Video Description
Master real-life Tokyo Japanese survival phrases and grammar with TokyoFlow!

TIMESTAMPS AND CHAPTERS:
00:00 - 01. Real-Life Tokyo Immersion
00:08 - 02. Vocabulary & Grammar Breakdown
00:48 - 03. Cultural Insights & Pro-Tips
00:55 - 04. Shadowing Practice & Outro

KEY PHRASES COVERED:
- {ep['slides'][0]['spoken_text']} ({ep['slides'][0]['meaning']})

VOCABULARY BREAKDOWN:
{tokens_txt}

GRAMMAR SPOTLIGHT:
{ep['slides'][1]['grammar_title']}
{chr(10).join([f"- {b[0]} {b[1]}" for b in ep['slides'][1]['grammar_bullets']])}

RECOMMENDED PRACTICE:
Download TokyoFlow - Japanese Speaking on the iOS App Store to practice interactive speech shadowing with instant AI pitch accent scoring!

#TokyoFlow #LearnJapanese #JapaneseSpeaking #TokyoTravel #JLPT #JapaneseShadowing #{ep['slug']}
"""
        with open(meta_file, "w", encoding="utf-8") as fp:
            fp.write(long_metadata_content)

        short_meta_file = release_dir / "short_metadata.md"
        short_tokens_txt = "\n".join([f"- {t['orig']} ({t['kana']}) : {t.get('meaning', '')}" for t in shorts_spec['tokens']])
        
        short_metadata_content = f"""# YouTube Short Manifest: SH.{ep_num:02d}

## Short Title
{shorts_spec['yt_short_title']}

## Interactive Pinned Comment
{shorts_spec['pinned_comment']}

## Description
{shorts_spec['hook_title']}
Japanese Phrase: {shorts_spec['jp_sentence']} ({shorts_spec['romaji_sentence']})
English: {shorts_spec['en_translation']}
Rule: {shorts_spec['pro_tip_body']}

VOCABULARY:
{short_tokens_txt}

Practice interactive speech shadowing with instant pitch accent scoring on TokyoFlow - Japanese Speaking on iOS!

#Shorts #LearnJapanese #JapaneseSpeaking #TokyoFlow #Tokyo #JLPT #JapaneseShadowing #{ep['slug']}
"""
        with open(short_meta_file, "w", encoding="utf-8") as fp:
            fp.write(short_metadata_content)

        # 5. Save YouTube Schedule Kit
        schedule_kit = {
            "release_date": ep["release_date"],
            "episode_number": ep_num,
            "folder_name": folder_name,
            "topic": ep["title"],
            "jlpt_difficulty": ep["level"],
            "scheduled_time_est": ep["publish_time_est"],
            "notify_subscribers": True,
            "long_form_package": {
                "file": str(release_dir / "video.mp4"),
                "thumbnail": str(release_dir / "thumbnail.jpg"),
                "title": ep["yt_title"],
                "metadata_file": str(meta_file)
            },
            "shorts_package": {
                "file": str(release_dir / "short.mp4"),
                "thumbnail": str(release_dir / "short_thumbnail.jpg"),
                "title": shorts_spec["yt_short_title"],
                "metadata_file": str(short_meta_file),
                "pinned_comment": shorts_spec["pinned_comment"]
            }
        }
        with open(release_dir / "youtube_schedule_kit.json", "w", encoding="utf-8") as fp:
            json.dump(schedule_kit, fp, indent=2, ensure_ascii=False)

        print(f"[OK] Complete Package Packaged for EP.{ep_num:02d} in {release_dir}")

    print("\n================================================================================")
    print("ALL 8 ENGLISH PACKAGES (EP.12 TO EP.19) SUCCESSFULLY GENERATED!")
    print("Matches Schedule Through Oct 19. Ready for Daily Generation Starting Oct 20.")
    print("================================================================================\n")

if __name__ == "__main__":
    asyncio.run(produce_all_english_batch())
