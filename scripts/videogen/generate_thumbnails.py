#!/usr/bin/env python3
"""
TokyoFlow Japanese • YouTube Serialized Thumbnail Engine
Matches Mystory video & cover factory design architecture:
- High contrast, 16:9 1080p canvas (1920x1080).
- Consistent top-left brand pill ('TokyoFlow 🎌').
- High-visibility yellow/white bold hook header + 'EP. XX' badge.
- Real-life Japanese key phrase in clean prominent font.
- Bottom pill badge ('🇯🇵 Native Audio • 1-Sec Reply').
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def generate_serialized_thumbnail(
    ep_num: int,
    english_hook: str,
    japanese_key_phrase: str,
    bottom_tag: str,
    bg_image_path: str,
    output_path: str
):
    width, height = 1920, 1080
    
    if bg_image_path and os.path.exists(bg_image_path):
        base_img = Image.open(bg_image_path).convert("RGB")
        base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
    else:
        # Fallback stylized Tokyo night gradient
        base_img = Image.new("RGB", (width, height), color=(15, 23, 42))

    # Add dark vignette gradient overlay for high contrast text readability
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Gradient overlay on top and bottom
    draw_overlay.rectangle([(0, 0), (width, 320)], fill=(10, 15, 30, 160))
    draw_overlay.rectangle([(0, height - 280), (width, height)], fill=(10, 15, 30, 200))
    
    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top Left Brand Badge Pill
    badge_w, badge_h = 320, 90
    draw.rounded_rectangle([(60, 50), (60 + badge_w, 50 + badge_h)], radius=24, fill=(255, 255, 255), outline=(220, 38, 38), width=4)
    font_brand = get_font(44)
    draw.text((95, 68), "TokyoFlow 🇯🇵", fill=(220, 38, 38), font=font_brand)

    # 2. Main English Hook + EP. XX Badge
    font_hook = get_font(110)
    font_ep = get_font(90)
    
    # Outer stroke / shadow for English Hook
    hook_text = english_hook.upper()
    ep_text = f"EP. {ep_num:02d}"
    
    # Draw Hook with thick black stroke
    for dx in range(-6, 7):
        for dy in range(-6, 7):
            draw.text((420 + dx, 55 + dy), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((420, 55), hook_text, fill=(254, 240, 138), font=font_hook) # bright yellow

    # Draw EP Badge
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            draw.text((width - 450 + dx, 65 + dy), ep_text, fill=(0, 0, 0), font=font_ep)
    draw.text((width - 450, 65), ep_text, fill=(255, 255, 255), font=font_ep)

    # 3. Japanese Key Phrase in Center Bottom
    font_jp = get_font(120)
    jp_w = len(japanese_key_phrase) * 120
    jp_x = (width - jp_w) // 2
    jp_y = height - 320
    
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            draw.text((jp_x + dx, jp_y + dy), japanese_key_phrase, fill=(0, 0, 0), font=font_jp)
    draw.text((jp_x, jp_y), japanese_key_phrase, fill=(255, 255, 255), font=font_jp)

    # 4. Bottom Info Pill
    pill_w, pill_h = 580, 80
    pill_x = (width - pill_w) // 2
    pill_y = height - 120
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=20, fill=(30, 41, 59), outline=(245, 158, 11), width=3)
    font_sub = get_font(36)
    draw.text((pill_x + 35, pill_y + 18), bottom_tag, fill=(255, 255, 255), font=font_sub)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Serialized Thumbnail generated: {output_path}")

if __name__ == "__main__":
    print("🎨 Serialized Thumbnail Generator Ready.")
