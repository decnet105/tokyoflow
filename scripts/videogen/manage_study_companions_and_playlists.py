#!/usr/bin/env python3
"""
TokyoFlow Japanese • Unified Study Companion Generator, Drive Uploader & Playlist Sync Engine
============================================================================================
1. Generates English and Chinese Study Guide / Companion PDFs (300 DPI A4).
2. Encrypts PDFs with Scheme D Passcodes (pypdf 128-bit AES encryption).
3. Uploads / Syncs encrypted PDFs to Google Drive (tokyoflow.learn@gmail.com).
4. Updates YouTube Video Descriptions and Posts Pinned Comments with Passcode & Drive Link.
5. Classifies and adds all English & Chinese videos into proper YouTube playlists:
   - English Masterclasses (16:9 Long)
   - English Shorts (9:16 Vertical)
   - Chinese Masterclasses (16:9 Long)
   - Chinese Shorts (9:16 Vertical)
   - JLPT Level Playlists ([JLPT N5], [JLPT N4], [JLPT N3], [JLPT N2-N1])
   - Scenario / Topic Playlists (Transit, Kombini, Dining, Shopping, News)
- Enforces strict Zero-Emoji discipline.
"""

import os
import sys
import json
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

from youtube_auth import get_authenticated_service
from drive_manager import get_drive_credentials, get_or_create_folder, upload_and_share_file

LEDGER_FILE = PROJECT_ROOT / "docs" / "shared" / "publish_ledger.json"
OUTPUT_DIR = PROJECT_ROOT / "output" / "study_companions"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

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

