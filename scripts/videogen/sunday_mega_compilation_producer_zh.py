#!/usr/bin/env python3
"""
TokyoFlow Japanese • Sunday Mega-Compilation Producer (Chinese Edition)
========================================================================
Automates production of the Chinese-localized mega-compilation:
- WL.02 / WM.01: 周一到周五东京生活全景大合集（实景精讲）【中文解说版】
- 100% Authentic 4K Real Tokyo Photography (Zero AI Cartoon / Zero Clutter)
- 3-Tier Ruby Typography & Millisecond Word-by-Word Glowing Yellow Karaoke
- Continuous Practice: Stage 1 原声示范 + Stage 2 影子跟读练读（原声领读，中间不停顿）
- Dual-Voice Role Separation: Nanami JA @ Tokyo Native + Yunxi ZH @ Chinese Masterclass
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
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import edge_tts
import pykakasi

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "videogen"))
from seamless_tts_engine import (
    synthesize_seamless_bilingual_audio,
    normalize_chinese_speech_text,
    get_audio_duration
)
from timing_engine import (
    extract_tokens_from_text,
    align_sentence_tokens_with_audio
)

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
    "series_code": "WL.02",
    "legacy_code": "WM.01",
    "shorts_code": "WS.02",
    "release_folder": "WM01-weekday_survival_mega_compilation-v1.0-zh",
    "title_zh": "【JLPT N5-N3】WL.02 周一到周五东京生活全景大合集 | 电车·便利店·居酒屋·秋叶原·拉面·温泉全场景28分钟精讲",
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
                "character": "云希",
                "lang": "zh",
                "content": "欢迎来到 TokyoFlow 日语周末大合集特辑。今天，我们将周一到周五的完整东京生活实景口语，浓缩进这堂全景深度精讲课中。无论你正在备考 JLPT，还是计划前往日本旅行与生活，本期视频都将成为你最实用的随身日语指南。",
                "speech_chunks": [
                    {"lang": "zh", "text": "欢迎来到 TokyoFlow 日语周末大合集特辑。今天，我们将周一到周五的完整东京生活实景口语，浓缩进这堂全景深度精讲课中。无论你正在备考 JLPT，还是计划前往日本旅行与生活，本期视频都将成为你最实用的随身日语指南。"}
                ],
                "duration_est": 21.0,
                "jlpt": "导览"
            },
            {
                "seg_id": "0_2",
                "type": "narration",
                "character": "云希",
                "lang": "zh",
                "content": "我们将精讲七大核心生活场景：山手线电车报站、便利店收银结账、居酒屋点单交流、秋叶原免税购物、拉面食券定制、温泉钱汤礼仪以及神社寺庙参拜。同时，深入剖析电车静音模式、鞠躬礼节、零小费原则与极致款待文化。让我们从第一天：山手线电车开始！",
                "speech_chunks": [
                    {"lang": "zh", "text": "我们将精讲七大核心生活场景：山手线电车报站、便利店收银结账、居酒屋点单交流、秋叶原免税购物、拉面食券定制、温泉钱汤礼仪以及神社寺庙参拜。同时，深入剖析电车静音模式、鞠躬礼节、零小费原则与极致款待文化。让我们从第一天：山手线电车开始！"}
                ],
                "duration_est": 25.0,
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
                "character": "云希",
                "lang": "zh",
                "content": "周一清晨，东京的脉搏从山手线开始跳动。在站台与车厢内，你最常听到的就是标准广播提示。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周一清晨，东京的脉搏从山手线开始跳动。在站台与车厢内，你最常听到的就是标准广播提示。"}
                ],
                "duration_est": 9.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "1_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "まもなく、二番線に電車がまいります。黄色い点字ブロックの内側までお下がりください。",
                "furi": "まもなく、 にばんせん に でんしゃ が まいります。 きいろい てんじ ぶろっく の うちがわ まで おさがり ください。",
                "romaji": "Mamonaku, nibansen ni densha ga mairimasu. Kiiroi tenji burokku no uchigawa made osagari kudasai.",
                "meaning": "列车即将到达2号站台，请退至黄色盲道内侧等候。",
                "tokens": [
                    {"orig": "まもなく", "kana": "まもなく", "romaji": "mamonaku"},
                    {"orig": "二番線に", "kana": "にばんせんに", "romaji": "nibansen ni"},
                    {"orig": "電車が", "kana": "でんしゃが", "romaji": "densha ga"},
                    {"orig": "まいります", "kana": "まいります", "romaji": "mairimasu"},
                    {"orig": "黄色い", "kana": "きいろい", "romaji": "kiiroi"},
                    {"orig": "点字ブロックの", "kana": "てんじぶろっくの", "romaji": "tenji burokku no"},
                    {"orig": "内側まで", "kana": "うちがわまで", "romaji": "uchigawa made"},
                    {"orig": "お下がりください", "kana": "おさがりください", "romaji": "osagari kudasai"}
                ],
                "jlpt": "N4",
                "duration_est": 18.0
            },
            {
                "seg_id": "1_3_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "请注意动词 'mairimasu'，这是 'kimasu'（来）的自谦语，体现了铁道公司的极高服务敬意；'osagari kudasai' 则是 'o + 动词连用形 + kudasai' 的高频敬语祈使句型。",
                "ref_sentence": "まもなく、二番線に電車がまいります。黄色い点字ブロックの内側までお下がりください。",
                "vocab": [
                    {"orig": "まもなく", "kana": "まもなく", "romaji": "mamonaku", "pos": "副词 (N4)", "meaning": "不久 / 马上"},
                    {"orig": "参る", "kana": "まいる", "romaji": "mairu", "pos": "自谦动词 (N3)", "meaning": "来（自谦敬语）"},
                    {"orig": "点字ブロック", "kana": "てんじぶろっく", "romaji": "tenji burokku", "pos": "名词 (N3)", "meaning": "盲道导盲砖"},
                    {"orig": "下がる", "kana": "さがる", "romaji": "sagaru", "pos": "动词 (N4)", "meaning": "后退 / 退后"}
                ],
                "grammar_title": "自谦动词 参る (Mairu) 与 敬语祈使句型",
                "grammar_bullets": [
                    ("• 自谦动词 参ります", "まいります 是 きます 的自谦形式，日本铁路与公共广播的标准用语"),
                    ("• 敬语祈使句型", "お + 动词ます形词干 + ください (お下がりください = 请向后退)"),
                    ("• 盲道安全提示", "黄色い点字ブロックの内側 (黄色盲道内侧安全区域)")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "请注意动词"},
                    {"lang": "ja", "text": "まいります"},
                    {"lang": "zh", "text": "，这是"},
                    {"lang": "ja", "text": "きます"},
                    {"lang": "zh", "text": "（来）的自谦语，体现了铁道公司的极高服务敬意；而"},
                    {"lang": "ja", "text": "お下がりください"},
                    {"lang": "zh", "text": "则是"},
                    {"lang": "ja", "text": "お"},
                    {"lang": "zh", "text": "加动词连用形加"},
                    {"lang": "ja", "text": "ください"},
                    {"lang": "zh", "text": "的高频敬语祈使句型。"}
                ],
                "duration_est": 16.0,
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
                "character": "云希",
                "lang": "zh",
                "content": "周二走进街头随处可见的 7-Eleven 或全家便利店。在收银台前，店员会连续询问便当加热与塑料袋需求。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周二走进街头随处可见的 7-Eleven 或全家便利店。在收银台前，店员会连续询问便当加热与塑料袋需求。"}
                ],
                "duration_est": 10.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "2_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "お弁当温めますか？レジ袋はご利用になりますか？",
                "furi": "おべんとう あたためます か？ れじぶくろ は ごりよう に なります か？",
                "romaji": "Obentou atatamemasu ka? Rejibukuro wa goriyou ni narimasu ka?",
                "meaning": "便当需要加热吗？需要使用塑料袋吗？",
                "tokens": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou"},
                    {"orig": "温めますか", "kana": "あたためますか", "romaji": "atatamemasu ka"},
                    {"orig": "レジ袋は", "kana": "れじぶくろは", "romaji": "rejibukuro wa"},
                    {"orig": "ご利用に", "kana": "ごりように", "romaji": "goriyou ni"},
                    {"orig": "なりますか", "kana": "なりますか", "romaji": "narimasu ka"}
                ],
                "jlpt": "N5",
                "duration_est": 16.0
            },
            {
                "seg_id": "2_3_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "如果需要加热，直接回答 'Onegaishimasu'；如果不需要塑料袋，最地道的回答是 'Fukuro wa daijoubu desu'（不用了，谢谢）。'Daijoubu desu' 在这里巧妙表达了礼貌拒绝。",
                "ref_sentence": "お弁当温めますか？レジ袋はご利用になりますか？",
                "vocab": [
                    {"orig": "温める", "kana": "あたためる", "romaji": "atatameru", "pos": "动词 (N5)", "meaning": "加热 / 热一下"},
                    {"orig": "レジ袋", "kana": "れじぶくろ", "romaji": "rejibukuro", "pos": "名词 (N5)", "meaning": "收银塑料袋"},
                    {"orig": "ご利用", "kana": "ごりよう", "romaji": "goriyou", "pos": "尊他名词 (N4)", "meaning": "使用（敬语）"},
                    {"orig": "大丈夫", "kana": "だいじょうぶ", "romaji": "daijoubu", "pos": "形容词 (N5)", "meaning": "不用/没关系"}
                ],
                "grammar_title": "便利店应答秘籍: お願いします 与 大丈夫です",
                "grammar_bullets": [
                    ("• 确认加热", "お願いします (onegai shimasu = 麻烦加热)"),
                    ("• 委婉拒绝塑料袋", "袋は大丈夫です (fukuro wa daijoubu desu = 塑料袋不用了，谢谢)"),
                    ("• 尊他敬语格式", "ご + 汉字词 + になる (ご利用になります = 您使用吗)")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "如果需要加热，直接回答"},
                    {"lang": "ja", "text": "お願いします"},
                    {"lang": "zh", "text": "；如果不需要塑料袋，最地道的回答是"},
                    {"lang": "ja", "text": "袋は大丈夫です"},
                    {"lang": "zh", "text": "（不用了，谢谢）。这里的"},
                    {"lang": "ja", "text": "大丈夫です"},
                    {"lang": "zh", "text": "巧妙表达了礼貌拒绝。"}
                ],
                "duration_est": 16.0,
                "jlpt": "N5 实战应答"
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
                "character": "云希",
                "lang": "zh",
                "content": "周三夜晚，步入烟火气十足的东京居酒屋。入座后第一件事不是看菜单，而是先点第一杯饮料。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周三夜晚，步入烟火气十足的东京居酒屋。入座后第一件事不是看菜单，而是先点第一杯饮料。"}
                ],
                "duration_est": 10.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "3_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "とりあえず生ビール二つと、枝豆をお願いします。",
                "furi": "とりあえず なまびーる ふたつ と、 えだまめ を おねがい します。",
                "romaji": "Toriaezu nama biiru futatsu to, edamame o onegai shimasu.",
                "meaning": "先来两杯生啤酒和一份毛豆，谢谢。",
                "tokens": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu"},
                    {"orig": "生ビール", "kana": "なまびーる", "romaji": "nama biiru"},
                    {"orig": "二つと", "kana": "ふたつと", "romaji": "futatsu to"},
                    {"orig": "枝豆を", "kana": "えだまめを", "romaji": "edamame o"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu"}
                ],
                "jlpt": "N5",
                "duration_est": 15.0
            },
            {
                "seg_id": "3_3_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "'Toriaezu' 是居酒屋黄金副词，意思是'总之先来……'。同时请注意桌上主动端上的席位小菜 'Otoushi'，这是日本居酒屋不成文的席位费文化，通常为300到500日元。",
                "ref_sentence": "とりあえず生ビール二つと、枝豆をお願いします。",
                "vocab": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "pos": "副词 (N4)", "meaning": "总之先 / 首先"},
                    {"orig": "生ビール", "kana": "なまびーる", "romaji": "nama biiru", "pos": "名词 (N5)", "meaning": "生啤酒"},
                    {"orig": "枝豆", "kana": "えだまめ", "romaji": "edamame", "pos": "名词 (N5)", "meaning": "毛豆"},
                    {"orig": "お通し", "kana": "おとおし", "romaji": "otooshi", "pos": "文化名词", "meaning": "居酒屋开胃小菜 / 席位小菜"}
                ],
                "grammar_title": "居酒屋黄金暗号: とりあえず 与 席位小菜文化",
                "grammar_bullets": [
                    ("• 居酒屋开场暗号", "とりあえず生で (toriaezu nama de = 先来生啤，全日本居酒屋通用)"),
                    ("• 数量词点餐句型", "名词 + 数量 (一つ/二つ) + を + お願いします"),
                    ("• 席位小菜文化 (お通し)", "居酒屋固定席位前菜，代表座位费与款待，结账时自动包含")
                ],
                "speech_chunks": [
                    {"lang": "ja", "text": "とりあえず"},
                    {"lang": "zh", "text": "是居酒屋黄金副词，意思是总之先来。同时请注意桌上主动端上的席位小菜"},
                    {"lang": "ja", "text": "お通し"},
                    {"lang": "zh", "text": "，这是日本居酒屋不成文的席位费文化，通常为300到500日元。"}
                ],
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
                "character": "云希",
                "lang": "zh",
                "content": "周四来到动漫圣地秋叶原。在友都八喜或手办店结账时，免税是外国游客最核心的交流诉求。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周四来到动漫圣地秋叶原。在友都八喜或手办店结账时，免税是外国游客最核心的交流诉求。"}
                ],
                "duration_est": 10.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "4_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "免税手続きをお願いできますか？パスポートはこちらです。",
                "furi": "めんぜい てつづき を おねがい できます か？ ぱすぽーと は こちら です。",
                "romaji": "Menzei tetsuzuki o onegai dekimasu ka? Pasupooto wa kochira desu.",
                "meaning": "请问可以办理免税手续吗？这是我的护照。",
                "tokens": [
                    {"orig": "免税手続きを", "kana": "めんぜいてつづきを", "romaji": "menzei tetsuzuki o"},
                    {"orig": "お願い", "kana": "おねがい", "romaji": "onegai"},
                    {"orig": "できますか", "kana": "できますか", "romaji": "dekimasu ka"},
                    {"orig": "パスポートは", "kana": "ぱすぽーとは", "romaji": "pasupooto wa"},
                    {"orig": "こちらです", "kana": "こちらです", "romaji": "kochira desu"}
                ],
                "jlpt": "N4",
                "duration_est": 16.0
            },
            {
                "seg_id": "4_3_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "'~o onegai dekimasu ka' 是比 '~kudasai' 更具礼貌色彩的可能形请求句型。日本消费税为10%，单笔消费满5000日元即可出示护照享受当场免税。",
                "ref_sentence": "免税手続きをお願いできますか？パスポートはこちらです。",
                "vocab": [
                    {"orig": "免税", "kana": "めんぜい", "romaji": "menzei", "pos": "名词 (N4)", "meaning": "免税 (Tax Free)"},
                    {"orig": "手続き", "kana": "てつづき", "romaji": "tetsuzuki", "pos": "名词 (N4)", "meaning": "手续 / 办理流程"},
                    {"orig": "パスポート", "kana": "ぱすぽーと", "romaji": "pasupooto", "pos": "外来语 (N5)", "meaning": "护照"},
                    {"orig": "こちら", "kana": "こちら", "romaji": "kochira", "pos": "代词 (N5)", "meaning": "这里 / 这边（敬语）"}
                ],
                "grammar_title": "可能形礼貌请求: お願いできますか 与 免税规则",
                "grammar_bullets": [
                    ("• 极具礼貌的请求句型", "お + 动词连用形 + できますか (比 ください 更委婉谦和)"),
                    ("• 递交物品礼仪", "パスポートはこちらです (出示护照并双手递上)"),
                    ("• 免税门槛", "单店消费满 5000 日元（不含税）即可享受 10% 消费税减免")
                ],
                "speech_chunks": [
                    {"lang": "ja", "text": "をお願いできますか"},
                    {"lang": "zh", "text": "是比"},
                    {"lang": "ja", "text": "ください"},
                    {"lang": "zh", "text": "更具礼貌色彩的可能形请求句型。日本消费税为10%，单笔消费满5000日元即可出示护照享受当场免税。"}
                ],
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
                "character": "云希",
                "lang": "zh",
                "content": "周五深夜，来到一兰或家系拉面店。在食券机前买好票后，店员会询问你对口味与面条硬度的详细偏好。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周五深夜，来到一兰或家系拉面店。在食券机前买好票后，店员会询问你对口味与面条硬度的详细偏好。"}
                ],
                "duration_est": 10.0,
                "jlpt": "场景引入"
            },
            {
                "seg_id": "5_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "麺は硬めで、味は濃いめでお願いします。替え玉を一つください。",
                "furi": "めん は かため で、 あじ は こいめ で おねがい します。 かえだま を ひとつ ください。",
                "romaji": "Men wa katame de, aji wa koime de onegai shimasu. Kaedama o hitotsu kudasai.",
                "meaning": "面条要偏硬一点，汤头要浓郁一点，谢谢。请再加一份面。",
                "tokens": [
                    {"orig": "麺は", "kana": "めんは", "romaji": "men wa"},
                    {"orig": "硬めで", "kana": "かためで", "romaji": "katame de"},
                    {"orig": "味は", "kana": "あじは", "romaji": "aji wa"},
                    {"orig": "濃いめで", "kana": "こいめで", "romaji": "koime de"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegai shimasu"},
                    {"orig": "替え玉を", "kana": "かえだまを", "romaji": "kaedama o"},
                    {"orig": "一つください", "kana": "ひとつください", "romaji": "hitotsu kudasai"}
                ],
                "jlpt": "N5",
                "duration_est": 18.0
            },
            {
                "seg_id": "5_3_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "后缀 '~me'（目）表示程度偏向，例如 'katame'（偏硬）、'koime'（偏浓）。博多豚骨拉面中的加面叫做 'Kaedama'，记得留半碗汤再呼叫店员哦。",
                "ref_sentence": "麺は硬めで、味は濃いめでお願いします。替え玉を一つください。",
                "vocab": [
                    {"orig": "硬め", "kana": "かため", "romaji": "katame", "pos": "形容词后缀 (N5)", "meaning": "偏硬一点"},
                    {"orig": "濃いめ", "kana": "こいめ", "romaji": "koime", "pos": "形容词后缀 (N5)", "meaning": "偏浓郁一点"},
                    {"orig": "替え玉", "kana": "かえだま", "romaji": "kaedama", "pos": "拉面专有名词", "meaning": "加一份拉面条"},
                    {"orig": "食券", "kana": "しょっけん", "romaji": "shokken", "pos": "名词 (N5)", "meaning": "自动贩卖食券"}
                ],
                "grammar_title": "拉面定制公式: 后缀 ~め (偏向) 与 替え玉 加面",
                "grammar_bullets": [
                    ("• 程度偏向后缀 〜め", "硬め (katame = 偏硬), 柔らかめ (yawarakame = 偏软), 濃いめ (koime = 偏浓)"),
                    ("• 替玉加面文化", "博多拉面特色：吃完面条保留汤底，喊 'すいません、替え玉！'"),
                    ("• 食券机流程", "先投币再按按钮，入座后直接将食券放在柜台上方")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "后缀"},
                    {"lang": "ja", "text": "目"},
                    {"lang": "zh", "text": "表示程度偏向，例如"},
                    {"lang": "ja", "text": "硬め"},
                    {"lang": "zh", "text": "（偏硬）、"},
                    {"lang": "ja", "text": "濃いめ"},
                    {"lang": "zh", "text": "（偏浓）。博多豚骨拉面中的加面叫做"},
                    {"lang": "ja", "text": "替え玉"},
                    {"lang": "zh", "text": "，记得留半碗汤再呼叫店员哦。"}
                ],
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
                "character": "云希",
                "lang": "zh",
                "content": "周末放松时刻，体验日本传统的钱汤与温泉。入浴前必须严格遵守'先洗净身体再入池'与'毛巾绝不浸入温泉水'等传统规矩。",
                "speech_chunks": [
                    {"lang": "zh", "text": "周末放松时刻，体验日本传统的钱汤与温泉。入浴前必须严格遵守先洗净身体再入池与毛巾绝不浸入温泉水等传统规矩。"}
                ],
                "duration_est": 11.0,
                "jlpt": "文化导入"
            },
            {
                "seg_id": "6_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "湯船に入る前に、必ず体を綺麗に洗ってください。タオルは湯に入れないでください。",
                "furi": "ゆぶね に はいる まえ に、 かならず からだ を きれい に あらって ください。 たおる は ゆ に いれないで ください。",
                "romaji": "Yubune ni hairu mae ni, kanarazu karada o kirei ni aratte kudasai. Taoru wa yu ni irenaide kudasai.",
                "meaning": "进入浴池之前，请务必将身体彻底清洗干净。毛巾请勿浸入浴池中。",
                "tokens": [
                    {"orig": "湯船に", "kana": "ゆぶねに", "romaji": "yubune ni"},
                    {"orig": "入る前に", "kana": "はいるまえに", "romaji": "hairu mae ni"},
                    {"orig": "必ず体を", "kana": "かならずからだを", "romaji": "kanarazu karada o"},
                    {"orig": "綺麗に", "kana": "きれいに", "romaji": "kirei ni"},
                    {"orig": "洗ってください", "kana": "あらってください", "romaji": "aratte kudasai"},
                    {"orig": "タオルは", "kana": "たおるは", "romaji": "taoru wa"},
                    {"orig": "湯に", "kana": "ゆに", "romaji": "yu ni"},
                    {"orig": "入れないでください", "kana": "いれないでください", "romaji": "irenaide kudasai"}
                ],
                "jlpt": "N4",
                "duration_est": 20.0
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
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "漫步浅草寺或明治神宫。参拜神道教神社的标准仪式是'二礼二拍手一礼'，投币时推荐使用5日元硬币（音同'有缘'）。",
                "speech_chunks": [
                    {"lang": "zh", "text": "漫步浅草寺或明治神宫。参拜神道教神社的标准仪式是"},
                    {"lang": "ja", "text": "二礼二拍手一礼"},
                    {"lang": "zh", "text": "，投币时推荐使用5日元硬币（音同'有缘'）。"}
                ],
                "duration_est": 12.0,
                "jlpt": "文化导入"
            },
            {
                "seg_id": "7_2_quote",
                "type": "audio_phrase",
                "character": "七海",
                "lang": "ja",
                "content": "お賽銭を入れて、二礼二拍手一礼の作法で参拝します。",
                "furi": "おさいせん を いれて、 にれい にはくしゅ いちれい の さほう で さんぱい します。",
                "romaji": "Osaisen o irete, nirei nihakushu ichirei no sahou de sanpai shimasu.",
                "meaning": "投入香油钱后，按照两次鞠躬、两次击掌、最后一次鞠躬的礼法进行参拜。",
                "tokens": [
                    {"orig": "お賽銭を", "kana": "おさいせんを", "romaji": "osaisen o"},
                    {"orig": "入れて", "kana": "いれて", "romaji": "irete"},
                    {"orig": "二礼二拍手一礼の", "kana": "にれいにはくしゅいちれいの", "romaji": "nirei nihakushu ichirei no"},
                    {"orig": "作法で", "kana": "さほうで", "romaji": "sahou de"},
                    {"orig": "参拝します", "kana": "さんぱいします", "romaji": "sanpai shimasu"}
                ],
                "jlpt": "N3",
                "duration_est": 18.0
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
                "character": "云希",
                "lang": "zh",
                "content": "恭喜你完成了整整28分钟的东京生活全景精讲特训！从电车到便利店，从居酒屋到温泉神宫，你已经系统掌握了东京日常所需的全部核心口语与文化礼节。欢迎访问 TokyoFlow 官网下载完整词汇讲义。点赞订阅，开启你的地道日语之旅！",
                "speech_chunks": [
                    {"lang": "zh", "text": "恭喜你完成了整整28分钟的东京生活全景精讲特训！从电车到便利店，从居酒屋到温泉神宫，你已经系统掌握了东京日常所需的全部核心口语与文化礼节。欢迎访问 TokyoFlow 官网下载完整词汇讲义。点赞订阅，开启你的地道日语之旅！"}
                ],
                "duration_est": 22.0,
                "jlpt": "结语"
            }
        ]
    }
]

# ==========================================
# AUDIO SYNTHESIS & MILLISECOND ALIGNMENT ENGINE
# ==========================================

# In-memory storage for token alignment timings
ALIGNMENT_STORE = {}

async def synthesize_all_audio_tracks_zh(output_dir: str):
    """
    Synthesizes all audio tracks:
    1. Japanese quotes: Two-stage continuous audio (Stage 1 Demo + 0.35s breath + Stage 2 Practice Shadowing Drill)
       with Nanami Tokyo Native voice, perfectly continuous without dead pauses.
    2. Explanations: Seamless bilingual in-line switching between Yunxi (Chinese) and Nanami (Japanese).
    3. Whisper word alignment: Extracts millisecond timestamps for word-by-word karaoke follow-along.
    """
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    temp_dir = "tmp/tts_mega_zh"
    os.makedirs(temp_dir, exist_ok=True)
    print("\n--- 正在合成 WL.02 中文大合集音频轨道 (含两段式连贯跟读练读与毫秒级时间轴) ---")

    for ch in MEGA_SCREENPLAY_ZH:
        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            seg_type = seg.get("type", "narration")
            out_file = os.path.join(audio_dir, f"seg_{seg_id}.mp3")

            if seg_type == "audio_phrase":
                # Two-Stage Continuous Practice Audio:
                # Stage 1: 原声示范 (Native Model Tempo)
                # Stage 2: 跟读练读 (Shadowing Drill Practice Tempo)
                text_ja = seg.get("content", "")
                f_demo = os.path.join(temp_dir, f"seg_{seg_id}_demo.mp3")
                f_drill = os.path.join(temp_dir, f"seg_{seg_id}_drill.mp3")

                # Stage 1 TTS
                comm_demo = edge_tts.Communicate(text_ja, "ja-JP-NanamiNeural", rate="-10%", pitch="+2Hz")
                await comm_demo.save(f_demo)

                # Stage 2 TTS
                comm_drill = edge_tts.Communicate(text_ja, "ja-JP-NanamiNeural", rate="-12%", pitch="+2Hz")
                await comm_drill.save(f_drill)

                # Align Tokens with Whisper for both Stage 1 and Stage 2
                tokens = seg.get("tokens", extract_tokens_from_text(text_ja))
                aligned_demo = align_sentence_tokens_with_audio(f_demo, tokens)
                aligned_drill = align_sentence_tokens_with_audio(f_drill, tokens)

                dur_demo = get_audio_duration(f_demo)
                dur_drill = get_audio_duration(f_drill)
                breath_pause = 0.35

                # Shift Stage 2 timestamps by (dur_demo + breath_pause)
                offset_drill = dur_demo + breath_pause
                aligned_drill_shifted = []
                for tok in aligned_drill:
                    aligned_drill_shifted.append({
                        **tok,
                        "start": tok.get("start", 0.0) + offset_drill,
                        "end": tok.get("end", 0.0) + offset_drill
                    })

                # Store alignment data for rendering
                ALIGNMENT_STORE[seg_id] = {
                    "dur_demo": dur_demo,
                    "breath_pause": breath_pause,
                    "dur_drill": dur_drill,
                    "total_dur": dur_demo + breath_pause + dur_drill,
                    "aligned_demo": aligned_demo,
                    "aligned_drill": aligned_drill_shifted,
                    "tokens": tokens
                }

                # Concatenate Stage 1 + breath pause + Stage 2 into seamless single audio file
                # Use apad on stage 1 for natural breath pause
                f_demo_padded = os.path.join(temp_dir, f"seg_{seg_id}_demo_pad.mp3")
                subprocess.run([
                    "ffmpeg", "-y", "-i", f_demo,
                    "-af", f"apad=pad_dur={breath_pause}",
                    "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    f_demo_padded
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

                cmd_concat = [
                    "ffmpeg", "-y",
                    "-i", f_demo_padded,
                    "-i", f_drill,
                    "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
                    "-map", "[outa]",
                    "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    out_file
                ]
                subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                print(f"   [OK] 日语示范与跟读练读无缝合并 [{seg_id}]: {os.path.basename(out_file)} (示范 {dur_demo:.1f}s + 练读 {dur_drill:.1f}s)")

            else:
                speech_chunks = seg.get("speech_chunks")
                if speech_chunks:
                    await synthesize_seamless_bilingual_audio(speech_chunks, out_file)
                    print(f"   [OK] 无缝多语言混读合成完毕 [{seg.get('character')}]: {os.path.basename(out_file)}")
                else:
                    lang = seg.get("lang", "zh")
                    text = seg.get("content", "")
                    if lang == "ja":
                        chunks = [{"lang": "ja", "text": text}]
                    else:
                        chunks = [{"lang": "zh", "text": text}]
                    await synthesize_seamless_bilingual_audio(chunks, out_file)
                    print(f"   [OK] 单语言音频合成完毕 [{seg.get('character')}]: {os.path.basename(out_file)}")

    # Save alignment store to json for verification
    align_json_path = os.path.join(output_dir, "alignment_cache.json")
    with open(align_json_path, "w", encoding="utf-8") as f:
        json.dump(ALIGNMENT_STORE, f, ensure_ascii=False, indent=2)

    print(" [OK] WL.02 全部音频轨道与毫秒级时间轴计算完成！")

# ==========================================
# METADATA & SCRIPTS
# ==========================================

def build_metadata_md_zh(output_dir: str):
    meta_path = os.path.join(output_dir, "metadata.md")
    title = f"【JLPT N5-N3】WL.02 周一到周五东京生活全景大合集 | 电车·便利店·居酒屋·秋叶原·拉面·温泉全场景28分钟精讲"
    description = f"""【TokyoFlow 日语实景大合集 • 中文解说版】
