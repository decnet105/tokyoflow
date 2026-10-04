#!/usr/bin/env python3
"""
TokyoFlow Japanese • YouTube Channel Banner Factory (2560x1440)
Full-Bleed Distant Tokyo Tower Panorama (Golden Master):
- 2560x1440 full-bleed continuous photography edge-to-edge (zero black borders)
- Ultra-wide high-altitude vantage point showing Mount Fuji, Tokyo Bay, and complete Tokyo Tower
- Entire Tokyo Tower (antenna tip to base) framed inside Desktop viewing band (Y: 508..932)
- Warm Amber / Golden Sunset lighting & rich metropolis glow
- Left-aligned clean Frosted Glass Hero Container
- Solid White Brand Pill 'TokyoFlow Japanese' (Crimson text) + Official App Icon
- Solid Crimson Capsule 'JLPT N5-N1 • TOKYO FLUENCY'
- 3D Solar Yellow Hook (#FEF08A) + Neon Pink Sub-hook (#F472B6)
- Japanese Tagline + Compact Crimson Schedule Ribbon
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "docs" / "youtube_assets"
BACKGROUNDS_DIR = ASSETS_DIR / "scene_backgrounds"

FONT_JP_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(FONT_EN_HEAVY):
    FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_EN_HEAVY if is_en else FONT_JP_PATH
    try:
        return ImageFont.truetype(font_file, size)
    except Exception:
        try:
            return ImageFont.truetype(FONT_JP_PATH, size)
        except Exception:
            return ImageFont.load_default()

def get_heavy_hook_font(size: int):
    try:
        return ImageFont.truetype(FONT_EN_HEAVY, size)
    except Exception:
        return get_font(size, is_en=True)

def generate_channel_banner(output_paths=None):
    width, height = 2560, 1440
    
    # ---------------------------------------------------------
    # 1. Base Image Loading (Full-Bleed Distant 4K Tokyo Panorama)
    # ---------------------------------------------------------
    bg_path = BACKGROUNDS_DIR / "scene_tokyo_skyline_distant_4k.jpg"
    if not bg_path.exists():
        bg_path = BACKGROUNDS_DIR / "scene_tokyo_skyline_wide.jpg"
        
    raw = Image.open(bg_path).convert("RGB")
    src_w, src_h = raw.size # 1376 x 768
    
    # Scale and vertically frame so Tokyo Tower (spire y=335, base y=560 in 768p)
    # lands with its entire height within the central Desktop band (Y: 508..932)
    crop_top = 58
    crop_raw = raw.crop((0, crop_top, src_w, src_h))
    
    base_img = crop_raw.resize((width, height), Image.Resampling.LANCZOS)
    base_img = ImageEnhance.Contrast(base_img).enhance(1.10)
    base_img = ImageEnhance.Color(base_img).enhance(1.18)

    # ---------------------------------------------------------
    # 2. TV Edge Atmospheric Soft Vignette
    # (Soft, gentle shading only at extreme TV edges, full-bleed continuous photo)
    # ---------------------------------------------------------
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    for y in range(260):
        rel = (260 - y) / 260.0
        alpha = int(100 * (rel ** 1.5))
        draw_ov.line([(0, y), (width, y)], fill=(16, 12, 22, alpha))
        
    for y in range(1180, height):
        rel = (y - 1180) / (height - 1180.0)
        alpha = int(120 * (rel ** 1.3))
        draw_ov.line([(0, y), (width, y)], fill=(16, 12, 22, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # ---------------------------------------------------------
    # YouTube Safe Area Coordinates
    # Canvas: 2560 x 1440
    # Safe Box: 1546 x 424 (x: 507..2053, y: 508..932)
    # ---------------------------------------------------------
    safe_left = 507
    safe_top = 508
    safe_width = 1546
    safe_height = 424

    # ---------------------------------------------------------
    # 3. Left Section: Clean Frosted Glass Hero Container
    # Width 680 px, leaving the right side wide open for Tokyo Tower
    # ---------------------------------------------------------
    hero_box_w = 680
    hero_box_h = 390
    hero_box_x = safe_left + 15
    hero_box_y = safe_top + 16

    hero_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_hero_ov = ImageDraw.Draw(hero_overlay)
    draw_hero_ov.rounded_rectangle(
        [(hero_box_x, hero_box_y), (hero_box_x + hero_box_w, hero_box_y + hero_box_h)],
        radius=20,
        fill=(14, 12, 22, 195),
        outline=(245, 158, 11, 190),  # Warm Amber Gold Outline
        width=2
    )
    img = Image.alpha_composite(img.convert("RGBA"), hero_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Load App Icon if available
    app_icon_path = ASSETS_DIR / "tokyoflow_official_app_icon.jpg"
    app_icon_img = None
    if app_icon_path.exists():
        app_icon_raw = Image.open(app_icon_path).convert("RGBA")
        icon_size = 44
        app_icon_raw = app_icon_raw.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (icon_size, icon_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([(0, 0), (icon_size, icon_size)], radius=12, fill=255)
        app_icon_img = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
        app_icon_img.paste(app_icon_raw, (0, 0), mask)

    # 1. Top Brand Pill inside Left Box
    pill_x = hero_box_x + 20
    pill_y = hero_box_y + 18
    pill_w = 310
    pill_h = 46
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=14, fill=(255, 255, 255))
    
    if app_icon_img:
        img.paste(app_icon_img, (pill_x + 6, pill_y + 1), app_icon_img)
        brand_text_x = pill_x + 56
    else:
        brand_text_x = pill_x + 16
        
    font_brand = get_font(21, is_en=True)
    draw.text((brand_text_x, pill_y + 11), "TokyoFlow Japanese", fill=(225, 29, 72), font=font_brand)

    # Sub-Pill / Dual Language Column & JLPT Level Badge
    badge_x = pill_x + pill_w + 10
    badge_y = pill_y
    badge_w = 300
    badge_h = 46
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=14, fill=(225, 29, 72))
    font_badge = get_font(17, is_en=False)
    badge_str = "中英双解说 • JLPT N5-N1"
    bbox_bg = draw.textbbox((0, 0), badge_str, font=font_badge)
    bw, bh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - bw) // 2, badge_y + (badge_h - bh) // 2 - bbox_bg[1]), badge_str, fill=(255, 255, 255), font=font_badge)

    # 2. Punchy 3D Solar Yellow Hook
    hook_y = hero_box_y + 80
    font_hook = get_heavy_hook_font(52)
    hook_lines = ["SPEAK REAL-LIFE", "TOKYO JAPANESE"]

    hy = hook_y
    for line in hook_lines:
        for dx, dy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((hero_box_x + 20 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((hero_box_x + 20, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 58

    # 3. Neon Pink Sub-Hook
    font_sub = get_font(19, is_en=False)
    draw.text((hero_box_x + 22, hy + 6), "山手线 • 便利店 • 居酒屋 • 沉浸实景精讲 • 原声跟读", fill=(244, 114, 182), font=font_sub)

    # 4. Bilingual Tagline
    font_jp_sub = get_font(17, is_en=False)
    draw.text((hero_box_x + 22, hy + 38), "东京真实生活口语最速通关 • Real Tokyo Immersion & Shadowing", fill=(254, 215, 170), font=font_jp_sub)

    # 5. Compact Publishing Schedule Ribbon inside Left Box Bottom
    ribbon_x = hero_box_x + 20
    ribbon_y = hero_box_y + hero_box_h - 56
    ribbon_w = hero_box_w - 40
    ribbon_h = 42
    draw.rounded_rectangle([(ribbon_x, ribbon_y), (ribbon_x + ribbon_w, ribbon_y + ribbon_h)], radius=12, fill=(225, 29, 72))
    
    ribbon_txt = "📅 每日 08:00 AM 精讲微课  •  17:00 PM 互动跟读 Shorts"
    font_ribbon = get_font(18, is_en=False)
    bbox_rb = draw.textbbox((0, 0), ribbon_txt, font=font_ribbon)
    rw, rh = bbox_rb[2] - bbox_rb[0], bbox_rb[3] - bbox_rb[1]
    draw.text((ribbon_x + (ribbon_w - rw) // 2, ribbon_y + (ribbon_h - rh) // 2 - bbox_rb[1]), ribbon_txt, fill=(255, 255, 255), font=font_ribbon)

    # ---------------------------------------------------------
    # 4. Save outputs
    # ---------------------------------------------------------
    if not output_paths:
        output_paths = [
            ASSETS_DIR / "tokyoflow_channel_banner.jpg",
            ASSETS_DIR / "tokyoflow_yt_banner.jpg",
            PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
        ]

    for p in output_paths:
        p_path = Path(p)
        p_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(p_path, "JPEG", quality=95)
        print(f"✓ Saved YouTube Banner: {p_path} (2560x1440)")

    return img

if __name__ == "__main__":
    generate_channel_banner()
