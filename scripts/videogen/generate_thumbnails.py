#!/usr/bin/env python3
"""
TokyoFlow Japanese • Master Serialized Thumbnail & Cover Factory (16:9 & 9:16)
Unified, production-grade Golden Master implementation:
1. 16:9 Long-Form 4K/Full HD Master Covers (thumbnail.jpg, 1920x1080)
   - Authentic HD Tokyo photographic scene on right 55-60% with contrast/color boost.
   - Smooth non-linear cosine dark gradient fade on left (x < 1180).
   - Top-Left Solid White Brand Pill 'TokyoFlow Japanese' (Crimson text).
   - Top-Right Solid Crimson Capsule '[JLPT Level] • EP.XX'.
   - 96pt Giant 3D Solar Yellow Hook (#FEF08A) + Pink Sub-hook (#F472B6).
   - Glassmorphic Deep Navy Learning Card (#0A0F1C) with Sky Cyan Border (#38BDF8).
   - Full-Width Crimson Conversion Ribbon at bottom.
2. 9:16 Shorts High-CTR Vertical Covers (short_thumbnail.jpg, 1080x1920)
   - Full-bleed authentic real photo from top to bottom.
   - Top-Left White Brand Pill + Top-Right Crimson Badge ('SH.XX • [JLPT Level]').
   - 74pt 3D Solar Yellow Hook + Pink Sub-hook.
   - Deep Navy Glassmorphic Learning Card (#0A0F1C) with Sky Cyan Border.
   - Full-Width Crimson CTA Action Banner ('WATCH FULL BREAKDOWN (EP.XX)').
"""

import os
import sys
import glob
import json
import math
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
ASSETS_DIR = PROJECT_ROOT / "docs" / "youtube_assets" / "thumbnails"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_PATH if not is_en else FONT_EN_HEAVY
    try:
        return ImageFont.truetype(font_file, size)
    except Exception:
        return ImageFont.load_default()

def get_heavy_hook_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