大合集专集编号：WL.02 (WM.01)
短视频跟读编号：WS.02
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
# 4K MASTER THUMBNAILS
# ==========================================

def render_master_thumbnail_zh(output_dir: str):
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
    badge_str = "【JLPT N5-N3】WL.02 大合集"
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

    for target_dir in ["assets/thumbnails", "site/assets/thumbnails", "docs/site/assets/thumbnails"]:
        os.makedirs(target_dir, exist_ok=True)
        img.save(os.path.join(target_dir, "WM01-weekday_survival_mega_compilation_zh_thumb.jpg"), quality=95)

def render_shorts_thumbnail_zh(output_dir: str):
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
    draw.text((width - 355, 65), "WS.02 • JLPT N5-N3", fill=(255, 255, 255), font=get_font(24))

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
    draw.text((70, 1690), "观看 28分钟 完整大课 (WL.02)", fill=(255, 255, 255), font=get_font(32))
    draw.text((70, 1745), "40+ 实用句型公式 • 语法深度拆解 • 日本文化秘籍", fill=(254, 240, 138), font=get_font(24))

    short_thumb_out = os.path.join(output_dir, "short_thumbnail.jpg")
    img.save(short_thumb_out, quality=95)
    print(f"  [OK] 保存 9:16 中文短片封面: {short_thumb_out}")

