#!/usr/bin/env python3
"""
TokyoFlow Japanese • Master Serialized Thumbnail & Cover Factory
Unified, production-grade implementation of tokyoflow-thumbnail-factory skill:
1. 16:9 Long-Form 4K/Full HD Covers (thumbnail.jpg, 1920x1080)
   - Real-life authentic Tokyo photographic scene with contrast/saturation boost.
   - Smooth cinematic multi-stop exponential top and bottom dark vignettes.
   - Top-Left 'TokyoFlow 🇯🇵' Brand Pill (white pill, crimson text, Gaussian shadow).
   - 3D Electric-Yellow Hook (88-96pt #FEF08A) + 360° deep black drop stroke.
   - Top-Right '[JLPT Level] EP.XX' Serialized Badge.
   - Center-Bottom Giant 116pt Japanese Soul Phrase (10px deep black shadow).
   - Bottom Scenario Value Tag Pill (dark slate, amber border, drop shadow).
2. 9:16 Shorts High-CTR Vertical Covers (short_thumbnail.jpg, 1080x1920)
   - Auto-sized dynamic Header Ribbon (dark glassmorphic capsule, cyan border, crisp white text, ZERO overflow).
   - 108pt 3D Solar Yellow Hook Banner.
   - Central 3-Tier Japanese Dialogue Card with glowing active word highlight & indicator dot.
   - Live Mic Shadowing HUD with animated waveform & pacing countdown.
   - AI Pitch Accent 98.6% Verification Badge.
"""

import os
import sys
import glob
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"
ASSETS_DIR = PROJECT_ROOT / "docs" / "youtube_assets" / "thumbnails"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_JP_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size: int, is_en: bool = False):
    font_file = FONT_EN_HEAVY if is_en else FONT_PATH
    try:
        return ImageFont.truetype(font_file, size)
    except Exception:
        return ImageFont.load_default()