# -------------------------------------------------------------------------
# 1. 16:9 Long-Form YouTube Golden Master Thumbnail Generator (1920x1080)
# -------------------------------------------------------------------------
def generate_serialized_thumbnail(
    ep_num: int,
    english_hook: str,
    japanese_key_phrase: str,
    bottom_tag: str,
    bg_image_path: str,
    output_path: str,
    jlpt_level: str = "JLPT N5",
    sub_hook: str = "REAL JAPANESE BREAKDOWN",
    grammar_tag: str = "",
    en_translation: str = "",
    context_note: str = "",
    location_tag: str = ""
):
    width, height = 1920, 1080
    
    # 1. Background Image Loading & Proportional Crop
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

    # 2. Smooth Left-to-Right Cosine Dark Gradient & Bottom Vignette
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    for x in range(width):
        if x < 1180:
            rel = x / 1180.0
            alpha = int(245 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Top-Left Brand Pill
    pill_w, pill_h = 360, 60
    draw.rounded_rectangle([(60, 45), (60 + pill_w, 45 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(26, is_en=True)
    bbox_b = draw.textbbox((0, 0), "TokyoFlow Japanese", font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((60 + (pill_w - bw) // 2, 45 + (pill_h - bh) // 2 - bbox_b[1]), "TokyoFlow Japanese", fill=(225, 29, 72), font=font_brand)

    # 4. Top-Right Level & Episode Badge
    ep_str = f"EP.{ep_num:02d}"
    jlpt_badge = f"{jlpt_level} • {ep_str}"
    badge_w, badge_h = 290, 60
    badge_x = width - 60 - badge_w
    draw.rounded_rectangle([(badge_x, 45), (badge_x + badge_w, 45 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), jlpt_badge, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 45 + (badge_h - gh) // 2 - bbox_bg[1]), jlpt_badge, fill=(255, 255, 255), font=font_badge)

    # 5. Giant 3D Yellow Hook Stack (Left Aligned)
    hook_words = [w.strip() for w in english_hook.replace("\n", " ").split(" ") if w.strip()]
    if len(hook_words) == 1:
        hook_lines = [hook_words[0], "IN TOKYO?!"]
    elif len(hook_words) == 2:
        hook_lines = [hook_words[0], hook_words[1]]
    elif len(hook_words) == 3:
        hook_lines = [hook_words[0], f"{hook_words[1]} {hook_words[2]}"]
    else:
        hook_lines = [" ".join(hook_words[:2]), " ".join(hook_words[2:4])]

    font_hook = get_heavy_hook_font(96)
    hy = 145
    for line in hook_lines:
        for dx in range(-5, 6, 2):
            for dy in range(-5, 6, 2):
                draw.text((60 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 112

    # Pink Sub-Hook
    clean_sub_hook = sub_hook.upper() if sub_hook else "POP CULTURE TREND"
    draw.text((65, 385), clean_sub_hook, fill=(244, 114, 182), font=get_font(34, is_en=True))

    # 6. Japanese Learning Card (Glassmorphic dark navy with Sky Cyan border)
    quote_box_w = 860
    quote_box_y = 450
    draw.rounded_rectangle([(60, quote_box_y), (60 + quote_box_w, quote_box_y + 410)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    
    draw.text((90, quote_box_y + 25), "[ REAL TOKYO JAPANESE BREAKDOWN ]", fill=(56, 189, 248), font=get_font(22, is_en=True))
    
    # Japanese Text Split
    jp_full = japanese_key_phrase.strip()
    if len(jp_full) > 14 and ("、" in jp_full or " " in jp_full or "が" in jp_full):
        if "、" in jp_full:
            parts = jp_full.split("、", 1)
            jp_l1, jp_l2 = parts[0] + "、", parts[1]
        elif " " in jp_full:
            parts = jp_full.split(" ", 1)
            jp_l1, jp_l2 = parts[0], parts[1]
        else:
            mid = len(jp_full) // 2
            jp_l1, jp_l2 = jp_full[:mid], jp_full[mid:]
    else:
        jp_l1, jp_l2 = jp_full, ""

    font_jp = get_font(38)
    draw.text((90, quote_box_y + 70), jp_l1, fill=(255, 255, 255), font=font_jp)
    if jp_l2:
        draw.text((90, quote_box_y + 125), jp_l2, fill=(254, 240, 138), font=font_jp)
        text_offset_y = 0
    else:
        text_offset_y = -35
    
    tag_str = grammar_tag if grammar_tag else f"{jlpt_level} Grammar • Key Pattern"
    draw.text((90, quote_box_y + 200 + text_offset_y), tag_str, fill=(244, 114, 182), font=get_font(23))
    
    en_str = en_translation if en_translation else f'"{english_hook.title()}"'
    draw.text((90, quote_box_y + 245 + text_offset_y), en_str, fill=(226, 232, 240), font=get_font(24, is_en=True))
    
    note_str = context_note if context_note else f"Daily spoken Tokyo Japanese for real situations"
    draw.text((90, quote_box_y + 300 + text_offset_y), note_str, fill=(148, 163, 184), font=get_font(20, is_en=True))
    
    loc_str = location_tag if location_tag else f"Setting: Tokyo, Japan • {jlpt_level} Mastery"
    draw.text((90, quote_box_y + 345 + text_offset_y), loc_str, fill=(56, 189, 248), font=get_font(20, is_en=True))

    # 7. Full-Width Crimson Conversion Ribbon
    draw.rounded_rectangle([(60, height - 120), (width - 60, height - 45)], radius=16, fill=(225, 29, 72))
    ribbon_txt = " 100% NATIVE TOKYO AUDIO  •  SHADOWING PRACTICE  •  FULL VOCAB & GRAMMAR BREAKDOWN"
    font_ribbon = get_font(24, is_en=True)
    bbox_rb = draw.textbbox((0, 0), ribbon_txt, font=font_ribbon)
    rw, rh = bbox_rb[2] - bbox_rb[0], bbox_rb[3] - bbox_rb[1]
    draw.text((60 + (width - 120 - rw) // 2, height - 120 + (75 - rh) // 2 - bbox_rb[1]), ribbon_txt, fill=(255, 255, 255), font=font_ribbon)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"✓ Master 16:9 Long-Form Thumbnail generated: {output_path}")

# -------------------------------------------------------------------------
# 2. 9:16 Shorts Vertical Golden Master Generator (1080x1920)
# -------------------------------------------------------------------------
def generate_shorts_thumbnail(
    ep_num: int,
    english_hook: str,
    japanese_sentence: str,
    kana_sentence: str,
    romaji_sentence: str,
    en_translation: str,
    output_path: str,
    category_theme: str = "anime",
    jlpt_level: str = "JLPT N5",
    bg_image_path: str = "",
    sub_hook: str = "",
    grammar_tag: str = ""
):
    width, height = 1080, 1920
    
    if bg_image_path and os.path.exists(bg_image_path):
        raw_img = Image.open(bg_image_path).convert("RGB")
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
            top = (src_h - new_h) // 2
            raw_img = raw_img.crop((0, top, src_w, top + new_h))
            
        base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
        base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
        base_img = ImageEnhance.Color(base_img).enhance(1.18)
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Top Gradient for Badges and Hook
    for y in range(540):
        rel = y / 540.0
        alpha = int(235 * (1.0 - (rel ** 1.3)))
        draw_ov.line([(0, y), (width, y)], fill=(8, 12, 24, alpha))
        
    # Left Gradient for Hook Text
    for x in range(700):
        rel = x / 700.0
        alpha = int(200 * (1.0 - (rel ** 1.2)))
        draw_ov.line([(x, 0), (x, 560)], fill=(8, 12, 24, alpha))

    # Smooth Bottom transition to card
    for y in range(1000, height):
        rel = (y - 1000) / (height - 1000.0)
        alpha = int(245 * (rel ** 0.8))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 20, min(245, alpha)))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top Header: TokyoFlow Brand Pill & Shorts Level Badge
    pill_w, pill_h = 390, 65
    draw.rounded_rectangle([(50, 50), (50 + pill_w, 50 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(28, is_en=True)
    bbox_b = draw.textbbox((0, 0), "TokyoFlow Japanese", font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((50 + (pill_w - bw) // 2, 50 + (pill_h - bh) // 2 - bbox_b[1]), "TokyoFlow Japanese", fill=(225, 29, 72), font=font_brand)

    sh_code = f"SH.{ep_num:02d} • {jlpt_level}"
    badge_w, badge_h = 310, 65
    badge_x = width - 50 - badge_w
    draw.rounded_rectangle([(badge_x, 50), (badge_x + badge_w, 50 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), sh_code, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 50 + (badge_h - gh) // 2 - bbox_bg[1]), sh_code, fill=(255, 255, 255), font=font_badge)

    # 2. Punchy 3D Action Hook
    hook_words = [w.strip() for w in english_hook.replace("\n", " ").split(" ") if w.strip()]
    if len(hook_words) >= 2:
        hook_lines = [" ".join(hook_words[:2]), " ".join(hook_words[2:])] if len(hook_words) > 2 else hook_words
    elif len(hook_words) == 1:
        hook_lines = [hook_words[0], "IN TOKYO?!"]
    else:
        hook_lines = ["JAPAN TREND", "IN TOKYO?!"]

    font_hook_sh = get_heavy_hook_font(74)
    hy = 150
    for line in hook_lines:
        for dx in range(-4, 5, 2):
            for dy in range(-4, 5, 2):
                draw.text((50 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook_sh)
        draw.text((50, hy), line, fill=(254, 240, 138), font=font_hook_sh)
        hy += 88

    # Pink Sub-Hook
    clean_sub = sub_hook.upper() if sub_hook else "POP CULTURE TREND"
    draw.text((55, hy + 5), clean_sub, fill=(244, 114, 182), font=get_font(28, is_en=True))

    # 3. Center/Bottom Learning Card (Glassmorphic container)
    card_x, card_y = 40, 1150
    card_w, card_h = 1000, 720
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=3)

    # Card Top Header
    draw.text((card_x + 35, card_y + 25), "[ TOKYO SURVIVAL GYM ]", fill=(56, 189, 248), font=get_font(24, is_en=True))
    draw.rounded_rectangle([(card_x + card_w - 240, card_y + 20), (card_x + card_w - 30, card_y + 62)], radius=10, fill=(225, 29, 72))
    draw.text((card_x + card_w - 225, card_y + 28), f"{jlpt_level} ESSENTIAL", fill=(255, 255, 255), font=get_font(19, is_en=True))

    draw.line([(card_x + 35, card_y + 75), (card_x + card_w - 35, card_y + 75)], fill=(51, 65, 85), width=2)

    # Japanese Target Sentence
    full_jp = japanese_sentence.strip()
    jp_size = 46
    font_jp = get_font(jp_size)
    bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    while (bbox_jp[2] - bbox_jp[0]) > (card_w - 70) and jp_size > 34:
        jp_size -= 2
        font_jp = get_font(jp_size)
        bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    draw.text((card_x + 35, card_y + 100), full_jp, fill=(255, 255, 255), font=font_jp)

    # Romaji
    draw.text((card_x + 35, card_y + 168), romaji_sentence, fill=(254, 240, 138), font=get_font(25, is_en=True))
    
    # English Translation
    en_clean = en_translation if en_translation.startswith('"') else f'"{en_translation}"'
    draw.text((card_x + 35, card_y + 215), en_clean, fill=(226, 232, 240), font=get_font(25, is_en=True))

    # Grammar Tag Pill inside card
    tag_clean = grammar_tag if grammar_tag else f"{jlpt_level} Spoken Japanese Pattern"
    draw.rounded_rectangle([(card_x + 35, card_y + 280), (card_x + card_w - 35, card_y + 345)], radius=12, fill=(15, 23, 42, 220), outline=(244, 114, 182), width=2)
    draw.text((card_x + 55, card_y + 298), tag_clean, fill=(244, 114, 182), font=get_font(21))

    # 4. CTA Action Banner at Bottom of Card
    cta_x = card_x + 30
    cta_y = card_y + 380
    cta_w = card_w - 60
    cta_h = 295
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=18, fill=(225, 29, 72))
    
    ep_str = f"EP.{ep_num:02d}"
    draw.text((cta_x + 35, cta_y + 35), f"WATCH FULL BREAKDOWN ({ep_str})", fill=(255, 255, 255), font=get_font(34, is_en=True))
    draw.text((cta_x + 35, cta_y + 95), "Complete Vocabulary • Grammar Rules • Shadowing Gym", fill=(254, 240, 138), font=get_font(22, is_en=True))
    draw.text((cta_x + 35, cta_y + 145), f"Tap Related Video Below  •  TokyoFlow Japanese", fill=(241, 245, 249), font=get_font(20, is_en=True))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"✓ Master 9:16 Shorts Cover generated: {output_path}")

# -------------------------------------------------------------------------
# Standalone CLI Runner (Processes Single Release or All Releases)
# -------------------------------------------------------------------------
def process_release_dir(rdir: str, sh_num: int = None):
    rdir_path = Path(rdir)
    if not rdir_path.exists():
        print(f"Directory not found: {rdir}")
        return
        
    dir_name = rdir_path.name
    try:
        ep_num = int(dir_name.split("-")[0].replace("E", "").replace("tokyoflow_v", ""))
    except Exception:
        ep_num = 1
        
    if sh_num is None:
        if ep_num == 13 or "E13" in dir_name:
            sh_num = 9
        else:
            sh_num = ep_num

    out_16_9 = str(rdir_path / "thumbnail.jpg")
    out_9_16 = str(rdir_path / "short_thumbnail.jpg")
    
    # Priority for base image:
    # 1. news_bg.jpg (High-res realistic photo)
    # 2. hero_16_9.jpg / hero_female_vert.jpg
    # 3. master asset in ASSETS_DIR
    bg_16_9 = ""
    bg_9_16 = ""
    
    news_bg = rdir_path / "news_bg.jpg"
    hero_16_9 = rdir_path / "hero_16_9.jpg"
    hero_9_16 = rdir_path / "hero_female_vert.jpg" or rdir_path / "hero_9_16.jpg"
    
    if hero_16_9.exists():
        bg_16_9 = str(hero_16_9)
    elif news_bg.exists():
        bg_16_9 = str(news_bg)
        
    if hero_9_16.exists():
        bg_9_16 = str(hero_9_16)
    elif news_bg.exists():
        bg_9_16 = str(news_bg)

    # Read manifest data
    spec_file = rdir_path / "production_spec.json"
    script_file = rdir_path / "script.json"
    
    if spec_file.exists():
        with open(spec_file) as fp:
            spec = json.load(fp)
        long_spec = spec.get("long_form", {})
        shorts_spec = spec.get("shorts", {})
        level = spec.get("target_jlpt_level", "JLPT N5")
        
        hook = long_spec.get("english_hook", "JAPAN TREND")
        jp = long_spec.get("japanese_key_phrase", spec.get("topic_title", "日本トレンド"))
        sub_hook = long_spec.get("sub_hook", "POP CULTURE TREND")
        grammar_tag = long_spec.get("grammar_point", f"{level} Grammar")
        en_trans = long_spec.get("en_translation", "")
        context = long_spec.get("context_note", "")
        location = long_spec.get("location_tag", "Tokyo, Japan")
        
        # 16:9 Cover
        generate_serialized_thumbnail(
            ep_num=ep_num,
            english_hook=hook,
            japanese_key_phrase=jp,
            bottom_tag=f"[{level}] Native Audio",
            bg_image_path=bg_16_9,
            output_path=out_16_9,
            jlpt_level=level,
            sub_hook=sub_hook,
            grammar_tag=grammar_tag,
            en_translation=en_trans,
            context_note=context,
            location_tag=location
        )
        
        # 9:16 Shorts Cover
        sh_hook = shorts_spec.get("hook_title", hook)
        sh_jp = shorts_spec.get("jp_sentence", jp)
        sh_kana = shorts_spec.get("kana_sentence", "")
        sh_romaji = shorts_spec.get("romaji_sentence", "")
        sh_en = shorts_spec.get("en_translation", en_trans)
        
        generate_shorts_thumbnail(
            ep_num=sh_num,
            english_hook=sh_hook,
            japanese_sentence=sh_jp,
            kana_sentence=sh_kana,
            romaji_sentence=sh_romaji,
            en_translation=sh_en,
            output_path=out_9_16,
            category_theme="anime",
            jlpt_level=level,
            bg_image_path=bg_9_16,
            sub_hook=sub_hook,
            grammar_tag=grammar_tag
        )
    elif script_file.exists():
        with open(script_file) as fp:
            data = json.load(fp)
        hook = data.get("cover", {}).get("hook", "TOKYO LESSON")
        jp = data.get("cover", {}).get("jp", "まもなく参ります")
        level = data.get("level", "JLPT N5")
        
        generate_serialized_thumbnail(
            ep_num=ep_num,
            english_hook=hook,
            japanese_key_phrase=jp,
            bottom_tag=f"[{level}] Native Audio",
            bg_image_path=bg_16_9,
            output_path=out_16_9,
            jlpt_level=level
        )
        
        first_slide = data.get("slides", [{}])[0]
        jp_sent = first_slide.get("spoken_text", jp)
        romaji_sent = " ".join([t.get("romaji", "") for t in first_slide.get("tokens", [])]).strip()
        kana_sent = " ".join([t.get("kana", "") for t in first_slide.get("tokens", [])]).strip()
        en_trans = first_slide.get("en", "Master Japanese in Tokyo")
        
        generate_shorts_thumbnail(
            ep_num=sh_num,
            english_hook=hook,
            japanese_sentence=jp_sent,
            kana_sentence=kana_sent,
            romaji_sentence=romaji_sent,
            en_translation=en_trans,
            output_path=out_9_16,
            category_theme="anime",
            jlpt_level=level,
            bg_image_path=bg_9_16
        )
    print(f"✅ Finished updating cover for {dir_name} (Short: SH.{sh_num:02d})")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TokyoFlow Master Thumbnail Factory")
    parser.add_argument("--dir", type=str, help="Target release directory to process")
    parser.add_argument("--episode", type=int, help="Episode number to process (e.g. 10)")
    parser.add_argument("--sh-num", type=int, help="Sequential Shorts number (e.g. 10 for SH.10)")
    parser.add_argument("--all", action="store_true", help="Explicitly process all release directories")

    args = parser.parse_args()

    if args.dir:
        process_release_dir(args.dir, sh_num=args.sh_num)
    elif args.episode:
        matches = glob.glob(f"docs/youtube_releases/E{args.episode:02d}*") or glob.glob(f"docs/youtube_releases/E{args.episode}*")
        if matches:
            for m in matches:
                process_release_dir(m, sh_num=args.sh_num)
        else:
            print(f"No release directory found for Episode {args.episode}")
    elif args.all:
        release_dirs = sorted(glob.glob("docs/youtube_releases/E*"))
        for rdir in release_dirs:
            process_release_dir(rdir)
        print("✅ All release thumbnails synchronized!")
    else:
        # Default single target: latest release (E11)
        latest_dir = "docs/youtube_releases/E11-shabuya-robot-drama-v1.0"
        if os.path.exists(latest_dir):
            print(f"ℹ️ No flags passed. Running incremental single-target on latest release: {latest_dir}")
            process_release_dir(latest_dir, sh_num=11)
        else:
            print("Please specify --dir <PATH>, --episode <NUM>, or --all")
