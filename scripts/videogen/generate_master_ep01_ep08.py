#!/usr/bin/env python3
"""
TokyoFlow Japanese • Golden Master Thumbnail & Cover Factory (EP.01 ~ EP.08)
Unified, production-grade implementation strictly adhering to the Golden Master Standard:
- 16:9 Long-Form 4K/Full HD Covers (thumbnail.jpg, 1920x1080)
- 9:16 Vertical Viral Shorts Covers (short_thumbnail.jpg, 1080x1920)
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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
    # WL01 uses Hiragino Sans GB for ultra bold hook rendering
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

EPISODES_CONFIG = [
    {
        "ep_num": 1,
        "sh_num": 1,
        "folder": "E01-Yamanote_Transit-v1.0",
        "jlpt": "JLPT N4",
        "video_id_long": "yN6dTC-LBz8",
        "video_id_short": "luY_kYPz5Bo",
        "hook_lines": ["TRAIN HACK", "YAMANOTE LINE"],
        "sub_hook": "STATION ANNOUNCEMENTS",
        "jp_line1": "点字ブロックの内側へ",
        "jp_line2": "お下がりください。",
        "grammar_tag": "JLPT N4 Grammar: ~の内側へ (Direction / Boundary)",
        "en_translation": '"Please stand behind the yellow tactile safety line."',
        "context_note": "Essential survival phrase heard at all JR Tokyo stations",
        "location_tag": "Setting: JR Shinjuku Station • Yamanote Line",
        "bg_16_9": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep01_yamanote_16_9_1791043147876.jpg",
        "bg_9_16": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep01_yamanote_9_16_1791043161193.jpg",
        "romaji": "Tenji burokku no uchigawa e osagari kudasai"
    },
    {
        "ep_num": 2,
        "sh_num": 2,
        "folder": "E02-Kombini_Checkout-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "6er1tWAH_oQ",
        "video_id_short": "npUV2_Ilid8",
        "hook_lines": ["7-ELEVEN", "CHECKOUT HACK"],
        "sub_hook": "KOMBINI SURVIVAL",
        "jp_line1": "レジ袋は結構です、",
        "jp_line2": "袋は大丈夫です！",
        "grammar_tag": "JLPT N5 Grammar: ~は大丈夫です (Polite Refusal)",
        "en_translation": '"No plastic bag needed, thank you."',
        "context_note": "Say it in 2 seconds like a Tokyo local at register",
        "location_tag": "Setting: Shibuya 7-Eleven Register Counter",
        "bg_16_9": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep02_kombini_16_9_1791043178178.jpg",
        "bg_9_16": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep02_kombini_9_16_1791043191774.jpg",
        "romaji": "Fukuro wa daijoubu desu"
    },
    {
        "ep_num": 3,
        "sh_num": 3,
        "folder": "E03-Izakaya_Night-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "B4sN_BkLcOw",
        "video_id_short": "9gMYd5lRwtI",
        "hook_lines": ["IZAKAYA", "ORDER HACK"],
        "sub_hook": "ORDER LIKE A LOCAL",
        "jp_line1": "とりあえず生で、",
        "jp_line2": "ビールをお願いします！",
        "grammar_tag": "JLPT N5 Grammar: とりあえず~で (To Start With)",
        "en_translation": '"Draft beer to start, please!"',
        "context_note": "The gold standard ordering chant at every Tokyo tavern",
        "location_tag": "Setting: Shinbashi Izakaya Alley • Tokyo Nightlife",
        "bg_16_9": "/Users/kilvonwu/.gemini/antigravity/brain/b34d491c-7bb1-4e81-ab7c-51e66a95dc10/ep03_izakaya_16_9_1791043208822.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep03_izakaya_cheers.jpg",
        "romaji": "Toriaezu nama de, biiru o onegaishimasu"
    },
    {
        "ep_num": 4,
        "sh_num": 4,
        "folder": "E04-Akiba_Pilgrimage-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "iaGo6ey75Ws",
        "video_id_short": "GerQ2oL84o8",
        "hook_lines": ["ANIME SHOP", "TAX-FREE HACK"],
        "sub_hook": "AKIHABARA MERCH",
        "jp_line1": "免税手続きは、",
        "jp_line2": "ここでできますか？",
        "grammar_tag": "JLPT N5 Grammar: ~できますか (Potential / Inquiries)",
        "en_translation": '"Can I do tax-free shopping here?"',
        "context_note": "Unlock 10% instant tax savings on anime scale figures",
        "location_tag": "Setting: Akihabara Electric Town • Figure Specialty Store",
        "bg_16_9": "tmp/videogen/real_photos/ep04_akiba_2.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep04_akiba_1.jpg",
        "romaji": "Menzei tetsuzuki wa koko de dekimasu ka?"
    },
    {
        "ep_num": 5,
        "sh_num": 5,
        "folder": "E05-Tokyo_Subway_Rush-v1.0",
        "jlpt": "JLPT N4",
        "video_id_long": "71K0XIHNZLs",
        "video_id_short": "K8E-XXJFu3I",
        "hook_lines": ["SUBWAY HACK", "TOKYO METRO"],
        "sub_hook": "NEVER GET LOST",
        "jp_line1": "乗り越し精算機は、",
        "jp_line2": "どこにありますか？",
        "grammar_tag": "JLPT N4 Grammar: ~はどこにありますか (Asking Location)",
        "en_translation": '"Where is the fare adjustment machine?"',
        "context_note": "Fix IC card balance errors instantly at any metro gate",
        "location_tag": "Setting: Tokyo Metro Station • Ticket Gate & Adjustment",
        "bg_16_9": "tmp/videogen/real_photos/ep05_metro_gates.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep05_metro_platform.jpg",
        "romaji": "Norikoshi seisanki wa doko ni arimasu ka?"
    },
    {
        "ep_num": 6,
        "sh_num": 6,
        "folder": "E06-Kombini_Coffee_ATM-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "kPXKS2r3o8w",
        "video_id_short": "fj-Yto1FF3U",
        "hook_lines": ["ICED COFFEE", "KOMBINI SECRET"],
        "sub_hook": "MACHINE PROTOCOL",
        "jp_line1": "アイスコーヒーのRを、",
        "jp_line2": "ひとつください！",
        "grammar_tag": "JLPT N5 Grammar: ~のRで / ひとつ (Ordering & Quantities)",
        "en_translation": '"One Regular Iced Coffee, please!"',
        "context_note": "Grab ice cup from freezer & brew fresh roast beans",
        "location_tag": "Setting: Modern Tokyo Convenience Store Coffee Counter",
        "bg_16_9": "tmp/videogen/real_photos/ep06_coffee_1.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep06_coffee_3.jpg",
        "romaji": "Aisu koohii no aaru o hitotsu kudasai"
    },
    {
        "ep_num": 7,
        "sh_num": 7,
        "folder": "E07-Ramen_Ticket_Vending-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "jB4I3CicHrs",
        "video_id_short": "4nH8UUKeEDA",
        "hook_lines": ["RAMEN CHANT", "PRO ORDER"],
        "sub_hook": "TICKET MACHINE & NOODLES",
        "jp_line1": "麺硬め・味濃いめ、",
        "jp_line2": "替え玉をお願いします！",
        "grammar_tag": "JLPT N5 Grammar: ~め (Preference) & 替え玉 (Refill)",
        "en_translation": '"Firm noodles, rich broth & extra noodle refill!"',
        "context_note": "Master custom broth chanting at Tokyo ramen counters",
        "location_tag": "Setting: Ikebukuro Authentic Ramen Alley • Tonkotsu Counter",
        "bg_16_9": "tmp/videogen/real_photos/ep07_ichiran_shinjuku.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep07_ichiran_bowl.jpg",
        "romaji": "Men katame, aji koime, kaedama o onegaishimasu"
    },
    {
        "ep_num": 8,
        "sh_num": 8,
        "folder": "E08-Ginza_TaxFree_Shopping-v1.0",
        "jlpt": "JLPT N5",
        "video_id_long": "9GOBcaATRjE",
        "video_id_short": "O2FjmMOFWgM",
        "hook_lines": ["FITTING ROOM", "GINZA HACK"],
        "sub_hook": "SHOPPING ETIQUETTE",
        "jp_line1": "この服を、",
        "jp_line2": "試着してもいいですか？",
        "grammar_tag": "JLPT N5 Grammar: ~てもいいですか (Asking Permission)",
        "en_translation": '"May I try this clothing on in the fitting room?"',
        "context_note": "Polite luxury boutique Japanese for Ginza shopping",
        "location_tag": "Setting: Ginza Flagship Store • Fashion Boutique",
        "bg_16_9": "tmp/videogen/real_photos/ep08_ginza_uniqlo.jpg",
        "bg_9_16": "tmp/videogen/real_photos/ep08_ginza_3.jpg",
        "romaji": "Kono fuku o shichaku shite mo ii desu ka?"
    }
]

# -------------------------------------------------------------------------
# 1. 16:9 Landscape Master Generator (1920x1080)
# -------------------------------------------------------------------------
def render_16_9_master(conf: dict) -> Image.Image:
    width, height = 1920, 1080
    bg_path = conf.get("bg_16_9")
    
    if bg_path and os.path.exists(bg_path):
        raw_img = Image.open(bg_path).convert("RGB")
        src_w, src_h = raw_img.size
        target_ratio = width / height
        src_ratio = src_w / src_h
        
        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            # Center slightly right to give text breathing room on left
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

    # Dark left-to-right cosine gradient fade (smoothly fading out at x=1180)
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    for x in range(width):
        if x < 1180:
            rel = x / 1180.0
            alpha = int(245 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    # Bottom Vignette
    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left Brand Pill
    pill_w, pill_h = 360, 60
    draw.rounded_rectangle([(60, 45), (60 + pill_w, 45 + pill_h)], radius=18, fill=(255, 255, 255))
    font_brand = get_font(26, is_en=True)
    bbox_b = draw.textbbox((0, 0), "TokyoFlow Japanese", font=font_brand)
    bw, bh = bbox_b[2] - bbox_b[0], bbox_b[3] - bbox_b[1]
    draw.text((60 + (pill_w - bw) // 2, 45 + (pill_h - bh) // 2 - bbox_b[1]), "TokyoFlow Japanese", fill=(225, 29, 72), font=font_brand)

    # 2. Top-Right Badge
    ep_str = f"EP.{conf['ep_num']:02d}"
    jlpt_badge = f"{conf['jlpt']} | {ep_str}"
    badge_w, badge_h = 290, 60
    badge_x = width - 60 - badge_w
    draw.rounded_rectangle([(badge_x, 45), (badge_x + badge_w, 45 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), jlpt_badge, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 45 + (badge_h - gh) // 2 - bbox_bg[1]), jlpt_badge, fill=(255, 255, 255), font=font_badge)

    # 3. Giant 3D Yellow Hook (Left Aligned)
    font_hook = get_heavy_hook_font(96)
    hy = 145
    for line in conf["hook_lines"]:
        for dx in range(-5, 6, 2):
            for dy in range(-5, 6, 2):
                draw.text((60 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 115

    # Sub-Hook in Pink
    draw.text((65, 385), conf["sub_hook"], fill=(244, 114, 182), font=get_font(36, is_en=True))

    # 4. Japanese Learning Card (Glassmorphic dark navy with cyan border)
    quote_box_w = 860
    quote_box_y = 450
    draw.rounded_rectangle([(60, quote_box_y), (60 + quote_box_w, quote_box_y + 410)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    
    # Card Header
    draw.text((90, quote_box_y + 25), "[ SURVIVAL JAPANESE BREAKDOWN ]", fill=(56, 189, 248), font=get_font(22, is_en=True))
    
    font_jp = get_font(38)
    draw.text((90, quote_box_y + 70), conf["jp_line1"], fill=(255, 255, 255), font=font_jp)
    draw.text((90, quote_box_y + 125), conf["jp_line2"], fill=(254, 240, 138), font=font_jp)
    
    draw.text((90, quote_box_y + 200), conf["grammar_tag"], fill=(244, 114, 182), font=get_font(23))
    draw.text((90, quote_box_y + 245), conf["en_translation"], fill=(226, 232, 240), font=get_font(24, is_en=True))
    draw.text((90, quote_box_y + 300), conf["context_note"], fill=(148, 163, 184), font=get_font(20, is_en=True))
    draw.text((90, quote_box_y + 345), conf["location_tag"], fill=(56, 189, 248), font=get_font(20, is_en=True))

    # 5. Full-Width Crimson Conversion Ribbon
    draw.rounded_rectangle([(60, height - 120), (width - 60, height - 45)], radius=16, fill=(225, 29, 72))
    ribbon_txt = " 100% NATIVE TOKYO AUDIO  •  SHADOWING PRACTICE  •  FULL VOCAB & GRAMMAR BREAKDOWN"
    font_ribbon = get_font(24, is_en=True)
    bbox_rb = draw.textbbox((0, 0), ribbon_txt, font=font_ribbon)
    rw, rh = bbox_rb[2] - bbox_rb[0], bbox_rb[3] - bbox_rb[1]
    draw.text((60 + (width - 120 - rw) // 2, height - 120 + (75 - rh) // 2 - bbox_rb[1]), ribbon_txt, fill=(255, 255, 255), font=font_ribbon)

    return img

# -------------------------------------------------------------------------
# 2. 9:16 Vertical Shorts Master Generator (1080x1920)
# -------------------------------------------------------------------------
def render_9_16_master(conf: dict) -> Image.Image:
    width, height = 1080, 1920
    bg_path = conf.get("bg_9_16")
    
    if bg_path and os.path.exists(bg_path):
        raw_img = Image.open(bg_path).convert("RGB")
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
    
    # Top Gradient for Badges and Hook (stronger dark fade for ultra legibility)
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

    sh_code = f"SH.{conf['sh_num']:02d} • {conf['jlpt']}"
    badge_w, badge_h = 310, 65
    badge_x = width - 50 - badge_w
    draw.rounded_rectangle([(badge_x, 50), (badge_x + badge_w, 50 + badge_h)], radius=18, fill=(225, 29, 72))
    font_badge = get_font(26, is_en=True)
    bbox_bg = draw.textbbox((0, 0), sh_code, font=font_badge)
    gw, gh = bbox_bg[2] - bbox_bg[0], bbox_bg[3] - bbox_bg[1]
    draw.text((badge_x + (badge_w - gw) // 2, 50 + (badge_h - gh) // 2 - bbox_bg[1]), sh_code, fill=(255, 255, 255), font=font_badge)

    # 2. Punchy 3D Action Hook
    font_hook_sh = get_heavy_hook_font(74)
    hy = 150
    for line in conf["hook_lines"]:
        for dx in range(-4, 5, 2):
            for dy in range(-4, 5, 2):
                draw.text((50 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook_sh)
        draw.text((50, hy), line, fill=(254, 240, 138), font=font_hook_sh)
        hy += 88

    # Pink Sub-Hook
    draw.text((55, hy + 5), conf["sub_hook"], fill=(244, 114, 182), font=get_font(28, is_en=True))

    # 3. Center/Bottom Learning Card (Glassmorphic container)
    card_x, card_y = 40, 1150
    card_w, card_h = 1000, 720
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=3)

    # Card Top Header
    draw.text((card_x + 35, card_y + 25), "[ TOKYO SURVIVAL GYM ]", fill=(56, 189, 248), font=get_font(24, is_en=True))
    draw.rounded_rectangle([(card_x + card_w - 240, card_y + 20), (card_x + card_w - 30, card_y + 62)], radius=10, fill=(225, 29, 72))
    draw.text((card_x + card_w - 225, card_y + 28), f"{conf['jlpt']} ESSENTIAL", fill=(255, 255, 255), font=get_font(19, is_en=True))

    draw.line([(card_x + 35, card_y + 75), (card_x + card_w - 35, card_y + 75)], fill=(51, 65, 85), width=2)

    # Japanese Target Sentence
    full_jp = f"{conf['jp_line1']} {conf['jp_line2']}".strip()
    jp_size = 46
    font_jp = get_font(jp_size)
    bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    while (bbox_jp[2] - bbox_jp[0]) > (card_w - 70) and jp_size > 34:
        jp_size -= 2
        font_jp = get_font(jp_size)
        bbox_jp = draw.textbbox((0, 0), full_jp, font=font_jp)
    draw.text((card_x + 35, card_y + 100), full_jp, fill=(255, 255, 255), font=font_jp)

    # Romaji
    draw.text((card_x + 35, card_y + 168), conf.get("romaji", ""), fill=(254, 240, 138), font=get_font(25, is_en=True))
    
    # English Translation
    draw.text((card_x + 35, card_y + 215), conf["en_translation"], fill=(226, 232, 240), font=get_font(25, is_en=True))

    # Grammar Tag Pill inside card
    draw.rounded_rectangle([(card_x + 35, card_y + 280), (card_x + card_w - 35, card_y + 345)], radius=12, fill=(15, 23, 42, 220), outline=(244, 114, 182), width=2)
    draw.text((card_x + 55, card_y + 298), conf["grammar_tag"], fill=(244, 114, 182), font=get_font(21))

    # 4. CTA Action Banner at Bottom of Card
    cta_x = card_x + 30
    cta_y = card_y + 380
    cta_w = card_w - 60
    cta_h = 295
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=18, fill=(225, 29, 72))
    
    ep_str = f"EP.{conf['ep_num']:02d}"
    draw.text((cta_x + 35, cta_y + 35), f"WATCH FULL BREAKDOWN ({ep_str})", fill=(255, 255, 255), font=get_font(34, is_en=True))
    draw.text((cta_x + 35, cta_y + 95), "Complete Vocabulary • Grammar Rules • Shadowing Gym", fill=(254, 240, 138), font=get_font(22, is_en=True))
    draw.text((cta_x + 35, cta_y + 145), f"Tap Related Video Below  •  TokyoFlow Japanese", fill=(241, 245, 249), font=get_font(20, is_en=True))

    return img

def render_all_master_covers():
    print("🚀 Rendering All Golden Master Thumbnails (EP.01 ~ EP.08)...")
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    for conf in EPISODES_CONFIG:
        folder_name = conf["folder"]
        rel_dir = RELEASES_DIR / folder_name
        rel_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 16:9 Landscape
        img_16_9 = render_16_9_master(conf)
        out_16_9 = rel_dir / "thumbnail.jpg"
        img_16_9.save(str(out_16_9), "JPEG", quality=95)
        
        asset_16_9 = ASSETS_DIR / f"{folder_name}_thumb.jpg"
        img_16_9.save(str(asset_16_9), "JPEG", quality=95)
        
        # 2. 9:16 Vertical Shorts
        img_9_16 = render_9_16_master(conf)
        out_9_16 = rel_dir / "short_thumbnail.jpg"
        img_9_16.save(str(out_9_16), "JPEG", quality=95)
        
        print(f"  ✓ [{conf['folder']}] 16:9 -> {out_16_9.name} ({out_16_9.stat().st_size/1024:.1f} KB) | 9:16 -> {out_9_16.name} ({out_9_16.stat().st_size/1024:.1f} KB)")

if __name__ == "__main__":
    render_all_master_covers()
