#!/usr/bin/env python3
"""
TokyoFlow Japanese Cinema Masterclass • Weekend Blockbuster Production Pipeline (Chinese Edition)
==================================================================================================
Automated production engine for 25-minute Chinese-localized cinematic deep-dives:
- WL.01: 电影《最后的里程》(ラストマイル) 25分钟影视沉浸大课【中文解说版】
- 100% Authentic Movie Action Footage (Clean Cuts, High Bitrate)
- Real-time Word-by-Word Karaoke Follow-Along Subtitles (Glowing Gold Capsule & Red Dot)
- Micro-Lesson Sentence Breakdown HUD (Chinese Vocabulary Grid + Active Grammar Spotlight)
- Strict Dual-Voice Separation (Yunxi 100% ZH / Nanami 100% JA with Slow, Crisp Speed)
- 4K Authentic Hikari Mitsushima (满岛光) Movie Hero Cover & 9:16 Shorts Cover (Zero Emoji Discipline)
"""

import os
import sys
import re
import glob
import json
import asyncio
import subprocess
from pathlib import Path
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
# MASTER FILM DATASET: LAST MILE (中文解说版)
# ==========================================
EPISODE_METADATA_ZH = {
    "episode_number": 1,
    "episode_code": "WL.01",
    "shorts_funnel_code": "WS.01",
    "series_name": "TokyoFlow 日语影视大课【中文解说版】",
    "slug": "last_mile_2024_zh",
    "movie_title_en": "Last Mile",
    "movie_title_ja": "ラストマイル",
    "movie_title_zh": "最后的里程",
    "release_year": 2024,
    "director": "冢原亚由子 (Ayuko Tsukahara)",
    "screenplay": "野木亚纪子 (Akiko Nogi)",
    "starring": ["满岛光", "冈田将生", "藤冈靛", "石原里美", "绫野刚"],
    "genre": "悬疑 / 商业社会派推理 / 现代物流危机",
    "target_duration_mins": 25,
    "jlpt_distribution": {
        "N5": "30%",
        "N4": "30%",
        "N3": "25%",
        "N2": "15%"
    },
    "core_dilemma": "黑色星期五狂欢季，东京发生多起连环包裹爆炸案。巨型物流中心运转速度高达每秒2.7米，究竟是该为了企业利益强行运转，还是为了人命彻底停下流水线？"
}

