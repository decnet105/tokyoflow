#!/usr/bin/env python3
"""
TokyoFlow Japanese • Sunday Mega-Compilation Producer (Chinese Edition)
========================================================================
Automates production of the 28-minute Chinese-localized mega-compilation:
- WM.01: 周一到周五东京生活全景大合集（28分钟超长沉浸精讲）【中文解说版】
- Explainer Voice: zh-CN-YunxiNeural (云希全中文名师精讲)
- Tokyo Standard Voice: ja-JP-NanamiNeural (七海纯正东京原声)
- Covers 7 Major Japanese Scenarios:
  1. 山手线电车与乘车礼仪
  2. 7-Eleven 与全家便利店结账
  3. 居酒屋点单与前菜文化 (お通し)
  4. 秋叶原二次元购物与免税退税
  5. 经典拉面食券机定制与加面 (替玉)
  6. 钱汤温泉入浴五大礼仪
  7. 神社与寺庙参拜礼仪 (二礼二拍手一礼)
- High-CTR 16:9 Master Chinese Cover & 9:16 Shorts Cover (Zero Emoji Discipline)
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import pykakasi

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
kakasi_inst = pykakasi.kakasi()

def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

# ==========================================
# MASTER COMPILATION METADATA (CHINESE EDITION)
# ==========================================
COMPILATION_METADATA_ZH = {
    "series_code": "WM.01",
    "shorts_code": "WS.01",
    "release_folder": "WM01-weekday_survival_mega_compilation-v1.0-zh",
    "title_zh": "周一到周五东京生活全景大合集 + 日本深度文化风俗旅行完全掌握 28分钟精讲",
    "title_ja": "【保存版】月〜金Tokyo日常サバイバル＆日本文化・風俗・旅行完全マスター28分スペシャル",
    "jlpt_level": "JLPT N5-N3",
    "target_duration_mins": 28,
    "district": "东京都全景（新宿、涩谷、秋叶原、浅草、六本木、银座）",
    "description_summary": "28分钟掌握周一到周五全套东京生活实景生存口语（电车、便利店、居酒屋、秋叶原、拉面店、温泉钱汤、神社参拜），融合深度日本文化风俗、出行礼仪与高频对话公式。"
}

MEGA_SCREENPLAY_ZH = [
    # ----------------------------------------------------
    # PROLOGUE: 序章 • 东京生活全景导览 (00:00 - 01:30)
    # ----------------------------------------------------
    {
        "chapter_id": 0,
        "chapter_title": "序章 • 东京生活全景学习导览",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "0_1",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "欢迎来到 TokyoFlow 日语周末大合集特辑。今天，我们将周一到周五的完整东京生活实景口语，浓缩进这堂28分钟的全景深度精讲课中。无论你正在备考 JLPT，还是计划前往日本旅行与生活，本期视频都将成为你最实用的随身日语指南。",
                "duration_est": 21.0,
                "jlpt": "导览"
            },
            {
                "seg_id": "0_2",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "在接下来的28分钟里，我们将精讲七大核心生活场景：山手线乘车报站、便利店收银结账、居酒屋点单交流、秋叶原免税购物、拉面食券定制、温泉钱汤礼仪以及神社寺庙参拜。同时，我们还将深入剖析电车静音模式、鞠躬礼节、零小费原则与极致款待文化。让我们从第一天：山手线电车开始！",
                "duration_est": 27.0,
                "jlpt": "课程大纲"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 1 [周一]: 山手线电车、发车音与电车礼仪 (01:30 - 05:15)
    # ----------------------------------------------------
    {
        "chapter_id": 1,
        "chapter_title": "Day 1 • 山手线电车报站与乘车礼仪",
        "bg_scene": "docs/shared/assets/backgrounds/scene_yamanote_platform.jpg",
        "segments": [
            {
                "seg_id": "1_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周一清晨，东京的脉搏从山手线开始跳动。在站台与车厢内，你最常听到的就是标准广播提示。",
                "duration_est": 10.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "1_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "まもなく、二番線に電車がまいります。黄色い点字ブロックの内側までお下がりください。",
                "furi": "まもなく、 にばんせん に でんしゃ が まいります。 きいろい てんじ ぶろっく の うちがわ まで おさがり ください。",
                "romaji": "Mamonaku, nibansen ni densha ga mairimasu. Kiiroi tenji burokku no uchigawa made osagari kudasai.",
                "meaning": "列车即将到达2号站台，请退至黄色盲道内侧等候。",
                "jlpt": "N4",
                "duration_est": 8.5
            },
            {
                "seg_id": "1_3_breakdown",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "请注意动词 'mairimasu'，这是 'kimasu'（来）的自谦语，体现了铁道公司的极高服务敬意；'osagari kudasai' 则是 'o + 动词连用形 + kudasai' 的高频敬语祈使句型。",
                "duration_est": 15.0,
                "jlpt": "N4 语法精讲"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 2 [周二]: 便利店结账、加热与塑料袋 (05:15 - 09:00)
    # ----------------------------------------------------
    {
        "chapter_id": 2,
        "chapter_title": "Day 2 • 7-Eleven 便利店结账全流程",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "2_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周二走进街头随处可见的 7-Eleven 或全家便利店。在收银台前，店员会连续询问便当加热与塑料袋需求。",
                "duration_est": 11.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "2_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "お弁当温めますか？レジ袋はご利用になりますか？",
                "furi": "おべんとう あたためます か？ れじぶくろ は ごりよう に なります か？",
                "romaji": "Obentou atatamemasu ka? Rejibukuro wa goriyou ni narimasu ka?",
                "meaning": "便当需要加热吗？需要使用塑料袋吗？",
                "jlpt": "N5",
                "duration_est": 7.5
            },
            {
                "seg_id": "2_3_breakdown",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "如果需要加热，直接回答 'Onegaishimasu'；如果不需要塑料袋，最地道的回答是 'Fukuro wa daijoubu desu'（不用了，谢谢）。'Daijoubu desu' 在这里巧妙表达了礼貌拒绝。",
                "duration_est": 16.0,
                "jlpt": "N5 实战应答应答"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 3 [周三]: 居酒屋点单、酒令与前菜文化 (09:00 - 13:00)
    # ----------------------------------------------------
    {
        "chapter_id": 3,
        "chapter_title": "Day 3 • 居酒屋点餐与前菜文化 (お通し)",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "3_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周三夜晚，步入烟火气十足的东京居酒屋。入座后第一件事不是看菜单，而是先点第一杯饮料。",
                "duration_est": 11.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "3_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "とりあえず生ビール二つと、枝豆をお願いします。",
                "furi": "とりあえず なまびーる ふたつ と、 えだまめ を おねがい します。",
                "romaji": "Toriaezu nama biiru futatsu to, edamame o onegai shimasu.",
                "meaning": "先来两杯生啤酒和一份毛豆，谢谢。",
                "jlpt": "N5",
                "duration_est": 7.0
            },
            {
                "seg_id": "3_3_breakdown",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "'Toriaezu' 是居酒屋黄金副词，意思是'总之先来……'。同时请注意桌上主动端上的小菜 'Otoushi'，这是日本居酒屋不成文的席位费文化，通常为300到500日元。",
                "duration_est": 17.0,
                "jlpt": "文化与高频副词"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 4 [周四]: 秋叶原二次元朝圣与免税退税 (13:00 - 17:00)
    # ----------------------------------------------------
    {
        "chapter_id": 4,
        "chapter_title": "Day 4 • 秋叶原二次元购物与免税退税",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "4_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周四来到动漫圣地秋叶原。在友都八喜或手办店结账时，免税是外国游客最核心的交流诉求。",
                "duration_est": 11.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "4_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "免税手続きをお願いできますか？パスポートはこちらです。",
                "furi": "めんぜい てつづき を おねがい できます か？ ぱすぽーと は こちら です。",
                "romaji": "Menzei tetsuzuki o onegai dekimasu ka? Pasupooto wa kochira desu.",
                "meaning": "请问可以办理免税手续吗？这是我的护照。",
                "jlpt": "N4",
                "duration_est": 7.5
            },
            {
                "seg_id": "4_3_breakdown",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "'~o onegai dekimasu ka' 是比 '~kudasai' 更具礼貌色彩的可能形请求句型。日本消费税为10%，单笔消费满5000日元即可出示护照享受当场免税。",
                "duration_est": 16.0,
                "jlpt": "N4 购物敬语"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 5 [周五]: 经典拉面食券机定制 (17:00 - 21:00)
    # ----------------------------------------------------
    {
        "chapter_id": 5,
        "chapter_title": "Day 5 • 拉面食券机定制与加面 (替玉)",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "5_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周五深夜，来到一兰或家系拉面店。在食券机前买好票后，店员会询问你对口味与面条硬度的详细偏好。",
                "duration_est": 11.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "5_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "麺は硬めで、味は濃いめでお願いします。替え玉を一つください。",
                "furi": "めん は かため で、 あじ は こいめ で おねがい します。 かえだま を ひとつ ください。",
                "romaji": "Men wa katame de, aji wa koime de onegai shimasu. Kaedama o hitotsu kudasai.",
                "meaning": "面条要偏硬一点，汤头要浓郁一点，谢谢。请再加一份面。",
                "jlpt": "N5",
                "duration_est": 8.0
            },
            {
                "seg_id": "5_3_breakdown",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "后缀 '~me'（目）表示程度偏向，例如 'katame'（偏硬）、'koime'（偏浓）。博多豚骨拉面中的加面叫做 'Kaedama'，记得留半碗汤再呼叫店员哦。",
                "duration_est": 16.0,
                "jlpt": "饮食定制表达"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 6 [周末 Part 1]: 钱汤温泉入浴五大礼仪 (21:00 - 24:30)
    # ----------------------------------------------------
    {
        "chapter_id": 6,
        "chapter_title": "Weekend Part 1 • 钱汤温泉入浴五大礼仪",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "6_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "周末放松时刻，体验日本传统的钱汤与温泉。入浴前必须严格遵守'先洗净身体再入池'与'毛巾绝不浸入温泉水'等传统规矩。",
                "duration_est": 12.0,
                "jlpt": "文化导入"
            },
            {
                "seg_id": "6_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "湯船に入る前に、必ず体を綺麗に洗ってください。タオルは湯に入れないでください。",
                "furi": "ゆぶね に はいる まえ に、 かならず からだ を きれい に あらって ください。 たおる は ゆ に いれないで ください。",
                "romaji": "Yubune ni hairu mae ni, kanarazu karada o kirei ni aratte kudasai. Taoru wa yu ni irenaide kudasai.",
                "meaning": "进入浴池之前，请务必将身体彻底清洗干净。毛巾请勿浸入浴池中。",
                "jlpt": "N4",
                "duration_est": 9.0
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 7 [周末 Part 2]: 神社与寺庙参拜礼仪 (24:30 - 27:00)
    # ----------------------------------------------------
    {
        "chapter_id": 7,
        "chapter_title": "Weekend Part 2 • 神社寺庙参拜礼仪 (二礼二拍手)",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "7_1_intro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "漫步浅草寺或明治神宫。参拜神道教神社的标准仪式是'二礼二拍手一礼'，投币时推荐使用5日元硬币（音同'有缘'）。",
                "duration_est": 13.0,
                "jlpt": "文化导入"
            },
            {
                "seg_id": "7_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "お賽銭を入れて、二礼二拍手一礼の作法で参拝します。",
                "furi": "おさいせん を いれて、 にれい にはくしゅ いちれい の さほう で さんぱい します。",
                "romaji": "Osaisen o irete, nirei nihakushu ichirei no sahou de sanpai shimasu.",
                "meaning": "投入香油钱后，按照两次鞠躬、两次击掌、最后一次鞠躬的礼法进行参拜。",
                "jlpt": "N3",
                "duration_est": 8.5
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 8: 终章 • 总结与复习 (27:00 - 28:00)
    # ----------------------------------------------------
    {
        "chapter_id": 8,
        "chapter_title": "终章 • 学习总结与复习展望",
        "bg_scene": "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "8_1_outro",
                "type": "narration",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "恭喜你完成了整整28分钟的东京生活全景精讲特训！从电车到便利店，从居酒屋到温泉神宫，你已经系统掌握了东京日常所需的全部核心口语与文化礼节。欢迎访问 TokyoFlow 官网下载完整词汇讲义。点赞订阅，开启你的地道日语之旅！",
                "duration_est": 22.0,
                "jlpt": "结语"
            }
        ]
    }
]

# ==========================================
# METADATA GENERATION
# ==========================================

def build_metadata_md_zh(output_dir: str):
    meta_path = os.path.join(output_dir, "metadata.md")
    title = f"【JLPT N5-N3】周一到周五东京生活全景大合集（WM.01）| 电车·便利店·居酒屋·秋叶原·拉面·温泉全场景28分钟精讲"
    description = f"""【TokyoFlow 日语实景大合集 • 中文解说版】
