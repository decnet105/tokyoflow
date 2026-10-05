#!/usr/bin/env python3
"""
TokyoFlow Japanese • Masterclass Study Guide & Roadmap Video Producer (16:9 1080p)
================================================================================
Generates a cinema-grade, practical guide & milestone roadmap video designed
for returning subscribers and dedicated learners.

Zero Emoji Policy strictly enforced.
High-end visual layout with Hiragino Sans GB, glassmorphic cards, and authentic Tokyo photos.

Outputs:
- output/study_guide_en/tokyoflow_study_guide_en_1080p.mp4
- output/study_guide_en/thumbnail.jpg
- output/study_guide_en/metadata.md
"""

import os
import sys
import math
import shutil
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "output" / "study_guide_en"
TEMP_DIR = OUT_DIR / "temp_render"

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
        str(audio_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def synth_line(text: str, voice: str, out_path: str, rate: str = "+0%", pitch: str = "+0Hz"):
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await comm.save(out_path)

def get_clean_background() -> Image.Image:
    """Returns a clean 1920x1080 dark skyline base."""
    W, H = 1920, 1080
    bg_skyline = PROJECT_ROOT / "output" / "tokyoflow_yt_channel_banner_2560x1440.jpg"
    base = Image.new("RGB", (W, H), (10, 14, 22))
    if bg_skyline.exists():
        sky = Image.open(bg_skyline).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        sky = ImageEnhance.Brightness(sky).enhance(0.28)
        base.paste(sky, (0, 0))
    return base

def draw_hud_header(draw, title_category="TOKYOFLOW ACADEMY", title_sub="STUDY GUIDE & ROADMAP"):
    font_cat = get_font(18)
    font_sub = get_font(15)
    
    # Left brand badge
    draw.rectangle([(60, 42), (240, 78)], fill=(18, 30, 48), outline=(56, 189, 248), width=1)
    draw.text((75, 50), "TOKYOFLOW ACADEMY", fill=(56, 189, 248), font=font_cat)
    
    # Right category indicator
    draw.text((1500, 50), title_sub, fill=(148, 163, 184), font=font_sub)
    draw.line([(60, 92), (1860, 92)], fill=(30, 41, 59), width=1)

def draw_subtitle_box(draw, speaker: str, text: str, subtext: str = ""):
    W, H = 1920, 1080
    box_w = 1600
    box_h = 100 if subtext else 80
    box_x = (W - box_w) // 2
    box_y = H - box_h - 35
    
    draw.rectangle(
        [(box_x, box_y), (box_x + box_w, box_y + box_h)],
        fill=(8, 12, 20),
        outline=(56, 189, 248) if "Nanami" in speaker else (74, 107, 130),
        width=2
    )
    
    font_spk = get_font(18)
    font_txt = get_font(22)
    font_sub = get_font(18)
    
    # Speaker tag
    tag_w = 140
    tag_bg = (16, 52, 96) if "Nanami" in speaker else (24, 38, 58)
    tag_fg = (56, 189, 248) if "Nanami" in speaker else (203, 213, 225)
    draw.rectangle([(box_x + 15, box_y + 12), (box_x + tag_w, box_y + 42)], fill=tag_bg)
    draw.text((box_x + 25, box_y + 16), speaker, fill=tag_fg, font=font_spk)
    
    # Main text
    draw.text((box_x + tag_w + 20, box_y + 15), text, fill=(255, 255, 255), font=font_txt)
    
    # Optional subtext
    if subtext:
        draw.text((box_x + tag_w + 20, box_y + 50), subtext, fill=(148, 163, 184), font=font_sub)

# =========================================================================
# SCENE RENDERERS
# =========================================================================

def render_scene_1_hero(draw, img):
    """Scene 1: Master Hero Overview"""
    draw_hud_header(draw, "TOKYOFLOW ACADEMY", "SYSTEM BLUEPRINT")
    
    font_badge = get_font(20)
    font_h1 = get_font(54)
    font_h2 = get_font(28)
    font_p = get_font(22)
    
    # Center Hero Card
    draw.rectangle([(180, 140), (1740, 880)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    # Tag
    draw.rectangle([(230, 180), (550, 225)], fill=(30, 58, 138), outline=(56, 189, 248), width=1)
    draw.text((250, 190), "OFFICIAL STUDY GUIDE & ROADMAP", fill=(255, 255, 255), font=font_badge)
    
    # Main Title
    draw.text((230, 250), "How to Master Real Spoken Tokyo Japanese", fill=(255, 255, 255), font=font_h1)
    draw.text((230, 325), "The Complete Use-Case Blueprint from [JLPT N5] to [JLPT N1]", fill=(56, 189, 248), font=font_h2)
    
    # 3 Pillar Summary Boxes
    pillars = [
        ("01. SCENARIO IMMERSION", "16:9 1080p Masterclasses", "Real Tokyo transit, kombini, dining & living situations."),
        ("02. VOCAL SHADOWING", "9:16 Shorts Speed Drilling", "Muscle memory training with standard Tokyo pitch contour."),
        ("03. JLPT PROGRESSION", "Structured Milestones", "Systematic ascent from N5 survival to N1 native nuance.")
    ]
    
    for i, (p_title, p_sub, p_desc) in enumerate(pillars):
        px = 230 + i * 490
        py = 410
        draw.rectangle([(px, py), (px + 460, py + 400)], fill=(18, 26, 42), outline=(45, 60, 85), width=1)
        draw.rectangle([(px, py), (px + 460, py + 50)], fill=(24, 38, 62))
        draw.text((px + 20, py + 15), p_title, fill=(56, 189, 248), font=get_font(20))
        draw.text((px + 20, py + 70), p_sub, fill=(255, 255, 255), font=get_font(22))
        
        # Multiline desc
        lines = [p_desc[:26], p_desc[26:]]
        for li, l in enumerate(lines):
            draw.text((px + 20, py + 120 + li * 30), l, fill=(148, 163, 184), font=font_p)
            
        draw.line([(px + 20, py + 220), (px + 440, py + 220)], fill=(35, 48, 70), width=1)
        draw.text((px + 20, py + 245), "Core Skill Focus:", fill=(203, 213, 225), font=get_font(18))
        if i == 0:
            draw.text((px + 20, py + 285), "- Contextual Listening\n- Keigo/Tameguchi Nuance\n- Cultural Social Rules", fill=(148, 163, 184), font=get_font(18))
        elif i == 1:
            draw.text((px + 20, py + 285), "- Fast Speech Rhythm\n- Intonation Mastery\n- Instant Muscle Recall", fill=(148, 163, 184), font=get_font(18))
        else:
            draw.text((px + 20, py + 285), "- Grammar Dissection\n- Particle Mechanics\n- Real News Decoding", fill=(148, 163, 184), font=get_font(18))

def render_scene_2_problem(draw, img):
    """Scene 2: Textbook vs. Real Tokyo Japanese"""
    draw_hud_header(draw, "METHODOLOGY", "THE REALITY GAP")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "Why Traditional Textbooks Fail in Real-Life Tokyo", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "Comparing Classroom Theory with Authentic Street Flow", fill=(148, 163, 184), font=font_sub)
    
    # Left Box: Traditional Textbooks (Red/Slate tint)
    draw.rectangle([(100, 220), (920, 850)], fill=(20, 22, 28), outline=(150, 60, 60), width=2)
    draw.rectangle([(100, 220), (920, 280)], fill=(45, 20, 20))
    draw.text((130, 235), "TRADITIONAL TEXTBOOKS", fill=(252, 165, 165), font=get_font(24))
    
    bad_points = [
        ("Robotic, Formal Keigo Overuse", "Teaches rigid 'Watashi wa gakusei desu' which locals rarely say."),
        ("No Speed or Ambient Background", "Slow, studio-isolated audio creates panic in loud stations."),
        ("Missing Colloquial Contractions", "Fails to explain '〜ちゃった', '〜とく', or particle omission."),
        ("Zero Situational Reaction Training", "Leaves you freezing at kombini registers and ticket machines.")
    ]
    for i, (title, desc) in enumerate(bad_points):
        y = 310 + i * 130
        draw.text((130, y), f"- {title}", fill=(248, 113, 113), font=get_font(22))
        draw.text((150, y + 35), desc, fill=(148, 163, 184), font=get_font(18))
        if i < 3:
            draw.line([(130, y + 105), (890, y + 105)], fill=(35, 30, 35), width=1)

    # Right Box: TokyoFlow Blueprint (Cyan/Blue tint)
    draw.rectangle([(1000, 220), (1820, 850)], fill=(14, 24, 38), outline=(56, 189, 248), width=2)
    draw.rectangle([(1000, 220), (1820, 280)], fill=(18, 48, 80))
    draw.text((1030, 235), "THE TOKYOFLOW APPROACH", fill=(56, 189, 248), font=get_font(24))
    
    good_points = [
        ("Use-Case Driven Immersion", "Every lesson is anchored in a concrete Tokyo living scenario."),
        ("Authentic Spoken Cadence", "Pure Tokyo standard pronunciation with natural rhythm."),
        ("Dual-Layer Analysis (1080p + Shorts)", "Full conceptual breakdown paired with high-rep shadowing."),
        ("Real Japanese Daily Reactions", "Master instant 1-second reflexes for shopping, transit, & dining.")
    ]
    for i, (title, desc) in enumerate(good_points):
        y = 310 + i * 130
        draw.text((1030, y), f"+ {title}", fill=(56, 189, 248), font=get_font(22))
        draw.text((1050, y + 35), desc, fill=(203, 213, 225), font=get_font(18))
        if i < 3:
            draw.line([(1030, y + 105), (1790, y + 105)], fill=(25, 45, 70), width=1)

def render_scene_3_cycle(draw, img):
    """Scene 3: The 3-Step Mastery Cycle"""
    draw_hud_header(draw, "LEARNING CYCLE", "THE 3-STEP MASTERY SYSTEM")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "The TokyoFlow 3-Step Mastery Cycle", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "How to Turn Scenario Comprehension into Automatic Vocal Muscle Memory", fill=(148, 163, 184), font=font_sub)
    
    steps = [
        ("STEP 01", "16:9 Cinema Masterclass", "Context Immersion & Listening",
         "- Watch the complete situational flow in 1080p\n- Absorb real station/store background atmosphere\n- Identify key verbs and conversational triggers",
         (30, 58, 138), (56, 189, 248)),
        
        ("STEP 02", "Grammar & Nuance Deconstruction", "Deep Linguistic Decoding",
         "- Dissect particles, polite vs casual switches\n- Unpack cultural unspoken etiquette\n- Map directly to standardized JLPT benchmarks",
         (20, 83, 45), (74, 222, 128)),
        
        ("STEP 03", "9:16 Spoken Shadowing Shorts", "High-Frequency Muscle Memory",
         "- Repeat sentences simultaneously with standard audio\n- Match Tokyo pitch accents and natural pacing\n- Drill 3-5 reps until speech flows automatically",
         (120, 53, 15), (251, 191, 36))
    ]
    
    for i, (s_num, s_title, s_sub, s_desc, bg_head, fg_head) in enumerate(steps):
        sx = 100 + i * 590
        sy = 220
        draw.rectangle([(sx, sy), (sx + 540, sy + 630)], fill=(14, 20, 32), outline=fg_head, width=2)
        
        # Header banner
        draw.rectangle([(sx, sy), (sx + 540, sy + 75)], fill=bg_head)
        draw.text((sx + 25, sy + 15), s_num, fill=fg_head, font=get_font(20))
        draw.text((sx + 25, sy + 40), s_title, fill=(255, 255, 255), font=get_font(22))
        
        # Subtitle
        draw.text((sx + 25, sy + 100), s_sub, fill=(255, 255, 255), font=get_font(22))
        draw.line([(sx + 25, sy + 140), (sx + 515, sy + 140)], fill=(35, 48, 70), width=1)
        
        # Bullet list
        draw.text((sx + 25, sy + 160), s_desc, fill=(203, 213, 225), font=get_font(20), spacing=18)
        
        # Bottom Tip Box
        draw.rectangle([(sx + 20, sy + 480), (sx + 520, sy + 600)], fill=(20, 30, 48), outline=(45, 65, 95), width=1)
        draw.text((sx + 35, sy + 495), "Recommended Routine:", fill=fg_head, font=get_font(18))
        if i == 0:
            draw.text((sx + 35, sy + 530), "Watch once with full attention at\n08:00 AM EDT release.", fill=(148, 163, 184), font=get_font(17))
        elif i == 1:
            draw.text((sx + 35, sy + 530), "Take active notes on sentence cards\nand JLPT grammar markers.", fill=(148, 163, 184), font=get_font(17))
        else:
            draw.text((sx + 35, sy + 530), "Loop 9:16 Shorts during your commute\nfor rapid vocal training.", fill=(148, 163, 184), font=get_font(17))

def render_scene_4_roadmap(draw, img):
    """Scene 4: The 5-Level JLPT Milestone Roadmap"""
    draw_hud_header(draw, "MILESTONE ROADMAP", "THE 5-LEVEL PROGRESSION")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "The TokyoFlow 5-Level Japanese Fluency Roadmap", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "From Fundamental Tokyo Survival to Native Nuance & Media Decoding", fill=(148, 163, 184), font=font_sub)
    
    stages = [
        ("[JLPT N5]", "STAGE 01: ESSENTIAL SURVIVAL", "Basic Tokyo Infrastructure",
         ["Yamanote Line Announcements & Transfers", "7-Eleven / FamilyMart Register Speed Replies", "Cafe & Quick Dining Requests", "Basic Numbers, Prices, and Point Cards"],
         (30, 58, 138), (56, 189, 248)),
        
        ("[JLPT N4]", "STAGE 02: DAILY INDEPENDENCE", "Navigating Public Life",
         ["Metro Fare Adjustment & IC Card Troubleshooting", "Kombini Hot Snack & Coffee Machine Hacks", "Pharmacy & Drugstore Symptom Explanations", "Standard Polite Requests and Permissions"],
         (14, 116, 144), (34, 211, 238)),
        
        ("[JLPT N3]", "STAGE 03: SOCIAL & LIFESTYLE", "Dining, Culture, and Socializing",
         ["Izakaya Draft Beer Ordering & Table Etiquette", "Ramen Ticket Machine Customization (Kame, Koi)", "Anime & Figure Tax-Free Shopping in Akihabara", "Sento & Onsen Bathhouse Etiquette Protocols"],
         (161, 98, 7), (250, 204, 21)),
        
        ("[JLPT N2]", "STAGE 04: ADVANCED CONVERSATION", "Professional & Nuanced Discussions",
         ["Ginza Fitting Room Protocols & Style Discussions", "Workplace Greetings & Business Etiquette", "Travel Troubleshooting & Hotel Requests", "Understanding Casual Slang vs. Polite Forms"],
         (194, 65, 12), (251, 146, 60)),
        
        ("[JLPT N1]", "STAGE 05: NATIVE NUANCE & MEDIA", "Media, News, and Complex Nuances",
         ["NHK Real News Broadcast Listening", "Tech, Economic, and Cultural Commentary", "Subtle Emotional Subtext & Japanese Humor", "Native Conversational Speed & Tone Decoding"],
         (126, 34, 206), (192, 132, 252))
    ]
    
    for i, (badge, stage_title, stage_sub, items, bg_b, fg_b) in enumerate(stages):
        sy = 220 + i * 125
        # Full width milestone row
        draw.rectangle([(100, sy), (1820, sy + 110)], fill=(14, 20, 32), outline=(40, 55, 80), width=1)
        
        # Left Badge
        draw.rectangle([(110, sy + 15), (280, sy + 95)], fill=bg_b, outline=fg_b, width=2)
        draw.text((125, sy + 40), badge, fill=(255, 255, 255), font=get_font(26))
        
        # Title and sub
        draw.text((310, sy + 25), stage_title, fill=fg_b, font=get_font(22))
        draw.text((310, sy + 60), stage_sub, fill=(148, 163, 184), font=get_font(18))
        
        # Right Items (4 columns)
        for ji, item in enumerate(items):
            jx = 760 + (ji % 2) * 520
            jy = sy + 25 + (ji // 2) * 38
            draw.text((jx, jy), f"- {item}", fill=(226, 232, 240), font=get_font(17))

def render_scene_5_routine(draw, img):
    """Scene 5: The Daily 15-Minute Mastery Routine"""
    draw_hud_header(draw, "DAILY DISCIPLINE", "THE 15-MINUTE PRO ROUTINE")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "The Daily 15-Minute TokyoFlow Fluency Routine", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "Small Daily High-Impact Repetitions Compound into Total Natural Fluency", fill=(148, 163, 184), font=font_sub)
    
    blocks = [
        ("08:00 AM EDT", "Morning Immersion (5 Mins)", "Watch the daily 16:9 Masterclass release.\nFocus on context, scenario visual cues, and key grammar markers.", (30, 58, 138), (56, 189, 248)),
        ("12:30 PM (LUNCH)", "Midday Shadowing (5 Mins)", "Play the corresponding 9:16 Shorts.\nShadow the audio aloud 3 times to train tongue and throat muscle memory.", (20, 83, 45), (74, 222, 128)),
        ("20:00 PM (NIGHT)", "Active Recall & Review (5 Mins)", "Review sentence cards and playlist collections.\nTest yourself by muting video and providing the Tokyo local reply.", (120, 53, 15), (251, 191, 36))
    ]
    
    for i, (time_tag, b_title, b_desc, bg_tag, fg_tag) in enumerate(blocks):
        bx = 100 + i * 590
        by = 240
        draw.rectangle([(bx, by), (bx + 540, by + 580)], fill=(14, 20, 32), outline=fg_tag, width=2)
        
        # Time badge
        draw.rectangle([(bx + 30, by + 30), (bx + 280, by + 80)], fill=bg_tag, outline=fg_tag, width=1)
        draw.text((bx + 45, by + 42), time_tag, fill=(255, 255, 255), font=get_font(22))
        
        draw.text((bx + 30, by + 110), b_title, fill=(255, 255, 255), font=get_font(24))
        draw.line([(bx + 30, by + 160), (bx + 510, by + 160)], fill=(35, 48, 70), width=1)
        
        # Description
        draw.text((bx + 30, by + 190), b_desc, fill=(203, 213, 225), font=get_font(20), spacing=15)
        
        # Bottom Metric
        draw.rectangle([(bx + 30, by + 420), (bx + 510, by + 540)], fill=(20, 30, 48), outline=(45, 65, 95), width=1)
        draw.text((bx + 45, by + 440), "Target Outcome:", fill=fg_tag, font=get_font(18))
        if i == 0:
            draw.text((bx + 45, by + 475), "100% Contextual Comprehension", fill=(255, 255, 255), font=get_font(20))
        elif i == 1:
            draw.text((bx + 45, by + 475), "Zero-Hesitation Spoken Speed", fill=(255, 255, 255), font=get_font(20))
        else:
            draw.text((bx + 45, by + 475), "Long-Term Synaptic Retention", fill=(255, 255, 255), font=get_font(20))

