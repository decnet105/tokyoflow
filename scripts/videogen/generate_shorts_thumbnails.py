#!/usr/bin/env python3
"""
TokyoFlow YouTube Shorts Thumbnail Designer (Golden Master Standard)
Generates minimalist, high-CTR, human-centric 9:16 vertical covers for all YouTube Shorts (SH.XX).
Adheres strictly to the TokyoFlow visual branding language (Zero emojis, high contrast, clean typography, glassmorphic card).
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
ASSETS_DIR = PROJECT_ROOT / "docs" / "youtube_assets" / "thumbnails"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def has_cjk(text: str) -> bool:
    return any(ord(c) > 0x2E80 for c in text)

def get_font(size: int, is_en: bool = False, text: str = ""):
    if is_en and text and not has_cjk(text):
        font_file = FONT_EN_HEAVY
    else:
        font_file = FONT_PATH
    try:
        return ImageFont.truetype(font_file, size)
    except Exception:
        return ImageFont.load_default()

def create_shorts_cover(item: dict) -> Image.Image:
    """Creates a 9:16 Golden Master Vertical Shorts Cover."""
    W, H = 1080, 1920
    bg_image_path = item.get("bg_image_path", "")
    
    if not (bg_image_path and os.path.exists(bg_image_path)) and item.get("folder"):
        cand = RELEASES_DIR / item["folder"] / "news_bg.jpg"
        if cand.exists():
            bg_image_path = str(cand)

    if not (bg_image_path and os.path.exists(bg_image_path)):
        scene_bg_dir = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds"
        ep_num = item.get("ep_num", 1)
        if scene_bg_dir.exists():
            for f in os.listdir(str(scene_bg_dir)):
                if f.startswith(f"E{ep_num:02d}") or f.startswith(f"E{ep_num}"):
                    bg_image_path = str(scene_bg_dir / f)
                    break
            if not (bg_image_path and os.path.exists(bg_image_path)):
                cand_sky = str(scene_bg_dir / "scene_tokyo_skyline.jpg")
                if os.path.exists(cand_sky):
                    bg_image_path = cand_sky

    # 1. Base Image Setup
    if bg_image_path and os.path.exists(bg_image_path):
        raw_img = Image.open(bg_image_path).convert("RGB")
        src_w, src_h = raw_img.size
        target_ratio = W / H
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

        base_img = raw_img.resize((W, H), Image.Resampling.LANCZOS)
        base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
        base_img = ImageEnhance.Color(base_img).enhance(1.18)
    else:
        base_img = Image.new("RGB", (W, H), (12, 17, 29))

    # 2. Dark Gradient Overlays
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    for y in range(540):
        rel = y / 540.0
        alpha = int(235 * (1.0 - (rel ** 1.3)))
        draw_ov.line([(0, y), (W, y)], fill=(8, 12, 24, alpha))
        
    for x in range(700):
        rel = x / 700.0
        alpha = int(200 * (1.0 - (rel ** 1.2)))
        draw_ov.line([(x, 0), (x, 560)], fill=(8, 12, 24, alpha))

    for y in range(1000, H):
        rel = (y - 1000) / (H - 1000.0)
        alpha = int(245 * (rel ** 0.8))
        draw_ov.line([(0, y), (W, y)], fill=(6, 10, 20, min(245, alpha)))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Top Header: TokyoFlow Brand Pill & Shorts Level Badge
    pill_w, pill_h = 390, 65
    draw.rounded_rectangle([(50, 50), (50 + pill_w, 50 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(28, is_en=True)
    bbox_b = draw.textbbox((0, 0), "TokyoFlow Japanese", font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((50 + (pill_w - bw) // 2, 50 + (pill_h - bh) // 2 - bbox_b[1]), "TokyoFlow Japanese", fill=(225, 29, 72), font=font_brand)

    level_str = item.get("jlpt_level", "JLPT N5")
    sh_code = f"{item.get('sh_code', 'SH.01')} • {level_str}"
    badge_w, badge_h = 310, 65
    badge_x = W - 50 - badge_w
    draw.rounded_rectangle([(badge_x, 50), (badge_x + badge_w, 50 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), sh_code, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 50 + (badge_h - gh) // 2 - bbox_bg[1]), sh_code, fill=(255, 255, 255), font=font_badge)

    # 4. Punchy 3D Action Hook
    hook_main = item.get("hook_main", "JAPAN TREND")
    hook_sub = item.get("hook_sub", "POP CULTURE")
    
    font_hook_sh = get_font(74)
    hy = 150
    hook_lines = [h.strip() for h in hook_main.split("\n") if h.strip()] if "\n" in hook_main else [hook_main]
    for line in hook_lines:
        for dx in range(-4, 5, 2):
            for dy in range(-4, 5, 2):
                draw.text((50 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook_sh)
        draw.text((50, hy), line, fill=(254, 240, 138), font=font_hook_sh)
        hy += 88

    # Pink Sub-Hook
    draw.text((55, hy + 5), hook_sub.upper(), fill=(244, 114, 182), font=get_font(28, is_en=True, text=hook_sub))

    # 5. Center/Bottom Learning Card
    card_x, card_y = 40, 1150
    card_w, card_h = 1000, 720
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=3)

    # Card Top Header
    draw.text((card_x + 35, card_y + 25), "[ TOKYO SURVIVAL GYM ]", fill=(56, 189, 248), font=get_font(24, is_en=True))
    draw.rounded_rectangle([(card_x + card_w - 240, card_y + 20), (card_x + card_w - 30, card_y + 62)], radius=10, fill=(225, 29, 72))
    draw.text((card_x + card_w - 225, card_y + 28), f"{level_str} ESSENTIAL", fill=(255, 255, 255), font=get_font(19, is_en=True))

    draw.line([(card_x + 35, card_y + 75), (card_x + card_w - 35, card_y + 75)], fill=(51, 65, 85), width=2)

    # Japanese Target Sentence
    full_jp = item.get("jp_phrase", "").strip()
    jp_size = 46
    font_jp = get_font(jp_size, text=full_jp)
    bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    while (bbox_jp[2] - bbox_jp[0]) > (card_w - 70) and jp_size > 34:
        jp_size -= 2
        font_jp = get_font(jp_size, text=full_jp)
        bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    draw.text((card_x + 35, card_y + 100), full_jp, fill=(255, 255, 255), font=font_jp)

    # Romaji
    draw.text((card_x + 35, card_y + 168), item.get("romaji", ""), fill=(254, 240, 138), font=get_font(25, is_en=True, text=item.get("romaji", "")))
    
    # English Translation
    en_meaning = item.get("en_meaning", "")
    en_clean = en_meaning if en_meaning.startswith('"') else f'"{en_meaning}"'
    draw.text((card_x + 35, card_y + 215), en_clean, fill=(226, 232, 240), font=get_font(25, is_en=True, text=en_clean))

    # Grammar Tag Pill inside card
    tag_clean = item.get("grammar_tag", f"{level_str} Spoken Japanese Pattern")
    draw.rounded_rectangle([(card_x + 35, card_y + 280), (card_x + card_w - 35, card_y + 345)], radius=12, fill=(15, 23, 42, 220), outline=(244, 114, 182), width=2)
    draw.text((card_x + 55, card_y + 298), tag_clean, fill=(244, 114, 182), font=get_font(21, text=tag_clean))

    # 6. CTA Action Banner at Bottom of Card
    cta_x = card_x + 30
    cta_y = card_y + 380
    cta_w = card_w - 60
    cta_h = 295
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=18, fill=(225, 29, 72))
    
    ep_num = item.get("ep_num", 1)
    ep_str = f"EP.{ep_num:02d}"
    draw.text((cta_x + 35, cta_y + 35), f"WATCH FULL BREAKDOWN ({ep_str})", fill=(255, 255, 255), font=get_font(34, is_en=True))
    draw.text((cta_x + 35, cta_y + 95), "Complete Vocabulary • Grammar Rules • Shadowing Gym", fill=(254, 240, 138), font=get_font(22, is_en=True))
    draw.text((cta_x + 35, cta_y + 145), f"Tap Related Video Below  •  TokyoFlow Japanese", fill=(241, 245, 249), font=get_font(20, is_en=True))

    return img
