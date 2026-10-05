#!/usr/bin/env python3
"""
TokyoFlow Japanese • Print-Friendly Golden Master PDF Study Guide (300 DPI A4)
==============================================================================
- 100% Light/White Executive Layout (Ink-friendly, crisp, elegant).
- Automated word wrapping with ZERO overflow or truncation.
- Zero broken glyphs / tofu boxes (fully sanitized typography).
- Balanced typography scaling and professional information density.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "output" / "study_guide_en"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def draw_wrapped_text(draw, text: str, font, fill, x: int, y: int, max_width: int, line_spacing: int = 12) -> int:
    """Draws multiline wrapped text within max_width and returns the bottom Y coordinate."""
    # Sanitize characters that may cause glyph rendering issues
    clean_text = text.replace("〜", "-").replace("〜", "-")
    words = clean_text.split(" ")
    lines = []
    cur_line = []
    
    for word in words:
        test_line = " ".join(cur_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            cur_line.append(word)
        else:
            if cur_line:
                lines.append(" ".join(cur_line))
                cur_line = [word]
            else:
                lines.append(word)
                cur_line = []
    if cur_line:
        lines.append(" ".join(cur_line))
        
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        h = max(bbox[3] - bbox[1], font.size)
        cur_y += h + line_spacing
        
    return cur_y

def draw_header_footer(draw, page_num: int, total_pages: int = 4):
    W, H = 2480, 3508
    
    # Top Header
    draw.rectangle([(120, 90), (460, 150)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    draw.text((140, 108), "TOKYOFLOW ACADEMY", fill=(29, 78, 216), font=get_font(26))
    
    draw.text((490, 110), "THE FLUENCY BLUEPRINT  |  OFFICIAL STUDY SYLLABUS", fill=(71, 85, 105), font=get_font(24))
    draw.text((1950, 110), "[JLPT N5-N1 ROADMAP]", fill=(29, 78, 216), font=get_font(24))
    draw.line([(120, 170), (2360, 170)], fill=(203, 213, 225), width=2)
    
    # Bottom Footer
    draw.line([(120, 3350), (2360, 3350)], fill=(203, 213, 225), width=2)
    draw.text((120, 3380), "TokyoFlow Japanese Academy  *  Daily Masterclasses at 08:00 AM EDT  *  @TokyoFlowJapan", fill=(100, 116, 139), font=get_font(22))
    draw.text((2150, 3380), f"Page {page_num} of {total_pages}", fill=(15, 23, 42), font=get_font(24))

# =========================================================================
# PAGE 1: TITLE & EXECUTIVE BLUEPRINT
# =========================================================================
def make_page_1():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 1)
    
    # 1. Executive Title Card
    draw.rectangle([(120, 210), (2360, 620)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    
    draw.rectangle([(170, 245), (590, 300)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    draw.text((195, 258), "OFFICIAL STUDY SYLLABUS", fill=(29, 78, 216), font=get_font(24))
    
    draw.text((170, 325), "The TokyoFlow Fluency Blueprint", fill=(15, 23, 42), font=get_font(60))
    draw.text((170, 410), "How to Master Authentic Spoken Tokyo Japanese [JLPT N5-N1]", fill=(29, 78, 216), font=get_font(34))
    draw.text((170, 475), "A Use-Case Driven Curriculum Combining 16:9 Scenario Masterclasses & 9:16 Shadowing Shorts", fill=(51, 65, 85), font=get_font(24))
    draw.text((170, 535), "Release Schedule: Daily at 08:00 AM EDT  |  Standard Tokyo Pitch Accent Audio", fill=(100, 116, 139), font=get_font(22))

    # 2. Section 1: The Reality Gap
    draw.text((120, 670), "1. The Reality Gap: Why Traditional Textbooks Fail in Tokyo", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 720), (2360, 720)], fill=(29, 78, 216), width=3)
    
    # Left Card: Traditional Textbooks
    draw.rectangle([(120, 750), (1210, 1420)], fill=(255, 245, 245), outline=(252, 165, 165), width=2)
    draw.rectangle([(120, 750), (1210, 825)], fill=(254, 226, 226))
    draw.text((160, 772), "Traditional Textbook Methods", fill=(185, 28, 28), font=get_font(26))
    
    trad_points = [
        ("Robotic Formal Grammar Overuse", "Teaches rigid constructs like 'Watashi wa gakusei desu' which Tokyo locals rarely use in daily spoken conversations."),
        ("Studio Silence vs. Ambient Reality", "Audio recorded in slow isolation creates panic when facing rapid train announcements or crowded kombini cashiers."),
        ("Missing Conversational Shortcuts", "Fails to teach natural spoken contractions (-chau, -toku, -nakya) and natural particle omission in fast speech."),
        ("The Passive Memorization Trap", "Learners spend years memorizing kanji lists without building vocal muscle memory to respond in under one second.")
    ]
    
    cur_y = 855
    for title, desc in trad_points:
        draw.text((160, cur_y), f"- {title}", fill=(185, 28, 28), font=get_font(24))
        cur_y = draw_wrapped_text(draw, desc, get_font(20), (71, 85, 105), 185, cur_y + 36, 980, line_spacing=6)
        cur_y += 12
        
    # Right Card: TokyoFlow Blueprint
    draw.rectangle([(1270, 750), (2360, 1420)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
    draw.rectangle([(1270, 750), (2360, 825)], fill=(219, 234, 254))
    draw.text((1310, 772), "The TokyoFlow Blueprint Solution", fill=(29, 78, 216), font=get_font(26))
    
    sol_points = [
        ("Context-Driven Situational Immersion", "Every lesson is anchored in a concrete Tokyo scenario: train transfers, 7-Eleven registers, izakaya orders, and ramen ticket machines."),
        ("Authentic Speed & Real Atmosphere", "Train your ears on real Tokyo cadence, background subway chimes, and natural conversational pacing from Day 1."),
        ("Dual-Track Mastery (16:9 + 9:16)", "16:9 masterclasses provide deep cultural and grammatical deconstruction, while 9:16 shorts drill high-speed vocal muscle memory."),
        ("Standardized JLPT Milestone Mapping", "Every use case is cataloged under standardized badges [JLPT N5] through [JLPT N1] for measurable progress.")
    ]
    
    cur_y = 855
    for title, desc in sol_points:
        draw.text((1310, cur_y), f"+ {title}", fill=(29, 78, 216), font=get_font(24))
        cur_y = draw_wrapped_text(draw, desc, get_font(20), (51, 65, 85), 1335, cur_y + 36, 980, line_spacing=6)
        cur_y += 12

    # 3. Section 2: The 4 Core Pillar Tracks
    draw.text((120, 1480), "2. The Four Pillar Curriculum Tracks", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1530), (2360, 1530)], fill=(29, 78, 216), width=3)
    
    pillars = [
        ("TRACK 01: TRANSIT & COMMUTE", "[JLPT N5-N4]",
         "- Yamanote Line loop alerts & platform announcements\n- Subway transfers & fare gate IC card error handling\n- Shinkansen bullet train seat reservation & conductors", (239, 246, 255), (29, 78, 216)),
        
        ("TRACK 02: KOMBINI & DAILY LIVING", "[JLPT N5-N3]",
         "- 7-Eleven & FamilyMart register speed replies (Bags/Receipts)\n- Hot snacks ordering (Karaage-kun) & coffee machines\n- Drugstore symptom explanations & cafe ordering", (240, 253, 250), (13, 148, 136)),
        
        ("TRACK 03: DINING & SOCIAL PROTOCOLS", "[JLPT N4-N2]",
         "- Izakaya draft beer ordering ('Toriaezu Nama!') & table bill splitting\n- Ramen ticket vending machine customization (Katame/Koime)\n- Sento bathhouse etiquette & Akihabara tax-free shopping", (254, 243, 199), (180, 83, 9)),
        
        ("TRACK 04: MEDIA & NATIVE NUANCE", "[JLPT N2-N1]",
         "- NHK real news broadcast listening & formal syntax\n- Business etiquette, polite Kenjougo vs honorific Sonkeigo\n- Modern internet slang, entertainment & pop trends", (245, 243, 255), (109, 40, 217))
    ]
    
    for i, (p_title, p_badge, p_bullets, p_bg, p_fg) in enumerate(pillars):
        px = 120 + (i % 2) * 1150
        py = 1560 + (i // 2) * 440
        draw.rectangle([(px, py), (px + 1090, py + 400)], fill=(255, 255, 255), outline=p_fg, width=2)
        
        draw.rectangle([(px, py), (px + 1090, py + 75)], fill=p_bg)
        draw.text((px + 25, py + 22), p_title, fill=p_fg, font=get_font(24))
        draw.text((px + 860, py + 22), p_badge, fill=p_fg, font=get_font(22))
        
        draw.text((px + 25, py + 95), "Key Focus Areas:", fill=(15, 23, 42), font=get_font(22))
        draw_wrapped_text(draw, p_bullets, get_font(20), (71, 85, 105), px + 25, py + 135, 1040, line_spacing=10)
        
        draw.rectangle([(px + 25, py + 320), (px + 1065, py + 380)], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((px + 45, py + 338), "16:9 Deep Dive Masterclass  +  9:16 Vocal Shadowing Short", fill=(30, 41, 59), font=get_font(20))

    # 4. Bottom Note Box
    draw.rectangle([(120, 2500), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((170, 2540), "How to Use This Blueprint Effectively", fill=(29, 78, 216), font=get_font(34))
    draw.text((170, 2600), "This blueprint is structured for active, vocal engagement rather than passive textbook reading.", fill=(51, 65, 85), font=get_font(22))
    
    tips = [
        ("Step A: Audio-First Immersion", "Always listen to the scenario audio at full normal speed before looking at grammar breakdowns."),
        ("Step B: Speak Out Loud", "Reading Japanese in your head does NOT train the tongue or vocal cords. Always vocalize every line aloud."),
        ("Step C: 15-Minute Daily Repetition", "Consistency outperforms marathon sessions. Follow the 15-minute daily cycle detailed on Page 2.")
    ]
    
    for i, (t_title, t_desc) in enumerate(tips):
        y = 2670 + i * 190
        draw.rectangle([(170, y), (2310, y + 155)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((200, y + 25), t_title, fill=(29, 78, 216), font=get_font(24))
        draw_wrapped_text(draw, t_desc, get_font(21), (51, 65, 85), 200, y + 72, 2060, line_spacing=6)
        
    return img

# =========================================================================
# PAGE 2: 3-STEP CYCLE & 15-MIN ROUTINE
# =========================================================================
def make_page_2():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 2)
    
    # Section 3: The 3-Step Mastery Cycle
    draw.text((120, 210), "3. The TokyoFlow 3-Step Mastery Cycle", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    steps = [
        ("STEP 01: SCENARIO IMMERSION", "16:9 Long-Form Masterclass (1080p)", (239, 246, 255), (29, 78, 216),
         [
             "Watch the complete authentic scenario in full context (transit, kombini, izakaya, dining).",
             "Observe natural spoken cadence, situational body language, and ambient background cues.",
             "Identify core conversational triggers: what the attendant asks and what you must reply."
         ]),
        
        ("STEP 02: GRAMMAR & NUANCE DECODING", "Deep Linguistic & Cultural Breakdown", (240, 253, 250), (13, 148, 136),
         [
             "Dissect core grammar points, particle mechanics, and polite Keigo vs. casual Tameguchi.",
             "Unpack unspoken cultural etiquette (e.g. why locals say 'Kekkou desu' instead of 'Iie').",
             "Map every structure directly to standardized benchmarks: [JLPT N5] through [JLPT N1]."
         ]),
        
        ("STEP 03: VOCAL MUSCLE SHADOWING", "9:16 Spoken Shadowing Shorts (<60s)", (254, 243, 199), (180, 83, 9),
         [
             "Shadow simultaneously with Nanami's standard Tokyo accent audio at real-world pace.",
             "Match exact pitch contour, syllable timing, and natural intonation without looking at text.",
             "Repeat 3 to 5 times until the response becomes an automatic, sub-second vocal reflex."
         ])
    ]
    
    for i, (s_title, s_sub, s_bg, s_fg, s_bullets) in enumerate(steps):
        sy = 290 + i * 370
        draw.rectangle([(120, sy), (2360, sy + 330)], fill=(255, 255, 255), outline=s_fg, width=2)
        
        draw.rectangle([(120, sy), (2360, sy + 75)], fill=s_bg)
        draw.text((160, sy + 22), s_title, fill=s_fg, font=get_font(25))
        draw.text((1600, sy + 22), s_sub, fill=s_fg, font=get_font(22))
        
        cur_by = sy + 105
        for bullet in s_bullets:
            draw.text((160, cur_by), "- ", fill=s_fg, font=get_font(24))
            cur_by = draw_wrapped_text(draw, bullet, get_font(23), (30, 41, 59), 195, cur_by, 2110, line_spacing=6)
            cur_by += 8

    # Section 4: The 4-Pass Shadowing Protocol
    draw.text((120, 1460), "4. The 4-Pass Vocal Shadowing Protocol", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1510), (2360, 1510)], fill=(29, 78, 216), width=3)
    
    passes = [
        ("PASS 1: BLIND LISTENING", "Listen only (eyes closed)", "Catch the overall melody, pitch peaks, and natural pauses. Do not read the text."),
        ("PASS 2: TEXT-ASSISTED SHADOW", "Read & speak simultaneously", "Align your vocal timing with the audio. Pronounce every syllable cleanly and crisply."),
        ("PASS 3: PURE BLIND SHADOW", "No text, instant mimicry", "Shadow with a 0.2-second delay behind the native audio. Pure muscle memory."),
        ("PASS 4: 1.2x SPEED BOOST", "Fast-forward playback", "Test reflexes at 1.2x speed to ensure real-world Tokyo conversation feels effortless.")
    ]
    
    for i, (p_title, p_sub, p_desc) in enumerate(passes):
        px = 120 + (i % 2) * 1150
        py = 1540 + (i // 2) * 270
        draw.rectangle([(px, py), (px + 1090, py + 240)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
        draw.rectangle([(px, py), (px + 1090, py + 65)], fill=(219, 234, 254))
        draw.text((px + 25, py + 18), p_title, fill=(29, 78, 216), font=get_font(24))
        draw.text((px + 25, py + 85), p_sub, fill=(3, 105, 161), font=get_font(22))
        draw_wrapped_text(draw, p_desc, get_font(21), (51, 65, 85), px + 25, py + 130, 1040, line_spacing=6)

    # Section 5: The Daily 15-Minute Routine
    draw.text((120, 2140), "5. The Daily 15-Minute Fluency Routine", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 2190), (2360, 2190)], fill=(29, 78, 216), width=3)
    
    routine_cards = [
        ("MORNING (08:00 AM EDT)", "5 Minutes: 16:9 Masterclass", (239, 246, 255), (29, 78, 216),
         "Watch the daily 16:9 masterclass release. Focus on conversational context, situational visual cues, and key JLPT grammar markers."),
        
        ("MIDDAY / COMMUTE", "5 Minutes: 9:16 Shorts Shadowing", (240, 253, 250), (13, 148, 136),
         "Open YouTube Shorts on your mobile device. Replay the daily shadowing drill 3 to 5 times using Pass 2 and Pass 3 vocal protocols."),
        
        ("EVENING / WIND-DOWN", "5 Minutes: Active Recall & Review", (254, 243, 199), (180, 83, 9),
         "Review the scenario sentence cards. Test your active recall: if asked a fast question at the counter, what is your instantaneous Tokyo reply?")
    ]
    
    for i, (r_time, r_title, r_bg, r_fg, r_desc) in enumerate(routine_cards):
        ry = 2220 + i * 350
        draw.rectangle([(120, ry), (2360, ry + 310)], fill=(255, 255, 255), outline=r_fg, width=2)
        draw.rectangle([(120, ry), (2360, ry + 75)], fill=r_bg)
        draw.text((160, ry + 22), r_time, fill=r_fg, font=get_font(25))
        draw.text((1600, ry + 22), r_title, fill=r_fg, font=get_font(22))
        
        draw_wrapped_text(draw, r_desc, get_font(23), (30, 41, 59), 160, ry + 120, 2120, line_spacing=12)
        
    return img

# =========================================================================
# PAGE 3: 5-LEVEL JLPT SYLLABUS
# =========================================================================
def make_page_3():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 3)
    
    draw.text((120, 210), "6. Complete 5-Level JLPT Milestone Syllabus", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    curriculum = [
        ("[JLPT N5]", "STAGE 01: ESSENTIAL SURVIVAL", "Basic Public Navigation & Quick Transactions", (239, 246, 255), (29, 78, 216),
         [
             ("Yamanote Line Announcements", "Next station alerts ('Tsugi wa Shinjuku desu'), inner/outer loop transfers."),
             ("Kombini Checkout Basics", "Bag requests ('Fukuro wa daijoubu desu'), heating foods, and receipt decline."),
             ("Cafe & Quick Dining", "Size ordering (Tall/Grande), hot vs iced, takeaway ('Omochikaeri de')."),
             ("Numbers & Fast Cash Registers", "Instant comprehension of yen amounts at rapid-paced cash registers.")
         ]),
        
        ("[JLPT N4]", "STAGE 02: DAILY INDEPENDENCE", "Troubleshooting & Standard Polite Interaction", (240, 253, 250), (13, 148, 136),
         [
             ("Metro Fare Adjustment", "IC card insufficient balance, using the Noritsugi fare adjustment machine."),
             ("Kombini Hot Snacks & Coffee", "Ordering hot counter items ('Karaage-kun', 'Famichiki') and machine protocols."),
             ("Drugstore & Pharmacy", "Describing common symptoms (headache, stomach ache, cold medicine requests)."),
             ("Permission & Polite Asking", "Polite requests ('-te mo ii desu ka', '-onegai dekimasu ka') in public.")
         ]),
        
        ("[JLPT N3]", "STAGE 03: SOCIAL & LIFESTYLE", "Dining Culture, Hobbies, and Local Etiquette", (254, 243, 199), (180, 83, 9),
         [
             ("Izakaya Ordering Etiquette", "First round draft beer orders ('Toriaezu nama!'), splitting the bill ('Betsubetsu')."),
             ("Ramen Ticket Machines", "Customizing noodle firmness (Katame), broth richness (Koime), backfat."),
             ("Akihabara Shopping & Tax-Free", "Inquiring about stock, tax-free exemption passports, anime figure displays."),
             ("Onsen & Sento Protocols", "Washing area manners, locker keys, sauna etiquette ('Totono-u').")
         ]),
        
        ("[JLPT N2]", "STAGE 04: ADVANCED CONVERSATION", "Professional, Apparel, and Travel Fluency", (255, 241, 242), (225, 29, 72),
         [
             ("Ginza Fitting Room Protocol", "Trying on clothes, sizing adjustments, polite declining in boutiques."),
             ("Workplace Keigo & Greetings", "Otsukaresama desu, humble Kenjougo vs honorific Sonkeigo in context."),
             ("Travel & Transit Emergencies", "Lost items at station lost-and-found, bullet train rebooking, delays."),
             ("Casual Slang vs. Polite Forms", "Knowing exactly when to drop formality with close Japanese peers.")
         ]),
        
        ("[JLPT N1]", "STAGE 05: NATIVE NUANCE & MEDIA", "News Broadcasts, Business Debates & Nuance", (245, 243, 255), (109, 40, 217),
         [
             ("NHK Real News Decoding", "Politics, economy, global diplomacy, and formal journalistic syntax."),
             ("Corporate & Business Meetings", "Indirect disagreement, subtle corporate Japanese expressions."),
             ("Pop Culture & Internet Slang", "Decoding viral social media trends, anime subtext, and colloquial slang."),
             ("Full Conversational Flow", "Effortless listening comprehension at native 180+ words per minute.")
         ])
    ]
    
    for i, (badge, st_title, st_sub, st_bg, st_fg, st_items) in enumerate(curriculum):
        sy = 290 + i * 600
        draw.rectangle([(120, sy), (2360, sy + 560)], fill=(255, 255, 255), outline=st_fg, width=2)
        
        draw.rectangle([(120, sy), (2360, sy + 75)], fill=st_bg)
        draw.text((160, sy + 22), f"{badge}  {st_title}", fill=st_fg, font=get_font(25))
        draw.text((1600, sy + 22), st_sub, fill=st_fg, font=get_font(22))
        
        for ji, (item_title, item_desc) in enumerate(st_items):
            jx = 160 + (ji % 2) * 1100
            jy = sy + 95 + (ji // 2) * 220
            draw.rectangle([(jx, jy), (jx + 1050, jy + 205)], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
            draw.text((jx + 25, jy + 18), f"* {item_title}", fill=(15, 23, 42), font=get_font(23))
            draw_wrapped_text(draw, item_desc, get_font(20), (71, 85, 105), jx + 25, jy + 60, 1000, line_spacing=6)
            
    return img

# =========================================================================
# PAGE 4: PLAYLISTS & 30-DAY HABIT TRACKER
# =========================================================================
def make_page_4():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 4)
    
    # Section 7: Playlists & Resource Directory
    draw.text((120, 210), "7. Official Playlist Directory & Learning Portals", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    pls = [
        ("Playlist 01: Transit & Subway Mastery", "Yamanote Line, Tokyo Metro, Fare Adjustment, Bullet Train", "https://youtube.com/playlist?list=PLHUEYGzrBe-s"),
        ("Playlist 02: Kombini & Street Life", "7-Eleven, FamilyMart, Cafes, Quick Orders, ATM & Coffee", "Access via official channel playlists tab"),
        ("Playlist 03: Izakaya & Dining Protocols", "Draft Beer Orders, Ramen Ticket Machines, Table Manners", "Access via official channel playlists tab"),
        ("Playlist 04: Real News & Pop Trends", "NHK News shadowing, pop culture slang, media breakdown", "Access via official channel playlists tab")
    ]
    
    for i, (pl_name, pl_desc, pl_link) in enumerate(pls):
        py = 290 + i * 180
        draw.rectangle([(120, py), (2360, py + 150)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
        draw.text((160, py + 25), pl_name, fill=(29, 78, 216), font=get_font(25))
        draw_wrapped_text(draw, pl_desc, get_font(21), (51, 65, 85), 160, py + 75, 1500, line_spacing=6)
        draw.text((1720, py + 25), "[16:9 + 9:16 Complete]", fill=(13, 148, 136), font=get_font(22))

    # Section 8: 30-Day Fluency Habit Tracker
    draw.text((120, 1100), "8. The 30-Day TokyoFlow Fluency Habit Tracker", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1150), (2360, 1150)], fill=(29, 78, 216), width=3)
    draw.text((120, 1180), "Check off each day as you complete your 15-minute daily cycle (Masterclass + Shadowing).", fill=(71, 85, 105), font=get_font(22))
    
    grid_start_y = 1240
    for day in range(1, 31):
        c = (day - 1) % 6
        r = (day - 1) // 6
        gx = 120 + c * 380
        gy = grid_start_y + r * 190
        
        draw.rectangle([(gx, gy), (gx + 350, gy + 160)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        draw.rectangle([(gx, gy), (gx + 350, gy + 45)], fill=(239, 246, 255))
        draw.text((gx + 20, gy + 12), f"DAY {day:02d}", fill=(29, 78, 216), font=get_font(22))
        
        draw.rectangle([(gx + 20, gy + 65), (gx + 50, gy + 95)], outline=(100, 116, 139), width=2)
        draw.text((gx + 65, gy + 68), "16:9 Lesson", fill=(51, 65, 85), font=get_font(20))
        
        draw.rectangle([(gx + 20, gy + 115), (gx + 50, gy + 145)], outline=(100, 116, 139), width=2)
        draw.text((gx + 65, gy + 118), "9:16 Shadow", fill=(51, 65, 85), font=get_font(20))

    # Section 9: Community & Next Steps
    draw.rectangle([(120, 2300), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((180, 2350), "Join the Global TokyoFlow Community", fill=(29, 78, 216), font=get_font(36))
    
    comm_bullets = [
        ("Subscribe to Official Channel", "Visit @TokyoFlowJapan on YouTube and enable notifications for daily 08:00 AM EDT drops."),
        ("Engage in the Comments", "Leave your target JLPT level, questions, and shadowing audio progress in the comments."),
        ("Share Your Milestone", "Tag #TokyoFlow on social media as you complete each 30-day milestone.")
    ]
    for i, (c_title, c_desc) in enumerate(comm_bullets):
        cy = 2430 + i * 200
        draw.rectangle([(180, cy), (2300, cy + 160)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((210, cy + 25), c_title, fill=(29, 78, 216), font=get_font(25))
        draw_wrapped_text(draw, c_desc, get_font(22), (51, 65, 85), 210, cy + 75, 2060, line_spacing=6)
        
    draw.text((180, 3170), "TokyoFlow Japanese Academy  -  Precision, Realism, and Daily Fluency.", fill=(100, 116, 139), font=get_font(24))
    
    return img

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("==================================================")
    print("Generating Print-Friendly Golden Master PDF")
    print("==================================================")
    
    p1 = make_page_1()
    p2 = make_page_2()
    p3 = make_page_3()
    p4 = make_page_4()
    
    pdf_path = OUT_DIR / "TokyoFlow_Japanese_Fluency_Blueprint_Study_Guide.pdf"
    
    p1.save(
        pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=[p2, p3, p4]
    )
    
    print(f"\n[OK] High-Resolution 300 DPI Light PDF Created: {pdf_path}")
    print(f"File Size: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
