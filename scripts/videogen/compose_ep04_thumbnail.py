#!/usr/bin/env python3
"""
High-Fidelity Serialized Thumbnail Compositor for TokyoFlow Episode 04
Faithfully matches the visual richness, lighting, typography, and contrast of EP 01 - EP 03.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FONT_JP_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_JP_HEAVY = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int, bold: bool = True):
    try:
        return ImageFont.truetype(FONT_JP_BOLD, size)
    except Exception:
        return ImageFont.load_default()

def compose_ep04_thumbnail():
    target_w, target_h = 1376, 768  # Native resolution matching E1-E3 master covers
    
    # 1. Base Background from Akihabara Anime Manga Art
    bg_path = "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/akiba_neon_manga_1790602623116.jpg"
    bg = Image.open(bg_path).convert("RGB")
    
    # Crop the most vibrant cinematic section (middle-top)
    w, h = bg.size
    crop_h = int(w * (target_h / target_w))
    top = int((h - crop_h) * 0.35)
    bg_cropped = bg.crop((0, top, w, top + crop_h))
    bg_resized = bg_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Enhance contrast and saturation for YouTube thumbnail pop
    enhancer_con = ImageEnhance.Contrast(bg_resized)
    bg_enhanced = enhancer_con.enhance(1.18)
    enhancer_col = ImageEnhance.Color(bg_enhanced)
    bg_enhanced = enhancer_col.enhance(1.22)

    # 2. Cinematic Gradient Overlay (Top and Bottom dark vignette for supreme text legibility)
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Smooth Top gradient (for Hook & Badge)
    for y in range(220):
        alpha = int(180 * (1.0 - (y / 220.0) ** 1.3))
        draw_ov.line([(0, y), (target_w, y)], fill=(8, 12, 24, alpha))
        
    # Smooth Bottom gradient (for Japanese Text & Pill)
    for y in range(target_h - 320, target_h):
        rel = (y - (target_h - 320)) / 320.0
        alpha = int(225 * (rel ** 1.2))
        draw_ov.line([(0, y), (target_w, y)], fill=(6, 10, 20, alpha))
        
    canvas = Image.alpha_composite(bg_enhanced.convert("RGBA"), overlay).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    # 3. Top-Left Brand Pill ("TokyoFlow 🎌")
    pill_w, pill_h = 240, 68
    pill_x, pill_y = 48, 38
    
    # Pill drop shadow
    shadow_pill = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_sp = ImageDraw.Draw(shadow_pill)
    draw_sp.rounded_rectangle([(pill_x + 3, pill_y + 4), (pill_x + pill_w + 3, pill_y + pill_h + 4)], radius=18, fill=(0, 0, 0, 160))
    shadow_pill = shadow_pill.filter(ImageFilter.GaussianBlur(6))
    canvas = Image.alpha_composite(canvas, shadow_pill)
    draw = ImageDraw.Draw(canvas)
    
    # Pill surface
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=18, fill=(255, 255, 255, 250), outline=(220, 38, 38), width=3)
    font_brand = get_font(34)
    draw.text((pill_x + 24, pill_y + 13), "TokyoFlow 🎌", fill=(220, 38, 38), font=font_brand)

    # 4. English Hook ("AKIBA MANGA HUNT") + Episode Badge ("EP. 04")
    font_hook = get_font(74)
    font_ep = get_font(68)
    
    hook_str = "AKIBA MANGA HUNT"
    ep_str = "EP. 04"
    
    hook_x = 320
    hook_y = 34
    
    # Heavy 3D Outline & Shadow for English Hook
    for off in range(8, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((hook_x + dx, hook_y + dy + 2), hook_str, fill=(0, 0, 0, 255), font=font_hook)
    draw.text((hook_x, hook_y), hook_str, fill=(254, 240, 138), font=font_hook) # Bright Yellow #FEF08A

    # EP Badge on Top Right
    ep_x = target_w - 320
    ep_y = 38
    for off in range(7, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((ep_x + dx, ep_y + dy + 2), ep_str, fill=(0, 0, 0, 255), font=font_ep)
    draw.text((ep_x, ep_y), ep_str, fill=(255, 255, 255), font=font_ep)

    # 5. Big Center-Bottom Japanese Key Phrase ("購入特典ありますか")
    font_jp = get_font(92)
    jp_text = "購入特典ありますか"
    
    bbox = draw.textbbox((0, 0), jp_text, font=font_jp)
    jp_w = bbox[2] - bbox[0]
    jp_x = (target_w - jp_w) // 2
    jp_y = target_h - 240

    # Multi-pass deep drop shadow & glowing outline
    for off in range(10, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((jp_x + dx, jp_y + dy + 3), jp_text, fill=(0, 0, 0, 255), font=font_jp)
    draw.text((jp_x, jp_y), jp_text, fill=(255, 255, 255), font=font_jp)

    # 6. Bottom Information Pill ("🇯🇵 Native Audio • Anime & Merch")
    font_pill = get_font(28)
    pill_text = "🇯🇵 Native Audio • Tax-Free & Merch"
    pill_text_bbox = draw.textbbox((0, 0), pill_text, font=font_pill)
    tag_w = pill_text_bbox[2] - pill_text_bbox[0]
    
    bp_w = tag_w + 64
    bp_h = 58
    bp_x = (target_w - bp_w) // 2
    bp_y = target_h - 95
    
    # Shadow for bottom pill
    shadow_bp = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    draw_sbp = ImageDraw.Draw(shadow_bp)
    draw_sbp.rounded_rectangle([(bp_x + 2, bp_y + 3), (bp_x + bp_w + 2, bp_y + bp_h + 3)], radius=16, fill=(0, 0, 0, 180))
    shadow_bp = shadow_bp.filter(ImageFilter.GaussianBlur(5))
    canvas = Image.alpha_composite(canvas, shadow_bp)
    draw = ImageDraw.Draw(canvas)
    
    draw.rounded_rectangle([(bp_x, bp_y), (bp_x + bp_w, bp_y + bp_h)], radius=16, fill=(24, 32, 47, 240), outline=(245, 158, 11), width=2)
    draw.text((bp_x + 32, bp_y + 12), pill_text, fill=(255, 255, 255), font=font_pill)

    # 7. Convert and Save Final 1080p output
    final_rgb = canvas.convert("RGB")
    final_hd = final_rgb.resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # Save to release package & asset thumbnail folders
    out_paths = [
        "docs/youtube_releases/ep04_akiba_pilgrimage/thumbnail.jpg",
        "docs/youtube_assets/thumbnails/ep04_akiba_pilgrimage_thumb.jpg"
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        final_hd.save(p, quality=96)
        print(f"✓ Master-grade EP04 thumbnail created: {p}")

if __name__ == "__main__":
    compose_ep04_thumbnail()
