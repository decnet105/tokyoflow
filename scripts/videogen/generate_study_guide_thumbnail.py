#!/usr/bin/env python3
"""
TokyoFlow Japanese • Luxury 16:9 Master Thumbnail Generator
Creates an ultra-high-end, cinema-grade thumbnail for the Study Guide & Roadmap video.
Strict Zero Emoji Policy.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "output" / "study_guide_en"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def generate_luxury_thumbnail():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    W, H = 1920, 1080
    
    # 1. Base dark background
    bg = Image.new("RGB", (W, H), (10, 14, 24))
    
    # Background Tokyo skyline photo
    skyline_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_tokyo_skyline_distant_4k.jpg"
    if not skyline_path.exists():
        skyline_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_tokyo_skyline_wide.jpg"
        
    if skyline_path.exists():
        sky = Image.open(skyline_path).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        sky = ImageEnhance.Brightness(sky).enhance(0.32)
        sky = ImageEnhance.Contrast(sky).enhance(1.15)
        bg.paste(sky, (0, 0))
        
    draw = ImageDraw.Draw(bg)
    
    # 2. Top Navigation & Brand Header
    draw.rectangle([(60, 40), (320, 85)], fill=(16, 28, 48), outline=(56, 189, 248), width=2)
    draw.text((80, 52), "TOKYOFLOW ACADEMY", fill=(56, 189, 248), font=get_font(20))
    
    draw.text((350, 53), "OFFICIAL STUDY GUIDE & ROADMAP", fill=(203, 213, 225), font=get_font(20))
    draw.text((1460, 53), "MASTERCLASS BLUEPRINT", fill=(148, 163, 184), font=get_font(18))
    draw.line([(60, 100), (1860, 100)], fill=(35, 50, 75), width=1)
    
    # 3. Left Panel (Main Content Glass Card)
    draw.rectangle([(60, 130), (1220, 980)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    # Top Gold Badge inside card
    draw.rectangle([(100, 165), (560, 215)], fill=(30, 58, 138), outline=(56, 189, 248), width=1)
    draw.text((120, 178), "COMPLETE STUDY BLUEPRINT", fill=(255, 255, 255), font=get_font(22))
    
    # Big Titles
    draw.text((100, 245), "HOW TO MASTER REAL", fill=(255, 255, 255), font=get_font(58))
    draw.text((100, 320), "TOKYO JAPANESE", fill=(56, 189, 248), font=get_font(68))
    draw.text((100, 420), "The Full Use-Case Syllabus & 15-Minute Shadowing Routine", fill=(226, 232, 240), font=get_font(24))
    
    # 3 Milestone Progress Bars
    stages = [
        ("[JLPT N5-N4]", "Transit & Kombini Survival", "Subway Transfers, 7-Eleven Speed Replies, Cafes", (30, 58, 138), (56, 189, 248)),
        ("[JLPT N3]", "Social & Dining Fluency", "Izakaya Draft Beer, Ramen Tickets, Akihabara", (161, 98, 7), (250, 204, 21)),
        ("[JLPT N2-N1]", "Real News & Native Nuance", "NHK Broadcasts, Business Discourse, Modern Slang", (126, 34, 206), (192, 132, 252))
    ]
    
    for i, (badge, title, desc, bg_b, fg_b) in enumerate(stages):
        sy = 485 + i * 125
        # Background card row
        draw.rectangle([(100, sy), (1180, sy + 105)], fill=(16, 24, 38), outline=(35, 50, 75), width=1)
        # Badge
        draw.rectangle([(115, sy + 15), (310, sy + 90)], fill=bg_b, outline=fg_b, width=2)
        draw.text((130, sy + 36), badge, fill=(255, 255, 255), font=get_font(26))
        # Title and description
        draw.text((335, sy + 22), title, fill=fg_b, font=get_font(24))
        draw.text((335, sy + 60), desc, fill=(148, 163, 184), font=get_font(18))
        
    # Bottom CTA inside Left Panel
    draw.rectangle([(100, 885), (1180, 945)], fill=(20, 50, 85), outline=(56, 189, 248), width=1)
    draw.text((125, 902), "FREE DOWNLOADABLE PDF SYLLABUS IN DESCRIPTION", fill=(255, 255, 255), font=get_font(22))
    
    # 4. Right Side: Multi-Scene Photo Composite
    # Top Photo: Subway / Transit
    photo_transit = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_yamanote_platform.jpg"
    # Bottom Photo: Kombini / Izakaya
    photo_dining = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_izakaya_yokocho.jpg"
    
    # Right panel frame
    draw.rectangle([(1260, 130), (1860, 980)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    if photo_transit.exists():
        t_img = Image.open(photo_transit).convert("RGB").resize((560, 395), Image.Resampling.LANCZOS)
        bg.paste(t_img, (1280, 150))
        draw.rectangle([(1280, 150), (1840, 545)], outline=(56, 189, 248), width=2)
        draw.rectangle([(1300, 485), (1820, 530)], fill=(10, 16, 26, 230))
        draw.text((1320, 496), "16:9 Scenario Masterclasses", fill=(255, 255, 255), font=get_font(20))
        
    if photo_dining.exists():
        d_img = Image.open(photo_dining).convert("RGB").resize((560, 395), Image.Resampling.LANCZOS)
        bg.paste(d_img, (1280, 565))
        draw.rectangle([(1280, 565), (1840, 960)], outline=(56, 189, 248), width=2)
        draw.rectangle([(1300, 900), (1820, 945)], fill=(10, 16, 26, 230))
        draw.text((1320, 911), "9:16 Vocal Shadowing Shorts", fill=(56, 189, 248), font=get_font(20))

    thumb_file = OUT_DIR / "thumbnail.jpg"
    bg.save(thumb_file, quality=95)
    print(f"Master 16:9 Thumbnail saved to: {thumb_file}")

if __name__ == "__main__":
    generate_luxury_thumbnail()