def render_scene_6_cta(draw, img):
    """Scene 6: Curated Playlists & Call to Action"""
    draw_hud_header(draw, "GET STARTED", "YOUR FLUENCY JOURNEY BEGINS NOW")
    
    font_h = get_font(42)
    font_sub = get_font(24)
    
    # Big Main Card
    draw.rectangle([(140, 140), (1780, 880)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    draw.text((200, 190), "Unlock Your Real Spoken Tokyo Japanese Today", fill=(255, 255, 255), font=font_h)
    draw.text((200, 260), "Organized Playlists, Daily Releases, and Cinema-Grade Lessons", fill=(56, 189, 248), font=font_sub)
    
    # 4 Playlist Mini Cards
    pl_cards = [
        ("Playlist 01", "Transit & Subway Mastery", "Yamanote Line, Metro Transfers, Fare Gates"),
        ("Playlist 02", "Kombini & Street Living", "7-Eleven, FamilyMart, Cafes, Checkout Hacks"),
        ("Playlist 03", "Izakaya & Japanese Dining", "Draft Beer, Ramen Ticket Machines, Table Etiquette"),
        ("Playlist 04", "NHK News & Cultural Trends", "Real Broadcasts, Pop Trends, Media Nuance")
    ]
    
    for i, (p_tag, p_name, p_items) in enumerate(pl_cards):
        cx = 200 + (i % 2) * 720
        cy = 340 + (i // 2) * 190
        draw.rectangle([(cx, cy), (cx + 680, cy + 160)], fill=(18, 26, 42), outline=(45, 60, 85), width=1)
        
        # Tag
        draw.rectangle([(cx + 20, cy + 20), (cx + 160, cy + 55)], fill=(30, 58, 138))
        draw.text((cx + 35, cy + 26), p_tag, fill=(56, 189, 248), font=get_font(18))
        
        draw.text((cx + 180, cy + 26), p_name, fill=(255, 255, 255), font=get_font(22))
        draw.text((cx + 20, cy + 85), p_items, fill=(148, 163, 184), font=get_font(18))
        draw.text((cx + 20, cy + 118), "[Full 1080p Masterclass + 9:16 Shadowing Series]", fill=(56, 189, 248), font=get_font(16))

    # Bottom Call to Action
    draw.rectangle([(200, 750), (1720, 840)], fill=(16, 40, 70), outline=(56, 189, 248), width=2)
    draw.text((250, 775), "Subscribe to @TokyoFlowJapan  |  Daily 08:00 AM EDT Masterclasses", fill=(255, 255, 255), font=get_font(26))
    draw.text((1200, 775), "Start with Episode 01 Now ->", fill=(56, 189, 248), font=get_font(24))

# =========================================================================
# SCRIPT DEFINITIONS & BUILDER
# =========================================================================

async def build_study_guide_video():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n==================================================")
    print("Building TokyoFlow Study Guide & Roadmap Master Video")
    print("==================================================")
    
    script = [
        # Scene 1: Introduction
        {"id": "sg_01", "scene": 1, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Welcome to TokyoFlow Japanese. If you are here, you know that textbook Japanese is not enough."},
        {"id": "sg_02", "scene": 1, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "speaker": "Nanami",
         "text": "本物の日本語は、教科書の中ではなく、東京の日常の中にあります！",
         "subtext": "Real Japanese is not inside textbooks, but inside Tokyo's daily life!"},
        {"id": "sg_03", "scene": 1, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "This guide breaks down our exact study system and fluency roadmap from JLPT N5 all the way to N1."},
        
        # Scene 2: The Problem with Traditional Textbooks
        {"id": "sg_04", "scene": 2, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Most learners study grammar rules for years, but freeze the moment a station attendant or cashier speaks."},
        {"id": "sg_05", "scene": 2, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Why? Because textbooks teach isolated, robotic sentences with zero real-life speed or background ambient noise."},
        {"id": "sg_06", "scene": 2, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "speaker": "Nanami",
         "text": "袋はご利用ですか？温めますか？ポイントカードはお持ちですか？",
         "subtext": "Will you need a bag? Would you like it heated? Do you have a point card?"},
        {"id": "sg_07", "scene": 2, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "At TokyoFlow, we solve this with context-driven immersion in authentic Tokyo environments."},
        
        # Scene 3: The 3-Step Mastery Cycle
        {"id": "sg_08", "scene": 3, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Every lesson is built around our proprietary Three-Step Mastery Cycle."},
        {"id": "sg_09", "scene": 3, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Step 1: Scenario Immersion. Watch the full 16:9 masterclass to absorb natural conversational speed and visual context."},
        {"id": "sg_10", "scene": 3, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Step 2: Grammar and Cultural Deconstruction. Understand every particle, keigo switch, and unspoken social nuance."},
        {"id": "sg_11", "scene": 3, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Step 3: High-Frequency Spoken Shadowing. Drill the 9:16 shorts to build vocal muscle memory with standard Tokyo pitch."},
        
        # Scene 4: The 5-Level JLPT Milestone Roadmap
        {"id": "sg_12", "scene": 4, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Our curriculum follows a clear five-level milestone roadmap mapped directly to JLPT benchmarks."},
        {"id": "sg_13", "scene": 4, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Levels N5 and N4 establish essential survival: Yamanote Line transfers, IC card troubleshooting, and kombini speed responses."},
        {"id": "sg_14", "scene": 4, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Level N3 unlocks lifestyle immersion: Izakaya ordering etiquette, ramen ticket customizers, Akihabara shopping, and onsen rules."},
        {"id": "sg_15", "scene": 4, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Levels N2 and N1 tackle professional Japanese, NHK news broadcast listening, and nuanced cultural commentary."},
        
        # Scene 5: The Daily 15-Minute Routine
        {"id": "sg_16", "scene": 5, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "To achieve maximum retention, follow our daily fifteen-minute pro learner routine."},
        {"id": "sg_17", "scene": 5, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Morning: Watch the daily 16:9 Masterclass released at 08:00 AM EDT."},
        {"id": "sg_18", "scene": 5, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Midday: Loop the corresponding 9:16 Shorts three times to train your vocal cords."},
        {"id": "sg_19", "scene": 5, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Evening: Review key sentence cards and test your active recall across playlist series."},
        
        # Scene 6: Playlists & Call to Action
        {"id": "sg_20", "scene": 6, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Explore our curated playlists by topic: Transit, Kombini Living, Izakaya Dining, and Real News."},
        {"id": "sg_21", "scene": 6, "voice": "en-US-AndrewNeural", "rate": "+3%", "speaker": "Andrew",
         "text": "Hit Subscribe, save the playlists to your library, and start your real Tokyo Japanese journey today."},
        {"id": "sg_22", "scene": 6, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+3Hz", "speaker": "Nanami",
         "text": "一緒に、自然な東京の日本語をマスターしましょう！チャンネル登録をお願いします！",
         "subtext": "Let's master natural Tokyo Japanese together! Please subscribe to the channel!"}
    ]
    
    # 1. Synthesize audio
    print("\n1. Synthesizing voice audio tracks...")
    timeline = []
    cur_time = 0.5
    for seg in script:
        out_f = str(TEMP_DIR / f"{seg['id']}.mp3")
        await synth_line(seg["text"], seg["voice"], out_f, rate=seg.get("rate", "+0%"), pitch=seg.get("pitch", "+0Hz"))
        dur = get_audio_duration(out_f)
        timeline.append({
            **seg,
            "audio_file": out_f,
            "start": cur_time,
            "duration": dur,
            "end": cur_time + dur
        })
        cur_time += dur + 0.35
        
    total_duration = cur_time + 1.0
    print(f"Total Video Duration: {total_duration:.2f}s ({total_duration/60:.2f} mins)")
    
    # 2. Concatenate audio with ffmpeg
    print("\n2. Concatenating audio timeline...")
    concat_list = TEMP_DIR / "audio_concat.txt"
    with open(concat_list, "w") as f:
        f.write("file 'sil_05.mp3'\n")
        # generate initial 0.5s silence
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.5", "-q:a", "9", "-acodec", "libmp3lame", str(TEMP_DIR / "sil_05.mp3")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.35", "-q:a", "9", "-acodec", "libmp3lame", str(TEMP_DIR / "sil_gap.mp3")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        for item in timeline:
            f.write(f"file '{Path(item['audio_file']).name}'\n")
            f.write("file 'sil_gap.mp3'\n")
            
    master_audio = TEMP_DIR / "master_audio.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(master_audio)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Render video frames at 30 fps
    print("\n3. Rendering video frames (1920x1080 @ 30fps)...")
    fps = 30
    total_frames = int(total_duration * fps)
    
    # Pre-render static scene backgrounds
    scene_bases = {}
    for s_idx in range(1, 7):
        base = get_clean_background()
        draw = ImageDraw.Draw(base)
        if s_idx == 1:
            render_scene_1_hero(draw, base)
        elif s_idx == 2:
            render_scene_2_problem(draw, base)
        elif s_idx == 3:
            render_scene_3_cycle(draw, base)
        elif s_idx == 4:
            render_scene_4_roadmap(draw, base)
        elif s_idx == 5:
            render_scene_5_routine(draw, base)
        elif s_idx == 6:
            render_scene_6_cta(draw, base)
        scene_bases[s_idx] = base
        
    frames_dir = TEMP_DIR / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    for f_idx in range(total_frames):
        t = f_idx / fps
        
        # Find active segment
        active_seg = None
        for seg in timeline:
            if seg["start"] <= t <= seg["end"]:
                active_seg = seg
                break
                
        # Determine scene
        if active_seg:
            cur_scene = active_seg["scene"]
        else:
            # find closest scene
            cur_scene = 1
            for seg in timeline:
                if t >= seg["start"]:
                    cur_scene = seg["scene"]
                    
        frame = scene_bases[cur_scene].copy()
        draw = ImageDraw.Draw(frame)
        
        # Draw subtitle box if active speech
        if active_seg:
            draw_subtitle_box(
                draw,
                speaker=active_seg["speaker"],
                text=active_seg["text"],
                subtext=active_seg.get("subtext", "")
            )
            
        frame.save(frames_dir / f"frame_{f_idx:05d}.jpg", quality=90)
        
        if f_idx % 300 == 0:
            print(f"  Rendered {f_idx}/{total_frames} frames ({(f_idx/total_frames)*100:.1f}%)...")
            
    # 4. Compile video with ffmpeg
    print("\n4. Encoding 1080p Master Video...")
    final_video = OUT_DIR / "tokyoflow_study_guide_en_1080p.mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", "30",
        "-i", str(frames_dir / "frame_%05d.jpg"),
        "-i", str(master_audio),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_video)
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Master Video rendered: {final_video}")
    
    # 5. Build 16:9 Master Thumbnail
    print("\n5. Generating 16:9 Master Thumbnail...")
    thumb = get_clean_background()
    draw_t = ImageDraw.Draw(thumb)
    
    # Top Brand Header
    draw_hud_header(draw_t, "TOKYOFLOW ACADEMY", "OFFICIAL STUDY GUIDE")
    
    # Left Hero Panel
    draw_t.rectangle([(100, 140), (1200, 960)], fill=(12, 18, 30), outline=(56, 189, 248), width=3)
    
    # Badge
    draw_t.rectangle([(150, 190), (520, 245)], fill=(30, 58, 138), outline=(56, 189, 248), width=2)
    draw_t.text((170, 202), "OFFICIAL STUDY GUIDE", fill=(255, 255, 255), font=get_font(24))
    
    # Big Titles
    draw_t.text((150, 280), "How to Master Real", fill=(255, 255, 255), font=get_font(56))
    draw_t.text((150, 360), "Tokyo Spoken Japanese", fill=(56, 189, 248), font=get_font(60))
    
    draw_t.text((150, 460), "The Complete Use-Case Blueprint & Shadowing Routine", fill=(226, 232, 240), font=get_font(26))
    
    # 3 Progress Badges
    badges = [
        ("[JLPT N5-N4]", "Transit & Kombini Survival", (30, 58, 138)),
        ("[JLPT N3]", "Izakaya & Social Fluency", (161, 98, 7)),
        ("[JLPT N2-N1]", "Real News & Native Nuance", (126, 34, 206))
    ]
    for bi, (b_txt, b_desc, b_bg) in enumerate(badges):
        by = 540 + bi * 110
        draw_t.rectangle([(150, by), (380, by + 80)], fill=b_bg, outline=(255, 255, 255), width=1)
        draw_t.text((170, by + 22), b_txt, fill=(255, 255, 255), font=get_font(26))
        draw_t.text((410, by + 25), b_desc, fill=(203, 213, 225), font=get_font(24))
        
    draw_t.rectangle([(150, 880), (1150, 930)], fill=(18, 48, 80))
    draw_t.text((170, 892), "Daily 16:9 Masterclasses + 9:16 Shadowing Shorts Routine", fill=(56, 189, 248), font=get_font(20))
    
    # Right Column: Real Tokyo Photo Feature
    right_photo_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_tokyo_skyline_distant_4k.jpg"
    if not right_photo_path.exists():
        right_photo_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_yamanote_platform.jpg"
        
    if right_photo_path.exists():
        r_img = Image.open(right_photo_path).convert("RGB")
        r_crop = r_img.resize((560, 820), Image.Resampling.LANCZOS)
        thumb.paste(r_crop, (1260, 140))
        # border overlay
        draw_t.rectangle([(1260, 140), (1820, 960)], outline=(56, 189, 248), width=3)
        # badge over photo
        draw_t.rectangle([(1280, 880), (1800, 940)], fill=(10, 16, 26, 220))
        draw_t.text((1310, 898), "Full Curriculum [JLPT N5-N1]", fill=(255, 255, 255), font=get_font(22))
        
    thumb_path = OUT_DIR / "thumbnail.jpg"
    thumb.save(thumb_path, quality=95)
    print(f"Master Thumbnail saved: {thumb_path}")
    
    # 6. Metadata file
    metadata_content = """# TokyoFlow Japanese • Official Study Guide & Fluency Roadmap

## Video Information
- **Title**: How to Master Real Tokyo Japanese: Complete Study Guide & Shadowing Roadmap [JLPT N5-N1]
- **Category**: Education (27)
- **Language**: English (en) / Spoken Japanese Audio (ja)
- **Target Placement**: YouTube Studio -> Customization -> Featured video for returning subscribers

## Video Description
Welcome to TokyoFlow Japanese — the cinema-grade, use-case-driven language academy dedicated to decoding authentic spoken Tokyo Japanese.

If you have studied traditional grammar for years but still freeze in Tokyo train stations, kombini registers, or izakaya counters, this video is your master blueprint.

In this Official Study Guide & Roadmap, you will learn:
1. The Reality Gap: Why traditional textbook Japanese fails in real-life Tokyo conversations.
2. The 3-Step Mastery Cycle: How to combine 16:9 Scenario Masterclasses with 9:16 Spoken Shadowing Shorts to build rapid vocal muscle memory.
3. The 5-Level JLPT Milestone Roadmap: Structured progression from [JLPT N5] essential survival to [JLPT N1] native news & media nuance.
4. The 15-Minute Daily Pro Routine: How 15 minutes of structured daily exposure compounds into effortless conversational fluency.
5. Curated Playlists & Resources: How to navigate our specialized playlists for transit, dining, shopping, and cultural trends.

---

### Recommended Study Playlists:
- Playlist 1: Transit & Subway Mastery (Yamanote Line, Tokyo Metro, Fare Adjustments)
- Playlist 2: Kombini & Daily Living (7-Eleven, FamilyMart, Cafes, Checkout Speed Replies)
- Playlist 3: Izakaya & Dining Protocols (Draft Beer Orders, Ramen Ticket Machines, Table Etiquette)
- Playlist 4: NHK News & Cultural Trends (Real Broadcasts, Pop Trends, Media Nuance)

Daily Masterclasses released at 08:00 AM EDT.
Subscribe to @TokyoFlowJapan and start mastering real Tokyo Japanese today!

#LearnJapanese #JLPT #TokyoFlow #StudyJapanese #JapaneseShadowing #Tokyo #JLPTN5 #JLPTN4 #JLPTN3 #JLPTN2 #JLPTN1

## YouTube Tags
TokyoFlow, Learn Japanese, Japanese Study Guide, Japanese Roadmap, JLPT, JLPT N5, JLPT N4, JLPT N3, JLPT N2, JLPT N1, Japanese Shadowing, Speak Japanese, Real Japanese, Tokyo Japanese, Japanese Pronunciation, Japanese Listening Practice
"""
    with open(OUT_DIR / "metadata.md", "w") as f:
        f.write(metadata_content)
        
    print("Metadata generated at:", OUT_DIR / "metadata.md")
    print("\n[OK] Study Guide & Roadmap Build Complete!")

if __name__ == "__main__":
    asyncio.run(build_study_guide_video())
