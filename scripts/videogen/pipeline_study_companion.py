#!/usr/bin/env python3
"""
TokyoFlow Japanese • Automated Pipeline Study Companion & Passcode Generator (Scheme D)
========================================================================================
Automates Scheme D (Video Passcode + Google Drive Download) across the entire video pipeline:
1. Dynamically generates episode/weekly study passcodes (e.g. TOKYOFLOW-WEEK1, TOKYO-EP12).
2. Compiles JLPT-categorized bilingual study workbooks (PDF 300 DPI A4).
3. Automatically syncs PDFs to Google Drive under 'TokyoFlow_Academy_Resources/Weekly_Master_Workbooks_PDF'.
4. Generates YouTube description boxes and pinned comments with passcode unlock instructions.
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VIDEOGEN_DIR = PROJECT_ROOT / "scripts" / "videogen"
sys.path.insert(0, str(VIDEOGEN_DIR))

try:
    from drive_manager import get_drive_credentials, get_or_create_folder, upload_and_share_file
    from googleapiclient.discovery import build
    DRIVE_AVAILABLE = True
except Exception:
    DRIVE_AVAILABLE = False

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def generate_passcode(series_code: str) -> str:
    """Generates standard uppercase alphanumeric passcode for Scheme D."""
    clean_code = series_code.upper().replace(".", "").replace("-", "")
    return f"TOKYOFLOW-{clean_code}"

def encrypt_pdf_with_passcode(pdf_path: Path, passcode: str) -> bool:
    """Encrypts a PDF file using 128-bit AES with user password."""
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(str(pdf_path))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password=passcode, owner_password=None, use_128bit=True)
        with open(pdf_path, "wb") as f:
            writer.write(f)
        print(f"  [SECURITY] Successfully encrypted {pdf_path.name} with passcode: {passcode}")
        return True
    except Exception as e:
        print(f"  [ERROR] Encryption failed for {pdf_path.name}: {e}")
        return False

def render_scheme_d_outro_card(passcode: str, is_zh: bool = False) -> Image.Image:
    """Renders a 1920x1080 Full HD Outro Passcode & Download Verification Card for video streams."""
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Top ribbon
    draw.rectangle([(0, 0), (W, 90)], fill=(30, 41, 59))
    draw.text((80, 28), "TokyoFlow Japanese Academy  |  Official Course Companion", fill=(255, 255, 255), font=get_font(28))
    draw.text((W - 420, 28), "[SUBSCRIBER REWARD]", fill=(244, 114, 182), font=get_font(26))
    
    # Central Card
    draw.rectangle([(160, 160), (W - 160, H - 140)], fill=(255, 255, 255), outline=(29, 78, 216), width=4)
    
    # Card Header
    draw.rectangle([(160, 160), (W - 160, 270)], fill=(239, 246, 255))
    h_title = "COMPANION STUDY WORKBOOK • UNLOCK PASSCODE" if not is_zh else "【配套研习讲义 • 完播专属解锁码】"
    draw.text((220, 195), h_title, fill=(29, 78, 216), font=get_font(34))
    
    # Passcode Display Box
    draw.rectangle([(220, 320), (1060, 560)], fill=(254, 243, 199), outline=(217, 119, 6), width=3)
    draw.text((260, 350), "OFFICIAL PDF UNLOCK CODE:" if not is_zh else "本期讲义解锁口令 / 密码：", fill=(146, 64, 14), font=get_font(24))
    draw.text((260, 415), passcode, fill=(180, 83, 9), font=get_font(56))
    draw.text((260, 500), "[SUBSCRIBE CHANNEL TO ACCESS DRIVE FOLDER]" if not is_zh else "【订阅频道并在置顶评论区获取网盘链接】", fill=(13, 148, 136), font=get_font(20))
    
    # Instructions
    draw.text((1140, 330), "How to Download Your PDF:" if not is_zh else "讲义获取三步法：", fill=(15, 23, 42), font=get_font(30))
    
    steps = [
        "1. Subscribe to TokyoFlow on YouTube.",
        "2. Click the Google Drive link in the pinned comment / description.",
        "3. Download the full JLPT N5-N3 Study Workbook PDF."
    ] if not is_zh else [
        "1. 订阅 TokyoFlow YouTube 官方频道。",
        "2. 点击置顶评论或简介栏中的 Google Drive 讲义链接。",
        "3. 免费保存并打印完整中英双语 JLPT 复习手册。"
    ]
    
    sy = 400
    for s in steps:
        draw.text((1140, sy), s, fill=(51, 65, 85), font=get_font(24))
        sy += 65
        
    # Footer Note
    draw.rectangle([(220, 620), (W - 220, 740)], fill=(248, 250, 252), outline=(226, 232, 240), width=2)
    note_txt = "Tip: Save this PDF for daily vocal shadowing drills and JLPT exam preparation!" if not is_zh else "学习建议：讲义包含全场景对白、JLPT分级词汇与语法详解，建议配合每日跟读复习！"
    draw.text((260, 660), note_txt, fill=(29, 78, 216), font=get_font(24))
    
    return img

def sync_study_guide_to_drive(pdf_path: Path, display_name: str) -> dict:
    """Syncs generated study guide to Google Drive and returns public links."""
    if not DRIVE_AVAILABLE or not pdf_path.exists():
        return {}
    
    try:
        creds = get_drive_credentials()
        drive = build("drive", "v3", credentials=creds)
        
        root_id = get_or_create_folder(drive, "TokyoFlow_Academy_Resources")
        guides_id = get_or_create_folder(drive, "Weekly_Master_Workbooks_PDF", parent_id=root_id)
        
        res = upload_and_share_file(drive, pdf_path, guides_id, display_name)
        return res
    except Exception as e:
        print(f"[Drive Sync Notice]: {e}")
        return {}

def format_youtube_scheme_d_text(passcode: str, drive_link: str, is_zh: bool = False) -> dict:
    """Generates standard YouTube description section and pinned comment for Scheme D."""
    if not is_zh:
        desc_snippet = (
            "\n------------------------------------------------------------\n"
            "[STUDY COMPANION & JLPT WORKBOOK DOWNLOAD]\n"
            "Download the complete Weekly JLPT Study Guide (PDF):\n"
            f"Link: {drive_link}\n"
            f"Unlock Passcode (from video): {passcode}\n"
            "- Organized by [JLPT N5], [JLPT N4], and [JLPT N3]\n"
            "- 100% Free for TokyoFlow Subscribers\n"
            "------------------------------------------------------------\n"
        )
        pinned_comment = (
            f"Thank you for watching! Download the complete JLPT Study Workbook (PDF) for this week:\n"
            f"Google Drive Link: {drive_link}\n"
            f"Unlock Passcode: {passcode}\n\n"
            "Remember to Subscribe to TokyoFlow for daily Tokyo immersion masterclasses and shadowing drills!"
        )
    else:
        desc_snippet = (
            "\n------------------------------------------------------------\n"
            "【本期课程配套 JLPT 研习讲义免费下载】\n"
            "完整中英双语 6 页高清 A4 打印版复习手册（词汇/语法/台词分级整理）：\n"
            f"Google Drive 下载链接：{drive_link}\n"
            f"视频完播口令 / 密码：{passcode}\n"
            "- 严格按照【JLPT N5】【JLPT N4】【JLPT N3】分级归纳\n"
            "- 订阅学员免费下载保存与打印\n"
            "------------------------------------------------------------\n"
        )
        pinned_comment = (
            f"感谢观看本期 TokyoFlow 实景精讲！第一周完整配套研习讲义与 JLPT 复习手册已更新：\n"
            f"网盘下载链接：{drive_link}\n"
            f"视频完播口令：{passcode}\n\n"
            "记得点击【订阅】TokyoFlow 官方频道并开启小铃铛，每日打卡实景跟读训练！"
        )
    return {
        "description_snippet": desc_snippet,
        "pinned_comment": pinned_comment
    }

if __name__ == "__main__":
    test_code = generate_passcode("WM.01")
    print(f"Sample Passcode: {test_code}")
    card = render_scheme_d_outro_card(test_code, is_zh=False)
    test_out = PROJECT_ROOT / "tmp" / "test_scheme_d_card.png"
    test_out.parent.mkdir(parents=True, exist_ok=True)
    card.save(test_out)
    print(f"Rendered test card to {test_out}")
