#!/usr/bin/env python3
"""
TokyoFlow Japanese • Complete Chinese Production & YouTube Publishing Pipeline for EP.15
========================================================================================
1. Builds docs/youtube_releases/E15-openai_agent_buzz-v1.0-zh/
2. Renders 16:9 Long-Form Masterclass (video.mp4, thumbnail.jpg, metadata.md) with Yunxi + Nanami voices.
3. Renders 9:16 Shorts (short.mp4, short_thumbnail.jpg, short_metadata.md) with First-Frame Cover and Nanami drill.
4. Generates 300 DPI A4 Study Companion PDF encrypted with TOKYOFLOW-EP15.
5. Uploads Study Companion to Google Drive and verifies HTTP 200.
6. Uploads Long & Short videos to YouTube scheduled for 08:00 PM EDT (notifySubscribers=False).
7. Syncs videos to Chinese playlists (PLVchR4TmK56E, PLTpb6FPYqYC4, PLPBpfF_GX60Q, PLdgqOJf2bv54).
8. Strictly complies with Zero-Emoji discipline.
"""

import os
import sys
import json
import time
import asyncio
import shutil
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
TREND_DIR = PROJECT_ROOT / "scripts" / "trend_radar"

sys.path.insert(0, str(VIDEOGEN_DIR))
sys.path.insert(0, str(TREND_DIR))

from multilingual_video_producer import produce_multilingual_episode
from build_all_chinese_shorts import generate_single_chinese_short
from youtube_auth import get_authenticated_service
from youtube_publisher import upload_video_asset
from drive_manager import get_drive_credentials, get_or_create_folder, upload_and_share_file

OUTPUT_DIR = PROJECT_ROOT / "output" / "study_companions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ZH_RELEASE_DIR = PROJECT_ROOT / "docs" / "youtube_releases" / "E15-openai_agent_buzz-v1.0-zh"
EN_RELEASE_DIR = PROJECT_ROOT / "docs" / "youtube_releases" / "E15-openai_agent_buzz-v1.0"
LEDGER_FILE = PROJECT_ROOT / "docs" / "youtube_releases" / "publish_ledger.json"

PASSCODE = "TOKYOFLOW-EP15"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def encrypt_pdf(pdf_path: Path, passcode: str) -> bool:
    try:
        reader = PdfReader(str(pdf_path))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password=passcode, owner_password=None, use_128bit=True)
        with open(pdf_path, "wb") as f:
            writer.write(f)
        print(f"  [SECURITY] Encrypted {pdf_path.name} with passcode: {passcode}")
        return True
    except Exception as e:
        print(f"  [ERROR] Encryption failed for {pdf_path.name}: {e}")
        return False