# ==========================================
# 1080P MASTER VIDEO RENDERING (MILLIS-KARAOKE + BREAKDOWN)
# ==========================================

def render_dialogue_karaoke_frame_zh(
    tokens: list,
    category_label: str,
    title_label: str,
    chinese_meaning: str,
    current_time: float,
    total_duration: float,
    jlpt_level: str = "N4",
    stage_label: str = "原声示范"
) -> Image.Image:
    """Renders 3-Tier dialogue card with active glowing yellow capsule and red bouncing mora dot."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top brand bar
    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语实景大课  |  WL.02 周一到周五东京生活全景大合集", fill=(255, 255, 255), font=get_font(26))
    badge_str = f"【{jlpt_level}】• {category_label}"
    draw.text((1400, 18), badge_str, fill=(244, 114, 182), font=get_font(22))

    # Stage Badge (示范 / 练读)
    is_drill = "练读" in stage_label or "跟读" in stage_label
    badge_color = (225, 29, 72) if not is_drill else (16, 185, 129)
    draw.rounded_rectangle([(50, 95), (480, 145)], radius=12, fill=badge_color)
    draw.text((70, 106), f"[ {stage_label} • 纯正东京原声 ]", fill=(255, 255, 255), font=get_font(22))

    # Main 3-Tier Card
    card_x, card_y, card_w, card_h = 50, 480, 1820, 540
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=2)

    # Layout tokens
    base_jp_sz = 44
    base_kana_sz = 22
    base_ro_sz = 22

    f_jp = get_font(base_jp_sz)
    f_ka = get_font(base_kana_sz)
    f_ro = get_font(base_ro_sz)

    pad_x = 24
    token_widths = []
    for tok in tokens:
        w_jp = draw.textbbox((0, 0), tok["orig"], font=f_jp)[2]
        w_ka = draw.textbbox((0, 0), tok.get("kana", ""), font=f_ka)[2] if tok.get("kana") else 0
        w_ro = draw.textbbox((0, 0), tok.get("romaji", ""), font=f_ro)[2] if tok.get("romaji") else 0
        w = max(w_jp, w_ka, w_ro) + pad_x
        token_widths.append(w)

    total_tokens_w = sum(token_widths)
    start_x = card_x + max(30, (card_w - total_tokens_w) // 2)
    curr_x = start_x

    y_kana = card_y + 40
    y_jp = card_y + 85
    y_romaji = card_y + 165

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        st = tok.get("start", 0.0)
        et = tok.get("end", 0.0)
        is_active = (st <= current_time <= et) and (et > st)

        if is_active:
            # Active glowing gold capsule
            draw.rounded_rectangle([(curr_x + 2, y_kana - 12), (curr_x + w - 2, y_romaji + 42)], radius=16, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            # Active bouncing mora indicator dot
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 26), (dot_cx + 6, y_kana - 14)], fill=(220, 38, 38))
            c_kana = (180, 83, 9)
            c_jp = (15, 23, 42)
            c_ro = (180, 83, 9)
        else:
            c_kana = (148, 163, 184)
            c_jp = (255, 255, 255)
            c_ro = (148, 163, 184)

        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=f_ka)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=c_kana, font=f_ka)

        jw = draw.textbbox((0, 0), tok["orig"], font=f_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=c_jp, font=f_jp)

        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=f_ro)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=c_ro, font=f_ro)

        curr_x += w

    # Divider
    draw.line([(card_x + 40, card_y + 245), (card_x + card_w - 40, card_y + 245)], fill=(51, 65, 85, 200), width=2)

    # Chinese Meaning
    draw.text((card_x + 45, card_y + 265), f"中文释义：「{chinese_meaning}」", fill=(226, 232, 240), font=get_font(30))

    # Follow-Along Prompt Box
    prompt_y = card_y + 335
    if is_drill:
        draw.rounded_rectangle([(card_x + 45, prompt_y), (card_x + card_w - 45, prompt_y + 105)], radius=14, fill=(30, 41, 59, 220), outline=(16, 185, 129), width=2)
        draw.text((card_x + 70, prompt_y + 20), "[ 影子跟读练读中 • 纯正东京原声领读 ]", fill=(16, 185, 129), font=get_font(24))
        draw.text((card_x + 70, prompt_y + 60), "跟随黄色发光胶囊同步大声朗读 • 强化语调与声调肌肉记忆", fill=(255, 255, 255), font=get_font(22))
    else:
        draw.rounded_rectangle([(card_x + 45, prompt_y), (card_x + card_w - 45, prompt_y + 105)], radius=14, fill=(30, 41, 59, 220), outline=(56, 189, 248), width=1)
        draw.text((card_x + 70, prompt_y + 20), "[ 场景示范聆听 • 纯正东京原声 ]", fill=(56, 189, 248), font=get_font(24))
        draw.text((card_x + 70, prompt_y + 60), "先聆听东京母语者标准发音与停顿节奏，随后进入连续跟读练读", fill=(226, 232, 240), font=get_font(22))

    # Bottom Studio Ribbon
    draw.rounded_rectangle([(card_x, card_y + card_h - 45), (card_x + card_w, card_y + card_h)], radius=10, fill=(15, 23, 42))
    draw.text((card_x + 25, card_y + card_h - 36), "[ TOKYOFLOW 实景学院 ]  100% 纯正东京原声 (Nanami) • 毫秒级卡拉OK跟读对齐", fill=(56, 189, 248), font=get_font(18))

    return img

def render_breakdown_frame_zh(
    ref_sentence: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    chapter_title: str,
    jlpt_level: str
) -> Image.Image:
    """Renders high-contrast Glassmorphic breakdown card with vocab grid and grammar spotlight."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语实景大课  |  WL.02 周一到周五东京生活全景大合集", fill=(255, 255, 255), font=get_font(26))
    draw.text((1400, 18), f"【{jlpt_level}】• {chapter_title}", fill=(244, 114, 182), font=get_font(22))

    card_x, card_w = 50, 1820

    # Header Target Sentence Banner (y=90..165)
    draw.rounded_rectangle([(card_x, 90), (card_x + card_w, 165)], radius=16, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
    draw.text((card_x + 30, 102), f"[ 名师核心句语法精讲 ]", fill=(244, 114, 182), font=get_font(20))
    draw.text((card_x + 300, 102), ref_sentence, fill=(255, 255, 255), font=get_font(24))

    # Vocab Grid Cards (y=180..440)
    grid_y = 180
    n_cards = min(4, len(vocab_list)) if vocab_list else 1
    cw = (card_w - (n_cards - 1) * 20) // max(1, n_cards)
    ch_h = 245

    for i in range(n_cards):
        v = vocab_list[i] if i < len(vocab_list) else {}
        cx = card_x + i * (cw + 20)
        draw.rounded_rectangle([(cx, grid_y), (cx + cw, grid_y + ch_h)], radius=16, fill=(10, 15, 28, 235), outline=(51, 65, 85, 200), width=2)

        pos_str = f" {v.get('pos', '重点词汇')} "
        draw.rounded_rectangle([(cx + 20, grid_y + 15), (cx + cw - 20, grid_y + 50)], radius=8, fill=(30, 41, 59))
        draw.text((cx + 30, grid_y + 20), pos_str, fill=(56, 189, 248), font=get_font(18))

        draw.text((cx + 25, grid_y + 65), v.get("orig", ""), fill=(254, 240, 138), font=get_font(30))
        draw.text((cx + 25, grid_y + 115), f"{v.get('kana', '')} ({v.get('romaji', '')})", fill=(148, 163, 184), font=get_font(18))
        draw.line([(cx + 20, grid_y + 155), (cx + cw - 20, grid_y + 155)], fill=(51, 65, 85, 180), width=1)
        draw.text((cx + 25, grid_y + 175), v.get("meaning", ""), fill=(241, 245, 249), font=get_font(20))

    # Grammar & Culture Spotlight Box (y=445..1020)
    box_y = 445
    box_h = 575
    draw.rounded_rectangle([(card_x, box_y), (card_x + card_w, box_y + box_h)], radius=20, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=2)

    draw.rounded_rectangle([(card_x + 2, box_y + 2), (card_x + card_w - 2, box_y + 60)], radius=18, fill=(30, 41, 59))
    draw.text((card_x + 35, box_y + 15), f"[ 语法与文化核心要点 ] {grammar_title}", fill=(254, 240, 138), font=get_font(26))

    by = box_y + 85
    for header, detail in grammar_bullets:
        draw.text((card_x + 35, by), header, fill=(244, 114, 182), font=get_font(24))
        draw.text((card_x + 40, by + 36), detail, fill=(241, 245, 249), font=get_font(24))
        by += 90

    # Bottom Tag
    draw.rounded_rectangle([(card_x, box_y + box_h - 45), (card_x + card_w, box_y + box_h)], radius=10, fill=(15, 23, 42))
    draw.text((card_x + 25, box_y + box_h - 36), "[ TOKYOFLOW 语法精讲 ] 云希全中文深度拆解 • 融入日本高语境文化习惯", fill=(56, 189, 248), font=get_font(18))

    return img

def render_story_narration_frame_zh(
    chapter_num: int,
    chapter_title: str,
    narration_text: str,
    character_name: str,
    jlpt_level: str
) -> Image.Image:
    """Renders general narration card."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top Banner
    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语实景大课  |  WL.02 周一到周五东京生活全景大合集", fill=(255, 255, 255), font=get_font(26))
    draw.text((1400, 18), f"【{jlpt_level}】• {chapter_title}", fill=(244, 114, 182), font=get_font(22))

    # Bottom Subtitle Card
    box_x, box_y, box_w, box_h = 50, 680, 1820, 350
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=2)

    draw.text((box_x + 35, box_y + 20), f"[ 章节 {chapter_num} • {chapter_title} ]", fill=(254, 240, 138), font=get_font(26))

    draw.rounded_rectangle([(box_x + box_w - 360, box_y + 15), (box_x + box_w - 35, box_y + 55)], radius=10, fill=(225, 29, 72))
    draw.text((box_x + box_w - 340, box_y + 22), f"名师解说 • {character_name}", fill=(255, 255, 255), font=get_font(18))

    draw.line([(box_x + 35, box_y + 65), (box_x + box_w - 35, box_y + 65)], fill=(51, 65, 85, 200), width=1)

    lines = [narration_text[i:i+45] for i in range(0, len(narration_text), 45)]
    ty = box_y + 85
    for line in lines[:4]:
        draw.text((box_x + 35, ty), line, fill=(241, 245, 249), font=get_font(28))
        ty += 48

    draw.rounded_rectangle([(box_x + 35, box_y + box_h - 45), (box_x + box_w - 35, box_y + box_h - 10)], radius=8, fill=(15, 23, 42))
    draw.text((box_x + 50, box_y + box_h - 38), "[ TOKYOFLOW 实景学院 ]  100% 纯正东京原声 (Nanami) • 云希全中文深度拆解", fill=(56, 189, 248), font=get_font(18))

    return img

def render_full_master_video_zh(output_dir: str):
    """Renders 1080p master video using authentic Tokyo 4K scenes, millisecond karaoke HUD, and continuous practice audio."""
    print("\n--- 正在使用 4K 东京实景渲染 1080p 中文大合集视频 ---")
    tmp_vid_dir = "tmp/videogen/sunday_mega_wm01_zh"
    os.makedirs(tmp_vid_dir, exist_ok=True)

    audio_dir = os.path.join(output_dir, "audio")
    segment_mp4s = []
    fps = 30

    for ch in MEGA_SCREENPLAY_ZH:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]
        bg_scene = ch.get("bg_scene", "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg")

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            seg_type = seg.get("type", "narration")
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            out_mp4 = os.path.join(tmp_vid_dir, f"clip_{seg_id}.mp4")

            if not os.path.exists(audio_path):
                continue

            dur = get_audio_duration(audio_path)
            total_frames = int((dur + 0.2) * fps)

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", bg_scene,
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", "1920x1080",
                "-pix_fmt", "rgba",
                "-r", str(fps),
                "-i", "-",
                "-i", audio_path,
                "-filter_complex",
                "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080[bg];[bg][1:v]overlay=0:0:shortest=1[v]",
                "-map", "[v]",
                "-map", "2:a",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", str(fps),
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                "-t", str(dur + 0.2),
                out_mp4
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps

                    if seg_type == "audio_phrase":
                        align_data = ALIGNMENT_STORE.get(seg_id, {})
                        dur_demo = align_data.get("dur_demo", dur * 0.5)
                        breath_p = align_data.get("breath_pause", 0.35)
                        t_demo_end = dur_demo + breath_p

                        if t < t_demo_end:
                            # Stage 1: 原声示范
                            active_tokens = align_data.get("aligned_demo", seg.get("tokens", []))
                            stg_lbl = "原声示范"
                        else:
                            # Stage 2: 影子跟读练读
                            active_tokens = align_data.get("aligned_drill", seg.get("tokens", []))
                            stg_lbl = "影子跟读"

                        frame = render_dialogue_karaoke_frame_zh(
                            tokens=active_tokens,
                            category_label=ch_title,
                            title_label=f"场景 {seg_id} • {ch_title}",
                            chinese_meaning=seg.get("meaning", ""),
                            current_time=t,
                            total_duration=dur,
                            jlpt_level=seg.get("jlpt", "N4"),
                            stage_label=stg_lbl
                        )
                    elif seg_type == "breakdown":
                        frame = render_breakdown_frame_zh(
                            ref_sentence=seg.get("ref_sentence", seg.get("content", "")),
                            vocab_list=seg.get("vocab", []),
                            grammar_title=seg.get("grammar_title", "JLPT 语法与文化解析"),
                            grammar_bullets=seg.get("grammar_bullets", []),
                            chapter_title=ch_title,
                            jlpt_level=seg.get("jlpt", "N4")
                        )
                    else:
                        frame = render_story_narration_frame_zh(
                            chapter_num=ch_id,
                            chapter_title=ch_title,
                            narration_text=seg.get("content", ""),
                            character_name=seg.get("character", "云希"),
                            jlpt_level=seg.get("jlpt", "导览")
                        )

                    proc.stdin.write(frame.tobytes())
            except Exception:
                pass
            finally:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait()

            segment_mp4s.append(out_mp4)
            print(f"  [RENDERED] clip_{seg_id}.mp4 ({dur:.1f}s)")

    concat_txt = os.path.join(tmp_vid_dir, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in segment_mp4s:
            f.write(f"file '{os.path.abspath(cf)}'\n")

    final_master_mp4 = os.path.join(output_dir, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", final_master_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  [OK] WM.01 / WL.02 1080p 中文大合集视频合成完毕: {final_master_mp4}")

# ==========================================
# MAIN ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: WL.02 / WM.01 周一到周五生活大合集【中文复刻版】生产管线")
    print(f" 编号: {COMPILATION_METADATA_ZH['series_code']} • 预估时长: {COMPILATION_METADATA_ZH['target_duration_mins']} 分钟")
    print("================================================================================")

    output_dir = os.path.join("docs/youtube_releases", COMPILATION_METADATA_ZH["release_folder"])
    os.makedirs(output_dir, exist_ok=True)

    render_master_thumbnail_zh(output_dir)
    render_shorts_thumbnail_zh(output_dir)
    build_metadata_md_zh(output_dir)
    build_script_json_zh(output_dir)
    await synthesize_all_audio_tracks_zh(output_dir)
    render_full_master_video_zh(output_dir)

    print(f"\n[OK] WL.02 / WM.01 中文全景大合集生成完成: {output_dir}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