# -------------------------------------------------------------------------
# 1. 16:9 Long-Form YouTube Thumbnail Generator (Master EP01-EP08 Style)
# -------------------------------------------------------------------------
def generate_serialized_thumbnail(
    ep_num: int,
    english_hook: str,
    japanese_key_phrase: str,
    bottom_tag: str,
    bg_image_path: str,
    output_path: str,
    jlpt_level: str = "JLPT N5"
):
    width, height = 1920, 1080
    
    # 1. Background Image Loading & Photographic Enhancement
    if bg_image_path and os.path.exists(bg_image_path):
        base_img = Image.open(bg_image_path).convert("RGB")
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
        
        # Enhance contrast and saturation for authentic YouTube pop
        base_img = ImageEnhance.Contrast(base_img).enhance(1.18)
        base_img = ImageEnhance.Color(base_img).enhance(1.22)
    else:
        # Default Deep Tokyo Cyber-Navy Gradient
        base_img = Image.new("RGB", (width, height), color=(12, 17, 29))
        draw_def = ImageDraw.Draw(base_img)
        draw_def.rectangle([(0, 0), (width, height)], fill=(12, 17, 29))

    # 2. Cinematic Multi-Stop Dark Left & Bottom Vignettes (for 3-Tier Hook & Japanese text)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Left dark vignette for 3-tier hook
    for x in range(950):
        alpha = int(220 * (1.0 - (x / 950.0) ** 1.4))
        draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 24, alpha))
        
    # Smooth Bottom Vignette (for Japanese Text & Value Pill)
    for y in range(height - 380, height):
        rel = (y - (height - 380)) / 380.0
        alpha = int(210 * (rel ** 1.2))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 20, alpha))
        
    canvas = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGBA")

    # 3. Top-Left Brand Pill ("TokyoFlow [Flag]") with Soft Shadow
    pill_w, pill_h = 320, 78
    pill_x, pill_y = 60, 48
    
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([(pill_x, pill_y), (pill_x + pill_w, pill_y + pill_h)], radius=39, fill=(220, 38, 38), outline=(255, 255, 255), width=3)
    font_brand = get_font(38, is_en=True)
    draw.text((pill_x + 28, pill_y + 16), "TokyoFlow", fill=(255, 255, 255), font=font_brand)
    
    # Vector Japanese flag badge
    flag_x = pill_x + 236
    flag_y = pill_y + 19
    draw.rounded_rectangle([(flag_x, flag_y), (flag_x + 50, flag_y + 38)], radius=6, fill=(255, 255, 255))
    draw.ellipse([(flag_x + 14, flag_y + 8), (flag_x + 36, flag_y + 30)], fill=(220, 38, 38))

    # 4. Left 3-Tier Giant 3D Hook Stack
    font_hook = get_font(116)
    hook_words = english_hook.upper().replace("\n", " ").split(" ")
    if len(hook_words) == 1:
        hook_lines = [hook_words[0], "HACK"]
    elif len(hook_words) == 2:
        hook_lines = [hook_words[0], hook_words[1], "HACK"]
    else:
        hook_lines = hook_words[:3]

    h_y = 150
    for idx, hline in enumerate(hook_lines):
        bbox_hl = draw.textbbox((0, 0), hline, font=font_hook)
        hw = bbox_hl[2] - bbox_hl[0]
        cur_font = font_hook
        if hw > 820:
            cur_font = get_font(96)
            bbox_hl = draw.textbbox((0, 0), hline, font=cur_font)
            hw = bbox_hl[2] - bbox_hl[0]

        hx = 60
        # Multi-pass 3D Deep Black Extrusion & Shadow
        for off in range(10, 0, -1):
            for dx in range(-off, off + 1):
                for dy in range(-off, off + 1):
                    draw.text((hx + dx, h_y + dy + 3), hline, fill=(0, 0, 0, 255), font=cur_font)
        
        # Color: Lines 1 & 2 in Solar Yellow, Line 3 in Metallic White
        text_color = (250, 204, 21) if idx < len(hook_lines) - 1 else (255, 255, 255)
        draw.text((hx, h_y), hline, fill=text_color, font=cur_font)
        h_y += 118

    # 5. Bottom-Left Giant Japanese Soul Phrase (with Magenta Neon Aura)
    font_jp = get_font(108)
    jp_text = japanese_key_phrase
    bbox_j = draw.textbbox((0, 0), jp_text, font=font_jp)
    jp_w = bbox_j[2] - bbox_j[0]
    
    if jp_w > 1200:
        font_jp = get_font(88)
        bbox_j = draw.textbbox((0, 0), jp_text, font=font_jp)
        jp_w = bbox_j[2] - bbox_j[0]

    jp_x = 60
    jp_y = height - 260

    # Magenta Glowing Outer Aura Layer
    aura_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_aura = ImageDraw.Draw(aura_img)
    for off in range(12, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw_aura.text((jp_x + dx, jp_y + dy), jp_text, fill=(236, 72, 153, 160), font=font_jp)
    aura_img = aura_img.filter(ImageFilter.GaussianBlur(8))
    canvas = Image.alpha_composite(canvas, aura_img)
    draw = ImageDraw.Draw(canvas)

    # Multi-pass deep drop shadow (10px) & Pure White Text
    for off in range(9, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((jp_x + dx, jp_y + dy + 3), jp_text, fill=(0, 0, 0, 255), font=font_jp)
    draw.text((jp_x, jp_y), jp_text, fill=(255, 255, 255), font=font_jp)

    # 6. Bottom-Right 3D Metallic Episode Badge ("EP.XX")
    font_ep_prefix = get_font(104)
    font_ep_num = get_font(114)
    
    prefix_str = "EP."
    num_str = f"{ep_num:02d}"
    
    bbox_p = draw.textbbox((0, 0), prefix_str, font=font_ep_prefix)
    pw = bbox_p[2] - bbox_p[0]
    bbox_n = draw.textbbox((0, 0), num_str, font=font_ep_num)
    nw = bbox_n[2] - bbox_n[0]
    
    badge_total_w = pw + nw + 12
    badge_x = width - badge_total_w - 60
    badge_y = height - 270

    # 3D shadow for EP prefix
    for off in range(9, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((badge_x + dx, badge_y + dy + 3), prefix_str, fill=(0, 0, 0, 255), font=font_ep_prefix)
    draw.text((badge_x, badge_y), prefix_str, fill=(255, 255, 255), font=font_ep_prefix)

    # 3D shadow & Golden Yellow for Episode Number
    num_x = badge_x + pw + 12
    for off in range(10, 0, -1):
        for dx in range(-off, off + 1):
            for dy in range(-off, off + 1):
                draw.text((num_x + dx, badge_y + dy + 3), num_str, fill=(0, 0, 0, 255), font=font_ep_num)
    draw.text((num_x, badge_y), num_str, fill=(250, 204, 21), font=font_ep_num)

    # 7. Bottom-Right Scenario Value Tag Pill
    clean_tag = bottom_tag.replace("🇯🇵", "").replace("Native Audio •", "").replace("Native Audio -", "").replace("[JLPT N5]", "").replace("JLPT N5", "").strip()
    tag_content = f"Native Audio • {jlpt_level} {clean_tag}" if clean_tag else f"Native Audio • {jlpt_level} Trend"
    
    font_pill = get_font(28)
    pill_text_bbox = draw.textbbox((0, 0), tag_content, font=font_pill)
    tag_w = pill_text_bbox[2] - pill_text_bbox[0]
    
    bp_w = tag_w + 104
    bp_h = 58
    bp_x = width - bp_w - 60
    bp_y = height - 100
    
    draw.rounded_rectangle([(bp_x, bp_y), (bp_x + bp_w, bp_y + bp_h)], radius=20, fill=(18, 25, 42, 240), outline=(255, 255, 255), width=2)
    # Vector flag badge in bottom pill
    flag_bx = bp_x + 18
    flag_by = bp_y + 11
    draw.rounded_rectangle([(flag_bx, flag_by), (flag_bx + 44, flag_by + 34)], radius=5, fill=(255, 255, 255))
    draw.ellipse([(flag_bx + 11, flag_by + 6), (flag_bx + 33, flag_by + 28)], fill=(220, 38, 38))
    
    draw.text((bp_x + 76, bp_y + 14), tag_content, fill=(255, 255, 255), font=font_pill)

    # 8. Convert and Save Output
    final_img = canvas.convert("RGB")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path, "JPEG", quality=95)
    print(f"✓ Master 16:9 Long-Form Thumbnail generated: {output_path}")

## -------------------------------------------------------------------------
# 2. 9:16 Shorts Minimalist High-CTR Vertical Cover (Zero Overflow Standard)
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
    bg_image_path: str = ""
):
    from generate_shorts_thumbnails import create_shorts_cover
    
    # Theme color palettes
    if category_theme == "transit":
        accent_color = (16, 185, 129)     # Emerald
        accent_secondary = (56, 189, 248)  # Sky Cyan
        location = "SHINJUKU STATION • YAMANOTE"
    elif category_theme == "kombini":
        accent_color = (249, 115, 22)     # Amber Orange
        accent_secondary = (250, 204, 21)  # Solar Yellow
        location = "SHIBUYA 7-ELEVEN • TOKYO"
    elif category_theme == "izakaya":
        accent_color = (234, 179, 8)      # Beer Gold
        accent_secondary = (249, 115, 22)  # Coral Warmth
        location = "SHINBASHI IZAKAYA ALLEY"
    else: # Anime / Shopping / Pop Culture
        accent_color = (236, 72, 153)     # Neon Pink
        accent_secondary = (250, 204, 21)  # Solar Yellow
        location = "TOKYO POP CULTURE • JLPT"

    hook_lines = [h.strip() for h in english_hook.replace("\n", " ").split(" ") if h.strip()]
    if len(hook_lines) >= 2:
        hook_main = " ".join(hook_lines[:2])
        hook_sub = " ".join(hook_lines[2:]) if len(hook_lines) > 2 else "JAPAN TREND"
    elif len(hook_lines) == 1:
        hook_main = hook_lines[0]
        hook_sub = "JAPAN TREND"
    else:
        hook_main = "JAPAN TREND"
        hook_sub = "POP CULTURE"

    item_dict = {
        "ep_num": ep_num,
        "sh_code": f"SH.{ep_num:02d}",
        "folder": f"E{ep_num:02d}",
        "hook_main": hook_main,
        "hook_sub": hook_sub,
        "jp_phrase": japanese_sentence,
        "romaji": romaji_sentence,
        "en_meaning": en_translation,
        "accent_color": accent_color,
        "secondary_color": accent_secondary,
        "location": location,
        "jlpt_level": jlpt_level,
        "bg_image_path": bg_image_path
    }
    
    img = create_shorts_cover(item_dict)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"✓ Master 9:16 Shorts Cover generated (3-Pill Header): {output_path}")

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Standalone CLI Runner (Incremental Single-Target & Batch Support)
# -------------------------------------------------------------------------
def process_release_dir(rdir: str, sh_num: int = None):
    rdir_path = Path(rdir)
    if not rdir_path.exists():
        print(f"Directory not found: {rdir}")
        return
        
    script_file = rdir_path / "script.json"
    wallpapers = {
        "transit": str(PROJECT_ROOT / "TokyoFlow" / "Resources" / "Wallpapers" / "tokyo_subway.jpg"),
        "kombini": str(PROJECT_ROOT / "TokyoFlow" / "Resources" / "Wallpapers" / "rainy_cafe.jpg"),
        "izakaya": str(PROJECT_ROOT / "TokyoFlow" / "Resources" / "Wallpapers" / "cozy_room.jpg"),
        "shopping": str(PROJECT_ROOT / "TokyoFlow" / "Resources" / "Wallpapers" / "liquid_glass.jpg")
    }

    dir_name = rdir_path.name
    # Determine episode and short number
    try:
        ep_num = int(dir_name.split("-")[0].replace("E", ""))
    except Exception:
        ep_num = 1
        
    if sh_num is None:
        # Default mapping: E13 is sequential Short SH.09 following SH.01-08
        if ep_num == 13 or "E13" in dir_name:
            sh_num = 9
        else:
            sh_num = ep_num

    out_16_9 = str(rdir_path / "thumbnail.jpg")
    out_9_16 = str(rdir_path / "short_thumbnail.jpg")
    master_asset_path = ASSETS_DIR / f"{dir_name}_thumb.jpg"

    if script_file.exists():
        with open(script_file) as fp:
            data = json.load(fp)
        hook = data.get("cover", {}).get("hook", "TOKYO LESSON")
        jp = data.get("cover", {}).get("jp", "まもなく参ります")
        tag = data.get("cover", {}).get("tag", "🇯🇵 Native Audio • JLPT")
        bg = data.get("bg_image", "")
        level = data.get("level", "JLPT N5")
        cat = data.get("category", "").lower()
        
        if "transit" in cat or "subway" in cat or "metro" in cat:
            theme = "transit"
        elif "kombini" in cat or "checkout" in cat or "coffee" in cat:
            theme = "kombini"
        elif "izakaya" in cat or "dining" in cat or "ramen" in cat:
            theme = "izakaya"
        else:
            theme = "shopping"
            
        news_bg = rdir_path / "news_bg.jpg"
        if not bg or not os.path.exists(bg):
            if news_bg.exists():
                bg = str(news_bg)
            else:
                bg = wallpapers.get(theme, wallpapers["shopping"])

        # 1. 16:9 Cover
        if master_asset_path.exists():
            shutil.copyfile(str(master_asset_path), out_16_9)
            print(f"✓ Preserved authentic 4K AI Master Thumbnail: {out_16_9}")
        else:
            generate_serialized_thumbnail(ep_num, hook, jp, tag, bg, out_16_9, level)

        # 2. 9:16 Shorts Cover
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
            category_theme=theme,
            jlpt_level=level,
            bg_image_path=bg
        )
    else:
        # Fallback for trend-radar episodes (reads production_spec.json)
        spec_file = rdir_path / "production_spec.json"
        if spec_file.exists():
            with open(spec_file) as fp:
                spec = json.load(fp)
            long_spec = spec.get("long_form", {})
            shorts_spec = spec.get("shorts", {})
            level = spec.get("target_jlpt_level", "JLPT N5")
            playlist = spec.get("matched_playlist", "")
            
            if "交通" in playlist or "Transit" in playlist:
                theme = "transit"
            elif "便利店" in playlist or "Kombini" in playlist:
                theme = "kombini"
            elif "居酒屋" in playlist or "Izakaya" in playlist:
                theme = "izakaya"
            else:
                theme = "anime"
                
            news_bg = rdir_path / "news_bg.jpg"
            if news_bg.exists():
                bg = str(news_bg)
            else:
                bg = wallpapers.get(theme, wallpapers["anime"])
            
            if master_asset_path.exists():
                shutil.copyfile(str(master_asset_path), out_16_9)
                print(f"✓ Preserved authentic 4K AI Master Thumbnail: {out_16_9}")
            else:
                hook = long_spec.get("english_hook", "JAPAN TREND")
                jp = long_spec.get("japanese_key_phrase", spec.get("topic_title", "Japan Trend"))
                tag = long_spec.get("bottom_tag", f"[{level}] Native Audio • Pop Culture Trend")
                generate_serialized_thumbnail(ep_num, hook, jp, tag, bg, out_16_9, level)
            
            generate_shorts_thumbnail(
                ep_num=sh_num,
                english_hook=shorts_spec.get("hook_title", "JAPAN TREND"),
                japanese_sentence=shorts_spec.get("jp_sentence", ""),
                kana_sentence=shorts_spec.get("kana_sentence", ""),
                romaji_sentence=shorts_spec.get("romaji_sentence", ""),
                en_translation=shorts_spec.get("en_translation", ""),
                output_path=out_9_16,
                category_theme=theme,
                jlpt_level=level,
                bg_image_path=bg
            )
        else:
            if master_asset_path.exists():
                shutil.copyfile(str(master_asset_path), out_16_9)
                print(f"✓ Preserved authentic 4K AI Master Thumbnail: {out_16_9}")
            else:
                bg = wallpapers["anime"]
                generate_serialized_thumbnail(ep_num, "JAPAN TREND", "日本語を話そう", f"[{jlpt_level}] Native Audio", bg, out_16_9, "JLPT N5")
                
            generate_shorts_thumbnail(
                ep_num=sh_num,
                english_hook="JAPAN TREND",
                japanese_sentence="日本語を話そう",
                kana_sentence="にほんごをはなそう",
                romaji_sentence="Nihongo o hanasou",
                en_translation="Let's speak Japanese!",
                output_path=out_9_16,
                category_theme="anime",
                jlpt_level="JLPT N5"
            )
    print(f"✅ Finished updating cover for {dir_name} (Short: SH.{sh_num:02d})")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TokyoFlow Master Thumbnail Factory")
    parser.add_argument("--dir", type=str, help="Target release directory to process")
    parser.add_argument("--episode", type=int, help="Episode number to process (e.g. 13)")
    parser.add_argument("--sh-num", type=int, help="Sequential Shorts number (e.g. 9 for SH.09)")
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
        # Default single target: latest release (E13)
        latest_dir = "docs/youtube_releases/E13-anime_sauna_trend-v1.0"
        if os.path.exists(latest_dir):
            print(f"ℹ️ No flags passed. Running incremental single-target on latest release: {latest_dir}")
            process_release_dir(latest_dir, sh_num=9)
        else:
            print("Please specify --dir <PATH>, --episode <NUM>, or --all")

