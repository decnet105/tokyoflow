#!/usr/bin/env python3
"""
TokyoFlow Japanese • Master YouTube Shorts Factory (Interactive Shadowing Engine)
Produces 9:16 vertical videos (1080x1920) with a 4-Stage Progressive Shadowing Engine:
1. Hook & Scenario Preview (Andrew)
2. STEP 1:  Listen at Native Speed with Real-Time Millisecond Karaoke Glow (Nanami)
3. STEP 2:  Slow Breakdown (0.8x) + Culture/Grammar Pro-Tip (Andrew & Nanami)
4. STEP 3:  YOUR TURN (3-2-1 Beep Countdown + Silent Recording Window + Animated Waveform & Syllable Guide)
5. STEP 4:  AI Pitch Accent Scoring (98.4% Match Chime) + TokyoFlow App CTA
"""

import os
import sys
import math
import shutil
import asyncio
import subprocess
import edge_tts
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timing_engine import extract_tokens_from_text, align_sentence_tokens_with_audio

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def synth_audio(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def generate_beep(freq: int, duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"sine=frequency={freq}:duration={duration}",
        "-c:a", "libmp3lame", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_silence(duration: float, out_path: str):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-c:a", "libmp3lame", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

SHORTS_CONFIGS = [
    {
        "ep_num": 1,
        "folder": "E01-Yamanote_Transit-v1.0",
        "district": "Shinjuku Station • ",
        "category": "Tokyo Transit • Yamanote Line",
        "hook_title": "WHAT TOKYO TRAIN STATIONS\nACTUALLY ANNOUNCE!",
        "hook_audio_en": "Here is the one sentence you will hear a hundred times in Tokyo train stations. Let's master it!",
        "jp_sentence": "",
        "kana_sentence": "",
        "romaji_sentence": "Kiiroi tenji burokku no uchigawa made osagari kudasai.",
        "en_translation": "Please stand behind the yellow tactile warning blocks.",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "kiiroi", "meaning": "Yellow"},
            {"orig": "", "kana": "", "romaji": "tenji burokku no", "meaning": "Tactile block"},
            {"orig": "", "kana": "", "romaji": "uchigawa made", "meaning": "Inside line"},
            {"orig": "", "kana": "", "romaji": "osagari", "meaning": "Step back"},
            {"orig": "", "kana": "", "romaji": "kudasai", "meaning": "Please"}
        ],
        "pro_tip_title": " LOCAL JR PRO-TIP",
        "pro_tip_body": "Notice ''. In Japanese, ' + verb stem + ' is the polite command formula used across all Tokyo public transit!",
        "pro_tip_audio_en": "Notice osagari kudasai. O plus verb stem plus kudasai is the polite command formula.",
        "yt_short_title": "What Tokyo Train Stations ACTUALLY Announce!  #Shorts #LearnJapanese",
        "slug": "yamanote_transit"
    },
    {
        "ep_num": 2,
        "folder": "E02-Kombini_Checkout-v1.0",
        "district": "7-Eleven Tokyo • ",
        "category": "Kombini Protocol • Checkout",
        "hook_title": "SURVIVE TOKYO 7-ELEVEN\nIN 30 SECONDS!",
        "hook_audio_en": "Every convenience store clerk in Tokyo will ask you this exact question!",
        "jp_sentence": "",
        "kana_sentence": "",
        "romaji_sentence": "Obentou atatamemasu ka? Fukuro wa otsuke shimasu ka?",
        "en_translation": "Would you like your bento warmed up? Do you need a plastic bag?",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "obentou", "meaning": "Bento meal"},
            {"orig": "", "kana": "", "romaji": "atatamemasu ka", "meaning": "Warm up?"},
            {"orig": "", "kana": "", "romaji": "fukuro wa", "meaning": "Bag"},
            {"orig": "", "kana": "", "romaji": "otsuke", "meaning": "Attach / Add"},
            {"orig": "", "kana": "", "romaji": "shimasu ka", "meaning": "Shall I?"}
        ],
        "pro_tip_title": " SURVIVAL RESPONSE HACK",
        "pro_tip_body": "To accept: say '' (Onegaishimasu).\nTo decline: wave your hand and say '' (Daijoubu desu).",
        "pro_tip_audio_en": "To accept, say onegaishimasu. To decline, simply say daijoubu desu.",
        "yt_short_title": "How to Survive Tokyo 7-Eleven Checkout in 30s  #Shorts #LearnJapanese",
        "slug": "kombini_checkout"
    },
    {
        "ep_num": 3,
        "folder": "E03-Izakaya_Night-v1.0",
        "district": "Shinjuku Omoide Yokocho • ",
        "category": "Izakaya Culture • Tokyo Dining",
        "hook_title": "HOW TOKYO LOCALS\nACTUALLY ORDER AT IZAKAYA!",
        "hook_audio_en": "Here is the magic Japanese phrase that instantly opens your night at any Tokyo izakaya.",
        "jp_sentence": "2",
        "kana_sentence": "",
        "romaji_sentence": "Toriaezu nama-biiru futatsu to, edamame o onegaishimasu!",
        "en_translation": "To start with, two draft beers and edamame please!",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "toriaezu", "meaning": "To start with"},
            {"orig": "", "kana": "", "romaji": "nama-biiru", "meaning": "Draft beer"},
            {"orig": "2", "kana": "", "romaji": "futatsu to", "meaning": "Two and"},
            {"orig": "", "kana": "", "romaji": "edamame o", "meaning": "Edamame"},
            {"orig": "", "kana": "", "romaji": "onegaishimasu", "meaning": "Please"}
        ],
        "pro_tip_title": " TOKYO IZAKAYA SECRET",
        "pro_tip_body": "'' means 'for now / to start with'. Locals always shout '!' the second they sit down!",
        "pro_tip_audio_en": "Toriaezu means for now. Locals shout toriaezu nama the second they sit down.",
        "yt_short_title": "How Locals Order at a Tokyo Izakaya  #Shorts #LearnJapanese",
        "slug": "izakaya_night"
    },
    {
        "ep_num": 4,
        "folder": "E04-Akiba_Pilgrimage-v1.0",
        "district": "Akihabara Electric Town • ",
        "category": "Akihabara Shopping • Anime Figures",
        "hook_title": "HOW TO UNLOCK TAX-FREE\nFIGURES IN AKIHABARA!",
        "hook_audio_en": "Want to buy anime figures in Akihabara? Here is the exact phrase to unlock showcase figures and get tax-free!",
        "jp_sentence": "",
        "kana_sentence": "",
        "romaji_sentence": "Kore, shookeesu kara dashite moraemasu ka? Menzei dekimasu ka?",
        "en_translation": "Could you take this out of the display case? Can I get tax-free?",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "kore", "meaning": "This"},
            {"orig": "", "kana": "", "romaji": "shookeesu kara", "meaning": "From showcase"},
            {"orig": "", "kana": "", "romaji": "dashite moraemasu ka", "meaning": "Take out for me?"},
            {"orig": "", "kana": "", "romaji": "menzei", "meaning": "Tax-free"},
            {"orig": "", "kana": "", "romaji": "dekimasu ka", "meaning": "Can I do?"}
        ],
        "pro_tip_title": " AKIBA TAX-FREE RULE",
        "pro_tip_body": "Over 5,000 yen qualifies for 10% tax refund. Always carry your physical passport and ask ''!",
        "pro_tip_audio_en": "Over 5000 yen qualifies for tax refund. Always carry your passport and ask menzei dekimasu ka.",
        "yt_short_title": "How to Buy Anime Figures in Akihabara Tax-Free!  #Shorts #LearnJapanese",
        "slug": "akiba_pilgrimage"
    },
    {
        "ep_num": 5,
        "folder": "E05-Tokyo_Subway_Rush-v1.0",
        "district": "Tokyo Metro Shibuya • ",
        "category": "Transit & Commute • Subway Hacks",
        "hook_title": "NEVER GET LOST ON\nTHE TOKYO SUBWAY!",
        "hook_audio_en": "Boarded the wrong train in Tokyo? Here is the survival phrase to ask station staff for fare adjustment.",
        "jp_sentence": "",
        "kana_sentence": "",
        "romaji_sentence": "Sumimasen, norikoshi seisan wa doko de dekimasu ka?",
        "en_translation": "Excuse me, where can I do a fare adjustment?",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "sumimasen", "meaning": "Excuse me"},
            {"orig": "", "kana": "", "romaji": "norikoshi seisan wa", "meaning": "Fare adjustment"},
            {"orig": "", "kana": "", "romaji": "doko de", "meaning": "Where"},
            {"orig": "", "kana": "", "romaji": "dekimasu ka", "meaning": "Can I do?"}
        ],
        "pro_tip_title": " SUBWAY FARE ADJUSTMENT HACK",
        "pro_tip_body": "'' (norikoshi seisan) lets you pay the remaining fare at yellow machines next to ticket gates without penalty!",
        "pro_tip_audio_en": "Norikoshi seisan lets you pay the remaining fare at yellow machines next to ticket gates without penalty.",
        "yt_short_title": "Never Get Lost on the Tokyo Subway!  #Shorts #LearnJapanese",
        "slug": "tokyo_subway_rush"
    },
    {
        "ep_num": 6,
        "folder": "E06-Kombini_Coffee_ATM-v1.0",
        "district": "FamilyMart Roppongi • ",
        "category": "Kombini & Daily Life • Coffee Orders",
        "hook_title": "HOW TO ORDER COFFEE\nAT JAPANESE 7-ELEVEN!",
        "hook_audio_en": "Ordering coffee at a Japanese convenience store is totally unique. Here is the exact sentence you need!",
        "jp_sentence": "",
        "kana_sentence": "",
        "romaji_sentence": "Aisu koohii no regyuraa saizu o hitotsu kudasai.",
        "en_translation": "One regular-sized iced coffee, please.",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "aisu koohii no", "meaning": "Iced coffee"},
            {"orig": "", "kana": "", "romaji": "regyuraa saizu o", "meaning": "Regular size"},
            {"orig": "", "kana": "", "romaji": "hitotsu", "meaning": "One item"},
            {"orig": "", "kana": "", "romaji": "kudasai", "meaning": "Please"}
        ],
        "pro_tip_title": " THE ICED COFFEE SECRET",
        "pro_tip_body": "For iced coffee, grab the plastic cup with ice cubes from the freezer section FIRST, bring it to the register, then brew!",
        "pro_tip_audio_en": "Grab the ice cup from the freezer section first, pay at the counter, then brew at the machine.",
        "yt_short_title": "How to Order Coffee at Japanese Convenience Stores  #Shorts #LearnJapanese",
        "slug": "kombini_coffee_atm"
    },
    {
        "ep_num": 7,
        "folder": "E07-Ramen_Ticket_Vending-v1.0",
        "district": "Ikebukuro Ramen Alley • ",
        "category": "Tokyo Dining • Ramen Customization",
        "hook_title": "HOW TO ORDER RAMEN\nLIKE A TOKYO MASTER!",
        "hook_audio_en": "The ramen chef asks for your preferences! Here is the legendary customized order chant.",
        "jp_sentence": "",
        "kana_sentence": " ",
        "romaji_sentence": "Men katame, aji koime, abura oome de onegaishimasu! Kaedama kudasai!",
        "en_translation": "Firm noodles, rich broth, extra oil please! Another noodle refill!",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "men katame", "meaning": "Firm noodles"},
            {"orig": "", "kana": "", "romaji": "aji koime", "meaning": "Rich broth"},
            {"orig": "", "kana": "", "romaji": "abura oome de", "meaning": "Extra oil"},
            {"orig": "", "kana": "", "romaji": "onegaishimasu", "meaning": "Please!"},
            {"orig": "", "kana": "", "romaji": "kaedama kudasai", "meaning": "Refill noodles!"}
        ],
        "pro_tip_title": " RAMEN CUSTOMIZATION TRIO",
        "pro_tip_body": "Noodles:  (katame) /  (futsuu)\nFlavor:  (koime) /  (usume)\nRefill:  (kaedama)!",
        "pro_tip_audio_en": "Remember the trio: Katame for firm noodles, Koime for rich broth, and Kaedama for noodle refills.",
        "yt_short_title": "How to Order Ramen Like a Tokyo Master  #Shorts #LearnJapanese",
        "slug": "ramen_ticket_vending"
    },
    {
        "ep_num": 8,
        "folder": "E08-Ginza_TaxFree_Shopping-v1.0",
        "district": "Ginza Shopping Boulevard • ",
        "category": "Shopping & Fashion • Fitting & Tax-Free",
        "hook_title": "HOW TO SHOP CLOTHES\nIN TOKYO GINZA!",
        "hook_audio_en": "Found the perfect clothes in Ginza? Never enter the fitting room without saying this polite phrase!",
        "jp_sentence": "M",
        "kana_sentence": "",
        "romaji_sentence": "Kore no emu-saizu o shichaku shite mo ii desu ka?",
        "en_translation": "Could I try this on in medium size?",
        "tokens": [
            {"orig": "", "kana": "", "romaji": "kore no", "meaning": "This"},
            {"orig": "M", "kana": "", "romaji": "emu-saizu o", "meaning": "Medium size"},
            {"orig": "", "kana": "", "romaji": "shichaku shite mo", "meaning": "Try on"},
            {"orig": "", "kana": "", "romaji": "ii desu ka", "meaning": "Is it okay?"}
        ],
        "pro_tip_title": " JAPANESE FITTING ROOM ETIQUETTE",
        "pro_tip_body": "'' is 'May I...?'. Always take off shoes before stepping on the carpet inside the fitting room!",
        "pro_tip_audio_en": "Always ask shichaku shite mo ii desu ka before entering, and remove your shoes inside.",
        "yt_short_title": "How to Shop Clothes in Tokyo Ginza!  #Shorts #LearnJapanese",
        "slug": "ginza_taxfree_shopping"
    }
]

