#!/usr/bin/env python3
"""
TokyoFlow Japanese Cinema Masterclass • Weekend Blockbuster Production Pipeline (V2)
=====================================================================================
Automated end-to-end production engine for 25-minute bilingual cinematic deep-dives:
- 100% Authentic Movie Action Footage (Clean Cuts, ZERO Roadshow/Text Slates)
- Real-time Word-by-Word Karaoke Follow-Along Subtitles (Glowing Gold Capsule & Red Dot)
- Micro-Lesson Sentence Breakdown HUD (Vocabulary Grid + Active Grammar Spotlight)
- Strict Dual-Voice Separation (Andrew 100% EN / Nanami 100% JA with Slow, Crisp Speed)
- Seamless Anti-Pop 44.1kHz Stereo Audio Engine
- 4K/1080p Storyboard Slides, Metadata, Specs, and Final Concatenated Master Movie
"""

import os
import sys
import re
import glob
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
# MASTER FILM DATASET: LAST MILE (ラストマイル)
# ==========================================
EPISODE_METADATA = {
    "episode_number": 1,
    "episode_code": "WL.01",
    "shorts_funnel_code": "WS.01",
    "series_name": "Weekend Long-form Japanese Cinema Masterclass",
    "slug": "last_mile_2024",
    "movie_title_en": "Last Mile",
    "movie_title_ja": "ラストマイル",
    "release_year": 2024,
    "director": "Ayuko Tsukahara",
    "screenplay": "Akiko Nogi",
    "starring": ["Hikari Mitsushima", "Masaki Okada", "Dean Fujioka", "Satomi Ishihara", "Go Ayano"],
    "genre": "Suspense / Corporate Crime Mystery / High-Stakes Logistics",
    "target_duration_mins": 25,
    "jlpt_distribution": {
        "N5": "30%",
        "N4": "30%",
        "N3": "25%",
        "N2": "15%"
    },
    "core_dilemma": "When parcels begin exploding on Black Friday across Tokyo, can a mega-logistics center stop its conveyor belts, or will corporate greed sacrifice innocent human lives?"
}

