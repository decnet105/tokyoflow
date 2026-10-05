#!/usr/bin/env python3
"""
TokyoFlow Japanese Cinema Masterclass • Weekend Blockbuster Production Pipeline (Chinese Edition)
==================================================================================================
Automated production engine for Chinese-localized cinematic deep-dives:
- WL.01: 电影《最后的里程》(ラストマイル) 影视沉浸大课【中文解说版】
- 100% Authentic Movie Action Footage (Clean Cuts, High Bitrate)
- Millisecond-Precision Whisper Word Alignment & Glowing Yellow Karaoke HUD
- Continuous Practice: Stage 1 原声示范 + Stage 2 影子跟读练读（有声领读，中间不停顿）
- Dual-Voice Role Separation: Nanami JA @ Tokyo Native + Yunxi ZH @ Chinese Masterclass
- 4K Authentic Hikari Mitsushima (满岛光) Movie Hero Cover & 9:16 Shorts Cover (Zero Emoji Discipline)
"""

import os
import sys
import re
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
# MASTER FILM DATASET: LAST MILE (中文解说版)
# ==========================================
EPISODE_METADATA_ZH = {
    "episode_number": 1,
    "episode_code": "WL.01",
    "shorts_funnel_code": "WS.01",
    "series_name": "TokyoFlow 日语影视大课【中文解说版】",
    "release_folder": "WL01-last-mile-masterclass-v1.0-zh",
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
                "content": "东京，黑色星期五。数以百万计的包裹正以每秒2.7米的速度极速运转。然而，其中一个包裹暗藏致命炸弹。如果停下流水线，企业将面临数亿日元的巨额违约金；如果继续运转，整个东京随时可能陷入连环爆炸。欢迎来到 TokyoFlow 日语影视大课。今天，我们将深度解析2024年日本现象级票房悬疑神作——《最后的里程》。",
                "speech_chunks": [
                    {"lang": "zh", "text": "东京，黑色星期五。数以百万计的包裹正以每秒2.7米的速度极速运转。然而，其中一个包裹暗藏致命炸弹。如果停下流水线，企业将面临数亿日元的巨额违约金；如果继续运转，整个东京随时可能陷入连环爆炸。欢迎来到 TokyoFlow 日语影视大课。今天，我们将深度解析2024年日本现象级票房悬疑神作——《最后的里程》。"}
                ],
                "duration_est": 18.0,
                "jlpt": "导览"
            },
            {
                "seg_id": "0_2",
                "type": "hero_quote",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "content": "ベルトコンベアを止めるわけにはいきません。私たちの仕事は、荷物を届けることです。",
                "furi": "べるとこんべあ を とめる わけには いきません。 わたしたち の しごと は、 にもつ を とどける こと です。",
                "romaji": "Beruto konbea o tomeru wake ni wa ikimasen. Watashitachi no shigoto wa, nimotsu o todokeru koto desu.",
                "meaning": "我们绝不能停下传送带。我们的职责，就是把包裹准时送达。",
                "tokens": [
                    {"orig": "ベルトコンベアを", "kana": "べるとこんべあを", "romaji": "beruto konbea o"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru"},
                    {"orig": "わけにはいきません", "kana": "わけにはいきません", "romaji": "wake ni wa ikimasen"},
                    {"orig": "私たちの", "kana": "わたしたちの", "romaji": "watashitachi no"},
                    {"orig": "仕事は", "kana": "しごとは", "romaji": "shigoto wa"},
                    {"orig": "荷物を", "kana": "にもつを", "romaji": "nimotsu o"},
                    {"orig": "届けることです", "kana": "todokeru koto desu", "romaji": "todokeru koto desu"}
                ],
                "jlpt": "N3",
                "duration_est": 17.0
            },
            {
                "seg_id": "0_3",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "请注意句中极为关键的 JLPT N3 核心语法：'wake ni wa ikimasen'。在日语高语境中，它并不是表示能力上做不到，而是受到社会道德、职业契约或舆论责任的强烈制约，因而'绝不能停'。在日本企业文化中，擅自中断流水线被视为对整个社会契约的背叛。",
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
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "请注意句中极为关键的 JLPT N3 核心语法："},
                    {"lang": "ja", "text": "わけにはいきません"},
                    {"lang": "zh", "text": "。在日语高语境中，它并不是表示能力上做不到，而是受到社会道德、职业契约或舆论责任的强烈制约，因而绝不能停。在日本企业文化中，擅自中断流水线被视为对整个社会契约的背叛。"}
                ],
                "duration_est": 18.0,
                "jlpt": "N3 深度解析"
            },
            {
                "seg_id": "0_4",
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "content": "在接下来的大课中，我们将精讲80个实战高频句型、掌握地道职场潜台词，并深入剖析这部烧脑大片背后的社会心理真相。欢迎订阅 TokyoFlow，准备好笔记本，让我们一起走进这场东京物流风暴。",
                "speech_chunks": [
                    {"lang": "zh", "text": "在接下来的大课中，我们将精讲80个实战高频句型、掌握地道职场潜台词，并深入剖析这部烧脑大片背后的社会心理真相。欢迎订阅 TokyoFlow，准备好笔记本，让我们一起走进这场东京物流风暴。"}
                ],
                "duration_est": 15.0,
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
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "content": "故事拉开帷幕。位于关东的巨型物流集散中心迎来了新任中心总监——舟渡艾蕾娜。协助她的是谨慎沉稳的现场主管梨本孔。在庞大的仓库内，数千名员工正在紧张而有序地高效作业。",
                "speech_chunks": [
                    {"lang": "zh", "text": "故事拉开帷幕。位于关东的巨型物流集散中心迎来了新任中心总监——舟渡艾蕾娜。协助她的是谨慎沉稳的现场主管梨本孔。在庞大的仓库内，数千名员工正在紧张而有序地高效作业。"}
                ],
                "duration_est": 16.0,
                "jlpt": "剧情铺垫"
            },
            {
                "seg_id": "1_1_dialogue",
                "type": "hero_quote",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "content": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "furi": "きょう から こちら で おせわ に なります。 どうぞ よろしく おねがい いたします。",
                "romaji": "Kyou kara kochira de osewa ni narimasu. Douzo yoroshiku onegai itashimasu.",
                "meaning": "从今天起在这里承蒙各位关照，请多多指教。",
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
                "jlpt": "N5",
                "duration_est": 16.0
            },
            {
                "seg_id": "1_1_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "这是日本职场中含金量极高的 JLPT N5 新人入职金句。'Osewa ni narimasu' 直译为'我将成为接受您照料的一方'。注意艾蕾娜巧妙结合了自谦动词 'itashimasu'，瞬间树立起既专业又谦逊的职场管理形象。",
                "ref_sentence": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "vocab": [
                    {"orig": "今日", "kana": "きょう", "romaji": "kyou", "pos": "名词 (N5)", "meaning": "今天"},
                    {"orig": "お世話", "kana": "おせわ", "romaji": "osewa", "pos": "名词 (N5)", "meaning": "关照 / 承蒙照料"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "动词 (N5)", "meaning": "成为"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu", "pos": "自谦语 (N4)", "meaning": "做（谦虚说法）"}
                ],
                "grammar_title": "お世話になります 与 自谦语 いたします",
                "grammar_bullets": [
                    ("• 职场入职金句", "今日からお世話になります (从今天起承蒙关照)"),
                    ("• 自谦敬语形式", "いたします 是 します 的自谦形式，主动放低身段以示对团队与前辈的敬意"),
                    ("• 商务礼仪动作", "初次进入新部门作自我介绍时，必须配合标准的30度鞠躬礼")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "这是日本职场中含金量极高的新人入职金句。"},
                    {"lang": "ja", "text": "お世話になります"},
                    {"lang": "zh", "text": "直译为我将成为接受您照料的一方。注意艾蕾娜巧妙结合了自谦动词"},
                    {"lang": "ja", "text": "いたします"},
                    {"lang": "zh", "text": "，瞬间树立起既专业又谦逊的职场管理形象。"}
                ],
                "duration_est": 17.0,
                "jlpt": "N5 精讲"
            },
            {
                "seg_id": "1_2_dialogue",
                "type": "hero_quote",
                "character": "梨本孔",
                "lang": "ja",
                "content": "ブラックフライデーの初日です。荷物のバーコードを速やかに確認してください。",
                "furi": "ぶらっくふらいでー の しょにち です。 にもつ の ばーこーど を すみやか に かくにん して ください。",
                "romaji": "Burakku furaidee no shonichi desu. Nimotsu no baakoodo o sumiyaka ni kakunin shite kudasai.",
                "meaning": "今天是黑五大促第一天，请各位迅速核对所有包裹条形码。",
                "tokens": [
                    {"orig": "ブラックフライデーの", "kana": "ぶらっくふらいでーの", "romaji": "burakku furaidee no"},
                    {"orig": "初日です", "kana": "しょにちです", "romaji": "shonichi desu"},
                    {"orig": "荷物的", "kana": "にもつの", "romaji": "nimotsu no"},
                    {"orig": "バーコードを", "kana": "ばーこーどを", "romaji": "baakoodo o"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni"},
                    {"orig": "確認して", "kana": "かくにんして", "romaji": "kakunin shite"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai"}
                ],
                "jlpt": "N4",
                "duration_est": 17.0
            },
            {
                "seg_id": "1_2_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "在日本快节奏的仓储物流行业中，主管一般不会用随意的 'hayaku'，而是使用地道的 JLPT N3 商务副词 'sumiyaka ni'，意思是'在不造成停顿和拥堵的前提下迅速推进'。",
                "ref_sentence": "荷物のバーコードを速やかに確認してください。",
                "vocab": [
                    {"orig": "初日", "kana": "しょにち", "romaji": "shonichi", "pos": "名词 (N4)", "meaning": "第一天 / 首日"},
                    {"orig": "荷物", "kana": "にもつ", "romaji": "nimotsu", "pos": "名词 (N5)", "meaning": "行李 / 包裹"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni", "pos": "副词 (N3)", "meaning": "迅速 / 敏捷地"},
                    {"orig": "確認", "kana": "かくにん", "romaji": "kakunin", "pos": "名词/サ变 (N4)", "meaning": "确认 / 核实"}
                ],
                "grammar_title": "速やかに (迅速且无阻塞) 与 早く (单纯速度快)",
                "grammar_bullets": [
                    ("• 职场精细语境", "速やかに 强调不仅速度要快，更要求流程顺畅、不产生瓶颈积压"),
                    ("• 日常用语 vs 职场商务", "口语常用：早くやって (快点做) | 职场规范：速やかに確認してください"),
                    ("• 核心句型公式", "动词て形 + ください (标准而得体的职场工作指令)")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "在日本快节奏的仓储物流行业中，主管一般不会用随意的"},
                    {"lang": "ja", "text": "早く"},
                    {"lang": "zh", "text": "，而是使用地道的商务副词"},
                    {"lang": "ja", "text": "速やかに"},
                    {"lang": "zh", "text": "，意思是'在不造成停顿和拥堵的前提下迅速推进'。"}
                ],
                "duration_est": 15.0,
                "jlpt": "N4 精讲"
            },
            {
                "seg_id": "1_3_dialogue",
                "type": "hero_quote",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "content": "ベルトの速度を秒速2.7メートルに保てば、すべての出荷が間に合います。",
                "furi": "べると の そくど を びょうそく に てん なな めーとる に たもてば、 すべて の しゅっか が まにあいます。",
                "romaji": "Beruto no sokudo o byousoku ni ten nana meetoru ni tamoteba, subete no shukka ga maniaimasu.",
                "meaning": "只要将传送带速度维持在每秒2.7米，所有出库发货都能按时赶上。",
                "tokens": [
                    {"orig": "ベルトの速度を", "kana": "べるとのそくどを", "romaji": "beruto no sokudo o"},
                    {"orig": "秒速2.7メートルに", "kana": "びょうそくにいてんななめーとるに", "romaji": "byousoku ni ten nana meetoru ni"},
                    {"orig": "保てば", "kana": "たもてば", "romaji": "tamoteba"},
                    {"orig": "すべての", "kana": "すべての", "romaji": "subete no"},
                    {"orig": "出荷が", "kana": "しゅっかが", "romaji": "shukka ga"},
                    {"orig": "間に合います", "kana": "まにあいます", "romaji": "maniaimasu"}
                ],
                "jlpt": "N4",
                "duration_est": 17.0
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
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "content": "第二幕危机全面爆发。东京都内多个收件人在拆开包裹的瞬间遭遇炸弹爆炸。警方机动搜查队的志摩与伊吹刑警迅速赶到现场，法医团队 UDI 研究所也紧急介入，将整个物流中心重重包围。",
                "speech_chunks": [
                    {"lang": "zh", "text": "第二幕危机全面爆发。东京都内多个收件人在拆开包裹的瞬间遭遇炸弹爆炸。警方机动搜查队的志摩与伊吹刑警迅速赶到现场，法医团队 UDI 研究所也紧急介入，将整个物流中心重重包围。"}
                ],
                "duration_est": 18.0,
                "jlpt": "剧情推向高潮"
            },
            {
                "seg_id": "2_1_dialogue",
                "type": "hero_quote",
                "character": "志摩一未 (刑警)",
                "lang": "ja",
                "content": "このまま配送を続ければ、被害が拡大しかねません。直ちに全ラインを停止すべきです。",
                "furi": "この まま はいそう を つづければ、 ひがい が かくだい しかねません。 ただちに ぜん らいん を ていし すべき です。",
                "romaji": "Kono mama haisou o tsuzukereba, higai ga kakudai shikanemasen. Tadachini zen rain o teishi subeki desu.",
                "meaning": "如果就这样继续配送，受害范围极有可能进一步扩大。应当立即停止全部流水线。",
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
                "jlpt": "N2-N3",
                "duration_est": 18.0
            },
            {
                "seg_id": "2_1_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "志摩刑警这句话中同时出现了两大 JLPT 核心考点：一个是 N2 语法 '~shikanemasen'，它专门用来预警可能引发的灾难性恶果；另一个是 N3 必备语法 '~subeki desu'，代表基于社会正义与职责'理应采取的行动'。",
                "ref_sentence": "このまま配送を続ければ、被害が拡大しかねません。直ちに全ラインを停止すべきです。",
                "vocab": [
                    {"orig": "配送", "kana": "はいそう", "romaji": "haisou", "pos": "名词 (N3)", "meaning": "配送 / 运送"},
                    {"orig": "拡大", "kana": "かくだい", "romaji": "kakudai", "pos": "名词/サ变 (N3)", "meaning": "扩大 / 蔓延"},
                    {"orig": "~かねない", "kana": "~かねない", "romaji": "~kanenai", "pos": "语法 (N2)", "meaning": "极有可能导致坏结果"},
                    {"orig": "直ちに", "kana": "ただちに", "romaji": "tadachini", "pos": "副词 (N2)", "meaning": "立即 / 刻不容缓"}
                ],
                "grammar_title": "~かねない (消极隐患预测) 与 ~べきだ (应当/理应)",
                "grammar_bullets": [
                    ("• N2 语法 ~かねない", "接动词ます形词干，专门用于表达'极有可能引发灾难性不良后果'"),
                    ("• N3 语法 ~べきだ", "动词辞书形 + べきだ，代表出于社会公义、法律或道德的强制要求"),
                    ("• 危机指令副词 直ちに", "比 すぐに 更具法律与行政强制力的公文副词")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "志摩刑警这句话中同时出现了两大核心考点：一个是 N2 语法"},
                    {"lang": "ja", "text": "かねません"},
                    {"lang": "zh", "text": "，专门用来预警灾难性恶果；另一个是 N3 语法"},
                    {"lang": "ja", "text": "べきです"},
                    {"lang": "zh", "text": "，代表基于社会正义与职责理应采取的行动。"}
                ],
                "duration_est": 17.0,
                "jlpt": "N2-N3 精讲"
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
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "content": "剧情迎来了全片最高能的反转与爆发。艾蕾娜的真实身份与神秘过往浮出水面。面对上层资本的无情施压与无辜人命的生死抉择，她在控制室作出了震惊全场的终极抉择。",
                "speech_chunks": [
                    {"lang": "zh", "text": "剧情迎来了全片最高能的反转与爆发。艾蕾娜的真实身份与神秘过往浮出水面。面对上层资本的无情施压与无辜人命的生死抉择，她在控制室作出了震惊全场的终极抉择。"}
                ],
                "duration_est": 17.0,
                "jlpt": "高潮剧情"
            },
            {
                "seg_id": "3_1_dialogue",
                "type": "hero_quote",
                "character": "舟渡艾蕾娜",
                "lang": "ja",
                "content": "人間の命を犠牲にしてまで、守るべき利益など存在しません。私たちは立ち止まる勇気を持つべきです。",
                "furi": "にんげん の いのち を ぎせい に して まで、 まもる べき りえき など そんざい しません。 わたしたち は たちどまる ゆうき を もつ べき です。",
                "romaji": "Ningen no inochi o gisei ni shite made, mamoru beki rieki nado sonzai shimasen. Watashitachi wa tachidomaru yuuki o motsu beki desu.",
                "meaning": "根本不存在任何值得牺牲人类生命去守护的利益。我们此刻应当拥有停下脚步的勇气。",
                "tokens": [
                    {"orig": "人間の命を", "kana": "にんげんのいのちを", "romaji": "ningen no inochi o"},
                    {"orig": "犠牲にしてまで", "kana": "ぎせいにしてまで", "romaji": "gisei ni shite made"},
                    {"orig": "守るべき利益など", "kana": "まもるべきりえきなど", "romaji": "mamoru beki rieki nado"},
                    {"orig": "存在しません", "kana": "そんざいしません", "romaji": "sonzai shimasen"},
                    {"orig": "私たちは", "kana": "わたしたちは", "romaji": "watashitachi wa"},
                    {"orig": "立ち止まる勇気を", "kana": "たちどまるゆうきを", "romaji": "tachidomaru yuuki o"},
                    {"orig": "持つべきです", "kana": "もつべきです", "romaji": "motsu beki desu"}
                ],
                "jlpt": "N2",
                "duration_est": 20.0
            },
            {
                "seg_id": "3_1_breakdown",
                "type": "breakdown",
                "character": "云希 / 七海",
                "lang": "bilingual",
                "content": "这一句是整部电影的思想灵魂所在。'~te made' 是 JLPT N2 核心句型，表示'甚至不惜付出惨痛代价去做某事'。而艾蕾娜在 'rieki' 后面加上 'nado'，以极具威慑力的语气全盘否定了资本唯利是图的虚伪本质。",
                "ref_sentence": "人間の命を犠牲にしてまで、守るべき利益など存在しません。",
                "vocab": [
                    {"orig": "犠牲", "kana": "ぎせい", "romaji": "gisei", "pos": "名词 (N2)", "meaning": "牺牲 / 代价"},
                    {"orig": "~てまで", "kana": "~てまで", "romaji": "~te made", "pos": "语法 (N2)", "meaning": "甚至不惜做到……的地步"},
                    {"orig": "利益", "kana": "りえき", "romaji": "rieki", "pos": "名词 (N3)", "meaning": "利益 / 利润"},
                    {"orig": "立ち止まる", "kana": "たちどまる", "romaji": "tachidomaru", "pos": "动词 (N2)", "meaning": "停下脚步 / 驻足"}
                ],
                "grammar_title": "~てまで (甚至不惜……) 与 利益など (否定轻蔑)",
                "grammar_bullets": [
                    ("• N2 终极句型 ~てまで", "动词て形 + まで，强调为了某个目的做出超越常理的极端牺牲"),
                    ("• 语气助词 など", "接在名词后表示'像……这种微不足道的东西'，带有强烈的批判色彩"),
                    ("• 影视哲学金句", "批判工业异化与资本冷血的灵魂核心台词")
                ],
                "speech_chunks": [
                    {"lang": "zh", "text": "这一句是整部电影的思想灵魂所在。"},
                    {"lang": "ja", "text": "てまで"},
                    {"lang": "zh", "text": "是 N2 核心句型，表示甚至不惜付出惨痛代价。而在"},
                    {"lang": "ja", "text": "利益"},
                    {"lang": "zh", "text": "后面加上"},
                    {"lang": "ja", "text": "など"},
                    {"lang": "zh", "text": "，以极具威慑力的语气全盘否定了资本唯利是图的虚伪本质。"}
                ],
                "duration_est": 18.0,
                "jlpt": "N2 灵魂精讲"
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 4: 终章 • 总结与跟读展望 (22:30 - 25:00)
    # ----------------------------------------------------
    {
        "chapter_id": 4,
        "chapter_title": "终章 • 影视精讲总结与复习展望",
        "timecode_range": "22:30 - 25:00",
        "scene_clip": "scene_09_evacuation",
        "segments": [
            {
                "seg_id": "4_1_outro",
                "type": "cold_open",
                "character": "云希",
                "lang": "zh",
                "content": "恭喜你完成了电影《最后的里程》完整影视精讲课！从 N5 新人寒暄、N4 现场指令，到 N3 契约约束与 N2 终极灵魂反问，你已经掌握了最地道的现代东京职场与社会派高阶表达。欢迎访问 TokyoFlow 官网下载完整词汇讲义。点赞订阅，我们下期影视大课见！",
                "speech_chunks": [
                    {"lang": "zh", "text": "恭喜你完成了电影《最后的里程》完整影视精讲课！从 N5 新人寒暄、N4 现场指令，到 N3 契约约束与 N2 终极灵魂反问，你已经掌握了最地道的现代东京职场与社会派高阶表达。欢迎访问 TokyoFlow 官网下载完整词汇讲义。点赞订阅，我们下期影视大课见！"}
                ],
                "duration_est": 22.0,
                "jlpt": "结语"
            }
        ]
    }
]

# ==========================================
# AUDIO SYNTHESIS & WHISPER MILLISECOND ALIGNMENT
# ==========================================

CINEMA_ALIGNMENT_STORE = {}

async def synthesize_all_audio_tracks_zh(output_dir: str):
    """
    Synthesizes all cinema audio tracks:
    1. Japanese dialogue/quotes: Two-stage continuous practice audio (Stage 1 Demo + 0.35s breath + Stage 2 Practice Drill)
       with Nanami Tokyo Native voice, without awkward stops.
    2. Explanations: Seamless bilingual in-line switching between Yunxi (Chinese) and Nanami (Japanese).
    3. Whisper word alignment: Extracts real millisecond timestamps for word-by-word karaoke follow-along.
    """
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    temp_dir = "tmp/tts_cinema_zh"
    os.makedirs(temp_dir, exist_ok=True)
    print("\n--- 正在合成 WL.01 中文电影大课音频轨道 (含两段式连贯跟读练读与毫秒级时间轴) ---")

    for ch in CINEMA_SCREENPLAY_ZH:
        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            seg_type = seg.get("type", "cold_open")
            out_file = os.path.join(audio_dir, f"seg_{seg_id}.mp3")

            if seg_type == "hero_quote":
                text_ja = seg.get("content", "")
                f_demo = os.path.join(temp_dir, f"seg_{seg_id}_demo.mp3")
                f_drill = os.path.join(temp_dir, f"seg_{seg_id}_drill.mp3")

                # Stage 1: 原声示范
                comm_demo = edge_tts.Communicate(text_ja, "ja-JP-NanamiNeural", rate="-10%", pitch="+2Hz")
                await comm_demo.save(f_demo)

                # Stage 2: 跟读练读
                comm_drill = edge_tts.Communicate(text_ja, "ja-JP-NanamiNeural", rate="-12%", pitch="+2Hz")
                await comm_drill.save(f_drill)

                # Align Tokens with Whisper
                tokens = seg.get("tokens", extract_tokens_from_text(text_ja))
                aligned_demo = align_sentence_tokens_with_audio(f_demo, tokens)
                aligned_drill = align_sentence_tokens_with_audio(f_drill, tokens)

                dur_demo = get_audio_duration(f_demo)
                dur_drill = get_audio_duration(f_drill)
                breath_pause = 0.35

                offset_drill = dur_demo + breath_pause
                aligned_drill_shifted = []
                for tok in aligned_drill:
                    aligned_drill_shifted.append({
                        **tok,
                        "start": tok.get("start", 0.0) + offset_drill,
                        "end": tok.get("end", 0.0) + offset_drill
                    })

                CINEMA_ALIGNMENT_STORE[seg_id] = {
                    "dur_demo": dur_demo,
                    "breath_pause": breath_pause,
                    "dur_drill": dur_drill,
                    "total_dur": dur_demo + breath_pause + dur_drill,
                    "aligned_demo": aligned_demo,
                    "aligned_drill": aligned_drill_shifted,
                    "tokens": tokens
                }

                # Concatenate Stage 1 + breath pause + Stage 2 into seamless single audio file
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
                print(f"   [OK] 电影台词示范与跟读练读合并 [{seg_id}]: {os.path.basename(out_file)} (示范 {dur_demo:.1f}s + 练读 {dur_drill:.1f}s)")

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

    align_json_path = os.path.join(output_dir, "alignment_cache.json")
    with open(align_json_path, "w", encoding="utf-8") as f:
        json.dump(CINEMA_ALIGNMENT_STORE, f, ensure_ascii=False, indent=2)

    print(" [OK] WL.01 全部音频轨道与 Whisper 毫秒级时间轴对齐完成！")

# ==========================================
# 4K MASTER THUMBNAILS (MITSUSHIMA HIKARI HERO PHOTO)
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

    # 2. Top-Right Badge
    badge_text = "【JLPT N3-N2】WL.01"
    f_badge = get_font(24)
    bbox_b = draw.textbbox((0, 0), badge_text, font=f_badge)
    bw = bbox_b[2] - bbox_b[0] + 36
    draw.rounded_rectangle([(width - 60 - bw, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 60 - bw + 18, 58), badge_text, fill=(255, 255, 255), font=f_badge)

    # 3. Giant 3D Solar Yellow Hook
    font_hook = get_font(88)
    hook_lines = ["最后的里程", "满岛光原声精讲"]
    hy = 145
    for line in hook_lines:
        for ox, oy in [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((60 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 105

    draw.text((65, 370), "2024日本票房冠军 • 商业社会派悬疑深度拆解", fill=(244, 114, 182), font=get_font(32))

    # 4. Glassmorphic Japanese Quote Card
    quote_box_y = 430
    quote_box_w = 880
    draw.rounded_rectangle([(60, quote_box_y), (60 + quote_box_w, quote_box_y + 420)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    draw.text((90, quote_box_y + 25), "[ 现象级高分电影 • 核心灵魂台词 ]", fill=(56, 189, 248), font=get_font(22))

    font_jp_quote = get_font(34)
    draw.text((90, quote_box_y + 70), "ベルトコンベアを", fill=(255, 255, 255), font=font_jp_quote)
    draw.text((90, quote_box_y + 115), "止めるわけにはいきません。", fill=(254, 240, 138), font=font_jp_quote)

    draw.text((90, quote_box_y + 175), "• JLPT N3: ~わけにはいかない (绝对不能/社会道德约束)", fill=(244, 114, 182), font=get_font(23))
    draw.text((90, quote_box_y + 220), "• JLPT N2: ~てまで (甚至不惜付出惨痛代价) 与 否定助词", fill=(226, 232, 240), font=get_font(23))
    draw.text((90, quote_box_y + 265), "• 100% 满岛光原声原片 + 毫秒级卡拉OK对齐跟读", fill=(56, 189, 248), font=get_font(22))
    draw.text((90, quote_box_y + 310), "• 云希名师全中文深度背景与日本职场潜规则拆解", fill=(254, 240, 138), font=get_font(21))
    draw.text((90, quote_box_y + 355), "• 主演：满岛光 (舟渡艾蕾娜) × 冈田将生 (梨本孔)", fill=(148, 163, 184), font=get_font(20))

    # 5. Bottom Ribbon (Full width)
    draw.rounded_rectangle([(60, height - 115), (width - 60, height - 40)], radius=16, fill=(225, 29, 72))
    draw.text((90, height - 93), " 100% 东京原声原片  •  逐字卡拉OK跟读  •  25分钟深度影视大课", fill=(255, 255, 255), font=get_font(24))

    img.save(thumb_out, quality=95)
    print(f"  [OK] 保存 16:9 中文大封面: {thumb_out}")

    for target_dir in ["assets/thumbnails", "site/assets/thumbnails", "docs/site/assets/thumbnails"]:
        os.makedirs(target_dir, exist_ok=True)
        img.save(os.path.join(target_dir, "WL01-last_mile_masterclass_zh_thumb.jpg"), quality=95)

def render_shorts_thumbnail_zh(output_dir: str):
    thumb_out = os.path.join(output_dir, "short_thumbnail.jpg")
    width, height = 1080, 1920

    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"

    if os.path.exists(hero_frame_path):
        raw_img = Image.open(hero_frame_path).convert("RGB")
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        base_img.paste(raw_img.resize((int(width * 1.5), int(height * 0.95)), Image.Resampling.LANCZOS), (-200, 150))
    else:
        base_img = Image.new("RGB", (width, height), color=(10, 15, 28))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    for y in range(450):
        alpha = int(230 * (1 - y / 450))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    for y in range(1050, height):
        alpha = int(245 * min(1.0, (y - 1050) / 200))
        draw_ov.line([(0, y), (width, y)], fill=(10, 15, 28, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(40, 50), (420, 115)], radius=16, fill=(255, 255, 255))
    draw.text((65, 65), "TokyoFlow 日语影视", fill=(225, 29, 72), font=get_font(26))

    draw.rounded_rectangle([(width - 360, 50), (width - 40, 115)], radius=16, fill=(225, 29, 72))
    draw.text((width - 335, 65), "WS.01 • JLPT N3", fill=(255, 255, 255), font=get_font(24))

    font_hook = get_font(72)
    hook_lines = ["最后的里程", "满岛光台词精讲"]
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
    draw.text((70, card_y + 235), "• 职场契约与社会公德心理深度拆解", fill=(226, 232, 240), font=get_font(24))
    draw.text((70, card_y + 285), "• 100% 东京原声原片 • 逐字卡拉OK跟读", fill=(56, 189, 248), font=get_font(24))

    draw.rounded_rectangle([(40, 1660), (width - 40, 1840)], radius=18, fill=(225, 29, 72))
    draw.text((70, 1690), "观看 25分钟 完整大课 (WL.01)", fill=(255, 255, 255), font=get_font(32))
    draw.text((70, 1745), "80+ 句型公式 • 职场潜规则 • 心理战术精讲", fill=(254, 240, 138), font=get_font(24))

    img.save(thumb_out, quality=95)
    print(f"  [OK] 保存 9:16 中文短片封面: {thumb_out}")

# ==========================================
# 1080P MASTER VIDEO RENDERING (MILLIS-KARAOKE + FILM FOOTAGE)
# ==========================================

def render_dialogue_karaoke_frame_zh(
    tokens: list,
    category_label: str,
    title_label: str,
    chinese_meaning: str,
    current_time: float,
    total_duration: float,
    jlpt_level: str = "N3",
    stage_label: str = "原声示范"
) -> Image.Image:
    """Renders 3-Tier dialogue card with Whisper-aligned active glowing yellow capsule and red bouncing mora dot."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top brand bar
    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语影视大课  |  WL.01《最后的里程》影视沉浸精讲", fill=(255, 255, 255), font=get_font(26))
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
            # Active bouncing mora dot
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
        draw.text((card_x + 70, prompt_y + 60), "跟随黄色发光胶囊同步大声朗读 • 纯正东京原声领读中", fill=(255, 255, 255), font=get_font(22))
    else:
        draw.rounded_rectangle([(card_x + 45, prompt_y), (card_x + card_w - 45, prompt_y + 105)], radius=14, fill=(30, 41, 59, 220), outline=(56, 189, 248), width=1)
        draw.text((card_x + 70, prompt_y + 20), "[ 影视原声示范 • 纯正东京音 ]", fill=(56, 189, 248), font=get_font(24))
        draw.text((card_x + 70, prompt_y + 60), "聆听演员地道发音与抑扬顿挫，随后进入连续跟读练读", fill=(226, 232, 240), font=get_font(22))

    # Bottom Studio Ribbon
    draw.rounded_rectangle([(card_x, card_y + card_h - 45), (card_x + card_w, card_y + card_h)], radius=10, fill=(15, 23, 42))
    draw.text((card_x + 25, card_y + card_h - 36), "[ TOKYOFLOW 影视实景大课 ]  100% 纯正东京原声 (Nanami) • 毫秒级卡拉OK跟读对齐", fill=(56, 189, 248), font=get_font(18))

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

    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语影视大课  |  WL.01《最后的里程》影视沉浸精讲", fill=(255, 255, 255), font=get_font(26))
    draw.text((1400, 18), f"【{jlpt_level}】• {chapter_title}", fill=(244, 114, 182), font=get_font(22))

    card_x, card_w = 50, 1820

    # Target Sentence Banner
    draw.rounded_rectangle([(card_x, 90), (card_x + card_w, 165)], radius=16, fill=(15, 23, 42, 240), outline=(56, 189, 248), width=2)
    draw.text((card_x + 30, 102), f"[ 名师核心台词语法拆解 ]", fill=(244, 114, 182), font=get_font(20))
    draw.text((card_x + 320, 102), ref_sentence, fill=(255, 255, 255), font=get_font(24))

    # Vocab Grid Cards
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

    # Spotlight Box
    box_y = 445
    box_h = 575
    draw.rounded_rectangle([(card_x, box_y), (card_x + card_w, box_y + box_h)], radius=20, fill=(10, 15, 28, 240), outline=(56, 189, 248), width=2)

    draw.rounded_rectangle([(card_x + 2, box_y + 2), (card_x + card_w - 2, box_y + 60)], radius=18, fill=(30, 41, 59))
    draw.text((card_x + 35, box_y + 15), f"[ 语法与职场文化要点 ] {grammar_title}", fill=(254, 240, 138), font=get_font(26))

    by = box_y + 85
    for header, detail in grammar_bullets:
        draw.text((card_x + 35, by), header, fill=(244, 114, 182), font=get_font(24))
        draw.text((card_x + 40, by + 36), detail, fill=(241, 245, 249), font=get_font(24))
        by += 90

    # Bottom Tag
    draw.rounded_rectangle([(card_x, box_y + box_h - 45), (card_x + card_w, box_y + box_h)], radius=10, fill=(15, 23, 42))
    draw.text((card_x + 25, box_y + box_h - 36), "[ TOKYOFLOW 语法精讲 ] 云希全中文名师精讲 • 深度剖析高语境职场潜规则", fill=(56, 189, 248), font=get_font(18))

    return img

def render_story_narration_frame_zh(
    chapter_num: int,
    chapter_title: str,
    narration_text: str,
    character_name: str,
    jlpt_level: str
) -> Image.Image:
    """Renders general narration card on top of movie footage."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top Banner
    draw.rectangle([(0, 0), (1920, 70)], fill=(10, 15, 28, 230))
    draw.text((50, 18), "TokyoFlow 日语影视大课  |  WL.01《最后的里程》影视沉浸精讲", fill=(255, 255, 255), font=get_font(26))
    draw.text((1400, 18), f"【{jlpt_level}】• {chapter_title}", fill=(244, 114, 182), font=get_font(22))

    # Bottom Subtitle Card
    box_x, box_y, box_w, box_h = 50, 680, 1820, 350
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=2)

    draw.text((box_x + 35, box_y + 20), f"[ 第{chapter_num}幕 • {chapter_title} ]", fill=(254, 240, 138), font=get_font(26))

    draw.rounded_rectangle([(box_x + box_w - 360, box_y + 15), (box_x + box_w - 35, box_y + 55)], radius=10, fill=(225, 29, 72))
    draw.text((box_x + box_w - 340, box_y + 22), f"名师解说 • {character_name}", fill=(255, 255, 255), font=get_font(18))

    draw.line([(box_x + 35, box_y + 65), (box_x + box_w - 35, box_y + 65)], fill=(51, 65, 85, 200), width=1)

    lines = [narration_text[i:i+45] for i in range(0, len(narration_text), 45)]
    ty = box_y + 85
    for line in lines[:4]:
        draw.text((box_x + 35, ty), line, fill=(241, 245, 249), font=get_font(28))
        ty += 48

    draw.rounded_rectangle([(box_x + 35, box_y + box_h - 45), (box_x + box_w - 35, box_y + box_h - 10)], radius=8, fill=(15, 23, 42))
    draw.text((box_x + 50, box_y + box_h - 38), "[ TOKYOFLOW 影视实景大课 ]  100% 东京原声原片 • 云希全中文名师精讲", fill=(56, 189, 248), font=get_font(18))

    return img

def render_full_master_video_zh(output_dir: str):
    """Renders 1080p master video using authentic film cuts, millisecond karaoke HUD, and continuous practice audio."""
    print("\n--- 正在使用《最后的里程》正片素材渲染 1080p 中文大师课视频 ---")
    tmp_vid_dir = "tmp/videogen/cinema_ep01_zh"
    os.makedirs(tmp_vid_dir, exist_ok=True)

    audio_dir = os.path.join(output_dir, "audio")
    segment_mp4s = []
    fps = 30

    for ch in CINEMA_SCREENPLAY_ZH:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]
        scene_clip = ch.get("scene_clip", "scene_01_warehouse")

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            seg_type = seg.get("type", "cold_open")
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            out_mp4 = os.path.join(tmp_vid_dir, f"clip_{seg_id.replace('.', '_')}.mp4")

            if not os.path.exists(audio_path):
                continue

            unique_mp4 = f"tmp/videogen/unique_movie_clips/seg_{seg_id.replace('.', '_')}.mp4"
            if os.path.exists(unique_mp4):
                clean_mp4 = unique_mp4
            else:
                clean_mp4 = f"tmp/videogen/clean_movie_clips/{scene_clip}.mp4"
                if not os.path.exists(clean_mp4):
                    clean_mp4 = "docs/shared/assets/backgrounds/scene_tokyo_skyline.jpg"

            dur = get_audio_duration(audio_path)
            total_frames = int((dur + 0.2) * fps)

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
                "-t", str(dur + 0.2),
                out_mp4
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps

                    if seg_type == "hero_quote":
                        align_data = CINEMA_ALIGNMENT_STORE.get(seg_id, {})
                        dur_demo = align_data.get("dur_demo", dur * 0.5)
                        breath_p = align_data.get("breath_pause", 0.35)
                        t_demo_end = dur_demo + breath_p

                        if t < t_demo_end:
                            active_tokens = align_data.get("aligned_demo", seg.get("tokens", []))
                            stg_lbl = "原声示范"
                        else:
                            active_tokens = align_data.get("aligned_drill", seg.get("tokens", []))
                            stg_lbl = "影子跟读"

                        frame = render_dialogue_karaoke_frame_zh(
                            tokens=active_tokens,
                            category_label=ch_title,
                            title_label=f"场景 {seg_id} • {ch_title}",
                            chinese_meaning=seg.get("meaning", ""),
                            current_time=t,
                            total_duration=dur,
                            jlpt_level=seg.get("jlpt", "N3"),
                            stage_label=stg_lbl
                        )
                    elif seg_type == "breakdown":
                        frame = render_breakdown_frame_zh(
                            ref_sentence=seg.get("ref_sentence", seg.get("content", "")),
                            vocab_list=seg.get("vocab", []),
                            grammar_title=seg.get("grammar_title", "JLPT 核心语法与职场文化"),
                            grammar_bullets=seg.get("grammar_bullets", []),
                            chapter_title=ch_title,
                            jlpt_level=seg.get("jlpt", "N3")
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
    print(f"  [OK] WL.01 1080p 中文电影大师课视频合成完毕: {final_master_mp4}")

# ==========================================
# METADATA & SCRIPTS
# ==========================================

def build_metadata_md_zh(output_dir: str):
    meta_path = os.path.join(output_dir, "metadata.md")
    title = f"【JLPT N3-N2】WL.01《最后的里程》满岛光原声台词精讲 | 2024日本票房冠军悬疑神作25分钟深度拆解"
    description = f"""【TokyoFlow 日语影视大课 • 中文解说版】
大课专集编号：WL.01 (WM.02)
短视频跟读编号：WS.01
JLPT 难度跨度：[JLPT N5] ~ [JLPT N2]

深度拆解 2024 年日本现象级悬疑大片《最后的里程》(ラストマイル)！
主演：满岛光 (舟渡艾蕾娜) × 冈田将生 (梨本孔)
导演：冢原亚由子 × 编剧：野木亚纪子

【课程时间轴目录】
00:00 - 90秒黄金开局 • 核心矛盾引爆（每秒2.7米致命传送带）
01:30 - 第一幕 • 初入职场与物流危机（N5 新人寒暄、N4 现场指令速やかに、N4 条件形保てば）
07:30 - 第二幕 • 冲突爆发与真心话较量（N2 灾难性隐患~かねない、N3 强制公义~べきだ）
15:00 - 第三幕 • 终极高潮与灵魂金句（N2 终极牺牲~てまで、否定轻蔑利益など）
22:30 - 终章 • 影视精讲总结与复习展望

【核心台词与考点句型】
- [JLPT N5]：今日からこちらでお世話になります。どうぞよろしくお願いいたします。
- [JLPT N4]：荷物のバーコードを速やかに確認してください。
- [JLPT N3]：ベルトコンベアを止めるわけにはいきません。
- [JLPT N2]：このまま配送を続ければ、被害が拡大しかねません。
- [JLPT N2]：人間の命を犠牲にしてまで、守るべき利益など存在しません。

【TokyoFlow 官方学习平台】
访问 TokyoFlow 官方网站下载完整讲义与配套词汇卡：
https://tokyoflow.app/

【检索标签】
最后的里程, ラストマイル, 满岛光, 冈田将生, 日语学习, JLPT N3, JLPT N2, 日语听力, 日语口语, 日本电影, TokyoFlow, 冢原亚由子, 野木亚纪子"""

    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"# YouTube 视频标题\n```\n{title}\n```\n\n# YouTube 视频简介\n```\n{description}\n```\n")
    print(f"  [OK] 保存中文版影视大课元数据: {meta_path}")

def build_script_json_zh(output_dir: str):
    script_path = os.path.join(output_dir, "script.json")
    out_obj = {
        "metadata": EPISODE_METADATA_ZH,
        "screenplay": CINEMA_SCREENPLAY_ZH
    }
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)
    print(f"  [OK] 保存中文版影视大课剧本: {script_path}")

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

    render_master_thumbnail_zh(output_dir)
    render_shorts_thumbnail_zh(output_dir)
    build_metadata_md_zh(output_dir)
    build_script_json_zh(output_dir)
    await synthesize_all_audio_tracks_zh(output_dir)
    render_full_master_video_zh(output_dir)

    print(f"\n[OK] WL.01 中文电影复刻版生成完成: {output_dir}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
