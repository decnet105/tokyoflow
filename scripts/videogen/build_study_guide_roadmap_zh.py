#!/usr/bin/env python3
"""
TokyoFlow Japanese • Chinese Study Guide & Roadmap Video Producer (16:9 1080p)
=============================================================================
Generates a cinema-grade Chinese version of the Study Guide & Milestone Roadmap video.

Voice:
- Chinese Explainer: zh-CN-YunxiNeural
- Japanese Spoken Audio: ja-JP-NanamiNeural

Zero Emoji Policy strictly enforced.
Typography: Hiragino Sans GB.

Outputs:
- output/study_guide_zh/tokyoflow_study_guide_zh_1080p.mp4
- output/study_guide_zh/thumbnail.jpg
- output/study_guide_zh/metadata.md
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
OUT_DIR = PROJECT_ROOT / "output" / "study_guide_zh"
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

def draw_hud_header(draw, title_category="TOKYOFLOW ACADEMY", title_sub="官方学习大纲与进阶路线图"):
    font_cat = get_font(18)
    font_sub = get_font(16)
    
    # Left brand badge
    draw.rectangle([(60, 42), (240, 78)], fill=(18, 30, 48), outline=(56, 189, 248), width=1)
    draw.text((75, 50), "TOKYOFLOW ACADEMY", fill=(56, 189, 248), font=font_cat)
    
    # Right category indicator
    draw.text((1480, 50), title_sub, fill=(148, 163, 184), font=font_sub)
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
    font_txt = get_font(23)
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
# SCENE RENDERERS (CHINESE)
# =========================================================================

def render_scene_1_hero(draw, img):
    draw_hud_header(draw, "TOKYOFLOW ACADEMY", "官方学习系统总览")
    
    font_badge = get_font(20)
    font_h1 = get_font(52)
    font_h2 = get_font(28)
    font_p = get_font(22)
    
    # Center Hero Card
    draw.rectangle([(180, 140), (1740, 880)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    # Tag
    draw.rectangle([(230, 180), (590, 225)], fill=(30, 58, 138), outline=(56, 189, 248), width=1)
    draw.text((250, 190), "官方学习指南与进阶路线图", fill=(255, 255, 255), font=font_badge)
    
    # Main Title
    draw.text((230, 250), "如何真正掌握地道东京实景日语", fill=(255, 255, 255), font=font_h1)
    draw.text((230, 325), "从【JLPT N5】基础生存到【JLPT N1】高阶母语语感的完整学习蓝图", fill=(56, 189, 248), font=font_h2)
    
    # 3 Pillar Summary Boxes
    pillars = [
        ("01. 实景深度精讲", "16:9 1080p 大班课", "真实还原东京电车、便利店、居酒屋等生活全景。"),
        ("02. 口语跟读训练", "9:16 跟读短视频", "纯正东京标准音速记，训练声带与发音肌肉记忆。"),
        ("03. JLPT 分级进阶", "标准化能力大纲", "从 N5 生存反应到 N1 原声新闻，构建科学进阶体系。")
    ]
    
    for i, (p_title, p_sub, p_desc) in enumerate(pillars):
        px = 230 + i * 490
        py = 410
        draw.rectangle([(px, py), (px + 460, py + 400)], fill=(18, 26, 42), outline=(45, 60, 85), width=1)
        draw.rectangle([(px, py), (px + 460, py + 50)], fill=(24, 38, 62))
        draw.text((px + 20, py + 15), p_title, fill=(56, 189, 248), font=get_font(20))
        draw.text((px + 20, py + 70), p_sub, fill=(255, 255, 255), font=get_font(22))
        
        lines = [p_desc[:18], p_desc[18:]]
        for li, l in enumerate(lines):
            draw.text((px + 20, py + 120 + li * 30), l, fill=(148, 163, 184), font=font_p)
            
        draw.line([(px + 20, py + 220), (px + 440, py + 220)], fill=(35, 48, 70), width=1)
        draw.text((px + 20, py + 245), "核心能力培养：", fill=(203, 213, 225), font=get_font(18))
        if i == 0:
            draw.text((px + 20, py + 285), "- 场景上下文听力\n- 敬语与常体切换\n- 日本本土潜规则", fill=(148, 163, 184), font=get_font(18))
        elif i == 1:
            draw.text((px + 20, py + 285), "- 纯正东京语调与节奏\n- 摆脱中式发音发力\n- 0.5 秒本能脱口而出", fill=(148, 163, 184), font=get_font(18))
        else:
            draw.text((px + 20, py + 285), "- 助词与句型深度拆解\n- 流行语与缩略口语\n- NHK 原声新闻精读", fill=(148, 163, 184), font=get_font(18))

def render_scene_2_problem(draw, img):
    draw_hud_header(draw, "学习方法论", "为什么传统教材容易失效")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "为什么学了多年日语，在东京街头依然会瞬间卡壳？", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "深度对比传统课堂死记硬背与 TokyoFlow 实景流利法", fill=(148, 163, 184), font=font_sub)
    
    # Left Box
    draw.rectangle([(100, 220), (920, 850)], fill=(20, 22, 28), outline=(150, 60, 60), width=2)
    draw.rectangle([(100, 220), (920, 280)], fill=(45, 20, 20))
    draw.text((130, 235), "传统教材与课堂学习痛点", fill=(252, 165, 165), font=get_font(24))
    
    bad_points = [
        ("过度依赖死板敬语", "死记'我是学生'等生硬句式，现实中日本人极少这样交流。"),
        ("录音棚极慢语速，无环境音", "慢速录音脱离真实世界，面对车站报站和便利店语速瞬间慌乱。"),
        ("忽略口语缩略与助词省略", "教材不教常见的口语省音（-ちゃった, -とく）与日常省略。"),
        ("被动背单词，缺少肌肉记忆", "只在脑中默念，声带和喉部未形成条件反射，开口即迟疑。")
    ]
    for i, (title, desc) in enumerate(bad_points):
        y = 310 + i * 130
        draw.text((130, y), f"- {title}", fill=(248, 113, 113), font=get_font(22))
        draw.text((150, y + 35), desc, fill=(148, 163, 184), font=get_font(18))
        if i < 3:
            draw.line([(130, y + 105), (890, y + 105)], fill=(35, 30, 35), width=1)

    # Right Box
    draw.rectangle([(1000, 220), (1820, 850)], fill=(14, 24, 38), outline=(56, 189, 248), width=2)
    draw.rectangle([(1000, 220), (1820, 280)], fill=(18, 48, 80))
    draw.text((1030, 235), "TOKYOFLOW 实景解决方案", fill=(56, 189, 248), font=get_font(24))
    
    good_points = [
        ("场景驱动（Use-Case Driven）", "每一课紧扣具体生活场景：地铁补票、便利店结账、居酒屋点餐。"),
        ("纯正东京标准音与真实语速", "Nanami 东京原声配音，融入真实环境杂音，磨炼实战听力。"),
        ("双轨闭环（1080p 精讲 + 短片跟读）", "大班课透彻理解底层逻辑，短视频高频跟读训练声带肌肉。"),
        ("标准 JLPT 能力阶梯量化", "精准对应【JLPT N5】至【JLPT N1】，学习进展清晰可见。")
    ]
    for i, (title, desc) in enumerate(good_points):
        y = 310 + i * 130
        draw.text((1030, y), f"+ {title}", fill=(56, 189, 248), font=get_font(22))
        draw.text((1050, y + 35), desc, fill=(203, 213, 225), font=get_font(18))
        if i < 3:
            draw.line([(1030, y + 105), (1790, y + 105)], fill=(25, 45, 70), width=1)

def render_scene_3_cycle(draw, img):
    draw_hud_header(draw, "学习闭环", "三步掌握法")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "TokyoFlow 实景日语三步掌握法", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "如何将场景理解迅速转化为脱口而出的发音肌肉记忆", fill=(148, 163, 184), font=font_sub)
    
    steps = [
        ("步骤 01", "16:9 场景精讲大班课", "沉浸式场景理解与听力捕捉",
         "- 观看 1080p 完整实景还原\n- 捕捉真实店员语速与核心动词\n- 理解对话发生的前提与文化背景",
         (30, 58, 138), (56, 189, 248)),
        
        ("步骤 02", "句型语法与文化深度拆解", "底层语言逻辑透彻解析",
         "- 深度拆解格助词与敬语/常体切换\n- 剖析日本本土潜规则与委婉拒绝方式\n- 对标标准化 JLPT 语法考点",
         (20, 83, 45), (74, 222, 128)),
        
        ("步骤 03", "9:16 口语跟读短视频", "高频声带肌肉记忆训练",
         "- 同步跟读 Nanami 标准东京音\n- 严格模仿原声音调（Pitch Accent）\n- 重复 3-5 遍直至形成秒级本能反应",
         (120, 53, 15), (251, 191, 36))
    ]
    
    for i, (s_num, s_title, s_sub, s_desc, bg_head, fg_head) in enumerate(steps):
        sx = 100 + i * 590
        sy = 220
        draw.rectangle([(sx, sy), (sx + 540, sy + 630)], fill=(14, 20, 32), outline=fg_head, width=2)
        
        draw.rectangle([(sx, sy), (sx + 540, sy + 75)], fill=bg_head)
        draw.text((sx + 25, sy + 15), s_num, fill=fg_head, font=get_font(20))
        draw.text((sx + 25, sy + 40), s_title, fill=(255, 255, 255), font=get_font(22))
        
        draw.text((sx + 25, sy + 100), s_sub, fill=(255, 255, 255), font=get_font(22))
        draw.line([(sx + 25, sy + 140), (sx + 515, sy + 140)], fill=(35, 48, 70), width=1)
        
        draw.text((sx + 25, sy + 160), s_desc, fill=(203, 213, 225), font=get_font(20), spacing=18)
        
        draw.rectangle([(sx + 20, sy + 480), (sx + 520, sy + 600)], fill=(20, 30, 48), outline=(45, 65, 95), width=1)
        draw.text((sx + 35, sy + 495), "推荐实践方案：", fill=fg_head, font=get_font(18))
        if i == 0:
            draw.text((sx + 35, sy + 530), "每晚 08:00 PM (EDT) 专注看一课，\n梳理核心表达。", fill=(148, 163, 184), font=get_font(17))
        elif i == 1:
            draw.text((sx + 35, sy + 530), "随手记录核心句型卡，\n理解背后的文化逻辑。", fill=(148, 163, 184), font=get_font(17))
        else:
            draw.text((sx + 35, sy + 530), "利用碎片时间反复循环短视频，\n大声朗读跟读。", fill=(148, 163, 184), font=get_font(17))

def render_scene_4_roadmap(draw, img):
    draw_hud_header(draw, "进阶路线图", "五阶段 JLPT 能力体系")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "TokyoFlow 五阶段实景日语能力进阶路线图", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "从基础生存交流无障碍，到原声新闻深度解码的系统化进阶", fill=(148, 163, 184), font=font_sub)
    
    stages = [
        ("【JLPT N5】", "第一阶段：基础生存与公共出行", "掌握东京基础设施交流",
         ["山手线报站与内外环换乘听力", "7-Eleven/全家收银台秒回（加热/袋子）", "咖啡馆点单与堂食外带区分", "基本数字、价格与积分卡应答"],
         (30, 58, 138), (56, 189, 248)),
        
        ("【JLPT N4】", "第二阶段：日常独立生活无障碍", "应对生活突发与标准互动",
         ["地铁精算机补票与西瓜卡余额处理", "便利店热柜炸鸡与咖啡机操作口诀", "药妆店与药局常见症状求助表达", "标准许可与请求句型礼貌运用"],
         (14, 116, 144), (34, 211, 238)),
        
        ("【JLPT N3】", "第三阶段：深度社交与生活娱乐", "融入本土餐饮与兴趣文化",
         ["居酒屋生啤开场（とりあえず生）与AA结账", "顶级拉面食券机定制口诀（面硬/味浓）", "秋叶原手办免税与专柜库存询问", "日式钱汤温泉与桑拿整体（ととのう）礼仪"],
         (161, 98, 7), (250, 204, 21)),
        
        ("【JLPT N2】", "第四阶段：高阶社交与职场交流", "商务职场与委婉语境应对",
         ["银座精品店试衣试穿与尺码沟通", "职场日常寒暄与敬语谦让语自然切换", "出行旅行突发状况与挂失退改处理", "熟人朋友间常体与流行俚语适度运用"],
         (194, 65, 12), (251, 146, 60)),
        
        ("【JLPT N1】", "第五阶段：母语语感与原声媒体", "全方位解码日本社会与新闻",
         ["NHK 原声新闻政治经济精读听力", "日本企业商务谈判与委婉异议表达", "网络流行梗、动漫深层文化暗语拆解", "母语级 180+ 词/分 自然语速无压力交流"],
         (126, 34, 206), (192, 132, 252))
    ]
    
    for i, (badge, stage_title, stage_sub, items, bg_b, fg_b) in enumerate(stages):
        sy = 220 + i * 125
        draw.rectangle([(100, sy), (1820, sy + 110)], fill=(14, 20, 32), outline=(40, 55, 80), width=1)
        
        # Left Badge
        draw.rectangle([(110, sy + 15), (280, sy + 95)], fill=bg_b, outline=fg_b, width=2)
        draw.text((120, sy + 40), badge, fill=(255, 255, 255), font=get_font(24))
        
        # Title and sub
        draw.text((310, sy + 25), stage_title, fill=fg_b, font=get_font(22))
        draw.text((310, sy + 60), stage_sub, fill=(148, 163, 184), font=get_font(18))
        
        # Right Items (4 columns)
        for ji, item in enumerate(items):
            jx = 760 + (ji % 2) * 520
            jy = sy + 25 + (ji // 2) * 38
            draw.text((jx, jy), f"- {item}", fill=(226, 232, 240), font=get_font(17))

def render_scene_5_routine(draw, img):
    draw_hud_header(draw, "高效学习法", "每日 15 分钟闭环")
    
    font_h = get_font(36)
    font_sub = get_font(22)
    
    draw.text((100, 115), "TokyoFlow 每日 15 分钟高能闭环", fill=(255, 255, 255), font=font_h)
    draw.text((100, 165), "小步高频重复，让地道日语成为声带的本能肌肉反应", fill=(148, 163, 184), font=font_sub)
    
    blocks = [
        ("20:00 PM (EDT)", "晚间精讲（5 分钟）", "观看每晚更新的 16:9 中文解说大班课。\n专注理解场景对话、视觉线索与核心语法点。", (30, 58, 138), (56, 189, 248)),
        ("通勤 / 碎片时间", "极速跟读（5 分钟）", "打开对应 9:16 短视频，跟着 Nanami 原声\n出声大声跟读 3-5 遍，训练发音节奏与音调。", (20, 83, 45), (74, 222, 128)),
        ("睡前 / 晨起", "主动回忆（5 分钟）", "复习核心句型卡与主题播单。\n遮住答案自测：店员提问时能否瞬间脱口而出？", (120, 53, 15), (251, 191, 36))
    ]
    
    for i, (time_tag, b_title, b_desc, bg_tag, fg_tag) in enumerate(blocks):
        bx = 100 + i * 590
        by = 240
        draw.rectangle([(bx, by), (bx + 540, by + 580)], fill=(14, 20, 32), outline=fg_tag, width=2)
        
        draw.rectangle([(bx + 30, by + 30), (bx + 280, by + 80)], fill=bg_tag, outline=fg_tag, width=1)
        draw.text((bx + 45, by + 42), time_tag, fill=(255, 255, 255), font=get_font(22))
        
        draw.text((bx + 30, by + 110), b_title, fill=(255, 255, 255), font=get_font(24))
        draw.line([(bx + 30, by + 160), (bx + 510, by + 160)], fill=(35, 48, 70), width=1)
        
        draw.text((bx + 30, by + 190), b_desc, fill=(203, 213, 225), font=get_font(20), spacing=15)
        
        draw.rectangle([(bx + 30, by + 420), (bx + 510, by + 540)], fill=(20, 30, 48), outline=(45, 65, 95), width=1)
        draw.text((bx + 45, by + 440), "达成目标：", fill=fg_tag, font=get_font(18))
        if i == 0:
            draw.text((bx + 45, by + 475), "100% 场景深度理解", fill=(255, 255, 255), font=get_font(20))
        elif i == 1:
            draw.text((bx + 45, by + 475), "零迟疑脱口而出", fill=(255, 255, 255), font=get_font(20))
        else:
            draw.text((bx + 45, by + 475), "长期突触神经记忆", fill=(255, 255, 255), font=get_font(20))

def render_scene_6_cta(draw, img):
    draw_hud_header(draw, "开启学习", "开启你的实景日语之旅")
    
    font_h = get_font(40)
    font_sub = get_font(24)
    
    draw.rectangle([(140, 140), (1780, 880)], fill=(12, 18, 30), outline=(56, 189, 248), width=2)
    
    draw.text((200, 190), "今天起，真正掌握地道东京实景口语", fill=(255, 255, 255), font=font_h)
    draw.text((200, 260), "结构化主题播单、每日定时更新与电影级实景课堂", fill=(56, 189, 248), font=font_sub)
    
    pl_cards = [
        ("播单 01", "交通出行与山手线实景", "山手线报站、地铁换乘、闸机补票"),
        ("播单 02", "便利店与街头生活", "7-Eleven、全家、咖啡点单、结账秒回"),
        ("播单 03", "居酒屋与地道美食", "生啤开场、拉面食券机定制、餐桌礼仪"),
        ("播单 04", "NHK新闻与流行文化", "原声新闻听力、网络流行语、当季热点")
    ]
    
    for i, (p_tag, p_name, p_items) in enumerate(pl_cards):
        cx = 200 + (i % 2) * 720
        cy = 340 + (i // 2) * 190
        draw.rectangle([(cx, cy), (cx + 680, cy + 160)], fill=(18, 26, 42), outline=(45, 60, 85), width=1)
        
        draw.rectangle([(cx + 20, cy + 20), (cx + 140, cy + 55)], fill=(30, 58, 138))
        draw.text((cx + 35, cy + 26), p_tag, fill=(56, 189, 248), font=get_font(18))
        
        draw.text((cx + 160, cy + 26), p_name, fill=(255, 255, 255), font=get_font(22))
        draw.text((cx + 20, cy + 85), p_items, fill=(148, 163, 184), font=get_font(18))
        draw.text((cx + 20, cy + 118), "【包含 1080p 精讲大班课 + 9:16 跟读短视频】", fill=(56, 189, 248), font=get_font(16))

    draw.rectangle([(200, 750), (1720, 840)], fill=(16, 40, 70), outline=(56, 189, 248), width=2)
    draw.text((250, 775), "欢迎订阅 @TokyoFlowJapan  |  每日晚 08:00 PM (EDT) 中文版更新", fill=(255, 255, 255), font=get_font(26))
    draw.text((1250, 775), "从第一集开始学习 ->", fill=(56, 189, 248), font=get_font(24))

# =========================================================================
# SCRIPT DEFINITIONS & BUILDER
# =========================================================================

async def build_study_guide_video_zh():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n==================================================")
    print("Building TokyoFlow Chinese Study Guide & Roadmap Video")
    print("==================================================")
    
    script = [
        # Scene 1: Introduction
        {"id": "sg_zh_01", "scene": 1, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "欢迎来到 TokyoFlow 日语实景精讲！如果你学了很久日语，却在现实中不敢开口，这支视频是你的通关蓝图。"},
        {"id": "sg_zh_02", "scene": 1, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "speaker": "Nanami",
         "text": "教科書と実際の会話は、全然違いますよ！",
         "subtext": "教科书和实际的对话完全不一样哦！"},
        {"id": "sg_zh_03", "scene": 1, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "本指南将为你完整拆解我们的实景学习体系，以及从 JLPT N5 直达 N1 的全套进阶路线。"},
        
        # Scene 2: Problem
        {"id": "sg_zh_04", "scene": 2, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "很多同学背了多年语法，但一到东京电车站或便利店收银台前，依然会瞬间大脑一片空白。"},
        {"id": "sg_zh_05", "scene": 2, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "因为传统教材只教极慢的生硬敬语，完全缺少真实场景的速度感和环境噪音。"},
        {"id": "sg_zh_06", "scene": 2, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+2Hz", "speaker": "Nanami",
         "text": "袋はご利用ですか？温めますか？ポイントカードはお持ちですか？",
         "subtext": "需要袋子吗？需要加热吗？有积分卡吗？"},
        {"id": "sg_zh_07", "scene": 2, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "TokyoFlow 通过场景驱动法，带你直接潜入东京最真实的日常现场。"},
        
        # Scene 3: 3-Step Cycle
        {"id": "sg_zh_08", "scene": 3, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "我们的每一课都围绕科学的三步掌握闭环展开。"},
        {"id": "sg_zh_09", "scene": 3, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "第一步：实景沉浸。通过 16:9 大班课感受真实语速、环境氛围与核心动词。"},
        {"id": "sg_zh_10", "scene": 3, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "第二步：句型深度拆解。透彻理解每一个助词、敬语常体切换与日本本土潜规则。"},
        {"id": "sg_zh_11", "scene": 3, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "第三步：声带肌肉跟读。通过 9:16 短视频进行高频跟读，训练标准东京声调与秒回本能。"},
        
        # Scene 4: 5-Level JLPT Roadmap
        {"id": "sg_zh_12", "scene": 4, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "我们的课程严格对应标准 JLPT 五阶段能力进阶大纲。"},
        {"id": "sg_zh_13", "scene": 4, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "N5 与 N4 夯实基础生存：搞定山手线换乘、西瓜卡补票与便利店快速应答。"},
        {"id": "sg_zh_14", "scene": 4, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "N3 阶段解锁深度生活：熟练掌握居酒屋点单、拉面食券机定制与秋叶原免税购物。"},
        {"id": "sg_zh_15", "scene": 4, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "N2 与 N1 阶段攻克高阶语境：深入职场商务沟通与 NHK 原声新闻听力精读。"},
        
        # Scene 5: Daily Routine
        {"id": "sg_zh_16", "scene": 5, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "要想达到最佳效果，推荐执行每日十五分钟的高能复习法。"},
        {"id": "sg_zh_17", "scene": 5, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "晚间 8 点：观看每日更新的 16:9 中文解说大班课。"},
        {"id": "sg_zh_18", "scene": 5, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "碎片时间：利用 9:16 短视频出声跟读 3 到 5 遍。"},
        {"id": "sg_zh_19", "scene": 5, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "睡前：自测核心句型卡，检验是否能形成本能反射。"},
        
        # Scene 6: Playlists & Call to Action
        {"id": "sg_zh_20", "scene": 6, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "欢迎进入频道播放列表，按主题学习出行、便利店、居酒屋与热点新闻等专栏。"},
        {"id": "sg_zh_21", "scene": 6, "voice": "zh-CN-YunxiNeural", "rate": "+3%", "speaker": "Yunxi",
         "text": "点击订阅，收藏播单，今天就开启你的地道东京日语之旅！"},
        {"id": "sg_zh_22", "scene": 6, "voice": "ja-JP-NanamiNeural", "rate": "-4%", "pitch": "+3Hz", "speaker": "Nanami",
         "text": "一緒に、自然な東京の日本語をマスターしましょう！チャンネル登録をお願いします！",
         "subtext": "让我们一起掌握自然地道的东京日语！请订阅频道！"}
    ]
    
    # 1. Synthesize audio
    print("\n1. Synthesizing Chinese & Japanese audio tracks...")
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
    
    # 2. Concatenate audio
    print("\n2. Concatenating audio timeline...")
    concat_list = TEMP_DIR / "audio_concat.txt"
    with open(concat_list, "w") as f:
        f.write("file 'sil_05.mp3'\n")
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
    
    # 3. Render frames
    print("\n3. Rendering video frames (1920x1080 @ 30fps)...")
    fps = 30
    total_frames = int(total_duration * fps)
    
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
        
        active_seg = None
        for seg in timeline:
            if seg["start"] <= t <= seg["end"]:
                active_seg = seg
                break
                
        if active_seg:
            cur_scene = active_seg["scene"]
        else:
            cur_scene = 1
            for seg in timeline:
                if t >= seg["start"]:
                    cur_scene = seg["scene"]
                    
        frame = scene_bases[cur_scene].copy()
        draw = ImageDraw.Draw(frame)
        
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
            
    # 4. Compile video
    print("\n4. Encoding 1080p Master Video...")
    final_video = OUT_DIR / "tokyoflow_study_guide_zh_1080p.mp4"
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
    
    # 5. Build 16:9 Chinese Master Thumbnail
    print("\n5. Generating 16:9 Chinese Master Thumbnail...")
    thumb = get_clean_background()
    draw_t = ImageDraw.Draw(thumb)
    
    draw_hud_header(draw_t, "TOKYOFLOW ACADEMY", "官方学习指南")
    
    # Left Hero Panel
    draw_t.rectangle([(100, 140), (1200, 960)], fill=(12, 18, 30), outline=(56, 189, 248), width=3)
    
    # Badge
    draw_t.rectangle([(150, 190), (520, 245)], fill=(30, 58, 138), outline=(56, 189, 248), width=2)
    draw_t.text((170, 202), "官方学习大纲与指南", fill=(255, 255, 255), font=get_font(24))
    
    # Big Titles
    draw_t.text((150, 280), "如何真正掌握地道", fill=(255, 255, 255), font=get_font(56))
    draw_t.text((150, 360), "东京实景日语", fill=(56, 189, 248), font=get_font(64))
    
    draw_t.text((150, 460), "全套实景教学大纲与每日 15 分钟跟读闭环", fill=(226, 232, 240), font=get_font(26))
    
    badges = [
        ("【JLPT N5-N4】", "电车出行与便利店生存应答", (30, 58, 138)),
        ("【JLPT N3】", "居酒屋点餐与深度生活文化", (161, 98, 7)),
        ("【JLPT N2-N1】", "原声新闻解码与母语级语感", (126, 34, 206))
    ]
    for bi, (b_txt, b_desc, b_bg) in enumerate(badges):
        by = 540 + bi * 110
        draw_t.rectangle([(150, by), (400, by + 80)], fill=b_bg, outline=(255, 255, 255), width=1)
        draw_t.text((165, by + 22), b_txt, fill=(255, 255, 255), font=get_font(25))
        draw_t.text((430, by + 25), b_desc, fill=(203, 213, 225), font=get_font(24))
        
    draw_t.rectangle([(150, 880), (1150, 930)], fill=(18, 48, 80))
    draw_t.text((170, 892), "1080p 精讲大班课 + 9:16 口语跟读短视频双轨驱动", fill=(56, 189, 248), font=get_font(20))
    
    # Right Column: Real Tokyo Photo Feature
    right_photo_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_tokyo_skyline_distant_4k.jpg"
    if not right_photo_path.exists():
        right_photo_path = PROJECT_ROOT / "docs" / "youtube_assets" / "scene_backgrounds" / "scene_yamanote_platform.jpg"
        
    if right_photo_path.exists():
        r_img = Image.open(right_photo_path).convert("RGB")
        r_crop = r_img.resize((560, 820), Image.Resampling.LANCZOS)
        thumb.paste(r_crop, (1260, 140))
        draw_t.rectangle([(1260, 140), (1820, 960)], outline=(56, 189, 248), width=3)
        draw_t.rectangle([(1280, 880), (1800, 940)], fill=(10, 16, 26, 220))
        draw_t.text((1310, 898), "完整课程大纲【JLPT N5-N1】", fill=(255, 255, 255), font=get_font(22))
        
    thumb_path = OUT_DIR / "thumbnail.jpg"
    thumb.save(thumb_path, quality=95)
    print(f"Master Thumbnail saved: {thumb_path}")
    
    # 6. Metadata file
    metadata_content = """# TokyoFlow 日语实景精讲 • 官方学习指南与进阶大纲