# 6-Chapter Cinematic Screenplay Structure
CINEMA_SCREENPLAY = [
    # ----------------------------------------------------
    # CHAPTER 0: THE 90-SECOND GOLDEN OPENING (00:00 - 01:30)
    # ----------------------------------------------------
    {
        "chapter_id": 0,
        "chapter_title": "THE 90-SECOND GOLDEN OPENING",
        "timecode_range": "00:00 - 01:30",
        "scene_clip": "scene_01_warehouse",
        "segments": [
            {
                "seg_id": "0.1",
                "type": "cold_open",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Tokyo, Black Friday. Millions of packages are moving at 2.7 meters per second. But inside one of these boxes is a bomb. If the belt stops, the company loses hundreds of millions of yen. If it keeps running, Tokyo explodes. Welcome to TokyoFlow Cinema Masterclass. Today, we break down Japan's biggest 2024 box office masterpiece: Last Mile.",
                "duration_est": 18.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "0.2",
                "type": "hero_quote",
                "character": "Elena Funado",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ベルトコンベアを止めるわけにはいきません。私たちの仕事は、荷物を届けることです。",
                "furi": "べるとこんべあ を とめる わけには いきません。 わたしたち の しごと は、 にもつ を とどける こと です。",
                "romaji": "Beruto konbea o tomeru wake ni wa ikimasen. Watashitachi no shigoto wa, nimotsu o todokeru koto desu.",
                "meaning": "We cannot afford to stop the conveyor belt. Our job is to deliver the packages.",
                "jlpt": "N3",
                "grammar": "~わけにはいかない (Cannot afford to / Bound by social obligation)",
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
                    {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea", "pos": "Noun", "meaning": "Conveyor belt"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru", "pos": "Verb (N4)", "meaning": "To stop / Halt"},
                    {"orig": "わけにはいかない", "kana": "わけにはいかない", "romaji": "wake ni wa ikanai", "pos": "Grammar (N3)", "meaning": "Cannot afford to"},
                    {"orig": "届ける", "kana": "とどける", "romaji": "todokeru", "pos": "Verb (N4)", "meaning": "To deliver"}
                ],
                "grammar_title": "~わけにはいかない (Social & Moral Constraint)",
                "grammar_bullets": [
                    ("• Grammatical Formula", "Verb Dictionary Form + わけにはいかない / わけにはいきません"),
                    ("• Core Psychological Nuance", "Not physically unable, but restrained by duty, reputation, or social contract"),
                    ("• Tokyo Business Context", "Stopping the warehouse belt means breaking an unwritten corporate contract with society")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "0.3",
                "type": "instant_breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Notice that JLPT N3 powerhouse: 'wake ni wa ikimasen'. It doesn't mean physically unable. It means moral and social pressure prevents you from doing it. In Japanese corporate culture, stopping the line is seen as breaking an unwritten contract with society.",
                "duration_est": 16.0,
                "jlpt": "N3 Breakdown",
                "ref_sentence": "ベルトコンベアを止めるわけにはいきません。",
                "vocab": [
                    {"orig": "ベルトコンベア", "kana": "べるとこんべあ", "romaji": "beruto konbea", "pos": "Noun", "meaning": "Conveyor belt"},
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru", "pos": "Verb (N4)", "meaning": "To stop / Halt"},
                    {"orig": "わけにはいかない", "kana": "わけにはいかない", "romaji": "wake ni wa ikanai", "pos": "Grammar (N3)", "meaning": "Cannot afford to"},
                    {"orig": "届ける", "kana": "とどける", "romaji": "todokeru", "pos": "Verb (N4)", "meaning": "To deliver"}
                ],
                "grammar_title": "~わけにはいかない (Social & Moral Constraint)",
                "grammar_bullets": [
                    ("• Grammatical Formula", "Verb Dictionary Form + わけにはいかない / わけにはいきません"),
                    ("• Core Psychological Nuance", "Not physically unable, but restrained by duty, reputation, or social contract"),
                    ("• Tokyo Business Context", "Stopping the warehouse belt means breaking an unwritten corporate contract with society")
                ]
            },
            {
                "seg_id": "0.4",
                "type": "channel_cta",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Over the next twenty-five minutes, you will master eighty essential JLPT N5 to N2 phrases, real Tokyo workplace nuance, and the psychological truth behind this gripping film. Hit subscribe now, grab your notebook, and let us step inside Tokyo's ultimate logistics crisis.",
                "duration_est": 14.5,
                "jlpt": "CTA"
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 1: THE SPARK — SURVIVAL IN TOKYO (01:30 - 07:30)
    # ----------------------------------------------------
    {
        "chapter_id": 1,
        "chapter_title": "THE SPARK — SURVIVAL IN TOKYO",
        "timecode_range": "01:30 - 07:30",
        "scene_clip": "scene_02_elena",
        "segments": [
            {
                "seg_id": "1.1_narration",
                "type": "story_setup",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Act One begins inside Daily Fast's colossal Kanto Distribution Center. Elena Funado arrives as the newly appointed Center Director. Alongside her is Ko Nashimoto, the cautious site manager. On the warehouse floor, thousands of workers move in synchronized precision.",
                "duration_est": 16.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "1.1_dialogue",
                "type": "dialogue_n5",
                "character": "Elena Funado",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "furi": "きょう から こちら で おせわ に なります。 どうぞ よろしく おねがい いたします。",
                "romaji": "Kyou kara kochira de osewa ni narimasu. Douzo yoroshiku onegai itashimasu.",
                "meaning": "I will be in your care starting today. I look forward to working with you.",
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
                    {"orig": "今日", "kana": "きょう", "romaji": "kyou", "pos": "Noun (N5)", "meaning": "Today"},
                    {"orig": "お世話", "kana": "おせわ", "romaji": "osewa", "pos": "Noun (N5)", "meaning": "Care / Favor"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "Verb (N5)", "meaning": "To become"},
                    {"orig": "よろしく", "kana": "よろしく", "romaji": "yoroshiku", "pos": "Adv (N5)", "meaning": "Favorably"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu", "pos": "Kenjougo (N4)", "meaning": "Humble 'Do'"}
                ],
                "grammar": "お世話になります (Essential Japanese self-introduction greeting) + いたします (Humble kenjougo)",
                "grammar_title": "お世話になります & Humble いたします",
                "grammar_bullets": [
                    ("• Self-Introduction Standard", "今日からお世話になります (I will be in your care from today)"),
                    ("• Humble Kenjougo Form", "いたします is the humble equivalent of します, lowering yourself to respect the team"),
                    ("• Tokyo Workplace Etiquette", "Always deliver with a crisp 30-degree bow when entering a new department")
                ],
                "duration_est": 7.0
            },
            {
                "seg_id": "1.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "This is the gold standard JLPT N5 workplace greeting. 'Osewa ni narimasu' literally translates to 'I will become a recipient of your care'. Notice how Elena combines it with the humble verb 'itashimasu' to establish immediate professional respect.",
                "duration_est": 17.0,
                "jlpt": "N5 Breakdown",
                "ref_sentence": "今日からこちらでお世話になります。どうぞよろしくお願いいたします。",
                "vocab": [
                    {"orig": "今日", "kana": "きょう", "romaji": "kyou", "pos": "Noun (N5)", "meaning": "Today"},
                    {"orig": "お世話", "kana": "おせわ", "romaji": "osewa", "pos": "Noun (N5)", "meaning": "Care / Favor"},
                    {"orig": "なる", "kana": "なる", "romaji": "naru", "pos": "Verb (N5)", "meaning": "To become"},
                    {"orig": "よろしく", "kana": "よろしく", "romaji": "yoroshiku", "pos": "Adv (N5)", "meaning": "Favorably"},
                    {"orig": "いたします", "kana": "いたします", "romaji": "itashimasu", "pos": "Kenjougo (N4)", "meaning": "Humble 'Do'"}
                ],
                "grammar_title": "お世話になります & Humble いたします",
                "grammar_bullets": [
                    ("• Self-Introduction Standard", "今日からお世話になります (I will be in your care from today)"),
                    ("• Humble Kenjougo Form", "いたします is the humble equivalent of します, lowering yourself to respect the team"),
                    ("• Tokyo Workplace Etiquette", "Always deliver with a crisp 30-degree bow when entering a new department")
                ]
            },
            {
                "seg_id": "1.2_dialogue",
                "type": "dialogue_n5_n4",
                "character": "Ko Nashimoto",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ブラックフライデーの初日です。荷物のバーコードを速やかに確認してください。",
                "furi": "ぶらっくふらいでー の しょにち です。 にもつ の ばーこーど を すみやか に かくにん して ください。",
                "romaji": "Burakku furaidee no shonichi desu. Nimotsu no baakoodo o sumiyaka ni kakunin shite kudasai.",
                "meaning": "Today is the first day of Black Friday. Please verify the parcel barcodes promptly.",
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
                    {"orig": "初日", "kana": "しょにち", "romaji": "shonichi", "pos": "Noun (N4)", "meaning": "First day"},
                    {"orig": "荷物", "kana": "にもつ", "romaji": "nimotsu", "pos": "Noun (N5)", "meaning": "Parcel / Cargo"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni", "pos": "Adv (N3)", "meaning": "Promptly / Swiftly"},
                    {"orig": "確認", "kana": "かくにん", "romaji": "kakunin", "pos": "Noun/Suru (N4)", "meaning": "Verification / Check"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "Helper (N5)", "meaning": "Please"}
                ],
                "grammar": "~てください (Polite request) + 速やかに (Formal workplace adverb)",
                "grammar_title": "速やかに (Promptly) vs 速く (Fast)",
                "grammar_bullets": [
                    ("• Workplace Nuance", "速やかに means swiftly and smoothly without causing bottleneck disruptions"),
                    ("• Casual vs Business", "Casual: 早くやって (Do it fast) | Business: 速やかに確認してください"),
                    ("• Key Formula", "Verb て-form + ください (Standard professional instruction)")
                ],
                "duration_est": 7.5
            },
            {
                "seg_id": "1.2_breakdown",
                "type": "pedagogical_lesson",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "In Japanese fast-paced operations, instead of using 'hayaku', professionals use 'sumiyaka ni'—a crisp JLPT N3 adverb meaning swiftly and smoothly without disruption.",
                "duration_est": 13.0,
                "jlpt": "N4 Breakdown",
                "ref_sentence": "荷物のバーコードを速やかに確認してください。",
                "vocab": [
                    {"orig": "初日", "kana": "しょにち", "romaji": "shonichi", "pos": "Noun (N4)", "meaning": "First day"},
                    {"orig": "荷物", "kana": "にもつ", "romaji": "nimotsu", "pos": "Noun (N5)", "meaning": "Parcel / Cargo"},
                    {"orig": "速やかに", "kana": "すみやかに", "romaji": "sumiyaka ni", "pos": "Adv (N3)", "meaning": "Promptly / Swiftly"},
                    {"orig": "確認", "kana": "かくにん", "romaji": "kakunin", "pos": "Noun/Suru (N4)", "meaning": "Verification / Check"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai", "pos": "Helper (N5)", "meaning": "Please"}
                ],
                "grammar_title": "速やかに (Promptly) vs 速く (Fast)",
                "grammar_bullets": [
                    ("• Workplace Nuance", "速やかに means swiftly and smoothly without causing bottleneck disruptions"),
                    ("• Casual vs Business", "Casual: 早くやって (Do it fast) | Business: 速やかに確認してください"),
                    ("• Key Formula", "Verb て-form + ください (Standard professional instruction)")
                ]
            },
            {
                "seg_id": "1.3_dialogue",
                "type": "dialogue_n4",
                "character": "Elena Funado",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ベルトの速度を秒速2.7メートルに保てば、すべての出荷が間に合います。",
                "furi": "べると の そくど を びょうそく に てん なな めーとる に たもてば、 すべて の しゅっか が まにあいます。",
                "romaji": "Beruto no sokudo o byousoku ni ten nana meetoru ni tamoteba, subete no shukka ga maniaimasu.",
                "meaning": "If we maintain the belt speed at 2.7 meters per second, all shipments will be on time.",
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
                    {"orig": "速度", "kana": "そくど", "romaji": "sokudo", "pos": "Noun (N4)", "meaning": "Speed / Velocity"},
                    {"orig": "保つ", "kana": "たもつ", "romaji": "tamotsu", "pos": "Verb (N3)", "meaning": "To maintain / Keep"},
                    {"orig": "出荷", "kana": "しゅっか", "romaji": "shukka", "pos": "Noun (N3)", "meaning": "Shipment / Dispatch"},
                    {"orig": "間に合う", "kana": "まにあう", "romaji": "maniau", "pos": "Verb (N4)", "meaning": "To be in time for"}
                ],
                "grammar": "~ば条件形 (Hypothetical conditional: If ... then) + 間に合う (To be on time)",
                "grammar_title": "~ば Conditional & 間に合う (On Time)",
                "grammar_bullets": [
                    ("• Conditional Formula", "Verb e-row + ば (保つ -> 保てば: If we maintain)"),
                    ("• Meaning", "Expresses direct causality: if condition A holds, result B naturally follows"),
                    ("• Key Verb 間に合う", "Used for catching trains, meeting shipment deadlines, and arriving on time")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "1.3_cultural_insight",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Here is the dark foreshadowing: 'Byousoku ni ten nana meetoru'—2.7 meters per second. This is not just a speed; it is the absolute metric enforced by global management. If it drops even one fraction, automated warning alarms trigger worldwide.",
                "duration_est": 16.0,
                "jlpt": "Cultural Context",
                "ref_sentence": "ベルトの速度を秒速2.7メートルに保てば、すべての出荷が間に合います。",
                "vocab": [
                    {"orig": "速度", "kana": "そくど", "romaji": "sokudo", "pos": "Noun (N4)", "meaning": "Speed / Velocity"},
                    {"orig": "保つ", "kana": "たもつ", "romaji": "tamotsu", "pos": "Verb (N3)", "meaning": "To maintain / Keep"},
                    {"orig": "出荷", "kana": "しゅっか", "romaji": "shukka", "pos": "Noun (N3)", "meaning": "Shipment / Dispatch"},
                    {"orig": "間に合う", "kana": "まにあう", "romaji": "maniau", "pos": "Verb (N4)", "meaning": "To be in time for"}
                ],
                "grammar_title": "~ば Conditional & 間に合う (On Time)",
                "grammar_bullets": [
                    ("• Conditional Formula", "Verb e-row + ば (保つ -> 保てば: If we maintain)"),
                    ("• Meaning", "Expresses direct causality: if condition A holds, result B naturally follows"),
                    ("• Key Verb 間に合う", "Used for catching trains, meeting shipment deadlines, and arriving on time")
                ]
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 2: THE CONFLICT — HONNE VS. TATEMAE (07:30 - 15:00)
    # ----------------------------------------------------
    {
        "chapter_id": 2,
        "chapter_title": "THE CONFLICT — HONNE VS. TATEMAE",
        "timecode_range": "07:30 - 15:00",
        "scene_clip": "scene_06_miu404",
        "segments": [
            {
                "seg_id": "2.1_narration",
                "type": "story_escalation",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Act Two erupts. Across the Tokyo metropolitan area, packages delivered from this exact facility begin detonating upon opening. The police arrive. Detectives Shima and Ibuki from the mobile investigative unit, alongside forensic experts from UDI Lab, surround the facility.",
                "duration_est": 18.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "2.1_dialogue",
                "type": "dialogue_n4_n3",
                "character": "Ko Nashimoto",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "これ以上配送を続けたら、さらに多くの被害者が出てしまいます！すぐにラインを止めるべきです！",
                "furi": "これ いじょう はいそう を つづけたら、 さらに おおく の ひがいしゃ が でて しまいます！ すぐに らいん を とめる べき です！",
                "romaji": "Kore ijou haisou o tsuzuketara, sara ni ooku no higaisha ga dete shimaimasu! Sugu ni rain o tomeru beki desu!",
                "meaning": "If we continue deliveries any further, even more victims will emerge! We must stop the line immediately!",
                "jlpt": "N3",
                "tokens": [
                    {"orig": "これ以上", "kana": "これいじょう", "romaji": "kore ijou"},
                    {"orig": "配送を続けたら", "kana": "はいそうをつづけたら", "romaji": "haisou o tsuzuketara"},
                    {"orig": "さらに多くの", "kana": "さらにおおくの", "romaji": "sara ni ooku no"},
                    {"orig": "被害者が", "kana": "ひがいしゃが", "romaji": "higaisha ga"},
                    {"orig": "出てしまいます", "kana": "でてしまいます", "romaji": "dete shimaimasu"},
                    {"orig": "すぐにラインを", "kana": "すぐにらいんを", "romaji": "sugu ni rain o"},
                    {"orig": "止めるべきです", "kana": "とめるべきです", "romaji": "tomeru beki desu"}
                ],
                "vocab": [
                    {"orig": "これ以上", "kana": "これいじょう", "romaji": "kore ijou", "pos": "Adv (N4)", "meaning": "Any more / Beyond this"},
                    {"orig": "被害者", "kana": "ひがいしゃ", "romaji": "higaisha", "pos": "Noun (N3)", "meaning": "Victim / Casualties"},
                    {"orig": "~てしまう", "kana": "てしまう", "romaji": "-te shimau", "pos": "Grammar (N4)", "meaning": "Regret / Unintended result"},
                    {"orig": "~べきだ", "kana": "べきだ", "romaji": "beki da", "pos": "Grammar (N3)", "meaning": "Should / Moral duty"}
                ],
                "grammar": "~たら (Conditional form) + ~てしまう (Regretful completion) + ~べきだ (Strong moral duty)",
                "grammar_title": "~べきだ (Moral Duty) & ~てしまう (Regret)",
                "grammar_bullets": [
                    ("• ~べきだ Formula", "Verb Dictionary Form + べきだ / べきです (Strong moral imperative: ought to do)"),
                    ("• Emotional Stacking", "~たら creates the frightening premise, ~てしまう expresses grief, ~べきだ demands action"),
                    ("• Business vs Ethics", "Used when standing up against company protocol on ethical grounds")
                ],
                "duration_est": 8.5
            },
            {
                "seg_id": "2.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Look at the emotional stacking here: 'tsuzuketara' creates the frightening hypothetical conditional, 'dete shimaimasu' expresses profound grief for the unavoidable harm, and 'tomeru beki desu' delivers the urgent JLPT N3 moral imperative: 'we ought to stop'.",
                "duration_est": 18.0,
                "jlpt": "N3 Breakdown",
                "ref_sentence": "これ以上配送を続けたら、さらに多くの被害者が出てしまいます！すぐにラインを止めるべきです！",
                "vocab": [
                    {"orig": "これ以上", "kana": "これいじょう", "romaji": "kore ijou", "pos": "Adv (N4)", "meaning": "Any more / Beyond this"},
                    {"orig": "被害者", "kana": "ひがいしゃ", "romaji": "higaisha", "pos": "Noun (N3)", "meaning": "Victim / Casualties"},
                    {"orig": "~てしまう", "kana": "てしまう", "romaji": "-te shimau", "pos": "Grammar (N4)", "meaning": "Regret / Unintended result"},
                    {"orig": "~べきだ", "kana": "べきだ", "romaji": "beki da", "pos": "Grammar (N3)", "meaning": "Should / Moral duty"}
                ],
                "grammar_title": "~べきだ (Moral Duty) & ~てしまう (Regret)",
                "grammar_bullets": [
                    ("• ~べきだ Formula", "Verb Dictionary Form + べきだ / べきです (Strong moral imperative: ought to do)"),
                    ("• Emotional Stacking", "~たら creates the frightening premise, ~てしまう expresses grief, ~べきだ demands action"),
                    ("• Business vs Ethics", "Used when standing up against company protocol on ethical grounds")
                ]
            },
            {
                "seg_id": "2.2_dialogue",
                "type": "dialogue_n3",
                "character": "Elena Funado",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "本社は補償金を払う代わりに、稼働率を落とさないよう要求してきています。利益を優先せざるを得ないのが現実です。",
                "furi": "ほんしゃ は ほしょうきん を はらう かわりに、 かどうりつ を おとさない よう ようきゅう してきて います。 りえき を ゆうせん せざる を えない のが げんじつ です。",
                "romaji": "Honsha wa hoshoukin o harau kawari ni, kadouritsu o otosanai you youkyuu shitekite imasu. Rieki o yuusen sezaru o enai no ga genjitsu desu.",
                "meaning": "In exchange for paying compensation, headquarters demands that we do not lower the operating rate. The reality is that we have no choice but to prioritize profit.",
                "jlpt": "N2",
                "tokens": [
                    {"orig": "本社は", "kana": "ほんしゃは", "romaji": "honsha wa"},
                    {"orig": "補償金を払う代わりに", "kana": "ほしょうきんをはらうかわりに", "romaji": "hoshoukin o harau kawari ni"},
                    {"orig": "稼働率を", "kana": "かどうりつを", "romaji": "kadouritsu o"},
                    {"orig": "落とさないよう", "kana": "おとさないよう", "romaji": "otosanai you"},
                    {"orig": "要求してきています", "kana": "ようきゅうしてきています", "romaji": "youkyuu shitekite imasu"},
                    {"orig": "利益を優先", "kana": "りえきをゆうせん", "romaji": "rieki o yuusen"},
                    {"orig": "せざるを得ないのが", "kana": "せざるをえないのが", "romaji": "sezaru o enai no ga"},
                    {"orig": "現実です", "kana": "げんじつです", "romaji": "genjitsu desu"}
                ],
                "vocab": [
                    {"orig": "本社", "kana": "ほんしゃ", "romaji": "honsha", "pos": "Noun (N4)", "meaning": "Headquarters"},
                    {"orig": "代わりに", "kana": "かわりに", "romaji": "kawari ni", "pos": "Grammar (N3)", "meaning": "In exchange for"},
                    {"orig": "稼働率", "kana": "かどうりつ", "romaji": "kadouritsu", "pos": "Noun (N2)", "meaning": "Operating capacity"},
                    {"orig": "せざるを得ない", "kana": "せざるをえない", "romaji": "sezaru o enai", "pos": "Grammar (N2)", "meaning": "Have no choice but to"}
                ],
                "grammar": "~代わりに (In exchange for) + ~せざるを得ない (JLPT N2: Compelled to do against one's will)",
                "grammar_title": "~せざるを得ない (Compelled Against Will)",
                "grammar_bullets": [
                    ("• Classical Origin", "Derived from classical negative ざる + を得ない (cannot obtain non-action)"),
                    ("• Formation Rule", "Verb Nai-stem + ざるを得ない (する -> せざるを得ない)"),
                    ("• Psychological Nuance", "Used when external executive pressure or unavoidable circumstances force compliance")
                ],
                "duration_est": 10.0
            },
            {
                "seg_id": "2.2_breakdown",
                "type": "pedagogical_lesson",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "This is one of the most famous JLPT N2 grammar patterns: 'sezaru o enai'. Formed from the classical negative 'zaru', it signifies that despite personal morals, external corporate pressure forces you into action.",
                "duration_est": 16.0,
                "jlpt": "N2 Breakdown",
                "ref_sentence": "利益を優先せざるを得ないのが現実です。",
                "vocab": [
                    {"orig": "本社", "kana": "ほんしゃ", "romaji": "honsha", "pos": "Noun (N4)", "meaning": "Headquarters"},
                    {"orig": "代わりに", "kana": "かわりに", "romaji": "kawari ni", "pos": "Grammar (N3)", "meaning": "In exchange for"},
                    {"orig": "稼働率", "kana": "かどうりつ", "romaji": "kadouritsu", "pos": "Noun (N2)", "meaning": "Operating capacity"},
                    {"orig": "せざるを得ない", "kana": "せざるをえない", "romaji": "sezaru o enai", "pos": "Grammar (N2)", "meaning": "Have no choice but to"}
                ],
                "grammar_title": "~せざるを得ない (Compelled Against Will)",
                "grammar_bullets": [
                    ("• Classical Origin", "Derived from classical negative ざる + を得ない (cannot obtain non-action)"),
                    ("• Formation Rule", "Verb Nai-stem + ざるを得ない (する -> せざるを得ない)"),
                    ("• Psychological Nuance", "Used when external executive pressure or unavoidable circumstances force compliance")
                ]
            },
            {
                "seg_id": "2.3_dialogue",
                "type": "dialogue_n3_subcontractor",
                "character": "Yatsusaka (Courier)",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "一個配達して百円ちょっとですよ！これ以上時間を削られたら、命が持ちませんよ！",
                "furi": "いっこ はいたつ して ひゃくえん ちょっと ですよ！ これ いじょう じかん を けずられたら、 いのち が もちません よ！",
                "romaji": "Ikko haitatsu shite hyakuen chotto desu yo! Kore ijou jikan o kezuraretara, inochi ga mochimasen yo!",
                "meaning": "We make barely a hundred yen per parcel delivered! If our time is cut any further, our lives won't survive this!",
                "jlpt": "N3",
                "tokens": [
                    {"orig": "一個配達して", "kana": "いっこはいたつして", "romaji": "ikko haitatsu shite"},
                    {"orig": "百円ちょっとですよ", "kana": "ひゃくえんちょっとですよ", "romaji": "hyakuen chotto desu yo"},
                    {"orig": "これ以上", "kana": "これいじょう", "romaji": "kore ijou"},
                    {"orig": "時間を", "kana": "じかんを", "romaji": "jikan o"},
                    {"orig": "削られたら", "kana": "けずられたら", "romaji": "kezuraretara"},
                    {"orig": "命が", "kana": "いのちが", "romaji": "inochi ga"},
                    {"orig": "持ちませんよ", "kana": "もちませんよ", "romaji": "mochimasen yo"}
                ],
                "vocab": [
                    {"orig": "配達", "kana": "はいたつ", "romaji": "haitatsu", "pos": "Noun/Suru (N4)", "meaning": "Delivery"},
                    {"orig": "削る", "kana": "けずる", "romaji": "kezuru", "pos": "Verb (N2)", "meaning": "To shave down / Cut"},
                    {"orig": "削られる", "kana": "けずられる", "romaji": "kezurareru", "pos": "Passive (N4)", "meaning": "To be cut (Suffering Passive)"},
                    {"orig": "命が持つ", "kana": "いのちがもつ", "romaji": "inochi ga motsu", "pos": "Idiom (N3)", "meaning": "To endure / Sustain life"}
                ],
                "grammar": "迷惑の受身 (Suffering passive: 削られたら) + 命が持たない (Idiom: Unable to endure physically)",
                "grammar_title": "迷惑の受身 (Suffering Passive: 削られる)",
                "grammar_bullets": [
                    ("• Suffering Passive", "Japanese passive adds emotional distress when action harms the speaker"),
                    ("• Structure", "時間 (Time) + を削られる (To have one's time forcibly cut by superiors)"),
                    ("• Cultural Reality", "Expresses the raw Honne of Japan's frontline subcontracted delivery drivers")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "2.3_deep_culture",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Notice the suffering passive 'kezuraretara'. In Japanese, when someone imposes hardship upon you, the passive form carries a deep emotional undertone of victimization. This is the raw Honne of Japan's overworked delivery couriers.",
                "duration_est": 17.5,
                "jlpt": "Cultural Nuance",
                "ref_sentence": "これ以上時間を削られたら、命が持ちませんよ！",
                "vocab": [
                    {"orig": "配達", "kana": "はいたつ", "romaji": "haitatsu", "pos": "Noun/Suru (N4)", "meaning": "Delivery"},
                    {"orig": "削る", "kana": "けずる", "romaji": "kezuru", "pos": "Verb (N2)", "meaning": "To shave down / Cut"},
                    {"orig": "削られる", "kana": "けずられる", "romaji": "kezurareru", "pos": "Passive (N4)", "meaning": "To be cut (Suffering Passive)"},
                    {"orig": "命が持つ", "kana": "いのちがもつ", "romaji": "inochi ga motsu", "pos": "Idiom (N3)", "meaning": "To endure / Sustain life"}
                ],
                "grammar_title": "迷惑の受身 (Suffering Passive: 削られる)",
                "grammar_bullets": [
                    ("• Suffering Passive", "Japanese passive adds emotional distress when action harms the speaker"),
                    ("• Structure", "時間 (Time) + を削られる (To have one's time forcibly cut by superiors)"),
                    ("• Cultural Reality", "Expresses the raw Honne of Japan's frontline subcontracted delivery drivers")
                ]
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 3: THE CLIMAX — THE SOUL OF THE MOVIE (15:00 - 22:30)
    # ----------------------------------------------------
    {
        "chapter_id": 3,
        "chapter_title": "THE CLIMAX — THE SOUL OF THE MOVIE",
        "timecode_range": "15:00 - 22:30",
        "scene_clip": "scene_08_speedgauge",
        "segments": [
            {
                "seg_id": "3.1_narration",
                "type": "climax_reveal",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Act Three delivers the shattering revelation. The bomber is not an external terrorist. It is the vengeance of a former manager who collapsed from Karoshi—overwork. On the locker room floor, he left a cryptic mathematical equation: '2.7m/s -> 0'. The final unexploded bomb is approaching the sorting junction right now.",
                "duration_est": 22.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "3.1_dialogue",
                "type": "dialogue_n2",
                "character": "Elena Funado",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "このまま見過ごせば、また誰かが命を落としかねない。今すぐ全ラインを緊急停止させなさい！",
                "furi": "この まま みすごせば、 また だれか が いのち を おとしかねない。 いま すぐ ぜん らいん を きんきゅう ていし させなさい！",
                "romaji": "Kono mama misugoseba, mata dareka ga inochi o otoshikanenai. Ima sugu zen rain o kinkyuu teishi sasenasai!",
                "meaning": "If we overlook this any longer, someone else could very well lose their life. Stop all lines immediately!",
                "jlpt": "N2",
                "tokens": [
                    {"orig": "このまま", "kana": "このまま", "romaji": "kono mama"},
                    {"orig": "見過ごせば", "kana": "みすごせば", "romaji": "misugoseba"},
                    {"orig": "また誰かが", "kana": "まただれかが", "romaji": "mata dareka ga"},
                    {"orig": "命を落とし", "kana": "いのちをおとし", "romaji": "inochi o otoshi"},
                    {"orig": "かねない", "kana": "かねない", "romaji": "kanenai"},
                    {"orig": "今すぐ全ラインを", "kana": "いますぐぜんらいんを", "romaji": "ima sugu zen rain o"},
                    {"orig": "緊急停止", "kana": "きんきゅうていし", "romaji": "kinkyuu teishi"},
                    {"orig": "させなさい", "kana": "させなさい", "romaji": "sasenasai"}
                ],
                "vocab": [
                    {"orig": "見過ごす", "kana": "みすごす", "romaji": "misugosu", "pos": "Verb (N2)", "meaning": "To overlook / Ignore"},
                    {"orig": "命を落とす", "kana": "いのちをおとす", "romaji": "inochi o otosu", "pos": "Idiom (N2)", "meaning": "To lose one's life"},
                    {"orig": "~かねない", "kana": "かねない", "romaji": "kanenai", "pos": "Grammar (N2)", "meaning": "High danger of bad outcome"},
                    {"orig": "緊急停止", "kana": "きんきゅうていし", "romaji": "kinkyuu teishi", "pos": "Noun (N2)", "meaning": "Emergency shutdown"}
                ],
                "grammar": "~かねない (JLPT N2: High danger of negative outcome) + 使役命令形 (Causative Command)",
                "grammar_title": "~かねない (Severe Risk of Danger)",
                "grammar_bullets": [
                    ("• Distinction from かもしれない", "かもしれない is neutral 50/50 possibility | かねない specifically warns of a catastrophic risk"),
                    ("• Formation Rule", "Verb Masu-stem + かねない (落とす -> 落としかねない)"),
                    ("• Executive Authority", "Elena uses causative imperative させなさい to assume absolute legal responsibility")
                ],
                "duration_est": 9.0
            },
            {
                "seg_id": "3.1_breakdown",
                "type": "pedagogical_lesson",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Look at the JLPT N2 grammar 'kanenai'. While 'kamo shirenai' means simple possibility, 'kanenai' specifically indicates a severe risk of an undesirable disaster. Elena's use of the causative imperative 'sasenasai' shows she is taking ultimate executive responsibility.",
                "duration_est": 19.0,
                "jlpt": "N2 Breakdown",
                "ref_sentence": "このまま見過ごせば、また誰かが命を落としかねない。",
                "vocab": [
                    {"orig": "見過ごす", "kana": "みすごす", "romaji": "misugosu", "pos": "Verb (N2)", "meaning": "To overlook / Ignore"},
                    {"orig": "命を落とす", "kana": "いのちをおとす", "romaji": "inochi o otosu", "pos": "Idiom (N2)", "meaning": "To lose one's life"},
                    {"orig": "~かねない", "kana": "かねない", "romaji": "kanenai", "pos": "Grammar (N2)", "meaning": "High danger of bad outcome"},
                    {"orig": "緊急停止", "kana": "きんきゅうていし", "romaji": "kinkyuu teishi", "pos": "Noun (N2)", "meaning": "Emergency shutdown"}
                ],
                "grammar_title": "~かねない (Severe Risk of Danger)",
                "grammar_bullets": [
                    ("• Distinction from かもしれない", "かもしれない is neutral 50/50 possibility | かねない specifically warns of a catastrophic risk"),
                    ("• Formation Rule", "Verb Masu-stem + かねない (落とす -> 落としかねない)"),
                    ("• Executive Authority", "Elena uses causative imperative させなさい to assume absolute legal responsibility")
                ]
            },
            {
                "seg_id": "3.2_dialogue",
                "type": "ultimate_soul_phrase",
                "character": "Ko Nashimoto & Elena",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "人が生きていくための仕組みが、人を殺す理由になっていいはずがありません。",
                "furi": "ひと が いきていく ため の しくみ が、 ひと を ころす りゆう に なって いい はず が ありません。",
                "romaji": "Hito ga ikiteiku tame no shikumi ga, hito o korosu riyuu ni natte ii hazu ga arimasen.",
                "meaning": "There is no possible way that a system built for people to live should ever become a reason to kill them.",
                "jlpt": "N2",
                "tokens": [
                    {"orig": "人が生きていく", "kana": "ひとがいきていく", "romaji": "hito ga ikite iku"},
                    {"orig": "ための仕組みが", "kana": "ためのしくみが", "romaji": "tame no shikumi ga"},
                    {"orig": "人を殺す", "kana": "ひとをころす", "romaji": "hito o korosu"},
                    {"orig": "理由になって", "kana": "りゆうになって", "romaji": "riyuu ni natte"},
                    {"orig": "いいはずが", "kana": "いいはずが", "romaji": "ii hazu ga"},
                    {"orig": "ありません", "kana": "ありません", "romaji": "arimasen"}
                ],
                "vocab": [
                    {"orig": "生きていく", "kana": "いきていく", "romaji": "ikite iku", "pos": "Grammar (N4)", "meaning": "To go on living into the future"},
                    {"orig": "仕組み", "kana": "しくみ", "romaji": "shikumi", "pos": "Noun (N3)", "meaning": "System / Mechanism"},
                    {"orig": "~はずがない", "kana": "はずがない", "romaji": "hazu ga nai", "pos": "Grammar (N3/N2)", "meaning": "There is no way / Cannot be"}
                ],
                "grammar": "~ていく (Continuing into future) + ~ていいはずがない (Absolute moral rejection)",
                "grammar_title": "~ていいはずがない (Absolute Moral Rejection)",
                "grammar_bullets": [
                    ("• Absolute Negation", "はずがない means 'there is zero justifiable reason'"),
                    ("• Ethical Stance", "~ていい (is acceptable) + はずがない = It can never be acceptable under any circumstances"),
                    ("• Film Climax Soul", "The foundational philosophical punchline of the entire Last Mile story")
                ],
                "duration_est": 9.0
            },
            {
                "seg_id": "3.2_movie_emotion",
                "type": "movie_climax_audio",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Listen to that phrasing: 'ii hazu ga arimasen'. It is an absolute rejection of corporate cruelty. When the emergency switch clicks down, the speed drops from 2.7 to zero. For the first time in ten years, silence falls across the warehouse.",
                "duration_est": 18.5,
                "jlpt": "Climax Emotional Audio"
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 4: CINEMA SHADOWING GYM (22:30 - 26:30)
    # ----------------------------------------------------
    {
        "chapter_id": 4,
        "chapter_title": "CINEMA SHADOWING GYM",
        "timecode_range": "22:30 - 26:30",
        "scene_clip": "scene_07_automated",
        "segments": [
            {
                "seg_id": "4.0_intro",
                "type": "gym_intro",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Welcome to the Cinema Shadowing Gym. We will now drill the five soul phrases from Last Mile across five levels of difficulty. First, listen to the native pacing at point eight-five speed. Then, match the pitch accent on the three-two-one countdown.",
                "duration_est": 16.5,
                "jlpt": "N/A"
            },
            {
                "seg_id": "4.1_drill",
                "type": "shadowing_drill_n5",
                "drill_level": "Level 1 • N5 Foundation",
                "character": "Nanami Coach",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "確認してください。",
                "furi": "かくにん して ください。",
                "romaji": "Kakunin shite kudasai.",
                "meaning": "Please verify / Please check.",
                "tokens": [
                    {"orig": "確認して", "kana": "かくにんして", "romaji": "kakunin shite"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai"}
                ],
                "duration_est": 4.5
            },
            {
                "seg_id": "4.2_drill",
                "type": "shadowing_drill_n4",
                "drill_level": "Level 2 • N4 Everyday",
                "character": "Nanami Coach",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "荷物を止めなきゃいけない。",
                "furi": "にもつ を とめなきゃ いけない。",
                "romaji": "Nimotsu o tomenakya ikenai.",
                "meaning": "We have to stop the packages.",
                "tokens": [
                    {"orig": "荷物を", "kana": "にもつを", "romaji": "nimotsu o"},
                    {"orig": "止めなきゃ", "kana": "とめなきゃ", "romaji": "tomenakya"},
                    {"orig": "いけない", "kana": "いけない", "romaji": "ikenai"}
                ],
                "duration_est": 5.0
            },
            {
                "seg_id": "4.3_drill",
                "type": "shadowing_drill_n3",
                "drill_level": "Level 3 • N3 Nuance",
                "character": "Nanami Coach",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "止めるわけにはいきません。",
                "furi": "とめる わけ に は いきません。",
                "romaji": "Tomeru wake ni wa ikimasen.",
                "meaning": "There is no way we can afford to stop.",
                "tokens": [
                    {"orig": "止める", "kana": "とめる", "romaji": "tomeru"},
                    {"orig": "わけには", "kana": "わけには", "romaji": "wake ni wa"},
                    {"orig": "いきません", "kana": "いきません", "romaji": "ikimasen"}
                ],
                "duration_est": 5.5
            },
            {
                "seg_id": "4.4_drill",
                "type": "shadowing_drill_n3_cultural",
                "drill_level": "Level 4 • N3 Cultural",
                "character": "Nanami Coach",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "現場に負担を押し付けるな。",
                "furi": "げんば に ふたん を おしつける な。",
                "romaji": "Genba ni futan o oshitsukeru na.",
                "meaning": "Do not push the burden onto the front line.",
                "tokens": [
                    {"orig": "現場に", "kana": "げんばに", "romaji": "genba ni"},
                    {"orig": "負担を", "kana": "ふたんを", "romaji": "futan o"},
                    {"orig": "押し付けるな", "kana": "おしつけるな", "romaji": "oshitsukeru na"}
                ],
                "duration_est": 5.5
            },
            {
                "seg_id": "4.5_drill",
                "type": "shadowing_drill_n2",
                "drill_level": "Level 5 • N2 Master",
                "character": "Nanami Coach",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "命より優先される数字などあってはならない。",
                "furi": "いのち より ゆうせん される すうじ など あっては ならない。",
                "romaji": "Inochi yori yuusen sareru suuji nado atte wa naranai.",
                "meaning": "No metric should ever be allowed to take priority over human life.",
                "tokens": [
                    {"orig": "命より", "kana": "いのちより", "romaji": "inochi yori"},
                    {"orig": "優先される", "kana": "ゆうせんされる", "romaji": "yuusen sareru"},
                    {"orig": "数字など", "kana": "すうじなど", "romaji": "suuji nado"},
                    {"orig": "あっては", "kana": "あっては", "romaji": "atte wa"},
                    {"orig": "ならない", "kana": "ならない", "romaji": "naranai"}
                ],
                "duration_est": 6.5
            }
        ]
    },

    # ----------------------------------------------------
    # CHAPTER 5: PHILOSOPHICAL WRAP-UP & NEXT RELEASE (26:30 - 28:00)
    # ----------------------------------------------------
    {
        "chapter_id": 5,
        "chapter_title": "PHILOSOPHICAL WRAP-UP & NEXT RELEASE",
        "timecode_range": "26:30 - 28:00",
        "scene_clip": "scene_10_climax",
        "segments": [
            {
                "seg_id": "5.1_philosophical",
                "type": "philosophical_summary",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Last Mile is far more than a detective thriller. It forces us to ask: in an era of same-day delivery and convenience, who really pays the price for our speed? When we master Japanese through real cinema, we do not just memorize grammar points—we understand the human soul behind every syllable.",
                "duration_est": 22.0,
                "jlpt": "Philosophy"
            },
            {
                "seg_id": "5.2_next_teaser",
                "type": "next_episode_teaser",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Next weekend on TokyoFlow Cinema Masterclass, we enter the dark underbelly of Tokyo real estate fraud with Netflix Japan's mega-hit series: Tokyo Swindlers. Prepare to master high-stakes deception vocabulary and executive negotiations.",
                "duration_est": 15.0,
                "jlpt": "Next Teaser"
            },
            {
                "seg_id": "5.3_app_cta",
                "type": "final_app_cta",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Practice all eighty lines from today's masterclass with real-time AI pitch accent scoring on the TokyoFlow iOS app. The link is in the description below. Subscribe to TokyoFlow, and I will see you at the cinema next weekend.",
                "duration_est": 15.0,
                "jlpt": "Outro CTA"
            }
        ]
    }
]

# ==========================================
# EXPORTERS & SPECS
# ==========================================

def build_production_spec(output_dir: str) -> dict:
    spec = {
        "metadata": EPISODE_METADATA,
        "generated_at": datetime.now().isoformat(),
        "total_chapters": len(CINEMA_SCREENPLAY),
        "target_resolution": "1920x1080 (FHD Master)",
        "audio_pipeline": {
            "narrator_voice": "en-US-AndrewNeural",
            "narrator_speed": "+2%",
            "dialogue_voice": "ja-JP-NanamiNeural",
            "dialogue_speed": "-16%",
            "drill_slow_speed": "-22%"
        },
        "chapters": CINEMA_SCREENPLAY
    }
    spec_path = os.path.join(output_dir, "production_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f" Saved Production Spec: {spec_path}")
    return spec

def build_script_json_and_fountain(output_dir: str):
    script_json_path = os.path.join(output_dir, "script.json")
    fountain_path = os.path.join(output_dir, "screenplay.fountain")

    with open(script_json_path, "w", encoding="utf-8") as f:
        json.dump(CINEMA_SCREENPLAY, f, ensure_ascii=False, indent=2)
    print(f" Saved Script JSON: {script_json_path}")

    fountain_lines = [
        f"Title: TOKYOFLOW CINEMA MASTERCLASS - WL.{EPISODE_METADATA['episode_number']:02d}: {EPISODE_METADATA['movie_title_en'].upper()} ({EPISODE_METADATA['movie_title_ja']})",
        f"Credit: Written and Directed by TokyoFlow Executive Director",
        f"Author: TokyoFlow Academy",
        f"Funnel Reference: Shorts Lead Funnel {EPISODE_METADATA.get('shorts_funnel_code', 'WS.01')}",
        f"Source: Inspired by the 2024 Japanese Blockbuster '{EPISODE_METADATA['movie_title_en']}'",
        f"Draft date: {datetime.now().strftime('%Y-%m-%d')}",
        "\n===\n\n"
    ]

    for ch in CINEMA_SCREENPLAY:
        fountain_lines.append(f"\n/* CHAPTER {ch['chapter_id']}: {ch['chapter_title']} ({ch['timecode_range']}) */\n")
        fountain_lines.append(f"EXT. TOKYO LOGISTICS HUB - DAY\n\n")
        for seg in ch["segments"]:
            char_name = seg.get("character", "HOST").upper()
            lang_tag = f"({seg.get('lang', 'en').upper()} - {seg.get('jlpt', '')})"
            fountain_lines.append(f"{char_name} {lang_tag}\n")
            if seg.get("lang") == "ja":
                fountain_lines.append(f"{seg.get('content')}\n")
                if "meaning" in seg:
                    fountain_lines.append(f"({seg['meaning']})\n\n")
            else:
                fountain_lines.append(f"{seg.get('content')}\n\n")

    with open(fountain_path, "w", encoding="utf-8") as f:
        f.writelines(fountain_lines)
    print(f" Saved Fountain Screenplay: {fountain_path}")

def build_metadata_md(output_dir: str):
    meta_path = os.path.join(output_dir, "metadata.md")
    title = f"[JLPT N5-N2] WL.01 Last Mile (ラストマイル) Full Breakdown | Learn Real Japanese Through Cinema"
    description = f"""Master real Japanese conversation, business etiquette, and JLPT grammar through Japan's 2024 blockbuster movie 'Last Mile' (ラストマイル).

[TokyoFlow Cinema Series]
Long-form Masterclass: WL.01
Shorts Traffic Funnel: WS.01

This comprehensive 25-minute masterclass provides word-by-word dialogue breakdowns, pitch accent guides, and step-by-step JLPT N5, N4, N3, and N2 grammar explanations.

TIMESTAMPS:
00:00 - Chapter 0: The 90-Second Golden Opening & Core Dilemma
01:30 - Chapter 1: The Spark — Survival in Tokyo (JLPT N5-N4 Greetings & Orders)
07:30 - Chapter 2: The Conflict — Honne vs Tatemae (JLPT N4-N3 Workplace Negotiations)
15:00 - Chapter 3: The Climax — The Soul of the Movie (JLPT N3-N2 Critical Grammar)
22:30 - Chapter 4: Cinema Shadowing Gym (5-Level Soul Phrase Workout)
26:30 - Chapter 5: Philosophical Wrap-Up & Next Release Preview

ABOUT THE MOVIE:
Movie: Last Mile (ラストマイル)
Director: Ayuko Tsukahara
Screenplay: Akiko Nogi
Starring: Hikari Mitsushima, Masaki Okada, Satomi Ishihara, Go Ayano

CORE PEDAGOGICAL HIGHLIGHTS:
- JLPT N5: Basic workplace greetings and standard requests
- JLPT N4: Conditional forms (~tara, ~ba) and colloquial contractions
- JLPT N3: Social obligation (~wake ni wa ikanai), moral duty (~beki da), and the suffering passive
- JLPT N2: Compulsion (~sezaru o enai) and severe risk indicators (~kanenai)

PRACTICE ON TOKYOFLOW APP:
Practice all lines from this episode with real-time AI pitch accent scoring and spaced repetition flashcards on the TokyoFlow iOS app:
https://apps.apple.com/app/tokyoflow

TAGS:
Japanese Cinema, Learn Japanese Through Anime, Japanese Movie Breakdown, JLPT N5, JLPT N4, JLPT N3, JLPT N2, Japanese Listening Practice, Japanese Shadowing, Last Mile Japanese Movie, TokyoFlow, Japanese Grammar Explained, Real Tokyo Japanese, Business Japanese Conversation, Hikari Mitsushima, Masaki Okada, Ayuko Tsukahara, Akiko Nogi, Japanese Pitch Accent, Japanese Subtitles, Japanese Storytelling, Tokyo Life Japanese, Japanese Workplace Culture, Honne and Tatemae, Japan Box Office 2024, Japanese Speaking Practice"""

    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"# YouTube Title\n```\n{title}\n```\n\n# YouTube Description\n```\n{description}\n```\n")
    print(f" Saved Metadata: {meta_path}")

def build_thumbnail_prompt_md(output_dir: str):
    thumb_path = os.path.join(output_dir, "thumbnail_prompt.md")
    content = """# 16:9 4K Master Thumbnail Design Specification

## Prompt for Midjourney v6.1 / FLUX.1 Pro:
```text
A cinematic, ultra-detailed 16:9 YouTube video thumbnail for a Japanese Cinema Masterclass. 
In the center-right, a dramatic cinematic portrait of Japanese actress Hikari Mitsushima wearing an executive logistics headset, looking intensely into the camera inside a vast, futuristic automated warehouse with glowing red warning lights and high-speed conveyor belts. 
On the left side, bold 3D extruded metallic yellow and white typography reading:
"LAST MILE" (Top line, bold cinematic red font)
"2.7m/s or DIE?" (Middle line, giant neon yellow 3D text)
"JLPT N5-N2 CINEMA BREAKDOWN" (Bottom badge in dark navy and electric pink capsule).
High contrast, dynamic cinematic lighting, depth of field, 8k resolution, movie poster aesthetic, photorealistic, anamorphic lens flare --ar 16:9 --style raw --v 6.1
```
"""
    with open(thumb_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f" Saved Thumbnail Prompt: {thumb_path}")

# ==========================================
# AUDIO SYNTHESIS ENGINE (Anti-Pop, Normalized)
# ==========================================

def normalize_speech_text(text: str, lang: str = "en") -> str:
    """Normalizes abbreviations like JLPT N1..N5 for crystal-clear letter-N TTS articulation."""
    if not text:
        return ""
    if lang == "en":
        # Avoid 'JLPT' + 'N' consonant collision (which sounds like 'JLPTin') by articulating 'JLPT Level N 3'
        text = re.sub(r'JLPT\s*N([1-5])\s*to\s*N([1-5])', r'JLPT Level N \1 to Level N \2', text, flags=re.IGNORECASE)
        text = re.sub(r'JLPT\s*N([1-5])', r'JLPT Level N \1', text, flags=re.IGNORECASE)
        text = re.sub(r'\bN([1-5])\b', r'N \1', text)
        text = text.replace("Level Level", "Level").replace(",,", ",").replace("  ", " ").strip()
    elif lang == "ja":
        # In Japanese audio, N1-N5 is spoken as エヌ (Enu)
        text = re.sub(r'\bN([1-5])\b', r'エヌ\1', text)
    return text

async def synthesize_all_audio_tracks(output_dir: str):
    """Synthesizes high-fidelity dual-language audio files with 44.1kHz stereo normalization and rich multi-voice breakdown."""
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    
    print("\n Synthesizing Comprehensive Dual-Language Audio Tracks (Nanami JA + Andrew EN)...")
    
    for ch in CINEMA_SCREENPLAY:
        for seg in ch["segments"]:
            seg_id = seg["seg_id"].replace(".", "_")
            out_file = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            seg["audio_file"] = out_file
            
            ref_sentence = seg.get("ref_sentence", "")
            
            # If segment is a Micro-Lesson Breakdown with target sentence:
            # We composite: 
            # 1. Target Dialogue: Nanami (JA) + Andrew (EN Translation)
            # 2. Vocab Breakdown: For each card -> Nanami (JA word) + Andrew (EN meaning)
            # 3. Grammar Spotlight: Andrew (EN Explanation & Nuance)
            if ref_sentence and seg.get("lang") == "en":
                audio_parts = []
                
                # Part 1: Target Sentence
                tmp_target_ja = out_file + ".t_ja.raw.mp3"
                comm_ja = edge_tts.Communicate(ref_sentence, "ja-JP-NanamiNeural", rate="-14%", pitch="+2Hz")
                await comm_ja.save(tmp_target_ja)
                dur_target_ja = get_audio_duration(tmp_target_ja)
                audio_parts.append(tmp_target_ja)
                
                meaning = seg.get("meaning", "")
                if not meaning:
                    for s in ch["segments"]:
                        if s.get("lang") == "ja" and (ref_sentence in s.get("content", "") or s.get("content") in ref_sentence):
                            meaning = s.get("meaning", "")
                            break
                if not meaning:
                    meaning = "Elena states the core operational principle."
                
                tmp_target_en = out_file + ".t_en.raw.mp3"
                spoken_trans = normalize_speech_text(f"Translation: {meaning}", "en")
                comm_en_sent = edge_tts.Communicate(spoken_trans, "en-US-AndrewNeural", rate="+3%", pitch="+0Hz")
                await comm_en_sent.save(tmp_target_en)
                dur_target_en = get_audio_duration(tmp_target_en)
                audio_parts.append(tmp_target_en)
                
                cur_timestamp = dur_target_ja + dur_target_en
                vocab_timings = []
                
                # Part 2: Vocab breakdown (Word-by-word)
                vocab_list = seg.get("vocab", [])[:5]
                for v_idx, v in enumerate(vocab_list):
                    v_ja_file = out_file + f".v_{v_idx}_ja.raw.mp3"
                    v_en_file = out_file + f".v_{v_idx}_en.raw.mp3"
                    
                    await edge_tts.Communicate(v.get("orig", ""), "ja-JP-NanamiNeural", rate="-14%", pitch="+2Hz").save(v_ja_file)
                    v_ja_dur = get_audio_duration(v_ja_file)
                    
                    spoken_meaning = normalize_speech_text(v.get("meaning", ""), "en")
                    await edge_tts.Communicate(spoken_meaning, "en-US-AndrewNeural", rate="+3%", pitch="+0Hz").save(v_en_file)
                    v_en_dur = get_audio_duration(v_en_file)
                    
                    vocab_timings.append({
                        "idx": v_idx,
                        "start": cur_timestamp,
                        "ja_end": cur_timestamp + v_ja_dur,
                        "end": cur_timestamp + v_ja_dur + v_en_dur
                    })
                    
                    audio_parts.extend([v_ja_file, v_en_file])
                    cur_timestamp += v_ja_dur + v_en_dur
                
                # Part 3: Grammar & Culture Spotlight
                spotlight_start = cur_timestamp
                tmp_spot_en = out_file + ".spot.raw.mp3"
                spoken_spot = normalize_speech_text(seg.get("content", ""), "en")
                comm_spot = edge_tts.Communicate(spoken_spot, "en-US-AndrewNeural", rate="+2%", pitch="+0Hz")
                await comm_spot.save(tmp_spot_en)
                dur_spot = get_audio_duration(tmp_spot_en)
                audio_parts.append(tmp_spot_en)
                
                seg["breakdown_timings"] = {
                    "target_ja_dur": dur_target_ja,
                    "target_en_dur": dur_target_en,
                    "target_end": dur_target_ja + dur_target_en,
                    "vocab_timings": vocab_timings,
                    "spotlight_start": spotlight_start,
                    "total_duration": spotlight_start + dur_spot
                }
                seg["ja_duration"] = dur_target_ja
                
                timings_path = out_file.replace(".mp3", ".timings.json")
                with open(timings_path, "w", encoding="utf-8") as tf:
                    json.dump(seg["breakdown_timings"], tf, indent=2, ensure_ascii=False)
                
                # Concat all audio parts with clean stereo 44.1kHz MP3
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
                print(f"   Normalized Full Dual-Voice Breakdown [JA+EN Multi-Voice]: {os.path.basename(out_file)} ({spotlight_start + dur_spot:.1f}s)")
            else:
                voice = seg.get("voice", "en-US-AndrewNeural")
                raw_text = seg.get("content", "")
                text = normalize_speech_text(raw_text, seg.get("lang", "en"))
                
                # Strict pacing: Slower Japanese for crystal-clear learning
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
                print(f"   Normalized Audio [{seg.get('character')}]: {os.path.basename(out_file)}")

    print(" All comprehensive dual-track audio synthesis normalized and complete!")

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

## ==========================================
# DYNAMIC TRANSPARENT RGBA FRAME RENDERERS
# ==========================================

def draw_top_brand_bar(draw: ImageDraw.Draw, width: int, chapter_title: str, jlpt_level: str):
    # Top Brand Ribbon
    draw.rectangle([(0, 0), (width, 68)], fill=(10, 15, 28, 220))
    draw.text((50, 18), "TokyoFlow Japanese  |  Cinema Masterclass • WL.01 Last Mile", fill=(255, 255, 255), font=get_font(26))
    
    # Clean JLPT badge text (normalize "N3 Breakdown", "N3", "JLPT N3", etc.)
    level_clean = jlpt_level.replace("Breakdown", "").replace("Lesson", "").replace("dialogue_", "").strip() if jlpt_level else ""
    if level_clean and level_clean != "N/A" and level_clean != "CTA":
        badge_str = f"JLPT {level_clean}" if not level_clean.upper().startswith("JLPT") else level_clean.upper()
    else:
        badge_str = "CINEMA"
    
    # Dynamic Auto-Fit Badge Pill (Zero Cutoff)
    f_badge = get_font(22)
    bbox = draw.textbbox((0, 0), badge_str, font=f_badge)
    text_w = bbox[2] - bbox[0]
    pill_w = max(140, text_w + 36)
    x1 = width - 50 - pill_w
    x2 = width - 50
    draw.rounded_rectangle([(x1, 12), (x2, 56)], radius=12, fill=(225, 29, 72, 230), outline=(255, 255, 255, 180), width=2)
    draw.text((x1 + (pill_w - text_w) // 2, 18), badge_str, fill=(255, 255, 255), font=f_badge)

def compute_mora_ranges(tokens: list, total_duration: float) -> list:
    """Calculates millisecond-accurate phonetic mora-based start and end timing for each token."""
    weights = []
    for tok in tokens:
        k = tok.get("kana", "") or tok.get("orig", "")
        m_count = float(len(k))
        for small in ["ゃ", "ゅ", "ょ", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "っ", "ャ", "ュ", "ョ", "ッ"]:
            m_count -= 0.35 * k.count(small)
        # Add pause weight for punctuation marks
        if any(p in tok.get("orig", "") for p in ["、", "。", "！", "？", ",", "!"]):
            m_count += 1.2
        weights.append(max(0.7, m_count))
    
    total_w = sum(weights)
    lead_in = 0.10  # Japanese TTS initial breath/silence (seconds)
    tail_out = 0.18 # trailing pause
    active_dur = max(0.4, total_duration - (lead_in + tail_out))
    
    ranges = []
    cur_t = lead_in
    for w in weights:
        dur = (w / total_w) * active_dur
        ranges.append((cur_t, cur_t + dur))
        cur_t += dur
    return ranges

def render_dialogue_karaoke_frame(
    tokens: list,
    category_label: str,
    title_label: str,
    english_meaning: str,
    grammar_text: str,
    current_time: float,
    total_duration: float,
    jlpt_level: str = "N3"
) -> Image.Image:
    """Renders 1080p transparent RGBA overlay with real-time Karaoke Follow-Along highlighting."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top & Bottom Dark Vignettes
    for y in range(80):
        alpha = int(220 * (1.0 - (y / 80.0)))
        draw.line([(0, y), (1920, y)], fill=(10, 15, 28, alpha))
        
    for y in range(540, 1080):
        rel = (y - 540) / 540.0
        alpha = int(240 * (rel ** 0.85))
        draw.line([(0, y), (1920, y)], fill=(8, 12, 22, alpha))

    # Top Brand Bar
    draw_top_brand_bar(draw, 1920, category_label, jlpt_level)

    # Category Pill
    draw.rounded_rectangle([(50, 80), (460, 120)], radius=10, fill=(30, 41, 59, 210))
    draw.text((65, 87), f"[ DIALOGUE & SHADOWING ]", fill=(244, 114, 182), font=get_font(18))

    # Main 3-Tier Dialogue Card
    card_x, card_y, card_w, card_h = 50, 580, 1820, 440
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=22, fill=(10, 15, 28, 230), outline=(51, 65, 85, 200), width=2)

    # Dynamic Auto-Fit Font Sizing
    max_tokens_w = card_w - 70 # 1750px
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

    # Auto-scale down smoothly if sentence is long, preventing any card overflow
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

    # Millisecond mora-accurate time ranges
    time_ranges = compute_mora_ranges(tokens, total_duration)

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        st, et = time_ranges[i]
        is_active = (st <= current_time <= et)

        if is_active:
            # Signature Glowing Gold Capsule
            draw.rounded_rectangle([(curr_x + 2, y_kana - 10), (curr_x + w - 2, y_romaji + 38)], radius=14, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            # Active Indicator Dot
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 22), (dot_cx + 6, y_kana - 10)], fill=(220, 38, 38))
            c_kana = (180, 83, 9)
            c_jp = (15, 23, 42)
            c_ro = (180, 83, 9)
        else:
            c_kana = (148, 163, 184)
            c_jp = (255, 255, 255)
            c_ro = (148, 163, 184)

        # 1. Furigana
        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=font_kana)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=c_kana, font=font_kana)

        # 2. Main Japanese
        jw = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=c_jp, font=font_jp)

        # 3. Romaji
        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=font_romaji)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=c_ro, font=font_romaji)

        curr_x += w

    # Divider
    draw.line([(card_x + 35, card_y + 215), (card_x + card_w - 35, card_y + 215)], fill=(51, 65, 85, 180), width=2)

    # English Meaning
    font_en = get_font(26)
    draw.text((card_x + 40, card_y + 230), f"Meaning:  {english_meaning}", fill=(226, 232, 240), font=font_en)

    # Grammar / Culture Box (Clean ASCII symbols, zero missing glyphs)
    if grammar_text:
        draw.rounded_rectangle([(card_x + 40, card_y + 285), (card_x + card_w - 40, card_y + 365)], radius=12, fill=(30, 41, 59, 230), outline=(244, 114, 182, 180), width=1)
        clean_g = grammar_text.replace("▶", ">").replace("􀀀", ">").replace("■", "•").strip()
        draw.text((card_x + 60, card_y + 295), f"[ GRAMMAR POINT ]  {clean_g}", fill=(244, 114, 182), font=get_font(20))
        draw.text((card_x + 60, card_y + 325), "Repeat aloud in Japanese • Match pitch accent and natural Tokyo phrasing", fill=(255, 255, 255), font=get_font(20))

    # Bottom Live Audio Indicator
    draw.rounded_rectangle([(card_x, card_y + 380), (card_x + card_w, card_y + 425)], radius=10, fill=(15, 23, 42, 230))
    draw.text((card_x + 25, card_y + 392), "[ SHADOWING ACTIVE ]  Tokyo Standard ja-JP-Nanami (100% Japanese Dialogue)", fill=(56, 189, 248), font=get_font(20))

    return img

def render_breakdown_frame(
    sentence_ja: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    current_time: float,
    total_duration: float,
    chapter_title: str = "Sentence Breakdown",
    jlpt_level: str = "N3",
    ja_duration: float = 0.0,
    tokens: list = None,
    timings: dict = None
) -> Image.Image:
    """Renders 1080p transparent RGBA micro-lesson breakdown HUD (Vocab Grid Cards + Active Grammar Spotlight + Multi-Voice Highlight)."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dark translucent background backing
    draw.rectangle([(0, 0), (1920, 1080)], fill=(10, 15, 28, 220))

    # Top Brand Ribbon
    draw_top_brand_bar(draw, 1920, chapter_title, jlpt_level)

    num_cards = min(5, len(vocab_list))
    active_vocab_idx = None
    spotlight_active = False
    is_ja_focus = False
    is_en_trans = False
    active_vocab_is_ja = False

    if timings:
        target_ja_dur = timings.get("target_ja_dur", 4.0)
        target_end = timings.get("target_end", 8.0)
        vocab_timings = timings.get("vocab_timings", [])
        spotlight_start = timings.get("spotlight_start", 20.0)

        if current_time < target_ja_dur:
            is_ja_focus = True
        elif current_time < target_end:
            is_en_trans = True
        elif current_time >= spotlight_start:
            spotlight_active = True
        else:
            for vt in vocab_timings:
                if vt["start"] <= current_time < vt["end"]:
                    active_vocab_idx = vt["idx"]
                    active_vocab_is_ja = (current_time < vt["ja_end"])
                    break
    elif ja_duration > 0.0:
        if current_time < ja_duration:
            is_ja_focus = True
        else:
            t_en = current_time - ja_duration
            rem_dur = max(1.0, total_duration - ja_duration)
            vocab_window = rem_dur * 0.55
            if t_en >= vocab_window:
                spotlight_active = True
            else:
                card_dur = vocab_window / max(1, num_cards)
                active_vocab_idx = min(num_cards - 1, int(t_en / card_dur))
    else:
        vocab_window = total_duration * 0.60
        card_dur = vocab_window / max(1, num_cards)
        if current_time >= vocab_window:
            spotlight_active = True
        else:
            active_vocab_idx = min(num_cards - 1, int(current_time / card_dur))

    # Category Pill & Target Sentence Bar
    if is_ja_focus:
        draw.rounded_rectangle([(50, 80), (620, 120)], radius=10, fill=(30, 41, 59, 230), outline=(245, 158, 11), width=2)
        draw.text((65, 87), f"[ JAPANESE AUDIO FOCUS ]  Native Dialogue & Pronunciation", fill=(254, 240, 138), font=get_font(18))

        draw.rounded_rectangle([(50, 135), (1870, 195)], radius=12, fill=(30, 41, 59, 245), outline=(245, 158, 11), width=3)
        draw.rounded_rectangle([(1530, 145), (1850, 185)], radius=8, fill=(225, 29, 72))
        draw.text((1545, 152), "[ AUDIO: NATIVE JA ]", fill=(255, 255, 255), font=get_font(18))

        # Real-time Karaoke Follow-Along Highlighting inside Target Dialogue Box
        font_pfx = get_font(26)
        pfx_text = "Target Dialogue:  "
        draw.text((70, 148), pfx_text, fill=(148, 163, 184), font=font_pfx)
        pfx_w = draw.textbbox((0, 0), pfx_text, font=font_pfx)[2]

        cur_x = 70 + pfx_w
        font_tok = get_font(28)

        target_ja_t = timings.get("target_ja_dur", ja_duration) if timings else ja_duration
        if tokens and len(tokens) > 0 and target_ja_t > 0:
            time_ranges = compute_mora_ranges(tokens, target_ja_t)
            for idx, tok in enumerate(tokens):
                st, et = time_ranges[idx] if idx < len(time_ranges) else (0, target_ja_t)
                is_active_tok = (st <= current_time <= et)
                tok_str = tok.get("orig", "")
                t_w = draw.textbbox((0, 0), tok_str, font=font_tok)[2]

                if is_active_tok:
                    draw.rounded_rectangle([(cur_x - 4, 142), (cur_x + t_w + 4, 188)], radius=8, fill=(254, 240, 138), outline=(245, 158, 11), width=2)
                    dot_cx = cur_x + t_w // 2
                    draw.ellipse([(dot_cx - 4, 135), (dot_cx + 4, 143)], fill=(220, 38, 38))
                    draw.text((cur_x, 148), tok_str, fill=(15, 23, 42), font=font_tok)
                else:
                    draw.text((cur_x, 148), tok_str, fill=(255, 255, 255), font=font_tok)
                cur_x += t_w + 8
        else:
            draw.text((70 + pfx_w, 148), sentence_ja, fill=(254, 240, 138), font=font_tok)
    elif is_en_trans:
        draw.rounded_rectangle([(50, 80), (620, 120)], radius=10, fill=(30, 41, 59, 220), outline=(56, 189, 248), width=2)
        draw.text((65, 87), f"[ ENGLISH TRANSLATION ]  Sentence Meaning & Context", fill=(56, 189, 248), font=get_font(18))

        draw.rounded_rectangle([(50, 135), (1870, 195)], radius=12, fill=(15, 23, 42, 235), outline=(56, 189, 248), width=2)
        draw.text((70, 148), f"Target Dialogue:  {sentence_ja}", fill=(255, 255, 255), font=get_font(28))
        draw.rounded_rectangle([(1500, 145), (1850, 185)], radius=8, fill=(37, 99, 235))
        draw.text((1520, 152), "HOST • ANDREW (EN)", fill=(255, 255, 255), font=get_font(18))
    else:
        draw.rounded_rectangle([(50, 80), (620, 120)], radius=10, fill=(30, 41, 59, 220))
        pill_txt = "[ VOCABULARY BREAKDOWN ]  Word-by-Word Analysis" if active_vocab_idx is not None else "[ HOST BREAKDOWN ]  Sentence Structure & Nuance"
        draw.text((65, 87), pill_txt, fill=(244, 114, 182), font=get_font(18))

        draw.rounded_rectangle([(50, 135), (1870, 195)], radius=12, fill=(15, 23, 42, 235), outline=(56, 189, 248), width=2)
        draw.text((70, 148), f"Target Dialogue:  {sentence_ja}", fill=(255, 255, 255), font=get_font(28))
        draw.rounded_rectangle([(1500, 145), (1850, 185)], radius=8, fill=(37, 99, 235))
        draw.text((1520, 152), "HOST • ANDREW (EN)", fill=(255, 255, 255), font=get_font(18))

    # Vocab Grid Cards (Top Half)
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
            # Active Warm Gold Glowing Card
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=16, fill=(254, 249, 195), outline=(245, 158, 11), width=3)
            draw.ellipse([(x + card_w // 2 - 7, y - 7), (x + card_w // 2 + 7, y + 7)], fill=(220, 38, 38))
            pos_fill = (254, 240, 138)
            pos_color = (180, 83, 9)
            kana_color = (180, 83, 9)
            jp_color = (220, 38, 38) if active_vocab_is_ja else (15, 23, 42)
            meaning_color = (30, 41, 59) if active_vocab_is_ja else (220, 38, 38)
        else:
            draw.rounded_rectangle([(x, y), (x + card_w, y + card_h)], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)
            pos_fill = (30, 41, 59)
            pos_color = (244, 114, 182)
            kana_color = (56, 189, 248)
            jp_color = (255, 255, 255)
            meaning_color = (226, 232, 240)

        # POS Pill
        draw.rounded_rectangle([(x + 14, y + 14), (x + min(card_w - 14, 140), y + 44)], radius=8, fill=pos_fill)
        draw.text((x + 20, y + 20), v.get("pos", "Word"), fill=pos_color, font=get_font(17))

        # Japanese Main
        draw.text((x + 14, y + 54), v.get("orig", ""), fill=jp_color, font=get_font(30))

        # Kana & Romaji
        kana_ro = f"{v.get('kana', '')} • {v.get('romaji', '')}"
        draw.text((x + 14, y + 105), kana_ro, fill=kana_color, font=get_font(19))

        # Meaning
        draw.text((x + 14, y + 145), v.get("meaning", ""), fill=meaning_color, font=get_font(20))

    # Grammar & Culture Spotlight Card (Bottom Half)
    spot_x = 50
    spot_y = 475
    spot_w = 1820
    spot_h = 475

    clean_grammar_title = grammar_title.replace("~", "~").replace("▶", ">").replace("􀀀", ">").strip()

    if spotlight_active:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=20, fill=(15, 23, 42, 240), outline=(99, 102, 241), width=4)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=20, fill=(49, 46, 129))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR & CULTURE SPOTLIGHT ]  {clean_grammar_title}", fill=(254, 240, 138), font=get_font(26))
    else:
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + spot_h)], radius=20, fill=(15, 23, 42, 230), outline=(51, 65, 85), width=2)
        draw.rounded_rectangle([(spot_x, spot_y), (spot_x + spot_w, spot_y + 60)], radius=20, fill=(30, 41, 59))
        draw.text((spot_x + 30, spot_y + 16), f"[ GRAMMAR & CULTURE SPOTLIGHT ]  {clean_grammar_title}", fill=(244, 114, 182), font=get_font(26))

    b_y = spot_y + 80
    for bullet in grammar_bullets:
        if isinstance(bullet, (list, tuple)) and len(bullet) >= 2:
            title, desc = bullet[0], bullet[1]
        elif isinstance(bullet, str) and ":" in bullet:
            parts = bullet.split(":", 1)
            title, desc = parts[0].strip(), parts[1].strip()
        else:
            title, desc = "• Rule", str(bullet)
        
        title = title.replace("~", "~").replace("▶", ">").replace("􀀀", ">")
        desc = desc.replace("~", "~").replace("▶", ">").replace("􀀀", ">")
        
        t_font = get_font(24)
        d_font = get_font(22)
        bbox_t = draw.textbbox((0, 0), title, font=t_font)
        title_w = bbox_t[2] - bbox_t[0]
        desc_x = spot_x + 30 + max(420, title_w + 24)

        b_title_color = (254, 240, 138) if spotlight_active else (244, 114, 182)
        draw.text((spot_x + 30, b_y), title, fill=b_title_color, font=t_font)
        draw.text((desc_x, b_y), desc, fill=(255, 255, 255), font=d_font)
        b_y += 75

    # Bottom App CTA
    draw.rounded_rectangle([(spot_x, 970), (spot_x + spot_w, 1030)], radius=12, fill=(10, 15, 28))
    draw.text((spot_x + 25, 985), "[ TOKYOFLOW ACADEMY ]  Hosted & Explained by Andrew • Practice pitch detection in iOS App", fill=(56, 189, 248), font=get_font(22))

    return img

def render_lower_third_story_overlay(
    chapter_num: int,
    chapter_title: str,
    title_main: str,
    narration_text: str,
    jlpt_level: str = "N/A"
) -> Image.Image:
    """Renders sleek, low-profile Lower-Third rectangular subtitle bar at the bottom, leaving 80% screen clear for movie action."""
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon (Low-profile)
    draw_top_brand_bar(draw, 1920, chapter_title, jlpt_level)

    # Bottom Dark Vignette
    for y in range(700, 1080):
        rel = (y - 700) / 380.0
        alpha = int(230 * (rel ** 0.85))
        draw.line([(0, y), (1920, y)], fill=(8, 12, 22, alpha))

    # Sleek Lower-Third Subtitle Rectangle (Pinned to y=770..1030)
    box_x, box_y, box_w, box_h = 50, 770, 1820, 260
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=20, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=2)

    # Header Bar inside Lower-Third
    draw.text((box_x + 35, box_y + 20), f"[ CH {chapter_num} • {title_main.upper()} ]", fill=(254, 240, 138), font=get_font(26))
    draw.rounded_rectangle([(box_x + box_w - 380, box_y + 15), (box_x + box_w - 35, box_y + 55)], radius=10, fill=(37, 99, 235, 220))
    draw.text((box_x + box_w - 365, box_y + 22), "HOST • ANDREW (EN)", fill=(255, 255, 255), font=get_font(18))

    # Divider
    draw.line([(box_x + 35, box_y + 65), (box_x + box_w - 35, box_y + 65)], fill=(51, 65, 85, 200), width=1)

    # Wrap narration text into 2-3 large readable lines
    font_body = get_font(28)
    words = narration_text.split(" ")
    lines = []
    curr_line = ""
    for w in words:
        test_line = curr_line + (" " if curr_line else "") + w
        bbox = draw.textbbox((0, 0), test_line, font=font_body)
        if (bbox[2] - bbox[0]) < (box_w - 70):
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)

    ty = box_y + 80
    for line in lines[:3]:
        draw.text((box_x + 35, ty), line, fill=(241, 245, 249), font=font_body)
        ty += 46

    # Bottom Pill
    draw.rounded_rectangle([(box_x + 35, box_y + box_h - 45), (box_x + box_w - 35, box_y + box_h - 10)], radius=8, fill=(15, 23, 42))
    draw.text((box_x + 50, box_y + box_h - 38), "[ TOKYOFLOW MASTERCLASS ]  100% English Narration • Real-Time Cinema Breakdown", fill=(56, 189, 248), font=get_font(18))

    return img

def render_master_thumbnail(output_dir: str):
    """Generates 16:9 1080p Masterclass YouTube Thumbnail using authentic movie HD hero shot of main protagonist."""
    thumb_out = os.path.join(output_dir, "thumbnail.jpg")
    width, height = 1920, 1080
    
    # 1. Authentic Main Character (Elena Funado / Hikari Mitsushima) Hero Shot
    hero_frame_path = "tmp/videogen/elena_closeups/t2_0051.jpg"
    if not os.path.exists(hero_frame_path):
        hero_frame_path = "tmp/videogen/character_heroes/elena_hero.jpg"
    
    if os.path.exists(hero_frame_path):
        raw_img = Image.open(hero_frame_path).convert("RGB")
        # Place character dynamically on the right half
        base_img = Image.new("RGB", (width, height), (15, 23, 42))
        base_img.paste(raw_img.resize((int(width * 1.1), int(height * 1.1)), Image.Resampling.LANCZOS), (80, -50))
    else:
        base_img = Image.new("RGB", (width, height), color=(10, 15, 28))

    # Photographic Contrast / Smooth Left Fade
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Smooth non-linear dark gradient from left to right (fading out before character)
    import math
    for x in range(width):
        if x < 1150:
            rel = x / 1150.0
            alpha = int(245 * (0.5 * (1 + math.cos(rel * math.pi))))
            draw_ov.line([(x, 0), (x, height)], fill=(8, 12, 22, alpha))

    # Bottom Vignette
    for y in range(850, height):
        rel = (y - 850) / 230.0
        alpha = int(220 * (rel ** 1.1))
        draw_ov.line([(0, y), (width, y)], fill=(6, 10, 18, alpha))

    img = Image.alpha_composite(base_img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 1. Top-Left Brand Pill
    draw.rounded_rectangle([(60, 45), (380, 105)], radius=18, fill=(255, 255, 255))
    draw.text((85, 58), "TokyoFlow Cinema", fill=(225, 29, 72), font=get_font(26))

    # 2. Top-Right Badge (WL.01)
    draw.rounded_rectangle([(width - 380, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 350, 58), "JLPT N5-N2 | WL.01", fill=(255, 255, 255), font=get_font(26))

    # 3. Giant 3D Yellow Hook (Left Aligned)
    font_hook = get_font(96)
    hook_lines = ["2.7m/s", "OR DIE?"]
    hy = 145
    for line in hook_lines:
        for dx in range(-5, 6, 2):
            for dy in range(-5, 6, 2):
                draw.text((60 + dx, hy + dy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 115

    # Movie Sub-Hook
    draw.text((65, 385), "LAST MILE (ラストマイル)", fill=(244, 114, 182), font=get_font(38))

    # 4. Japanese Soul Quote Box (Left Column: width=860, perfectly avoids character face)
    quote_box_w = 860
    quote_box_y = 460
    draw.rounded_rectangle([(60, quote_box_y), (60 + quote_box_w, quote_box_y + 400)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    draw.text((90, quote_box_y + 25), "[ CLIMAX SOUL PHRASE ]", fill=(56, 189, 248), font=get_font(22))
    
    font_jp_quote = get_font(38)
    jp_text_1 = "ベルトコンベアを"
    jp_text_2 = "止めるわけにはいきません。"
    draw.text((90, quote_box_y + 70), jp_text_1, fill=(255, 255, 255), font=font_jp_quote)
    draw.text((90, quote_box_y + 125), jp_text_2, fill=(254, 240, 138), font=font_jp_quote)
    
    draw.text((90, quote_box_y + 200), "JLPT N3 Grammar: ~わけにはいかない", fill=(244, 114, 182), font=get_font(24))
    draw.text((90, quote_box_y + 245), '\"We cannot afford to stop the conveyor belt.\"', fill=(226, 232, 240), font=get_font(25))
    draw.text((90, quote_box_y + 300), "Explosive mystery meets corporate survival Japanese", fill=(148, 163, 184), font=get_font(21))
    draw.text((90, quote_box_y + 345), "Main Star: 満島ひかり (Hikari Mitsushima as Elena)", fill=(56, 189, 248), font=get_font(20))

    # 5. Bottom Ribbon (Full width)
    draw.rounded_rectangle([(60, height - 120), (width - 60, height - 45)], radius=16, fill=(225, 29, 72))
    draw.text((90, height - 98), " 100% NATIVE CINEMA AUDIO  •  KARAOKE SHADOWING GYM  •  FULL 25-MIN MASTERCLASS", fill=(255, 255, 255), font=get_font(24))

    img.save(thumb_out, quality=95)
    print(f" Saved Master HD Thumbnail: {thumb_out}")

# ==========================================
# MASTER VIDEO PRODUCTION PIPELINE
# ==========================================

def render_full_master_video(output_dir: str):
    """Renders 1080p master video with smooth full-motion movie background, karaoke follow-along & lower-third HUD."""
    print("\n================================================================================")
    print(" RENDERING 1080P MASTERCLASS MOVIE (SMOOTH FULL-MOTION MOVIE + DYNAMIC HUD)...")
    print("================================================================================")
    
    tmp_vid_dir = "tmp/videogen/cinema_ep01"
    os.makedirs(tmp_vid_dir, exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)

    audio_dir = os.path.join(output_dir, "audio")
    segment_mp4s = []
    total_duration = 0.0

    fps = 30

    for ch in CINEMA_SCREENPLAY:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]
        scene_clip = ch.get("scene_clip", "scene_01_warehouse")
        clean_mp4 = f"tmp/videogen/clean_movie_clips/{scene_clip}.mp4"

        for seg in ch["segments"]:
            seg_id = seg["seg_id"].replace(".", "_")
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            out_mp4 = os.path.join(tmp_vid_dir, f"clip_{seg_id}.mp4")

            if not os.path.exists(audio_path):
                print(f"   Skipping missing audio: {seg_id}")
                continue

            # Dedicated unique non-repeating movie action clip for every segment
            unique_mp4 = f"tmp/videogen/unique_movie_clips/seg_{seg_id}.mp4"
            if os.path.exists(unique_mp4):
                clean_mp4 = unique_mp4
            else:
                clean_mp4 = f"tmp/videogen/clean_movie_clips/{scene_clip}.mp4"

            duration = get_audio_duration(audio_path)
            total_duration += duration + 0.2
            total_frames = int((duration + 0.2) * fps)

            # Native FFmpeg video compositing: [0:v] is smooth movie MP4, [1:v] is transparent RGBA HUD pipe
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
                "-preset", "fast",
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
            seg_type = seg.get("type", "")

            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps

                    if seg.get("lang") == "ja":
                        # 1. Japanese Dialogue or Shadowing Drill -> Karaoke Follow-Along Transparent HUD
                        frame = render_dialogue_karaoke_frame(
                            tokens=seg.get("tokens", [{"orig": seg.get("content", ""), "kana": seg.get("furi", ""), "romaji": seg.get("romaji", "")}]),
                            category_label=ch_title,
                            title_label=f"Scene {seg['seg_id']} • {seg.get('character')}",
                            english_meaning=seg.get("meaning", ""),
                            grammar_text=seg.get("grammar", ""),
                            current_time=t,
                            total_duration=duration,
                            jlpt_level=seg.get("jlpt", "N3")
                        )
                    elif "breakdown" in seg_type or "lesson" in seg_type or "cultural" in seg_type:
                        # 2. Breakdown Micro-Lesson -> Vocab Grid + Active Grammar Spotlight + Target Karaoke
                        tokens = seg.get("tokens")
                        if not tokens:
                            ref_s = seg.get("ref_sentence", "")
                            for s in ch["segments"]:
                                if s.get("lang") == "ja" and s.get("tokens"):
                                    c_txt = s.get("content", "")
                                    if ref_s and (ref_s in c_txt or c_txt in ref_s or any(tok.get("orig", "") in ref_s for tok in s.get("tokens", []))):
                                        tokens = s.get("tokens")
                                        break
                        if not tokens:
                            raw_s = seg.get("ref_sentence", seg.get("content", ""))
                            tokens = [{"orig": raw_s, "kana": raw_s, "romaji": ""}]

                        timings_json_path = os.path.join(audio_dir, f"seg_{seg_id}.timings.json")
                        b_timings = seg.get("breakdown_timings")
                        if not b_timings and os.path.exists(timings_json_path):
                            try:
                                with open(timings_json_path, "r", encoding="utf-8") as tf:
                                    b_timings = json.load(tf)
                            except Exception:
                                pass

                        frame = render_breakdown_frame(
                            sentence_ja=seg.get("ref_sentence", seg.get("content", "")),
                            vocab_list=seg.get("vocab", []),
                            grammar_title=seg.get("grammar_title", "JLPT Grammar & Culture Spotlight"),
                            grammar_bullets=seg.get("grammar_bullets", []),
                            current_time=t,
                            total_duration=duration,
                            chapter_title=ch_title,
                            jlpt_level=seg.get("jlpt", "N3"),
                            ja_duration=seg.get("ja_duration", 0.0),
                            tokens=tokens,
                            timings=b_timings
                        )
                    else:
                        # 3. Storytelling & Narration -> Sleek Lower-Third Rectangle Subtitle Bar (80% screen clear)
                        frame = render_lower_third_story_overlay(
                            chapter_num=ch_id,
                            chapter_title=ch_title,
                            title_main=f"Scene {seg['seg_id']} • {ch_title}",
                            narration_text=seg.get("content", ""),
                            jlpt_level=seg.get("jlpt", "N/A")
                        )

                    proc.stdin.write(frame.tobytes())
            except (BrokenPipeError, IOError):
                pass
            finally:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait()

            segment_mp4s.append(out_mp4)
            print(f"   Rendered Smooth Full-Motion Clip: clip_{seg_id}.mp4 ({duration:.1f}s)")

    # Concatenate all segment clips into Master Video
    concat_list_file = os.path.join(tmp_vid_dir, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for v in segment_mp4s:
            f.write(f"file '{os.path.abspath(v)}'\n")

    final_master_mp4 = os.path.join(output_dir, "last_mile_cinema_masterclass_full.mp4")
    published_mp4 = "output/videos/tokyoflow_cinema_wl01_last_mile.mp4"

    print(f"\n Concatenating {len(segment_mp4s)} Full-Motion Smooth clips into Final Master Video...")
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        final_master_mp4
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    import shutil
    shutil.copyfile(final_master_mp4, published_mp4)

    print(f" Master 1080p Cinema Video Ready: {final_master_mp4}")
    print(f" Channel Publish Video Ready: {published_mp4}")
    print(f" Total Video Duration: {total_duration / 60.0:.2f} minutes")

# ==========================================
# MAIN EXECUTION ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE CINEMA MASTERCLASS • PRODUCTION PIPELINE V2")
    print(f" Episode: WL.01 {EPISODE_METADATA['movie_title_en']} ({EPISODE_METADATA['movie_title_ja']}) [Shorts Lead: WS.01]")
    print("================================================================================")

    output_dir = "output/cinema_masterclass/wl01_last_mile"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Build Machine-Readable Spec
    build_production_spec(output_dir)

    # 2. Build Fountain & JSON Screenplays
    build_script_json_and_fountain(output_dir)

    # 3. Build Zero-Emoji Metadata & 25 SEO Tags
    build_metadata_md(output_dir)

    # 4. Build 16:9 4K Master Thumbnail Prompt & Graphic
    build_thumbnail_prompt_md(output_dir)
    render_master_thumbnail(output_dir)

    # 5. Synthesize Dual-Voice Audio Assets (Slower JA, Anti-Pop)
    await synthesize_all_audio_tracks(output_dir)

    # 6. Render Dynamic Video Masterpiece (Karaoke + Micro-Lesson Breakdown HUD)
    render_full_master_video(output_dir)

    print("\n================================================================================")
    print(" PRODUCTION COMPLETED SUCCESSFULLY!")
    print(f" Master Deliverables generated inside: {output_dir}")
    print("================================================================================")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