大合集专集编号：WM.01
短视频跟读编号：WS.01
JLPT 难度跨度：[JLPT N5] ~ [JLPT N3]

28分钟完整掌握周一到周五东京日常实景全场景日语口语！涵盖山手线电车、7-Eleven便利店、居酒屋、秋叶原免税购物、拉面食券机定制、温泉钱汤入浴五大守则以及神社寺庙参拜礼法。

【课程时间轴目录】
00:00 - 序章 • 东京生活全景学习导览
01:30 - Day 1 • 山手线电车报站与乘车礼仪（黄色盲道、自谦语 mairimasu）
05:15 - Day 2 • 7-Eleven 便利店结账全流程（便当加热、塑料袋礼貌拒绝）
09:00 - Day 3 • 居酒屋点餐与前菜文化（Toriaezu 黄金副词、席位小菜 Otoushi）
13:00 - Day 4 • 秋叶原二次元购物与免税退税（Menzei 护照退税流程）
17:00 - Day 5 • 拉面食券机定制与加面（面条硬度、汤头浓淡、替玉 Kaedama）
21:00 - Weekend Part 1 • 钱汤温泉入浴五大礼仪（洗净身体、毛巾规则）
24:30 - Weekend Part 2 • 神社寺庙参拜礼仪（手水舍洗手、二礼二拍手一礼）
27:00 - 终章 • 学习总结与复习展望