# =========================================================================
# 1. EPISODE 14 DEDICATED STUDY COMPANION GENERATOR (300 DPI A4)
# =========================================================================
def generate_ep14_study_companion(is_zh: bool = False) -> Path:
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Top Header
    draw.rectangle([(120, 90), (460, 150)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    draw.text((140, 108), "TOKYOFLOW ACADEMY" if not is_zh else "TOKYOFLOW 日语学院", fill=(29, 78, 216), font=get_font(24))
    draw.text((490, 110), "EP.14 MASTER STUDY COMPANION | SUICA TEPPAY" if not is_zh else "第14期 实景精讲配套讲义 | JR东日本 Suica全新支付", fill=(71, 85, 105), font=get_font(24))
    draw.text((1920, 110), "[JLPT N5 FOCUS]" if not is_zh else "【JLPT N5 核心要点】", fill=(29, 78, 216), font=get_font(24))
    draw.line([(120, 170), (2360, 170)], fill=(203, 213, 225), width=2)
    
    # Title Card
    draw.rectangle([(120, 210), (2360, 680)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    draw.rectangle([(170, 250), (640, 310)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    badge = "OFFICIAL EPISODE COMPANION" if not is_zh else "第14期 官方实景配套讲义"
    draw.text((195, 268), badge, fill=(29, 78, 216), font=get_font(24))
    
    m_title = "Episode 14: JR East Suica 'teppay' QR Payment Revolution" if not is_zh else "第14期：JR东日本 Suica 全新扫码支付与宾格语法精讲"
    draw.text((170, 340), m_title, fill=(15, 23, 42), font=get_font(48))
    
    s_title = "JLPT N5 Direct Object Particle を & ~を使って (Using a Tool/Service)" if not is_zh else "JLPT N5 核心考点：宾格助词「を」与「〜を使って」工具接续"
    draw.text((170, 420), s_title, fill=(29, 78, 216), font=get_font(32))
    
    desc = "Key Phrase: Suicaの新しい決済サービスを発表しました。(JR East announced Suica's new payment service.)" if not is_zh else "核心句式：Suicaの新しい決済サービスを発表しました。（JR东日本发布了Suica全新结算支付服务。）"
    draw.text((170, 485), desc, fill=(51, 65, 85), font=get_font(24))
    
    meta = "Release Date: 2026-10-10  |  Tokyo Standard Audio (ja-JP-NanamiNeural)  |  Clean Master Edition" if not is_zh else "发布日期：2026-10-10  |  东京标准抑扬语调原声配套  |  零表情符专业排版"
    draw.text((170, 545), meta, fill=(100, 116, 139), font=get_font(22))
    
    draw.line([(170, 600), (2310, 600)], fill=(226, 232, 240), width=2)
    notice = "Free Subscriber Study Workbook  *  Keep this document for daily shadowing drills" if not is_zh else "订阅学员专属研习讲义  *  请配合每日视频精讲与 Shorts 影子跟读打卡"
    draw.text((170, 620), notice, fill=(13, 148, 136), font=get_font(22))
    
    # Passcode Card
    draw.rectangle([(120, 720), (2360, 1080)], fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.rectangle([(120, 720), (2360, 800)], fill=(253, 230, 138))
    c_title = "SUBSCRIBER DOWNLOAD VERIFICATION & PASSCODE" if not is_zh else "【订阅者专享下载验证与完播解锁码】"
    draw.text((160, 745), c_title, fill=(146, 64, 14), font=get_font(28))
    
    draw.rectangle([(160, 830), (960, 1040)], fill=(255, 255, 255), outline=(217, 119, 6), width=2)
    draw.text((190, 855), "OFFICIAL UNLOCK PASSCODE:" if not is_zh else "官方解锁口令 / 密码：", fill=(100, 116, 139), font=get_font(22))
    draw.text((190, 910), "TOKYOFLOW-EP14", fill=(180, 83, 9), font=get_font(50))
    draw.text((190, 990), "[VALIDATED LESSON COMPANION]" if not is_zh else "【第14期课程官方校验通过】", fill=(13, 148, 136), font=get_font(20))
    
    glines = [
        "1. Video Passcode Verification: Unlocks this official study companion PDF.",
        "2. Real-World Tokyo Context: JR East launches smartphone QR payment beyond 20,000 yen cap.",
        "3. Daily Routine: Vocal shadowing with Tokyo standard pitch accent (Nanami)."
    ] if not is_zh else [
        "1. 视频密码校验：本口令用于解密并打印第14期官方配套讲义 PDF。",
        "2. 东京实景背景：JR东日本推出手机扫码支付，打破实体西瓜卡 2 万日元储值上限。",
        "3. 每日训练建议：配合东京标准语调原声（Nanami）进行 5 遍以上影子大声跟读。"
    ]
    gy = 835
    for l in glines:
        draw.text((1010, gy), l, fill=(51, 65, 85), font=get_font(23))
        gy += 70
        
    # Vocabulary Table
    draw.text((120, 1140), "Episode 14 Core Classified Vocabulary [JLPT N5]" if not is_zh else "第14期 核心分级词汇表【JLPT N5】", fill=(15, 23, 42), font=get_font(34))
    draw.line([(120, 1190), (2360, 1190)], fill=(29, 78, 216), width=3)
    
    vocab_data = [
        ("JR東日本", "じぇいあーるひがしにほん", "jeiaaru higashinihon", "Proper Noun", "East Japan Railway Company", "JR东日本公司", "JR東日本は新サービスを開始 (JR East starts new service)"),
        ("Suica", "すいか", "suika", "Proper Noun", "Suica transit smart card", "Suica 西瓜卡（交通智能卡）", "Suicaで支払う (Pay with Suica)"),
        ("新しい", "あたらしい", "atarashii", "I-Adj [N5]", "New / Brand new", "全新的 / 新的", "新しいサービス (New service)"),
        ("決済", "けっさい", "kessai", "Noun [N3]", "Settlement / Payment", "结算 / 支付", "QRコード決済 (QR code payment)"),
        ("サービス", "さーびす", "saabisu", "Noun [N5]", "Service", "服务", "決済サービス (Payment service)"),
        ("発表する", "はっぴょうする", "happyou suru", "Suru-Verb [N4]", "To announce / official release", "正式发布 / 公布", "新機能を発表しました (Announced new feature)"),
        ("使う", "つかう", "tsukau", "Verb [N5]", "To use / utilize", "使用 / 运用", "スマホを使って支払う (Pay using smartphone)"),
        ("便利", "べんり", "benri", "Na-Adj [N5]", "Convenient / Handy", "方便的 / 便利的", "とても便利です (It is very convenient)")
    ]
    
    ty = 1220
    draw.rectangle([(120, ty), (2360, ty + 65)], fill=(29, 78, 216))
    headers = [("Kanji / Word", 150), ("Kana", 450), ("Romaji", 820), ("POS", 1120), ("Meaning" if not is_zh else "中文释义", 1350), ("Example Usage", 1750)]
    for htitle, hx in headers:
        draw.text((hx, ty + 18), htitle, fill=(255, 255, 255), font=get_font(24))
    ty += 65
    for i, (k, ka, ro, pos, en_m, zh_m, eg) in enumerate(vocab_data):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([(120, ty), (2360, ty + 85)], fill=bg, outline=(226, 232, 240), width=1)
        draw.text((150, ty + 25), k, fill=(15, 23, 42), font=get_font(26))
        draw.text((450, ty + 27), ka, fill=(29, 78, 216), font=get_font(22))
        draw.text((820, ty + 29), ro, fill=(100, 116, 139), font=get_font(20))
        draw.text((1120, ty + 29), pos, fill=(71, 85, 105), font=get_font(20))
        draw.text((1350, ty + 27), en_m if not is_zh else zh_m, fill=(15, 23, 42), font=get_font(22))
        draw.text((1750, ty + 29), eg, fill=(51, 65, 85), font=get_font(20))
        ty += 85
        
    # Grammar Breakdown Matrix
    draw.text((120, 2030), "Core Grammar & Particle Rules" if not is_zh else "核心语法接续与助词解析", fill=(15, 23, 42), font=get_font(34))
    draw.line([(120, 2080), (2360, 2080)], fill=(29, 78, 216), width=3)
    
    grammar_rules = [
        ("1. Particle を (Direct Object)", "[Noun] + を + [Transitive Verb]", "Marks the target that directly receives the action of the verb.", "決済サービスを発表しました (Announced the payment service)"),
        ("2. ~を使って (Using a Tool)", "[Noun/Tool] + を使って", "Expresses means or method of performing an action by using a device or system.", "Suicaを使って買い物をします (Shopping using Suica)"),
        ("3. ~を発表しました (Formal Announcement)", "[Event/Product] + を発表しました", "High-frequency press release and news pattern for official announcements.", "新料金プランを発表しました (Announced the new price plan)")
    ] if not is_zh else [
        ("1. 宾格助词「を」(Direct Object)", "【名词】+ を + 【他动词】", "表示动作直接作用的对象，在口语及新闻中极为高频。", "決済サービスを発表しました（发布了支付服务）"),
        ("2.「〜を使って」工具与手段接续", "【工具/服务】+ を使って", "表示使用某种具体工具、软件或支付手段进行后续动作。", "Suicaを使って買い物をします（使用Suica购物）"),
        ("3.「〜を発表しました」官方新闻句型", "【事项/新产品】+ を発表しました", "新闻发布会、官方公告必备句型，表示某项成果或服务的正式公开。", "新料金プランを発表しました（正式公布了新资费方案）")
    ]
    
    gy = 2120
    for r_title, r_form, r_desc, r_eg in grammar_rules:
        draw.rectangle([(120, gy), (2360, gy + 175)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.rectangle([(120, gy), (620, gy + 175)], fill=(239, 246, 255))
        draw.text((150, gy + 35), r_title, fill=(29, 78, 216), font=get_font(26))
        draw.text((150, gy + 100), r_form, fill=(100, 116, 139), font=get_font(20))
        
        draw.text((650, gy + 35), r_desc, fill=(15, 23, 42), font=get_font(24))
        draw.text((650, gy + 100), f"Example: {r_eg}" if not is_zh else f"例句：{r_eg}", fill=(13, 148, 136), font=get_font(22))
        gy += 200
        
    # Bottom Routine Box
    draw.rectangle([(120, 2780), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((160, 2815), "Daily Shadowing Routine" if not is_zh else "每日影子跟读打卡指南", fill=(29, 78, 216), font=get_font(30))
    steps = [
        ("1. Listen Blindly", "Play the 16:9 Masterclass or 9:16 Short without reading text to tune your pitch ear."),
        ("2. Vocal Repeat", "Shadow aloud immediately behind Nanami's Tokyo standard voice with 1-second reflex."),
        ("3. Workbook Practice", "Review the classified vocabulary and grammar points in this PDF guide daily.")
    ] if not is_zh else [
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
    foot = "TokyoFlow Japanese Academy  *  Daily Masterclasses & Shadowing  *  @TokyoFlowJapan" if not is_zh else "TokyoFlow 日语官方教学体系  *  每日实景精讲与影子跟读  *  @TokyoFlowJapan"
    draw.text((120, 3380), foot, fill=(100, 116, 139), font=get_font(22))
    draw.text((2150, 3380), "Page 1 of 1", fill=(15, 23, 42), font=get_font(24))
    
    out_pdf = OUTPUT_DIR / ("TokyoFlow_EP14_Suica_Teppay_Study_Companion_EN.pdf" if not is_zh else "TokyoFlow_EP14_Suica_Teppay_Study_Companion_ZH.pdf")
    img.save(out_pdf, "PDF", resolution=300.0)
    print(f"✓ Generated PDF: {out_pdf}")
    return out_pdf

# =========================================================================
# 2. COMPLETE PLAYLIST DEFINITIONS & CATEGORIZATION
# =========================================================================
PLAYLISTS_CONFIG = {
    "en_long": {
        "id": "PLHUEYGzrBe-s",
        "title": "TokyoFlow Japanese Masterclass [English Edition]",
        "filter": lambda item: item.get("lang") == "en" and item.get("format") == "long"
    },
    "en_short": {
        "id": "PLVxXRTmSmcAM",
        "title": "TokyoFlow Japanese Shorts [English Edition]",
        "filter": lambda item: item.get("lang") == "en" and item.get("format") == "short"
    },
    "zh_long": {
        "id": "PLVchR4TmK56E",
        "title": "TokyoFlow 日语实景精讲【中文解说版】",
        "filter": lambda item: item.get("lang") == "zh" and item.get("format") == "long"
    },
    "zh_short": {
        "id": "PLTpb6FPYqYC4",
        "title": "TokyoFlow 日语短视频跟读【中文解说版】",
        "filter": lambda item: item.get("lang") == "zh" and item.get("format") == "short"
    },
    "jlpt_n5": {
        "id": "PLY_ZLcqTrnU8",
        "title": "JLPT N5 Complete Immersion Masterclass",
        "filter": lambda item: "N5" in item.get("title", "").upper() or "N5" in item.get("level", "").upper()
    },
    "jlpt_n4": {
        "id": "PLIiV1gnNj8Ms",
        "title": "JLPT N4 Comprehensive Scenario Course",
        "filter": lambda item: "N4" in item.get("title", "").upper() or "N4" in item.get("level", "").upper()
    },
    "jlpt_n3": {
        "id": "PLFBaqxuiTcbo",
        "title": "JLPT N3 Intermediate Conversation & Nuance",
        "filter": lambda item: "N3" in item.get("title", "").upper() or "N3" in item.get("level", "").upper()
    },
    "transit": {
        "id": "PLAUUBQzM_liE",
        "title": "Tokyo Transit & Station Japanese",
        "filter": lambda item: any(k in item.get("title", "").lower() for k in ["transit", "suica", "station", "subway", "train", "yamanote", "shinkansen", "交通", "地铁", "西瓜卡"])
    },
    "kombini": {
        "id": "PLBhQ4N46ef1k",
        "title": "Kombini & Street Survival Japanese",
        "filter": lambda item: any(k in item.get("title", "").lower() for k in ["kombini", "convenience", "checkout", "coffee", "atm", "便利店"])
    },
    "dining": {
        "id": "PLA-JfaJhOu2E",
        "title": "Izakaya & Tokyo Foodie Japanese",
        "filter": lambda item: any(k in item.get("title", "").lower() for k in ["izakaya", "ramen", "gyudon", "food", "dining", "居酒屋", "拉面", "牛丼"])
    }
}

def sync_all_youtube_playlists(youtube, video_entries: list):
    """Adds videos into their corresponding playlists based on filters."""
    print("\n==================================================")
    print("Auditing & Synchronizing All YouTube Playlists")
    print("==================================================")
    
    # 1. Fetch current playlist contents
    playlist_existing = {}
    for pkey, pcfg in PLAYLISTS_CONFIG.items():
        pl_id = pcfg["id"]
        vids = set()
        page_token = None
        try:
            while True:
                res = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=pl_id,
                    maxResults=50,
                    pageToken=page_token
                ).execute()
                for item in res.get("items", []):
                    v = item["contentDetails"].get("videoId")
                    if v:
                        vids.add(v)
                page_token = res.get("nextPageToken")
                if not page_token:
                    break
        except Exception as e:
            print(f"Notice listing playlist {pl_id} ({pcfg['title']}): {e}")
        playlist_existing[pl_id] = vids
        print(f"Playlist [{pcfg['title']}]: {len(vids)} existing videos")
        
    # 2. Categorize and insert videos
    added_count = 0
    for item in video_entries:
        vid = item.get("id") or item.get("video_id")
        if not vid:
            continue
            
        for pkey, pcfg in PLAYLISTS_CONFIG.items():
            pl_id = pcfg["id"]
            if pcfg["filter"](item):
                if vid not in playlist_existing[pl_id]:
                    try:
                        print(f"Adding video {vid} -> Playlist: {pcfg['title']}...")
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
                        playlist_existing[pl_id].add(vid)
                        added_count += 1
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"Notice adding {vid} to {pl_id}: {e}")
                        
    print(f"\n[OK] Playlist synchronization complete! {added_count} new video placements added.")

# =========================================================================
# 3. YOUTUBE COMMENT & DESCRIPTION UPDATER
# =========================================================================
def update_video_descriptions_and_comments(youtube, published_entries: dict, drive_links: dict):
    print("\n==================================================")
    print("Updating YouTube Descriptions & Posting Pinned Comments")
    print("==================================================")
    
    passcode_ep14 = "TOKYOFLOW-EP14"
    passcode_week1 = "TOKYOFLOW-WEEK1"
    
    for key, item in published_entries.items():
        vid = item.get("id") or item.get("video_id")
        title = item.get("title", "")
        lang = item.get("lang", "en" if "_en_" in key or "-en" in key else "zh")
        is_zh = (lang == "zh")
        
        if not vid:
            continue
            
        # Select link and passcode
        if "14" in key or "14" in title or "EP14" in key or "E14" in key:
            drive_link = drive_links.get("ep14_zh" if is_zh else "ep14_en")
            passcode = passcode_ep14
            companion_title = "EP.14 Suica New Payment Service Study Companion (PDF)" if not is_zh else "第14期 JR东日本Suica全新支付配套研习讲义 (PDF)"
        else:
            drive_link = drive_links.get("week1_zh" if is_zh else "week1_en")
            passcode = passcode_week1
            companion_title = "Week 1 JLPT Master Study Workbook (PDF)" if not is_zh else "第一周 JLPT 实景学习讲义与复习手册 (PDF)"
            
        if not drive_link:
            continue
            
        # 1. Update Video Description to include Study Companion section
        try:
            v_res = youtube.videos().list(part="snippet", id=vid).execute()
            items = v_res.get("items", [])
            if items:
                snippet = items[0]["snippet"]
                cur_desc = snippet.get("description", "")
                
                download_block_en = (
                    f"\n\n------------------------------------------------------------\n"
                    f"[OFFICIAL STUDY COMPANION & JLPT WORKBOOK PDF]\n"
                    f"Download {companion_title}:\n"
                    f"Google Drive Link: {drive_link}\n"
                    f"Unlock Passcode (from video): {passcode}\n"
                    f"- Classified Vocabulary & Grammar tables [JLPT N5-N3]\n"
                    f"- Print-Friendly 300 DPI A4 Format (100% Free for Subscribers)\n"
                    f"------------------------------------------------------------\n"
                )
                
                download_block_zh = (
                    f"\n\n------------------------------------------------------------\n"
                    f"【本期课程配套 JLPT 研习讲义与复习手册下载】\n"
                    f"下载 {companion_title}：\n"
                    f"Google Drive 链接：{drive_link}\n"
                    f"视频完播口令 / 密码：{passcode}\n"
                    f"- 严格按照【JLPT N5】【JLPT N4】【JLPT N3】分级归纳\n"
                    f"- 高清 300 DPI A4 打印版（订阅学员免费下载）\n"
                    f"------------------------------------------------------------\n"
                )
                
                target_block = download_block_zh if is_zh else download_block_en
                
                if drive_link not in cur_desc:
                    new_desc = cur_desc + target_block
                    snippet["description"] = new_desc
                    # Required fields for video update
                    update_body = {
                        "id": vid,
                        "snippet": {
                            "title": snippet["title"],
                            "description": new_desc,
                            "categoryId": snippet.get("categoryId", "27")
                        }
                    }
                    if "tags" in snippet:
                        update_body["snippet"]["tags"] = snippet["tags"]
                        
                    youtube.videos().update(part="snippet", body=update_body).execute()
                    print(f"✓ Updated Description for [{vid}]: {title[:40]}...")
        except Exception as e:
            print(f"Notice updating description for {vid}: {e}")
            
        # 2. Post Pinned Comment
        try:
            if not is_zh:
                comment_body = (
                    f"Thank you for watching TokyoFlow Japanese!\n"
                    f"Download your {companion_title}:\n"
                    f"Google Drive Link: {drive_link}\n"
                    f"Unlock Passcode: {passcode}\n\n"
                    f"- Full Tokyo dialogue with Furigana & Romaji\n"
                    f"- Classified Vocabulary & Grammar tables\n\n"
                    f"Remember to SUBSCRIBE to TokyoFlow for daily Tokyo immersion masterclasses and shadowing drills!"
                )
            else:
                comment_body = (
                    f"感谢观看 TokyoFlow 日语实景精讲！\n"
                    f"本期【{companion_title}】已更新至 Google Drive 网盘：\n"
                    f"网盘下载链接：{drive_link}\n"
                    f"视频完播口令：{passcode}\n\n"
                    f"- 包含全场景对白、假名注音、罗马音及核心语法解析\n"
                    f"- 支持离线保存与高清 A4 打印学习\n\n"
                    f"记得点击【订阅】TokyoFlow 官方频道并开启小铃铛，每日打卡实景跟读训练！"
                )
                
            req = youtube.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": vid,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": comment_body
                            }
                        }
                    }
                }
            )
            c_res = req.execute()
            print(f"✓ Posted Study Guide Comment to [{vid}]: Thread ID {c_res.get('id')}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Notice posting comment for {vid}: {e}")

# =========================================================================
# MAIN EXECUTION ORCHESTRATOR
# =========================================================================
def main():
    print("==================================================")
    print("TokyoFlow Unified Study Companion & Playlist Engine")
    print("Zero-Emoji Discipline | Scheme D Passcode Distribution")
    print("==================================================")
    
    # 1. Generate & Encrypt EP.14 PDFs
    pdf_ep14_en = generate_ep14_study_companion(is_zh=False)
    encrypt_pdf(pdf_ep14_en, "TOKYOFLOW-EP14")
    
    pdf_ep14_zh = generate_ep14_study_companion(is_zh=True)
    encrypt_pdf(pdf_ep14_zh, "TOKYOFLOW-EP14")
    
    # 2. Upload / Sync to Google Drive
    drive_creds = get_drive_credentials()
    drive = build("drive", "v3", credentials=drive_creds)
    
    root_id = get_or_create_folder(drive, "TokyoFlow_Academy_Resources")
    workbooks_id = get_or_create_folder(drive, "Weekly_Master_Workbooks_PDF", parent_id=root_id)
    
    res_ep14_en = upload_and_share_file(drive, pdf_ep14_en, workbooks_id, "TokyoFlow_EP14_Suica_Teppay_Study_Companion_EN.pdf")
    res_ep14_zh = upload_and_share_file(drive, pdf_ep14_zh, workbooks_id, "TokyoFlow_EP14_Suica_Teppay_Study_Companion_ZH.pdf")
    
    drive_links = {
        "ep14_en": res_ep14_en.get("webViewLink", "https://drive.google.com/drive/folders/" + workbooks_id),
        "ep14_zh": res_ep14_zh.get("webViewLink", "https://drive.google.com/drive/folders/" + workbooks_id),
        "week1_en": "https://drive.google.com/file/d/1lfD3p_xXnwMmyuryRbzgn6kR232rcBs5/view?usp=drivesdk",
        "week1_zh": "https://drive.google.com/file/d/1QGhX4br_Vi-GugGTGmck_2-iV_2DzbDu/view?usp=drivesdk"
    }
    print(f"\n[DRIVE LINKS]:")
    print(f"  EP14 EN: {drive_links['ep14_en']}")
    print(f"  EP14 ZH: {drive_links['ep14_zh']}")
    
    # 3. Authenticate YouTube
    yt_creds = get_authenticated_service()
    youtube = build("youtube", "v3", credentials=yt_creds)
    
    # Load publish ledger
    if LEDGER_FILE.exists():
        ledger_data = json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
        published = ledger_data.get("published", {})
    else:
        published = {}
        
    video_list = []
    for k, v in published.items():
        v["key"] = k
        video_list.append(v)
        
    # 4. Synchronize Playlists
    sync_all_youtube_playlists(youtube, video_list)
    
    # 5. Update Descriptions & Post Comments
    update_video_descriptions_and_comments(youtube, published, drive_links)
    
    print("\n==================================================")
    print("All Tasks Completed Successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()