def prepare_shorts_background(bg_path: str, width: int = 1080, height: int = 1920) -> Image.Image:
    """Prepares an authentic scene photograph base canvas for 9:16 vertical shorts."""
    if bg_path and os.path.exists(bg_path):
        try:
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
                top = max(0, (src_h - new_h) // 2)
                raw_img = raw_img.crop((0, top, src_w, top + new_h))

            base_img = raw_img.resize((width, height), Image.Resampling.LANCZOS)
            from PIL import ImageEnhance
            base_img = ImageEnhance.Contrast(base_img).enhance(1.15)
            base_img = ImageEnhance.Color(base_img).enhance(1.15)
        except Exception:
            base_img = Image.new("RGB", (width, height), (12, 17, 29))
    else:
        base_img = Image.new("RGB", (width, height), (12, 17, 29))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # 1. Dark atmospheric overlay across whole screen
    draw_ov.rectangle([(0, 0), (width, height)], fill=(10, 14, 23, 140))

    # 2. Top header gradient (y=0..320)
    for y in range(320):
        rel = (320 - y) / 320.0
        alpha = int(180 * (rel ** 1.2))
        draw_ov.line([(0, y), (width, y)], fill=(8, 12, 22, alpha))

    # 3. Bottom footer gradient (y=1450..1920)
    for y in range(1450, height):
        rel = (y - 1450) / 470.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    return Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")

def render_interactive_frame(
    width: int,
    height: int,
    conf: dict,
    active_token_idx: int,
    stage_num: int, # 0: hook, 1: listen, 2: slow/pro-tip, 3: shadow/rec, 4: score/app
    stage_title: str,
    stage_subtext: str,
    speaking_prog: float, # 0.0 to 1.0 during shadow
    total_progress: float,
    frame_idx: int,
    base_canvas: Image.Image = None
) -> Image.Image:
    img = base_canvas.copy() if base_canvas is not None else Image.new("RGB", (width, height), color=(12, 17, 29))
    draw = ImageDraw.Draw(img)

    # 1. Top Header Brand Capsule (y=65..118 - Auto-measured, zero overflow)
    header_str = f"TokyoFlow  •  [{conf.get('jlpt_level', 'JLPT N5')}] SH.{conf['ep_num']:02d}"
    font_brand = get_font(24)
    bbox_hdr = draw.textbbox((0, 0), header_str, font=font_brand)
    hdr_w = bbox_hdr[2] - bbox_hdr[0]
    brand_w = hdr_w + 64
    bx = (width - brand_w) // 2
    draw.rounded_rectangle([(bx, 65), (bx + brand_w, 115)], radius=24, fill=(24, 32, 47, 240), outline=(56, 189, 248), width=2)
    draw.text((bx + 32, 77), header_str, fill=(255, 255, 255), font=font_brand)

    # 3. Hook Title (y=135..240)
    font_hook = get_font(44)
    hook_lines = conf["hook_title"].split("\n")
    cur_hy = 135
    for hline in hook_lines:
        bbox = draw.textbbox((0, 0), hline, font=font_hook)
        hw = bbox[2] - bbox[0]
        hx = (width - hw) // 2
        draw.text((hx + 3, cur_hy + 3), hline, fill=(0, 0, 0), font=font_hook)
        draw.text((hx, cur_hy), hline, fill=(250, 204, 21), font=font_hook)
        cur_hy += 50

    # 4. District / Scenario Pill (y=255..300)
    font_dist = get_font(21)
    dist_text = f" {conf['district']}"
    bbox_d = draw.textbbox((0, 0), dist_text, font=font_dist)
    dw = bbox_d[2] - bbox_d[0] + 40
    dx = (width - dw) // 2
    draw.rounded_rectangle([(dx, 255), (dx + dw, 298)], radius=12, fill=(224, 231, 255), outline=(165, 180, 252), width=1)
    draw.text((dx + 20, 264), dist_text, fill=(49, 46, 129), font=font_dist)

    # 5. Central 3-Tier Dialogue Card (y=320..940, height=620)
    card_x, card_y, card_w, card_h = 50, 320, width - 100, 620
    is_shadow_stage = (stage_num == 3)
    card_border = (239, 68, 68) if is_shadow_stage else (71, 85, 105)
    card_bg = (24, 24, 37) if is_shadow_stage else (30, 41, 59)
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=28, fill=card_bg, outline=card_border, width=4 if is_shadow_stage else 2)

    # Card Top Header
    font_card_head = get_font(22)
    card_header_title = " SHADOWING PRACTICE PHRASE" if is_shadow_stage else " NATIVE TOKYO PHRASE"
    draw.text((card_x + 36, card_y + 24), card_header_title, fill=(239, 68, 68) if is_shadow_stage else (148, 163, 184), font=font_card_head)
    
    # Tag
    level_tag = "SHADOW DRILL" if is_shadow_stage else "NATIVE AUDIO"
    tag_bg = (239, 68, 68) if is_shadow_stage else (244, 63, 94)
    draw.rounded_rectangle([(card_x + card_w - 180, card_y + 18), (card_x + card_w - 30, card_y + 52)], radius=10, fill=tag_bg)
    draw.text((card_x + card_w - 170, card_y + 24), level_tag, fill=(255, 255, 255), font=get_font(18))

    draw.line([(card_x + 30, card_y + 64), (card_x + card_w - 30, card_y + 64)], fill=(51, 65, 85), width=2)

    # 3-Tier Ruby Tokens
    font_jp = get_font(52)
    font_kana = get_font(24)
    font_meaning = get_font(22)

    tokens = conf["tokens"]
    lines = []
    current_line = []
    current_w = 0
    max_line_w = card_w - 70

    for idx, tok in enumerate(tokens):
        bbox_j = draw.textbbox((0, 0), tok["orig"], font=font_jp)
        w_j = bbox_j[2] - bbox_j[0]
        tok_w = max(w_j + 16, 70)
        if current_w + tok_w > max_line_w and len(current_line) > 0:
            lines.append(current_line)
            current_line = [(idx, tok, tok_w)]
            current_w = tok_w
        else:
            current_line.append((idx, tok, tok_w))
            current_w += tok_w + 12
    if current_line:
        lines.append(current_line)

    start_y = card_y + 84
    for line in lines:
        line_total_w = sum(item[2] for item in line) + (len(line) - 1) * 12
        start_x = card_x + (card_w - line_total_w) // 2

        for idx, tok, tok_w in line:
            is_active = (idx == active_token_idx)
            
            if is_active:
                # Active glowing 3D pill
                pill_bg = (251, 191, 36) if not is_shadow_stage else (239, 68, 68)
                pill_outline = (245, 158, 11) if not is_shadow_stage else (255, 255, 255)
                draw.rounded_rectangle(
                    [(start_x - 6, start_y - 6), (start_x + tok_w + 6, start_y + 124)],
                    radius=14,
                    fill=pill_bg,
                    outline=pill_outline,
                    width=3
                )
                # Active bouncing indicator dot / arrow above word
                dot_cx = start_x + tok_w // 2
                draw.ellipse([(dot_cx - 6, start_y - 18), (dot_cx + 6, start_y - 6)], fill=(239, 68, 68) if not is_shadow_stage else (250, 204, 21))
                
                kana_color = (15, 23, 42) if not is_shadow_stage else (255, 255, 255)
                jp_color = (15, 23, 42) if not is_shadow_stage else (255, 255, 255)
                meaning_color = (67, 20, 7) if not is_shadow_stage else (254, 202, 202)
            else:
                kana_color = (56, 189, 248)
                jp_color = (255, 255, 255)
                meaning_color = (148, 163, 184)

            if tok.get("kana"):
                bbox_k = draw.textbbox((0, 0), tok["kana"], font=font_kana)
                kw = bbox_k[2] - bbox_k[0]
                kx = start_x + (tok_w - kw) // 2
                draw.text((kx, start_y), tok["kana"], fill=kana_color, font=font_kana)

            bbox_t = draw.textbbox((0, 0), tok["orig"], font=font_jp)
            tw = bbox_t[2] - bbox_t[0]
            tx = start_x + (tok_w - tw) // 2
            draw.text((tx, start_y + 28), tok["orig"], fill=jp_color, font=font_jp)

            if tok.get("meaning"):
                bbox_m = draw.textbbox((0, 0), tok["meaning"], font=font_meaning)
                mw = bbox_m[2] - bbox_m[0]
                mx = start_x + (tok_w - mw) // 2
                draw.text((mx, start_y + 92), tok["meaning"], fill=meaning_color, font=font_meaning)

            start_x += tok_w + 12

        start_y += 138

    # Romaji Subtitle inside card
    font_romaji = get_font(26)
    bbox_r = draw.textbbox((0, 0), conf["romaji_sentence"], font=font_romaji)
    rw = bbox_r[2] - bbox_r[0]
    rx = card_x + (card_w - rw) // 2
    draw.text((rx, card_y + 395), conf["romaji_sentence"], fill=(254, 240, 138), font=font_romaji)

    # English Translation Box inside card
    draw.rounded_rectangle(
        [(card_x + 24, card_y + 445), (card_x + card_w - 24, card_y + 595)],
        radius=16,
        fill=(15, 23, 42),
        outline=(51, 65, 85),
        width=2
    )
    font_en = get_font(30)
    en_words = conf["en_translation"].split(" ")
    en_lines = []
    cur_el = []
    for ew in en_words:
        cur_el.append(ew)
        test_str = " ".join(cur_el)
        if draw.textbbox((0, 0), test_str, font=font_en)[2] > card_w - 80:
            cur_el.pop()
            en_lines.append(" ".join(cur_el))
            cur_el = [ew]
    if cur_el:
        en_lines.append(" ".join(cur_el))

    cur_ey = card_y + 470 if len(en_lines) == 2 else card_y + 495
    for eline in en_lines:
        bbox_el = draw.textbbox((0, 0), eline, font=font_en)
        elw = bbox_el[2] - bbox_el[0]
        elx = card_x + (card_w - elw) // 2
        draw.text((elx, cur_ey), eline, fill=(248, 250, 252), font=font_en)
        cur_ey += 38

    # 6. Interactive Middle Interactive Zone (y=960..1520, height=560)
    mid_x, mid_y, mid_w, mid_h = 50, 960, width - 100, 560

    if stage_num == 3: #  ACTIVE SHADOWING / SPEAKING MODE
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(35, 14, 20), outline=(239, 68, 68), width=3)
        
        # Red pulsing header
        draw.text((mid_x + 30, mid_y + 24), " REC | LIVE MIC • REPEAT OUT LOUD NOW!", fill=(248, 113, 113), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(85, 30, 40), width=2)

        # Big pulsing microphone badge & prompt
        mic_cx = mid_x + mid_w // 2
        mic_cy = mid_y + 140
        # Draw concentric pulsing audio rings
        pulse_r1 = int(45 + math.sin(frame_idx * 0.3) * 6)
        pulse_r2 = int(58 + math.cos(frame_idx * 0.3) * 8)
        draw.ellipse([(mic_cx - pulse_r2, mic_cy - pulse_r2), (mic_cx + pulse_r2, mic_cy + pulse_r2)], outline=(239, 68, 68, 100), width=2)
        draw.ellipse([(mic_cx - pulse_r1, mic_cy - pulse_r1), (mic_cx + pulse_r1, mic_cy + pulse_r1)], fill=(225, 29, 72), outline=(255, 255, 255), width=2)
        
        font_mic_icon = get_font(36)
        draw.text((mic_cx - 18, mic_cy - 22), "", fill=(255, 255, 255), font=font_mic_icon)

        # Prompt text
        font_mic_prompt = get_font(32)
        prompt_txt = "SPEAK NOW! MATCH NATIVE PITCH & SPEED"
        bbox_p = draw.textbbox((0, 0), prompt_txt, font=font_mic_prompt)
        pw = bbox_p[2] - bbox_p[0]
        draw.text((mid_x + (mid_w - pw) // 2, mid_y + 215), prompt_txt, fill=(255, 255, 255), font=font_mic_prompt)

        # Animated Audio Waveform Bars (22 dynamic bars moving)
        num_bars = 22
        wave_start_x = mid_x + 40
        bar_w = (mid_w - 80) // num_bars - 6
        wave_base_y = mid_y + 310
        for b_i in range(num_bars):
            amp = math.sin((frame_idx * 0.3) + (b_i * 0.5)) * 0.5 + 0.5
            bar_h = int(24 + amp * 70)
            bx_bar = wave_start_x + b_i * (bar_w + 6)
            draw.rounded_rectangle(
                [(bx_bar, wave_base_y - bar_h // 2), (bx_bar + bar_w, wave_base_y + bar_h // 2)],
                radius=6,
                fill=(239, 68, 68) if b_i % 2 == 0 else (244, 114, 182)
            )

        # Speaking Progress Bar inside Shadow Card
        prog_bar_y = mid_y + 380
        draw.text((mid_x + 30, prog_bar_y), "⏱ SHADOWING PACING COUNTDOWN:", fill=(203, 213, 225), font=get_font(22))
        draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + mid_w - 30, prog_bar_y + 64)], radius=12, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
        sp_fill_w = int((mid_w - 60) * max(0.0, min(1.0, speaking_prog)))
        if sp_fill_w > 0:
            draw.rounded_rectangle([(mid_x + 30, prog_bar_y + 34), (mid_x + 30 + sp_fill_w, prog_bar_y + 64)], radius=12, fill=(239, 68, 68))
        
        # Helper coaching text
        draw.text((mid_x + 40, mid_y + 465), " Coaching: Follow the red active word highlight above!", fill=(254, 240, 138), font=get_font(22))
        draw.text((mid_x + 40, mid_y + 500), "Say each syllable in cadence with the Tokyo voice guide.", fill=(203, 213, 225), font=get_font(20))

    elif stage_num == 4: #  AI SCORING & TOKYOFLOW APP RESULT
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(16, 44, 87), outline=(56, 189, 248), width=3)
        draw.text((mid_x + 30, mid_y + 24), " AI PITCH ACCENT EVALUATION", fill=(56, 189, 248), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(30, 58, 138), width=2)

        # Huge 98.4% Score Pill
        draw.rounded_rectangle([(mid_x + 40, mid_y + 90), (mid_x + mid_w - 40, mid_y + 230)], radius=20, fill=(30, 58, 138), outline=(96, 165, 250), width=2)
        font_score = get_font(56)
        score_str = "98.6% MATCH "
        bbox_sc = draw.textbbox((0, 0), score_str, font=font_score)
        scw = bbox_sc[2] - bbox_sc[0]
        draw.text((mid_x + (mid_w - scw) // 2, mid_y + 110), score_str, fill=(250, 204, 21), font=font_score)
        
        font_subscore = get_font(24)
        sub_str = "Tokyo Standard Pitch Accent Verified"
        bbox_sub = draw.textbbox((0, 0), sub_str, font=font_subscore)
        subw = bbox_sub[2] - bbox_sub[0]
        draw.text((mid_x + (mid_w - subw) // 2, mid_y + 180), sub_str, fill=(255, 255, 255), font=font_subscore)

        # Breakdown stats
        draw.text((mid_x + 40, mid_y + 265), "• Rhythm & Intonation: Excellent (100%)", fill=(241, 245, 249), font=get_font(24))
        draw.text((mid_x + 40, mid_y + 305), "• High-Low Pitch Match: Native Equivalent", fill=(241, 245, 249), font=get_font(24))
        draw.text((mid_x + 40, mid_y + 345), "• Mora Cadence: 0.12s Standard Interval", fill=(241, 245, 249), font=get_font(24))

        # App Recommendation Pill
        draw.rounded_rectangle([(mid_x + 40, mid_y + 400), (mid_x + mid_w - 40, mid_y + 510)], radius=18, fill=(15, 23, 42), outline=(52, 211, 153), width=2)
        draw.text((mid_x + 60, mid_y + 420), " Score your voice in TokyoFlow App", fill=(52, 211, 153), font=get_font(26))
        draw.text((mid_x + 60, mid_y + 460), "10,000+ JLPT Vocabulary & Real Tokyo Scenarios", fill=(203, 213, 225), font=get_font(20))

    else: #  PRO-TIP & VALUE MODE (stage 1 & 2)
        draw.rounded_rectangle([(mid_x, mid_y), (mid_x + mid_w, mid_y + mid_h)], radius=24, fill=(30, 41, 59), outline=(52, 211, 153) if stage_num==2 else (51, 65, 85), width=3 if stage_num==2 else 2)
        
        draw.text((mid_x + 30, mid_y + 24), conf["pro_tip_title"], fill=(52, 211, 153), font=get_font(28))
        draw.line([(mid_x + 24, mid_y + 64), (mid_x + mid_w - 24, mid_y + 64)], fill=(51, 65, 85), width=2)

        font_tip_body = get_font(26)
        tip_lines = conf["pro_tip_body"].split("\n")
        cur_ty = mid_y + 84
        for tline in tip_lines:
            words = tline.split(" ")
            sub_lines = []
            cur_s = []
            for w in words:
                cur_s.append(w)
                if draw.textbbox((0, 0), " ".join(cur_s), font=font_tip_body)[2] > mid_w - 60:
                    cur_s.pop()
                    sub_lines.append(" ".join(cur_s))
                    cur_s = [w]
            if cur_s:
                sub_lines.append(" ".join(cur_s))

            for sline in sub_lines:
                draw.text((mid_x + 30, cur_ty), sline, fill=(241, 245, 249), font=font_tip_body)
                cur_ty += 38
            cur_ty += 12

        # Step indicator guide inside pro tip card
        draw.rounded_rectangle([(mid_x + 30, mid_y + 360), (mid_x + mid_w - 30, mid_y + 510)], radius=16, fill=(15, 23, 42))
        draw.text((mid_x + 50, mid_y + 380), "3-STEP SHADOWING MASTER SYSTEM:", fill=(250, 204, 21), font=get_font(22))
        draw.text((mid_x + 50, mid_y + 420), "1.  Listen  2.  Breakdown  3.  Shadow Out Loud", fill=(203, 213, 225), font=get_font(21))
        draw.text((mid_x + 50, mid_y + 458), "Speak after the 3-2-1 countdown beep!", fill=(244, 114, 182), font=get_font(21))

    # 7. Dynamic 4-Step Floating Progress Status Badge (y=1545..1625)
    status_x, status_y, status_w, status_h = 50, 1545, width - 100, 75
    if stage_num == 3:
        s_bg = (225, 29, 72) # Red
        s_text_color = (255, 255, 255)
    elif stage_num == 4:
        s_bg = (16, 185, 129) # Emerald
        s_text_color = (255, 255, 255)
    elif stage_num == 2:
        s_bg = (245, 158, 11) # Amber
        s_text_color = (15, 23, 42)
    elif stage_num == 1:
        s_bg = (79, 70, 229) # Indigo
        s_text_color = (255, 255, 255)
    else:
        s_bg = (51, 65, 85) # Slate
        s_text_color = (255, 255, 255)

    draw.rounded_rectangle([(status_x, status_y), (status_x + status_w, status_y + status_h)], radius=18, fill=s_bg)
    font_status = get_font(28)
    full_status_str = stage_title
    bbox_st = draw.textbbox((0, 0), full_status_str, font=font_status)
    stw = bbox_st[2] - bbox_st[0]
    stx = status_x + (status_w - stw) // 2
    draw.text((stx, status_y + 20), full_status_str, fill=s_text_color, font=font_status)

    # 8. Bottom CTA Conversion Block (y=1640..1870, height=230)
    cta_x, cta_y, cta_w, cta_h = 50, 1640, width - 100, 230
    draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=22, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

    font_cta_app = get_font(24)
    draw.text((cta_x + 30, cta_y + 20), " TokyoFlow - Japanese Speaking (iOS App)", fill=(56, 189, 248), font=font_cta_app)
    
    font_cta_sub = get_font(20)
    draw.text((cta_x + 30, cta_y + 56), "Instant Pitch Accent Scoring • 10,000+ JLPT Vocab", fill=(203, 213, 225), font=font_cta_sub)

    # Action Subscribe Pill
    draw.rounded_rectangle([(cta_x + 24, cta_y + 105), (cta_x + cta_w - 24, cta_y + 195)], radius=16, fill=(244, 63, 94))
    font_sub_btn = get_font(28)
    btn_text = " SUBSCRIBE & SHADOW DAILY!"
    bbox_btn = draw.textbbox((0, 0), btn_text, font=font_sub_btn)
    btn_w = bbox_btn[2] - bbox_btn[0]
    draw.text((cta_x + (cta_w - btn_w) // 2, cta_y + 130), btn_text, fill=(255, 255, 255), font=font_sub_btn)

    # 9. Bottom Progress Line (y=1900..1910)
    draw.rectangle([(0, 1900), (width, 1910)], fill=(30, 41, 59))
    prog_w = int(width * max(0.0, min(1.0, total_progress)))
    draw.rectangle([(0, 1900), (prog_w, 1910)], fill=(250, 204, 21))

    return img

async def generate_single_short(conf: dict):
    ep_num = conf["ep_num"]
    folder_name = conf["folder"]
    release_dir = os.path.join("docs", "youtube_releases", folder_name)
    os.makedirs(release_dir, exist_ok=True)

    tmp_dir = os.path.join("/tmp", f"tokyoflow_short_ep{ep_num:02d}_v2")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)

    print(f"\n==========================================")
    print(f" Building Interactive Shadowing Short EP.{ep_num:02d}: {conf['yt_short_title']}")
    print(f"==========================================")

    # 1. Synthesize Audio Tracks
    # 1.1 Andrew Hook
    hook_audio = os.path.join(tmp_dir, "01_hook.mp3")
    await synth_audio(conf["hook_audio_en"], "en-US-AndrewNeural", hook_audio, rate="+4%")

    # 1.2 Nanami Native Normal Speed (Listen Phase)
    jp_audio_norm = os.path.join(tmp_dir, "02_jp_norm.mp3")
    await synth_audio(conf["jp_sentence"], "ja-JP-NanamiNeural", jp_audio_norm, rate="-4%", pitch="+2Hz")

    # 1.3 Andrew Pro-tip & Culture note
    tip_audio = os.path.join(tmp_dir, "03_tip.mp3")
    await synth_audio(conf["pro_tip_audio_en"], "en-US-AndrewNeural", tip_audio, rate="+4%")

    # 1.4 Andrew Countdown Prompt: "Now your turn! Shadow after the countdown!"
    shadow_cue_audio = os.path.join(tmp_dir, "04_shadow_cue.mp3")
    await synth_audio("Now your turn! Shadow out loud in 3, 2, 1, go!", "en-US-AndrewNeural", shadow_cue_audio, rate="+6%")

    # 1.5 Beeps (3-2-1 countdown)
    beep_low = os.path.join(tmp_dir, "beep_low.mp3")
    generate_beep(800, 0.12, beep_low)
    beep_high = os.path.join(tmp_dir, "beep_high.mp3")
    generate_beep(1600, 0.25, beep_high)

    # 1.6 Silent Shadowing Duration (Sentence length + 1.0s buffer for user speech)
    dur_jp_norm = get_audio_duration(jp_audio_norm)
    shadow_silence_dur = dur_jp_norm + 1.2
    shadow_silence_audio = os.path.join(tmp_dir, "05_shadow_silence.mp3")
    generate_silence(shadow_silence_dur, shadow_silence_audio)

    # 1.7 Chime Success + Andrew Outro Feedback & App CTA
    chime_audio = os.path.join(tmp_dir, "chime.mp3")
    generate_beep(1200, 0.25, chime_audio)
    outro_audio = os.path.join(tmp_dir, "06_outro.mp3")
    await synth_audio("Great job! Practice pitch accent scoring with TokyoFlow on iOS!", "en-US-AndrewNeural", outro_audio, rate="+4%")

    # 2. Extract Token Timings with Whisper for Normal Speed
    print(" Aligning tokens with Whisper for precise karaoke glow...")
    token_objs = conf["tokens"]
    aligned_tokens = align_sentence_tokens_with_audio(jp_audio_norm, token_objs)

    # Build sequence of audio blocks
    dur_hook = get_audio_duration(hook_audio)
    dur_tip = get_audio_duration(tip_audio)
    dur_cue = get_audio_duration(shadow_cue_audio)
    dur_out = get_audio_duration(outro_audio)

    audio_segments = [
        {"file": hook_audio, "dur": dur_hook, "pause": 0.25},
        {"file": jp_audio_norm, "dur": dur_jp_norm, "pause": 0.35},
        {"file": tip_audio, "dur": dur_tip, "pause": 0.35},
        {"file": shadow_cue_audio, "dur": dur_cue, "pause": 0.15},
        {"file": beep_low, "dur": 0.12, "pause": 0.25},
        {"file": beep_low, "dur": 0.12, "pause": 0.25},
        {"file": beep_high, "dur": 0.25, "pause": 0.2},
        {"file": shadow_silence_audio, "dur": shadow_silence_dur, "pause": 0.2},
        {"file": chime_audio, "dur": 0.25, "pause": 0.2},
        {"file": outro_audio, "dur": dur_out, "pause": 0.4}
    ]

    full_audio_path = os.path.join(tmp_dir, "full_shadow_audio.mp3")
    concat_filter = "".join([f"[{i}:a]" for i in range(len(audio_segments))]) + f"concat=n={len(audio_segments)}:v=0:a=1[outa]"
    cmd_audio = ["ffmpeg", "-y"]
    for seg in audio_segments:
        cmd_audio.extend(["-i", seg["file"]])
    cmd_audio.extend(["-filter_complex", concat_filter, "-map", "[outa]", "-c:a", "libmp3lame", full_audio_path])
    subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    total_duration = get_audio_duration(full_audio_path)
    print(f"⏱ Total Interactive Short Duration: {total_duration:.2f}s")

    # Time boundaries calculation
    t_hook = dur_hook + 0.25
    t_listen = t_hook + dur_jp_norm + 0.35
    t_tip = t_listen + dur_tip + 0.35
    t_countdown = t_tip + dur_cue + 0.15 + (0.12+0.25)*2 + 0.25 + 0.2
    t_shadow_start = t_countdown
    t_shadow_end = t_shadow_start + shadow_silence_dur + 0.2
    t_score_end = total_duration

    # 3. Render Video Frames
    frames_dir = os.path.join(tmp_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    fps = 30
    total_frames = int(total_duration * fps)
    print(f" Rendering {total_frames} interactive shadowing frames (1080x1920 @ {fps}fps)...")

    # Generate 9:16 Minimalist Cover Thumbnail per tokyoflow-shorts-factory
    from generate_shorts_thumbnails import create_shorts_cover
    hook_lines = conf["hook_title"].split("\n")
    hook_main = hook_lines[0]
    hook_sub = hook_lines[1] if len(hook_lines) > 1 else "SURVIVAL JAPANESE"
    
    cat_str = conf.get("category", "")
    if "Transit" in cat_str or "Yamanote" in cat_str or "Subway" in cat_str:
        accent_col = (16, 185, 129)
        sec_col = (56, 189, 248)
    elif "Kombini" in cat_str:
        accent_col = (249, 115, 22)
        sec_col = (250, 204, 21)
    elif "Izakaya" in cat_str:
        accent_col = (234, 179, 8)
        sec_col = (249, 115, 22)
    elif "Ramen" in cat_str:
        accent_col = (239, 68, 68)
        sec_col = (245, 158, 11)
    else:
        accent_col = (168, 85, 247)
        sec_col = (236, 72, 153)

    cover_dict = {
        "ep_num": ep_num,
        "sh_code": f"SH.{ep_num:02d}",
        "folder": folder_name,
        "hook_main": hook_main,
        "hook_sub": hook_sub,
        "jp_phrase": conf["jp_sentence"],
        "romaji": conf["romaji_sentence"],
        "en_meaning": conf["en_translation"],
        "accent_color": accent_col,
        "secondary_color": sec_col,
        "location": f"{conf.get('district', 'Tokyo Scene').strip()} • JLPT N5"
    }
    thumb_img = create_shorts_cover(cover_dict)
    short_thumb_path = os.path.join(release_dir, "short_thumbnail.jpg")
    thumb_img.save(short_thumb_path, "JPEG", quality=95)
    cover_frame_img = thumb_img.convert("RGB").resize((1080, 1920), Image.Resampling.LANCZOS)

    # Discover authentic base scene image for background canvas
    bg_cand = os.path.join(release_dir, "news_bg.jpg")
    if not os.path.exists(bg_cand):
        bg_cand = os.path.join(release_dir, "thumbnail.jpg")
    if not os.path.exists(bg_cand):
        scene_dir = "docs/youtube_assets/scene_backgrounds"
        if os.path.exists(scene_dir):
            for f in os.listdir(scene_dir):
                if f.startswith(f"E{ep_num:02d}") or f.startswith(f"E{ep_num}"):
                    bg_cand = os.path.join(scene_dir, f)
                    break
    base_canvas_9_16 = prepare_shorts_background(bg_cand)

    for frame_idx in range(total_frames):
        cur_t = frame_idx / fps
        prog = cur_t / total_duration

        # First-Frame Injection: Frames 0..7 (first ~0.26s) use the exact 9:16 master cover
        if frame_idx < 8 and cover_frame_img is not None:
            frame_img = cover_frame_img
        elif cur_t < t_hook:
            # Stage 0: Hook
            stg = 0
            active_tok = -1
            stg_title = " INTRO: SURVIVAL JAPANESE"
            stg_sub = "Scenario Context"
            spk_prog = 0.0
            frame_img = render_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_listen:
            # Stage 1: Listen (Normal Speed)
            stg = 1
            rel_t = cur_t - t_hook
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens):
                st = tok.get("start", 0.0) - 0.08
                et = tok.get("end", 0.0)
                if st <= rel_t <= et:
                    active_tok = tok_i
                    break
            stg_title = " STEP 1: LISTEN (Native Tokyo Speed)"
            stg_sub = "Listen carefully"
            spk_prog = 0.0
            frame_img = render_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_countdown:
            # Stage 2: Breakdown & Pro-Tip
            stg = 2
            active_tok = -1
            stg_title = " STEP 2: PRO-TIP & FORMULA"
            stg_sub = "Grammar & Nuance"
            spk_prog = 0.0
            frame_img = render_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        elif cur_t < t_shadow_end:
            # Stage 3: Shadowing / Speaking Mode
            stg = 3
            rel_spk_t = cur_t - t_shadow_start
            spk_prog = rel_spk_t / shadow_silence_dur
            # Provide real-time syllable pacing during user's shadowing gap!
            active_tok = -1
            for tok_i, tok in enumerate(aligned_tokens):
                st = tok.get("start", 0.0)
                et = tok.get("end", 0.0)
                if st <= rel_spk_t <= et:
                    active_tok = tok_i
                    break
            stg_title = "  YOUR TURN: SHADOW NOW!"
            stg_sub = "Speak out loud!"
            frame_img = render_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )
        else:
            # Stage 4: AI Scoring & App Outro
            stg = 4
            active_tok = -1
            stg_title = " STEP 4: AI PITCH MATCH SCORING"
            stg_sub = "TokyoFlow App"
            spk_prog = 1.0
            frame_img = render_interactive_frame(
                1080, 1920, conf,
                active_token_idx=active_tok,
                stage_num=stg,
                stage_title=stg_title,
                stage_subtext=stg_sub,
                speaking_prog=spk_prog,
                total_progress=prog,
                frame_idx=frame_idx,
                base_canvas=base_canvas_9_16
            )

        frame_file = os.path.join(frames_dir, f"frame_{frame_idx:05d}.jpg")
        frame_img.save(frame_file, "JPEG", quality=90)

    # 4. Assemble Video with ffmpeg
    out_video_path = os.path.join(release_dir, "short.mp4")
    print(f" Encoding interactive Short to {out_video_path}...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video_path
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 5. Update short_metadata.md (Zero URLs, Zero Emojis in Body)
    meta_path = os.path.join(release_dir, "short_metadata.md")
    tokens_txt = "\n".join([f"- {t['orig']} ({t['kana']}) : {t.get('meaning', '')}" for t in conf["tokens"]])
    
    meta_content = f"""# YouTube Short Launch Package: {conf['folder']}
# {conf['yt_short_title']}

## Release Information
- Episode: EP. {conf['ep_num']:02d} ({conf['folder']})
- Format: 9:16 Vertical Video (1080x1920, 30 fps)
- Shadowing Structure: 4-Stage Progressive Interactive Engine (Listen -> Breakdown -> 3-2-1 Speak Now -> AI Pitch Score)
- Asset File: short.mp4
- Cover Thumbnail: short_thumbnail.jpg
- Duration: {total_duration:.1f}s

---

## YouTube Shorts Title (Copy and Paste)

```
{conf['yt_short_title']}
```

---

## YouTube Shorts Description Box (Copy and Paste Ready - No URLs, No Emojis)

```markdown
{conf['yt_short_title']}

Master real-life Tokyo Japanese survival phrases with interactive 3-step shadowing drills in 30 seconds.

JAPANESE PHRASE:
{conf['jp_sentence']}
{conf['romaji_sentence']}

ENGLISH TRANSLATION:
{conf['en_translation']}

VOCABULARY BREAKDOWN:
{tokens_txt}

PRO-TIP AND GRAMMAR NOTE:
{conf['pro_tip_body']}

SHADOWING PRACTICE INSTRUCTIONS:
1. Listen to the native Tokyo pronunciation at normal speed.
2. Review the grammar formula and cultural context.
3. Speak out loud during the recording countdown to calibrate your pitch accent.

PRACTICE RECOMMENDATION:
Practice interactive speech shadowing with instant pitch accent scoring on the TokyoFlow - Japanese Speaking companion app on the iOS App Store.

Subscribe to TokyoFlow Japanese for daily Tokyo Japanese micro-lessons and real-world immersion.

#Shorts #LearnJapanese #JapaneseSpeaking #TokyoFlow #Tokyo #JLPT #JapaneseShadowing #{conf['slug']}
```

---

## YouTube Tags (Comma Separated)

```
shorts, learn japanese, japanese speaking, tokyo japanese, jlpt, japanese shadowing, tokyoflow, {conf['slug']}
```
"""
    with open(meta_path, "w", encoding="utf-8") as fp:
        fp.write(meta_content)

    print(f" Completed Interactive Shadowing Short for EP.{ep_num:02d} -> {release_dir}")

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="TokyoFlow Master YouTube Shorts Factory")
    parser.add_argument("--ep", "--episode", type=int, help="Target episode number to generate (e.g. 1)")
    parser.add_argument("--all", action="store_true", help="Explicitly regenerate all configured shorts")
    args = parser.parse_args()

    if args.ep:
        targets = [c for c in SHORTS_CONFIGS if c["ep_num"] == args.ep]
        if not targets:
            print(f"[ERROR] No short configuration found for EP.{args.ep:02d}")
            return
        for conf in targets:
            await generate_single_short(conf)
    elif args.all:
        print("Starting Batch Generation of all Interactive Shadowing YouTube Shorts...")
        for conf in SHORTS_CONFIGS:
            await generate_single_short(conf)
        print("\nAll configured shorts successfully generated.")
    else:
        print("[INFO] No target specified. Use --ep <NUM> (e.g. --ep 1) or --all to process all shorts.")
        print(f"Available episodes: {[c['ep_num'] for c in SHORTS_CONFIGS]}")

if __name__ == "__main__":
    asyncio.run(main())