【核心场景与高频语法】
- [JLPT N5]：お + 动词ます形词干 + ください (标准敬语祈使)
- [JLPT N5]：~は大丈夫です (便利店与日常委婉礼貌拒绝)
- [JLPT N4]：~ていただく / ~お願いいできますか (客气请求可能形)
- [JLPT N3]：二礼二拍手一礼作法、自谦语与尊他语日常切换

【TokyoFlow 官方学习平台】
访问 TokyoFlow 官方网站下载完整讲义与配套词汇卡：
https://tokyoflow.app/

【检索标签】
日语学习, 东京生活, 日本旅游日语, JLPT N5, JLPT N4, JLPT N3, 山手线, 便利店日语, 居酒屋日语, 拉面定制, 温泉礼仪, 日本文化, TokyoFlow, 日语听力, 日语口语, 日语入门"""

    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"# YouTube 视频标题\n```\n{title}\n```\n\n# YouTube 视频简介\n```\n{description}\n```\n")
    print(f"  [OK] 保存中文版大合集元数据: {meta_path}")

def build_script_json_zh(output_dir: str):
    script_path = os.path.join(output_dir, "script.json")
    out_obj = {
        "metadata": COMPILATION_METADATA_ZH,
        "screenplay": MEGA_SCREENPLAY_ZH
    }
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)
    print(f"  [OK] 保存中文版大合集剧本: {script_path}")

# ==========================================
# THUMBNAIL ENGINE (16:9 & 9:16 CHINESE EDITION)
# ==========================================

def render_master_thumbnail_zh(output_dir: str):
    """Generates 16:9 Golden Master Landscape Thumbnail in Chinese conforming to Zero Emoji Discipline."""
    width, height = 1920, 1080
    bg_path = "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg"
    if not os.path.exists(bg_path):
        bg_path = "docs/shared/assets/backgrounds/scene_yamanote_platform.jpg"

    base = Image.open(bg_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    import math
    for x in range(1200):
        alpha = int(250 * 0.5 * (1 + math.cos(math.pi * x / 1200)))
        draw_ov.line([(x, 0), (x, height)], fill=(10, 15, 28, alpha))

    for y in range(820, height):
        alpha = int(220 * (y - 820) / (height - 820))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    img = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left White Brand Pill
    draw.rounded_rectangle([(60, 45), (450, 105)], radius=18, fill=(255, 255, 255))
    draw.text((85, 58), "TokyoFlow 日语实景", fill=(225, 29, 72), font=get_font(26))

    # 2. Top-Right Crimson Series Badge
    badge_str = "【JLPT N5-N3】WM.01 大合集"
    draw.rounded_rectangle([(width - 450, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 425, 58), badge_str, fill=(255, 255, 255), font=get_font(24))

    # 3. Giant 3D Solar Yellow Hook
    font_hook = get_font(92)
    hook_lines = ["东京日常", "全景大课"]
    hy = 145
    for line in hook_lines:
        for ox, oy in [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((60 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 110

    draw.text((65, 375), "周一至周五实景全覆盖 + 日本深度文化礼仪", fill=(244, 114, 182), font=get_font(32))

    # 4. Glassmorphic Japanese Learning Card
    card_y = 435
    card_w = 880
    draw.rounded_rectangle([(60, card_y), (60 + card_w, card_y + 430)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    draw.text((90, card_y + 25), "[ 周末特辑 • 全景沉浸特训营 ]", fill=(56, 189, 248), font=get_font(22))

    font_jp_quote = get_font(34)
    draw.text((90, card_y + 70), "月-金 Tokyo 日常サバイバル &", fill=(255, 255, 255), font=font_jp_quote)
    draw.text((90, card_y + 115), "日本文化・风俗・旅行完全掌握！", fill=(254, 240, 138), font=font_jp_quote)

    draw.text((90, card_y + 180), "• 山手线报站、便利店结账、居酒屋点单、秋叶原退税、拉面定制、钱汤温泉", fill=(244, 114, 182), font=get_font(22))
    draw.text((90, card_y + 225), "• 40+ 高频实用口语句型与毫秒级卡拉OK跟读", fill=(226, 232, 240), font=get_font(22))
    draw.text((90, card_y + 270), "• 礼貌振动模式、鞠躬角度、零小费文化与极致款待之道", fill=(148, 163, 184), font=get_font(21))
    draw.text((90, card_y + 315), "• 纯正东京原声 (Nanami) + 云希全中文名师语法拆解", fill=(56, 189, 248), font=get_font(21))
    draw.text((90, card_y + 360), "• 28分钟超长周末沉浸式大合集", fill=(254, 240, 138), font=get_font(21))

    # 5. Full-Width Crimson Conversion Ribbon
    draw.rounded_rectangle([(60, height - 115), (width - 60, height - 40)], radius=16, fill=(225, 29, 72))
    draw.text((90, height - 93), " 100% 纯正东京原声  •  40+ 实用口语公式  •  28分钟全景深度特训", fill=(255, 255, 255), font=get_font(24))

    thumb_out = os.path.join(output_dir, "thumbnail.jpg")
    img.save(thumb_out, quality=95)
    print(f"  [OK] 保存 16:9 中文大合集封面: {thumb_out}")

    # Sync to assets
    asset_sync = os.path.join("assets/thumbnails", "WM01-weekday_survival_mega_compilation_zh_thumb.jpg")
    img.save(asset_sync, quality=95)
    site_sync = os.path.join("site/assets/thumbnails", "WM01-weekday_survival_mega_compilation_zh_thumb.jpg")
    os.makedirs(os.path.dirname(site_sync), exist_ok=True)
    img.save(site_sync, quality=95)
    docs_sync = os.path.join("docs/site/assets/thumbnails", "WM01-weekday_survival_mega_compilation_zh_thumb.jpg")
    os.makedirs(os.path.dirname(docs_sync), exist_ok=True)
    img.save(docs_sync, quality=95)
    print(f"  [OK] 同步至站点封面库: {asset_sync}")

def render_shorts_thumbnail_zh(output_dir: str):
    """Generates 9:16 Golden Master Vertical Shorts Cover in Chinese."""
    width, height = 1080, 1920
    bg_path = "docs/shared/assets/backgrounds/scene_yamanote_platform.jpg"
    if not os.path.exists(bg_path):
        bg_path = "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg"

    base = Image.open(bg_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    for y in range(450):
        alpha = int(230 * (1 - y / 450))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    for y in range(1050, height):
        alpha = int(245 * min(1.0, (y - 1050) / 200))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    img = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(40, 50), (450, 115)], radius=16, fill=(255, 255, 255))
    draw.text((65, 65), "TokyoFlow 日语实景", fill=(225, 29, 72), font=get_font(26))

    draw.rounded_rectangle([(width - 380, 50), (width - 40, 115)], radius=16, fill=(225, 29, 72))
    draw.text((width - 355, 65), "WS.01 • JLPT N5-N3", fill=(255, 255, 255), font=get_font(24))

    font_hook = get_font(72)
    hook_lines = ["东京日常", "周末大合集"]
    hy = 155
    for line in hook_lines:
        for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((40 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((40, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 85

    draw.text((45, 335), "周一到周五全景生活 + 深度日本文化", fill=(244, 114, 182), font=get_font(26))

    card_y = 1120
    draw.rounded_rectangle([(40, card_y), (width - 40, 1640)], radius=24, fill=(10, 15, 28, 245), outline=(56, 189, 248), width=3)
    draw.text((70, card_y + 25), "[ 东京实景特训营 • 中文解说大合集 ]", fill=(56, 189, 248), font=get_font(22))

    draw.text((70, card_y + 70), "月-金 Tokyo サバイバル & 日本文化", fill=(255, 255, 255), font=get_font(36))
    draw.text((70, card_y + 120), "5天全场景沉浸精讲课", fill=(254, 240, 138), font=get_font(30))

    draw.text((70, card_y + 180), "• 电车 • 便利店 • 居酒屋 • 秋叶原 • 拉面", fill=(244, 114, 182), font=get_font(26))
    draw.text((70, card_y + 225), "• 钱汤温泉 5大入浴礼仪逐条拆解", fill=(226, 232, 240), font=get_font(24))
    draw.text((70, card_y + 270), "• 振动模式、鞠躬角度与零小费文化", fill=(148, 163, 184), font=get_font(22))
    draw.text((70, card_y + 315), "• 100% 东京原声（Nanami）+ 云希中文名师精讲", fill=(56, 189, 248), font=get_font(22))

    draw.rounded_rectangle([(40, 1660), (width - 40, 1840)], radius=18, fill=(225, 29, 72))
    draw.text((70, 1690), "观看 28分钟 完整大课 (WM.01)", fill=(255, 255, 255), font=get_font(32))
    draw.text((70, 1745), "40+ 实用句型公式 • 语法深度拆解 • 日本文化秘籍", fill=(254, 240, 138), font=get_font(24))

    short_thumb_out = os.path.join(output_dir, "short_thumbnail.jpg")
    img.save(short_thumb_out, quality=95)
    print(f"  [OK] 保存 9:16 中文短片封面: {short_thumb_out}")

# ==========================================
# AUDIO SYNTHESIS ENGINE (CHINESE EDITION)
# ==========================================

async def synthesize_audio_segment_zh(seg: dict, audio_dir: str):
    seg_id = seg["seg_id"]
    voice = seg["voice"]
    content = seg["content"]
    out_mp3 = os.path.join(audio_dir, f"seg_{seg_id}.mp3")

    if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
        return out_mp3

    rate = "-5%" if seg.get("lang") == "ja" else "+0%"
    communicate = edge_tts.Communicate(content, voice, rate=rate)
    await communicate.save(out_mp3)
    return out_mp3

async def synthesize_all_audio_tracks_zh(output_dir: str):
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    print("\n 合成双语配音音轨（Nanami 日语原声 + 云希 中文名师讲解）...")

    tasks = []
    for ch in MEGA_SCREENPLAY_ZH:
        for seg in ch["segments"]:
            tasks.append(synthesize_audio_segment_zh(seg, audio_dir))

    await asyncio.gather(*tasks)
    print(f"  [OK] 全部中文版音频合成完毕: {len(tasks)} 段音频")

# ==========================================
# MAIN ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: WM.01 周一到周五生活大合集【中文解说版】生产管线")
    print(f" 编号: {COMPILATION_METADATA_ZH['series_code']} • 预估时长: {COMPILATION_METADATA_ZH['target_duration_mins']} 分钟")
    print("================================================================================")

    output_dir = os.path.join("docs/youtube_releases", "WM01-weekday_survival_mega_compilation-v1.0-zh")
    os.makedirs(output_dir, exist_ok=True)

    # 1. 渲染中文字幕封面 (16:9 & 9:16)
    render_master_thumbnail_zh(output_dir)
    render_shorts_thumbnail_zh(output_dir)

    # 2. 生成中文元数据与剧本文件
    build_metadata_md_zh(output_dir)
    build_script_json_zh(output_dir)

    # 3. 合成中文配音与原声音轨
    await synthesize_all_audio_tracks_zh(output_dir)

    print("\n================================================================================")
    print(f" WM.01 中文版发布套件全部生成完成: {output_dir}")
    print("================================================================================")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
