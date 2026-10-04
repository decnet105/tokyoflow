#!/usr/bin/env python3
"""
TokyoFlow Japanese Cinema Masterclass • 11-Second Viral Shorts Funnel Engine (WS.01)
=====================================================================================
Produces 9:16 vertical 1080x1920 high-conversion YouTube Short / Reel funnel video:
- Duration: Exactly 11.0 Seconds
- Phase 1 (0.0s - 3.2s): High-Tension Hook (Andrew EN) + "2.7m/s OR DIE?" 3D Visual
- Phase 2 (3.2s - 7.8s): Climax Soul Sentence + Real-Time Glowing Karaoke Follow-Along (Elena JA)
- Phase 3 (7.8s - 11.0s): High-Converting Funnel CTA to WL.01 Masterclass (Andrew EN)
"""

import os
import sys
import re
import math
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

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 11.0

# ==========================================
# 1. AUDIO SYNTHESIS FOR 11S FUNNEL
# ==========================================

async def synthesize_funnel_audio(out_mp3: str) -> dict:
    """Synthesizes perfectly timed 12.0-second 3-phase dual-voice audio with complete natural endings."""
    os.makedirs(os.path.dirname(out_mp3), exist_ok=True)
    
    tmp_p1 = out_mp3 + ".p1_hook.mp3"
    tmp_p2 = out_mp3 + ".p2_ja.mp3"
    tmp_p3 = out_mp3 + ".p3_cta.mp3"
    
    # 1. Hook (Andrew) - Fast & Urgent
    hook_text = "In Japan's biggest thriller, one sentence decides who lives or dies!"
    await edge_tts.Communicate(hook_text, "en-US-AndrewNeural", rate="+15%", pitch="+1Hz").save(tmp_p1)
    d1 = get_audio_duration(tmp_p1)
    
    # 2. Climax Japanese Soul Phrase (Elena / Nanami JA) - Native Cinema Clarity
    ja_text = "ベルトコンベアを止めるわけにはいきません。"
    await edge_tts.Communicate(ja_text, "ja-JP-NanamiNeural", rate="-6%", pitch="+2Hz").save(tmp_p2)
    d2 = get_audio_duration(tmp_p2)
    
    # 3. Funnel Callout to Long Video (Andrew) - Crisp & Natural with complete decay
    cta_text = "Master the full breakdown in the linked video below!"
    await edge_tts.Communicate(cta_text, "en-US-AndrewNeural", rate="+8%", pitch="+0Hz").save(tmp_p3)
    d3 = get_audio_duration(tmp_p3)
    
    target_total = 12.0
    gap = 0.2
    
    # Concat with FFmpeg into clean normalized stereo MP3 (12.0s)
    filter_complex = (
        f"[0:a]adelay=0|0[a0];"
        f"[1:a]adelay={int((d1 + gap)*1000)}|{int((d1 + gap)*1000)}[a1];"
        f"[2:a]adelay={int((d1 + d2 + gap*2)*1000)}|{int((d1 + d2 + gap*2)*1000)}[a2];"
        f"[a0][a1][a2]amix=inputs=3:duration=longest:dropout_transition=0[aout]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", tmp_p1,
        "-i", tmp_p2,
        "-i", tmp_p3,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-t", "12.0",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        out_mp3
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    for f in [tmp_p1, tmp_p2, tmp_p3]:
        if os.path.exists(f):
            os.remove(f)
            
    timings = {
        "hook_start": 0.0,
        "hook_end": d1,
        "ja_start": d1 + gap,
        "ja_end": d1 + gap + d2,
        "cta_start": d1 + gap + d2 + gap,
        "total_duration": 12.0
    }
    
    print(f" Funnel 12s Audio Synthesized: {out_mp3} (Hook: 0..{d1:.1f}s, JA: {timings['ja_start']:.1f}..{timings['ja_end']:.1f}s, CTA: {timings['cta_start']:.1f}..12.0s)")
    return timings

# ==========================================
# 2. VERTICAL 9:16 FRAME COMPOSITOR
# ==========================================

def render_vertical_funnel_frame(current_time: float, total_duration: float, timings: dict) -> Image.Image:
    """Renders 1080x1920 vertical transparent RGBA overlay for YouTube Shorts / Reels."""
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    ja_start = timings["ja_start"]
    ja_end = timings["ja_end"]
    cta_start = timings["cta_start"]
    
    is_hook = (current_time < ja_start)
    is_ja = (ja_start <= current_time < ja_end)
    is_cta = (current_time >= ja_end)
    
    # ----------------------------------------------------
    # TOP HEADER (y=50..220)
    # ----------------------------------------------------
    # Top Brand Ribbon
    draw.rounded_rectangle([(40, 50), (1040, 120)], radius=18, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=2)
    draw.text((65, 68), "TokyoFlow Japanese  •  Cinema Funnel", fill=(255, 255, 255), font=get_font(26))
    
    # Top-Right Badge
    draw.rounded_rectangle([(820, 60), (1020, 110)], radius=12, fill=(225, 29, 72))
    draw.text((842, 70), "WS.01 • N3", fill=(255, 255, 255), font=get_font(22))
    
    # Dynamic Phase Sub-Pill
    if is_hook:
        pill_txt = "[ 2024 BLOCKBUSTER HOOK ]  The Ultimate Logistics Crisis"
        pill_fill = (225, 29, 72)
    elif is_ja:
        pill_txt = "[ JAPANESE CINEMA GYM ]  Shadowing & Pitch Accent Drill"
        pill_fill = (245, 158, 11)
    else:
        pill_txt = "[ FULL MASTERCLASS AVAILABLE ]  25-Min Deep-Dive Breakdown"
        pill_fill = (37, 99, 235)
        
    draw.rounded_rectangle([(40, 140), (1040, 200)], radius=14, fill=(15, 23, 42, 230), outline=pill_fill, width=2)
    draw.text((65, 155), pill_txt, fill=(254, 240, 138), font=get_font(22))

    # ----------------------------------------------------
    # CENTER MOVIE FRAME CALLOUTS (y=230..1120)
    # ----------------------------------------------------
    # Character & Scene Title Bar (Over top of movie window)
    draw.rounded_rectangle([(40, 230), (520, 280)], radius=10, fill=(10, 15, 28, 220))
    draw.text((55, 242), "LAST MILE (2024)  •  満島ひかり", fill=(244, 114, 182), font=get_font(20))
    
    # ----------------------------------------------------
    # BOTTOM HUD (y=1140..1880) - DYNAMIC 3-STAGE CONTENT
    # ----------------------------------------------------
    hud_x, hud_y, hud_w, hud_h = 40, 1140, 1000, 720
    draw.rounded_rectangle([(hud_x, hud_y), (hud_x + hud_w, hud_y + hud_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=3)
    
    # 1. Header inside HUD
    draw.text((hud_x + 35, hud_y + 25), "[ CLIMAX SOUL PHRASE ]", fill=(56, 189, 248), font=get_font(24))
    draw.rounded_rectangle([(hud_x + hud_w - 260, hud_y + 20), (hud_x + hud_w - 30, hud_y + 60)], radius=10, fill=(225, 29, 72))
    draw.text((hud_x + hud_w - 245, hud_y + 27), "JLPT N3 ESSENTIAL", fill=(255, 255, 255), font=get_font(18))
    
    # Divider
    draw.line([(hud_x + 35, hud_y + 75), (hud_x + hud_w - 35, hud_y + 75)], fill=(51, 65, 85), width=2)
    
    # 2. Main Japanese Target Box with Real-time Glowing Follow-Along
    tokens = [
        {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea"},
        {"orig": "を", "kana": "を", "romaji": "o"},
        {"orig": "止める", "kana": "とめる", "romaji": "tomeru"},
        {"orig": "わけにはいきません", "kana": "わけにはいきません", "romaji": "wake ni wa ikimasen"}
    ]
    
    # Compute active token during JA phase
    active_idx = -1
    if is_ja:
        rel_t = current_time - ja_start
        dur_ja = ja_end - ja_start
        # distribute across 4 tokens: 0.35, 0.10, 0.20, 0.35
        weights = [0.35, 0.10, 0.20, 0.35]
        cum = 0.0
        for i, w in enumerate(weights):
            st = cum * dur_ja
            et = (cum + w) * dur_ja
            if st <= rel_t <= et:
                active_idx = i
                break
            cum += w
            
    # Draw Karaoke Tokens
    curr_x = hud_x + 35
    token_y_kana = hud_y + 95
    token_y_jp = hud_y + 135
    token_y_ro = hud_y + 200
    
    f_ka = get_font(20)
    f_jp = get_font(38)
    f_ro = get_font(20)
    
    for i, tok in enumerate(tokens):
        w_jp = draw.textbbox((0, 0), tok["orig"], font=f_jp)[2]
        w_ka = draw.textbbox((0, 0), tok["kana"], font=f_ka)[2]
        w_ro = draw.textbbox((0, 0), tok["romaji"], font=f_ro)[2]
        tok_w = max(w_jp, w_ka, w_ro) + 20
        
        is_active = (active_idx == i)
        
        if is_active:
            # Signature Glowing Gold Capsule
            draw.rounded_rectangle([(curr_x, token_y_kana - 8), (curr_x + tok_w, token_y_ro + 28)], radius=12, fill=(254, 240, 138), outline=(245, 158, 11), width=2)
            dot_cx = curr_x + tok_w // 2
            draw.ellipse([(dot_cx - 5, token_y_kana - 18), (dot_cx + 5, token_y_kana - 8)], fill=(220, 38, 38))
            c_ka, c_jp, c_ro = (180, 83, 9), (15, 23, 42), (180, 83, 9)
        else:
            c_ka, c_jp, c_ro = (148, 163, 184), (255, 255, 255), (148, 163, 184)
            
        kw = draw.textbbox((0, 0), tok["kana"], font=f_ka)[2]
        draw.text((curr_x + (tok_w - kw) // 2, token_y_kana), tok["kana"], fill=c_ka, font=f_ka)
        
        jw = draw.textbbox((0, 0), tok["orig"], font=f_jp)[2]
        draw.text((curr_x + (tok_w - jw) // 2, token_y_jp), tok["orig"], fill=c_jp, font=f_jp)
        
        rw = draw.textbbox((0, 0), tok["romaji"], font=f_ro)[2]
        draw.text((curr_x + (tok_w - rw) // 2, token_y_ro), tok["romaji"], fill=c_ro, font=f_ro)
        
        curr_x += tok_w + 10

    # 3. English Meaning Box
    draw.rounded_rectangle([(hud_x + 35, hud_y + 255), (hud_x + hud_w - 35, hud_y + 325)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    draw.text((hud_x + 55, hud_y + 275), 'Meaning:  "We cannot afford to stop the conveyor belt."', fill=(226, 232, 240), font=get_font(24))

    # 4. Grammar Spotlight Capsule
    draw.rounded_rectangle([(hud_x + 35, hud_y + 345), (hud_x + hud_w - 35, hud_y + 445)], radius=14, fill=(30, 41, 59, 230), outline=(244, 114, 182), width=2)
    draw.text((hud_x + 55, hud_y + 360), "[ JLPT N3 GRAMMAR ]  ~わけにはいかない", fill=(244, 114, 182), font=get_font(24))
    draw.text((hud_x + 55, hud_y + 400), "Cannot do due to moral, social, or corporate obligation", fill=(255, 255, 255), font=get_font(22))

    # 5. GIANT HIGH-CONVERSION FUNNEL CTA (y=1610..1820)
    cta_box_y = hud_y + 465
    if is_cta:
        # Pulsing Electric Gold & Cyan CTA Button
        draw.rounded_rectangle([(hud_x + 25, cta_box_y), (hud_x + hud_w - 25, cta_box_y + 215)], radius=18, fill=(225, 29, 72), outline=(254, 240, 138), width=3)
        draw.text((hud_x + 65, cta_box_y + 25), "WATCH FULL 25-MIN MASTERCLASS (WL.01)", fill=(255, 255, 255), font=get_font(30))
        draw.text((hud_x + 65, cta_box_y + 75), "Complete Scene Breakdown • 80+ Real Tokyo Phrases", fill=(254, 240, 138), font=get_font(23))
        
        # Link Indicator Pill
        draw.rounded_rectangle([(hud_x + 65, cta_box_y + 125), (hud_x + hud_w - 65, cta_box_y + 185)], radius=12, fill=(15, 23, 42))
        draw.text((hud_x + 110, cta_box_y + 140), " CLICK LINKED VIDEO BELOW ON SHORTS ", fill=(56, 189, 248), font=get_font(24))
    else:
        # Subtle Preview State
        draw.rounded_rectangle([(hud_x + 25, cta_box_y), (hud_x + hud_w - 25, cta_box_y + 215)], radius=18, fill=(15, 23, 42, 230), outline=(56, 189, 248), width=2)
        draw.text((hud_x + 65, cta_box_y + 35), "TokyoFlow Weekend Japanese Cinema Masterclass", fill=(244, 114, 182), font=get_font(24))
        draw.text((hud_x + 65, cta_box_y + 80), "Episode WL.01 • Last Mile (ラストマイル) Full Breakdown", fill=(255, 255, 255), font=get_font(26))
        draw.text((hud_x + 65, cta_box_y + 135), "Full 25-Minute Masterclass Linked Below", fill=(56, 189, 248), font=get_font(22))

    return img

# ==========================================
# 3. VERTICAL MASTERCLASS THUMBNAIL (9:16)
# ==========================================

def render_vertical_thumbnail(out_path: str):
    """Generates high-converting 9:16 vertical Shorts cover with 100% natural, un-distorted aspect ratio."""
    hero_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_path):
        hero_path = "tmp/videogen/character_heroes/elena_hero.jpg"
        
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), (10, 15, 28))
    
    if os.path.exists(hero_path):
        raw = Image.open(hero_path).convert("RGB")
        orig_w, orig_h = raw.size
        # Strict proportional scaling (scale by height=1120px): 100% authentic aspect ratio
        scale = 1120.0 / orig_h
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        scaled = raw.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Frame Elena naturally (Elena's face centered-right)
        paste_x = -760
        paste_y = 60
        img.paste(scaled, (paste_x, paste_y))
        
    # Top and Bottom dark vignettes & left fade
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    import math
    for x in range(width):
        if x < 480:
            rel = x / 480.0
            alpha = int(245 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 60), (x, 1180)], fill=(10, 15, 28, alpha))
            
    for y in range(950, 1200):
        rel = (y - 950) / 250.0
        alpha = int(255 * (rel ** 0.9))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))
        
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # 1. Top Brand Pill & Badge
    draw.rounded_rectangle([(40, 50), (450, 115)], radius=16, fill=(255, 255, 255))
    draw.text((65, 68), "TokyoFlow Cinema", fill=(225, 29, 72), font=get_font(28))
    
    draw.rounded_rectangle([(width - 340, 50), (width - 40, 115)], radius=16, fill=(225, 29, 72))
    draw.text((width - 315, 68), "WS.01 • JLPT N3", fill=(255, 255, 255), font=get_font(26))
    
    # 2. Hook Text (Left Column, cleanly framed)
    font_h = get_font(72)
    for dx in range(-4, 5, 2):
        for dy in range(-4, 5, 2):
            draw.text((50 + dx, 160 + dy), "2.7m/s", fill=(0, 0, 0), font=font_h)
            draw.text((50 + dx, 245 + dy), "OR DIE?", fill=(0, 0, 0), font=font_h)
    draw.text((50, 160), "2.7m/s", fill=(254, 240, 138), font=font_h)
    draw.text((50, 245), "OR DIE?", fill=(254, 240, 138), font=font_h)
    draw.text((50, 340), "LAST MILE (ラストマイル)", fill=(244, 114, 182), font=get_font(26))
    
    # 3. Climax Quote Box (Bottom)
    draw.rounded_rectangle([(40, 1180), (1040, 1840)], radius=24, fill=(10, 15, 28, 245), outline=(56, 189, 248), width=3)
    draw.text((70, 1220), "[ CLIMAX SOUL PHRASE ]", fill=(56, 189, 248), font=get_font(26))
    draw.text((70, 1280), "ベルトコンベアを", fill=(255, 255, 255), font=get_font(40))
    draw.text((70, 1340), "止めるわけにはいきません。", fill=(254, 240, 138), font=get_font(40))
    draw.text((70, 1430), "JLPT N3 Grammar: ~わけにはいかない", fill=(244, 114, 182), font=get_font(26))
    draw.text((70, 1475), '"We cannot afford to stop the conveyor belt."', fill=(226, 232, 240), font=get_font(24))
    draw.text((70, 1530), "Main Star: 満島ひかり (Hikari Mitsushima as Elena)", fill=(148, 163, 184), font=get_font(22))
    
    # 4. CTA Banner
    draw.rounded_rectangle([(70, 1630), (1010, 1790)], radius=18, fill=(225, 29, 72))
    draw.text((105, 1665), "WATCH FULL MASTERCLASS (WL.01)", fill=(255, 255, 255), font=get_font(30))
    draw.text((105, 1720), "25-Min Complete Breakdown Linked Below", fill=(254, 240, 138), font=get_font(22))
    
    img.save(out_path, quality=95)
    print(f" Saved Vertical Funnel Thumbnail: {out_path}")

# ==========================================
# 4. METADATA & SEO GENERATOR
# ==========================================

def generate_shorts_metadata(out_path: str):
    """Generates complete SEO metadata and funnel description for YouTube Shorts."""
    content = """# TokyoFlow Cinema • YouTube Shorts Funnel Specification (WS.01)

## Video Title
[JLPT N5-N2] WS.01 2.7m/s OR DIE? The Darkest Phrase in Japanese Cinema (Last Mile) #Shorts #LearnJapanese

## Funnel Link Configuration (CRITICAL)
- **Related Video (Linked Video)**: `[JLPT N5-N2] WL.01 Last Mile (ラストマイル) Full Breakdown | Learn Real Japanese Through Cinema`
- **Pinned Comment**:
```
Watch the FULL 25-Minute Cinema Masterclass (WL.01) here:
https://youtube.com/watch?v=YOUR_WL01_VIDEO_ID

Break down 80+ native phrases, pitch accent guides, and JLPT N5-N2 grammar patterns from 2024's biggest Japanese movie!
```

## Description
When packages start exploding across Tokyo on Black Friday, Elena Funado delivers the movie's most iconic line:
「ベルトコンベアを止めるわけにはいきません。」
(We cannot afford to stop the conveyor belt.)

Master the full scene-by-scene breakdown, corporate Japanese nuances, and JLPT N5-N2 grammar in our full 25-minute Weekend Masterclass (WL.01) linked on this Short!

#LastMile #ラストマイル #JapaneseCinema #LearnJapanese #JLPT #JLPTN3 #JapaneseListening #Shadowing #TokyoFlow
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f" Saved Shorts Funnel Metadata: {out_path}")

# ==========================================
# 5. FULL PRODUCTION PIPELINE (11 SECONDS)
# ==========================================

async def produce_funnel_short():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE CINEMA • 11-SECOND SHORTS FUNNEL PRODUCTION (WS.01)")
    print("================================================================================")
    
    out_dir = "output/cinema_masterclass/wl01_last_mile"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)
    
    audio_path = os.path.join(out_dir, "ws01_short_11s_audio.mp3")
    short_mp4_master = os.path.join(out_dir, "ws01_short_11s.mp4")
    short_mp4_published = "output/videos/tokyoflow_cinema_ws01_last_mile_short.mp4"
    thumb_path = os.path.join(out_dir, "ws01_thumbnail.jpg")
    meta_path = os.path.join(out_dir, "ws01_metadata.md")
    
    # 1. Generate Metadata & Thumbnail
    generate_shorts_metadata(meta_path)
    render_vertical_thumbnail(thumb_path)
    
    # 2. Synthesize Precise 11.0s Audio
    timings = await synthesize_funnel_audio(audio_path)
    
    # 3. Source Video: High-Tension Pure Last Mile Action Clip
    source_clip = "tmp/videogen/unique_movie_clips/seg_0_2.mp4"
    if not os.path.exists(source_clip):
        source_clip = "tmp/videogen/unique_movie_clips/seg_1_3_dialogue.mp4"
    if not os.path.exists(source_clip):
        source_clip = "tmp/videogen/last_mile_pure_sources/last_mile_main_trailer.mp4"
        
    fps = 30
    total_frames = int(12.0 * fps)
    
    print("\n Rendering 12-Second 9:16 Vertical Masterpiece (1080x1920)...")
    
    # FFmpeg compositing: [0:v] is scaled/cropped background movie, [1:v] is RGBA overlay pipe
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", source_clip,
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];[bg][1:v]overlay=0:0:shortest=1[v]",
        "-map", "[v]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", "12.0",
        short_mp4_master
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    try:
        for f_idx in range(total_frames):
            t = f_idx / fps
            frame = render_vertical_funnel_frame(current_time=t, total_duration=12.0, timings=timings)
            proc.stdin.write(frame.tobytes())
    except (BrokenPipeError, IOError):
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()
        
    import shutil
    shutil.copyfile(short_mp4_master, short_mp4_published)
    
    print("\n================================================================================")
    print(f" 12-SECOND SHORTS FUNNEL READY: {short_mp4_published}")
    print(f" Master Deliverable inside: {short_mp4_master}")
    print("================================================================================")

def main():
    asyncio.run(produce_funnel_short())

if __name__ == "__main__":
    main()
