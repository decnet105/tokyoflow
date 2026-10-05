#!/usr/bin/env python3
"""
Fix Chinese EP.05 Shorts Cover
Generates Golden Master 9:16 vertical cover for Chinese EP.05 using the authentic subway gate photo,
matching the English EP.05 standard with Chinese localized typography.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
OUT_FILE = RELEASES_DIR / "E05-Tokyo_Subway_Rush-v1.0-zh" / "short_thumbnail.jpg"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_PATH if not is_en else FONT_EN_HEAVY
    try:
        return ImageFont.truetype(font_file, size)
    except Exception:
        return ImageFont.load_default()

def generate_chinese_ep05_shorts_cover():
    W, H = 1080, 1920
    
    # Authentic background photo
    bg_candidates = [
        "/Users/kilvonwu/.gemini/antigravity/brain/05184417-05e5-4849-b75b-23838a5adf09/tokyoflow_thumb_ep05_1790725833742.jpg",
        str(PROJECT_ROOT / "tmp" / "videogen" / "real_photos" / "ep05_metro_gates.jpg"),
        str(PROJECT_ROOT / "docs" / "youtube_releases" / "E05-Tokyo_Subway_Rush-v1.0" / "short_thumbnail.jpg")
    ]
    bg_path = None
    for cand in bg_candidates:
        if os.path.exists(cand):
            bg_path = cand
            break

    if bg_path:
        raw_img = Image.open(bg_path).convert("RGB")
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

    # Dark Gradient Overlays
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

    # 1. Top Header: TokyoFlow Brand Pill & Shorts Level Badge
    pill_w, pill_h = 390, 65
    draw.rounded_rectangle([(50, 50), (50 + pill_w, 50 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(28, is_en=True)
    draw.text((50 + 40, 50 + 16), "TokyoFlow 日语", fill=(225, 29, 72), font=get_font(28))

    sh_code = "SH.05 • 【JLPT N4】"
    badge_w, badge_h = 310, 65
    badge_x = W - 50 - badge_w
    draw.rounded_rectangle([(badge_x, 50), (badge_x + badge_w, 50 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26)
    draw.text((badge_x + 25, 50 + 16), sh_code, fill=(255, 255, 255), font=font_badge)

    # 2. Punchy 3D Action Hook
    hook_main = "东京地铁坐过站？\n精算机补票实战"
    hook_sub = "出站余额不足 30秒解决"
    
    font_hook_sh = get_font(74)
    hy = 150
    hook_lines = hook_main.split("\n")
    for line in hook_lines:
        for dx in range(-4, 5, 2):
            for dy in range(-4, 5, 2):
                draw.text((50 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook_sh)
        draw.text((50, hy), line, fill=(254, 240, 138), font=font_hook_sh)
        hy += 88

    # Sub-Hook
    draw.text((55, hy + 5), hook_sub, fill=(244, 114, 182), font=get_font(32))

    # 3. Learning Card (y=1150)
    card_x, card_y = 40, 1150
    card_w, card_h = 1000, 720
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=3)

    # Card Top Header
    draw.text((card_x + 35, card_y + 25), "【 东京地铁出行实战 】", fill=(56, 189, 248), font=get_font(26))
    draw.rounded_rectangle([(card_x + card_w - 240, card_y + 20), (card_x + card_w - 30, card_y + 62)], radius=10, fill=(225, 29, 72))
    draw.text((card_x + card_w - 225, card_y + 26), "【JLPT N4】必备", fill=(255, 255, 255), font=get_font(20))

    draw.line([(card_x + 35, card_y + 75), (card_x + card_w - 35, card_y + 75)], fill=(51, 65, 85), width=2)

    # Japanese Target Sentence
    full_jp = "乗り越し精算機はどこですか？"
    font_jp = get_font(44)
    draw.text((card_x + 35, card_y + 98), full_jp, fill=(255, 255, 255), font=font_jp)

    # Romaji
    draw.text((card_x + 35, card_y + 162), "Norikoshi seisanki wa doko desu ka?", fill=(254, 240, 138), font=get_font(24, is_en=True))
    
    # Chinese Translation
    draw.text((card_x + 35, card_y + 208), "「请问坐过站的补票结算机在哪里？」", fill=(226, 232, 240), font=get_font(26))

    # Grammar Tag Pill inside card
    tag_clean = "【JLPT N4 语法】~はどこですか（询问方位与场所）"
    draw.rounded_rectangle([(card_x + 35, card_y + 270), (card_x + card_w - 35, card_y + 335)], radius=12, fill=(15, 23, 42, 220), outline=(244, 114, 182), width=2)
    draw.text((card_x + 55, card_y + 288), tag_clean, fill=(244, 114, 182), font=get_font(23))

    # 4. CTA Action Banner at Bottom of Card
    cta_x = card_x + 30
    cta_y = card_y + 365
    cta_w = card_w - 60
    cta_h = 310
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=18, fill=(225, 29, 72))
    
    draw.text((cta_x + 35, cta_y + 35), "观看完整精讲大班课 (EP.05)", fill=(255, 255, 255), font=get_font(34))
    draw.text((cta_x + 35, cta_y + 95), "完整词汇拆解 • 语法考点 • 纯正原声跟读", fill=(254, 240, 138), font=get_font(24))
    draw.text((cta_x + 35, cta_y + 145), "点击下方关联长视频 • TokyoFlow Japanese", fill=(241, 245, 249), font=get_font(22))

    img.save(OUT_FILE, quality=95)
    print(f"✅ Generated Chinese EP.05 Shorts Cover: {OUT_FILE}")

if __name__ == "__main__":
    generate_chinese_ep05_shorts_cover()