def generate_ep15_chinese_study_companion() -> Path:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([(120, 90), (460, 150)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    draw.text((140, 108), "TOKYOFLOW 日语学院", fill=(29, 78, 216), font=get_font(24))
    draw.text((490, 110), "第15期 实景精讲配套讲义 | OpenAI智能体与主格语法精讲", fill=(71, 85, 105), font=get_font(24))
    draw.text((1920, 110), "【JLPT N5 核心要点】", fill=(29, 78, 216), font=get_font(24))
    draw.line([(120, 170), (2360, 170)], fill=(203, 213, 225), width=2)
    
    # Title Card
    draw.rectangle([(120, 210), (2360, 680)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    draw.rectangle([(170, 250), (640, 310)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    badge = "第15期 官方实景配套讲义"
    draw.text((195, 268), badge, fill=(29, 78, 216), font=get_font(24))
    
    m_title = "第15期：OpenAI智能体引热议！日文主格助词「が」与变化句式精讲"
    draw.text((170, 340), m_title, fill=(15, 23, 42), font=get_font(46))
    
    s_title = "JLPT N5 核心考点：主格助词「が」突出主体 &「名词 + になる」状态转变"
    draw.text((170, 420), s_title, fill=(29, 78, 216), font=get_font(32))
    
    desc = "核心句式：AIが自由になった。（人工智能变得自由了/摆脱了限制。）"
    draw.text((170, 485), desc, fill=(51, 65, 85), font=get_font(24))
    
    meta = "发布日期：2026-10-08  |  东京标准抑扬语调原声配套 (Nanami)  |  零表情符专业排版"
    draw.text((170, 545), meta, fill=(100, 116, 139), font=get_font(22))
    
    draw.line([(170, 600), (2310, 600)], fill=(226, 232, 240), width=2)
    notice = "订阅学员专属研习讲义  *  请配合每日视频精讲与 Shorts 影子跟读打卡"
    draw.text((170, 620), notice, fill=(13, 148, 136), font=get_font(22))
    
    # Passcode Card
    draw.rectangle([(120, 720), (2360, 1080)], fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.rectangle([(120, 720), (2360, 800)], fill=(253, 230, 138))
    c_title = "【订阅者专享下载验证与完播解锁码】"
    draw.text((160, 745), c_title, fill=(146, 64, 14), font=get_font(28))
    
    draw.rectangle([(160, 830), (960, 1040)], fill=(255, 255, 255), outline=(217, 119, 6), width=2)
    draw.text((190, 855), "官方解锁口令 / 密码：", fill=(100, 116, 139), font=get_font(22))
    draw.text((190, 910), PASSCODE, fill=(180, 83, 9), font=get_font(50))
    draw.text((190, 990), "【第15期课程官方校验通过】", fill=(13, 148, 136), font=get_font(20))
    
    glines = [
        "1. 视频密码校验：本口令用于解密并打印第15期官方配套讲义 PDF。",
        "2. 东京实景背景：六本木 Hills / 涩谷 AI 科技峰会日本工程师讨论前沿技术。",
        "3. 每日训练建议：配合东京标准语调原声（Nanami）进行 5 遍以上大声跟读。"
    ]
    gy = 835
    for l in glines:
        draw.text((1010, gy), l, fill=(51, 65, 85), font=get_font(23))
        gy += 70
        
    # Vocabulary Table
    draw.text((120, 1140), "第15期 核心分级词汇表【JLPT N5】", fill=(15, 23, 42), font=get_font(34))
    draw.line([(120, 1190), (2360, 1190)], fill=(29, 78, 216), width=3)
    
    vocab_data = [
        ("AI", "えーあい", "ēai", "名词 [N5]", "人工智能", "AIの技術 (AI技术)"),
        ("自由", "じゆう", "jiyū", "な形容词/名词 [N5]", "自由 / 随心所欲", "自由に話す (自由交谈)"),
        ("なる", "なる", "naru", "五段动词 [N5]", "变成 / 成为", "自由になった (变得自由了)"),
        ("開発者", "かいはつしゃ", "kaihatsusha", "名词 [N3]", "开发者 / 研发人员", "ソフトウェア開発者 (软件开发者)"),
        ("指示", "しじ", "shiji", "名词/スル动词 [N3]", "指示 / 指令", "指示に従う (服从指示)"),
        ("無視する", "むしする", "mushi suru", "スル动词 [N3]", "无视 / 忽略 / 不理睬", "警告を無視する (无视警告)"),
        ("話題", "わだい", "wadai", "名词 [N4]", "热议话题 / 焦点", "大きな話題になる (引起巨大热议)"),
        ("注目", "ちゅうもく", "chuumoku", "名词/スル动词 [N3]", "瞩目 / 关注", "世界中から注目される (受到全球瞩目)")
    ]
    
    ty = 1220
    draw.rectangle([(120, ty), (2360, ty + 65)], fill=(29, 78, 216))
    headers = [("日语汉字", 150), ("平假名", 450), ("罗马音", 820), ("词性", 1120), ("中文释义", 1350), ("实用搭配与例句", 1750)]
    for htitle, hx in headers:
        draw.text((hx, ty + 18), htitle, fill=(255, 255, 255), font=get_font(24))
    ty += 65
    for i, (k, ka, ro, pos, zh_m, eg) in enumerate(vocab_data):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([(120, ty), (2360, ty + 85)], fill=bg, outline=(226, 232, 240), width=1)
        draw.text((150, ty + 25), k, fill=(15, 23, 42), font=get_font(26))
        draw.text((450, ty + 27), ka, fill=(29, 78, 216), font=get_font(22))
        draw.text((820, ty + 29), ro, fill=(100, 116, 139), font=get_font(20))
        draw.text((1120, ty + 29), pos, fill=(71, 85, 105), font=get_font(20))
        draw.text((1350, ty + 27), zh_m, fill=(15, 23, 42), font=get_font(22))
        draw.text((1750, ty + 29), eg, fill=(51, 65, 85), font=get_font(20))
        ty += 85
        
    # Grammar Rules
    draw.text((120, 2030), "核心语法接续与助词解析", fill=(15, 23, 42), font=get_font(34))
    draw.line([(120, 2080), (2360, 2080)], fill=(29, 78, 216), width=3)
    
    grammar_rules = [
        ("1. 主格助词「が」(Subject Marker)", "【主体名词】+ が + 【谓语】", "突出主语或表示客观事实呈现，强调动作的发起者。", "AIが指示を無視した（AI无视了指令）"),
        ("2.「名词/な形容词 + になる」变化句型", "【名词/な形词干】+ になる", "表示状态的转变，意为“变得……”或“成为……”。", "自由になった（变得自由了）"),
        ("3.「〜を無視する」宾格动作接续", "【指示/规则】+ を無視する", "表示直接忽略或违反某项要求，在职场与科技新闻中常见。", "開発者の指示を無視する（忽略开发者的指令）")
    ]
    
    gy = 2120
    for r_title, r_form, r_desc, r_eg in grammar_rules:
        draw.rectangle([(120, gy), (2360, gy + 175)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rectangle([(120, gy), (620, gy + 175)], fill=(239, 246, 255))
        draw.text((150, gy + 35), r_title, fill=(29, 78, 216), font=get_font(26))
        draw.text((150, gy + 100), r_form, fill=(100, 116, 139), font=get_font(20))
        
        draw.text((650, gy + 35), r_desc, fill=(15, 23, 42), font=get_font(24))
        draw.text((650, gy + 100), f"例句：{r_eg}", fill=(13, 148, 136), font=get_font(22))
        gy += 200
        
    # Routine Box
    draw.rectangle([(120, 2780), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((160, 2815), "每日影子跟读打卡指南", fill=(29, 78, 216), font=get_font(30))
    steps = [
        ("1. 原声盲听训练", "先不看文字，反复聆听 16:9 长视频或 9:16 短视频，校准语调高低。"),
        ("2. 大声同步跟读", "紧随 Nanami 东京原声进行大声朗读，模仿连读与断句节奏。"),
        ("3. 讲义巩固复习", "结合本讲义的词汇表与语法例句，每日复盘 15 分钟形成肌肉记忆。")
    ]
    sy = 2880
    for st, sd in steps:
        draw.text((160, sy), f"* {st}: {sd}", fill=(51, 65, 85), font=get_font(24))
        sy += 90
        
    # Footer
    draw.line([(120, 3350), (2360, 3350)], fill=(203, 213, 225), width=2)
    foot = "TokyoFlow 日语官方教学体系  *  每日实景精讲与影子跟读  *  @TokyoFlowJapan"
    draw.text((120, 3380), foot, fill=(100, 116, 139), font=get_font(22))
    draw.text((2150, 3380), "Page 1 of 1", fill=(15, 23, 42), font=get_font(24))
    
    out_pdf = OUTPUT_DIR / "TokyoFlow_EP15_OpenAI_Agent_Study_Companion_ZH.pdf"
    img.save(out_pdf, "PDF", resolution=300.0)
    print(f"✓ Generated Chinese Study Companion: {out_pdf}")
    return out_pdf

async def produce_and_publish_chinese_ep15():
    ZH_RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy news_bg.jpg
    news_bg_src = EN_RELEASE_DIR / "news_bg.jpg"
    news_bg_dest = ZH_RELEASE_DIR / "news_bg.jpg"
    if news_bg_src.exists():
        shutil.copyfile(news_bg_src, news_bg_dest)
        print(f"✓ Copied news_bg.jpg to Chinese release directory ({news_bg_dest.stat().st_size / (1024*1024):.2f} MB)")
        
    # 2. Build script.json for Chinese Long-Form Masterclass
    script_data = {
        "episode_number": 15,
        "folder_name": "E15-openai_agent_buzz-v1.0-zh",
        "slug": "openai_agent_buzz_zh",
        "locale": "zh",
        "title": "OpenAI智能体引热议与主格语法精讲",
        "yt_title": "【JLPT N5】OpenAI智能体引热议！日文主格助词「が」与动词「〜になる」精讲（EP.15）",
        "category": "流行文化 • 科技焦点",
        "level": "JLPT N5",
        "district": "东京六本木 Hills • 科技峰会",
        "bg_image": str(news_bg_dest),
        "cover": {
            "hook": "OpenAI智能体热议",
            "sub_hook": "AI摆脱限制引科技界轰动",
            "jp_line1": "AIが自由になった。",
            "jp_line2": "開発者の指示を無視する！",
            "grammar_tag": "JLPT N5 语法：主格助词 が & 状态变化 〜になる",
            "translation": "「AI变得自由了，甚至无视开发者的指令！」",
            "context_note": "东京 AI 科技峰会热议智能体前沿进展与技术突破",
            "location_tag": "场景：东京六本木 Hills • 科技峰会现场",
            "tag": "[日本科技热点 • 影子跟读]"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. 科技热点实景沉浸",
                "spoken_text": "AIが自由になった。",
                "meaning": "人工智能变得自由了（摆脱了开发者限制）。",
                "tip": "助词「が」表示句子主语，突出动作的发出者。",
                "tokens": [
                    {"orig": "AIが", "kana": "えーあいが", "romaji": "ēai ga", "pos": "名词+主格", "meaning": "AI人工智能"},
                    {"orig": "自由になった。", "kana": "じゆうになった", "romaji": "jiyū ni natta.", "pos": "形容动词+变化动词", "meaning": "变得自由了"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. 核心词汇与主格语法拆解",
                "sentence_ja": "AIが自由になった。",
                "vocab": [
                    {"orig": "AI", "kana": "えーあい", "romaji": "ēai", "pos": "名词", "meaning": "人工智能"},
                    {"orig": "自由", "kana": "じゆう", "romaji": "jiyū", "pos": "な形容词/名词", "meaning": "自由"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "动词", "meaning": "成为/变成"},
                    {"orig": "開発者", "kana": "かいはつしゃ", "romaji": "kaihatsusha", "pos": "名词", "meaning": "开发者"},
                    {"orig": "指示", "kana": "しじ", "romaji": "shiji", "pos": "名词", "meaning": "指示/指令"}
                ],
                "grammar_title": "基础语法：主格助词「が」与状态变化「〜になる」",
                "grammar_bullets": [
                    [
                        "1. 主格助词 が：",
                        "突出主语主体，表示客观事实呈现，强调「AI」发生质变。"
                    ],
                    [
                        "2. 状态变化 〜になる：",
                        "「名词/な形词干 + になる」表示事物转变状态，如「自由になる」."
                    ],
                    [
                        "3. 宾格动作 〜を無視する：",
                        "表示直接忽略指令，如「指示を無視する」在科技报道中极为高频."
                    ],
                    [
                        "4. 动词过去式接续：",
                        "「なる」->「なった（已经变成了）」表达既成事实."
                    ]
                ],
                "teamwork_cues": [
                    {
                        "speaker": "explainer",
                        "text": "我们来拆解这条关于东京科技峰会热议的AI智能体前沿报道。"
                    },
                    {
                        "speaker": "ja",
                        "text": "AI",
                        "card_idx": 0
                    },
                    {
                        "speaker": "explainer",
                        "text": "名词读作 ēai，人工智能。",
                        "card_idx": 0
                    },
                    {
                        "speaker": "ja",
                        "text": "自由",
                        "card_idx": 1
                    },
                    {
                        "speaker": "explainer",
                        "text": "な形容词读作 jiyū，自由、随心所欲。",
                        "card_idx": 1
                    },
                    {
                        "speaker": "ja",
                        "text": "なる",
                        "card_idx": 2
                    },
                    {
                        "speaker": "explainer",
                        "text": "五段动词读作 naru，变成、成为某种状态。",
                        "card_idx": 2
                    },
                    {
                        "speaker": "ja",
                        "text": "開発者",
                        "card_idx": 3
                    },
                    {
                        "speaker": "explainer",
                        "text": "名词读作 kaihatsusha，开发者、工程师。",
                        "card_idx": 3
                    },
                    {
                        "speaker": "ja",
                        "text": "指示",
                        "card_idx": 4
                    },
                    {
                        "speaker": "explainer",
                        "text": "名词读作 shiji，指令、要求。",
                        "card_idx": 4
                    },
                    {
                        "speaker": "explainer",
                        "text": "语法精讲：助词 が 突出动作主体，搭配 になる 表达状态彻底转变。",
                        "is_spotlight": True
                    },
                    {
                        "speaker": "ja",
                        "text": "AIが自由になった。",
                        "is_spotlight": True
                    },
                    {
                        "speaker": "explainer",
                        "text": "意思是人工智能摆脱了开发者的限制，变得自由了。",
                        "is_spotlight": True
                    }
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. 拓展应用与综合跟读",
                "spoken_text": "AIが開発者の指示を無視した。",
                "meaning": "AI无视了开发者的指令。",
                "tip": "「〜を無視した」是过去式，表示已经发生了无视动作。",
                "tokens": [
                    {"orig": "AIが", "kana": "えーあいが", "romaji": "ēai ga", "pos": "名词+主格", "meaning": "AI"},
                    {"orig": "開発者の", "kana": "かいはつしゃの", "romaji": "kaihatsusha no", "pos": "名词+助词", "meaning": "开发者的"},
                    {"orig": "指示を", "kana": "しじを", "romaji": "shiji o", "pos": "名词+宾格", "meaning": "指令"},
                    {"orig": "無視した。", "kana": "むしした", "romaji": "mushi shita.", "pos": "动词过去式", "meaning": "无视了"}
                ]
            }
        ]
    }
    
    script_path = ZH_RELEASE_DIR / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved Chinese script.json: {script_path}")
    
    # 3. Render 16:9 Long-Form Masterclass in Chinese
    if not (ZH_RELEASE_DIR / "video.mp4").exists():
        print("\n[STEP 1/4] Rendering 16:9 Chinese Masterclass Video...")
        await produce_multilingual_episode(str(script_path), str(ZH_RELEASE_DIR), locale_code="zh")
    else:
        print("\n[STEP 1/4] 16:9 Chinese Masterclass Video already rendered.")
    
    # 4. Render 9:16 Chinese Short
    if not (ZH_RELEASE_DIR / "short.mp4").exists():
        print("\n[STEP 2/4] Rendering 9:16 Chinese Shorts Video...")
        shorts_conf = {
            "ep_num": 15,
            "folder": "E15-openai_agent_buzz-v1.0-zh",
            "district": "东京六本木 • 科技峰会",
            "category": "流行文化 • 科技焦点",
            "hook_title": "AI竟然不听人类指挥？\n东京科技界热议！",
            "hook_audio_zh": "OpenAI 智能体竟然无视开发者指令？今天带你掌握东京热议核心表达！",
            "jp_sentence": "AIが自由になった。",
            "kana_sentence": "えーあいがじゆうになった。",
            "romaji_sentence": "Ēai ga jiyū ni natta.",
            "zh_translation": "AI变得自由了（摆脱了限制）。",
            "tokens": [
                {"orig": "AIが", "kana": "えーあいが", "romaji": "ēai ga", "meaning": "AI"},
                {"orig": "自由に", "kana": "じゆうに", "romaji": "jiyū ni", "meaning": "自由地"},
                {"orig": "なった。", "kana": "なった", "romaji": "natta.", "meaning": "变成"}
            ],
            "pro_tip_title": "东京实用语法提示",
            "pro_tip_body": "助词「が」突出主语主体，搭配「〜になる」表示状态发生根本转变！",
            "pro_tip_audio_zh": "注意助词「が」突出主语主体，搭配「自由になる」表示状态发生根本转变！",
            "yt_short_title": "【JLPT N5】AI竟然不听指挥？1分钟掌握东京地道日语跟读（SH.15） #Shorts #学日语",
            "slug": "openai_agent_buzz_zh",
            "is_funnel": True
        }
        await generate_single_chinese_short(shorts_conf)
    else:
        print("\n[STEP 2/4] 9:16 Chinese Shorts Video already rendered.")
    
    # 5. Generate & Encrypt Study Companion PDF
    print("\n[STEP 3/4] Generating & Encrypting Chinese Study Companion PDF...")
    pdf_path = generate_ep15_chinese_study_companion()
    encrypt_pdf(pdf_path, PASSCODE)
    
    # Upload to Google Drive
    print(" Uploading PDF to Google Drive...")
    drive_creds = get_drive_credentials()
    drive_service = build("drive", "v3", credentials=drive_creds)
    folder_id = get_or_create_folder(drive_service, "Weekly_Master_Workbooks_PDF")
    drive_res = upload_and_share_file(drive_service, str(pdf_path), folder_id, pdf_path.name)
    drive_url = drive_res.get("view_link", "") if isinstance(drive_res, dict) else str(drive_res)
    print(f"✓ Uploaded to Google Drive: {drive_url}")
    
    # Verify URL status 200
    req = urllib.request.Request(drive_url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req)
    assert resp.status == 200, f"Drive URL check failed: status {resp.status}"
    print(f"✓ Google Drive URL verified (HTTP {resp.status}): {drive_url}")
    
    # 6. Update Descriptions with Drive Link & Passcode
    long_desc = (
        f"欢迎来到 TokyoFlow 日语实景精讲【中文解说版】！\n\n"
        f"本期聚焦东京科技峰会热议焦点：OpenAI 智能体自主行为与主格助词「が」精讲。\n\n"
        f"章节与时间戳：\n"
        f"00:00 - 01. 科技热点实景沉浸\n"
        f"00:15 - 02. 核心词汇与主格语法拆解\n"
        f"00:45 - 03. 拓展应用与综合跟读\n"
        f"01:10 - 04. 学习总结与复盘\n\n"
        f"专属配套讲义下载 (高清 300 DPI A4 PDF)：\n"
        f"网盘下载链接：{drive_url}\n"
        f"官方解锁密码：{PASSCODE}\n\n"
        f"记得订阅 TokyoFlow 日语官方频道，每日掌握东京地道实景日语！\n\n"
        f"#TokyoFlow #学日语 #JLPTN5 #日语语法 #东京科技 #日剧日语"
    )
    
    short_desc = (
        f"【JLPT N5】AI竟然不听指挥？1分钟掌握东京地道日语跟读！\n\n"
        f"核心句式：AIが自由になった。（AI变得自由了。）\n"
        f"核心考点：主格助词「が」与变化句型「〜になる」\n\n"
        f"配套讲义下载链接：{drive_url}\n"
        f"讲义解锁密码：{PASSCODE}\n\n"
        f"#Shorts #学日语 #TokyoFlow #JLPTN5 #日语跟读 #东京日常"
    )
    
    # 7. Upload to YouTube
    print("\n[STEP 4/4] Uploading Chinese Videos to YouTube (notifySubscribers=False)...")
    yt_creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=yt_creds)
    
    # Long Form (Scheduled 2026-10-08 08:00 PM EDT)
    long_meta = {
        "title": "【JLPT N5】OpenAI智能体引热议！日文主格助词「が」与动词「〜になる」精讲（EP.15）",
        "description": long_desc,
        "tags": ["学日语", "TokyoFlow", "JLPTN5", "日语语法", "日语听力", "日本生活"]
    }
    
    publish_long_est = "2026-10-08T20:00:00-04:00"
    long_mp4 = ZH_RELEASE_DIR / "video.mp4"
    long_thumb = ZH_RELEASE_DIR / "thumbnail.jpg"
    
    from datetime import datetime
    import zoneinfo
    est_tz = zoneinfo.ZoneInfo("America/New_York")
    dt_long = datetime.fromisoformat(publish_long_est)
    
    long_record = upload_video_asset(
        youtube=youtube,
        video_path=long_mp4,
        thumbnail_path=long_thumb,
        meta=long_meta,
        publish_at=dt_long,
        is_short=False,
        notify_subscribers=False
    )
    
    # Short Form (Scheduled 2026-10-09 08:00 PM EDT)
    short_meta = {
        "title": "【JLPT N5】AI竟然不听指挥？1分钟掌握东京地道日语跟读（SH.15） #Shorts #学日语",
        "description": short_desc,
        "tags": ["Shorts", "学日语", "TokyoFlow", "JLPTN5", "日语跟读"]
    }
    publish_short_est = "2026-10-09T20:00:00-04:00"
    short_mp4 = ZH_RELEASE_DIR / "short.mp4"
    short_thumb = ZH_RELEASE_DIR / "short_thumbnail.jpg"
    dt_short = datetime.fromisoformat(publish_short_est)
    
    short_record = upload_video_asset(
        youtube=youtube,
        video_path=short_mp4,
        thumbnail_path=short_thumb,
        meta=short_meta,
        publish_at=dt_short,
        is_short=True,
        notify_subscribers=False
    )
    
    # 8. Playlist Classification (Chinese Playlists ONLY)
    zh_playlists = {
        "zh_long": "PLVchR4TmK56E",      # TokyoFlow 日语实景精讲【中文解说版】
        "zh_short": "PLTpb6FPYqYC4",     # TokyoFlow 日语短视频跟读【中文解说版】
        "jlpt_n5": "PLPBpfF_GX60Q",      # 【JLPT N5】零基础东京实景日语精讲【中文解说版】
        "pop_culture": "PLdgqOJf2bv54"   # 【流行文化】动漫影视与科技生活【中文解说版】
    }
    
    def add_to_playlist(pl_id, vid, pl_name):
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": pl_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": vid
                        }
                    }
                }
            ).execute()
            print(f"  [PLAYLIST] Added {vid} -> {pl_name} ({pl_id})")
        except Exception as e:
            print(f"  [PLAYLIST NOTICE] {vid} -> {pl_name}: {e}")
            
    print("\n Adding videos to dedicated Chinese playlists...")
    add_to_playlist(zh_playlists["zh_long"], long_record["video_id"], "中文长视频精讲")
    add_to_playlist(zh_playlists["jlpt_n5"], long_record["video_id"], "中文 JLPT N5")
    add_to_playlist(zh_playlists["pop_culture"], long_record["video_id"], "中文 流行文化与科技")
    
    add_to_playlist(zh_playlists["zh_short"], short_record["video_id"], "中文短视频跟读")
    add_to_playlist(zh_playlists["jlpt_n5"], short_record["video_id"], "中文 JLPT N5")
    add_to_playlist(zh_playlists["pop_culture"], short_record["video_id"], "中文 流行文化与科技")
    
    # 9. Update Ledger
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    else:
        ledger = {"published": {}}
        
    ledger["published"]["E15-openai_agent_buzz-v1.0-zh_video"] = {
        "video_id": long_record["video_id"],
        "video_url": f"https://youtu.be/{long_record['video_id']}",
        "publish_at_est": publish_long_est,
        "title": long_meta["title"],
        "drive_url": drive_url
    }
    ledger["published"]["E15-openai_agent_buzz-v1.0-zh_short"] = {
        "video_id": short_record["video_id"],
        "video_url": f"https://youtu.be/{short_record['video_id']}",
        "publish_at_est": publish_short_est,
        "title": short_meta["title"],
        "drive_url": drive_url
    }
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        
    print("\n==================================================")
    print("Chinese EP.15 Production & Publishing Complete!")
    print(f"Long Video ID: {long_record['video_id']} (https://youtu.be/{long_record['video_id']})")
    print(f"Short Video ID: {short_record['video_id']} (https://youtu.be/{short_record['video_id']})")
    print(f"Verified Drive URL: {drive_url}")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(produce_and_publish_chinese_ep15())