## 视频基本信息
- **标题**: 【TokyoFlow 官方学习指南】告别死板教材！东京实景日语学习法与进阶大纲【JLPT N5-N1】
- **分类**: 教育 (27)
- **语言**: 中文解说 (zh) / 日文原声 (ja)
- **目标归属**: 播单《TokyoFlow 日语实景精讲【中文解说版】》置顶视频

## 视频简介
欢迎来到 TokyoFlow 日语实景精讲【中文解说版】！

如果你学了多年死板语法，但在东京街头面对店员提问依然会瞬间卡壳，这支视频将为你提供完整的实景日语破局方案。

在本期官方指南与路线图中，你将掌握：
1. 告别哑巴日语：为什么传统教材在真实东京街头会失效
2. 三步掌握闭环：1080p 大班课沉浸 -> 句型文化拆解 -> 9:16 短视频声带肌肉跟读（Shadowing）
3. 五阶段 JLPT 进阶路线图：从【JLPT N5】基础生存到【JLPT N1】NHK 原声新闻解码
4. 每日 15 分钟高能闭环：小步高频重复，构建终身语言神经反射
5. 主题播单与资源索引：如何高效利用交通出行、便利店生活、居酒屋餐饮等专栏

---

### 推荐学习播单：
- 播单 01：交通出行与山手线实景（山手线报站、地铁换乘、闸机补票）
- 播单 02：便利店与街头生活（7-Eleven、全家、咖啡点单、结账秒回）
- 播单 03：居酒屋与地道美食（生啤开场、拉面食券机定制、餐桌礼仪）
- 播单 04：NHK新闻与流行文化（原声新闻听力、网络流行语、当季热点）

每日晚 08:00 PM (EDT) 定时更新！
欢迎订阅 @TokyoFlowJapan，开启你的真实东京实景日语之旅！

#日语学习 #JLPT #东京实景 #日语口语 #东京 #TokyoFlow #JLPTN5 #JLPTN4 #JLPTN3 #JLPTN2 #JLPTN1

## YouTube 标签
TokyoFlow, 日语学习, 日本语, JLPT, JLPT N5, JLPT N4, JLPT N3, JLPT N2, JLPT N1, 东京, 场景日语, 日语口语, 日语听力, 跟读, 居酒屋日语, 便利店日语
"""
    with open(OUT_DIR / "metadata.md", "w") as f:
        f.write(metadata_content)
        
    print("Metadata generated at:", OUT_DIR / "metadata.md")
    print("\n[OK] Chinese Study Guide & Roadmap Build Complete!")

if __name__ == "__main__":
    asyncio.run(build_study_guide_video_zh())
