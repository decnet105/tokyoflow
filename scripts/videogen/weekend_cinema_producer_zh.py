#!/usr/bin/env python3
"""
TokyoFlow Japanese Cinema Masterclass • Weekend Blockbuster Production Pipeline (Chinese Edition)
==================================================================================================
Automated production engine for 25-minute Chinese-localized cinematic deep-dives:
- WL.01: 电影《最后的里程》(ラストマイル) 25分钟影视沉浸大课【中文解说版】
- Explainer Voice: zh-CN-YunxiNeural (云希全中文名师精讲)
- Tokyo Standard Voice: ja-JP-NanamiNeural (七海纯正东京原声)
- Real-time Word-by-Word Karaoke Subtitles & Micro-Lesson Sentence Breakdown HUD
- High-CTR 16:9 Master Chinese Cover & 9:16 Shorts Cover (Zero Emoji Discipline)
"""

import os
import sys
import re
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
                "seg_id": "0.1",
                "type": "cold_open",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "东京，黑色星期五。数以百万计的包裹正以每秒2.7米的速度极速运转。然而，其中一个包裹暗藏致命炸弹。如果停下流水线，企业将面临数亿日元的巨额违约金；如果继续运转，整个东京随时可能陷入连环爆炸。欢迎来到 TokyoFlow 日语影视大课。今天，我们将深度解析2024年日本现象级票房悬疑神作——《最后的里程》。",
                "duration_est": 18.0,
                "jlpt": "导览"
            },
            {
                "seg_id": "0.2",
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
                "seg_id": "0.3",
                "type": "instant_breakdown",
                "character": "Yunxi",
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
                "seg_id": "0.4",
                "type": "channel_cta",
                "character": "Yunxi",
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
                "seg_id": "1.1_narration",
                "type": "story_setup",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "故事拉开帷幕。位于关东的巨型物流集散中心迎来了新任中心总监——舟渡艾蕾娜。协助她的是谨慎沉稳的现场主管梨本孔。在庞大的仓库内，数千名员工正在紧张而有序地高效作业。",
                "duration_est": 16.0,
                "jlpt": "剧情铺垫"
            },
            {
                "seg_id": "1.1_dialogue",
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
                "seg_id": "1.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Yunxi",
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
                "seg_id": "1.2_dialogue",
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
                "seg_id": "1.2_breakdown",
                "type": "pedagogical_lesson",
                "character": "Yunxi",
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
                "seg_id": "1.3_dialogue",
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
                "seg_id": "1.3_cultural_insight",
                "type": "cultural_insight",
                "character": "Yunxi",
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
                "seg_id": "2.1_narration",
                "type": "story_escalation",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "第二幕危机全面爆发。东京都内多个收件人在拆开包裹的瞬间遭遇炸弹爆炸。警方机动搜查队的志摩与伊吹刑警迅速赶到现场，法医团队 UDI 研究所也紧急介入，将整个物流中心重重包围。",
                "duration_est": 18.0,
                "jlpt": "剧情推向高潮"
            },
            {
                "seg_id": "2.1_dialogue",
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
                "seg_id": "2.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Yunxi",
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
        "scene_clip": "scene_08_climax",
        "segments": [
            {
                "seg_id": "3.1_narration",
                "type": "climax_intro",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "剧情迎来了全片最高能的反转与爆发。艾蕾娜的真实身份与神秘过往浮出水面。面对上层资本的无情施压与无辜人命的生死抉择，她在控制室作出了震惊全场的终极抉择。",
                "duration_est": 17.0,
                "jlpt": "高潮剧情"
            },
            {
                "seg_id": "3.1_dialogue",
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
                "seg_id": "3.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Yunxi",
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
        "scene_clip": "scene_shadowing",
        "segments": [
            {
                "seg_id": "4.1_intro",
                "type": "shadowing_intro",
                "character": "Yunxi",
                "lang": "zh",
                "voice": "zh-CN-YunxiNeural",
                "content": "现在进入 TokyoFlow 影视沉浸影子跟读特训营。请跟随七海纯正东京原声，在屏幕上的金色卡拉OK高亮引导下，大声朗读以下五条经典台词。",
                "duration_est": 11.0,
                "jlpt": "跟读特训"
            },
            {
                "seg_id": "4.2_line1",
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
                "seg_id": "4.3_line2",
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
                "seg_id": "4.4_line3",
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
                "seg_id": "4.5_line4",
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
                "seg_id": "4.6_line5",
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
        "scene_clip": "scene_outro",
        "segments": [
            {
                "seg_id": "5.1_outro",
                "type": "outro",
                "character": "Yunxi",
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
# METADATA & SCHEDULE GENERATION
# ==========================================

def build_metadata_md_zh(output_dir: str):
    meta_path = os.path.join(output_dir, "metadata.md")
    title = f"【JLPT N5-N2】电影《最后的里程》影视沉浸精讲（WL.01）| 满岛光×冈田将生 2024票房冠军超长深度解析"
    description = f"""【TokyoFlow 日语影视实景大课 • 中文解说版】
长视频特辑编号：WL.01
短视频跟读编号：WS.01
JLPT 难度跨度：[JLPT N5] ~ [JLPT N2]

通过 2024 年日本现象级院线票房冠军悬疑大作《最后的里程》（ラストマイル / Last Mile），深度掌握地道东京职场高语境日语、商务寒暄法则与 JLPT N5 至 N2 必考核心句型！

【课程时间轴目录】
00:00 - 90秒黄金开局 • 核心矛盾引爆（每秒2.7米还是爆炸？）
01:30 - 第一幕 • 初入职场与物流危机（JLPT N5-N4 职场新人寒暄与工作指令）
07:30 - 第二幕 • 冲突爆发与真心话较量（JLPT N4-N3 危机处理与隐患预警）
15:00 - 第三幕 • 终极高潮与灵魂金句（JLPT N3-N2 深度语法与资本哲学剖析）
22:30 - 影视影子跟读特训营 • 5大等级灵魂台词跟读
24:00 - 总结结语与下期影视预告

【本片核心制作信息】
电影名称：最后的里程（ラストマイル / Last Mile）
导演：冢原亚由子 (Ayuko Tsukahara)
编剧：野木亚纪子 (Akiko Nogi)
领衔主演：满岛光 (Hikari Mitsushima)、冈田将生 (Masaki Okada)、石原里美 (Satomi Ishihara)、绫野刚 (Go Ayano)

【核心教学语法点】
- [JLPT N5]：今日からお世話になります (职场入职标准问候语) + いたします (自谦动词)
- [JLPT N4]：~ば 条件形 (假定条件) + 間に合う (赶得上/按时)
- [JLPT N3]：~わけにはいかない (受社会契约与道德约束的绝不能) + ~べきだ (理应/应当)
- [JLPT N2]：~かねない (极有可能引发灾难恶果) + ~てまで (甚至不惜付出代价)

【TokyoFlow 官方学习平台】
访问 TokyoFlow 官方网站下载完整讲义与配套词汇卡：
https://tokyoflow.app/

【检索标签】
日语学习, 最后的里程, 满岛光, 冈田将生, 石原里美, 绫野刚, 冢原亚由子, 野木亚纪子, 看电影学日语, JLPT N5, JLPT N4, JLPT N3, JLPT N2, 日语听力, 日语影子跟读, 日本电影, 职场日语, 日语语法, TokyoFlow, 日语口语, 日语敬语"""

    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"# YouTube 视频标题\n```\n{title}\n```\n\n# YouTube 视频简介\n```\n{description}\n```\n")
    print(f"  [OK] 保存中文版视频元数据: {meta_path}")

def build_script_json_zh(output_dir: str):
    script_path = os.path.join(output_dir, "script.json")
    out_obj = {
        "metadata": EPISODE_METADATA_ZH,
        "screenplay": CINEMA_SCREENPLAY_ZH
    }
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)
    print(f"  [OK] 保存中文版剧本配置: {script_path}")

# ==========================================
# THUMBNAIL ENGINE (16:9 & 9:16 CHINESE EDITION)
# ==========================================

def render_master_thumbnail_zh(output_dir: str):
    """Generates 16:9 1080p Masterclass YouTube Thumbnail in Chinese conforming to strict Zero Emoji Discipline."""
    thumb_out = os.path.join(output_dir, "thumbnail.jpg")
    width, height = 1920, 1080

    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"

    if os.path.exists(hero_frame_path):
        raw_img = Image.open(hero_frame_path).convert("RGB")
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        base_img.paste(raw_img.resize((int(width * 1.1), int(height * 1.1)), Image.Resampling.LANCZOS), (80, -50))
    else:
        base_img = Image.new("RGB", (width, height), color=(10, 15, 28))

    # Photographic Contrast / Smooth Left Fade
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    import math
    for x in range(width):
        if x < 1180:
            rel = x / 1180.0
            alpha = int(248 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    # Bottom Vignette
    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left Brand Pill
    draw.rounded_rectangle([(60, 45), (420, 105)], radius=18, fill=(255, 255, 255))
    draw.text((85, 58), "TokyoFlow 日语实景", fill=(225, 29, 72), font=get_font(26))

    # 2. Top-Right Badge (WL.01)
    badge_text = "【JLPT N5-N2】WL.01"
    draw.rounded_rectangle([(width - 380, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 350, 58), badge_text, fill=(255, 255, 255), font=get_font(26))

    # 3. Giant 3D Yellow Hook (Left Aligned)
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

    # Also sync to assets/thumbnails
    asset_sync = os.path.join("assets/thumbnails", "WL01-last-mile-masterclass_zh_thumb.jpg")
    img.save(asset_sync, quality=95)
    site_sync = os.path.join("site/assets/thumbnails", "WL01-last-mile-masterclass_zh_thumb.jpg")
    os.makedirs(os.path.dirname(site_sync), exist_ok=True)
    img.save(site_sync, quality=95)
    docs_sync = os.path.join("docs/site/assets/thumbnails", "WL01-last-mile-masterclass_zh_thumb.jpg")
    os.makedirs(os.path.dirname(docs_sync), exist_ok=True)
    img.save(docs_sync, quality=95)
    print(f"  [OK] 同步至站点封面库: {asset_sync}")

def render_shorts_thumbnail_zh(output_dir: str):
    """Generates 9:16 Shorts Cover in Chinese."""
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
    for ch in CINEMA_SCREENPLAY_ZH:
        for seg in ch["segments"]:
            tasks.append(synthesize_audio_segment_zh(seg, audio_dir))

    await asyncio.gather(*tasks)
    print(f"  [OK] 全部中文版音频合成完毕: {len(tasks)} 段音频")

# ==========================================
# MAIN ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: WL.01《最后的里程》影视大课【中文解说版】生产管线")
    print(f" 编号: {EPISODE_METADATA_ZH['episode_code']} • 预估时长: {EPISODE_METADATA_ZH['target_duration_mins']} 分钟")
    print("================================================================================")

    output_dir = os.path.join("docs/youtube_releases", "WL01-last-mile-masterclass-v1.0-zh")
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
    print(f" WL.01 中文版发布套件全部生成完成: {output_dir}")
    print("================================================================================")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
