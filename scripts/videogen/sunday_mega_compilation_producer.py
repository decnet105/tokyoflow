#!/usr/bin/env python3
"""
TokyoFlow Japanese • Sunday Mega-Compilation & Cultural Masterclass Producer
===========================================================================
Produces the 25-30 minute comprehensive Monday-to-Friday micro-lessons +
Deep Japanese Culture, Customs, Etiquette & Travel Learning Masterclass.

Pipeline Specifications:
- 100% Authentic 4K Real Tokyo Photography (Zero AI Cartoon / Zero Baked-in Text Clutter)
- Crystal Clear Subtitle & Typography Safety (Zero Text Collision / Opaque Contrast Card)
- 1080p Full HD (1920x1080, 30fps, H.264 / AAC 44.1kHz Stereo)
- Dual-Voice Role Separation (Nanami JA @ -10% slow + Andrew EN @ +2%)
- 3-Tier Ruby Typography with Word-by-Word Glowing Yellow Karaoke
- Bilingual Breakdown HUD (Vocabulary Grid + Active Grammar & Cultural Spotlight)
- High-CTR Master Thumbnail (16:9 1920x1080) & Minimalist Shorts Cover (9:16 1080x1920)
- Zero-URL & Zero-Emoji Clean YouTube Launch Kit with Millisecond-Precise Timestamps
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
# MASTER COMPILATION METADATA
# ==========================================
COMPILATION_METADATA = {
    "series_code": "WM.01",
    "shorts_code": "WS.01",
    "release_folder": "WM01-weekday_survival_mega_compilation-v1.0",
    "title_en": "Monday to Friday Tokyo Survival All-in-One + Japanese Culture, Customs & Travel 28-Min Masterclass",
    "title_ja": "【保存版】月〜金Tokyo日常サバイバル＆日本文化・風俗・旅行完全マスター28分スペシャル",
    "jlpt_level": "JLPT N5-N3",
    "target_duration_mins": 28,
    "district": "Tokyo Metropolitan (Shinjuku, Shibuya, Akihabara, Asakusa, Roppongi, Ginza)",
    "description_summary": "The ultimate 28-minute Japanese learning mega-compilation combining Monday-to-Friday daily survival scenarios (Transit, Kombini, Izakaya, Akiba, Ramen, Sento/Onsen, Shrine/Temple) with in-depth cultural insights, travel etiquette, bathing customs, and conversation formulas."
}

# ==========================================
# 8-MODULE + PROLOGUE/EPILOGUE SCREENPLAY (28 MINS)
# ==========================================
MEGA_SCREENPLAY = [
    # ----------------------------------------------------
    # PROLOGUE: WELCOME & MASTERCLASS ROADMAP (00:00 - 01:30)
    # ----------------------------------------------------
    {
        "chapter_id": 0,
        "chapter_title": "PROLOGUE • THE ULTIMATE TOKYO SURVIVAL ROADMAP",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "0_1",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Welcome to the TokyoFlow Weekend Mega-Compilation. Today, we bring together the complete Monday through Friday Tokyo survival curriculum into one seamless 28-minute masterclass. Whether you are prepping for the JLPT, planning your dream trip to Japan, or wanting to understand authentic Japanese life, this episode is your definitive guide.",
                "duration_est": 21.0,
                "jlpt": "Roadmap"
            },
            {
                "seg_id": "0_2",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Over the next twenty-eight minutes, we will cover seven essential weekday and weekend life survival zones: Tokyo train transit, convenience store checkout, izakaya pub dining, Akihabara anime shopping, ramen ticket ordering, onsen bathhouse etiquette, and shrine temple customs. Plus, we will dive deep into fascinating Japanese cultural secrets, from train manner mode and bowing angles to zero-tipping and omotenashi hospitality. Let us begin with Day 1: Tokyo train mastery.",
                "duration_est": 27.0,
                "jlpt": "Curriculum"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 1 [MONDAY]: TRANSIT, TRAIN MELODIES & MANNER MODE (01:30 - 05:15)
    # ----------------------------------------------------
    {
        "chapter_id": 1,
        "chapter_title": "DAY 1 • YAMANOTE LINE TRANSIT & TRAIN MANNERS",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_yamanote_platform.jpg",
        "segments": [
            {
                "seg_id": "1_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Day 1 begins on the platforms of Shinjuku Station, the busiest transit hub in the world with over 3.5 million daily passengers. When stepping onto a JR platform, the first sound you will hear is the automated arrival broadcast.",
                "duration_est": 14.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "1_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "まもなく、2番線に山手線内回りがまいります。黄色い点字ブロックの内側までお下がりください。",
                "furi": "まもなく、 にばんせん に やまのてせん うちまわり が まいります。 きいろい てんじぶろっく の うちがわ まで おさがりください。",
                "romaji": "Mamonaku, nibansen ni Yamanotesen uchimawari ga mairimasu. Kiiroi tenji burokku no uchigawa made osagari kudasai.",
                "meaning": "The Yamanote Line inner loop will soon arrive at track 2. Please stand back behind the yellow tactile braille blocks.",
                "jlpt": "JLPT N4-N3",
                "grammar": "まもなく (Soon) + 参ります (Humble come) + お下がりください (Polite request)",
                "tokens": [
                    {"orig": "まもなく", "kana": "まもなく", "romaji": "mamonaku"},
                    {"orig": "2番線に", "kana": "にばんせんに", "romaji": "nibansen ni"},
                    {"orig": "山手線", "kana": "やまのてせん", "romaji": "yamanotesen"},
                    {"orig": "内回りが", "kana": "うちまわりが", "romaji": "uchimawari ga"},
                    {"orig": "まいります", "kana": "まいります", "romaji": "mairimasu"},
                    {"orig": "黄色い", "kana": "きいろい", "romaji": "kiiroi"},
                    {"orig": "点字ブロックの", "kana": "てんじぶろっくの", "romaji": "tenji burokku no"},
                    {"orig": "内側まで", "kana": "うちがわまで", "romaji": "uchigawa made"},
                    {"orig": "お下がりください", "kana": "おさがりください", "romaji": "osagari kudasai"}
                ],
                "vocab": [
                    {"orig": "まもなく", "kana": "まもなく", "romaji": "mamonaku", "pos": "Adv (N4)", "meaning": "Soon / Shortly"},
                    {"orig": "内回り", "kana": "うちまわり", "romaji": "uchimawari", "pos": "Noun (N3)", "meaning": "Inner loop (Counter-clockwise)"},
                    {"orig": "参る", "kana": "まいる", "romaji": "mairu", "pos": "Kenjougo (N3)", "meaning": "Humble 'To come'"},
                    {"orig": "点字ブロック", "kana": "てんじぶろっく", "romaji": "tenji burokku", "pos": "Noun (N3)", "meaning": "Tactile braille paving"},
                    {"orig": "下がる", "kana": "さがる", "romaji": "sagaru", "pos": "Verb (N4)", "meaning": "To step back / Stand back"}
                ],
                "grammar_title": "Humble 参る (Mairu) & Polite お〜ください",
                "grammar_bullets": [
                    ("• Humble Transit Verb", "参ります (mairimasu) is the humble equivalent of 来ます (kimasu), standard on all Japanese railways"),
                    ("• Polite Request Pattern", "お + Verb stem + ください (お下がりください = Please step back)"),
                    ("• Inner vs Outer Loop", "内回り (Uchimawari = Counter-clockwise) vs 外回り (Sotomawari = Clockwise)")
                ],
                "duration_est": 10.0
            },
            {
                "seg_id": "1_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Let us break down the transit grammar. 'Mairimasu' is the humble form of 'kimasu', used in public transit announcements across Japan. When the broadcast says 'osagari kudasai', notice the honorific prefix 'o' combined with the verb stem 'sagari' and 'kudasai'. This forms the universal polite public request formula.",
                "duration_est": 21.0,
                "jlpt": "N4-N3 Breakdown",
                "ref_sentence": "まもなく、2番線に山手線内回りがまいります。黄色い点字ブロックの内側までお下がりください。",
                "vocab": [
                    {"orig": "まもなく", "kana": "まもなく", "romaji": "mamonaku", "pos": "Adv (N4)", "meaning": "Soon / Shortly"},
                    {"orig": "内回り", "kana": "うちまわり", "romaji": "uchimawari", "pos": "Noun (N3)", "meaning": "Inner loop (Counter-clockwise)"},
                    {"orig": "参る", "kana": "まいる", "romaji": "mairu", "pos": "Kenjougo (N3)", "meaning": "Humble 'To come'"},
                    {"orig": "点字ブロック", "kana": "てんじぶろっく", "romaji": "tenji burokku", "pos": "Noun (N3)", "meaning": "Tactile braille paving"},
                    {"orig": "下がる", "kana": "さがる", "romaji": "sagaru", "pos": "Verb (N4)", "meaning": "To step back / Stand back"}
                ],
                "grammar_title": "Humble 参る (Mairu) & Polite お〜ください",
                "grammar_bullets": [
                    ("• Humble Transit Verb", "参ります (mairimasu) is the humble equivalent of 来ます (kimasu), standard on all Japanese railways"),
                    ("• Polite Request Pattern", "お + Verb stem + ください (お下がりください = Please step back)"),
                    ("• Inner vs Outer Loop", "内回り (Uchimawari = Counter-clockwise) vs 外回り (Sotomawari = Clockwise)")
                ]
            },
            {
                "seg_id": "1_2_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "すみません、中央線への乗り換えはどのホームですか？",
                "furi": "すみません、 ちゅうおうせん への のりかえ は どの ほーむ ですか？",
                "romaji": "Sumimasen, Chuuousen e no norikae wa dono hoomu desu ka?",
                "meaning": "Excuse me, which platform is the transfer for the Chuo Line?",
                "jlpt": "JLPT N5",
                "grammar": "乗り換え (Transfer) + どのホーム (Which platform?)",
                "tokens": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen"},
                    {"orig": "中央線への", "kana": "ちゅうおうせんへの", "romaji": "chuuousen e no"},
                    {"orig": "乗り換えは", "kana": "のりかえは", "romaji": "norikae wa"},
                    {"orig": "どのホーム", "kana": "どのほーむ", "romaji": "dono hoomu"},
                    {"orig": "ですか", "kana": "ですか", "romaji": "desu ka"}
                ],
                "vocab": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "pos": "Exp (N5)", "meaning": "Excuse me / Sorry"},
                    {"orig": "中央線", "kana": "ちゅうおうせん", "romaji": "chuuousen", "pos": "Noun (N5)", "meaning": "Chuo Line (Rapid)"},
                    {"orig": "乗り換え", "kana": "のりかえ", "romaji": "norikae", "pos": "Noun (N5)", "meaning": "Transfer / Connection"},
                    {"orig": "どの", "kana": "どの", "romaji": "dono", "pos": "Pronoun (N5)", "meaning": "Which"},
                    {"orig": "ホーム", "kana": "ほーむ", "romaji": "hoomu", "pos": "Noun (N5)", "meaning": "Platform / Track"}
                ],
                "grammar_title": "Transfer Formula: [Line Name] + への乗り換え",
                "grammar_bullets": [
                    ("• Particle Combo ~への", "Combines directional particle へ with possessive の (Transfer TO the line)"),
                    ("• Asking Directions", "〜はどのホームですか？ (Which platform is ~?)"),
                    ("• Natural Station Staff Reply", "7番ホームです (Platform 7) or まっすぐ進んでください (Go straight)")
                ],
                "duration_est": 6.0
            },
            {
                "seg_id": "1_2_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "This is your golden transfer phrase. Notice the particle combination 'e no'. 'E' marks direction, and 'no' connects it to 'norikae' (transfer). If you ever get turned around in Tokyo's giant stations, simply replace 'Chuuousen' with any subway or train line name.",
                "duration_est": 16.0,
                "jlpt": "N5 Breakdown",
                "ref_sentence": "すみません、中央線への乗り換えはどのホームですか？",
                "vocab": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen", "pos": "Exp (N5)", "meaning": "Excuse me / Sorry"},
                    {"orig": "中央線", "kana": "ちゅうおうせん", "romaji": "chuuousen", "pos": "Noun (N5)", "meaning": "Chuo Line (Rapid)"},
                    {"orig": "乗り換え", "kana": "のりかえ", "romaji": "norikae", "pos": "Noun (N5)", "meaning": "Transfer / Connection"},
                    {"orig": "どの", "kana": "どの", "romaji": "dono", "pos": "Pronoun (N5)", "meaning": "Which"},
                    {"orig": "ホーム", "kana": "ほーむ", "romaji": "hoomu", "pos": "Noun (N5)", "meaning": "Platform / Track"}
                ],
                "grammar_title": "Transfer Formula: [Line Name] + への乗り換え",
                "grammar_bullets": [
                    ("• Particle Combo ~への", "Combines directional particle へ with possessive の (Transfer TO the line)"),
                    ("• Asking Directions", "〜はどのホームですか？ (Which platform is ~?)"),
                    ("• Natural Station Staff Reply", "7番ホームです (Platform 7) or まっすぐ進んでください (Go straight)")
                ]
            },
            {
                "seg_id": "1_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Now for our deep Japanese cultural insight. In Japan, train etiquette is sacred. You will notice that Japanese trains are whisper quiet. Passengers switch their phones to 'Manner Mode'—meaning silent mode—and phone calls are strictly forbidden inside the train car. If you receive a call, you either decline it or quickly whisper that you are on the train and will call back.",
                "duration_est": 21.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "1_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Did you know that every train station in Tokyo has its own unique 7-second departure jingle called a 'Hassha Melody'? For example, Ebisu Station plays the famous theme from The Third Man because Yebisu Beer was founded there, and Takadanobaba Station plays Astro Boy! These melodic chimes prevent rushed boarding while reducing commuter stress.",
                "duration_est": 24.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "1_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Also, pay close attention to escalator etiquette. In Tokyo and Eastern Japan, you always stand on the left side and walk on the right side. But in Osaka and Western Japan, the rule flips: you stand on the right and walk on the left! Remembering this simple custom will make you look like a seasoned local from day one.",
                "duration_est": 20.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 2 [TUESDAY]: KOMBINI 24/7 & SEASONAL CULTURE (05:15 - 09:00)
    # ----------------------------------------------------
    {
        "chapter_id": 2,
        "chapter_title": "DAY 2 • CONVENIENCE STORE SURVIVAL & KOMBINI CULTURE",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_kombini_store.jpg",
        "segments": [
            {
                "seg_id": "2_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Day 2 brings us inside Japan's modern miracle: the convenience store, or kombini. With over fifty thousand branches of 7-Eleven, FamilyMart, and Lawson, you will visit one almost every single day. Here is the rapid-fire checkout dialogue you must master.",
                "duration_est": 16.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "2_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "お弁当温めますか？レジ袋はご利用ですか？",
                "furi": "おべんとう あたためます か？ れじぶくろ は ごりよう です か？",
                "romaji": "Obentou atatamemasu ka? Rejibukuro wa goriyou desu ka?",
                "meaning": "Would you like your lunch box heated up? Will you be using a plastic shopping bag?",
                "jlpt": "JLPT N5-N4",
                "grammar": "温めますか (Microwave question) + ご利用ですか (Polite use)",
                "tokens": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou"},
                    {"orig": "温めますか", "kana": "あたためますか", "romaji": "atatamemasu ka"},
                    {"orig": "レジ袋は", "kana": "れじぶくろは", "romaji": "rejibukuro wa"},
                    {"orig": "ご利用", "kana": "ごりよう", "romaji": "goriyou"},
                    {"orig": "ですか", "kana": "ですか", "romaji": "desu ka"}
                ],
                "vocab": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou", "pos": "Noun (N5)", "meaning": "Bento lunch box"},
                    {"orig": "温める", "kana": "あたためる", "romaji": "atatameru", "pos": "Verb (N4)", "meaning": "To warm up / Heat"},
                    {"orig": "レジ袋", "kana": "れじぶくろ", "romaji": "rejibukuro", "pos": "Noun (N5)", "meaning": "Plastic checkout bag"},
                    {"orig": "ご利用", "kana": "ごりよう", "romaji": "goriyou", "pos": "Noun (N4)", "meaning": "Polite usage / Use"}
                ],
                "grammar_title": "Kombini Register Double Question",
                "grammar_bullets": [
                    ("• Heating Response", "温めてください (Please heat it) or そのままで大丈夫です (As-is is fine)"),
                    ("• Declining Bag", "袋は大丈夫です (I'm fine without a bag / I have my own)"),
                    ("• Polite 'Go-' Prefix", "ご利用 (goriyou) adds respectful prefix ご to indicate customer usage")
                ],
                "duration_est": 6.0
            },
            {
                "seg_id": "2_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "These are the two iconic questions asked at every register. To reply to heating, say 'Atatamete kudasai' if you want it hot, or 'Sono mama de daijoubu desu' if you will eat it cold. When asked about a bag, a gentle nod with 'Daijoubu desu' is the standard polite Japanese way to decline.",
                "duration_est": 18.0,
                "jlpt": "N5 Breakdown",
                "ref_sentence": "お弁当温めますか？レジ袋はご利用ですか？",
                "vocab": [
                    {"orig": "お弁当", "kana": "おべんとう", "romaji": "obentou", "pos": "Noun (N5)", "meaning": "Bento lunch box"},
                    {"orig": "温める", "kana": "あたためる", "romaji": "atatameru", "pos": "Verb (N4)", "meaning": "To warm up / Heat"},
                    {"orig": "レジ袋", "kana": "れじぶくろ", "romaji": "rejibukuro", "pos": "Noun (N5)", "meaning": "Plastic checkout bag"},
                    {"orig": "ご利用", "kana": "ごりよう", "romaji": "goriyou", "pos": "Noun (N4)", "meaning": "Polite usage / Use"}
                ],
                "grammar_title": "Kombini Register Double Question",
                "grammar_bullets": [
                    ("• Heating Response", "温めてください (Please heat it) or そのままで大丈夫です (As-is is fine)"),
                    ("• Declining Bag", "袋は大丈夫です (I'm fine without a bag / I have my own)"),
                    ("• Polite 'Go-' Prefix", "ご利用 (goriyou) adds respectful prefix ご to indicate customer usage")
                ]
            },
            {
                "seg_id": "2_2_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "支払いはSuicaでお願いします。領収書もいただけますか？",
                "furi": "しはらい は すいか で おねがいします。 りょうしゅうしょ も いただけます か？",
                "romaji": "Shiharai wa Suica de onegaishimasu. Ryoushuusho mo itadakemasu ka?",
                "meaning": "I'll pay with Suica, please. Could I also get a tax receipt?",
                "jlpt": "JLPT N5-N4",
                "grammar": "[Payment] + でお願いします + いただけますか (Humble request)",
                "tokens": [
                    {"orig": "支払いは", "kana": "しはらいは", "romaji": "shiharai wa"},
                    {"orig": "Suicaで", "kana": "すいかで", "romaji": "suika de"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu"},
                    {"orig": "領収書も", "kana": "りょうしゅうしょも", "romaji": "ryoushuusho mo"},
                    {"orig": "いただけますか", "kana": "いただけますか", "romaji": "itadakemasu ka"}
                ],
                "vocab": [
                    {"orig": "支払い", "kana": "しはらい", "romaji": "shiharai", "pos": "Noun (N4)", "meaning": "Payment / Settle check"},
                    {"orig": "Suica", "kana": "すいか", "romaji": "suika", "pos": "Noun (N5)", "meaning": "Tokyo IC Transit Card"},
                    {"orig": "領収書", "kana": "りょうしゅうしょ", "romaji": "ryoushuusho", "pos": "Noun (N4)", "meaning": "Official itemized tax receipt"},
                    {"orig": "いただく", "kana": "いただく", "romaji": "itadaku", "pos": "Kenjougo (N4)", "meaning": "Humble 'To receive'"}
                ],
                "grammar_title": "Payment Formula & Polite Receipt Request",
                "grammar_bullets": [
                    ("• Cashless Payment Formula", "[PayPay / クレジットカード / Suica] + でお願いします"),
                    ("• Receipt Nuance", "レシート (Register slip) vs 領収書 (Official tax receipt with company name)"),
                    ("• Humble Request いただけますか", "More polite than ください; literally 'Could I humbly receive ~?'")
                ],
                "duration_est": 6.5
            },
            {
                "seg_id": "2_2_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "For payment, simply state your method followed by 'de onegaishimasu'—such as 'Kurejitto kaado de' or 'PayPay de'. If you need a formal business receipt for expense reimbursement, ask for 'ryoushuusho' instead of a standard register 'reshiito'.",
                "duration_est": 15.0,
                "jlpt": "N4 Breakdown",
                "ref_sentence": "支払いはSuicaでお願いします。領収書もいただけますか？",
                "vocab": [
                    {"orig": "支払い", "kana": "しはらい", "romaji": "shiharai", "pos": "Noun (N4)", "meaning": "Payment / Settle check"},
                    {"orig": "Suica", "kana": "すいか", "romaji": "suika", "pos": "Noun (N5)", "meaning": "Tokyo IC Transit Card"},
                    {"orig": "領収書", "kana": "りょうしゅうしょ", "romaji": "ryoushuusho", "pos": "Noun (N4)", "meaning": "Official itemized tax receipt"},
                    {"orig": "いただく", "kana": "いただく", "romaji": "itadaku", "pos": "Kenjougo (N4)", "meaning": "Humble 'To receive'"}
                ],
                "grammar_title": "Payment Formula & Polite Receipt Request",
                "grammar_bullets": [
                    ("• Cashless Payment Formula", "[PayPay / クレジットカード / Suica] + でお願いします"),
                    ("• Receipt Nuance", "レシート (Register slip) vs 領収書 (Official tax receipt with company name)"),
                    ("• Humble Request いただけますか", "More polite than ください; literally 'Could I humbly receive ~?'")
                ]
            },
            {
                "seg_id": "2_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Japanese kombini culture is famous worldwide for its seasonal limited editions, known as 'Kikan Gentei'. In spring, shelves turn pink with sakura flavored lattes and sweets. In autumn, you will find rich chestnut and sweet potato treats, and in winter, steaming hot oden stew counters and nikuman meat buns right beside the register.",
                "duration_est": 22.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "2_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When ordering from the winter Oden counter, pick your favorite simmered ingredients like Daikon radish, Hanpen fish cake, and hard-boiled Tamago. The staff will ask if you want 'Karashi' (spicy Japanese yellow mustard) on the side of your bowl. Say 'Karashi tsukete kudasai' for the authentic winter flavor kick!",
                "duration_est": 22.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "2_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Here is a fun travel hack: when opening an onigiri rice ball, follow the numbered red pull-tabs 1, 2, and 3. Pull tab 1 straight down the middle and all the way around the back, then gently slide corners 2 and 3 off. This clever packaging keeps the crisp seaweed separated from the moist rice until the exact moment you take your first bite!",
                "duration_est": 22.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 3 [WEDNESDAY]: IZAKAYA NIGHT & DRINKING ETIQUETTE (09:00 - 12:45)
    # ----------------------------------------------------
    {
        "chapter_id": 3,
        "chapter_title": "DAY 3 • IZAKAYA SHOWA PUB ORDERING & NIGHTLIFE ETIQUETTE",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_izakaya_yokocho.jpg",
        "segments": [
            {
                "seg_id": "3_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Day 3 takes us into the lantern-lit alleys of Shinjuku Omoide Yokocho. The Japanese izakaya is more than a restaurant; it is where colleagues and friends unwind after work. The moment you sit down, you receive a hot damp towel called an oshibori and prepare your opening order.",
                "duration_est": 18.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "3_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "とりあえず生ビール二つお願いします！焼き鳥は塩とタレ、どちらがおすすめですか？",
                "furi": "とりあえず なまびーる ふたつ おねがいします！ やきとり は しお と たれ、 どちら が おすすめ です か？",
                "romaji": "Toriaezu nama biiru futatsu onegaishimasu! Yakitori wa shio to tare, dochira ga osusume desu ka?",
                "meaning": "Two draft beers to start, please! Between salt and sweet tare sauce, which do you recommend for the yakitori skewers?",
                "jlpt": "JLPT N5-N4",
                "grammar": "とりあえず (For now / To start) + どちら (Which of two) + おすすめ (Recommendation)",
                "tokens": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu"},
                    {"orig": "生ビール", "kana": "なまびーる", "romaji": "nama biiru"},
                    {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu"},
                    {"orig": "焼き鳥は", "kana": "やきとりは", "romaji": "yakitori wa"},
                    {"orig": "塩と", "kana": "しおと", "romaji": "shio to"},
                    {"orig": "タレ", "kana": "たれ", "romaji": "tare"},
                    {"orig": "どちらが", "kana": "どちらが", "romaji": "dochira ga"},
                    {"orig": "おすすめですか", "kana": "おすすめですか", "romaji": "osusume desu ka"}
                ],
                "vocab": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "pos": "Adv (N4)", "meaning": "To begin with / For now"},
                    {"orig": "生ビール", "kana": "なまびーる", "romaji": "nama biiru", "pos": "Noun (N5)", "meaning": "Draft beer on tap"},
                    {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu", "pos": "Counter (N5)", "meaning": "Two items"},
                    {"orig": "焼き鳥", "kana": "やきとり", "romaji": "yakitori", "pos": "Noun (N5)", "meaning": "Grilled chicken skewers"},
                    {"orig": "おすすめ", "kana": "おすすめ", "romaji": "osusume", "pos": "Noun (N4)", "meaning": "Recommendation"}
                ],
                "grammar_title": "Toriaezu Formula & Comparative Recommendation",
                "grammar_bullets": [
                    ("• The Izakaya Golden Opener", "とりあえず生 (Toriaezu nama) = 'Draft beer to start!' ensures instant table delivery"),
                    ("• Salt vs Tare Sauce", "塩 (Shio = Savory salt) highlights ingredient quality; タレ (Tare = Sweet soy glaze)"),
                    ("• Two-Choice Question", "AとB、どちらが〜ですか？ (Between A and B, which one is ~?)")
                ],
                "duration_est": 8.5
            },
            {
                "seg_id": "3_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "'Toriaezu nama' is the iconic phrase heard in every pub across Japan. 'Toriaezu' means 'for now' or 'to start'. Ordering draft beers first gives the kitchen time while getting drinks on the table instantly. For yakitori, 'shio' gives a clean salted taste, while 'tare' is a rich caramelized sweet soy sauce.",
                "duration_est": 20.0,
                "jlpt": "N4 Breakdown",
                "ref_sentence": "とりあえず生ビール二つお願いします！焼き鳥は塩とタレ、どちらがおすすめですか？",
                "vocab": [
                    {"orig": "とりあえず", "kana": "とりあえず", "romaji": "toriaezu", "pos": "Adv (N4)", "meaning": "To begin with / For now"},
                    {"orig": "生ビール", "kana": "なまびーる", "romaji": "nama biiru", "pos": "Noun (N5)", "meaning": "Draft beer on tap"},
                    {"orig": "二つ", "kana": "ふたつ", "romaji": "futatsu", "pos": "Counter (N5)", "meaning": "Two items"},
                    {"orig": "焼き鳥", "kana": "やきとり", "romaji": "yakitori", "pos": "Noun (N5)", "meaning": "Grilled chicken skewers"},
                    {"orig": "おすすめ", "kana": "おすすめ", "romaji": "osusume", "pos": "Noun (N4)", "meaning": "Recommendation"}
                ],
                "grammar_title": "Toriaezu Formula & Comparative Recommendation",
                "grammar_bullets": [
                    ("• The Izakaya Golden Opener", "とりあえず生 (Toriaezu nama) = 'Draft beer to start!' ensures instant table delivery"),
                    ("• Salt vs Tare Sauce", "塩 (Shio = Savory salt) highlights ingredient quality; タレ (Tare = Sweet soy glaze)"),
                    ("• Two-Choice Question", "AとB、どちらが〜ですか？ (Between A and B, which one is ~?)")
                ]
            },
            {
                "seg_id": "3_2_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "すみません、お会計をお願いします。別々に払えますか？",
                "furi": "すみません、 おかいけい を おねがいします。 べつべつ に はらえます か？",
                "romaji": "Sumimasen, okaikei o onegaishimasu. Betsubetsu ni haraemasu ka?",
                "meaning": "Excuse me, could we get the check? Can we pay separately?",
                "jlpt": "JLPT N5-N4",
                "grammar": "お会計 (The bill) + 別々に (Separately) + 払えますか (Potential form: Can pay)",
                "tokens": [
                    {"orig": "すみません", "kana": "すみません", "romaji": "sumimasen"},
                    {"orig": "お会計を", "kana": "おかいけいを", "romaji": "okaikei o"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu"},
                    {"orig": "別々に", "kana": "べつべつに", "romaji": "betsubetsu ni"},
                    {"orig": "払えますか", "kana": "はらえますか", "romaji": "haraemasu ka"}
                ],
                "vocab": [
                    {"orig": "お会計", "kana": "おかいけい", "romaji": "okaikei", "pos": "Noun (N5)", "meaning": "Bill / Check settlement"},
                    {"orig": "別々", "kana": "べつべつ", "romaji": "betsubetsu", "pos": "Noun/Adv (N4)", "meaning": "Separately / Individually"},
                    {"orig": "払う", "kana": "はらう", "romaji": "harau", "pos": "Verb (N5)", "meaning": "To pay"},
                    {"orig": "払える", "kana": "はらえる", "romaji": "haraeru", "pos": "Potential Verb (N4)", "meaning": "Can pay / Able to pay"}
                ],
                "grammar_title": "Settling the Bill & Split Payment",
                "grammar_bullets": [
                    ("• Asking for the Bill", "お会計お願いします (Okaikei onegaishimasu) or お勘定 (Okanjou)"),
                    ("• Splitting the Bill", "別々で (Betsubetsu de = Split individual tabs) or 割り勘 (Warikan = Split evenly)"),
                    ("• Potential Verb Form", "払う (harau) -> 払える (haraeru = can pay)")
                ],
                "duration_est": 6.5
            },
            {
                "seg_id": "3_2_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When ready to leave, cross your index fingers in an 'X' gesture or say 'Okaikei onegaishimasu'. If you wish to split the check, use 'betsubetsu ni' for individual item checks, or 'warikan' for splitting the total evenly.",
                "duration_est": 14.5
            },
            {
                "seg_id": "3_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Many visitors are surprised when a small unrequested dish appears at their izakaya table. This is called 'Otoshi' or 'Tsukidashi'—a traditional seating cover charge that comes with an appetizer made fresh daily by the chef. It acts as the table charge and acknowledges your patronage.",
                "duration_est": 17.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "3_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When doing a 'Kanpai' toast with Japanese friends or colleagues, there is a subtle rule of respect: if you are toasting with someone older or senior in rank, tap your glass slightly lower than theirs. Also, never pour your own beer from a bottle; pouring for each other builds harmony and social connection!",
                "duration_est": 18.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "3_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "And here is an important table manner regarding the hot Oshibori towel: it is provided strictly for wiping your hands before eating. In formal or polite dining settings, avoid wiping your face or neck with the towel, as that is considered overly casual.",
                "duration_est": 17.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 4 [THURSDAY]: AKIHABARA POP CULTURE & MAID CAFES (12:45 - 16:30)
    # ----------------------------------------------------
    {
        "chapter_id": 4,
        "chapter_title": "DAY 4 • AKIHABARA ANIME PILGRIMAGE & POP CULTURE",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_akiba_street.jpg",
        "segments": [
            {
                "seg_id": "4_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Day 4 brings us into Electric Town: Akihabara. From towering eight-story manga department stores to retro gaming alleys, navigating Akiba requires specific vocabulary for merchandise, pre-order perks, and tax-free processing.",
                "duration_est": 15.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "4_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "今期の新作アニメの原作はどこにありますか？購入特典はまだ付きますか？",
                "furi": "こんき の しんさく あにめ の げんさく は どこ に あります か？ こうにゅう とくてん は まだ つきます か？",
                "romaji": "Konki no shinsaku anime no gensaku wa doko ni arimasu ka? Kounyuu tokuten wa mada tsukimasu ka?",
                "meaning": "Where are the original manga or novels for this season's new anime? Does it still come with the purchase bonus perk?",
                "jlpt": "JLPT N4-N3",
                "grammar": "今期 (Current season) + 原作 (Original work) + 特典が付く (Include bonus)",
                "tokens": [
                    {"orig": "今期の", "kana": "こんきの", "romaji": "konki no"},
                    {"orig": "新作アニメの", "kana": "しんさくあにめの", "romaji": "shinsaku anime no"},
                    {"orig": "原作は", "kana": "げんさくは", "romaji": "gensaku wa"},
                    {"orig": "どこに", "kana": "どこに", "romaji": "doko ni"},
                    {"orig": "ありますか", "kana": "ありますか", "romaji": "arimasu ka"},
                    {"orig": "購入特典は", "kana": "こうにゅうとくてんは", "romaji": "kounyuu tokuten wa"},
                    {"orig": "まだ", "kana": "まだ", "romaji": "mada"},
                    {"orig": "付きますか", "kana": "つきますか", "romaji": "tsukimasu ka"}
                ],
                "vocab": [
                    {"orig": "今期", "kana": "こんき", "romaji": "konki", "pos": "Noun (N3)", "meaning": "Current broadcasting term/season"},
                    {"orig": "新作", "kana": "しんさく", "romaji": "shinsaku", "pos": "Noun (N4)", "meaning": "New release / New work"},
                    {"orig": "原作", "kana": "げんさく", "romaji": "gensaku", "pos": "Noun (N3)", "meaning": "Original manga / light novel source"},
                    {"orig": "購入特典", "kana": "こうにゅうとくてん", "romaji": "kounyuu tokuten", "pos": "Noun (N3)", "meaning": "Exclusive buyer bonus perk"},
                    {"orig": "付く", "kana": "つく", "romaji": "tsuku", "pos": "Verb (N4)", "meaning": "To come with / Be attached"}
                ],
                "grammar_title": "Anime Merch Hunting & Exclusive Bonus Inquiries",
                "grammar_bullets": [
                    ("• The Core Anime Term 原作", "Manga or light novel upon which an anime is adapted"),
                    ("• Bonus Perk Formula", "特典は付きますか？ (Does the limited bonus still come with it?)"),
                    ("• Still Available", "まだ (Mada = Still / Yet)")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "4_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When shopping for anime merchandise, 'gensaku' is the essential term for the original source manga or light novel. Japanese specialty shops often include exclusive collector postcards or acrylic stands called 'tokuten'. Asking 'Kounyuu tokuten wa mada tsukimasu ka?' confirms if limited bonus items remain in stock.",
                "duration_est": 20.0,
                "jlpt": "N3 Breakdown",
                "ref_sentence": "今期の新作アニメの原作はどこにありますか？購入特典はまだ付きますか？",
                "vocab": [
                    {"orig": "今期", "kana": "こんき", "romaji": "konki", "pos": "Noun (N3)", "meaning": "Current broadcasting term/season"},
                    {"orig": "新作", "kana": "しんさく", "romaji": "shinsaku", "pos": "Noun (N4)", "meaning": "New release / New work"},
                    {"orig": "原作", "kana": "げんさく", "romaji": "gensaku", "pos": "Noun (N3)", "meaning": "Original manga / light novel source"},
                    {"orig": "購入特典", "kana": "こうにゅうとくてん", "romaji": "kounyuu tokuten", "pos": "Noun (N3)", "meaning": "Exclusive buyer bonus perk"},
                    {"orig": "付く", "kana": "つく", "romaji": "tsuku", "pos": "Verb (N4)", "meaning": "To come with / Be attached"}
                ],
                "grammar_title": "Anime Merch Hunting & Exclusive Bonus Inquiries",
                "grammar_bullets": [
                    ("• The Core Anime Term 原作", "Manga or light novel upon which an anime is adapted"),
                    ("• Bonus Perk Formula", "特典は付きますか？ (Does the limited bonus still come with it?)"),
                    ("• Still Available", "まだ (Mada = Still / Yet)")
                ]
            },
            {
                "seg_id": "4_2_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "パスポートを提示すれば、免税手続きは可能ですか？",
                "furi": "ぱすぽーと を ていじ すれば、 めんぜい てつづき は かのう です か？",
                "romaji": "Pasupooto o teiji sureba, menzei tetsuzuki wa kanou desu ka?",
                "meaning": "If I present my passport, is tax-free processing possible?",
                "jlpt": "JLPT N4-N3",
                "grammar": "~ば条件形 (Hypothetical conditional) + 免税手続き (Tax-free procedure)",
                "tokens": [
                    {"orig": "パスポートを", "kana": "ぱすぽーとを", "romaji": "pasupooto o"},
                    {"orig": "提示すれば", "kana": "ていじすれば", "romaji": "teiji sureba"},
                    {"orig": "免税手続きは", "kana": "めんぜいてつづきは", "romaji": "menzei tetsuzuki wa"},
                    {"orig": "可能ですか", "kana": "かのうですか", "romaji": "kanou desu ka"}
                ],
                "vocab": [
                    {"orig": "パスポート", "kana": "ぱすぽーと", "romaji": "pasupooto", "pos": "Noun (N5)", "meaning": "Passport"},
                    {"orig": "提示", "kana": "ていじ", "romaji": "teiji", "pos": "Noun/Suru (N3)", "meaning": "Presentation / Showing document"},
                    {"orig": "免税", "kana": "めんぜい", "romaji": "menzei", "pos": "Noun (N3)", "meaning": "Tax-free / Tax exemption"},
                    {"orig": "手続き", "kana": "てつづき", "romaji": "tetsuzuki", "pos": "Noun (N3)", "meaning": "Procedure / Formal process"},
                    {"orig": "可能", "kana": "かのう", "romaji": "kanou", "pos": "Na-Adj (N3)", "meaning": "Possible / Feasible"}
                ],
                "grammar_title": "~ば Conditional & Tax-Free Processing",
                "grammar_bullets": [
                    ("• Conditional ~ば", "Verb e-row + ば (提示する -> 提示すれば = If I present)"),
                    ("• Tax-Free Minimum", "Requires purchases exceeding 5,000 yen (excluding tax) on the same day"),
                    ("• Essential Document", "Must present physical passport with temporary visitor entry landing sticker")
                ],
                "duration_est": 5.5
            },
            {
                "seg_id": "4_2_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "For foreign visitors spending over five thousand yen on general goods or consumables, you save Japan's ten percent consumption tax. Remember to carry your physical passport with the immigration landing stamp, as digital photos on smartphones are not accepted for tax-free processing.",
                "duration_est": 16.5
            },
            {
                "seg_id": "4_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "In Akihabara, you will see walls of hundreds of 'Gachapon' capsule toy machines. These machines dispense highly detailed miniature collectibles ranging from famous anime figurines to tiny realistic Japanese food replicas. The golden rule: have plenty of hundred-yen coins ready, and please return empty plastic capsules into the recycling baskets beside the machines.",
                "duration_est": 22.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "4_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "If you visit an Akiba Maid Cafe, you will be welcomed with 'Okaerinasaimase, goshujinsama!' (Welcome home, Master!). Before eating, the maid will lead you in chanting a cute food-blessing spell: 'Oishiku naare, Moe Moe Kyun!'. Remember the etiquette: taking photos of the maids or touching them is strictly forbidden.",
                "duration_est": 23.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "4_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Another unique cultural phenomenon is 'Seichi Junrei'—anime pilgrimage. Anime fans travel across Tokyo to visit the exact real-world stairs, intersections, and shrines depicted in famous series like Your Name and Jujutsu Kaisen. Always respect local residents by taking quiet photos without blocking pathways.",
                "duration_est": 20.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 5 [FRIDAY]: RAMEN VENDING TICKET MACHINE & NOODLE SLURPING (16:30 - 20:15)
    # ----------------------------------------------------
    {
        "chapter_id": 5,
        "chapter_title": "DAY 5 • RAMEN TICKET MACHINE CUSTOMIZATION & DINING ETIQUETTE",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_ramen_counter.jpg",
        "segments": [
            {
                "seg_id": "5_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Day 5 brings us to Tokyo's supreme culinary obsession: Ramen. Most ramen shops in Japan do not take verbal orders at the counter; instead, you purchase a meal ticket from a vending machine called a 'Shokkenki' before sitting down.",
                "duration_est": 16.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "5_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "食券をお買い求めください。麺の硬さはカタメで、味は濃いめでお願いします！",
                "furi": "しょっけん を おかいもとめ ください。 めん の かたさ は かため で、 あじ は こいめ で おねがいします！",
                "romaji": "Shokken o okaimotome kudasai. Men no katasa wa katame de, aji wa koime de onegaishimasu!",
                "meaning": "Please purchase a food ticket. I would like firm noodles and rich, bold broth seasoning, please!",
                "jlpt": "JLPT N4-N3",
                "grammar": "お買い求めください (Polite purchase) + [Customization] + でお願いします",
                "tokens": [
                    {"orig": "食券を", "kana": "しょっけんを", "romaji": "shokken o"},
                    {"orig": "お買い求めください", "kana": "おかいもとめください", "romaji": "okaimotome kudasai"},
                    {"orig": "麺の硬さは", "kana": "めんのかたさは", "romaji": "men no katasa wa"},
                    {"orig": "カタメで", "kana": "かためで", "romaji": "katame de"},
                    {"orig": "味は", "kana": "あじは", "romaji": "aji wa"},
                    {"orig": "濃いめで", "kana": "こいめで", "romaji": "koime de"},
                    {"orig": "お願いします", "kana": "おねがいします", "romaji": "onegaishimasu"}
                ],
                "vocab": [
                    {"orig": "食券", "kana": "しょっけん", "romaji": "shokken", "pos": "Noun (N4)", "meaning": "Meal coupon / Food ticket"},
                    {"orig": "硬さ", "kana": "かたさ", "romaji": "katasa", "pos": "Noun (N3)", "meaning": "Firmness / Hardness"},
                    {"orig": "カタメ", "kana": "かため", "romaji": "katame", "pos": "Noun (N4)", "meaning": "Firm / Al dente noodle texture"},
                    {"orig": "濃いめ", "kana": "こいめ", "romaji": "koime", "pos": "Noun (N4)", "meaning": "Stronger / Richer broth flavor"}
                ],
                "grammar_title": "Ramen Customization: Firmness & Broth Richness",
                "grammar_bullets": [
                    ("• Noodle Firmness Options", "バリ柔 (Bari-yawa) -> 普通 (Futsuu) -> カタメ (Katame) -> バリカタ (Bari-kata = Extra firm)"),
                    ("• Broth Flavor Adjustments", "薄め (Usume = Light) vs 普通 (Futsuu) vs 濃いめ (Koime = Rich & Bold)"),
                    ("• Oil & Fat Levels", "あっさり (Assari = Light oil) vs こってり (Kotteri = Rich oil/backfat)")
                ],
                "duration_est": 8.5
            },
            {
                "seg_id": "5_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When you hand your ticket to the chef, they will ask for your preferences. 'Katame' means firm noodles with great chew, while 'Futsuu' is standard. If you love deep savory flavors, say 'Koime' for richer seasoning and 'Kotteri' for extra aromatic pork fat.",
                "duration_est": 18.5,
                "jlpt": "N4 Breakdown",
                "ref_sentence": "食券をお買い求めください。麺の硬さはカタメで、味は濃いめでお願いします！",
                "vocab": [
                    {"orig": "食券", "kana": "しょっけん", "romaji": "shokken", "pos": "Noun (N4)", "meaning": "Meal coupon / Food ticket"},
                    {"orig": "硬さ", "kana": "かたさ", "romaji": "katasa", "pos": "Noun (N3)", "meaning": "Firmness / Hardness"},
                    {"orig": "カタメ", "kana": "かため", "romaji": "katame", "pos": "Noun (N4)", "meaning": "Firm / Al dente noodle texture"},
                    {"orig": "濃いめ", "kana": "こいめ", "romaji": "koime", "pos": "Noun (N4)", "meaning": "Stronger / Richer broth flavor"}
                ],
                "grammar_title": "Ramen Customization: Firmness & Broth Richness",
                "grammar_bullets": [
                    ("• Noodle Firmness Options", "バリ柔 (Bari-yawa) -> 普通 (Futsuu) -> カタメ (Katame) -> バリカタ (Bari-kata = Extra firm)"),
                    ("• Broth Flavor Adjustments", "薄め (Usume = Light) vs 普通 (Futsuu) vs 濃いめ (Koime = Rich & Bold)"),
                    ("• Oil & Fat Levels", "あっさり (Assari = Light oil) vs こってり (Kotteri = Rich oil/backfat)")
                ]
            },
            {
                "seg_id": "5_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Why do Japanese people loudly slurp their ramen? In Japanese dining culture, slurping noodles together with air cools down the boiling hot broth while enhancing the aroma of the soup in your nasal passage. It is not considered rude; rather, it signals to the ramen master that you are thoroughly enjoying your meal!",
                "duration_est": 23.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "5_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "At tonkotsu ramen shops like Ichiran or Ippudo, when you finish your noodles but still have soup left in your bowl, you can order an extra noodle refill called 'Kaedama'! Simply say 'Kaedama katame de onegaishimasu' and hand one or two hundred yen to the chef.",
                "duration_est": 21.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "5_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When you finish eating at a ramen counter, do the master a courtesy: wipe down your counter space with the cloth provided, place your empty bowl onto the raised upper ledge, and say 'Gochisousama deshita!' on your way out.",
                "duration_est": 18.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 6 [SATURDAY]: SENTO & ONSEN BATHHOUSE ETIQUETTE (20:15 - 24:00)
    # ----------------------------------------------------
    {
        "chapter_id": 6,
        "chapter_title": "DAY 6 • SENTO BATHS & ONSEN 5 GOLDEN RULES",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_onsen_sento.jpg",
        "segments": [
            {
                "seg_id": "6_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Weekend relaxation in Japan revolves around thermal water: soaking in a neighborhood sento public bathhouse or visiting a natural volcanic onsen hot spring resort. But before stepping into the steaming bath, you must know the 5 Golden Rules of Japanese Bathing.",
                "duration_est": 18.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "6_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "湯船に入る前に、体をきれいに洗ってください。タオルは湯船に入れないでくださいね。",
                "furi": "ゆぶね に はいる まえ に、 からだ を きれい に あらって ください。 たおる は ゆぶね に いれないで ください ね。",
                "romaji": "Yubune ni hairu mae ni, karada o kirei ni aratte kudasai. Taoru wa yubune ni irenaide kudasai ne.",
                "meaning": "Before entering the bathtub, please wash your body thoroughly. Please do not put your towel into the bathwater.",
                "jlpt": "JLPT N4-N3",
                "grammar": "Verb辞書形 + 前に (Before doing) + ~ないでください (Negative polite request)",
                "tokens": [
                    {"orig": "湯船に", "kana": "ゆぶねに", "romaji": "yubune ni"},
                    {"orig": "入る前に", "kana": "はいるまえに", "romaji": "hairu mae ni"},
                    {"orig": "体を", "kana": "からだを", "romaji": "karada o"},
                    {"orig": "きれいに", "kana": "きれいに", "romaji": "kirei ni"},
                    {"orig": "洗って", "kana": "あらって", "romaji": "aratte"},
                    {"orig": "ください", "kana": "ください", "romaji": "kudasai"},
                    {"orig": "タオルは", "kana": "たおるは", "romaji": "taoru wa"},
                    {"orig": "湯船に", "kana": "ゆぶねに", "romaji": "yubune ni"},
                    {"orig": "入れないで", "kana": "いれないで", "romaji": "irenaide"},
                    {"orig": "くださいね", "kana": "くださいね", "romaji": "kudasai ne"}
                ],
                "vocab": [
                    {"orig": "湯船", "kana": "ゆぶね", "romaji": "yubune", "pos": "Noun (N3)", "meaning": "Bathtub / Communal soaking tub"},
                    {"orig": "洗う", "kana": "あらう", "romaji": "arau", "pos": "Verb (N5)", "meaning": "To wash / Cleanse"},
                    {"orig": "入れる", "kana": "いれる", "romaji": "ireru", "pos": "Verb (N5)", "meaning": "To put in / Submerge"},
                    {"orig": "きれいに", "kana": "きれいに", "romaji": "kirei ni", "pos": "Adv (N5)", "meaning": "Cleanly / Thoroughly"}
                ],
                "grammar_title": "Before Action (〜前に) & Negative Request (〜ないでください)",
                "grammar_bullets": [
                    ("• Timing Formula", "Verb Dictionary Form + 前に (入る前に = Before entering)"),
                    ("• Negative Request Pattern", "Verb ない-form + でください (入れないでください = Please do not put in)"),
                    ("• Communal Bathing Principle", "The tub is solely for peaceful soaking; all soap and scrubbing occur at wash stalls")
                ],
                "duration_est": 8.5
            },
            {
                "seg_id": "6_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Notice the two fundamental grammar rules here: 'hairu mae ni' means 'before entering', where a dictionary verb pairs with 'mae ni'. And 'irenaide kudasai' is the polite negative command formed by taking the negative 'nai' stem plus 'de kudasai'.",
                "duration_est": 18.0,
                "jlpt": "N4 Breakdown",
                "ref_sentence": "湯船に入る前に、体をきれいに洗ってください。タオルは湯船に入れないでくださいね。",
                "vocab": [
                    {"orig": "湯船", "kana": "ゆぶね", "romaji": "yubune", "pos": "Noun (N3)", "meaning": "Bathtub / Communal soaking tub"},
                    {"orig": "洗う", "kana": "あらう", "romaji": "arau", "pos": "Verb (N5)", "meaning": "To wash / Cleanse"},
                    {"orig": "入れる", "kana": "いれる", "romaji": "ireru", "pos": "Verb (N5)", "meaning": "To put in / Submerge"},
                    {"orig": "きれいに", "kana": "きれいに", "romaji": "kirei ni", "pos": "Adv (N5)", "meaning": "Cleanly / Thoroughly"}
                ],
                "grammar_title": "Before Action (〜前に) & Negative Request (〜ないでください)",
                "grammar_bullets": [
                    ("• Timing Formula", "Verb Dictionary Form + 前に (入る前に = Before entering)"),
                    ("• Negative Request Pattern", "Verb ない-form + でください (入れないでください = Please do not put in)"),
                    ("• Communal Bathing Principle", "The tub is solely for peaceful soaking; all soap and scrubbing occur at wash stalls")
                ]
            },
            {
                "seg_id": "6_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Let us review the 5 Golden Rules of Japanese Bathing. Rule 1: Wash thoroughly at the shower stalls before soaking. Rule 2: Never submerge your towel into the bath; fold it and place it on your head! Rule 3: Tie long hair up so it never touches the mineral water. Rule 4: No swimming or splashing. And Rule 5: Wipe off with your towel before stepping back into the dressing room.",
                "duration_est": 26.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "6_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "And after your relaxing bath, follow the timeless Showa tradition: buy a glass bottle of ice-cold Coffee Milk or Meiji Milk from the lobby vending machine, stand with one hand on your hip, and drink it down in one satisfying gulp. That is the true Japanese onsen experience!",
                "duration_est": 20.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "6_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When staying at a traditional Ryokan onsen inn, you will wear a cotton robe called a Yukata. Remember the vital rule of wearing a Yukata: always wrap the LEFT side over the RIGHT side. Wrapping right over left is reserved exclusively for traditional funerals, so remember 'Left on Top for Living'!",
                "duration_est": 23.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # MODULE 7 [SUNDAY]: SHRINES, TEMPLES, BOWING & OMOTENASHI (24:00 - 27:00)
    # ----------------------------------------------------
    {
        "chapter_id": 7,
        "chapter_title": "DAY 7 • SHRINES, TEMPLES, BOWING ANGLES & OMOTENASHI",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_shrine_asakusa.jpg",
        "segments": [
            {
                "seg_id": "7_1_intro",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Sunday brings us to Tokyo's historic spiritual landmarks, from Asakusa Sensoji Temple to Meiji Jingu Shrine. Understanding the ritual etiquette of shrine purification, prayer claps, and bowing angles reveals the soul of Japanese culture.",
                "duration_est": 16.0,
                "jlpt": "N/A"
            },
            {
                "seg_id": "7_1_dialogue",
                "type": "dialogue",
                "character": "Nanami",
                "lang": "ja",
                "voice": "ja-JP-NanamiNeural",
                "content": "ごちそうさまでした。とても美味しかったです。おもてなしをありがとうございました。",
                "furi": "ごちそうさまでした。 とても おいしかった です。 おもてなし を ありがとうございました。",
                "romaji": "Gochisousama deshita. Totemo oishikatta desu. Omotenashi o arigatou gozaimashita.",
                "meaning": "Thank you for the wonderful meal. It was truly delicious. Thank you for your gracious hospitality.",
                "jlpt": "JLPT N5",
                "grammar": "ごちそうさまでした (Post-meal gratitude) + おもてなし (Japanese hospitality)",
                "tokens": [
                    {"orig": "ごちそうさまでした", "kana": "ごちそうさまでした", "romaji": "gochisousama deshita"},
                    {"orig": "とても", "kana": "とても", "romaji": "totemo"},
                    {"orig": "美味しかったです", "kana": "おいしかったです", "romaji": "oishikatta desu"},
                    {"orig": "おもてなしを", "kana": "おもてなしを", "romaji": "omotenashi o"},
                    {"orig": "ありがとうございました", "kana": "ありがとうございました", "romaji": "arigatou gozaimashita"}
                ],
                "vocab": [
                    {"orig": "ごちそうさまでした", "kana": "ごちそうさまでした", "romaji": "gochisousama deshita", "pos": "Exp (N5)", "meaning": "Post-meal appreciation formula"},
                    {"orig": "とても", "kana": "とても", "romaji": "totemo", "pos": "Adv (N5)", "meaning": "Very / Truly"},
                    {"orig": "美味しい", "kana": "おいしい", "romaji": "oishii", "pos": "I-Adj (N5)", "meaning": "Delicious / Tasty"},
                    {"orig": "おもてなし", "kana": "おもてなし", "romaji": "omotenashi", "pos": "Noun (N3)", "meaning": "Selfless Japanese hospitality"}
                ],
                "grammar_title": "Dining Gratitude & Expressing Appreciation",
                "grammar_bullets": [
                    ("• Post-Meal Etiquette", "Always say ごちそうさまでした (Gochisousama deshita) when leaving any dining counter"),
                    ("• Past Tense of I-Adjectives", "美味しい (Oishii) -> 美味しかった (Oishikatta = It was delicious)"),
                    ("• The Spirit of Omotenashi", "Anticipating guests' needs before they even ask")
                ],
                "duration_est": 8.0
            },
            {
                "seg_id": "7_1_breakdown",
                "type": "breakdown",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Whenever you finish dining in Japan, say 'Gochisousama deshita' to the chef or staff as you leave. It literally means 'it was a feast' and acknowledges the effort behind preparing your meal. Notice the past tense of the adjective: 'oishii' becomes 'oishikatta desu'.",
                "duration_est": 18.0,
                "jlpt": "N5 Breakdown",
                "ref_sentence": "ごちそうさまでした。とても美味しかったです。おもてなしをありがとうございました。",
                "vocab": [
                    {"orig": "ごちそうさまでした", "kana": "ごちそうさまでした", "romaji": "gochisousama deshita", "pos": "Exp (N5)", "meaning": "Post-meal appreciation formula"},
                    {"orig": "とても", "kana": "とても", "romaji": "totemo", "pos": "Adv (N5)", "meaning": "Very / Truly"},
                    {"orig": "美味しい", "kana": "おいしい", "romaji": "oishii", "pos": "I-Adj (N5)", "meaning": "Delicious / Tasty"},
                    {"orig": "おもてなし", "kana": "おもてなし", "romaji": "omotenashi", "pos": "Noun (N3)", "meaning": "Selfless Japanese hospitality"}
                ],
                "grammar_title": "Dining Gratitude & Expressing Appreciation",
                "grammar_bullets": [
                    ("• Post-Meal Etiquette", "Always say ごちそうさまでした (Gochisousama deshita) when leaving any dining counter"),
                    ("• Past Tense of I-Adjectives", "美味しい (Oishii) -> 美味しかった (Oishikatta = It was delicious)"),
                    ("• The Spirit of Omotenashi", "Anticipating guests' needs before they even ask")
                ]
            },
            {
                "seg_id": "7_cultural_deep_dive_1",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "When entering a Shinto shrine, bow lightly before passing through the red Torii gate, and walk along the outer edges of the path—as the center path is reserved for the deities. At the water pavilion (Temizuya), rinse your left hand, right hand, and mouth using the wooden ladle.",
                "duration_est": 21.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "7_cultural_deep_dive_2",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "For shrine prayer, follow the ancient rule of 'Ni-rei, Ni-hai, Ichi-rei': Toss a 5-yen coin into the offering box, bow deeply twice at ninety degrees, clap your hands twice firmly, pray quietly in your heart, and finish with one final deep bow. Note that at Buddhist temples, you bow with palms pressed silently together without clapping!",
                "duration_est": 25.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "7_cultural_deep_dive_3",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Let us master the 3 Bowing Angles of Japan. Angle 1: Eshaku (fifteen degrees) is a casual greeting used when passing colleagues or neighbors. Angle 2: Keirei (thirty degrees) is the standard business bow used when greeting clients or entering shops. And Angle 3: Saikeirei (forty-five degrees) expresses profound gratitude or deep apologies. Keep your back straight and bend smoothly from the hips!",
                "duration_est": 25.0,
                "jlpt": "Culture"
            },
            {
                "seg_id": "7_cultural_deep_dive_4",
                "type": "cultural_insight",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Finally, remember the No-Tipping Rule. In Japan, exceptional service is seen as standard pride in one's profession, and tipping is not practiced. If you leave extra cash on a table, the server will often run down the street to return the money you accidentally left behind. Instead, a warm smile and a polite 'Arigatou gozaimashita' is the highest praise you can give.",
                "duration_est": 24.0,
                "jlpt": "Culture"
            }
        ]
    },

    # ----------------------------------------------------
    # EPILOGUE: FULL REVIEW & TOKYOFLOW OUTRO (27:00 - 28:15)
    # ----------------------------------------------------
    {
        "chapter_id": 8,
        "chapter_title": "EPILOGUE • 40+ KEY PHRASE RECAP & TOKYOFLOW ACADEMY",
        "bg_scene": "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg",
        "segments": [
            {
                "seg_id": "8_1_recap",
                "type": "narration",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "Congratulations on completing this 28-minute TokyoFlow Japanese Masterclass! You have mastered over forty essential JLPT N5 to N3 phrases, seven real-world Tokyo life survival scenarios, and the cultural rules of trains, kombini, izakayas, anime shopping, ramen customization, onsen bathing, shrine worship, and Japanese etiquette.",
                "duration_est": 22.0,
                "jlpt": "Recap"
            },
            {
                "seg_id": "8_2_app_cta",
                "type": "app_outro",
                "character": "Andrew",
                "lang": "en",
                "voice": "en-US-AndrewNeural",
                "content": "To practice interactive shadowing with real-time AI pitch accent scoring and explore over fourteen thousand native audio recordings across ten thousand JLPT vocabulary words, download TokyoFlow - Japanese Speaking on the iOS App Store today. Subscribe for new episodes every day, and we will see you in Tokyo. Mata ne!",
                "duration_est": 22.0,
                "jlpt": "App Showcase"
            }
        ]
    }
]

# ==========================================
# AUDIO SYNTHESIS & TIMING ENGINE
# ==========================================

async def synthesize_segment_audio(text: str, voice: str, out_mp3: str):
    """Synthesizes high-definition audio using edge_tts with speed/pitch adjustments."""
    if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
        return
    
    if "Nanami" in voice:
        rate = "-10%"
        pitch = "+2Hz"
    else:
        rate = "+2%"
        pitch = "+0Hz"

    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(out_mp3)

def get_audio_duration(file_path: str) -> float:
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        out = subprocess.check_output(cmd).decode().strip()
        return float(out)
    except Exception:
        return 5.0

async def synthesize_all_audio_tracks(output_dir: str):
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    print("\n--- SYNTHESIZING DUAL-VOICE AUDIO TRACKS ---")
    
    total_audio_sec = 0.0
    for ch in MEGA_SCREENPLAY:
        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            out_mp3 = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            await synthesize_segment_audio(seg["content"], seg["voice"], out_mp3)
            dur = get_audio_duration(out_mp3)
            seg["actual_duration"] = dur
            total_audio_sec += dur
            print(f"  [OK] Seg {seg_id} ({seg['character']}): {dur:.1f}s")
            
            # Generate word tokens timing approximation if JA dialogue
            if seg.get("lang") == "ja" and seg.get("tokens"):
                toks = seg["tokens"]
                n_toks = len(toks)
                time_per_tok = dur / max(1, n_toks)
                for idx, tok in enumerate(toks):
                    tok["start"] = idx * time_per_tok
                    tok["end"] = (idx + 1) * time_per_tok

    print(f"\nTotal Synthesized Master Audio: {total_audio_sec:.1f}s ({total_audio_sec/60.0:.2f} mins)")
    return total_audio_sec

# ==========================================
# FRAME & SLIDE DESIGNER (100% CONTRAST & SAFETY)
# ==========================================

def draw_top_brand_bar(draw: ImageDraw.Draw, width: int, chapter_title: str, ep_label: str):
    draw.rectangle([(0, 0), (width, 75)], fill=(15, 23, 42))
    font_brand = get_font(26)
    draw.text((60, 22), "TokyoFlow Japanese  |  Real-Life Tokyo Japanese Academy", fill=(255, 255, 255), font=font_brand)
    
    font_badge = get_font(22)
    badge_str = f"{ep_label} • {chapter_title}"
    bbox = draw.textbbox((0, 0), badge_str, font=font_badge)
    badge_w = bbox[2] - bbox[0]
    draw.text((width - badge_w - 60, 24), badge_str, fill=(244, 114, 182), font=font_badge)

def render_dialogue_karaoke_frame(
    tokens: list,
    category_label: str,
    title_label: str,
    english_meaning: str,
    grammar_text: str,
    current_time: float,
    total_duration: float,
    jlpt_level: str
) -> Image.Image:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # 1. Top Ribbon
    draw_top_brand_bar(draw, width, category_label, "SUNDAY MEGA-COMPILATION")

    # 2. Category Pill & JLPT Badge (y=105)
    font_cat = get_font(20)
    pill_text = f"  {category_label}  "
    bbox_p = draw.textbbox((0, 0), pill_text, font=font_cat)
    pw = bbox_p[2] - bbox_p[0] + 30
    draw.rounded_rectangle([(100, 105), (100 + pw, 150)], radius=12, fill=(238, 242, 255), outline=(199, 210, 254), width=2)
    draw.text((115, 116), pill_text, fill=(79, 70, 229), font=font_cat)

    jlpt_str = f" [ {jlpt_level} ] "
    bbox_j = draw.textbbox((0, 0), jlpt_str, font=font_cat)
    jw = bbox_j[2] - bbox_j[0] + 30
    draw.rounded_rectangle([(width - 100 - jw, 105), (width - 100, 150)], radius=12, fill=(254, 242, 242), outline=(254, 202, 202), width=2)
    draw.text((width - 100 - jw + 15, 116), jlpt_str, fill=(225, 29, 72), font=font_cat)

    draw.text((100, 170), title_label, fill=(15, 23, 42), font=get_font(34))

    # 3. Main 3-Tier Dialogue Card (y=230..680)
    card_x, card_y, card_w, card_h = 100, 230, width - 200, 450
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)

    font_jp = get_font(48)
    font_kana = get_font(24)
    font_romaji = get_font(26)

    token_widths = []
    for tok in tokens:
        w_jp = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        w_kana = draw.textbbox((0, 0), tok.get("kana", ""), font=font_kana)[2] if tok.get("kana") else 0
        w_ro = draw.textbbox((0, 0), tok.get("romaji", ""), font=font_romaji)[2] if tok.get("romaji") else 0
        w = max(w_jp, w_kana, w_ro) + 24
        token_widths.append(w)

    total_tokens_w = sum(token_widths)
    start_x = card_x + max(40, (card_w - total_tokens_w) // 2)
    curr_x = start_x

    y_kana = card_y + 40
    y_jp = card_y + 90
    y_romaji = card_y + 180

    for i, tok in enumerate(tokens):
        w = token_widths[i]
        start_t = tok.get("start", 0.0)
        end_t = tok.get("end", 0.0)
        
        is_active = (start_t <= current_time <= end_t) and (end_t > start_t)
        
        if is_active:
            draw.rounded_rectangle([(curr_x + 2, y_kana - 10), (curr_x + w - 2, y_romaji + 45)], radius=16, fill=(254, 240, 138), outline=(245, 158, 11), width=3)
            dot_cx = curr_x + w // 2
            draw.ellipse([(dot_cx - 6, y_kana - 24), (dot_cx + 6, y_kana - 12)], fill=(220, 38, 38))
            color_kana = (180, 83, 9)
            color_jp = (15, 23, 42)
            color_romaji = (180, 83, 9)
        else:
            color_kana = (100, 116, 139)
            color_jp = (15, 23, 42)
            color_romaji = (71, 85, 105)

        if tok.get("kana"):
            kw = draw.textbbox((0, 0), tok["kana"], font=font_kana)[2]
            draw.text((curr_x + (w - kw) // 2, y_kana), tok["kana"], fill=color_kana, font=font_kana)

        jw = draw.textbbox((0, 0), tok["orig"], font=font_jp)[2]
        draw.text((curr_x + (w - jw) // 2, y_jp), tok["orig"], fill=color_jp, font=font_jp)

        if tok.get("romaji"):
            rw = draw.textbbox((0, 0), tok["romaji"], font=font_romaji)[2]
            draw.text((curr_x + (w - rw) // 2, y_romaji), tok["romaji"], fill=color_romaji, font=font_romaji)

        curr_x += w

    draw.line([(card_x + 40, card_y + 280), (card_x + card_w - 40, card_y + 280)], fill=(241, 245, 249), width=2)

    font_meaning = get_font(30)
    meaning_str = f"Meaning: \"{english_meaning}\""
    draw.text((card_x + 50, card_y + 310), meaning_str, fill=(30, 41, 59), font=font_meaning)

    if grammar_text:
        font_g = get_font(22)
        g_str = f"  Grammar: {grammar_text}  "
        bbox_g = draw.textbbox((0, 0), g_str, font=font_g)
        gw = bbox_g[2] - bbox_g[0] + 20
        draw.rounded_rectangle([(card_x + 50, card_y + 375), (card_x + 50 + gw, card_y + 418)], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=2)
        draw.text((card_x + 60, card_y + 386), g_str, fill=(5, 150, 105), font=font_g)

    # 4. Bottom Shadowing Drill Bar (y=710..980)
    drill_y = 710
    draw.rounded_rectangle([(card_x, drill_y), (card_x + card_w, drill_y + 240)], radius=20, fill=(241, 245, 249), outline=(226, 232, 240), width=2)
    draw.text((card_x + 40, drill_y + 25), "SHADOWING PRACTICE • REPEAT ALOUD WITH NATIVE TOKYO ACCENT", fill=(71, 85, 105), font=get_font(22))
    
    draw.rounded_rectangle([(card_x + 40, drill_y + 70), (card_x + card_w - 40, drill_y + 210)], radius=16, fill=(15, 23, 42))
    draw.text((card_x + 80, drill_y + 105), "[ NATIVE TOKYO AUDIO ] Nanami @ -10% Tempo", fill=(254, 240, 138), font=get_font(26))
    draw.text((card_x + 80, drill_y + 155), "Focus on pitch accent and natural mora rhythm", fill=(148, 163, 184), font=get_font(22))

    progress = min(1.0, current_time / max(0.1, total_duration))
    draw.rectangle([(0, height - 12), (int(width * progress), height)], fill=(225, 29, 72))

    return img

def render_breakdown_frame(
    ref_sentence: str,
    vocab_list: list,
    grammar_title: str,
    grammar_bullets: list,
    current_time: float,
    total_duration: float,
    chapter_title: str,
    jlpt_level: str
) -> Image.Image:
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(248, 250, 252))
    draw = ImageDraw.Draw(img)

    # 1. Top Ribbon
    draw_top_brand_bar(draw, width, chapter_title, "SUNDAY MEGA-COMPILATION")

    # 2. Header & Japanese Target Sentence Banner (y=95..180)
    card_x, card_w = 100, width - 200
    draw.rounded_rectangle([(card_x, 95), (card_x + card_w, 180)], radius=16, fill=(15, 23, 42))
    draw.text((card_x + 30, 108), f"[ BILINGUAL BREAKDOWN ] {jlpt_level}", fill=(244, 114, 182), font=get_font(20))
    draw.text((card_x + 30, 136), ref_sentence, fill=(255, 255, 255), font=get_font(28))

    # 3. Top Half: 4 Vocabulary Grid Cards (y=200..490)
    grid_y = 200
    n_cards = min(4, len(vocab_list)) if vocab_list else 1
    cw = (card_w - (n_cards - 1) * 20) // max(1, n_cards)
    ch_h = 280

    for i in range(n_cards):
        v = vocab_list[i] if i < len(vocab_list) else {}
        cx = card_x + i * (cw + 20)
        draw.rounded_rectangle([(cx, grid_y), (cx + cw, grid_y + ch_h)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

        pos_str = f" {v.get('pos', 'Vocab')} "
        draw.rounded_rectangle([(cx + 20, grid_y + 18), (cx + cw - 20, grid_y + 54)], radius=8, fill=(238, 242, 255))
        draw.text((cx + 30, grid_y + 24), pos_str, fill=(79, 70, 229), font=get_font(18))

        draw.text((cx + 25, grid_y + 70), v.get("orig", ""), fill=(15, 23, 42), font=get_font(32))
        draw.text((cx + 25, grid_y + 125), f"{v.get('kana', '')} ({v.get('romaji', '')})", fill=(100, 116, 139), font=get_font(20))

        draw.line([(cx + 20, grid_y + 175), (cx + cw - 20, grid_y + 175)], fill=(241, 245, 249), width=2)
        draw.text((cx + 25, grid_y + 195), v.get("meaning", ""), fill=(30, 41, 59), font=get_font(22))

    # 4. Bottom Half: Grammar & Nuance Spotlight Box (y=505..960)
    box_y = 505
    box_h = 455
    draw.rounded_rectangle([(card_x, box_y), (card_x + card_w, box_y + box_h)], radius=20, fill=(255, 255, 255), outline=(79, 70, 229), width=3)

    draw.rounded_rectangle([(card_x + 3, box_y + 3), (card_x + card_w - 3, box_y + 65)], radius=18, fill=(238, 242, 255))
    draw.text((card_x + 35, box_y + 18), f"[ SPOTLIGHT ] {grammar_title}", fill=(67, 56, 202), font=get_font(26))

    by = box_y + 90
    for header, detail in grammar_bullets:
        draw.text((card_x + 35, by), header, fill=(225, 29, 72), font=get_font(22))
        draw.text((card_x + 40, by + 32), detail, fill=(30, 41, 59), font=get_font(24))
        by += 90

    draw.rounded_rectangle([(card_x + 20, box_y + box_h - 60), (card_x + card_w - 20, box_y + box_h - 15)], radius=10, fill=(248, 250, 252))
    draw.text((card_x + 40, box_y + box_h - 48), "[ TOKYOFLOW ACADEMY ] Master authentic grammar & pitch accent on the TokyoFlow iOS App", fill=(100, 116, 139), font=get_font(19))

    progress = min(1.0, current_time / max(0.1, total_duration))
    draw.rectangle([(0, height - 12), (int(width * progress), height)], fill=(225, 29, 72))

    return img

def render_story_culture_overlay_frame(
    chapter_num: int,
    chapter_title: str,
    section_label: str,
    narration_text: str,
    bg_image_path: str,
    current_time: float,
    total_duration: float
) -> Image.Image:
    width, height = 1920, 1080
    
    # 1. Authentic 4K Real Photography Base (Clean, zero baked-in text, zero cartoon)
    if os.path.exists(bg_image_path):
        bg = Image.open(bg_image_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    else:
        bg = Image.new("RGB", (width, height), color=(15, 23, 42))

    # 2. Dark contrast overlay ensuring zero background bleed-through
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # Subtle darkening on upper scenery to pop the photo's real colors
    ov_draw.rectangle([(0, 0), (width, 100)], fill=(10, 15, 28, 240))
    
    # Opaque, solid dark navy container card (y=620..1010) with sky cyan border - 100% text isolation
    ov_draw.rounded_rectangle([(80, 620), (width - 80, 1010)], radius=24, fill=(10, 15, 28, 250), outline=(56, 189, 248, 255), width=3)
    
    img = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top Brand Ribbon
    draw_top_brand_bar(draw, width, chapter_title, f"MODULE {chapter_num}")

    # Bottom Subtitle & Culture HUD Content
    hud_x = 120
    draw.text((hud_x, 655), f"[ {chapter_title} ] {section_label}", fill=(244, 114, 182), font=get_font(24))
    
    font_narr = get_font(30)
    words = narration_text.split(" ")
    lines = []
    curr_line = ""
    for w in words:
        test = f"{curr_line} {w}".strip()
        if draw.textbbox((0, 0), test, font=font_narr)[2] < (width - 280):
            curr_line = test
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)

    ny = 715
    for line in lines[:4]:
        draw.text((hud_x, ny), line, fill=(255, 255, 255), font=font_narr)
        ny += 46

    progress = min(1.0, current_time / max(0.1, total_duration))
    draw.rectangle([(0, height - 12), (int(width * progress), height)], fill=(225, 29, 72))

    return img

# ==========================================
# THUMBNAIL ENGINE (16:9 & 9:16)
# ==========================================

def render_master_thumbnail(output_dir: str):
    """Generates 16:9 Golden Master Landscape Thumbnail (1920x1080) conforming to tokyoflow-thumbnail-factory."""
    width, height = 1920, 1080
    bg_path = "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg"
    if not os.path.exists(bg_path):
        bg_path = "docs/youtube_assets/scene_backgrounds/scene_yamanote_platform.jpg"

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
    draw.text((90, 58), "TokyoFlow Japanese", fill=(225, 29, 72), font=get_font(28))

    # 2. Top-Right Crimson Series Badge
    badge_str = "JLPT N5-N3 • MEGA-COMPILATION"
    bbox = draw.textbbox((0, 0), badge_str, font=get_font(24))
    bw = bbox[2] - bbox[0] + 50
    draw.rounded_rectangle([(width - 60 - bw, 45), (width - 60, 105)], radius=18, fill=(225, 29, 72))
    draw.text((width - 60 - bw + 25, 60), badge_str, fill=(255, 255, 255), font=get_font(24))

    # 3. Giant 3D Solar Yellow Hook (96pt Heavy)
    font_hook = get_font(92)
    hook_lines = ["TOKYO SURVIVAL", "5-DAY MASTERCLASS"]
    hy = 145
    for line in hook_lines:
        for ox, oy in [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((60 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((60, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 110

    draw.text((65, 375), "MON-FRI ALL-IN-ONE + DEEP JAPANESE CULTURE & TRAVEL", fill=(244, 114, 182), font=get_font(32))

    # 4. Glassmorphic Japanese Learning Card
    card_y = 435
    card_w = 880
    draw.rounded_rectangle([(60, card_y), (60 + card_w, card_y + 430)], radius=22, fill=(10, 15, 28, 235), outline=(56, 189, 248), width=3)
    draw.text((90, card_y + 25), "[ WEEKEND MEGA MASTERCLASS ]", fill=(56, 189, 248), font=get_font(22))

    font_jp_quote = get_font(36)
    draw.text((90, card_y + 70), "月-金 Tokyo 日常サバイバル &", fill=(255, 255, 255), font=font_jp_quote)
    draw.text((90, card_y + 120), "日本文化・風俗・旅行完全マスター！", fill=(254, 240, 138), font=font_jp_quote)

    draw.text((90, card_y + 190), "• Transit, Kombini, Izakaya, Akiba, Ramen, Sento & Temples", fill=(244, 114, 182), font=get_font(24))
    draw.text((90, card_y + 235), "• 40+ High-Frequency Spoken Formulas with Millisecond Karaoke", fill=(226, 232, 240), font=get_font(23))
    draw.text((90, card_y + 280), "• Manner Mode, Bowing Angles, Zero-Tipping & Omotenashi", fill=(148, 163, 184), font=get_font(21))
    draw.text((90, card_y + 330), "• Dual-Voice Teamwork: 100% Native JA (Nanami) + EN Breakdown", fill=(56, 189, 248), font=get_font(21))
    draw.text((90, card_y + 375), "• Complete 28-Min All-in-One Sunday Immersion", fill=(254, 240, 138), font=get_font(21))

    # 5. Full-Width Crimson Conversion Ribbon
    draw.rounded_rectangle([(60, height - 115), (width - 60, height - 40)], radius=16, fill=(225, 29, 72))
    draw.text((90, height - 93), " 100% NATIVE TOKYO AUDIO  •  40+ SURVIVAL FORMULAS  •  FULL 28-MIN MASTERCLASS", fill=(255, 255, 255), font=get_font(24))

    thumb_out = os.path.join(output_dir, "thumbnail.jpg")
    img.save(thumb_out, quality=95)
    print(f"  [OK] Saved Master 16:9 Thumbnail: {thumb_out}")

def render_shorts_thumbnail(output_dir: str):
    """Generates 9:16 Golden Master Vertical Shorts Cover (1080x1920)."""
    width, height = 1080, 1920
    bg_path = "docs/youtube_assets/scene_backgrounds/scene_yamanote_platform.jpg"
    if not os.path.exists(bg_path):
        bg_path = "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg"

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

    draw.rounded_rectangle([(40, 50), (430, 115)], radius=16, fill=(255, 255, 255))
    draw.text((65, 65), "TokyoFlow Japanese", fill=(225, 29, 72), font=get_font(26))

    draw.rounded_rectangle([(width - 360, 50), (width - 40, 115)], radius=16, fill=(225, 29, 72))
    draw.text((width - 335, 65), "WS.01 • JLPT N5-N3", fill=(255, 255, 255), font=get_font(24))

    font_hook = get_font(72)
    hook_lines = ["TOKYO SURVIVAL", "WEEKEND MEGA-SET!"]
    hy = 155
    for line in hook_lines:
        for ox, oy in [(4, 4), (3, 3), (2, 2), (1, 1)]:
            draw.text((40 + ox, hy + oy), line, fill=(0, 0, 0), font=font_hook)
        draw.text((40, hy), line, fill=(254, 240, 138), font=font_hook)
        hy += 85

    draw.text((45, 335), "MON-FRI ALL-IN-ONE + DEEP JAPANESE CULTURE", fill=(244, 114, 182), font=get_font(26))

    card_y = 1120
    draw.rounded_rectangle([(40, card_y), (width - 40, 1640)], radius=24, fill=(10, 15, 28, 245), outline=(56, 189, 248), width=3)
    draw.text((70, card_y + 25), "[ TOKYO SURVIVAL GYM • WEEKEND EDITION ]", fill=(56, 189, 248), font=get_font(22))
    
    draw.text((70, card_y + 70), "月-金 Tokyo サバイバル & 日本文化", fill=(255, 255, 255), font=get_font(38))
    draw.text((70, card_y + 125), "5-Day All-in-One Masterclass", fill=(254, 240, 138), font=get_font(30))
    
    draw.text((70, card_y + 185), "• Transit • Kombini • Izakaya • Akiba • Ramen", fill=(244, 114, 182), font=get_font(26))
    draw.text((70, card_y + 230), "• Sento & Onsen 5 Bathing Rules Decoded", fill=(226, 232, 240), font=get_font(24))
    draw.text((70, card_y + 275), "• Manner Mode, Bowing Angles & Zero Tipping", fill=(148, 163, 184), font=get_font(22))
    draw.text((70, card_y + 325), "• 100% Native Tokyo Audio (Nanami) + Karaoke HUD", fill=(56, 189, 248), font=get_font(22))

    draw.rounded_rectangle([(40, 1660), (width - 40, 1840)], radius=18, fill=(225, 29, 72))
    draw.text((70, 1690), "WATCH FULL 28-MIN MASTERCLASS (WM.01)", fill=(255, 255, 255), font=get_font(32))
    draw.text((70, 1745), "40+ Formulas • Grammar Rules • Deep Japanese Culture", fill=(254, 240, 138), font=get_font(24))

    short_thumb_out = os.path.join(output_dir, "short_thumbnail.jpg")
    img.save(short_thumb_out, quality=95)
    print(f"  [OK] Saved Master 9:16 Shorts Thumbnail: {short_thumb_out}")

# ==========================================
# MASTER VIDEO RENDERING ENGINE
# ==========================================

def render_full_master_video(output_dir: str):
    """Renders 1080p full master video with smooth segment transitions, karaoke HUD, breakdown cards, and cultural overlays."""
    print("\n--- RENDERING 1080P MASTER VIDEO (1920x1080 @ 30FPS) ---")
    tmp_vid_dir = "tmp/videogen/sunday_mega_wm01"
    os.makedirs(tmp_vid_dir, exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)

    audio_dir = os.path.join(output_dir, "audio")
    segment_mp4s = []
    total_rendered_duration = 0.0
    fps = 30

    for ch in MEGA_SCREENPLAY:
        ch_id = ch["chapter_id"]
        ch_title = ch["chapter_title"]
        bg_scene = ch.get("bg_scene", "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg")

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            out_mp4 = os.path.join(tmp_vid_dir, f"clip_{seg_id}.mp4")

            if not os.path.exists(audio_path):
                print(f"  [WARN] Missing audio for seg_{seg_id}, skipping")
                continue

            duration = get_audio_duration(audio_path)
            total_rendered_duration += duration
            total_frames = int(duration * fps) + 1
            seg_type = seg.get("type", "narration")

            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", "1920x1080",
                "-pix_fmt", "rgb24",
                "-r", str(fps),
                "-i", "-",
                "-i", audio_path,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-r", str(fps),
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100",
                "-ac", "2",
                "-shortest",
                out_mp4
            ]

            proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

            try:
                for f_idx in range(total_frames):
                    t = f_idx / fps

                    if seg_type == "dialogue":
                        frame = render_dialogue_karaoke_frame(
                            tokens=seg.get("tokens", [{"orig": seg.get("content", ""), "kana": seg.get("furi", ""), "romaji": seg.get("romaji", "")}]),
                            category_label=ch_title,
                            title_label=f"Scene {seg_id} • {ch_title}",
                            english_meaning=seg.get("meaning", ""),
                            grammar_text=seg.get("grammar", ""),
                            current_time=t,
                            total_duration=duration,
                            jlpt_level=seg.get("jlpt", "JLPT N5-N3")
                        )
                    elif seg_type == "breakdown":
                        frame = render_breakdown_frame(
                            ref_sentence=seg.get("ref_sentence", seg.get("content", "")),
                            vocab_list=seg.get("vocab", []),
                            grammar_title=seg.get("grammar_title", "JLPT Grammar & Culture Spotlight"),
                            grammar_bullets=seg.get("grammar_bullets", []),
                            current_time=t,
                            total_duration=duration,
                            chapter_title=ch_title,
                            jlpt_level=seg.get("jlpt", "JLPT N5-N3")
                        )
                    else:
                        frame = render_story_culture_overlay_frame(
                            chapter_num=ch_id,
                            chapter_title=ch_title,
                            section_label="DEEP CULTURE & TRAVEL ETIQUETTE" if "cultural" in seg_type else "MASTERCLASS ROADMAP",
                            narration_text=seg.get("content", ""),
                            bg_image_path=bg_scene,
                            current_time=t,
                            total_duration=duration
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
            print(f"  [RENDERED] clip_{seg_id}.mp4 ({duration:.1f}s)")

    # Concatenate all clips into Final Master Video
    concat_list_file = os.path.join(tmp_vid_dir, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for v in segment_mp4s:
            f.write(f"file '{os.path.abspath(v)}'\n")

    final_master_mp4 = os.path.join(output_dir, "video.mp4")
    published_mp4 = "output/videos/tokyoflow_wm01_weekday_mega_compilation.mp4"

    print(f"\nConcatenating {len(segment_mp4s)} clips into Final 1080p Master Video...")
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
    print(f"  [OK] Master Video: {final_master_mp4}")
    print(f"  [OK] Channel Video: {published_mp4}")
    print(f"  [OK] Total Video Duration: {total_rendered_duration/60.0:.2f} minutes ({total_rendered_duration:.1f}s)")

# ==========================================
# METADATA & LAUNCH KIT GENERATORS
# ==========================================

def build_metadata_md(output_dir: str):
    """Builds clean YouTube Studio metadata with zero URLs, zero emojis, granular timestamps, and 25 SEO tags."""
    audio_dir = os.path.join(output_dir, "audio")
    
    chapters_data = []
    curr_sec = 0.0

    for ch in MEGA_SCREENPLAY:
        ch_title = ch["chapter_title"]
        mins = int(curr_sec // 60)
        secs = int(curr_sec % 60)
        time_str = f"{mins:02d}:{secs:02d}"
        chapters_data.append((time_str, ch_title))

        for seg in ch["segments"]:
            seg_id = seg["seg_id"]
            audio_path = os.path.join(audio_dir, f"seg_{seg_id}.mp3")
            dur = get_audio_duration(audio_path)
            curr_sec += dur

    meta_file = os.path.join(output_dir, "metadata.md")
    with open(meta_file, "w", encoding="utf-8") as f:
        f.write(f"# YouTube Launch Kit: [JLPT N5-N3] WM.01 Monday to Friday Tokyo Survival All-in-One + Japanese Culture & Travel Masterclass\n\n")
        f.write(f"## Title\n")
        f.write(f"[JLPT N5-N3] WM.01 Monday to Friday Tokyo Survival All-in-One + Japanese Culture & Travel Masterclass | Real Japanese Breakdown\n\n")
        f.write(f"## Description\n\n")
        f.write(f"The ultimate 28-minute Japanese learning compilation. Master Monday-to-Friday real Tokyo life scenarios (Train Transit, 7-Eleven Kombini, Izakaya Dining, Akihabara Shopping, Ramen Ticket Ordering, Sento/Onsen Baths, and Shrine Etiquette) combined with in-depth cultural insights, travel etiquette, bathing customs, and conversation formulas.\n\n")
        f.write(f"TIMESTAMPS AND CHAPTERS:\n")
        for t_str, title in chapters_data:
            f.write(f"{t_str} - {title}\n")
        f.write(f"\n")
        
        f.write(f"KEY PHRASES COVERED:\n")
        f.write(f"1. まもなく、2番線に山手線内回りがまいります (The Yamanote Line inner loop will soon arrive at track 2)\n")
        f.write(f"2. 黄色い点字ブロックの内側までお下がりください (Please stand back behind the yellow tactile braille blocks)\n")
        f.write(f"3. 中央線への乗り換えはどのホームですか？ (Which platform is the transfer for the Chuo Line?)\n")
        f.write(f"4. お弁当温めますか？レジ袋はご利用ですか？ (Would you like your bento heated up? Will you be using a bag?)\n")
        f.write(f"5. 支払いはSuicaでお願いします (I will pay with Suica, please)\n")
        f.write(f"6. とりあえず生ビール二つお願いします！ (Two draft beers to start, please!)\n")
        f.write(f"7. 焼き鳥は塩とタレ、どちらがおすすめですか？ (Which do you recommend between salt and tare sauce?)\n")
        f.write(f"8. お会計をお願いします。別々に払えますか？ (The check, please. Can we pay separately?)\n")
        f.write(f"9. 今期の新作アニメの原作はどこにありますか？ (Where is the original manga for this season's anime?)\n")
        f.write(f"10. パスポートを提示すれば、免税手続きは可能ですか？ (If I show my passport, is tax-free processing possible?)\n")
        f.write(f"11. 食券をお買い求めください。麺の硬さはカタメでお願いします (Please buy a food ticket. Firm noodles, please)\n")
        f.write(f"12. 湯船に入る前に、体をきれいに洗ってください (Please wash thoroughly before entering the bath)\n")
        f.write(f"13. ごちそうさまでした。とても美味しかったです (Thank you for the feast. It was delicious)\n\n")

        f.write(f"JAPANESE CULTURE & ETIQUETTE DEEP DIVES:\n")
        f.write(f"• Train Departure Melodies (Hassha Melody) & Tokyo vs Osaka Escalator Standing Etiquette\n")
        f.write(f"• Kombini Seasonal Limited Editions, Oden Ordering & Onigiri Unwrapping Secret\n")
        f.write(f"• Izakaya Otoshi Appetizer Custom, Kanpai Glass Etiquette & Oshibori Rules\n")
        f.write(f"• Akihabara Gachapon Capsule Toys, Maid Cafe Magic Spells & Anime Pilgrimage (Seichi Junrei)\n")
        f.write(f"• Ramen Noodle Slurping Etiquette, Firmness Customization & Kaedama Refills\n")
        f.write(f"• Sento vs Onsen 5 Golden Bathing Rules, Post-Bath Coffee Milk & Yukata Left-over-Right Rule\n")
        f.write(f"• Shinto Shrine Torii Gate Bowing, Temizuya Purification & Ni-rei Ni-hai Ichi-rei Prayer\n")
        f.write(f"• The 3 Bowing Angles (15 deg / 30 deg / 45 deg) & Zero Tipping Omotenashi Philosophy\n\n")

        f.write(f"RECOMMENDED PRACTICE:\n")
        f.write(f"Practice interactive shadowing, pitch accent scoring, and 14,000+ native audio recordings on the companion iOS app: TokyoFlow - Japanese Speaking.\n\n")

        f.write(f"TAGS:\n")
        f.write(f"TokyoFlow, LearnJapanese, JapaneseCompilation, JapaneseListening, JapaneseShadowing, JLPTN5, JLPTN4, JLPTN3, TokyoTravel, JapaneseCulture, JapaneseEtiquette, Kombini, Izakaya, YamanoteLine, TokyoMetro, Akihabara, Ramen, Onsen, Sento, ShintoShrine, LearnJapaneseForBeginners, JapaneseGrammar, JapaneseVocabulary, TokyoLife, JapaneseSpeaking, JapanTravelTips, JapaneseCultureMasterclass\n\n")

        f.write(f"PINNED COMMENT POLL:\n")
        f.write(f"Which Japanese custom or survival phrase surprised you the most? A) The 5 Onsen Bathing Rules, B) Standing on the Left in Tokyo vs Right in Osaka, C) The Otoshi cover charge in Izakayas, D) The Onigiri 1-2-3 unwrapping hack, or E) Slurping noodles at ramen shops! Let us know below!\n")

    print(f"  [OK] Saved YouTube Studio Metadata: {meta_file}")

def build_short_metadata_md(output_dir: str):
    """Builds short metadata for the Sunday teaser short."""
    short_file = os.path.join(output_dir, "short_metadata.md")
    with open(short_file, "w", encoding="utf-8") as f:
        f.write(f"# YouTube Shorts Launch Kit: [JLPT N5-N3] WS.01 Tokyo Survival Mega-Set!\n\n")
        f.write(f"## Title\n")
        f.write(f"[JLPT N5-N3] WS.01 Monday to Friday Tokyo Survival All-in-One! #Shorts #LearnJapanese\n\n")
        f.write(f"## Description\n\n")
        f.write(f"The ultimate Tokyo daily survival and culture masterclass. Master real Japanese transit, convenience store checkout, izakaya dining, Akihabara shopping, ramen ordering, and onsen bathhouse etiquette in one complete lesson.\n\n")
        f.write(f"Watch the full 28-minute masterclass on our channel (WM.01).\n\n")
        f.write(f"Companion iOS App: TokyoFlow - Japanese Speaking\n\n")
        f.write(f"#Shorts #LearnJapanese #JapaneseSpeaking #TokyoFlow #Tokyo #JLPT #JapaneseShadowing #JapanTravel\n")
    print(f"  [OK] Saved Shorts Metadata: {short_file}")

def build_schedule_kit_json(output_dir: str):
    """Builds YouTube publishing and scheduling kit payload."""
    kit_file = os.path.join(output_dir, "youtube_schedule_kit.json")
    payload = {
        "episode_code": "WM.01",
        "shorts_code": "WS.01",
        "target_release_day": "Sunday",
        "target_release_time_est": "05:00 PM EST",
        "video_path": os.path.abspath(os.path.join(output_dir, "video.mp4")),
        "thumbnail_path": os.path.abspath(os.path.join(output_dir, "thumbnail.jpg")),
        "short_video_path": os.path.abspath(os.path.join(output_dir, "short.mp4")),
        "short_thumbnail_path": os.path.abspath(os.path.join(output_dir, "short_thumbnail.jpg")),
        "metadata_path": os.path.abspath(os.path.join(output_dir, "metadata.md")),
        "playlists": [
            "Weekly Mega-Compilations & Masterclasses",
            "JLPT N5-N3 Complete Curriculum",
            "Real-Life Tokyo Scenario Guides"
        ],
        "category_id": "27",
        "privacy_status": "public"
    }
    with open(kit_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Saved Schedule Kit JSON: {kit_file}")

def build_script_json(output_dir: str):
    """Saves complete machine-readable curriculum & screenplay."""
    script_file = os.path.join(output_dir, "script.json")
    with open(script_file, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": COMPILATION_METADATA,
            "screenplay": MEGA_SCREENPLAY
        }, f, indent=2, ensure_ascii=False)
    print(f"  [OK] Saved Screenplay Script JSON: {script_file}")

def render_sunday_teaser_short(output_dir: str):
    """Renders 9:16 vertical teaser short (35s) for Sunday using authentic 4K photo base."""
    print("\n--- RENDERING 9:16 SUNDAY TEASER SHORT ---")
    tmp_short_dir = "tmp/videogen/sunday_short"
    os.makedirs(tmp_short_dir, exist_ok=True)
    out_short = os.path.join(output_dir, "short.mp4")

    audio_path = os.path.join(output_dir, "audio", "seg_1_1_dialogue.mp3")
    if not os.path.exists(audio_path):
        return

    dur = get_audio_duration(audio_path)
    fps = 30
    total_frames = int((dur + 4.0) * fps)
    
    width, height = 1080, 1920
    bg_path = "docs/youtube_assets/scene_backgrounds/scene_yamanote_platform.jpg"
    if not os.path.exists(bg_path):
        bg_path = "docs/youtube_assets/scene_backgrounds/scene_tokyo_skyline.jpg"
    base = Image.open(bg_path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1080x1920",
        "-pix_fmt", "rgb24",
        "-r", str(fps),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        "-t", str(dur + 3.0),
        out_short
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            t = f_idx / fps
            img = base.copy()
            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle([(40, 50), (width - 40, 150)], radius=16, fill=(15, 23, 42, 230))
            draw.text((70, 75), "TokyoFlow - [JLPT N5-N3] WS.01", fill=(244, 114, 182), font=get_font(28))

            draw.rounded_rectangle([(40, 200), (width - 40, 420)], radius=20, fill=(15, 23, 42, 240), outline=(250, 204, 21), width=3)
            draw.text((70, 230), "TOKYO SURVIVAL GYM", fill=(250, 204, 21), font=get_font(32))
            draw.text((70, 290), "Sunday Mega-Compilation Teaser", fill=(255, 255, 255), font=get_font(36))
            draw.text((70, 350), "Transit • Kombini • Izakaya • Akiba • Sento", fill=(148, 163, 184), font=get_font(24))

            draw.rounded_rectangle([(40, 460), (width - 40, 1180)], radius=24, fill=(10, 15, 28, 245), outline=(56, 189, 248), width=3)
            draw.text((70, 500), "[ LIVE SHADOWING DRILL ]", fill=(56, 189, 248), font=get_font(24))
            draw.text((70, 560), "まもなく、2番線に山手線がまいります。", fill=(255, 255, 255), font=get_font(38))
            draw.text((70, 640), "黄色い点字ブロックの内側までお下がりください。", fill=(254, 240, 138), font=get_font(34))
            draw.text((70, 740), "Mamonaku, nibansen ni Yamanotesen ga mairimasu.", fill=(244, 114, 182), font=get_font(24))
            draw.text((70, 800), "Meaning: The Yamanote Line will soon arrive at track 2.", fill=(226, 232, 240), font=get_font(26))
            draw.text((70, 870), "💡 Stand behind the yellow tactile braille paving tiles", fill=(52, 211, 153), font=get_font(24))

            draw.rounded_rectangle([(40, 1220), (width - 40, 1820)], radius=20, fill=(225, 29, 72))
            draw.text((70, 1260), "WATCH FULL 28-MIN MASTERCLASS", fill=(255, 255, 255), font=get_font(34))
            draw.text((70, 1330), "• Full Mon-Fri 5-Day Scenario Micro-Lessons", fill=(254, 240, 138), font=get_font(26))
            draw.text((70, 1390), "• Deep Japanese Customs, Etiquette & Bathing Rules", fill=(255, 255, 255), font=get_font(24))
            draw.text((70, 1460), "TokyoFlow - Japanese Speaking (iOS)", fill=(255, 255, 255), font=get_font(28))

            proc.stdin.write(img.tobytes())
    except (BrokenPipeError, IOError):
        pass
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.wait()

    print(f"  [OK] Saved Sunday Teaser Short: {out_short}")

# ==========================================
# MAIN ENTRYPOINT
# ==========================================

async def main_async():
    print("================================================================================")
    print(" TOKYOFLOW JAPANESE: SUNDAY MEGA-COMPILATION PRODUCTION PIPELINE (REAL 4K PHOTOS)")
    print(f" Series Code: {COMPILATION_METADATA['series_code']} • Target Duration: {COMPILATION_METADATA['target_duration_mins']} mins")
    print("================================================================================")

    output_dir = os.path.join("docs/youtube_releases", COMPILATION_METADATA["release_folder"])
    os.makedirs(output_dir, exist_ok=True)

    # 1. Synthesize Dual-Voice Audio Assets
    await synthesize_all_audio_tracks(output_dir)

    # 2. Build 16:9 & 9:16 Golden Master Thumbnails (Real 4K Photo Base)
    render_master_thumbnail(output_dir)
    render_shorts_thumbnail(output_dir)

    # 3. Build Metadata & Schedule Kits
    build_metadata_md(output_dir)
    build_short_metadata_md(output_dir)
    build_schedule_kit_json(output_dir)
    build_script_json(output_dir)

    # 4. Render 9:16 Vertical Teaser Short
    render_sunday_teaser_short(output_dir)

    # 5. Render 1080p Full Master Video (25-30 mins)
    render_full_master_video(output_dir)

    print("\n================================================================================")
    print(f" ALL RELEASE DELIVERABLES PRODUCED IN: {output_dir}")
    print("================================================================================")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
