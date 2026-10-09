#!/usr/bin/env python3
"""
TokyoFlow Japanese • Slide Designer & Follow-Along Video Renderer
Renders high-definition (1920x1080) slides with:
1. 3-Tier Typography (Kana above Kanji, Japanese Main Text, Romaji below Japanese, English meaning)
2. Millisecond-level word-by-word karaoke follow-along highlight (with anticipatory lead)
3. English-narrated Vocabulary & Grammar Breakdown Micro-lessons with Dynamic Card Follow-Along Highlighting
4. Fast 3-second Call to Action Outro Cards
5. Pixel-perfect UI alignment and emoji-safe typography
"""

import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def draw_top_brand_bar(draw: ImageDraw.Draw, width: int, chapter_title: str, ep_label: str):
    # Top Brand Ribbon (Pixel-locked at y=0..80)
    draw.rectangle([(0, 0), (width, 80)], fill=(15, 23, 42))
    font_brand = get_font(28)
    draw.text((60, 24), "TokyoFlow Japanese  |  Real-Life Tokyo Japanese Academy", fill=(255, 255, 255), font=font_brand)
    font_badge = get_font(22)
    badge_str = f"{ep_label} • {chapter_title}"
    bbox = draw.textbbox((0, 0), badge_str, font=font_badge)
    badge_w = bbox[2] - bbox[0]
    draw.text((width - badge_w - 60, 26), badge_str, fill=(244, 114, 182), font=font_badge)