# 6-Chapter Cinematic Screenplay Structure (Chinese Edition)
CINEMA_SCREENPLAY_ZH = [
    # ----------------------------------------------------
    # CHAPTER 0: 90秒高能黄金开场 (00:00 - 01:30)
    # ----------------------------------------------------
    {
        "chapter_id": 0,
        "chapter_title": "90秒黄金开局 • 核心矛盾引爆",
        "timecode_range": "00:00 - 01:30",
        "scene_clip": "scene_01_warehouse",
        "segments": [
            {
                "seg_id": "0_1",
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "东京，黑色星期五。数以百万计的包裹正以每秒2.7米的速度极速运转。然而，其中一个包裹暗藏致命炸弹。如果停下流水线，企业将面临数亿日元的巨额违约金；如果继续运转，整个东京随时可能陷入连环爆炸。欢迎来到 TokyoFlow 日语影视大课。今天，我们将深度解析2024年日本现象级票房悬疑神作——《最后的里程》。",
                "duration_est": 18.0,
                "jlpt": "导览"
            },
            {
                "seg_id": "0_2",
                "type": "hero_quote",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ベルトコンベアを止めるわけにはいきません。私たちの仕事は、荷物を届けることです。",
                "furi": "べるとこんべあ を とめる わけには いきません。 わたしたち の しごと は、 にもつ を とどける こと です。",
                "romaji": "Beruto konbea o tomeru wake ni wa ikimasen. Watashitachi no shigoto wa, nimotsu o todokeru koto desu.",
                "meaning": "我们绝不能停下传送带。我们的职责，就是把包裹准时送达。",
                "jlpt": "N3",
                "grammar": "~わけにはいかない（道德与社会契约约束：绝不能 / 无法轻易推脱）",
                "tokens": [
                    {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea"},
                    {"orig": "を", "kana": "を", "romaji": "o"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru"},
                    {"orig": "わけにはいきません", "kana": "わけにはいきません", "romaji": "wake ni wa ikimasen"},
                    {"orig": "私たち", "kana": "わたしたち", "romaji": "watashitachi"},
                    {"orig": "の仕事は", "kana": "のしごとは", "romaji": "no shigoto wa"},
                    {"orig": "荷物を", "kana": "にもつを", "romaji": "nimotsu o"},
                    {"orig": "届けることです", "kana": "とどけることです", "romaji": "todokeru koto desu"}
                ],
                "vocab": [
                    {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea", "pos": "名词", "meaning": "传送带 / 流水线"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru", "pos": "动词 (N4)", "meaning": "停下 / 停止"},
                    {"orig": "わけにはいかない", "kana": "わけにはいかない", "romaji": "wake ni wa ikanai", "pos": "语法 (N3)", "meaning": "绝不能 / 不可以"},
                    {"orig": "届ける", "kana": "とどける", "romaji": "todokeru", "pos": "动词 (N4)", "meaning": "递送 / 准时送达"}
                ],
                "grammar_title": "~わけにはいかない (社会责任与心理约束)",
                "grammar_bullets": [
                    ("• 核心接续句型", "动词辞书形 + わけにはいかない / わけにはいきません"),
                    ("• 心理高语境解析", "并非物理上无法停止，而是受制于职业道德、社会责任或企业契约，绝对不能停"),
                    ("• 东京职场语境", "在物流与外包企业中，停下流水线意味着公然违背对全社会的履约承诺")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "0_3",
                "type": "instant_breakdown",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "请注意句中极为关键的 JLPT N3 核心语法：'wake ni wa ikimasen'。在日语高语境中，它并不是表示能力上做不到，而是受到社会道德、职业契约或舆论责任的强烈制约，因而'绝不能停'。在日本企业文化中，擅自中断流水线被视为对整个社会契约的背叛。",
                "duration_est": 16.0,
                "jlpt": "N3 深度解析",
                "ref_sentence": "ベルトコンベアを止めるわけにはいきません。",
                "vocab": [
                    {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea", "pos": "名词", "meaning": "传送带 / 流水线"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru", "pos": "动词 (N4)", "meaning": "停下 / 停止"},
                    {"orig": "わけにはいかない", "kana": "わけにはいかない", "romaji": "wake ni wa ikanai", "pos": "语法 (N3)", "meaning": "绝不能 / 不可以"},
                    {"orig": "届ける", "kana": "とどける", "romaji": "todokeru", "pos": "动词 (N4)", "meaning": "递送 / 准时送达"}
                ],
                "grammar_title": "~わけにはいかない (社会责任与心理约束)",
                "grammar_bullets": [
                    ("• 核心接续句型", "动词辞书形 + わけにはいかない / わけにはいきません"),
                    ("• 心理高语境解析", "并非物理上无法停止，而是受制于职业道德、社会责任或企业契约，绝对不能停"),
                    ("• 东京职场语境", "在物流与外包企业中，停下流水线意味着公然违背对全社会的履约承诺")
                ]
            },
            {
                "seg_id": "0_4",
                "type": "channel_cta",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "在接下来的25分钟超长大课中，你将掌握从 JLPT N5 到 N2 的80个实战高频句型、掌握地道职场潜台词，并深入剖析这部烧脑大片背后的社会心理真相。欢迎订阅 TokyoFlow，准备好笔记本，让我们一起走进这场东京物流风暴。",
                "duration_est": 14.5,
                "jlpt": "学习导览"
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 1: 第一幕 • 初入职场与物流危机 (01:30 - 07:30)
    # ----------------------------------------------------
    {
        "chapter_id": 1,
        "chapter_title": "第一幕 • 初入职场与物流危机",
        "timecode_range": "01:30 - 07:30",
        "scene_clip": "scene_02_elena",
        "segments": [
            {
                "seg_id": "1_1_narration",
                "type": "story_setup",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "故事拉开帷幕。位于关东的巨型物流集散中心迎来了新任中心总监——舟渡艾蕾娜。协助她的是谨慎沉稳的现场主管梨本孔。在庞大的仓库内，数千名员工正在紧张而有序地高效作业。",
                "duration_est": 16.0,
                "jlpt": "剧情铺垫"
            },
            {
                "seg_id": "1_1_dialogue",
                "type": "dialogue_n5",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "furi": "きょう から こちら で おせわ に なります。 どうぞ よろしく おねがい いたします。",
                "romaji": "Kyou kara kochira de osewa ni narimasu. Douzo yoroshiku onegai itashimasu.",
                "meaning": "从今天起在这里承蒙各位关照，请多多指教。",
                "jlpt": "N5",
                "tokens": [
                    {"orig": "今日から", "kana": "きょうから", "romaji": "kyou kara"},
                    {"orig": "こちらで", "kana": "こちらで", "romaji": "kochira de"},
                    {"orig": "お世話に", "kana": "おせわに", "romaji": "osewa ni"},
                    {"orig": "なります", "kana": "なります", "romaji": "narimasu"},
                    {"orig": "どうぞ", "kana": "どうぞ", "romaji": "douzo"},
                    {"orig": "よろしく", "kana": "よろしく", "romaji": "yoroshiku"},
                    {"orig": "お願い", "kana": "おねがい", "romaji": "onegai"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu"}
                ],
                "vocab": [
                    {"orig": "今日", "kana": "きょう", "romaji": "kyou", "pos": "名词 (N5)", "meaning": "今天"},
                    {"orig": "お世話", "kana": "おせわ", "romaji": "osewa", "pos": "名词 (N5)", "meaning": "关照 / 承蒙照料"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "动词 (N5)", "meaning": "成为"},
                    {"orig": "よろしく", "kana": "よろしく", "romaji": "yoroshiku", "pos": "副词 (N5)", "meaning": "请多关照"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu", "pos": "自谦语 (N4)", "meaning": "做（谦虚说法）"}
                ],
                "grammar": "お世話になります (职场新人入职经典寒暄语) + いたします (自谦语)",
                "grammar_title": "お世話になります 与 自谦语 いたします",
                "grammar_bullets": [
                    ("• 职场入职金句", "今日からお世話になります (从今天起承蒙关照)"),
                    ("• 自谦敬语形式", "いたします 是 します 的自谦形式，主动放低身段以示对团队与前辈的敬意"),
                    ("• 商务礼仪动作", "初次进入新部门作自我介绍时，必须配合标准的30度鞠躬礼")
                ],
                "duration_est": 7.0
            },
            {
                "seg_id": "1_1_breakdown",
                "type": "pedagogical_lesson",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "这是日本职场中含金量极高的 JLPT N5 新人入职金句。'Osewa ni narimasu' 直译为'我将成为接受您照料的一方'。注意艾蕾娜巧妙结合了自谦动词 'itashimasu'，瞬间树立起既专业又谦逊的职场管理形象。",
                "duration_est": 17.0,
                "jlpt": "N5 精讲",
                "ref_sentence": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "vocab": [
                    {"orig": "今日", "kana": "きょう", "romaji": "kyou", "pos": "名词 (N5)", "meaning": "今天"},
                    {"orig": "お世話", "kana": "おせわ", "romaji": "osewa", "pos": "名词 (N5)", "meaning": "关照 / 承蒙照料"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "动词 (N5)", "meaning": "成为"},
                    {"orig": "よろしく", "kana": "よろしく", "romaji": "yoroshiku", "pos": "副词 (N5)", "meaning": "请多关照"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu", "pos": "自谦语 (N4)", "meaning": "做（谦虚说法）"}
                ],
                "grammar_title": "お世話になります 与 自谦语 いたします",
                "grammar_bullets": [
                    ("• 职场入职金句", "今日からお世話になります (从今天起承蒙关照)"),
                    ("• 自谦敬语形式", "いたします 是 します 的自谦形式，主动放低身段以示对团队与前辈的敬意"),
                    ("• 商务礼仪动作", "初次进入新部门作自我介绍时，必须配合标准的30度鞠躬礼")
                ]
            },
            {
                "seg_id": "1_2_dialogue",
                "type": "dialogue_n5_n4",
                "character": "梨本孔",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ブラックフライデーの初日です。荷物のバーコードを速やかに確認してください。",
                "furi": "ぶらっくふらいでー の しょにち です。 にもつ の ばーこーど を すみやか に かくにん して ください。",
                "romaji": "Burakku furaidee no shonichi desu. Nimotsu no baakoodo o sumiyaka ni kakunin shite kudasai.",
                "meaning": "今天是黑五大促第一天，请各位迅速核对所有包裹条形码。",
                "jlpt": "N4",
                "tokens": [
                    {"orig": "ブラックフライデーの", "kana": "ぶらっくふらいでーの", "romaji": "burakku furaidee no"},
                    {"orig": "初日です", "kana": "しょにちです", "romaji": "shonichi desu"},
                    {"orig": "荷物の", "kana": "にもつの", "romaji": "nimotsu no"},
                    {"orig": "バーコードを", "kana": "ばーこーどを", "romaji": "baakoodo o"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni"},
                    {"orig": "確認して", "kana": "かくにんして", "romaji": "kakunin shite"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai"}
                ],
                "vocab": [
                    {"orig": "初日", "kana": "しょにち", "romaji": "shonichi", "pos": "名词 (N4)", "meaning": "第一天 / 首日"},
                    {"orig": "荷物", "kana": "にもつ", "romaji": "nimotsu", "pos": "名词 (N5)", "meaning": "行李 / 包裹"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni", "pos": "副词 (N3)", "meaning": "迅速 / 敏捷地"},
                    {"orig": "確認", "kana": "かくにん", "romaji": "kakunin", "pos": "名词/サ变 (N4)", "meaning": "确认 / 核实"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "补助词 (N5)", "meaning": "请……"}
                ],
                "grammar": "~てください (礼貌请求/指令) + 速やかに (高频职场副词)",
                "grammar_title": "速やかに (迅速且无阻塞) 与 早く (单纯速度快)",
                "grammar_bullets": [
                    ("• 职场精细语境", "速やかに 强调不仅速度要快，更要求流程顺畅、不产生瓶颈积压"),
                    ("• 日常用语 vs 职场商务", "口语常用：早くやって (快点做) | 职场规范：速やかに確認してください"),
                    ("• 核心句型公式", "动词て形 + ください (标准而得体的职场工作指令)")
                ],
                "duration_est": 7.5
            },
            {
                "seg_id": "1_2_breakdown",
                "type": "pedagogical_lesson",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "在日本快节奏的仓储物流行业中，主管一般不会用随意的 'hayaku'，而是使用地道的 JLPT N3 商务副词 'sumiyaka ni'，意思是'在不造成停顿和拥堵的前提下迅速推进'。",
                "duration_est": 13.0,
                "jlpt": "N4 精讲",
                "ref_sentence": "荷物のバーコードを速やかに確認してください。",
                "vocab": [
                    {"orig": "初日", "kana": "しょにち", "romaji": "shonichi", "pos": "名词 (N4)", "meaning": "第一天 / 首日"},
                    {"orig": "荷物", "kana": "にもつ", "romaji": "nimotsu", "pos": "名词 (N5)", "meaning": "行李 / 包裹"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni", "pos": "副词 (N3)", "meaning": "迅速 / 敏捷地"},
                    {"orig": "確認", "kana": "かくにん", "romaji": "kakunin", "pos": "名词/サ变 (N4)", "meaning": "确认 / 核实"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "补助词 (N5)", "meaning": "请……"}
                ],
                "grammar_title": "速やかに (迅速且无阻塞) 与 早く (单纯速度快)",
                "grammar_bullets": [
                    ("• 职场精细语境", "速やかに 强调不仅速度要快，更要求流程顺畅、不产生瓶颈积压"),
                    ("• 日常用语 vs 职场商务", "口语常用：早くやって (快点做) | 职场规范：速やかに確認してください"),
                    ("• 核心句型公式", "动词て形 + ください (标准而得体的职场工作指令)")
                ]
            },
            {
                "seg_id": "1_3_dialogue",
                "type": "dialogue_n4",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ベルトの速度を秒速2.7メートルに保てば、すべての出荷が間に合います。",
                "furi": "べると の そくど を びょうそく に てん なな めーとる に たもてば、 すべて の しゅっか が まにあいます。",
                "romaji": "Beruto no sokudo o byousoku ni ten nana meetoru ni tamoteba, subete no shukka ga maniaimasu.",
                "meaning": "只要将传送带速度维持在每秒2.7米，所有出库发货都能按时赶上。",
                "jlpt": "N4",
                "tokens": [
                    {"orig": "ベルトの速度を", "kana": "べるとのそくどを", "romaji": "beruto no sokudo o"},
                    {"orig": "秒速2.7メートルに", "kana": "びょうそくにてんななめーとるに", "romaji": "byousoku ni ten nana meetoru ni"},
                    {"orig": "保てば", "kana": "たもてば", "romaji": "tamoteba"},
                    {"orig": "すべての", "kana": "すべての", "romaji": "subete no"},
                    {"orig": "出荷が", "kana": "しゅっかが", "romaji": "shukka ga"},
                    {"orig": "間に合います", "kana": "まにあいます", "romaji": "maniaimasu"}
                ],
                "vocab": [
                    {"orig": "速度", "kana": "そくど", "romaji": "sokudo", "pos": "名词 (N4)", "meaning": "速度 / 速率"},
                    {"orig": "保つ", "kana": "たもつ", "romaji": "tamotsu", "pos": "动词 (N3)", "meaning": "维持 / 保持"},
                    {"orig": "出荷", "kana": "しゅっか", "romaji": "shukka", "pos": "名词 (N3)", "meaning": "出货 / 发货"},
                    {"orig": "間に合う", "kana": "まにあう", "romaji": "maniau", "pos": "动词 (N4)", "meaning": "赶得上 / 准时"}
                ],
                "grammar": "~ば条件形 (假定条件：只要……就……) + 間に合う (赶得上/按时)",
                "grammar_title": "~ば 假定条件形 与 間に合う (按时赶上)",
                "grammar_bullets": [
                    ("• 条件句变形规则", "动词词尾变e段 + ば (保つ -> 保てば：只要维持)"),
                    ("• 逻辑因果", "表达因果关系：只要满足前置条件A，结果B就必然能实现"),
                    ("• 高频实用动词 間に合う", "广泛用于赶火车、赶交货期或守时约定")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "1_3_cultural_insight",
                "type": "cultural_insight",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "这里埋下了电影最致命的伏笔：'Byousoku ni ten nana meetoru'——每秒2.7米。这不仅仅是一个物理数字，更是跨国巨头物流系统强行设定的绝对考核指标。一旦降速哪怕0.1秒，全球管理系统就会自动拉响红色警报。",
                "duration_est": 16.0,
                "jlpt": "剧情与文化背景",
                "ref_sentence": "ベルトの速度を秒速2.7メートルに保てば、すべての出荷が間に合います。",
                "vocab": [
                    {"orig": "速度", "kana": "そくど", "romaji": "sokudo", "pos": "名词 (N4)", "meaning": "速度 / 速率"},
                    {"orig": "保つ", "kana": "たもつ", "romaji": "tamotsu", "pos": "动词 (N3)", "meaning": "维持 / 保持"},
                    {"orig": "出荷", "kana": "しゅっか", "romaji": "shukka", "pos": "名词 (N3)", "meaning": "出货 / 发货"},
                    {"orig": "間に合う", "kana": "まにあう", "romaji": "maniau", "pos": "动词 (N4)", "meaning": "赶得上 / 准时"}
                ],
                "grammar_title": "~ば 假定条件形 与 間に合う (按时赶上)",
                "grammar_bullets": [
                    ("• 条件句变形规则", "动词词尾变e段 + ば (保つ -> 保てば：只要维持)"),
                    ("• 逻辑因果", "表达因果关系：只要满足前置条件A，结果B就必然能实现"),
                    ("• 高频实用动词 間に合う", "广泛用于赶火车、赶交货期或守时约定")
                ]
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 2: 第二幕 • 冲突爆发与真心话较量 (07:30 - 15:00)
    # ----------------------------------------------------
    {
        "chapter_id": 2,
        "chapter_title": "第二幕 • 冲突爆发与真心话较量",
        "timecode_range": "07:30 - 15:00",
        "scene_clip": "scene_06_miu404",
        "segments": [
            {
                "seg_id": "2_1_narration",
                "type": "story_escalation",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "第二幕危机全面爆发。东京都内多个收件人在拆开包裹的瞬间遭遇炸弹爆炸。警方机动搜查队的志摩与伊吹刑警迅速赶到现场，法医团队 UDI 研究所也紧急介入，将整个物流中心重重包围。",
                "duration_est": 18.0,
                "jlpt": "剧情推向高潮"
            },
            {
                "seg_id": "2_1_dialogue",
                "type": "dialogue_n3",
                "character": "志摩一未 (刑警)",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "このまま配送を続ければ、被害が拡大しかねません。直ちに全ラインを停止すべきです。",
                "furi": "この まま はいそう を つづければ、 ひがい が かくだい しかねません。 ただちに ぜん らいん を ていし すべき です。",
                "romaji": "Kono mama haisou o tsuzukereba, higai ga kakudai shikanemasen. Tadachini zen rain o teishi subeki desu.",
                "meaning": "如果就这样继续配送，受害范围极有可能进一步扩大。应当立即停止全部流水线。",
                "jlpt": "N2-N3",
                "tokens": [
                    {"orig": "このまま", "kana": "このまま", "romaji": "kono mama"},
                    {"orig": "配送を", "kana": "はいそうを", "romaji": "haisou o"},
                    {"orig": "続ければ", "kana": "つづければ", "romaji": "tsuzukereba"},
                    {"orig": "被害が", "kana": "ひがいが", "romaji": "higai ga"},
                    {"orig": "拡大しかねません", "kana": "かくだいしかねません", "romaji": "kakudai shikanemasen"},
                    {"orig": "直ちに", "kana": "ただちに", "romaji": "tadachini"},
                    {"orig": "全ラインを", "kana": "ぜんらいんを", "romaji": "zen rain o"},
                    {"orig": "停止すべきです", "kana": "ていしすべきです", "romaji": "teishi subeki desu"}
                ],
                "vocab": [
                    {"orig": "配送", "kana": "はいそう", "romaji": "haisou", "pos": "名词 (N3)", "meaning": "配送 / 运送"},
                    {"orig": "拡大", "kana": "かくだい", "romaji": "kakudai", "pos": "名词/サ变 (N3)", "meaning": "扩大 / 蔓延"},
                    {"orig": "~かねない", "kana": "~かねない", "romaji": "~kanenai", "pos": "语法 (N2)", "meaning": "极有可能导致坏结果"},
                    {"orig": "直ちに", "kana": "ただちに", "romaji": "tadachini", "pos": "副词 (N2)", "meaning": "立即 / 刻不容缓"},
                    {"orig": "~べきだ", "kana": "~べきだ", "romaji": "~beki da", "pos": "语法 (N3)", "meaning": "理应 / 应当"}
                ],
                "grammar": "~かねない (N2: 严重恶果隐患) + ~べきだ (N3: 道德/职责上应当)",
                "grammar_title": "~かねない (消极隐患预测) 与 ~べきだ (应当/理应)",
                "grammar_bullets": [
                    ("• N2 语法 ~かねない", "接动词ます形词干，专门用于表达'极有可能引发灾难性不良后果'"),
                    ("• N3 语法 ~べきだ", "动词辞书形 + べきだ，代表出于社会公义、法律或道德的强制要求"),
                    ("• 危机指令副词 直ちに", "比 すぐに 更具法律与行政强制力的公文副词")
                ],
                "duration_est": 8.5
            },
            {
                "seg_id": "2_1_breakdown",
                "type": "pedagogical_lesson",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "志摩刑警这句话中同时出现了两大 JLPT 核心考点：一个是 N2 语法 '~shikanemasen'，它专门用来预警可能引发的灾难性恶果；另一个是 N3 必备语法 '~subeki desu'，代表基于社会正义与职责'理应采取的行动'。",
                "duration_est": 17.0,
                "jlpt": "N2-N3 精讲",
                "ref_sentence": "このまま配送を続ければ、被害が拡大しかねません。直ちに全ラインを停止すべきです。",
                "vocab": [
                    {"orig": "配送", "kana": "はいそう", "romaji": "haisou", "pos": "名词 (N3)", "meaning": "配送 / 运送"},
                    {"orig": "拡大", "kana": "かくだい", "romaji": "kakudai", "pos": "名词/サ变 (N3)", "meaning": "扩大 / 蔓延"},
                    {"orig": "~かねない", "kana": "~かねない", "romaji": "~kanenai", "pos": "语法 (N2)", "meaning": "极有可能导致坏结果"},
                    {"orig": "直ちに", "kana": "ただちに", "romaji": "tadachini", "pos": "副词 (N2)", "meaning": "立即 / 刻不容缓"},
                    {"orig": "~べきだ", "kana": "~べきだ", "romaji": "~beki da", "pos": "语法 (N3)", "meaning": "理应 / 应当"}
                ],
                "grammar_title": "~かねない (消极隐患预测) 与 ~べきだ (应当/理应)",
                "grammar_bullets": [
                    ("• N2 语法 ~かねない", "接动词ます形词干，专门用于表达'极有可能引发灾难性不良后果'"),
                    ("• N3 语法 ~べきだ", "动词辞书形 + べきだ，代表出于社会公义、法律或道德的强制要求"),
                    ("• 危机指令副词 直ちに", "比 すぐに 更具法律与行政强制力的公文副词")
                ]
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 3: 第三幕 • 终极高潮与灵魂金句 (15:00 - 22:30)
    # ----------------------------------------------------
    {
        "chapter_id": 3,
        "chapter_title": "第三幕 • 终极高潮与灵魂金句",
        "timecode_range": "15:00 - 22:30",
        "scene_clip": "scene_08_speedgauge",
        "segments": [
            {
                "seg_id": "3_1_narration",
                "type": "climax_intro",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "剧情迎来了全片最高能的反转与爆发。艾蕾娜的真实身份与神秘过往浮出水面。面对上层资本的无情施压与无辜人命的生死抉择，她在控制室作出了震惊全场的终极抉择。",
                "duration_est": 17.0,
                "jlpt": "高潮剧情"
            },
            {
                "seg_id": "3_1_dialogue",
                "type": "dialogue_n2",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "人間の命を犠牲にしてまで、守るべき利益など存在しません。私たちは立ち止まる勇気を持つべきです。",
                "furi": "にんげん の いのち を ぎせい に して まで、 まもる べき りえき など そんざい しません。 わたしたち は たちどまる ゆうき を もつ べき です。",
                "romaji": "Ningen no inochi o gisei ni shite made, mamoru beki rieki nado sonzai shimasen. Watashitachi wa tachidomaru yuuki o motsu beki desu.",
                "meaning": "根本不存在任何值得牺牲人类生命去守护的利益。我们此刻应当拥有停下脚步的勇气。",
                "jlpt": "N2",
                "tokens": [
                    {"orig": "人間の命を", "kana": "にんげんのいのちを", "romaji": "ningen no inochi o"},
                    {"orig": "犠牲にしてまで", "kana": "ぎせいにしてまで", "romaji": "gisei ni shite made"},
                    {"orig": "守るべき利益など", "kana": "まもるべきりえきなど", "romaji": "mamoru beki rieki nado"},
                    {"orig": "存在しません", "kana": "そんざいしません", "romaji": "sonzai shimasen"},
                    {"orig": "私たちは", "kana": "わたしたちは", "romaji": "watashitachi wa"},
                    {"orig": "立ち止まる勇気を", "kana": "たちどまるゆうきを", "romaji": "tachidomaru yuuki o"},
                    {"orig": "持つべきです", "kana": "もつべきです", "romaji": "motsu beki desu"}
                ],
                "vocab": [
                    {"orig": "犠牲", "kana": "ぎせい", "romaji": "gisei", "pos": "名词 (N2)", "meaning": "牺牲 / 代价"},
                    {"orig": "~てまで", "kana": "~てまで", "romaji": "~te made", "pos": "语法 (N2)", "meaning": "甚至不惜做到……的地步"},
                    {"orig": "利益", "kana": "りえき", "romaji": "rieki", "pos": "名词 (N3)", "meaning": "利益 / 利润"},
                    {"orig": "存在", "kana": "そんざい", "romaji": "sonzai", "pos": "名词/サ变 (N3)", "meaning": "存在"},
                    {"orig": "立ち止まる", "kana": "たちどまる", "romaji": "tachidomaru", "pos": "动词 (N2)", "meaning": "停下脚步 / 驻足"}
                ],
                "grammar": "~てまで (N2: 不惜做出极端行为) + など (轻蔑/全盘否定)",
                "grammar_title": "~てまで (甚至不惜……) 与 利益など (否定轻蔑)",
                "grammar_bullets": [
                    ("• N2 终极句型 ~てまで", "动词て形 + まで，强调为了某个目的做出超越常理的极端牺牲"),
                    ("• 语气助词 など", "接在名词后表示'像……这种微不足道的东西'，带有强烈的批判色彩"),
                    ("• 影视哲学金句", "批判工业异化与资本冷血的灵魂核心台词")
                ],
                "duration_est": 9.5
            },
            {
                "seg_id": "3_1_breakdown",
                "type": "pedagogical_lesson",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "这一句是整部电影的思想灵魂所在。'~te made' 是 JLPT N2 核心句型，表示'甚至不惜付出惨痛代价去做某事'。而艾蕾娜在 'rieki' 后面加上 'nado'，以极具威慑力的语气全盘否定了资本唯利是图的虚伪本质。",
                "duration_est": 18.0,
                "jlpt": "N2 灵魂精讲",
                "ref_sentence": "人間の命を犠牲にしてまで、守るべき利益など存在しません。",
                "vocab": [
                    {"orig": "犠牲", "kana": "ぎせい", "romaji": "gisei", "pos": "名词 (N2)", "meaning": "牺牲 / 代价"},
                    {"orig": "~てまで", "kana": "~てまで", "romaji": "~te made", "pos": "语法 (N2)", "meaning": "甚至不惜做到……的地步"},
                    {"orig": "利益", "kana": "りえき", "romaji": "rieki", "pos": "名词 (N3)", "meaning": "利益 / 利润"},
                    {"orig": "存在", "kana": "そんざい", "romaji": "sonzai", "pos": "名词/サ变 (N3)", "meaning": "存在"},
                    {"orig": "立ち止まる", "kana": "たちどまる", "romaji": "tachidomaru", "pos": "动词 (N2)", "meaning": "停下脚步 / 驻足"}
                ],
                "grammar_title": "~てまで (甚至不惜……) 与 利益など (否定轻蔑)",
                "grammar_bullets": [
                    ("• N2 终极句型 ~てまで", "动词て形 + まで，强调为了某个目的做出超越常理的极端牺牲"),
                    ("• 语气助词 など", "接在名词后表示'像……这种微不足道的东西'，带有强烈的批判色彩"),
                    ("• 影视哲学金句", "批判工业异化与资本冷血的灵魂核心台词")
                ]
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 4: 影子跟读特训营 (22:30 - 24:00)
    # ----------------------------------------------------
    {
        "chapter_id": 4,
        "chapter_title": "影视影子跟读特训营 • 5大等级灵魂台词",
        "timecode_range": "22:30 - 24:00",
        "scene_clip": "scene_09_evacuation",
        "segments": [
            {
                "seg_id": "4_0_intro",
                "type": "shadowing_intro",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "现在进入 TokyoFlow 影视沉浸影子跟读特训营。请跟随七海纯正东京原声，在屏幕上的金色卡拉OK高亮引导下，大声朗读以下五条经典台词。",
                "duration_est": 11.0,
                "jlpt": "跟读特训"
            },
            {
                "seg_id": "4_1_drill",
                "type": "shadowing_line",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "今日からこちらでお世話になります。",
                "furi": "きょう から こちら で おせわ に なります。",
                "meaning": "从今天起在这里承蒙关照。（JLPT N5 职场入门）",
                "duration_est": 5.0
            },
            {
                "seg_id": "4_2_drill",
                "type": "shadowing_line",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "荷物のバーコードを速やかに確認してください。",
                "furi": "にもつ の ばーこーど を すみやか に かくにん して ください。",
                "meaning": "请迅速核对包裹条形码。（JLPT N4 现场指令）",
                "duration_est": 5.5
            },
            {
                "seg_id": "4_3_drill",
                "type": "shadowing_line",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ベルトコンベアを止めるわけにはいきません。",
                "furi": "べるとこんべあ を とめる わけには いきません。",
                "meaning": "我们绝不能停下传送带。（JLPT N3 核心约束）",
                "duration_est": 5.5
            },
            {
                "seg_id": "4_4_drill",
                "type": "shadowing_line",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "このまま配送を続ければ、被害が拡大しかねません。",
                "furi": "この まま はいそう を つづければ、 ひがい が かくだい しかねません。",
                "meaning": "继续配送极有可能导致受害扩大。（JLPT N2 严重隐患）",
                "duration_est": 6.0
            },
            {
                "seg_id": "4_5_drill",
                "type": "shadowing_line",
                "character": "七海",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "人間の命を犠牲にしてまで、守るべき利益など存在しません。",
                "furi": "にんげん の いのち を ぎせい に して まで、 まもる べき りえき など そんざい しません。",
                "meaning": "绝不存在任何值得牺牲人类生命去守护的利益。（JLPT N2 灵魂金句）",
                "duration_est": 7.0
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 5: 结语与复习总结 (24:00 - 25:00)
    # ----------------------------------------------------
    {
        "chapter_id": 5,
        "chapter_title": "总结结语与下期预告",
        "timecode_range": "24:00 - 25:00",
        "scene_clip": "scene_10_climax",
        "segments": [
            {
                "seg_id": "5_1_philosophical",
                "type": "outro",
                "character": "云希",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "以上就是本期《最后的里程》电影级深度大课的全部精讲。通过地道的影视对白，我们不仅掌握了从 N5 到 N2 的高频句型，更读懂了日本现代社会中职场人内心的挣扎与温情。如果本期内容对你的日语学习有所启发，请点赞、订阅并分享给你的学习伙伴。在评论区留下你印象最深的一句台词，我们下期影视大课再见！",
                "duration_est": 22.0,
                "jlpt": "结语"
            }
        ]
    }
]

# ==========================================
# AUDIO DURATION HELPER
# ==========================================

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 5.0

# ==========================================
# HUD FRAME RENDERING (100% CONTRAST & ZERO CUTOFF)
# ==========================================

def draw_top_brand_bar_zh(draw: ImageDraw.Draw, width: int, chapter_title: str, jlpt_level: str):
    draw.rectangle([(0, 0), (width, 68)], fill=(10, 15, 28, 220))
    draw.text((50, 18), "TokyoFlow 日语影视大课  |  WL.01《最后的里程》影视沉浸精讲", fill=(255, 255, 255), font=get_font(26))

    level_clean = jlpt_level.replace("Breakdown", "").replace("Lesson", "").replace("dialogue_", "").strip() if jlpt_level else ""
    if level_clean and level_clean != "N/A" and level_clean != "CTA":
        badge_str = f"【{level_clean}】" if not level_clean.startswith("【") else level_clean
    else:
        badge_str = "【影视大课】"

    f_badge = get_font(22)
    bbox = draw.textbbox((0, 0), badge_str, font=f_badge)
    text_w = bbox[2] - bbox[0]
    pill_w = max(140, text_w + 36)
    x1 = width - 50 - pill_w
    x2 = width - 50
    draw.rounded_rectangle([(x1, 12), (x2, 56)], radius=12, fill=(225, 29, 72, 230), outline=(255, 255, 255, 180), width=2)
    draw.text((x1 + (pill_w - text_w) // 2, 18), badge_str, fill=(255, 255, 255), font=f_badge)

def compute_mora_ranges(tokens: list, total_duration: float) -> list:
    weights = []
    for tok in tokens:
        k = tok.get("kana", "") or tok.get("orig", "")
        m_count = float(len(k))
        for small in ["ゃ", "ゅ", "ょ", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "っ", "ャ", "ュ", "ョ", "ッ"]:
            m_count -= 0.35 * k.count(small)
        if any(p in tok.get("orig", "") for p in ["、", "。", "！", "？", ",", "!"]):
            m_count += 1.2
        weights.append(max(0.7, m_count))

    total_w = sum(weights)
    lead_in = 0.10
    tail_out = 0.18
    active_dur = max(0.4, total_duration - (lead_in + tail_out))

    ranges = []
    cur_t = lead_in
    for w in weights:
        dur = (w / total_w) * active_dur
        ranges.append((cur_t, cur_t + dur))
        cur_t += dur
    return ranges

def render_dialogue_karaoke_frame_zh(
    tokens: list,
    category_label: str,
    title_label: str,
    chinese_meaning: str,
    grammar_text: str,
    current_time: float,
    total_duration: float,
    jlpt_level: str = "N3"
) -> Image.Image:
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(80):
        alpha = int(220 * (1.0 - (y / 80.0)))
        draw.line([(0, y), (1920, y)], fill=(10, 15, 28, alpha))

    for y in range(540, 1080):
        rel = (y - 540) / 540.0
        alpha = int(240 * (rel ** 0.85))
        draw.line([(0, y), (1920, y)], fill=(8, 12, 22, alpha))

    draw_top_brand_bar_zh(draw, 1920, category_label, jlpt_level)

    draw.rounded_rectangle([(50, 80), (460, 120)], radius=10, fill=(30, 41, 59, 210))
    draw.text((65, 87), "[ 影视对白 • 影子跟读 ]", fill=(244, 114, 182), font=get_font(18))

    card_x, card_y, card_w, card_h = 50, 580, 1820, 440
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=22, fill=(10, 15, 28, 230), outline=(51, 65, 85, 200), width=2)

    max_tokens_w = card_w - 70
    base_jp_size = 46
    base_kana_size = 22
    base_ro_size = 22

    def calc_widths(jp_sz, kana_sz, ro_sz, pad_x):
        f_jp = get_font(jp_sz)
        f_ka = get_font(kana_sz)
        f_ro = get_font(ro_sz)
        t_widths = []
        for tok in tokens:
            w_jp = draw.textbbox((0, 0), tok["orig"], font=f_jp)[2]
            w_kana = draw.textbbox((0, 0), tok.get("kana", ""), font=f_ka)[2] if tok.get("kana") else 0
            w_ro = draw.textbbox((0, 0), tok.get("romaji", ""), font=f_ro)[2] if tok.get("romaji") else 0
            w = max(w_jp, w_kana, w_ro) + pad_x
            t_widths.append(w)
        return t_widths, f_jp, f_ka, f_ro

    pad_x = 22
    token_widths, font_jp, font_kana, font_romaji = calc_widths(base_jp_size, base_kana_size, base_ro_size, pad_x)
    total_tokens_w = sum(token_widths)

    if total_tokens_w > max_tokens_w:
        scale = max_tokens_w / total_tokens_w
        jp_sz = max(28, int(base_jp_size * scale))
        kana_sz = max(15, int(base_kana_size * scale))
        ro_sz = max(15, int(base_ro_size * scale))
        pad_x = max(8, int(22 * scale))
        token_widths, font_jp, font_kana, font_romaji = calc_widths(jp_sz, kana_sz, ro_sz, pad_x)
        total_tokens_w = sum(token_widths)

    start_x = card_x + max(25, (card_w - total_tokens_w) // 2)
    curr_x = start_x

    y_kana = card_y + 35
    y_jp = card_y + 80
    y_romaji = card_y + 155

    time_ranges = compute_mora_ranges(tokens, total_duration)

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        st, et = time_ranges[i]
        is_active = (st <= current_time <= et)

        if is_active:
            draw.rounded_rectangle([(curr_x + 2, y_kana - 10), (curr_x + w - 2, y_romaji + 38)], radius=14, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 22), (dot_cx + 6, y_kana - 10)], fill=(220, 38, 38))
            c_kana = (180, 83, 9)
            c_jp = (15, 23, 42)
            c_ro = (180, 83, 9)
        else:
            c_kana = (148, 163, 184)
            c_jp = (255, 255, 255)
            c_ro = (148, 163, 184)

        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=font_kana)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=c_kana, font=font_kana)

        jw = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=c_jp, font=font_jp)

        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=font_romaji)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=c_ro, font=font_romaji)

        curr_x += w

    draw.line([(card_x + 35, card_y + 215), (card_x + card_w - 35, card_y + 215)], fill=(51, 65, 85, 180), width=2)

    font_zh = get_font(26)
    draw.text((card_x + 40, card_y + 230), f"中文释义： {chinese_meaning}", fill=(226, 232, 240), font=font_zh)

    if grammar_text:
        draw.rounded_rectangle([(card_x + 40, card_y + 285), (card_x + card_w - 40, card_y + 365)], radius=12, fill=(30, 41, 59, 230), outline=(244, 114, 182, 180), width=1)
        clean_g = grammar_text.replace("▶", ">").replace("􀀀", ">").replace("■", "•").strip()
        draw.text((card_x + 60, card_y + 295), f"[ 核心语法解析 ]  {clean_g}", fill=(244, 114, 182), font=get_font(20))
        draw.text((card_x + 60, card_y + 325), "跟随东京原声大声跟读 • 掌握地道音调与职场语境", fill=(255, 255, 255), font=get_font(20))

    draw.rounded_rectangle([(card_x, card_y + 380), (card_x + card_w, card_y + 425)], radius=10, fill=(15, 23, 42, 230))
    draw.text((card_x + 25, card_y + 392), "[ 影子跟读进行中 ]  纯正东京原声 ja-JP-NanamiNeural", fill=(56, 189, 248), font=get_font(20))

    return img

def render_breakdown_frame_zh(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    current_time: float,
    total_duration: float,
    chapter_title: str = "句型拆解",
    jlpt_level: str = "N3"
) -> Image.Image:
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (1920, 1080)], fill=(10, 15, 28, 220))
    draw_top_brand_bar_zh(draw, 1920, chapter_title, jlpt_level)

    num_cards = min(5, len(vocab_list))
    vocab_window = total_duration * 0.55
    card_dur = vocab_window / max(1, num_cards)

    if current_time >= vocab_window:
        spotlight_active = True
        active_vocab_idx = None
    else:
        spotlight_active = False
        active_vocab_idx = min(num_cards - 1, int(current_time / card_dur))

    # Top Dialogue Header
    draw.rounded_rectangle([(50, 80), (620, 120)], radius=10, fill=(30, 41, 59, 220))
    pill_txt = "[ 核心词汇精讲 ] 逐词发音与词性" if active_vocab_idx is not None else "[ 名师语法拆解 ] 高频句型与文化背景"
    draw.text((65, 87), pill_txt, fill=(244, 114, 182), font=get_font(18))

    draw.rounded_rectangle([(50, 135), (1870, 195)], radius=12, fill=(15, 23, 42, 235), outline=(56, 189, 248), width=2)
    draw.text((70, 148), f"原声台词： {sentence_ja}", fill=(255, 255, 255), font=get_font(28))
    draw.rounded_rectangle([(1500, 145), (1850, 185)], radius=8, fill=(225, 29, 72))
    draw.text((1520, 152), "名师解说 • 云希", fill=(255, 255, 255), font=get_font(18))

    # Vocab Grid Cards
    grid_x = 50
    grid_y = 215
    gap = 20
    card_w = (1820 - (num_cards - 1) * gap) // num_cards
    card_h = 240

    for i in range(num_cards):
        v = vocab_list[i]
        x = grid_x + i * (card_w + gap)
        y = grid_y
        is_active = (active_vocab_idx == i)

        if is_active:
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=16, fill=(254, 249, 195), outline=(245, 158, 11), width=3)
            draw.ellipse([(x + card_w // 2 - 7, y - 7), (x + card_w // 2 + 7, y + 7)], fill=(220, 38, 38))
            pos_fill = (254, 240, 138)
            pos_color = (180, 83, 9)
            kana_color = (180, 83, 9)
            jp_color = (15, 23, 42)
            meaning_color = (180, 83, 9)
        else:
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)
            pos_fill = (30, 41, 59)
            pos_color = (244, 114, 182)
            kana_color = (56, 189, 248)
            jp_color = (255, 255, 255)
            meaning_color = (226, 232, 240)

        draw.rounded_rectangle([(x + 14, y + 14), (x + min(card_w - 14, 140), y + 44)], radius=8, fill=pos_fill)
        draw.text((x + 20, y + 20), v.get("pos", "词汇"), fill=pos_color, font=get_font(17))

        draw.text((x + 14, y + 54), v.get("orig", ""), fill=jp_color, font=get_font(30))

        kana_ro = f"{v.get('kana', '')} • {v.get('romaji', '')}"
        draw.text((x + 14, y + 105), kana_ro, fill=kana_color, font=get_font(18))

        draw.text((x + 14, y + 145), v.get("meaning", ""), fill=meaning_color, font=get_font(20))

    # Grammar Spotlight Card
    spot_x = 50
    spot_y = 475
    spot_w = 1820
    spot_h = 475

    clean_grammar_title = grammar_title.replace("~", "~").strip()

    if spotlight_active:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=20, fill=(15, 23, 42, 240), outline=(99, 102, 241), width=4)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=20, fill=(49, 46, 129))
        draw.text((spot_x + 30, spot_y + 16), f"[ 语法与社会文化深度解析 ]  {clean_grammar_title}", fill=(254, 240, 138), font=get_font(26))
    else:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=20, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=20, fill=(30, 41, 59))
        draw.text((spot_x + 30, spot_y + 16), f"[ 语法与社会文化深度解析 ]  {clean_grammar_title}", fill=(244, 114, 182), font=get_font(26))

    b_y = spot_y + 80
    for bullet in grammar_bullets:
        if isinstance(bullet, (list, tuple)) and len(bullet) >= 2:
            title, desc = bullet[0], bullet[1]
        elif isinstance(bullet, str) and ":" in bullet:
            parts = bullet.split(":", 1)
            title, desc = parts[0].strip(), parts[1].strip()
        else:
            title, desc = "• 要点", str(bullet)

        t_font = get_font(24)
        d_font = get_font(22)
        bbox_t = draw.textbbox((0, 0), title, font=t_font)
        title_w = bbox_t[2] - bbox_t[0]
        desc_x = spot_x + 30 + max(420, title_w + 24)

        b_title_color = (254, 240, 138) if spotlight_active else (244, 114, 182)
        draw.text((spot_x + 30, b_y), title, fill=b_title_color, font=t_font)
        draw.text((desc_x, b_y), desc, fill=(255, 255, 255), font=d_font)
        b_y += 75

    draw.rounded_rectangle([(spot_x, 970), (spot_x + spot_w, 1030)], radius=12, fill=(10, 15, 28))
    draw.text((spot_x + 25, 985), "[ TOKYOFLOW 日语学院 ]  云希全中文深度拆解  •  tokyoflow.app 官网下载完整讲义", fill=(56, 189, 248), font=get_font(22))

    return img

def render_lower_third_story_overlay_zh(
    chapter_num: int,
    chapter_title: str,
    title_main: str,
    narration_text: str,
    jlpt_level: str = "N/A"
) -> Image.Image:
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw_top_brand_bar_zh(draw, 1920, chapter_title, jlpt_level)

    for y in range(700, 1080):
        rel = (y - 700) / 380.0
        alpha = int(230 * (rel ** 0.85))
        draw.line([(0, y), (1920, y)], fill=(8, 12, 22, alpha))

    box_x, box_y, box_w, box_h = 50, 770, 1820, 260
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=20, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=2)

    draw.text((box_x + 35, box_y + 20), f"[ 第{chapter_num}幕 • {title_main} ]", fill=(254, 240, 138), font=get_font(26))
    draw.rounded_rectangle([(box_x + box_w - 380, box_y + 15), (box_x + box_w - 35, box_y + 55)], radius=10, fill=(225, 29, 72))
    draw.text((box_x + box_w - 365, box_y + 22), "名师解说 • 云希", fill=(255, 255, 255), font=get_font(18))

    draw.line([(box_x + 35, box_y + 65), (box_x + box_w - 35, box_y + 65)], fill=(51, 65, 85, 200), width=1)

    font_body = get_font(28)
    lines = [narration_text[i:i+45] for i in range(0, len(narration_text), 45)]
    ty = box_y + 80
    for line in lines[:3]:
        draw.text((box_x + 35, ty), line, fill=(241, 245, 249), font=font_body)
        ty += 46

    draw.rounded_rectangle([(box_x + 35, box_y + box_h - 45), (box_x + box_w - 35, box_y + box_h - 10)], radius=8, fill=(15, 23, 42))
    draw.text((box_x + 50, box_y + box_h - 38), "[ TOKYOFLOW 影视实景大课 ]  100% 东京原声原片 • 云希全中文名师精讲", fill=(56, 189, 248), font=get_font(18))

    return img

# ==========================================
# 4K MASTER THUMBNAIL (AUTHENTIC MITSUSHIMA HIKARI HERO PHOTO)
# ==========================================

def render_master_thumbnail_zh(output_dir: str):
    thumb_out = os.path.join(output_dir, "thumbnail.jpg")
    width, height = 1920, 1080

    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"

    if os.path.exists(hero_frame_path):
        raw_img = Image.open(hero_frame_path).convert("RGB")
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        # Place character dynamically on the right half exactly as English version
        base_img.paste(raw_img.resize((int(width * 1.1), int(height * 1.1)), Image.Resampling.LANCZOS), (80, -50))
    else:
        base_img = Image.new("RGB", (width, height), color=(10, 15, 28))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    import math
    for x in range(width):
        if x < 1180:
            rel = x / 1180.0
            alpha = int(248 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left Brand Pill
    draw.rounded_rectangle([(60, 45), (420, 105)], radius=18, fill=(255, 255, 255))
    draw.text((85, 58), "TokyoFlow 日语影视", fill=(225, 29, 72), font=get_font(26))

    # 2. Top-Right Badge (WL.01)
    badge_text = "【JLPT N5-N2】WL.01"
    draw.rounded_rectangle([(width - 380, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 350, 58), badge_text, fill=(255, 255, 255), font=get_font(26))

    # 3. Giant 3D Solar Yellow Hook (Left Aligned)
    font_hook = get_font(96)
    hook_lines = ["2.7米/秒", "绝不停运？"]
    hy = 145
    for line in hook_lines:
        for dx in range(-5, 6, 2):
            for dy in range(-5, 6, 2):
                draw.text((60 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 115

    # Movie Sub-Hook
    draw.text((65, 385), "电影《最后的里程》(ラストマイル)", fill=(244, 114, 182), font=get_font(38))

    # 4. Japanese Soul Quote Box
    quote_box_w = 880
    quote_box_y = 450
    draw.rounded_rectangle([(60, quote_box_y), (60 + quote_box_w, quote_box_y + 410)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    draw.text((90, quote_box_y + 25), "[ 电影级核心高光金句 ]", fill=(56, 189, 248), font=get_font(22))

    font_jp_quote = get_font(38)
    jp_text_1 = "ベルトコンベアを"
    jp_text_2 = "止めるわけにはいきません。"
    draw.text((90, quote_box_y + 70), jp_text_1, fill=(255, 255, 255), font=font_jp_quote)
    draw.text((90, quote_box_y + 125), jp_text_2, fill=(254, 240, 138), font=font_jp_quote)

    draw.text((90, quote_box_y + 200), "JLPT N3 语法：~わけにはいかない（道德与社会契约约束）", fill=(244, 114, 182), font=get_font(24))
    draw.text((90, quote_box_y + 245), "「我们绝不能停下传送带。」", fill=(226, 232, 240), font=get_font(26))
    draw.text((90, quote_box_y + 300), "悬疑推理与东京职场高语境日语沉浸精讲", fill=(148, 163, 184), font=get_font(22))
    draw.text((90, quote_box_y + 345), "主演：满岛光 (舟渡艾蕾娜) × 冈田将生 (梨本孔)", fill=(56, 189, 248), font=get_font(20))

    # 5. Bottom Ribbon (Full width)
    draw.rounded_rectangle([(60, height - 120), (width - 60, height - 45)], radius=16, fill=(225, 29, 72))
    draw.text((90, height - 98), " 100% 东京原声原片 • 逐字卡拉OK跟读 • 25分钟深度影视大课", fill=(255, 255, 255), font=get_font(24))

    img.save(thumb_out, quality=95)
    print(f"  [OK] 保存 16:9 中文大封面: {thumb_out}")

    # Sync to assets
    for target_dir in ["assets/thumbnails", "site/assets/thumbnails", "docs/site/assets/thumbnails"]:
        os.makedirs(target_dir, exist_ok=True)
        img.save(os.path.join(target_dir, "WL01-last-mile-masterclass_zh_thumb.jpg"), quality=95)

def render_shorts_thumbnail_zh(output_dir: str):
    thumb_out = os.path.join(output_dir, "short_thumbnail.jpg")
    width, height = 1080, 1920

    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"

    if os.path.exists(hero_frame_path):
        raw_img = Image.open(hero_frame_path).convert("RGB")
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        base_img.paste(raw_img.resize((int(width * 2.2), int(height * 1.3)), Image.Resampling.LANCZOS), (-200, 100))
    else:
        base_img = Image.new("RGB", (width, height), color=(10, 15, 28))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    for y in range(480):
        alpha = int(230 * (1 - y / 480))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    for y in range(1050, height):
        alpha = int(245 * min(1.0, (y - 1050) / 200))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(40, 50), (450, 115)], radius=16, fill=(255, 255, 255))
    draw.text((65, 65), "TokyoFlow 日语影视", fill=(225, 29, 72), font=get_font(26))

    draw.rounded_rectangle([(width - 380, 50), (width - 40, 115)], radius=16, fill=(225, 29, 72))
    draw.text((width - 355, 65), "WS.01 • JLPT N5-N2", fill=(255, 255, 255), font=get_font(24))

    font_hook = get_font(72)
    hook_lines = ["2.7米/秒", "绝不停运？"]
    hy = 155
    for line in hook_lines:
        for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((40 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((40, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 85

    draw.text((45, 335), "电影《最后的里程》高光台词拆解", fill=(244, 114, 182), font=get_font(26))

    card_y = 1120
    draw.rounded_rectangle([(40, card_y), (width - 40, 1640)], radius=24, fill=(10, 15, 28, 245), outline=(56, 189, 248), width=3)
    draw.text((70, card_y + 25), "[ 影视跟读特训 • 中文解说版 ]", fill=(56, 189, 248), font=get_font(22))

    draw.text((70, card_y + 70), "ベルトコンベアを", fill=(255, 255, 255), font=get_font(38))
    draw.text((70, card_y + 125), "止めるわけにはいきません。", fill=(254, 240, 138), font=get_font(34))

    draw.text((70, card_y + 185), "• JLPT N3: ~わけにはいかない（绝对不能）", fill=(244, 114, 182), font=get_font(26))
    draw.text((70, card_y + 230), "•「我们绝不能停下传送带。」", fill=(226, 232, 240), font=get_font(24))
    draw.text((70, card_y + 275), "• 满岛光 × 冈田将生 2024 现象级悬疑大作", fill=(148, 163, 184), font=get_font(22))
    draw.text((70, card_y + 325), "• 100% 东京原声（Nanami）+ 云希中文名师精讲", fill=(56, 189, 248), font=get_font(22))

    draw.rounded_rectangle([(40, 1660), (width - 40, 1840)], radius=18, fill=(225, 29, 72))
    draw.text((70, 1690), "观看 25分钟 完整大课 (WL.01)", fill=(255, 255, 255), font=get_font(32))
    draw.text((70, 1745), "掌握 80+ 职场高频句型 • 破解高语境潜台词", fill=(254, 240, 138), font=get_font(24))

    img.save(thumb_out, quality=95)
    print(f"  [OK] 保存 9:16 中文短片封面: {thumb_out}")

# ==========================================
# AUDIO SYNTHESIS ENGINE (CHINESE EDITION)
# ==========================================

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 5.0

def normalize_speech_text_zh(text: str, lang: str = "zh") -> str:
    """Normalizes JLPT levels and terms for clear TTS articulation in Chinese & Japanese."""
    if not text:
        return ""
    if lang == "zh":
        text = re.sub(r'JLPT\s*N([1-5])\s*至\s*N([1-5])', r'JLPT N \1 到 N \2', text, flags=re.IGNORECASE)
        text = re.sub(r'JLPT\s*N([1-5])', r'JLPT N \1', text, flags=re.IGNORECASE)
    elif lang == "ja":
        text = re.sub(r'\bN([1-5])\b', r'エヌ\1', text)
    return text

async def synthesize_all_audio_tracks_zh(output_dir: str):
    """Synthesizes high-fidelity Chinese and Japanese dual-language audio tracks."""
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    print("\n--- 正在合成中文解说版音频轨道 (Nanami 日语原声 + 云希 中文名师) ---")

    for ch in CINEMA_SCREENPLAY_ZH:
        for seg in ch["segments"]:
            seg_id = seg["seg_id"].replace(".", "_")
            out_file = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            seg["audio_file"] = out_file

            if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
                print(f"   [SKIP] 音频已存在: {os.path.basename(out_file)}")
                continue

            ref_sentence = seg.get("ref_sentence", "")
            if ref_sentence and seg.get("lang") == "zh":
                # Multi-voice breakdown: Nanami (JA sentence) -> Yunxi (ZH translation) -> Nanami+Yunxi (Vocab) -> Yunxi (Grammar)
                audio_parts = []

                # Part 1: Target Japanese Sentence
                tmp_target_ja = out_file + ".t_ja.raw.mp3"
                await edge_tts.Communicate(ref_sentence, "ja-JP-NanamiNeural", rate="-14%", pitch="+2Hz").save(tmp_target_ja)
                dur_target_ja = get_audio_duration(tmp_target_ja)
                audio_parts.append(tmp_target_ja)

                meaning = seg.get("meaning", "")
                if not meaning:
                    for s in ch["segments"]:
                        if s.get("lang") == "ja" and (ref_sentence in s.get("content", "") or s.get("content") in ref_sentence):
                            meaning = s.get("meaning", "")
                            break
                if not meaning:
                    meaning = "舟渡艾蕾娜强调核心运作原则。"

                # Part 2: Chinese translation
                tmp_target_zh = out_file + ".t_zh.raw.mp3"
                spoken_trans = f"中文翻译：{meaning}"
                await edge_tts.Communicate(spoken_trans, "zh-CN-YunxiNeural", rate="+2%", pitch="+0Hz").save(tmp_target_zh)
                audio_parts.append(tmp_target_zh)

                # Part 3: Vocab breakdown
                vocab_list = seg.get("vocab", [])[:4]
                for v_idx, v in enumerate(vocab_list):
                    v_ja_file = out_file + f".v_{v_idx}_ja.raw.mp3"
                    v_zh_file = out_file + f".v_{v_idx}_zh.raw.mp3"

                    await edge_tts.Communicate(v.get("orig", ""), "ja-JP-NanamiNeural", rate="-14%", pitch="+2Hz").save(v_ja_file)
                    spoken_meaning = f"{v.get('orig', '')}，含义是：{v.get('meaning', '')}"
                    await edge_tts.Communicate(spoken_meaning, "zh-CN-YunxiNeural", rate="+2%", pitch="+0Hz").save(v_zh_file)
                    audio_parts.extend([v_ja_file, v_zh_file])

                # Part 4: Grammar Spotlight
                tmp_spot_zh = out_file + ".spot.raw.mp3"
                spoken_spot = seg.get("content", "")
                await edge_tts.Communicate(spoken_spot, "zh-CN-YunxiNeural", rate="+2%", pitch="+0Hz").save(tmp_spot_zh)
                audio_parts.append(tmp_spot_zh)

                # Concat all audio parts with ffmpeg
                n = len(audio_parts)
                inputs = []
                for p in audio_parts:
                    inputs.extend(["-i", p])
                filter_str = "".join([f"[{i}:a]" for i in range(n)]) + f"concat=n={n}:v=0:a=1[a]"
                cmd_norm = [
                    "ffmpeg", "-y"
                ] + inputs + [
                    "-filter_complex", filter_str,
                    "-map", "[a]",
                    "-c:a", "libmp3lame",
                    "-b:a", "192k",
                    "-ar", "44100",
                    "-ac", "2",
                    out_file
                ]
                subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                for tmp_p in audio_parts:
                    if os.path.exists(tmp_p):
                        os.remove(tmp_p)
                print(f"   [OK] 中文多角色拆解音频生成完毕: {os.path.basename(out_file)}")
            else:
                voice = seg.get("voice", "zh-CN-YunxiNeural")
                raw_text = seg.get("content", "")
                text = normalize_speech_text_zh(raw_text, seg.get("lang", "zh"))

                if seg.get("lang") == "ja":
                    rate = "-16%"
                    pitch = "+2Hz"
                    if "drill" in seg.get("type", ""):
                        rate = "-22%"
                else:
                    rate = "+2%"
                    pitch = "+0Hz"

                tmp_raw = out_file + ".raw.mp3"
                comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                await comm.save(tmp_raw)

                cmd_norm = [
                    "ffmpeg", "-y",
                    "-i", tmp_raw,
                    "-c:a", "libmp3lame",
                    "-b:a", "192k",
                    "-ar", "44100",
                    "-ac", "2",
                    out_file
                ]
                subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                if os.path.exists(tmp_raw):
                    os.remove(tmp_raw)
                print(f"   [OK] 单轨音频生成完毕 [{seg.get('character')}]: {os.path.basename(out_file)}")

    print(" [OK] 全部中文版音频轨道生成完毕！")

# ==========================================
# MASTER VIDEO RENDERING (AUTHENTIC MOVIE FOOTAGE)
# ==========================================

def render_full_master_video_zh(output_dir: str):
    """Renders 1080p master video using authentic Last Mile film clips and real-time Chinese RGBA HUD."""
    print("\n--- 正在使用《最后的里程》正片原素材渲染 1080p 中文大师课视频 ---")
    tmp_vid_dir = "tmp/videogen/cinema_ep01_zh"
    os.makedirs(tmp_vid_dir, exist_ok=True)

    audio_dir = os.path.join(output_dir, "audio")
    segment_mp4s = []
    total_duration = 0.0
    fps = 30

    for ch in CINEMA_SCREENPLAY_ZH:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]
        scene_clip = ch.get("scene_clip", "scene_01_warehouse")

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            if not os.path.exists(audio_path):
                audio_path = os.path.join(audio_dir, f"seg_{seg_id.replace('_', '.')}.mp3")
            if not os.path.exists(audio_path):
                print(f"  [WARN] Missing audio for seg_{seg_id}: {audio_path}")
                continue

            out_mp4 = os.path.join(tmp_vid_dir, f"clip_{seg_id.replace('.', '_')}.mp4")

            unique_mp4 = f"tmp/videogen/unique_movie_clips/seg_{seg_id.replace('.', '_')}.mp4"
            if os.path.exists(unique_mp4):
                clean_mp4 = unique_mp4
            else:
                clean_mp4 = f"tmp/videogen/clean_movie_clips/{scene_clip}.mp4"

            duration = get_audio_duration(audio_path)
            total_duration += duration + 0.2
            total_frames = int((duration + 0.2) * fps)
            seg_type = seg.get("type", "")

            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", clean_mp4,
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
                "-t", str(duration + 0.2),
                out_mp4
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps

                    if seg.get("lang") == "ja":
                        frame = render_dialogue_karaoke_frame_zh(
                            tokens=seg.get("tokens", [{"orig": seg.get("content", ""), "kana": seg.get("furi", ""), "romaji": seg.get("romaji", "")}]),
                            category_label=ch_title,
                            title_label=f"场景 {seg['seg_id']} • {seg.get('character')}",
                            chinese_meaning=seg.get("meaning", ""),
                            grammar_text=seg.get("grammar", ""),
                            current_time=t,
                            total_duration=duration,
                            jlpt_level=seg.get("jlpt", "N3")
                        )
                    elif "breakdown" in seg_type or "lesson" in seg_type or "cultural" in seg_type:
                        frame = render_breakdown_frame_zh(
                            sentence_ja=seg.get("ref_sentence", seg.get("content", "")),
                            vocab_list=seg.get("vocab", []),
                            grammar_title=seg.get("grammar_title", "JLPT 核心语法与文化背景"),
                            grammar_bullets=seg.get("grammar_bullets", []),
                            current_time=t,
                            total_duration=duration,
                            chapter_title=ch_title,
                            jlpt_level=seg.get("jlpt", "N3")
                        )
                    else:
                        frame = render_lower_third_story_overlay_zh(
                            chapter_num=ch_id,
                            chapter_title=ch_title,
                            title_main=f"场景 {seg['seg_id']} • {ch_title}",
                            narration_text=seg.get("content", ""),
                            jlpt_level=seg.get("jlpt", "N/A")
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

    concat_txt = os.path.join(tmp_vid_dir, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for cf in segment_mp4s:
            f.write(f"file '{os.path.abspath(cf)}'\n")

    final_master_mp4 = os.path.join(output_dir, "video.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", final_master_mp4
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  [OK] WL.01 电影原片 1080p 中文大师课视频合成完毕: {final_master_mp4}")

# ==========================================
# MAIN ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: WL.01《最后的里程》电影级大课【中文复刻版】生产管线")
    print(f" 编号: {EPISODE_METADATA_ZH['episode_code']} • 预估时长: {EPISODE_METADATA_ZH['target_duration_mins']} 分钟")
    print("================================================================================")

    output_dir = os.path.join("docs/youtube_releases", "WL01-last-mile-masterclass-v1.0-zh")
    os.makedirs(output_dir, exist_ok=True)

    # 1. 渲染 4K 满岛光专属封面
    render_master_thumbnail_zh(output_dir)
    render_shorts_thumbnail_zh(output_dir)

    # 2. 合成中文与东京原声音频
    await synthesize_all_audio_tracks_zh(output_dir)

    # 3. 合成电影原片 1080p 视频
    render_full_master_video_zh(output_dir)

    print(f"\n[OK] WL.01 中文电影复刻版生成完成: {output_dir}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
