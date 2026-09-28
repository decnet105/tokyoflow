#!/usr/bin/env python3
"""
TokyoFlow Japanese • YouTube Serialized Thumbnail Engine (Skill Standard)
Renders 100% consistent, high-CTR 16:9 Full HD (1920x1080) YouTube covers for all episodes:
- Brand Badge: Top-left pill 'TokyoFlow 🇯🇵' (White background, crimson border)
- Hook Title: High-contrast uppercase bold text in bright yellow (#FEF08A) with thick black stroke
- Episode Badge: Top-right 'EP. XX' in bold white with black stroke
- Japanese Key Phrase: Prominent Japanese phrase in clean bold white font with deep shadow/stroke
- Subtitle Badge: Bottom center dark slate pill with golden amber border ('🇯🇵 Native Audio • ...')
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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
    
    # 1. Load Background Image or Create Cinematic Gradient
    if bg_image_path and os.path.exists(bg_image_path):
        base_img = Image.open(bg_image_path).convert("RGB")
        # Crop & Resize to 16:9 1920x1080
        src_w, src_h = base_img.size
        target_ratio = width / height
        src_ratio = src_w / src_h
        
        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            left = (src_w - new_w) // 2
            base_img = base_img.crop((left, 0, left + new_w, src_h))
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            base_img = base_img.crop((0, top, src_w, top + new_h))
            
        base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
    else:
        base_img = Image.new("RGB", (width, height), color=(15, 23, 42))

    # 2. Add Cinematic Vignette & Readability Gradient Overlay
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Top header shadow banner
    draw_overlay.rectangle([(0, 0), (width, 260)], fill=(10, 15, 30, 175))
    # Bottom footer shadow banner
    draw_overlay.rectangle([(0, height - 380), (width, height)], fill=(10, 15, 30, 210))
    
    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Top-Left Brand Pill
    badge_w, badge_h = 320, 84
    badge_x, badge_y = 60, 48
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=22, fill=(255, 255, 255), outline=(220, 38, 38), width=4)
    font_brand = get_font(42)
    draw.text((badge_x + 32, badge_y + 16), "TokyoFlow 🇯🇵", fill=(220, 38, 38), font=font_brand)

    # 4. Top Hook Title + Episode Badge
    font_hook = get_font(96)
    font_ep = get_font(90)
    hook_text = english_hook.upper()
    ep_text = f"EP. {ep_num:02d}"

    # Draw Hook with thick 360-degree black stroke for max readability
    hook_x = 420
    hook_y = 42
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            draw.text((hook_x + dx, hook_y + dy), hook_text, fill=(0, 0, 0), font=font_hook)
    draw.text((hook_x, hook_y), hook_text, fill=(254, 240, 138), font=font_hook) # Bright Yellow #FEF08A

    # Draw EP Badge at top right
    ep_x = width - 420
    ep_y = 45
    for dx in range(-6, 7):
        for dy in range(-6, 7):
            draw.text((ep_x + dx, ep_y + dy), ep_text, fill=(0, 0, 0), font=font_ep)
    draw.text((ep_x, ep_y), ep_text, fill=(255, 255, 255), font=font_ep)

    # 5. Big Center Japanese Key Phrase
    font_jp = get_font(118)
    # Measure text bounding box for exact center alignment
    bbox = draw.textbbox((0, 0), japanese_key_phrase, font=font_jp)
    jp_w = bbox[2] - bbox[0]
    jp_x = (width - jp_w) // 2
    jp_y = height - 320

    for dx in range(-9, 10):
        for dy in range(-9, 10):
            draw.text((jp_x + dx, jp_y + dy), japanese_key_phrase, fill=(0, 0, 0), font=font_jp)
    draw.text((jp_x, jp_y), japanese_key_phrase, fill=(255, 255, 255), font=font_jp)

    # 6. Bottom Information Pill
    font_sub = get_font(34)
    pill_bbox = draw.textbbox((0, 0), bottom_tag, font=font_sub)
    tag_w = pill_bbox[2] - pill_bbox[0]
    pill_w = max(580, tag_w + 80)
    pill_h = 76
    pill_x = (width - pill_w) // 2
    pill_y = height - 125

    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=20, fill=(30, 41, 59), outline=(245, 158, 11), width=3)
    text_x = pill_x + (pill_w - tag_w) // 2
    draw.text((text_x, pill_y + 18), bottom_tag, fill=(255, 255, 255), font=font_sub)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Standardized Serialized Thumbnail generated: {output_path}")

EPISODE_COVERS = [
    {
        "ep_num": 1,
        "hook": "TOKYO METRO HACK",
        "jp": "まもなく参ります",
        "tag": "🇯🇵 Native Transit Audio • Shadowing",
        "bg": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/tokyo_subway_metro_1790613022369.jpg",
        "out_rel": "docs/youtube_releases/ep01_yamanote_transit/thumbnail.jpg",
        "out_asset": "docs/youtube_assets/thumbnails/ep01_yamanote_transit_thumb.jpg"
    },
    {
        "ep_num": 2,
        "hook": "KOMBINI SURVIVAL",
        "jp": "温めますか？",
        "tag": "🇯🇵 1-Sec Register Reply • Shadowing",
        "bg": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_kombini_1790626387613.jpg",
        "out_rel": "docs/youtube_releases/ep02_kombini_checkout/thumbnail.jpg",
        "out_asset": "docs/youtube_assets/thumbnails/ep02_kombini_checkout_thumb.jpg"
    },
    {
        "ep_num": 3,
        "hook": "IZAKAYA MASTERY",
        "jp": "とりあえず生！",
        "tag": "🇯🇵 Showa Pub Etiquette • Shadowing",
        "bg": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_izakaya_1790626403507.jpg",
        "out_rel": "docs/youtube_releases/ep03_izakaya_night/thumbnail.jpg",
        "out_asset": "docs/youtube_assets/thumbnails/ep03_izakaya_night_thumb.jpg"
    },
    {
        "ep_num": 4,
        "hook": "AKIBA MANGA HUNT",
        "jp": "購入特典ありますか",
        "tag": "🇯🇵 Tax-Free & Merch • Shadowing",
        "bg": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/akiba_neon_manga_1790602623116.jpg",
        "out_rel": "docs/youtube_releases/ep04_akiba_pilgrimage/thumbnail.jpg",
        "out_asset": "docs/youtube_assets/thumbnails/ep04_akiba_pilgrimage_thumb.jpg"
    }
]

def main():
    print("🎨 Generating 100% Consistent Serialized Thumbnails (E1 to E4)...")
    for item in EPISODE_COVERS:
        generate_serialized_thumbnail(
            ep_num=item["ep_num"],
            english_hook=item["hook"],
            japanese_key_phrase=item["jp"],
            bottom_tag=item["tag"],
            bg_image_path=item["bg"],
            output_path=item["out_rel"]
        )
        if "out_asset" in item:
            generate_serialized_thumbnail(
                ep_num=item["ep_num"],
                english_hook=item["hook"],
                japanese_key_phrase=item["jp"],
                bottom_tag=item["tag"],
                bg_image_path=item["bg"],
                output_path=item["out_asset"]
            )
    print("🎉 E1 to E4 thumbnails rendered with 100% unified visual style!")

if __name__ == "__main__":
    main()