def draw_category_pill(draw: ImageDraw.Draw, text: str, x: int = 120, y: int = 115) -> int:
    font_cat = get_font(22)
    bbox = draw.textbbox((0, 0), text, font=font_cat)
    text_w = bbox[2] - bbox[0]
    pill_w = max(240, text_w + 48)
    pill_h = 46
    draw.rounded_rectangle([(x, y), (x + pill_w, y + pill_h)], radius=12, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((x + 24, y + 10), text, fill=(79, 70, 229), font=font_cat)
    return pill_w

def prepare_16_9_background_canvas(bg_image_path: str = "", width: int = 1920, height: int = 1080) -> Image.Image:
    """Prepares an authentic scene photograph base canvas with cinematic dark gradient shading."""
    if bg_image_path and os.path.exists(bg_image_path):
        try:
            raw_img = Image.open(bg_image_path).convert("RGB")
            src_w, src_h = raw_img.size
            target_ratio = width / height
            src_ratio = src_w / src_h

            if src_ratio > target_ratio:
                new_w = int(src_h * target_ratio)
                center_x = int(src_w * 0.58)
                left = max(0, min(src_w - new_w, center_x - new_w // 2))
                raw_img = raw_img.crop((left, 0, left + new_w, src_h))
            else:
                new_h = int(src_w / target_ratio)
                top = max(0, (src_h - new_h) // 2)
                raw_img = raw_img.crop((0, top, src_w, top + new_h))

            base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
            base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
            base_img = ImageEnhance.Color(base_img).enhance(1.18)
        except Exception:
            base_img = Image.new("RGB", (width, height), (15, 23, 42))
    else:
        base_img = Image.new("RGB", (width, height), (15, 23, 42))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    draw_ov.rectangle([(0, 0), (width, height)], fill=(10, 15, 26, 130))

    for x in range(1200):
        rel = x / 1200.0
        alpha = int(140 * (0.5 * (1 + math.cos(rel * math.pi))))
        draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(180 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")

def render_follow_along_frame(
    tokens: list,
    category_label: str,
    title_label: str,
    english_meaning: str,
    pro_tip: str,
    current_time: float,
    chapter_label: str,
    ep_label: str,
    en_window: tuple = (0.0, 0.0),
    base_canvas: Image.Image = None
) -> Image.Image:
    width, height = 1920, 1080
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Top Ribbon
    draw_top_brand_bar(draw, width, chapter_label, ep_label)

    # 2. Category Pill & Title (Pixel-locked at y=115 and y=180)
    draw_category_pill(draw, category_label, x=120, y=115)
    title_font = get_font(36)
    draw.text((122, 182), title_label, fill=(10, 15, 26), font=title_font)
    draw.text((120, 180), title_label, fill=(254, 240, 138), font=title_font)

    # 3. Main 3-Tier Dialogue Card (Pixel-locked at y=250..695)
    card_x, card_y, card_w, card_h = 120, 250, width - 240, 445
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)

    font_jp = get_font(52)
    font_kana = get_font(26)
    font_romaji = get_font(28)

    # Measure token widths
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
        
        # Check active follow-along highlight
        is_active = (start_t <= current_time <= end_t) and (end_t > start_t)
        
        if is_active:
            # Active glowing gold capsule
            draw.rounded_rectangle([(curr_x + 2, y_kana - 12), (curr_x + w - 2, y_romaji + 46)], radius=16, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            # Active indicator dot
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 26), (dot_cx + 6, y_kana - 14)], fill=(220, 38, 38))
            color_kana = (180, 83, 9)
            color_jp = (15, 23, 42)
            color_romaji = (180, 83, 9)
        else:
            color_kana = (100, 116, 139)
            color_jp = (15, 23, 42)
            color_romaji = (71, 85, 105)

        # 1. Furigana / Kana (Top Row)
        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=font_kana)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=color_kana, font=font_kana)

        # 2. Main Japanese (Middle Row)
        jw = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=color_jp, font=font_jp)

        # 3. Romaji (Bottom Row)
        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=font_romaji)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=color_romaji, font=font_romaji)

        curr_x += w

    # Divider Line
    draw.line([(card_x + 50, card_y + 265), (card_x + card_w - 50, card_y + 265)], fill=(241, 245, 249), width=2)

    # 4. English Meaning (with active voice follow-along glow)
    is_en_active = (en_window[0] <= current_time <= en_window[1]) and (en_window[1] > 0)
    font_en = get_font(32)
    if is_en_active:
        draw.rounded_rectangle([(card_x + 35, card_y + 280), (card_x + card_w - 35, card_y + 350)], radius=14, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.ellipse([(card_x + 50, card_y + 305), (card_x + 64, card_y + 319)], fill=(99, 102, 241))
        draw.text((card_x + 78, card_y + 295), f"Meaning:  {english_meaning}", fill=(67, 56, 202), font=font_en)
    else:
        draw.text((card_x + 50, card_y + 295), f"Meaning:  {english_meaning}", fill=(30, 41, 59), font=font_en)

    # 5. Pro-Tip
    if pro_tip:
        font_tip = get_font(25)
        draw.text((card_x + 50, card_y + 365), f"[ PRO-TIP ]  {pro_tip}", fill=(16, 185, 129), font=font_tip)

    # 6. Bottom Shadowing Drill Banner
    draw.rounded_rectangle([(120, 735), (width - 120, 885)], radius=20, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    if is_en_active:
        draw.text((160, 770), "[ ENGLISH EXPLANATION ACTIVE ]  Andrew explaining English meaning & nuance", fill=(67, 56, 202), font=get_font(28))
        draw.text((160, 825), "Next: Shadowing Drill • Repeat aloud in Japanese with native timing", fill=(100, 116, 139), font=get_font(22))
    else:
        draw.text((160, 770), "[ SHADOWING DRILL ]  Repeat aloud with native timing & pitch accent", fill=(51, 65, 85), font=get_font(28))
        draw.text((160, 825), "Native Audio: Nanami (Tokyo Standard) • Millisecond Follow-Along Highlighting", fill=(100, 116, 139), font=get_font(22))

    return img

def render_breakdown_frame(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    category_label: str,
    chapter_label: str,
    ep_label: str,
    current_time: float = 0.0,
    timings: dict = None,
    base_canvas: Image.Image = None
) -> Image.Image:
    width, height = 1920, 1080
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw_top_brand_bar(draw, width, chapter_label, ep_label)

    # Category Pill & Title (Pixel-locked at y=115 and y=180)
    draw_category_pill(draw, "[ BREAKDOWN ]  Sentence Structure & Nuance", x=120, y=115)
    
    # Vocab Grid Cards (Top Half)
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

    # Sentence Bar (with active highlight during full sentence repeat)
    sent_font = get_font(34)
    if spotlight_active and active_vocab_idx is None:
        draw.rounded_rectangle([(110, 168), (width - 110, 222)], radius=12, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((124, 178), f"Sentence:  {sentence_ja}", fill=(67, 56, 202), font=sent_font)
    else:
        draw.text((122, 182), f"Sentence:  {sentence_ja}", fill=(10, 15, 26), font=sent_font)
        draw.text((120, 180), f"Sentence:  {sentence_ja}", fill=(254, 240, 138), font=sent_font)

    for i in range(num_cards):
        v = vocab_list[i]
        x = grid_x + i * (card_w + gap)
        y = grid_y
        is_active = (active_vocab_idx == i)

        if is_active:
            # Active highlighted card (Warm Gold / Blue Glow)
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=18, fill=(254, 249, 195), outline=(245, 158, 11), width=3)
            # Active Indicator Dot (Pinned cleanly to top edge)
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
        draw.text((x + 20, y + 20), v.get("pos", "Word"), fill=pos_color, font=get_font(17))

        # Japanese Main
        draw.text((x + 14, y + 54), v.get("orig", ""), fill=(15, 23, 42), font=get_font(30))

        # Kana & Romaji
        kana_ro = f"{v.get('kana', '')} • {v.get('romaji', '')}"
        draw.text((x + 14, y + 105), kana_ro, fill=kana_color, font=get_font(19))

        # Meaning
        draw.text((x + 14, y + 145), v.get("meaning", ""), fill=(51, 65, 85), font=get_font(20))

    # Grammar & Nuance Spotlight Card (Bottom Half)
    spot_x = 120
    spot_y = 510
    spot_w = width - 240
    spot_h = 375

    if spotlight_active:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(79, 70, 229), width=4)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(224, 231, 255))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR SPOTLIGHT ]  {grammar_title}", fill=(67, 56, 202), font=get_font(26))
    else:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(238, 242, 255))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR SPOTLIGHT ]  {grammar_title}", fill=(67, 56, 202), font=get_font(26))

    b_y = spot_y + 80
    for bullet in grammar_bullets:
        if isinstance(bullet, (list, tuple)) and len(bullet) >= 2:
            title, desc = bullet[0], bullet[1]
        elif isinstance(bullet, str) and ":" in bullet:
            parts = bullet.split(":", 1)
            title, desc = parts[0].strip(), parts[1].strip()
        else:
            title, desc = "• Rule", str(bullet)
        bullet_title_color = (220, 38, 38) if spotlight_active else (185, 28, 28)
        draw.text((spot_x + 30, b_y), title, fill=bullet_title_color, font=get_font(22))
        draw.text((spot_x + 330, b_y), desc, fill=(30, 41, 59), font=get_font(22))
        b_y += 62

    # Bottom App CTA
    draw.rounded_rectangle([(120, 915), (width - 120, 1020)], radius=18, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    draw.text((160, 945), "[ TOKYOFLOW ACADEMY ]  Practice interactive word drills & pitch accent scoring in the TokyoFlow iOS App!", fill=(51, 65, 85), font=get_font(25))

    return img

def render_outro_frame(ep_label: str, passcode: str = None, base_canvas: Image.Image = None, bg_image_path: str = "") -> Image.Image:
    width, height = 1920, 1080
    if base_canvas is None:
        if bg_image_path:
            base_canvas = prepare_16_9_background_canvas(bg_image_path)
        else:
            base_canvas = Image.new("RGB", (width, height), color=(15, 23, 42))

    img = base_canvas.copy()
    draw = ImageDraw.Draw(img)

    if not passcode:
        clean_ep = ep_label.upper().replace(".", "").replace("-", "").replace(" ", "")
        passcode = f"TOKYOFLOW-{clean_ep}"

    draw_top_brand_bar(draw, width, "Outro & Practice", ep_label)

    # Main Frosted Translucent Card
    card_x, card_y, card_w, card_h = 120, 140, width - 240, height - 240
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
    
    font_hero = get_font(44)
    draw.text((180, 180), "Subscribe to TokyoFlow Japanese on YouTube", fill=(220, 38, 38), font=font_hero)
    
    font_sub = get_font(28)
    draw.text((180, 245), "Learn Natural Tokyo Japanese Through Real-Life Scenarios", fill=(30, 41, 59), font=font_sub)
    
    # Feature Bullets
    font_bullets = get_font(23)
    draw.text((180, 315), "• Real Tokyo Life Scenarios (Transit, Kombini, Izakaya, Akiba...)", fill=(71, 85, 105), font=font_bullets)
    draw.text((180, 365), "• 14,000+ Native VoiceBank Audio & Pitch Accent Intonation Guides", fill=(71, 85, 105), font=font_bullets)
    draw.text((180, 415), "• 10,000+ JLPT N5-N1 Vocabulary & Interactive Drills", fill=(71, 85, 105), font=font_bullets)
    
    # Passcode Card Box
    draw.rounded_rectangle([(180, 485), (width - 180, 715)], radius=18, fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.rounded_rectangle([(180, 485), (width - 180, 545)], radius=18, fill=(253, 230, 138))
    draw.text((210, 502), "[ STUDY PASSCODE ]  OFFICIAL STUDY WORKBOOK UNLOCK CODE:", fill=(146, 64, 14), font=get_font(24))
    draw.text((210, 570), passcode, fill=(180, 83, 9), font=get_font(56))
    draw.text((210, 660), "Download full JLPT N5-N3 Study Workbook PDF in description with this code", fill=(13, 148, 136), font=get_font(22))

    # Bottom App CTA Card
    draw.rounded_rectangle([(180, 745), (width - 180, 890)], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=2)
    font_app = get_font(27)
    draw.text((210, 770), "[ iOS APP STORE ]  Download 'TokyoFlow - Japanese Speaking' Free on App Store", fill=(37, 99, 235), font=font_app)
    font_app_sub = get_font(22)
    draw.text((210, 830), "Pair with iOS App for Speech Shadowing Scoring, Kana Mastery & SRS Flashcards", fill=(100, 116, 139), font=font_app_sub)

    return img

def render_follow_along_video_clip(
    tokens: list,
    category_label: str,
    title_label: str,
    english_meaning: str,
    pro_tip: str,
    chapter_label: str,
    ep_label: str,
    audio_path: str,
    duration: float,
    out_mp4_path: str,
    fps: int = 30,
    en_window: tuple = (0.0, 0.0),
    base_canvas: Image.Image = None,
    bg_image_path: str = "",
    cover_frame: Image.Image = None
):
    total_duration = duration + 0.3
    total_frames = int(total_duration * fps)

    if base_canvas is None and bg_image_path:
        base_canvas = prepare_16_9_background_canvas(bg_image_path)

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
            # First-Frame Master Cover Injection: Frames 0..7 (~0.26s) use the exact 16:9 master cover
            if f_idx < 8 and cover_frame is not None:
                frame = cover_frame
            else:
                t = f_idx / fps
                frame = render_follow_along_frame(
                    tokens=tokens,
                    category_label=category_label,
                    title_label=title_label,
                    english_meaning=english_meaning,
                    pro_tip=pro_tip,
                    current_time=t,
                    chapter_label=chapter_label,
                    ep_label=ep_label,
                    en_window=en_window,
                    base_canvas=base_canvas
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

def render_breakdown_frame(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    category_label: str,
    chapter_label: str,
    ep_label: str,
    current_time: float = 0.0,
    timings: dict = None,
    base_canvas: Image.Image = None
) -> Image.Image:
    width, height = 1920, 1080
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # 1. Top Brand Ribbon
    draw_top_brand_bar(draw, width, chapter_label, ep_label)

    # 2. Category Pill & Title
    draw_category_pill(draw, category_label, x=120, y=115)
    
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

    # Sentence Bar (with active highlight during full sentence repeat)
    sent_font = get_font(34)
    if spotlight_active and active_vocab_idx is None:
        draw.rounded_rectangle([(110, 168), (width - 110, 222)], radius=12, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
        draw.text((124, 178), f"Sentence:  {sentence_ja}", fill=(67, 56, 202), font=sent_font)
    else:
        draw.text((122, 182), f"Sentence:  {sentence_ja}", fill=(10, 15, 26), font=sent_font)
        draw.text((120, 180), f"Sentence:  {sentence_ja}", fill=(254, 240, 138), font=sent_font)

    for i in range(num_cards):
        v = vocab_list[i]
        x = grid_x + i * (card_w + gap)
        y = grid_y
        is_active = (active_vocab_idx == i)

        if is_active:
            # Active highlighted card (Warm Gold / Blue Glow)
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=18, fill=(254, 249, 195), outline=(245, 158, 11), width=3)
            # Active Indicator Dot (Pinned cleanly to top edge)
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
        draw.text((x + 20, y + 20), v.get("pos", "Word"), fill=pos_color, font=get_font(17))

        # Japanese Main
        draw.text((x + 14, y + 54), v.get("orig", ""), fill=(15, 23, 42), font=get_font(30))

        # Kana & Romaji
        kana_ro = f"{v.get('kana', '')} • {v.get('romaji', '')}"
        draw.text((x + 14, y + 105), kana_ro, fill=kana_color, font=get_font(19))

        # Meaning
        draw.text((x + 14, y + 145), v.get("meaning", ""), fill=(51, 65, 85), font=get_font(20))

    # Grammar & Nuance Spotlight Card (Bottom Half)
    spot_x = 120
    spot_y = 510
    spot_w = width - 240
    spot_h = 375

    if spotlight_active:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(79, 70, 229), width=4)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(224, 231, 255))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR SPOTLIGHT ]  {grammar_title}", fill=(67, 56, 202), font=get_font(26))
    else:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=22, fill=(238, 242, 255))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR SPOTLIGHT ]  {grammar_title}", fill=(67, 56, 202), font=get_font(26))

    b_y = spot_y + 80
    for bullet in grammar_bullets:
        if isinstance(bullet, (list, tuple)) and len(bullet) >= 2:
            title, desc = bullet[0], bullet[1]
        elif isinstance(bullet, str) and ":" in bullet:
            parts = bullet.split(":", 1)
            title, desc = parts[0].strip(), parts[1].strip()
        else:
            title, desc = "• Rule", str(bullet)
        bullet_title_color = (220, 38, 38) if spotlight_active else (185, 28, 28)
        draw.text((spot_x + 30, b_y), title, fill=bullet_title_color, font=get_font(22))
        draw.text((spot_x + 330, b_y), desc, fill=(30, 41, 59), font=get_font(22))
        b_y += 62

    # Bottom Academy Banner
    draw.rounded_rectangle([(120, 915), (width - 120, 1020)], radius=18, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    draw.text((160, 945), "[ TOKYOFLOW JAPANESE ACADEMY ]  Real-life Tokyo Japanese immersion masterclass • Practice shadowing with native audio", fill=(51, 65, 85), font=get_font(25))

    return img

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
    fps: int = 30,
    base_canvas: Image.Image = None,
    bg_image_path: str = "",
    cover_frame: Image.Image = None
):
    total_duration = duration + 0.3
    total_frames = int(total_duration * fps)

    if base_canvas is None and bg_image_path:
        base_canvas = prepare_16_9_background_canvas(bg_image_path)

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
            # First-Frame Master Cover Injection: Frames 0..7 (~0.26s) use the exact 16:9 master cover
            if f_idx < 8 and cover_frame is not None:
                frame = cover_frame
            else:
                t = f_idx / fps
                frame = render_breakdown_frame(
                    sentence_ja=sentence_ja,
                    vocab_list=vocab_list,
                    grammar_title=grammar_title,
                    grammar_bullets=grammar_bullets,
                    category_label=category_label,
                    chapter_label=chapter_label,
                    ep_label=ep_label,
                    current_time=t,
                    timings=timings,
                    base_canvas=base_canvas
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

def render_news_broadcast_frame(
    bg_image_path: str,
    headline_ja: str,
    location_tag: str,
    current_time: float,
    ep_label: str = "EP.10"
) -> Image.Image:
    width, height = 1920, 1080
    if bg_image_path and os.path.exists(bg_image_path):
        base_img = Image.open(bg_image_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    else:
        base_img = Image.new("RGB", (width, height), (15, 23, 42))

    # Add cinematic dark overlays
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Top banner vignette
    for y in range(140):
        alpha = int(180 * (1.0 - (y / 140.0)))
        draw_ov.line([(0, y), (width, y)], fill=(5, 8, 16, alpha))
        
    # Bottom lower-third vignette
    for y in range(700, height):
        rel = (y - 700) / 380.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(3, 6, 14, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left Live Breaking News Capsule
    live_w, live_h = 360, 68
    live_x, live_y = 70, 45
    draw.rounded_rectangle([(live_x, live_y), (live_x + live_w, live_y + live_h)], radius=18, fill=(220, 38, 38), outline=(255, 255, 255), width=2)
    
    # Blinking Live Red Dot
    dot_color = (255, 255, 255) if int(current_time * 2) % 2 == 0 else (254, 202, 202)
    draw.ellipse([(live_x + 22, live_y + 24), (live_x + 42, live_y + 44)], fill=dot_color)
    
    font_live = get_font(30)
    draw.text((live_x + 56, live_y + 16), "LIVE ニュース速報", fill=(255, 255, 255), font=font_live)

    # 2. Top-Right Channel Bug
    font_bug = get_font(24)
    bug_str = f"TOKYO NEWS 24  |  {ep_label} LIVE"
    bbox_bug = draw.textbbox((0, 0), bug_str, font=font_bug)
    bw = bbox_bug[2] - bbox_bug[0]
    draw.rounded_rectangle([(width - bw - 110, live_y), (width - 70, live_y + live_h)], radius=18, fill=(15, 23, 42, 220), outline=(56, 189, 248), width=2)
    draw.text((width - bw - 90, live_y + 18), bug_str, fill=(255, 255, 255), font=font_bug)

    # 3. TV Broadcast Lower-Third Banner
    bar_x, bar_y, bar_w, bar_h = 70, 830, width - 140, 180
    draw.rounded_rectangle([(bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h)], radius=24, fill=(10, 15, 28, 235), outline=(51, 65, 85), width=3)
    
    # Red Accent "速報" Badge on the left
    badge_bw, badge_bh = 140, bar_h - 24
    draw.rounded_rectangle([(bar_x + 12, bar_y + 12), (bar_x + 12 + badge_bw, bar_y + 12 + badge_bh)], radius=16, fill=(225, 29, 72))
    font_soku = get_font(44)
    draw.text((bar_x + 36, bar_y + 52), "速報", fill=(255, 255, 255), font=font_soku)

    # Headline Text
    font_head = get_font(46)
    head_text = headline_ja
    bbox_h = draw.textbbox((0, 0), head_text, font=font_head)
    if (bbox_h[2] - bbox_h[0]) > (bar_w - 200):
        font_head = get_font(38)
    
    # Drop shadow
    for dx, dy in [(-2, 2), (2, 2), (0, 3)]:
        draw.text((bar_x + badge_bw + 35 + dx, bar_y + 35 + dy), head_text, fill=(0, 0, 0, 220), font=font_head)
    draw.text((bar_x + badge_bw + 35, bar_y + 35), head_text, fill=(255, 255, 255), font=font_head)

    # Sub-Ticker Line
    font_sub = get_font(24)
    tri_x = bar_x + badge_bw + 35
    tri_y = bar_y + 120
    draw.polygon([(tri_x, tri_y), (tri_x + 12, tri_y + 8), (tri_x, tri_y + 16)], fill=(56, 189, 248))
    ticker_text = f"{location_tag.upper()}  |  AUTHENTIC BROADCAST AUDIO & REAL NEWS IMMERSION"
    draw.text((tri_x + 22, bar_y + 115), ticker_text, fill=(56, 189, 248), font=font_sub)

    return img.convert("RGB")

def render_news_broadcast_video_clip(
    bg_image_path: str,
    headline_ja: str,
    location_tag: str,
    audio_path: str,
    duration: float,
    out_mp4_path: str,
    ep_label: str = "EP.10",
    fps: int = 30
):
    total_duration = duration + 0.2
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
            frame = render_news_broadcast_frame(
                bg_image_path=bg_image_path,
                headline_ja=headline_ja,
                location_tag=location_tag,
                current_time=t,
                ep_label=ep_label
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
