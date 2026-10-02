#!/usr/bin/env python3
"""
TokyoFlow YouTube Shorts Thumbnail Designer
Generates minimalist, high-CTR, human-centric 9:16 vertical covers for all YouTube Shorts (SH.XX).
Adheres strictly to the TokyoFlow visual branding language (Zero emojis, high contrast, clean typography).
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RELEASES_DIR = PROJECT_ROOT / "docs" / "youtube_releases"

FONT_JP_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_EN_HEAVY = "/System/Library/Fonts/Helvetica.ttc"

SHORTS_CONFIG = [
    {
        "ep_num": 1,
        "sh_code": "SH.01",
        "folder": "E01-Yamanote_Transit-v1.0",
        "hook_main": "TRAIN HACK",
        "hook_sub": "STATION ANNOUNCEMENTS",
        "jp_phrase": "点字ブロックの内側へ",
        "romaji": "Tenji burokku no uchigawa e",
        "en_meaning": "Behind The Yellow Line",
        "accent_color": (16, 185, 129),     # Emerald Yamanote
        "secondary_color": (56, 189, 248),  # Sky Cyan
        "location": "SHINJUKU STATION • YAMANOTE"
    },
    {
        "ep_num": 2,
        "sh_code": "SH.02",
        "folder": "E02-Kombini_Checkout-v1.0",
        "hook_main": "7-ELEVEN",
        "hook_sub": "CHECKOUT SURVIVAL",
        "jp_phrase": "袋は大丈夫です",
        "romaji": "Fukuro wa daijoubu desu",
        "en_meaning": "No Bag Needed, Thanks",
        "accent_color": (249, 115, 22),     # Kombini Orange
        "secondary_color": (250, 204, 21),  # Warm Yellow
        "location": "SHIBUYA 7-ELEVEN • TOKYO"
    },
    {
        "ep_num": 3,
        "sh_code": "SH.03",
        "folder": "E03-Izakaya_Night-v1.0",
        "hook_main": "IZAKAYA",
        "hook_sub": "ORDER LIKE A LOCAL",
        "jp_phrase": "とりあえず生で！",
        "romaji": "Toriaezu nama de!",
        "en_meaning": "Draft Beer To Start!",
        "accent_color": (234, 179, 8),      # Amber Beer Gold
        "secondary_color": (249, 115, 22),  # Warm Glow
        "location": "SHINBASHI IZAKAYA ALLEY"
    },
    {
        "ep_num": 4,
        "sh_code": "SH.04",
        "folder": "E04-Akiba_Pilgrimage-v1.0",
        "hook_main": "ANIME SHOP",
        "hook_sub": "TAX-FREE MERCH",
        "jp_phrase": "免税できますか？",
        "romaji": "Menzei dekimasu ka?",
        "en_meaning": "Can I Get Tax-Free?",
        "accent_color": (168, 85, 247),     # Cyberpunk Purple
        "secondary_color": (236, 72, 153),  # Neon Pink
        "location": "AKIHABARA ELECTRIC TOWN"
    },
    {
        "ep_num": 5,
        "sh_code": "SH.05",
        "folder": "E05-Tokyo_Subway_Rush-v1.0",
        "hook_main": "SUBWAY HACK",
        "hook_sub": "NEVER GET LOST",
        "jp_phrase": "精算機はどこですか？",
        "romaji": "Seisanki wa doko desu ka?",
        "en_meaning": "Where Is Fare Adjustment?",
        "accent_color": (6, 182, 212),      # Tokyo Metro Cyan
        "secondary_color": (59, 130, 246),  # Blue Line
        "location": "TOKYO METRO • MARUNOUCHI"
    },
    {
        "ep_num": 6,
        "sh_code": "SH.06",
        "folder": "E06-Kombini_Coffee_ATM-v1.0",
        "hook_main": "ICED COFFEE",
        "hook_sub": "KOMBINI MACHINE SECRET",
        "jp_phrase": "アイスコーヒーのRで",
        "romaji": "Aisu koohii no aaru de",
        "en_meaning": "Regular Iced Coffee",
        "accent_color": (217, 119, 6),      # Roasted Coffee Amber
        "secondary_color": (251, 191, 36),  # Crema Gold
        "location": "ROPPONGI LAWSON • TOKYO"
    },
    {
        "ep_num": 7,
        "sh_code": "SH.07",
        "folder": "E07-Ramen_Ticket_Vending-v1.0",
        "hook_main": "RAMEN CHANT",
        "hook_sub": "PRO CUSTOM ORDER",
        "jp_phrase": "硬め・濃いめ・替え玉！",
        "romaji": "Katame, koime, kaedama!",
        "en_meaning": "Firm Broth & Extra Noodles",
        "accent_color": (239, 68, 68),      # Fiery Ramen Red
        "secondary_color": (245, 158, 11),  # Tonkotsu Gold
        "location": "IKEBUKURO RAMEN ALLEY"
    },
    {
        "ep_num": 8,
        "sh_code": "SH.08",
        "folder": "E08-Ginza_TaxFree_Shopping-v1.0",
        "hook_main": "FITTING ROOM",
        "hook_sub": "GINZA SHOPPING ETIQUETTE",
        "jp_phrase": "試着してもいいですか？",
        "romaji": "Shichaku shite mo ii desu ka?",
        "en_meaning": "Can I Try This On?",
        "accent_color": (236, 72, 153),     # Luxury Rose Gold
        "secondary_color": (168, 85, 247),  # Fashion Lavender
        "location": "GINZA SHOPPING BOULEVARD",
        "jlpt_level": "JLPT N5"
    },
    {
        "ep_num": 9,
        "sh_code": "SH.09",
        "folder": "E09-anime_sauna_trend-v1.0",
        "hook_main": "ANIME SAUNA",
        "hook_sub": "STUDIO OPENS REAL SAUNA",
        "jp_phrase": "アニメの会社がサウナを作った！",
        "romaji": "Anime no kaisha ga sauna o tsukutta!",
        "en_meaning": "Anime Studio Made A Sauna!",
        "accent_color": (236, 72, 153),     # Neon Anime Pink
        "secondary_color": (250, 204, 21),  # Solar Sauna Yellow
        "location": "TOKYO ANIME STUDIO • SAUNA",
        "jlpt_level": "JLPT N5"
    }
]

def create_shorts_cover(item: dict) -> Image.Image:
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (10, 14, 24)) # Deep Tokyo Night
    draw = ImageDraw.Draw(img)

    # 1. Subtle Aesthetic Background Gradient & Glow Orbs
    accent = item["accent_color"]
    sec = item["secondary_color"]

    # Background ambient circular radial lights
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Top Orb
    glow_draw.ellipse([W//2 - 400, 100, W//2 + 400, 900], fill=(accent[0], accent[1], accent[2], 40))
    # Mid-lower Orb
    glow_draw.ellipse([W//2 - 450, 800, W//2 + 450, 1700], fill=(sec[0], sec[1], sec[2], 30))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.paste(glow, (0, 0), glow)

    # 2. Typography Setup
    font_brand = ImageFont.truetype(FONT_EN_HEAVY, 36)
    font_sh_badge = ImageFont.truetype(FONT_EN_HEAVY, 42)
    font_hook_giant = ImageFont.truetype(FONT_EN_HEAVY, 110)
    font_hook_sub = ImageFont.truetype(FONT_EN_HEAVY, 40)
    font_jp_phrase = ImageFont.truetype(FONT_JP_BOLD, 86)
    font_romaji = ImageFont.truetype(FONT_EN_HEAVY, 44)
    font_meaning = ImageFont.truetype(FONT_EN_HEAVY, 46)
    font_tag = ImageFont.truetype(FONT_EN_HEAVY, 30)

    # 3. Top Header: TokyoFlow Brand Capsule + JLPT Level Badge + SH Code Badge
    pill_h = 64
    pill_y = 90

    # Brand Pill (Solid white pill, bold crimson red text, auto-sized to fit text perfectly)
    brand_text = "TokyoFlow"
    font_brand_bold = ImageFont.truetype(FONT_EN_HEAVY, 36)
    bbox_b = draw.textbbox((0, 0), brand_text, font=font_brand_bold)
    bw = bbox_b[2] - bbox_b[0]
    bh = bbox_b[3] - bbox_b[1]
    pill_bw = bw + 52
    draw.rounded_rectangle([70, pill_y, 70 + pill_bw, pill_y + pill_h], radius=pill_h // 2, fill=(255, 255, 255), outline=(220, 38, 38), width=2)
    tx_b = 70 + (pill_bw - bw) // 2 - bbox_b[0]
    ty_b = pill_y + (pill_h - bh) // 2 - bbox_b[1]
    draw.text((tx_b, ty_b), brand_text, font=font_brand_bold, fill=(220, 38, 38))

    # JLPT Level Badge (Prominent dark glassmorphic badge with golden yellow level text)
    level_text = item.get("jlpt_level", "JLPT N5")
    font_level = ImageFont.truetype(FONT_EN_HEAVY, 32)
    bbox_l = draw.textbbox((0, 0), level_text, font=font_level)
    lw = bbox_l[2] - bbox_l[0]
    lh = bbox_l[3] - bbox_l[1]
    pill_lw = lw + 44
    pill_lx = 70 + pill_bw + 18
    draw.rounded_rectangle([pill_lx, pill_y, pill_lx + pill_lw, pill_y + pill_h], radius=pill_h // 2, fill=(24, 32, 47), outline=(56, 189, 248), width=2)
    tx_l = pill_lx + (pill_lw - lw) // 2 - bbox_l[0]
    ty_l = pill_y + (pill_h - lh) // 2 - bbox_l[1]
    draw.text((tx_l, ty_l), level_text, font=font_level, fill=(250, 204, 21))

    # SH Code Badge (High-Contrast Theme Accent Pill)
    sh_text = item["sh_code"]
    bbox_s = draw.textbbox((0, 0), sh_text, font=font_sh_badge)
    sw = bbox_s[2] - bbox_s[0]
    sh = bbox_s[3] - bbox_s[1]
    pill_sw = sw + 44
    draw.rounded_rectangle([W - 70 - pill_sw, pill_y, W - 70, pill_y + pill_h], radius=pill_h // 2, fill=accent)
    tx_s = W - 70 - pill_sw + (pill_sw - sw) // 2 - bbox_s[0]
    ty_s = pill_y + (pill_h - sh) // 2 - bbox_s[1]
    draw.text((tx_s, ty_s), sh_text, font=font_sh_badge, fill=(10, 14, 24))

    # Location Subtitle Pill
    draw.text((75, 185), item["location"], font=font_tag, fill=(148, 163, 184))

    # 4. Hero Section: Minimalist 1-2 Words Punchy Hook
    hook_main = item["hook_main"]
    hook_sub = item["hook_sub"]
    
    # 3D Drop Shadow on Main Hook
    draw.text((75, 275), hook_main, font=font_hook_giant, fill=(0, 0, 0, 180))
    draw.text((70, 270), hook_main, font=font_hook_giant, fill=sec)
    
    draw.text((75, 405), hook_sub, font=font_hook_sub, fill=(226, 232, 240))

    # Decorative Accent Line
    draw.rectangle([70, 475, 300, 483], fill=accent)

    # 5. Center Human Feature: Glassmorphic Japanese Hero Card
    card_top = 530
    card_h = 920
    card_w = W - 140
    
    # Card Background with Glow Border
    draw.rounded_rectangle([70, card_top, 70 + card_w, card_top + card_h], radius=40, fill=(15, 23, 42, 230), outline=accent, width=4)
    
    # Inner Tag "SURVIVAL JAPANESE"
    draw.rounded_rectangle([110, card_top + 45, 470, card_top + 105], radius=24, fill=(30, 41, 59), outline=(51, 65, 85), width=2)
    draw.text((135, card_top + 60), "TOKYO SURVIVAL PHRASE", font=font_tag, fill=(148, 163, 184))

    # Giant Japanese Phrase (Auto-scale to never overflow card_w - 80)
    jp_phrase = item["jp_phrase"]
    jp_size = 86
    font_jp = ImageFont.truetype(FONT_JP_BOLD, jp_size)
    bbox_jp = draw.textbbox((0, 0), jp_phrase, font=font_jp)
    jpw = bbox_jp[2] - bbox_jp[0]
    while jpw > card_w - 80 and jp_size > 44:
        jp_size -= 4
        font_jp = ImageFont.truetype(FONT_JP_BOLD, jp_size)
        bbox_jp = draw.textbbox((0, 0), jp_phrase, font=font_jp)
        jpw = bbox_jp[2] - bbox_jp[0]
    draw.text((110, card_top + 150), jp_phrase, font=font_jp, fill=(255, 255, 255))

    # Romaji (Auto-scale to never overflow card_w - 80)
    romaji_text = item["romaji"]
    rom_size = 44
    font_rom = ImageFont.truetype(FONT_EN_HEAVY, rom_size)
    bbox_rom = draw.textbbox((0, 0), romaji_text, font=font_rom)
    rw = bbox_rom[2] - bbox_rom[0]
    while rw > card_w - 80 and rom_size > 24:
        rom_size -= 2
        font_rom = ImageFont.truetype(FONT_EN_HEAVY, rom_size)
        bbox_rom = draw.textbbox((0, 0), romaji_text, font=font_rom)
        rw = bbox_rom[2] - bbox_rom[0]
    draw.text((110, card_top + 340), romaji_text, font=font_rom, fill=(250, 204, 21))

    # Divider line
    draw.line([(110, card_top + 430), (W - 110, card_top + 430)], fill=(51, 65, 85), width=2)

    # English Translation Box
    draw.text((110, card_top + 470), "ENGLISH MEANING:", font=font_tag, fill=(100, 116, 139))
    draw.text((110, card_top + 520), f'"{item["en_meaning"]}"', font=font_meaning, fill=(241, 245, 249))

    # Audio Shadowing Status Badge inside Card
    draw.rounded_rectangle([110, card_top + 680, W - 110, card_top + 840], radius=28, fill=(30, 41, 59, 180), outline=(71, 85, 105), width=2)
    draw.text((145, card_top + 720), "3-STEP INTERACTIVE SHADOWING", font=font_brand, fill=accent)
    draw.text((145, card_top + 775), "Listen • Break Down • Speak With AI Pitch", font=font_tag, fill=(203, 213, 225))

    # 6. Bottom Conversion Strip: App & Subscription
    draw.rounded_rectangle([70, H - 380, W - 70, H - 120], radius=32, fill=(2, 6, 23, 240), outline=(30, 41, 59), width=2)
    draw.text((110, H - 340), "TOKYOFLOW - JAPANESE SPEAKING", font=font_brand, fill=(255, 255, 255))
    draw.text((110, H - 280), "Real Scenarios • 10,000+ Native Words & Audio", font=font_tag, fill=(148, 163, 184))
    draw.text((110, H - 210), "Available on the App Store", font=font_tag, fill=sec)

    return img

def generate_all():
    print("🎨 Generating all new minimalist, high-CTR YouTube Shorts covers (SH.01 ~ SH.08)...")
    for idx, conf in enumerate(SHORTS_CONFIG):
        folder = conf["folder"]
        sh_code = conf["sh_code"]
        target_dir = RELEASES_DIR / folder
        target_dir.mkdir(parents=True, exist_ok=True)
        
        cover_img = create_shorts_cover(conf)
        out_path = target_dir / "short_thumbnail.jpg"
        cover_img.save(str(out_path), "JPEG", quality=95)
        print(f"  ✅ Saved [{sh_code}] cover -> {out_path.relative_to(PROJECT_ROOT)} ({out_path.stat().st_size / 1024:.1f} KB)")
        
        if idx == 0:
            std_format_path = PROJECT_ROOT / "output" / "日语短片标准格式.jpg"
            cover_img.save(str(std_format_path), "JPEG", quality=95)
            print(f"  🌟 Standard format reference updated -> {std_format_path}")

if __name__ == "__main__":
    generate_all()
