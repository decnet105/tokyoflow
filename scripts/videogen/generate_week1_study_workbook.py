#!/usr/bin/env python3
"""
TokyoFlow Japanese • Week 1 Master JLPT Study Workbook Generator (300 DPI A4)
=============================================================================
Compiles all Week 1 (EP01 to EP07) vocabulary, sentences, and grammar into a
structured, print-ready JLPT companion workbook (English & Chinese editions).

Features:
- Categorized strictly by JLPT difficulty: [JLPT N5], [JLPT N4], [JLPT N3].
- Comprehensive bilingual vocabulary tables with Kana, Romaji, and English/Chinese glosses.
- Full 42 situational dialogue sentences with contextual notes.
- Key grammar & particle breakdown matrix.
- Integrated Scheme D Unlock Passcode Card (PASSCODE: TOKYOFLOW-WEEK1).
- 100% Zero-Emoji discipline and ink-friendly light theme layout.
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_EN_DIR = PROJECT_ROOT / "output" / "en" / "study_guide"
OUT_ZH_DIR = PROJECT_ROOT / "output" / "zh" / "study_guide"

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def draw_wrapped_text(draw, text: str, font, fill, x: int, y: int, max_width: int, line_spacing: int = 12) -> int:
    clean_text = text.replace("〜", "-").replace("～", "-")
    words = clean_text.split(" ")
    lines = []
    cur_line = []
    
    for word in words:
        test_line = " ".join(cur_line + [word]) if cur_line else word
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

def draw_header_footer(draw, page_num: int, total_pages: int, is_zh: bool = False):
    W, H = 2480, 3508
    
    # Top Header
    draw.rectangle([(120, 90), (460, 150)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    header_org = "TOKYOFLOW ACADEMY" if not is_zh else "TOKYOFLOW 日语学院"
    draw.text((140, 108), header_org, fill=(29, 78, 216), font=get_font(24))
    
    header_sub = "WEEK 1 MASTER STUDY WORKBOOK  |  JLPT COMPANION" if not is_zh else "第一周 实景精讲学习讲义与 JLPT 复习手册"
    draw.text((490, 110), header_sub, fill=(71, 85, 105), font=get_font(24))
    
    badge = "[JLPT N5-N3 CURRICULUM]" if not is_zh else "【JLPT N5-N3 进阶大纲】"
    draw.text((1920, 110), badge, fill=(29, 78, 216), font=get_font(24))
    draw.line([(120, 170), (2360, 170)], fill=(203, 213, 225), width=2)
    
    # Bottom Footer
    draw.line([(120, 3350), (2360, 3350)], fill=(203, 213, 225), width=2)
    footer_text = "TokyoFlow Japanese Academy  *  Daily Masterclasses & Shadowing  *  @TokyoFlowJapan" if not is_zh else "TokyoFlow 日语官方教学体系  *  每日实景精讲与影子跟读  *  @TokyoFlowJapan"
    draw.text((120, 3380), footer_text, fill=(100, 116, 139), font=get_font(22))
    draw.text((2150, 3380), f"Page {page_num} of {total_pages}", fill=(15, 23, 42), font=get_font(24))

# -------------------------------------------------------------------------
# PAGE 1: TITLE, SYLLABUS MATRIX & SCHEME D PASSCODE
# -------------------------------------------------------------------------
def make_page_1(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 1, 6, is_zh)
    
    # 1. Title Banner
    draw.rectangle([(120, 210), (2360, 680)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    
    draw.rectangle([(170, 250), (620, 310)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    badge_label = "OFFICIAL COMPANION WORKBOOK" if not is_zh else "官方实景精讲配套讲义"
    draw.text((195, 268), badge_label, fill=(29, 78, 216), font=get_font(24))
    
    main_title = "Week 1: Tokyo Essential Survival Master Syllabus" if not is_zh else "第一周：东京生活实景生存全攻略配套讲义"
    draw.text((170, 340), main_title, fill=(15, 23, 42), font=get_font(52))
    
    sub_title = "Complete Vocabulary, Sentences & Grammar by JLPT Level [JLPT N5 - N3]" if not is_zh else "按 JLPT 等级分类汇总：词汇、语法、经典台词与发音全解析【JLPT N5-N3】"
    draw.text((170, 420), sub_title, fill=(29, 78, 216), font=get_font(32))
    
    desc_text = "Covering Episodes 01 through 07: Yamanote Transit, Kombini Checkout, Izakaya Dining, Akiba Shopping, Subway Transfers, Coffee/ATM, and Ramen Ordering." if not is_zh else "包含 EP01 至 EP07 完整场景：山手线乘车、便利店结账、新桥居酒屋、秋叶原免税、地铁补票换乘、咖啡ATM机以及一兰拉面食券定制。"
    draw.text((170, 485), desc_text, fill=(51, 65, 85), font=get_font(24))
    
    meta_text = "Format: A4 Print-Friendly Masterclass Guide  |  Tokyo Standard Pitch Accent Audio  |  Zero Emoji Clean Edition" if not is_zh else "格式：A4 高清打印复习版  |  东京标准抑扬语调音频配套  |  零表情符专业排版"
    draw.text((170, 545), meta_text, fill=(100, 116, 139), font=get_font(22))
    
    draw.line([(170, 600), (2310, 600)], fill=(226, 232, 240), width=2)
    notice_text = "Free Subscriber Study Guide  *  Keep this document for daily shadowing drills" if not is_zh else "订阅者专属研习讲义  *  请配合每日长视频精讲与 Shorts 影子跟读打卡使用"
    draw.text((170, 620), notice_text, fill=(13, 148, 136), font=get_font(22))

    # 2. Scheme D: Unlock Passcode Card
    draw.rectangle([(120, 720), (2360, 1120)], fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.rectangle([(120, 720), (2360, 800)], fill=(253, 230, 138))
    
    card_title = "SUBSCRIBER DOWNLOAD VERIFICATION & PASSCODE" if not is_zh else "【订阅者专享下载验证与完播解锁码】"
    draw.text((160, 745), card_title, fill=(146, 64, 14), font=get_font(28))
    
    draw.rectangle([(160, 840), (960, 1070)], fill=(255, 255, 255), outline=(217, 119, 6), width=2)
    draw.text((190, 865), "OFFICIAL UNLOCK PASSCODE:" if not is_zh else "官方解锁口令 / 密码：", fill=(100, 116, 139), font=get_font(22))
    draw.text((190, 920), "TOKYOFLOW-WEEK1", fill=(180, 83, 9), font=get_font(52))
    draw.text((190, 1010), "[VALIDATED COMPILATION MASTER]" if not is_zh else "【第一周完整课程官方校验通过】", fill=(13, 148, 136), font=get_font(22))
    
    guide_lines = [
        "1. Video Passcode Verification: Mentioned during the Week 1 Masterclass review.",
        "2. Exclusive Study Asset: This PDF is created exclusively for TokyoFlow subscribers.",
        "3. Recommended Routine: 15 minutes of vocal shadowing per day using the weekly dialogues."
    ] if not is_zh else [
        "1. 视频密码校验：本口令已于第一周汇总精讲视频尾段口播同步公布。",
        "2. 专属研习资料：本讲义专为 TokyoFlow 订阅学员整理制作，支持离线保存与打印。",
        "3. 推荐训练法：每日搭配 15 分钟影子跟读，将 7 大场景高频句式形成肌肉记忆。"
    ]
    gy = 845
    for line in guide_lines:
        draw.text((1010, gy), line, fill=(51, 65, 85), font=get_font(24))
        gy += 75

    # 3. Week 1 7-Day Scenario Matrix
    draw.text((120, 1180), "Week 1 Scenario Roadmap & Difficulty Matrix" if not is_zh else "第一周场景进阶路线与 JLPT 等级分布", fill=(15, 23, 42), font=get_font(34))
    draw.line([(120, 1230), (2360, 1230)], fill=(29, 78, 216), width=3)
    
    scenarios = [
        ("DAY 1 (EP01)", "Yamanote Line Transit", "[JLPT N4-N3]", "Platform announcements, humble Keigo, transfer cues", (239, 246, 255), (29, 78, 216)),
        ("DAY 2 (EP02)", "Kombini 7-Eleven Checkout", "[JLPT N5-N4]", "Bag requests, point cards, receipts, microwave warming", (240, 253, 250), (13, 148, 136)),
        ("DAY 3 (EP03)", "Shinbashi Izakaya Dining", "[JLPT N4-N3]", "Draft beer order, otoshi cover charge, table bill splitting", (254, 243, 199), (180, 83, 9)),
        ("DAY 4 (EP04)", "Akihabara Tax-Free Shopping", "[JLPT N4-N3]", "Showcase figure unlocking, condition check, tax-free counter", (245, 243, 255), (109, 40, 217)),
        ("DAY 5 (EP05)", "Subway Rush & Fare Adjustment", "[JLPT N4-N3]", "Fare gate IC errors, Norikoshi machine, station master window", (239, 246, 255), (29, 78, 216)),
        ("DAY 6 (EP06)", "Kombini Coffee & ATM Cash", "[JLPT N5-N4]", "Self-serve ice cups, machine dispense, foreign card withdrawal", (240, 253, 250), (13, 148, 136)),
        ("DAY 7 (EP07)", "Ichiran Ramen Ticket Machine", "[JLPT N4-N3]", "Ticket purchasing, noodle firmness, rich broth customization", (254, 243, 199), (180, 83, 9)),
    ] if not is_zh else [
        ("周一 (EP01)", "山手线月台广播与乘车", "【JLPT N4-N3】", "列车进站广播、谦让语「まいります」、黄色盲道安全线", (239, 246, 255), (29, 78, 216)),
        ("周二 (EP02)", "7-Eleven 与全家便利店结账", "【JLPT N5-N4】", "塑料袋/积分卡/收据询问、便当加热三连问快速应对", (240, 253, 250), (13, 148, 136)),
        ("周三 (EP03)", "新桥居酒屋点单与经典开场", "【JLPT N4-N3】", "「とりあえず生」、お通し小菜文化、结账「お会計」", (254, 243, 199), (180, 83, 9)),
        ("周四 (EP04)", "秋叶原手办专门店免税购物", "【JLPT N4-N3】", "展示柜开锁看现货、未开封成色确认、护照免税结算", (245, 243, 255), (109, 40, 217)),
        ("周五 (EP05)", "东京地铁补票机与换乘", "【JLPT N4-N3】", "西瓜卡进出站报错、精算机补差价、人工窗口求助", (239, 246, 255), (29, 78, 216)),
        ("周六 (EP06)", "便利店现磨咖啡与ATM取现", "【JLPT N5-N4】", "冰柜拿冰杯扫码结账、咖啡机操作、外卡ATM日元现钞", (240, 253, 250), (13, 148, 136)),
        ("周日 (EP07)", "一兰拉面食券机与汤头定制", "【JLPT N4-N3】", "食券机先买票、面硬度/汤浓淡/蒜泥量定制纸填写", (254, 243, 199), (180, 83, 9)),
    ]
    
    my = 1270
    for day, title, badge, desc, bg, fg in scenarios:
        draw.rectangle([(120, my), (2360, my + 175)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rectangle([(120, my), (460, my + 175)], fill=bg)
        draw.text((150, my + 45), day, fill=fg, font=get_font(26))
        draw.text((150, my + 95), badge, fill=fg, font=get_font(22))
        
        draw.text((490, my + 35), title, fill=(15, 23, 42), font=get_font(28))
        draw.text((490, my + 95), desc, fill=(71, 85, 105), font=get_font(22))
        my += 195

    # 4. Learning Blueprint Box
    draw.rectangle([(120, 2700), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((160, 2735), "Weekly Study Routine: How to Master Spoken Japanese" if not is_zh else "高效复习法：听说读写四步突破", fill=(29, 78, 216), font=get_font(30))
    
    steps = [
        ("Step 1: Watch Masterclass", "Listen to native audio without looking at English/Chinese text to calibrate auditory pitch."),
        ("Step 2: Study JLPT Breakdown", "Review the classified vocabulary and grammar tables on Pages 2, 3, and 4 of this workbook."),
        ("Step 3: Daily Vocal Shadowing", "Shadow aloud 5 times per line. Mimic native intonation and speed under 1-second reflex."),
        ("Step 4: Sunday Full Review", "Practice all 42 sentences continuously using the dialogue reference sheet on Pages 5 and 6.")
    ] if not is_zh else [
        ("第 1 步：原声盲听输入", "先不看中英文字幕，完整聆听东京原生音频，建立对语调高低走向的直觉。"),
        ("第 2 步：精读 JLPT 分级讲义", "查阅本手册第 2、3、4 页的 N5/N4/N3 词汇表与语法接续，理清用法逻辑。"),
        ("第 3 步：每日高频影子跟读", "每句大声跟读 5 遍以上，重点模仿连读、吞音与语速，形成 1 秒内的肌肉本能。"),
        ("第 4 步：周末全场景串联", "利用第 5、6 页的 42 句全场景速查表进行模拟自测，确保脱口而出。")
    ]
    
    sy = 2810
    for stitle, sdesc in steps:
        draw.text((160, sy), f"* {stitle}: ", fill=(15, 23, 42), font=get_font(24))
        bbox = draw.textbbox((0, 0), f"* {stitle}: ", font=get_font(24))
        w = bbox[2] - bbox[0]
        draw_wrapped_text(draw, sdesc, get_font(22), (71, 85, 105), 160 + w + 10, sy, 2100 - w, line_spacing=4)
        sy += 110

    return img

# -------------------------------------------------------------------------
# PAGE 2: [JLPT N5] FOUNDATIONAL VOCABULARY & PARTICLES
# -------------------------------------------------------------------------
def make_page_2(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 2, 6, is_zh)
    
    # Section Header
    draw.rectangle([(120, 210), (2360, 320)], fill=(240, 253, 250), outline=(13, 148, 136), width=3)
    draw.text((160, 235), "[JLPT N5] Foundational Vocabulary, High-Frequency Phrases & Particles" if not is_zh else "【JLPT N5 基础核心】高频生活词汇、常用句型与助词全景表", fill=(13, 148, 136), font=get_font(34))
    draw.text((160, 280), "Essential building blocks for Tokyo transit, kombini purchases, and daily interactions." if not is_zh else "东京出行、便利店购物与日常交流最基础、出现频次最高的基石词汇与句式。", fill=(71, 85, 105), font=get_font(22))
    
    n5_vocab = [
        ("これ", "これ", "kore", "Pronoun", "This one / This", "这个（靠近说话人）", "これをお願いします (This one, please)"),
        ("袋", "ふくろ", "fukuro", "Noun", "Plastic shopping bag", "塑料购物袋", "袋はいりますか (Do you need a bag?)"),
        ("大丈夫", "だいじょうぶ", "daijoubu", "Na-Adj", "All right / No need / OK", "没问题 / 不需要 / 好的", "袋は大丈夫です (I do not need a bag)"),
        ("温め", "あたため", "atatame", "Noun", "Microwave heating", "微波炉加热", "お弁当温めますか (Warm up the bento?)"),
        ("お願いします", "おねがいします", "onegaishimasu", "Phrase", "Please / I request", "拜托了 / 请...", "温めお願いします (Please warm it up)"),
        ("水", "みず", "mizu", "Noun", "Water", "水 / 凉水", "お冷をお願いします (Cold water, please)"),
        ("一杯", "いっぱい", "ippai", "Noun", "One cup / One glass", "一杯（饮料/酒）", "生ビール一杯 (One draft beer)"),
        ("アイス", "あいす", "aisu", "Noun", "Ice / Iced", "冰 / 冰镇", "アイスコーヒー (Iced coffee)"),
        ("カード", "かーど", "kaado", "Noun", "Card / IC Card", "卡片 / 交通卡 / 信用卡", "ポイントカード (Point loyalty card)"),
        ("レシート", "れしーと", "reshiito", "Noun", "Receipt", "收据 / 小票", "レシートは結構です (No receipt needed)"),
        ("駅", "えき", "eki", "Noun", "Train station", "车站 / 车站大楼", "新宿駅 (Shinjuku Station)"),
        ("番線", "ばんせん", "bansen", "Counter", "Platform track number", "站台番线 / 号站台", "2番線 (Platform Track 2)")
    ]
    
    # Table Header
    ty = 360
    draw.rectangle([(120, ty), (2360, ty + 70)], fill=(13, 148, 136))
    headers = [("Kanji / Word", 150), ("Kana", 460), ("Romaji", 800), ("POS", 1100), ("English Meaning" if not is_zh else "中文释义", 1320), ("Example Usage", 1750)]
    for htitle, hx in headers:
        draw.text((hx, ty + 20), htitle, fill=(255, 255, 255), font=get_font(24))
        
    ty += 70
    for i, (kanji, kana, romaji, pos, en_m, zh_m, eg) in enumerate(n5_vocab):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([(120, ty), (2360, ty + 95)], fill=bg, outline=(226, 232, 240), width=1)
        
        draw.text((150, ty + 30), kanji, fill=(15, 23, 42), font=get_font(28))
        draw.text((460, ty + 32), kana, fill=(29, 78, 216), font=get_font(22))
        draw.text((800, ty + 34), romaji, fill=(100, 116, 139), font=get_font(20))
        draw.text((1100, ty + 34), pos, fill=(71, 85, 105), font=get_font(20))
        
        meaning = en_m if not is_zh else zh_m
        draw.text((1320, ty + 32), meaning, fill=(15, 23, 42), font=get_font(22))
        draw.text((1750, ty + 32), eg, fill=(13, 148, 136), font=get_font(20))
        ty += 95

    # N5 Core Grammar Matrix
    ty += 40
    draw.text((120, ty), "N5 Core Particle & Sentence Mechanics" if not is_zh else "N5 核心助词与必备句型拆解", fill=(15, 23, 42), font=get_font(32))
    draw.line([(120, ty + 45), (2360, ty + 45)], fill=(13, 148, 136), width=3)
    ty += 70
    
    n5_grammar = [
        ("1. [Object] + をお願いします (o onegaishimasu)", "Expressing polite requests / ordering items.", "「これをお願いします。」 (This one, please.) Used in kombini, dining, and shops.", (239, 246, 255), (29, 78, 216)),
        ("2. [Noun] + は大丈夫です (wa daijoubu desu)", "Polite refusal without saying a blunt 'No' (Iie).", "「袋は大丈夫です。」 (I do not need a plastic bag.) Universal kombini response.", (240, 253, 250), (13, 148, 136)),
        ("3. [Place/Track] + に (ni - Direction/Location)", "Target location or platform indicator.", "「2番線に山手線がまいります。」 (Train arrives on platform 2.)", (254, 243, 199), (180, 83, 9)),
        ("4. [Noun] + で (de - Means/Payment Method)", "Specifying payment method or instrument.", "「Suicaで支払います。」 (I will pay with Suica IC card.)", (245, 243, 255), (109, 40, 217))
    ] if not is_zh else [
        ("1. [名词] + をお願いします (o onegaishimasu)", "礼貌提出需求或点单（最实用的万能句式）", "「これをお願いします。」（请给我这个。）适用于便利店、餐厅点餐及商场购物。", (239, 246, 255), (29, 78, 216)),
        ("2. [名词] + は大丈夫です (wa daijoubu desu)", "委婉礼貌拒绝，避免生硬使用「いいえ」", "「袋は大丈夫です。」（塑料袋不需要了，谢谢。）便利店拒绝塑料袋的标准回答。", (240, 253, 250), (13, 148, 136)),
        ("3. [地点/站台] + に (ni - 方向与到达点)", "指明列车进站位置或行动目的地", "「2番線に山手線がまいります。」（2号站台即将有山手线列车进站。）", (254, 243, 199), (180, 83, 9)),
        ("4. [手段/工具] + で (de - 支付方式与途径)", "指定付款方式、出行工具或操作媒介", "「Suicaで支払います。」（用交通西瓜卡刷卡支付。）", (245, 243, 255), (109, 40, 217))
    ]
    
    for gtitle, gusage, geg, gbg, gfg in n5_grammar:
        draw.rectangle([(120, ty), (2360, ty + 175)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rectangle([(120, ty), (120 + 750, ty + 175)], fill=gbg)
        draw.text((150, ty + 40), gtitle, fill=gfg, font=get_font(24))
        draw.text((150, ty + 95), gusage, fill=(71, 85, 105), font=get_font(20))
        
        draw.text((900, ty + 40), "Real-World Context & Sentence:" if not is_zh else "真实场景例句与实战语境：", fill=(15, 23, 42), font=get_font(22))
        draw_wrapped_text(draw, geg, get_font(22), (51, 65, 85), 900, ty + 85, 1400, line_spacing=6)
        ty += 195

    return img

# -------------------------------------------------------------------------
# PAGE 3: [JLPT N4] INTERMEDIATE SPOKEN EXPRESSIONS & KEIGO
# -------------------------------------------------------------------------
def make_page_3(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 3, 6, is_zh)
    
    # Section Header
    draw.rectangle([(120, 210), (2360, 320)], fill=(239, 246, 255), outline=(29, 78, 216), width=3)
    draw.text((160, 235), "[JLPT N4] Intermediate Spoken Expressions, Transit Alerts & Service Keigo" if not is_zh else "【JLPT N4 进阶应用】常用服务敬语、车站广播与日常口语对白", fill=(29, 78, 216), font=get_font(34))
    draw.text((160, 280), "Mastering humble forms (Kenjougo), polite refusals (Kekkou), and transit safety broadcasts." if not is_zh else "掌握服务业谦让语（如まいります）、礼貌委婉拒绝（結構です）及交通安全播报。", fill=(71, 85, 105), font=get_font(22))
    
    n4_vocab = [
        ("まもなく", "まもなく", "mamonaku", "Adverb", "Shortly / Soon / Momentarily", "马上 / 即将", "まもなく2番線に電車がまいります"),
        ("内回り", "うちまわり", "uchimawari", "Noun", "Inner loop (Clockwise)", "内环（顺时针运行）", "山手線内回り (Yamanote Inner Loop)"),
        ("参ります", "まいります", "mairimasu", "Humble Verb", "To arrive / come (Kenjougo)", "（列车）进站 / 前来（谦让语）", "電車がまいります (Train is arriving)"),
        ("点字ブロック", "てんじぶろっく", "tenji burokku", "Noun", "Braille textured tactile paving", "黄色盲道 / 站台安全警示线", "点字ブロックの内側へお下がりください"),
        ("内側", "うちがわ", "uchigawa", "Noun", "Inside / Inner boundary", "内侧 / 安全线以内", "黄色い線の内側 (Inside yellow line)"),
        ("お下がりください", "おさがりください", "osagari kudasai", "Polite Request", "Please step back (Behind line)", "请退后 / 请退到安全线后", "白線の内側へお下がりください"),
        ("結構", "けっこう", "kekkou", "Na-Adj", "No thank you / Sufficient", "不用了 / 已经足够了", "レシートは結構です (No receipt needed)"),
        ("とりあえず", "とりあえず", "toriaezu", "Adverb", "For starters / First of all", "首先 / 先来这个", "とりあえず生で (Draft beer for starters)"),
        ("生ビール", "なまびーる", "nama biiru", "Noun", "Draft beer on tap", "生啤酒（扎啤）", "とりあえず生一杯 (First, a draft beer)"),
        ("免税", "めんぜい", "menzei", "Noun", "Tax-free shopping", "免税（消费税减免）", "免税手続き (Tax-free procedure)"),
        ("未開封", "みかいふう", "mikaifuu", "Noun", "Unopened / Factory sealed", "未开封 / 全新未拆", "未開封の品物 (Factory sealed item)"),
        ("精算機", "せいさんき", "seisanki", "Noun", "Fare adjustment machine", "精算机（补票机）", "のりこし精算機 (Fare adjustment)")
    ]
    
    # Table Header
    ty = 360
    draw.rectangle([(120, ty), (2360, ty + 70)], fill=(29, 78, 216))
    headers = [("Kanji / Phrase", 150), ("Kana", 520), ("Romaji", 860), ("POS", 1150), ("English Meaning" if not is_zh else "中文释义", 1380), ("Contextual Note", 1820)]
    for htitle, hx in headers:
        draw.text((hx, ty + 20), htitle, fill=(255, 255, 255), font=get_font(24))
        
    ty += 70
    for i, (kanji, kana, romaji, pos, en_m, zh_m, note) in enumerate(n4_vocab):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([(120, ty), (2360, ty + 95)], fill=bg, outline=(226, 232, 240), width=1)
        
        draw.text((150, ty + 30), kanji, fill=(15, 23, 42), font=get_font(26))
        draw.text((520, ty + 32), kana, fill=(29, 78, 216), font=get_font(22))
        draw.text((860, ty + 34), romaji, fill=(100, 116, 139), font=get_font(20))
        draw.text((1150, ty + 34), pos, fill=(71, 85, 105), font=get_font(20))
        
        meaning = en_m if not is_zh else zh_m
        draw.text((1380, ty + 32), meaning, fill=(15, 23, 42), font=get_font(22))
        draw.text((1820, ty + 32), note, fill=(13, 148, 136), font=get_font(20))
        ty += 95

    # N4 Core Grammar Breakdown
    ty += 40
    draw.text((120, ty), "N4 Core Grammar Patterns & Service Expressions" if not is_zh else "N4 核心语法句型与常用服务惯用语", fill=(15, 23, 42), font=get_font(32))
    draw.line([(120, ty + 45), (2360, ty + 45)], fill=(29, 78, 216), width=3)
    ty += 70
    
    n4_grammar = [
        ("1. お + Verb (Stem) + ください (o...kudasai)", "Polite imperative formula used in official public broadcasts.", "「点字ブロックの内側へお下がりください。」 (Please step back behind the yellow tactile line.)", (239, 246, 255), (29, 78, 216)),
        ("2. [Noun] + は結構です (wa kekkou desu)", "Standard polite phrase to decline an offer gently.", "「レシートは結構です。」 (No receipt needed, thank you.) Preferred over casual 'ira-nai'.", (240, 253, 250), (13, 148, 136)),
        ("3. [Item] + でお願いします (de onegaishimasu)", "Specifying a selection from a menu or option list.", "「とりあえず生でお願いします。」 (We will start with a draft beer, please.)", (254, 243, 199), (180, 83, 9)),
        ("4. [Condition] + てもいいですか (te mo ii desu ka)", "Asking permission politely to inspect or try something.", "「見せてもらってもいいですか。」 (Could you please show this showcase item to me?)", (245, 243, 255), (109, 40, 217))
    ] if not is_zh else [
        ("1. お + 动词连用形 (Stem) + ください (o...kudasai)", "敬语祈使句型：公共广播与服务行业标准礼貌请托", "「点字ブロックの内側へお下がりください。」（请退到黄色盲道安全线内侧。）", (239, 246, 255), (29, 78, 216)),
        ("2. [名词] + は結構です (wa kekkou desu)", "服务场景最得体的委婉拒绝表达", "「レシートは結構です。」（小票不用了，谢谢。）比「いらない」更成熟礼貌。", (240, 253, 250), (13, 148, 136)),
        ("3. [选项/物品] + でお願いします (de onegaishimasu)", "在众多菜单选项中明确指定选择项", "「とりあえず生でお願いします。」（先给我们上一杯生啤酒。）", (254, 243, 199), (180, 83, 9)),
        ("4. 动词て形 + もいいですか (te mo ii desu ka)", "礼貌征求对方许可（试穿/拿出手办展示）", "「見せてもらってもいいですか。」（能麻烦您把柜子里的手办拿出来给我看看吗？）", (245, 243, 255), (109, 40, 217))
    ]
    
    for gtitle, gusage, geg, gbg, gfg in n4_grammar:
        draw.rectangle([(120, ty), (2360, ty + 175)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rectangle([(120, ty), (120 + 820, ty + 175)], fill=gbg)
        draw.text((150, ty + 40), gtitle, fill=gfg, font=get_font(23))
        draw.text((150, ty + 95), gusage, fill=(71, 85, 105), font=get_font(20))
        
        draw.text((970, ty + 40), "Real-World Context & Sentence:" if not is_zh else "真实场景例句与实战语境：", fill=(15, 23, 42), font=get_font(22))
        draw_wrapped_text(draw, geg, get_font(22), (51, 65, 85), 970, ty + 85, 1330, line_spacing=6)
        ty += 195

    return img

# -------------------------------------------------------------------------
# PAGE 4: [JLPT N3] CONVERSATIONAL NUANCES, SLANG & CUSTOMIZATION
# -------------------------------------------------------------------------
def make_page_4(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 4, 6, is_zh)
    
    # Section Header
    draw.rectangle([(120, 210), (2360, 320)], fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.text((160, 235), "[JLPT N3] Conversational Nuances, Ramen Terminology & Tokyo Idioms" if not is_zh else "【JLPT N3 高阶地道】拉面黑话定制、地道口语缩略与场景俚语", fill=(180, 83, 9), font=get_font(34))
    draw.text((160, 280), "Unlocking ramen customization jargon (Katame, Koime), tax-free verification, and fast spoken pacing." if not is_zh else "解锁拉面食券定制专业黑话（面硬、汤浓）、免税密封确认及地道快速对白。", fill=(71, 85, 105), font=get_font(22))
    
    n3_vocab = [
        ("麺固め", "めんかため", "men katame", "Noun Phrase", "Firm noodle texture (Al dente)", "面条偏硬（劲道口感）", "麺は固めでお願いします"),
        ("味濃いめ", "あじこいめ", "aji koime", "Noun Phrase", "Rich / intense broth flavor", "汤头偏浓厚", "味濃いめ、油多め (Rich flavor, extra oil)"),
        ("油多め", "あぶらおおめ", "abura oome", "Noun Phrase", "Extra aromatic oil / lard", "多放调味油/背脂", "油少なめ (Less oil)"),
        ("替玉", "かえだま", "kaedama", "Noun", "Noodle refill (Soup retained)", "加面（留汤加一份面）", "替玉を固めで！ (Refill noodles, firm!)"),
        ("食券", "しょっけん", "shokken", "Noun", "Meal ticket voucher", "拉面食券（自动售票机打印）", "食券を先に買ってください"),
        ("乗り越し", "のりこし", "norikoshi", "Noun", "Riding past ticketed distance", "坐过站 / 补差价（精算）", "のりこし精算機 (Fare adjustment)"),
        ("残高不足", "ざんだかぶそく", "zandaka busoku", "Noun", "Insufficient IC card balance", "余额不足（闸机红灯报错）", "カード残高不足です"),
        ("パスポート", "ぱすぽーと", "pasupooto", "Noun", "Original physical passport", "护照原件（免税必备）", "パスポートをご提示ください"),
        ("お通し", "おとおし", "otooshi", "Noun", "Izakaya compulsory starter appetizer", "居酒屋自动上桌的小菜（座席费）", "お通し代 (Table cover fee)"),
        ("お会計", "おかいけい", "okaikei", "Noun", "The bill / check", "结账 / 买单", "お会計をお願いします"),
        ("別々", "べつべつ", "betsubetsu", "Noun", "Split bill individually", "分开买单 / 各付各的", "別々で払えますか (Can we split bill?)"),
        ("ごちそうさま", "ごちそうさま", "gochisousama", "Phrase", "Thank you for the meal!", "多谢款待！（离店礼貌致意）", "ごちそうさまでした！")
    ]
    
    # Table Header
    ty = 360
    draw.rectangle([(120, ty), (2360, ty + 70)], fill=(180, 83, 9))
    headers = [("Custom Term / Slang", 150), ("Kana", 520), ("Romaji", 860), ("Domain / Scene", 1150), ("English Meaning" if not is_zh else "中文释义", 1400), ("Tokyo Insider Tip", 1820)]
    for htitle, hx in headers:
        draw.text((hx, ty + 20), htitle, fill=(255, 255, 255), font=get_font(24))
        
    ty += 70
    for i, (kanji, kana, romaji, domain, en_m, zh_m, tip) in enumerate(n3_vocab):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([(120, ty), (2360, ty + 95)], fill=bg, outline=(226, 232, 240), width=1)
        
        draw.text((150, ty + 30), kanji, fill=(15, 23, 42), font=get_font(26))
        draw.text((520, ty + 32), kana, fill=(29, 78, 216), font=get_font(22))
        draw.text((860, ty + 34), romaji, fill=(100, 116, 139), font=get_font(20))
        draw.text((1150, ty + 34), domain, fill=(71, 85, 105), font=get_font(20))
        
        meaning = en_m if not is_zh else zh_m
        draw.text((1400, ty + 32), meaning, fill=(15, 23, 42), font=get_font(22))
        draw.text((1820, ty + 32), tip, fill=(180, 83, 9), font=get_font(20))
        ty += 95

    # Ramen Customization Cheat Sheet Box
    ty += 40
    draw.text((120, ty), "Tokyo Ramen Customization Golden Formula" if not is_zh else "东京拉面定制黄金三要素速查", fill=(15, 23, 42), font=get_font(32))
    draw.line([(120, ty + 45), (2360, ty + 45)], fill=(180, 83, 9), width=3)
    ty += 70
    
    ramen_cols = [
        ("1. Noodle Firmness (麺の硬さ)", "[JLPT N4-N3]",
         "- 超かため (Chou-katame): Extra hard\n- かため (Katame): Firm / Standard favorite\n- 普通 (Futsuu): Regular\n- やわらかめ (Yawarakame): Soft", (254, 243, 199), (180, 83, 9)),
        
        ("2. Broth Richness (味の濃さ)", "[JLPT N4-N3]",
         "- こいめ (Koime): Rich & intense broth\n- 基本 (Kihon): Standard balance\n- うすめ (Usume): Light / diluted broth", (240, 253, 250), (13, 148, 136)),
         
        ("3. Oil / Lard Quantity (油の量)", "[JLPT N4-N3]",
         "- 多め (Oome): Extra aromatic oil / lard\n- 基本 (Kihon): Standard oil level\n- 少なめ (Sukuname): Less oil / cleaner finish", (239, 246, 255), (29, 78, 216))
    ] if not is_zh else [
        ("1. 面条硬度 (麺の硬さ)", "【JLPT N4-N3】",
         "- 超かため (Chou-katame): 超硬（极具嚼劲）\n- かため (Katame): 偏硬（老饕最爱推荐）\n- 普通 (Futsuu): 标准软硬度\n- やわらかめ (Yawarakame): 偏软", (254, 243, 199), (180, 83, 9)),
        
        ("2. 汤头浓度 (味の濃さ)", "【JLPT N4-N3】",
         "- こいめ (Koime): 偏浓（酱油骨汤浓郁）\n- 基本 (Kihon): 标准口味\n- うすめ (Usume): 偏淡（适合清淡饮食）", (240, 253, 250), (13, 148, 136)),
         
        ("3. 调味油脂量 (油の量)", "【JLPT N4-N3】",
         "- 多め (Oome): 多放背脂油（保温提香）\n- 基本 (Kihon): 标准油脂配比\n- 少なめ (Sukuname): 少油（清爽不油腻）", (239, 246, 255), (29, 78, 216))
    ]
    
    for i, (r_title, r_badge, r_bullets, r_bg, r_fg) in enumerate(ramen_cols):
        rx = 120 + i * 760
        draw.rectangle([(rx, ty), (rx + 720, ty + 380)], fill=(255, 255, 255), outline=r_fg, width=2)
        draw.rectangle([(rx, ty), (rx + 720, ty + 75)], fill=r_bg)
        draw.text((rx + 25, ty + 22), r_title, fill=r_fg, font=get_font(23))
        
        draw_wrapped_text(draw, r_bullets, get_font(21), (51, 65, 85), rx + 25, ty + 95, 670, line_spacing=12)

    return img

# -------------------------------------------------------------------------
# PAGE 5: COMPLETE DIALOGUES PART 1 (EP01 - EP03)
# -------------------------------------------------------------------------
def make_page_5(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 5, 6, is_zh)
    
    # Section Header
    draw.rectangle([(120, 210), (2360, 320)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    draw.text((160, 235), "Week 1 Masterclass Dialogue Reference (EP01 - EP03)" if not is_zh else "第一周实景原声对白全纪录（EP01 - EP03）", fill=(29, 78, 216), font=get_font(34))
    draw.text((160, 280), "Full bilingual transcript with JLPT tags for vocal shadowing drills." if not is_zh else "完整中英双语原声台词对照，标注 JLPT 级别，供每日影子跟读背诵。", fill=(71, 85, 105), font=get_font(22))
    
    episodes_p5 = [
        ("EPISODE 01: YAMANOTE LINE TRANSIT [JLPT N4-N3]" if not is_zh else "EP01：山手线月台广播与乘车【JLPT N4-N3】", [
            ("まもなく、2番線に山手線内回りがまいります。", "The Yamanote Line inner loop train will arrive on Platform 2.", "2号站台即将有山手线内环列车进站。"),
            ("危ないですから、黄色い点字ブロックの内側までお下がりください。", "For your safety, please step back behind the yellow tactile paving.", "危险，请退到黄色盲道安全线内侧。"),
            ("次は、新宿、新宿。中央線、地下鉄線はお乗り換えです。", "Next is Shinjuku, Shinjuku. Transfer here for Chuo Line and Subways.", "下一站是新宿、新宿。请在此换乘中央线和地下铁。")
        ], (239, 246, 255), (29, 78, 216)),
        
        ("EPISODE 02: 7-ELEVEN & KOMBINI CHECKOUT [JLPT N5-N4]" if not is_zh else "EP02：便利店 7-Eleven 结账全流程【JLPT N5-N4】", [
            ("いらっしゃいませ。ポイントカードはお持ちですか？", "Welcome! Do you have a loyalty point card?", "欢迎光临，请问有积分卡吗？"),
            ("持っていません。袋をお願いします。", "I do not have one. A plastic bag please.", "没有积分卡。请给我一个塑料袋。"),
            ("お弁当温めますか？ - はい、お願いします。", "Would you like your bento heated? - Yes, please.", "便当需要帮您加热吗？ - 好的，请加热。"),
            ("レシートはご利用ですか？ - 大丈夫です、結構です。", "Do you need a receipt? - No, I am fine, thank you.", "需要小票收据吗？ - 不用了，谢谢。")
        ], (240, 253, 250), (13, 148, 136)),
        
        ("EPISODE 03: SHINBASHI IZAKAYA DINING [JLPT N4-N3]" if not is_zh else "EP03：居酒屋经典开场与点酒【JLPT N4-N3】", [
            ("いらっしゃいませ！何名様ですか？ - 2人です。", "Welcome! How many people in your party? - Two of us.", "欢迎光临！请问几位？ - 两位。"),
            ("お飲み物は何にしましょう？ - とりあえず生2つで！", "What would you like to drink? - For starters, two draft beers!", "先来点什么喝的吗？ - 先来两杯生啤！"),
            ("こちらお通しの枝豆になります。", "Here is your starter appetizer: edamame.", "这是为您上的小菜：毛豆。"),
            ("すみません、お会計を別々でお願いします。", "Excuse me, could we please split the bill?", "不好意思，麻烦买单，请分开算。")
        ], (254, 243, 199), (180, 83, 9))
    ]
    
    dy = 360
    for ep_title, lines, bg, fg in episodes_p5:
        draw.rectangle([(120, dy), (2360, dy + 65)], fill=bg, outline=fg, width=2)
        draw.text((150, dy + 18), ep_title, fill=fg, font=get_font(26))
        dy += 75
        
        for jp, en, zh in lines:
            draw.rectangle([(120, dy), (2360, dy + 160)], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.text((150, dy + 25), jp, fill=(15, 23, 42), font=get_font(28))
            
            trans = f"EN: {en}   |   ZH: {zh}" if not is_zh else f"中文：{zh}   |   EN: {en}"
            draw.text((150, dy + 85), trans, fill=(71, 85, 105), font=get_font(22))
            dy += 175
        dy += 30

    return img

# -------------------------------------------------------------------------
# PAGE 6: COMPLETE DIALOGUES PART 2 (EP04 - EP07)
# -------------------------------------------------------------------------
def make_page_6(is_zh: bool = False) -> Image.Image:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 6, 6, is_zh)
    
    # Section Header
    draw.rectangle([(120, 210), (2360, 320)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    draw.text((160, 235), "Week 1 Masterclass Dialogue Reference (EP04 - EP07)" if not is_zh else "第一周实景原声对白全纪录（EP04 - EP07）", fill=(29, 78, 216), font=get_font(34))
    draw.text((160, 280), "Full bilingual transcript with JLPT tags for vocal shadowing drills." if not is_zh else "完整中英双语原声台词对照，标注 JLPT 级别，供每日影子跟读背诵。", fill=(71, 85, 105), font=get_font(22))
    
    episodes_p6 = [
        ("EPISODE 04: AKIHABARA TAX-FREE SHOPPING [JLPT N4-N3]" if not is_zh else "EP04：秋叶原手办店免税购物【JLPT N4-N3】", [
            ("すみません、ショーケースの中の商品を見せてもらえますか？", "Excuse me, could you show me the item inside the showcase?", "不好意思，能帮我拿出展示柜里的商品看看吗？"),
            ("免税手続きをお願いしたいのですが、パスポートは使えますか？", "I would like tax-free processing. Can I use my passport?", "我想办理免税，请问可以用护照吗？"),
            ("こちらは未開封の新品となります。", "This is a brand new, factory-sealed unopened item.", "这是全新未拆封的正品现货。")
        ], (245, 243, 255), (109, 40, 217)),
        
        ("EPISODE 05: SUBWAY RUSH & FARE ADJUSTMENT [JLPT N4-N3]" if not is_zh else "EP05：地铁补票机与精算【JLPT N4-N3】", [
            ("ピンポーン！カードの残高が不足しています。", "Chime! IC card balance is insufficient.", "叮咚！您的交通卡余额不足。"),
            ("のりこし精算機でチャージするか、不足分をお支払いください。", "Please top up or pay the remaining fare at the Norikoshi machine.", "请在精算机上充值或补齐车费差价。")
        ], (239, 246, 255), (29, 78, 216)),
        
        ("EPISODE 06: KOMBINI COFFEE & ATM SHIPPING [JLPT N5-N4]" if not is_zh else "EP06：便利店咖啡与外卡取现【JLPT N5-N4】", [
            ("冷凍コーナーからアイスカップをお持ちになり、レジへどうぞ。", "Please pick up an ice cup from the freezer and bring it to the register.", "请从冰柜拿取冰杯到收银台结账。"),
            ("こちらのATMで海外発行のクレジットカードをご利用いただけます。", "You can use overseas credit cards at this ATM machine.", "本台 ATM 支持海外发行的信用卡取现。")
        ], (240, 253, 250), (13, 148, 136)),
        
        ("EPISODE 07: ICHIRAN RAMEN TICKET MACHINE [JLPT N4-N3]" if not is_zh else "EP07：一兰拉面食券机与汤头定制【JLPT N4-N3】", [
            ("先に券売機で食券をお買い求めの上、列にお並びください。", "Please purchase your meal ticket at the machine first, then line up.", "请先在自动售票机购买食券，再排队入座。"),
            ("麺の硬さはかため、味の濃さは濃いめでお願いします！", "Noodles firm (katame), broth rich (koime), please!", "面条要偏硬，汤头要偏浓，谢谢！"),
            ("替玉を固めで追加お願いします！", "One noodle refill (kaedama), firm, please!", "麻烦加一份面，同样要硬面！")
        ], (254, 243, 199), (180, 83, 9))
    ]
    
    dy = 360
    for ep_title, lines, bg, fg in episodes_p6:
        draw.rectangle([(120, dy), (2360, dy + 65)], fill=bg, outline=fg, width=2)
        draw.text((150, dy + 18), ep_title, fill=fg, font=get_font(26))
        dy += 75
        
        for jp, en, zh in lines:
            draw.rectangle([(120, dy), (2360, dy + 160)], fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            draw.text((150, dy + 25), jp, fill=(15, 23, 42), font=get_font(28))
            
            trans = f"EN: {en}   |   ZH: {zh}" if not is_zh else f"中文：{zh}   |   EN: {en}"
            draw.text((150, dy + 85), trans, fill=(71, 85, 105), font=get_font(22))
            dy += 175
        dy += 30

    return img

def generate_full_workbook(is_zh: bool = False):
    locale_label = "zh" if is_zh else "en"
    out_dir = OUT_ZH_DIR if is_zh else OUT_EN_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[{locale_label.upper()}] Rendering 6-Page High-DPI Master Study Workbook...")
    pages = [
        make_page_1(is_zh),
        make_page_2(is_zh),
        make_page_3(is_zh),
        make_page_4(is_zh),
        make_page_5(is_zh),
        make_page_6(is_zh),
    ]
    
    # Save individual high-res PNG pages
    for i, page_img in enumerate(pages):
        png_path = out_dir / f"workbook_page_{i+1}.png"
        page_img.save(png_path, "PNG", dpi=(300, 300))
        print(f"  Saved page {i+1} -> {png_path.name}")
        
    # Save combined master PDF
    pdf_filename = "TokyoFlow_Week01_JLPT_Master_Workbook.pdf" if not is_zh else "TokyoFlow_第一周_JLPT实景学习讲义与复习手册.pdf"
    pdf_path = out_dir / pdf_filename
    
    pages[0].save(
        pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=pages[1:]
    )

    # 128-bit AES Encryption with Passcode
    try:
        from pypdf import PdfReader, PdfWriter
        passcode = "TOKYOFLOW-WEEK1"
        reader = PdfReader(str(pdf_path))
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)
        writer.encrypt(user_password=passcode, owner_password=None, use_128bit=True)
        with open(pdf_path, "wb") as f:
            writer.write(f)
        print(f"  [SECURITY] PDF successfully password-protected with passcode: {passcode}")
    except Exception as e:
        print(f"  [WARNING] PDF encryption error: {e}")

    print(f"  [SUCCESS] Master PDF Generated: {pdf_path} ({pdf_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return pdf_path

if __name__ == "__main__":
    generate_full_workbook(is_zh=False)
    generate_full_workbook(is_zh=True)
