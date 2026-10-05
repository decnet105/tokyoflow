#!/usr/bin/env python3
"""
TokyoFlow Japanese • Chinese Print-Friendly PDF Study Guide Generator (300 DPI A4)
==================================================================================
- 100% Print-Friendly Light/White Layout (节省墨水，高清雅致).
- 自动文本换行，确保零文字溢出与零截断.
- 严格遵循零 Emoji 纪律.
- 标准化能力徽章: 【JLPT N5】至【JLPT N1】.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "output" / "study_guide_zh"
FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def draw_wrapped_text(draw, text: str, font, fill, x: int, y: int, max_width: int, line_spacing: int = 12) -> int:
    """Draws multiline wrapped text within max_width and returns the bottom Y coordinate."""
    clean_text = text.replace("〜", "-").replace("〜", "-")
    
    # Handle Chinese/Japanese character wrapping
    lines = []
    cur_line = ""
    
    for char in clean_text:
        test_line = cur_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            cur_line = test_line
        else:
            if cur_line:
                lines.append(cur_line)
                cur_line = char
            else:
                lines.append(char)
                cur_line = ""
    if cur_line:
        lines.append(cur_line)
        
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
    
    draw.text((490, 110), "实景日语流利蓝图  |  官方教学大纲与进阶路线图", fill=(71, 85, 105), font=get_font(24))
    draw.text((1950, 110), "【JLPT N5-N1 路线图】", fill=(29, 78, 216), font=get_font(24))
    draw.line([(120, 170), (2360, 170)], fill=(203, 213, 225), width=2)
    
    # Bottom Footer
    draw.line([(120, 3350), (2360, 3350)], fill=(203, 213, 225), width=2)
    draw.text((120, 3380), "TokyoFlow 日语实景精讲  *  每日晚 08:00 PM (EDT) 定时更新  *  @TokyoFlowJapan", fill=(100, 116, 139), font=get_font(22))
    draw.text((2150, 3380), f"第 {page_num} 页 / 共 {total_pages} 页", fill=(15, 23, 42), font=get_font(24))

# =========================================================================
# PAGE 1: TITLE & EXECUTIVE BLUEPRINT (CHINESE)
# =========================================================================
def make_page_1():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 1)
    
    # Executive Title Card
    draw.rectangle([(120, 210), (2360, 620)], fill=(248, 250, 252), outline=(29, 78, 216), width=3)
    
    draw.rectangle([(170, 245), (590, 300)], fill=(239, 246, 255), outline=(29, 78, 216), width=2)
    draw.text((195, 258), "官方学习大纲与方法指南", fill=(29, 78, 216), font=get_font(24))
    
    draw.text((170, 325), "TokyoFlow 实景日语流利蓝图", fill=(15, 23, 42), font=get_font(58))
    draw.text((170, 410), "如何真正掌握地道东京实景日语【JLPT N5-N1】", fill=(29, 78, 216), font=get_font(34))
    draw.text((170, 475), "场景驱动体系：16:9 场景精讲大班课 与 9:16 声带肌肉跟读短视频双轨闭环", fill=(51, 65, 85), font=get_font(24))
    draw.text((170, 535), "更新时间：每日晚 08:00 PM (EDT)  |  东京标准语调原声音频", fill=(100, 116, 139), font=get_font(22))

    # Section 1: The Reality Gap
    draw.text((120, 670), "一、 现实鸿沟：为什么传统教材在东京街头容易失效？", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 720), (2360, 720)], fill=(29, 78, 216), width=3)
    
    # Left Card: Traditional Textbooks
    draw.rectangle([(120, 750), (1210, 1420)], fill=(255, 245, 245), outline=(252, 165, 165), width=2)
    draw.rectangle([(120, 750), (1210, 825)], fill=(254, 226, 226))
    draw.text((160, 772), "传统教材与传统教学痛点", fill=(185, 28, 28), font=get_font(26))
    
    trad_points = [
        ("生硬死板的敬语过度依赖", "反复练习'我是学生'等脱离现实的句式，现实生活中日本人极少如此对话。"),
        ("录音棚极慢语速脱离真实场景", "无环境噪音的慢速发音，导致在面对真实的电车报站与便利店语速时瞬间慌乱。"),
        ("忽略口语缩略与助词省略现象", "极少讲解日常高频的口语省音（-ちゃった, -とく, -なきゃ）与自然的助词脱落。"),
        ("被动默读陷阱，缺乏发音肌肉记忆", "只在脑中背诵单词，声带与喉部缺乏条件反射，遇到提问无法在 0.5 秒内做出反应。")
    ]
    
    cur_y = 855
    for title, desc in trad_points:
        draw.text((160, cur_y), f"- {title}", fill=(185, 28, 28), font=get_font(24))
        cur_y = draw_wrapped_text(draw, desc, get_font(20), (71, 85, 105), 185, cur_y + 36, 980, line_spacing=6)
        cur_y += 12
        
    # Right Card: TokyoFlow Blueprint
    draw.rectangle([(1270, 750), (2360, 1420)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
    draw.rectangle([(1270, 750), (2360, 825)], fill=(219, 234, 254))
    draw.text((1310, 772), "TokyoFlow 实景教学破局方案", fill=(29, 78, 216), font=get_font(26))
    
    sol_points = [
        ("场景驱动（Use-Case Driven）", "每一课紧扣真实东京生活场景：地铁补票、便利店应答、居酒屋点单、拉面定制。"),
        ("纯正东京原声与真实环境音", "Nanami 东京原声配音，融入环境白噪音，从第一天起适应真实街头听力语境。"),
        ("双轨闭环（1080p 精讲 + 9:16 跟读）", "大班课透彻解析语法与文化逻辑，短视频高频跟读训练声带肌肉，形成本能反应。"),
        ("标准 JLPT 能力阶梯量化", "精准对应【JLPT N5】至【JLPT N1】，明确掌握每一阶段的实战交际能力。")
    ]
    
    cur_y = 855
    for title, desc in sol_points:
        draw.text((1310, cur_y), f"+ {title}", fill=(29, 78, 216), font=get_font(24))
        cur_y = draw_wrapped_text(draw, desc, get_font(20), (51, 65, 85), 1335, cur_y + 36, 980, line_spacing=6)
        cur_y += 12

    # Section 2: The 4 Core Pillar Tracks
    draw.text((120, 1480), "二、 四大实景核心专栏体系", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1530), (2360, 1530)], fill=(29, 78, 216), width=3)
    
    pillars = [
        ("专栏 01：交通出行与电车实景", "【JLPT N5-N4】",
         "- 山手线内外环报站与站台广播听力\n- 地铁换乘、精算机补票与西瓜卡异常处理\n- 新干线指定席购买、补票与乘务员对话", (239, 246, 255), (29, 78, 216)),
        
        ("专栏 02：便利店与街头生活", "【JLPT N5-N3】",
         "- 7-Eleven/全家收银台秒回（加热/袋子/小票）\n- 热柜炸鸡（炸鸡块/全家桶）与现磨咖啡机操作\n- 药妆店常见症状求助与咖啡馆点单", (240, 253, 250), (13, 148, 136)),
        
        ("专栏 03：居酒屋与地道美食", "【JLPT N4-N2】",
         "- 居酒屋生啤开场（とりあえず生）与AA结账\n- 顶级拉面食券机定制（面硬/味浓/加背脂）\n- 传统钱汤温泉礼仪与秋叶原手办免税退税", (254, 243, 199), (180, 83, 9)),
        
        ("专栏 04：原声新闻与文化热点", "【JLPT N2-N1】",
         "- NHK 原声时政经济新闻听力精读\n- 日本职场寒暄、敬语与谦让语自然切换\n- 网络流行梗、动漫深层文化暗语拆解", (245, 243, 255), (109, 40, 217))
    ]
    
    for i, (p_title, p_badge, p_bullets, p_bg, p_fg) in enumerate(pillars):
        px = 120 + (i % 2) * 1150
        py = 1560 + (i // 2) * 440
        draw.rectangle([(px, py), (px + 1090, py + 400)], fill=(255, 255, 255), outline=p_fg, width=2)
        
        draw.rectangle([(px, py), (px + 1090, py + 75)], fill=p_bg)
        draw.text((px + 25, py + 22), p_title, fill=p_fg, font=get_font(24))
        draw.text((px + 860, py + 22), p_badge, fill=p_fg, font=get_font(22))
        
        draw.text((px + 25, py + 95), "核心场景涵盖：", fill=(15, 23, 42), font=get_font(22))
        draw_wrapped_text(draw, p_bullets, get_font(20), (71, 85, 105), px + 25, py + 135, 1040, line_spacing=10)
        
        draw.rectangle([(px + 25, py + 320), (px + 1065, py + 380)], fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((px + 45, py + 338), "16:9 场景深度大班课  +  9:16 声带跟读短视频", fill=(30, 41, 59), font=get_font(20))

    # Bottom Note Box
    draw.rectangle([(120, 2500), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((170, 2540), "如何最高效运用本学习大纲", fill=(29, 78, 216), font=get_font(34))
    draw.text((170, 2600), "本蓝图旨在培养'听得懂、接得上、脱口而出'的主动口语能力，而非死记硬背语法规则。", fill=(51, 65, 85), font=get_font(22))
    
    tips = [
        ("法则一：声音优先，建立语感", "在查看语法解析前，务必先盲听场景原声音频，捕捉整体语速、语调与店员意图。"),
        ("法则二：必须出声大声跟读", "在脑中默读无法训练声带与面部发音肌肉。必须跟着 Nanami 原声大声朗读。"),
        ("法则三：每日 15 分钟闭环复习", "持续的高频小步重复远胜于周末突击。请遵循第二页详述的 15 分钟每日学习法。")
    ]
    
    for i, (t_title, t_desc) in enumerate(tips):
        y = 2670 + i * 190
        draw.rectangle([(170, y), (2310, y + 155)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((200, y + 25), t_title, fill=(29, 78, 216), font=get_font(24))
        draw_wrapped_text(draw, t_desc, get_font(21), (51, 65, 85), 200, y + 72, 2060, line_spacing=6)
        
    return img

# =========================================================================
# PAGE 2: 3-STEP CYCLE & 15-MIN ROUTINE (CHINESE)
# =========================================================================
def make_page_2():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 2)
    
    # Section 3: 3-Step Mastery Cycle
    draw.text((120, 210), "三、 TokyoFlow 实景日语三步掌握闭环", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    steps = [
        ("步骤 01：实景沉浸", "16:9 场景精讲大班课 (1080p)", (239, 246, 255), (29, 78, 216),
         [
             "在完整的真实场景中观看 1080p 视频（车站、便利店、居酒屋、拉面店）。",
             "观察自然的母语对话语速、身体动作线索以及真实的环境环境杂音。",
             "捕捉对话核心触发点：店员问了什么，需要以什么样的句式在 0.5 秒内回应。"
         ]),
        
        ("步骤 02：句型与文化深度拆解", "底层语言逻辑与文化潜规则透彻解析", (240, 253, 250), (13, 148, 136),
         [
             "深度拆解核心句型、助词用法以及敬语与常体的自然切换。",
             "剖析日本本土潜规则（例如为什么日本人习惯说'結構です'而非生硬拒绝'いいえ'）。",
             "精准对标标准化能力考点：【JLPT N5】至【JLPT N1】。"
         ]),
        
        ("步骤 03：声带肌肉跟读", "9:16 口语跟读短视频 (<60秒)", (254, 243, 199), (180, 83, 9),
         [
             "同步跟读 Nanami 标准东京原声音频，不看字幕同步模仿发音。",
             "严格匹配东京声调音高（Pitch Accent）、音节停顿与地道语速节奏。",
             "高频重复 3 到 5 遍，直至形成脱口而出的条件反射。"
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

    # Section 4: 4-Pass Shadowing Protocol
    draw.text((120, 1460), "四、 四轮科学跟读法（4-Pass Shadowing）", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1510), (2360, 1510)], fill=(29, 78, 216), width=3)
    
    passes = [
        ("第 1 轮：闭眼盲听", "纯听不看字幕（闭眼）", "感受整体声调起伏、重音停顿与东京节奏。不急于朗读。"),
        ("第 2 轮：字幕伴读", "对照日文字幕同步发声", "将发音节奏与原声对齐，确保每一个音节清晰到位、发力准确。"),
        ("第 3 轮：纯粹盲跟", "脱离字幕，0.2秒延迟紧随", "在原声后 0.2 秒同步跟读，锻炼声带肌肉记忆与本能反应。"),
        ("第 4 轮：1.2倍速挑战", "快进播放高能冲刺", "在 1.2 倍速下挑战跟读，确保在真实东京日常对话中游刃有余。")
    ]
    
    for i, (p_title, p_sub, p_desc) in enumerate(passes):
        px = 120 + (i % 2) * 1150
        py = 1540 + (i // 2) * 270
        draw.rectangle([(px, py), (px + 1090, py + 240)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
        draw.rectangle([(px, py), (px + 1090, py + 65)], fill=(219, 234, 254))
        draw.text((px + 25, py + 18), p_title, fill=(29, 78, 216), font=get_font(24))
        draw.text((px + 25, py + 85), p_sub, fill=(3, 105, 161), font=get_font(22))
        draw_wrapped_text(draw, p_desc, get_font(21), (51, 65, 85), px + 25, py + 130, 1040, line_spacing=6)

    # Section 5: Daily 15-Minute Routine
    draw.text((120, 2140), "五、 每日 15 分钟高能复习法", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 2190), (2360, 2190)], fill=(29, 78, 216), width=3)
    
    routine_cards = [
        ("晚间 20:00 PM (EDT)", "5 分钟：精看 16:9 大班课", (239, 246, 255), (29, 78, 216),
         "观看每晚更新的 1080p 中文解说实景课，梳理对话场景脉络，记录核心句型与助词。"),
        
        ("碎片时间 / 通勤", "5 分钟：9:16 短视频跟读", (240, 253, 250), (13, 148, 136),
         "打开手机 YouTube Shorts，利用第 2 轮与第 3 轮跟读法大声练习 3 到 5 遍。"),
        
        ("睡前 / 晨起", "5 分钟：主动自测与回忆", (254, 243, 199), (180, 83, 9),
         "复习核心句型卡，遮住答案自测：如果店员询问是否需要积分卡，你能否瞬间脱口而出？")
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
# PAGE 3: 5-LEVEL JLPT SYLLABUS (CHINESE)
# =========================================================================
def make_page_3():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 3)
    
    draw.text((120, 210), "六、 五阶段 JLPT 实景能力大纲", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    curriculum = [
        ("【JLPT N5】", "第一阶段：基础生存与公共出行", "公共基础设施交流与日常简单互动", (239, 246, 255), (29, 78, 216),
         [
             ("山手线报站与换乘", "下一站提示听力（次は新宿です）、内外环与线路换乘。"),
             ("便利店收银台基础", "袋子需求（袋は大丈夫です）、便当加热与小票拒绝。"),
             ("咖啡馆与快餐点单", "杯型大小（Tall/Grande）、冷热与堂食/外带（お持ち帰り）。"),
             ("数字与极速价格应答", "收银台日元金额听辨与积分卡有无快速反应。")
         ]),
        
        ("【JLPT N4】", "第二阶段：日常独立生活无障碍", "应对生活突发状况与标准礼貌互动", (240, 253, 250), (13, 148, 136),
         [
             ("地铁精算机补票", "西瓜卡/Pasmo 余额不足、使用精算机补票全流程。"),
             ("便利店热柜与咖啡机", "点购热柜炸鸡（炸鸡块/全家桶）与自助咖啡机操作。"),
             ("药妆店与药局问询", "描述头痛、胃痛、感冒等常见症状与用药咨询。"),
             ("礼貌请求与许可", "公共场合标准礼貌询问（-てもいいですか, -お願いします）。")
         ]),
        
        ("【JLPT N3】", "第三阶段：深度社交与生活娱乐", "融入本土餐饮、爱好文化与生活礼仪", (254, 243, 199), (180, 83, 9),
         [
             ("居酒屋点餐与AA结账", "首轮生啤点单（とりあえず生！）、加单与分开结账（別々）。"),
             ("拉面食券机定制", "定制面条硬度（硬め）、汤头浓淡（濃いめ）与加背脂。"),
             ("秋叶原免税购物", "专柜询问现货、护照免税退税流程与手办交流。"),
             ("钱汤温泉与桑拿礼仪", "清洗区洗浴礼仪、储物柜钥匙使用与桑拿（ととのう）文化。")
         ]),
        
        ("【JLPT N2】", "第四阶段：高阶社交与职场交流", "商务沟通、精品购物与突发事件应对", (255, 241, 242), (225, 29, 72),
         [
             ("银座精品店试衣", "服装试穿、尺码调整沟通与高雅委婉表达。"),
             ("职场寒暄与敬语切换", "お疲れ様です、谦让语与尊他语在真实职场中自然切换。"),
             ("出行突发状况处理", "电车站失物招领（遺失物）、新干线退改签与延误证明。"),
             ("熟人常体与流行语", "准确把握与日本朋友交流时常体与流行口语的使用分寸。")
         ]),
        
        ("【JLPT N1】", "第五阶段：母语语感与原声媒体", "全方位解码日本社会、新闻与高阶语境", (245, 243, 255), (109, 40, 217),
         [
             ("NHK 原声新闻精读", "时政经济新闻听力、专业术语与严谨文法拆解。"),
             ("商务谈判与委婉异议", "委婉表达不同意见、日本企业深层商务沟通逻辑。"),
             ("网络流行语与动漫暗语", "解码社交媒体热梗、动漫作品双关语与深层文化隐喻。"),
             ("母语级流畅交流", "在每分钟 180+ 词的母语语速下无障碍轻松交流。")
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
# PAGE 4: PLAYLISTS & 30-DAY HABIT TRACKER (CHINESE)
# =========================================================================
def make_page_4():
    W, H = 2480, 3508
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, 4)
    
    # Section 7: Playlists
    draw.text((120, 210), "七、 官方主题播单与学习专栏", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 260), (2360, 260)], fill=(29, 78, 216), width=3)
    
    pls = [
        ("播单 01：交通出行与山手线实景", "山手线报站、东京地铁换乘、闸机补票全流程", "https://youtube.com/playlist?list=PLVchR4TmK56E"),
        ("播单 02：便利店与街头生活", "7-Eleven、全家便利店、咖啡点单、结账秒回口诀", "进入频道【播放列表】专区点击学习"),
        ("播单 03：居酒屋与地道美食", "生啤开场、拉面食券机定制、餐桌礼仪与AA结账", "进入频道【播放列表】专区点击学习"),
        ("播单 04：NHK新闻与流行文化", "原声新闻听力精读、网络流行语、当季热点新闻", "进入频道【播放列表】专区点击学习")
    ]
    
    for i, (pl_name, pl_desc, pl_link) in enumerate(pls):
        py = 290 + i * 180
        draw.rectangle([(120, py), (2360, py + 150)], fill=(240, 249, 255), outline=(147, 197, 253), width=2)
        draw.text((160, py + 25), pl_name, fill=(29, 78, 216), font=get_font(25))
        draw_wrapped_text(draw, pl_desc, get_font(21), (51, 65, 85), 160, py + 75, 1500, line_spacing=6)
        draw.text((1720, py + 25), "【包含精讲与跟读】", fill=(13, 148, 136), font=get_font(22))

    # Section 8: 30-Day Habit Tracker
    draw.text((120, 1100), "八、 30 天实景日语流利习惯打卡表（Habit Tracker）", fill=(15, 23, 42), font=get_font(36))
    draw.line([(120, 1150), (2360, 1150)], fill=(29, 78, 216), width=3)
    draw.text((120, 1180), "每完成当天的 15 分钟闭环（大班课 + 极速跟读），请在对应方框内打勾记录成就。", fill=(71, 85, 105), font=get_font(22))
    
    grid_start_y = 1240
    for day in range(1, 31):
        c = (day - 1) % 6
        r = (day - 1) // 6
        gx = 120 + c * 380
        gy = grid_start_y + r * 190
        
        draw.rectangle([(gx, gy), (gx + 350, gy + 160)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
        draw.rectangle([(gx, gy), (gx + 350, gy + 45)], fill=(239, 246, 255))
        draw.text((gx + 20, gy + 12), f"第 {day:02d} 天", fill=(29, 78, 216), font=get_font(22))
        
        draw.rectangle([(gx + 20, gy + 65), (gx + 50, gy + 95)], outline=(100, 116, 139), width=2)
        draw.text((gx + 65, gy + 68), "16:9 精讲课", fill=(51, 65, 85), font=get_font(20))
        
        draw.rectangle([(gx + 20, gy + 115), (gx + 50, gy + 145)], outline=(100, 116, 139), width=2)
        draw.text((gx + 65, gy + 118), "9:16 短跟读", fill=(51, 65, 85), font=get_font(20))

    # Section 9: Community & Next Steps
    draw.rectangle([(120, 2300), (2360, 3280)], fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((180, 2350), "加入 TokyoFlow 全球学习者社区", fill=(29, 78, 216), font=get_font(36))
    
    comm_bullets = [
        ("订阅官方频道", "访问 @TokyoFlowJapan 并开启通知，锁定每日晚 08:00 PM (EDT) 中文版更新。"),
        ("参与评论区互动", "在评论区留下你今年的 JLPT 目标等级与今日跟读打卡心得。"),
        ("分享你的阶段性成果", "完成 30 天打卡挑战后，欢迎在社交平台带标签 #TokyoFlow 分享你的进步。")
    ]
    for i, (c_title, c_desc) in enumerate(comm_bullets):
        cy = 2430 + i * 200
        draw.rectangle([(180, cy), (2300, cy + 160)], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        draw.text((210, cy + 25), c_title, fill=(29, 78, 216), font=get_font(25))
        draw_wrapped_text(draw, c_desc, get_font(22), (51, 65, 85), 210, cy + 75, 2060, line_spacing=6)
        
    draw.text((180, 3170), "TokyoFlow 日语实景精讲  -  告别死板教科书，每天沉浸式掌握地道日语。", fill=(100, 116, 139), font=get_font(24))
    
    return img

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("==================================================")
    print("Generating Print-Friendly Chinese TokyoFlow PDF")
    print("==================================================")
    
    p1 = make_page_1()
    p2 = make_page_2()
    p3 = make_page_3()
    p4 = make_page_4()
    
    pdf_path = OUT_DIR / "TokyoFlow_日语实景精讲_官方学习指南与进阶大纲.pdf"
    
    p1.save(
        pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=[p2, p3, p4]
    )
    
    print(f"\n[OK] High-Resolution 300 DPI Chinese PDF Created: {pdf_path}")
    print(f"File Size: {pdf_path.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
