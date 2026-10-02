#!/usr/bin/env python3
"""
TokyoFlow Japanese • Unified YouTube Video & Release Pipeline
Produces modernized, high-converting YouTube micro-lesson packages for EP. 01 to EP. 04:
1. 3-Tier Ruby Typography (Kana top, Japanese center, Romaji bottom, English meaning)
2. Millisecond-level word-by-word karaoke follow-along highlight with 80ms anticipatory lead
3. Bilingual Teamwork Breakdown Slides:
   - Nanami (ja-JP-NanamiNeural) pronounces 100% native Japanese words & spotlight examples
   - Andrew (en-US-AndrewNeural) explains English definitions, grammar rules & cultural nuances
   - Dynamic Card & Spotlight Follow-Along Highlighting synchronized to the exact audio cues
4. Fast 3-second Action-Oriented Outro Cards
5. 16:9 High-CTR Serialized YouTube Thumbnails (Yellow Hook, Bold Japanese, Episode Badge)
6. Complete Release Packages (video.mp4, thumbnail.jpg, metadata.md, script.json)
"""

import os
import sys
import json
import shutil
import asyncio
import subprocess
import edge_tts

from timing_engine import (
    extract_tokens_from_text,
    align_sentence_tokens_with_audio
)
from slide_designer import (
    render_follow_along_video_clip,
    render_breakdown_video_clip,
    render_static_video_clip,
    render_outro_frame
)
from voice_engine import synthesize_speech
from generate_thumbnails import generate_serialized_thumbnail

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def build_teamwork_breakdown_audio(cues: list, out_final_path: str, tmp_dir: str) -> dict:
    """
    Builds a bilingual teamwork breakdown track:
    - Nanami (ja-JP-NanamiNeural) for Japanese words & example phrases
    - Andrew (en-US-AndrewNeural) for English explanations
    Returns exact card & spotlight timings for seamless visual follow-along.
    """
    os.makedirs(tmp_dir, exist_ok=True)
    seg_files = []
    card_timings = {}
    spotlight_timings = (9999.0, 9999.0)
    current_time = 0.0

    for i, cue in enumerate(cues):
        speaker = cue["speaker"]
        text = cue["text"]
        fn = os.path.join(tmp_dir, f"cue_{i:02d}.mp3")
        
        voice = "ja-JP-NanamiNeural" if speaker == "ja" else "en-US-AndrewNeural"
        rate = "-6%" if speaker == "ja" else "+2%"
        pitch = "+3Hz" if speaker == "ja" else "+0Hz"
        
        comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await comm.save(fn)
        dur = get_audio_duration(fn)
        
        start_t = current_time
        end_t = current_time + dur
        
        if "card_idx" in cue:
            c_idx = cue["card_idx"]
            if c_idx not in card_timings:
                card_timings[c_idx] = (start_t, end_t)
            else:
                card_timings[c_idx] = (card_timings[c_idx][0], end_t)
                
        if cue.get("is_spotlight"):
            if spotlight_timings == (9999.0, 9999.0):
                spotlight_timings = (start_t, end_t)
            else:
                spotlight_timings = (spotlight_timings[0], end_t)
                
        seg_files.append(fn)
        current_time += dur

    list_path = os.path.join(tmp_dir, "cues.txt")
    with open(list_path, "w") as f:
        for fn in seg_files:
            f.write(f"file '{os.path.abspath(fn)}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_path,
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        out_final_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    total_dur = get_audio_duration(out_final_path)
    return {
        "total_duration": total_dur,
        "timings": {
            "active_vocab_idx": card_timings,
            "spotlight_window": spotlight_timings
        }
    }

def concat_videos_seamless(video_list: list, final_output_path: str):
    concat_txt_path = "tmp/videogen/concat_list.txt"
    os.makedirs(os.path.dirname(concat_txt_path), exist_ok=True)
    with open(concat_txt_path, "w") as f:
        for v in video_list:
            f.write(f"file '{os.path.abspath(v)}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        final_output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

EPISODES = [
    {
        "episode_number": 1,
        "folder_name": "E01-Yamanote_Transit-v1.0",
        "slug": "yamanote_transit",
        "title": "Tokyo Metro & Yamanote Line Platform Broadcasts",
        "yt_title": "Tokyo Train Station Announcements Decoded!  Yamanote Line Immersion (EP. 01)",
        "category": "Tokyo Transit • Yamanote Line",
        "level": "JLPT N4-N3",
        "district": "Shinjuku ()",
        "youtube_id": "yN6dTC-LBz8",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/tokyo_subway_metro_1790613022369.jpg",
        "cover": {
            "hook": "TOKYO METRO HACK",
            "jp": "",
            "tag": " Native Transit Audio • Shadowing"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Approaching Train Announcement",
                "spoken_text": "2",
                "en": "The Yamanote Line inner loop train will arrive on Platform 2.",
                "tip": "'' is Kenjougo (humble Japanese), standard JR platform phrasing.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "mamonaku", "pos": "Adverb", "meaning": "Shortly / Soon"},
                    {"orig": "", "kana": "", "romaji": ""},
                    {"orig": "2", "kana": "", "romaji": "ni-ban-sen ni", "pos": "Noun + Part.", "meaning": "On Platform 2"},
                    {"orig": "", "kana": "", "romaji": "yamanote-sen", "pos": "Proper Noun", "meaning": "Yamanote Line"},
                    {"orig": "", "kana": "", "romaji": "uchi-mawari ga", "pos": "Noun + Part.", "meaning": "Inner loop (clockwise)"},
                    {"orig": "", "kana": "", "romaji": "mairimasu.", "pos": "Humble Verb", "meaning": "Is arriving (humble)"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Train Announcement Breakdown",
                "sentence_ja": "2",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "mamonaku", "pos": "Adverb", "meaning": "Shortly / Soon"},
                    {"orig": "2", "kana": "", "romaji": "ni-ban-sen ni", "pos": "Noun + Part.", "meaning": "On Platform 2"},
                    {"orig": "", "kana": "", "romaji": "yamanote-sen", "pos": "Proper Noun", "meaning": "Yamanote Loop Line"},
                    {"orig": "", "kana": "", "romaji": "uchi-mawari ga", "pos": "Noun + Part.", "meaning": "Clockwise Inner Loop"},
                    {"orig": "", "kana": "", "romaji": "mairimasu", "pos": "Humble Verb", "meaning": "Kenjougo for  (Coming)"}
                ],
                "grammar_title": " (Kenjougo) — ",
                "grammar_bullets": [
                    ("1. Humble Verb ():", "'' is the humble form of ' (kuru, to come)'."),
                    ("2. Tokyo Transit Etiquette:", "Station announcements universally humble the train staff to elevate passengers."),
                    ("3. Daily Life Equivalent:", "'' (I will be right there with you)."),
                    ("4. Key Takeaway:", "Never use Kenjougo when referring to your customer's actions.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down the vocabulary and grammar."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Adverb: shortly, or very soon.", "card_idx": 0},
                    {"speaker": "ja", "text": "2", "card_idx": 1},
                    {"speaker": "en", "text": "On platform 2.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "The JR Yamanote Loop Line.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Clockwise inner loop direction.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Humble verb for arriving, Kenjougo of kuru.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar Spotlight: Kenjougo humble speech.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "I will be right there with you. Station broadcasts use humble verbs to elevate passengers.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Safety & Tactile Paving",
                "spoken_text": "",
                "en": "Please stand behind the yellow tactile warning blocks.",
                "tip": "'' is the respectful imperative formula ( + Verb stem + ).",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kiiroi", "pos": "Adjective", "meaning": "Yellow"},
                    {"orig": "", "kana": "", "romaji": "tenji-burokku no", "pos": "Noun + Part.", "meaning": "Tactile warning block's"},
                    {"orig": "", "kana": "", "romaji": "uchigawa made", "pos": "Noun + Part.", "meaning": "To the inside / behind"},
                    {"orig": "", "kana": "", "romaji": "osagari kudasai.", "pos": "Polite Imperative", "meaning": "Please step back"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Platform Safety Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "kiiroi", "pos": "Adjective", "meaning": "Yellow color"},
                    {"orig": "", "kana": "", "romaji": "tenji burokku", "pos": "Noun", "meaning": "Braille / tactile paving"},
                    {"orig": "", "kana": "", "romaji": "uchigawa made", "pos": "Noun + Part.", "meaning": "Behind / inside limit"},
                    {"orig": "", "kana": "", "romaji": "osagari", "pos": "Verb Stem", "meaning": "Step back (from )"},
                    {"orig": "", "kana": "", "romaji": "kudasai", "pos": "Polite Request", "meaning": "Please do"}
                ],
                "grammar_title": ":  +  + ",
                "grammar_bullets": [
                    ("1. Respectful Command:", "Used by staff to politely instruct customers or passengers."),
                    ("2. Formation Formula:", " + Verb Masu-Stem +  (e.g.  = Please wait)."),
                    ("3. Platform Context:", "Heard at every station before trains arrive for commuter safety."),
                    ("4. Casual Equivalent:", " (Sagatte) — only used with friends/family.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down this platform safety announcement."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Adjective: yellow color.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Noun: tactile paving blocks.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Behind the safety line.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Verb stem from sagaru, to step back.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Polite request formula.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Respectful command formula, O plus verb stem plus kudasai.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Please wait a moment. Used widely by transit and store staff.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Transfer Assistance Drill",
                "spoken_text": "",
                "en": "Excuse me, which platform is the transfer for the Chuo Line?",
                "tip": "Essential phrase when asking station staff. Replace '' with any train line.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "sumimasen", "pos": "Phrase", "meaning": "Excuse me"},
                    {"orig": "", "kana": "", "romaji": ""},
                    {"orig": "", "kana": "", "romaji": "chuuou-sen e no", "pos": "Proper Noun + Part.", "meaning": "To Chuo Line"},
                    {"orig": "", "kana": "", "romaji": "norikae wa", "pos": "Noun + Topic", "meaning": "Transfer"},
                    {"orig": "", "kana": "", "romaji": "dono hoomu desu ka?", "pos": "Question", "meaning": "Which platform is it?"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },
    {
        "episode_number": 2,
        "folder_name": "E02-Kombini_Checkout-v1.0",
        "slug": "kombini_checkout",
        "title": "Japanese 7-Eleven & FamilyMart Checkout Mastery",
        "yt_title": "Survive Tokyo 7-Eleven Checkout!  Rapid Register Japanese Decoded (EP. 02)",
        "category": "Kombini Protocol • Checkout Guide",
        "level": "JLPT N5-N4",
        "district": "Shibuya ()",
        "youtube_id": "6er1tWAH_oQ",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_kombini_1790626387613.jpg",
        "cover": {
            "hook": "KOMBINI SURVIVAL",
            "jp": "",
            "tag": " 1-Sec Register Reply • Shadowing"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Bento Heating Question",
                "spoken_text": "",
                "en": "Would you like your bento heated up?",
                "tip": "Reply with ' (Please heat it)' or ' (No thanks)'.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "obentou", "pos": "Noun", "meaning": "Bento boxed lunch"},
                    {"orig": "", "kana": "", "romaji": "atatamemasu ka?", "pos": "Verb + Q", "meaning": "Would you like it heated?"},
                    {"orig": "", "kana": "", "romaji": "shoushou", "pos": "Adverb", "meaning": "A little moment"},
                    {"orig": "", "kana": "", "romaji": "omachi kudasai.", "pos": "Polite Request", "meaning": "Please wait"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Register Conversation Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "obentou", "pos": "Polite Noun", "meaning": "Bento lunch box"},
                    {"orig": "", "kana": "", "romaji": "atatamemasu ka", "pos": "Verb + Q", "meaning": "Do you want it heated?"},
                    {"orig": "", "kana": "", "romaji": "shoushou", "pos": "Adverb", "meaning": "A short moment"},
                    {"orig": "", "kana": "", "romaji": "omachi kudasai", "pos": "Polite Imperative", "meaning": "Please wait politely"}
                ],
                "grammar_title": ": ",
                "grammar_bullets": [
                    ("1. Yes Response:", "' (Atatamete kudasai)' or simply ' (Onegaishimasu)'."),
                    ("2. No Response:", "' (Daijoubu desu)' or ' (Kono mama de, as is)'."),
                    ("3. Polite Honorific '-':", "'' adds the polite prefix '' to show customer respect."),
                    ("4. Speed Tip:", "Clerks ask very fast; answer with a crisp nod and 1-word reply.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down this convenience store register phrase."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Polite noun: bento lunch box.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Would you like it heated up?", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Adverb: just a short moment.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Please wait politely.", "card_idx": 3},
                    {"speaker": "en", "text": "Register etiquette: To heat your food, answer:", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Please heat it. Or if you prefer it as is, say:", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "It is fine as is.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Declining Plastic Bags",
                "spoken_text": "",
                "en": "No plastic bag needed, thank you. A tape sticker is fine.",
                "tip": "'' paired with a gentle nod is the natural way to politely decline.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "reji-bukuro wa", "pos": "Noun + Topic", "meaning": "Plastic bag"},
                    {"orig": "", "kana": "", "romaji": "daijoubu desu.", "pos": "Phrase", "meaning": "No thanks / I'm fine"},
                    {"orig": "", "kana": "", "romaji": "shiiru de", "pos": "Noun + Part.", "meaning": "With a sticker"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Declining Etiquette Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "reji bukuro", "pos": "Noun", "meaning": "Register plastic shopping bag"},
                    {"orig": "", "kana": "", "romaji": "daijoubu desu", "pos": "Polite Phrase", "meaning": "I'm okay / No thank you"},
                    {"orig": "", "kana": "", "romaji": "shiiru", "pos": "Loanword", "meaning": "Proof of purchase tape sticker"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu", "pos": "Polite Request", "meaning": "Please do so"}
                ],
                "grammar_title": ":  (Polite Refusal)",
                "grammar_bullets": [
                    ("1. The Polite 'No':", "Avoid saying blunt ' (I don't want it)'. Use '' instead."),
                    ("2. Sticker Protocol:", "If you refuse a bag, the clerk applies a small tape '' on items."),
                    ("3. If you DO want a bag:", "' (Fukuro o ichimai onegaishimasu)' (3-5 JPY)."),
                    ("4. Body Language:", "A slight hand palm-down gesture makes your refusal crystal clear.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down how to decline plastic bags politely."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Plastic shopping bag.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "I am okay, no thank you.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Proof of purchase tape sticker.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Please do so.", "card_idx": 3},
                    {"speaker": "en", "text": "Grammar spotlight: The universal polite refusal with Daijoubu desu.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Pair this with a gentle nod for natural Tokyo manners.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Contactless Payment Drill",
                "spoken_text": "Suica",
                "en": "I will pay with Suica, please. No point card.",
                "tip": "'[Payment method] ' works for Suica, PayPay, or Credit Card.",
                "tokens": [
                    {"orig": "Suica", "kana": "", "romaji": "Suica de", "pos": "Noun + Part.", "meaning": "With Suica"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"},
                    {"orig": "", "kana": "", "romaji": "pointo kaado wa", "pos": "Noun + Topic", "meaning": "Reward card"},
                    {"orig": "", "kana": "", "romaji": "arimasen.", "pos": "Verb (Neg)", "meaning": "I don't have"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },
    {
        "episode_number": 3,
        "folder_name": "E03-Izakaya_Night-v1.0",
        "slug": "izakaya_night",
        "title": "Authentic Tokyo Izakaya Ordering & Toasting Etiquette",
        "yt_title": "Order Like a Tokyo Local at an Izakaya!  'Toriaezu Nama!' Explained (EP. 03)",
        "category": "Izakaya Culture • Dining Guide",
        "level": "JLPT N4-N3",
        "district": "Shinjuku Omoide Yokocho ()",
        "youtube_id": "B4sN_BkLcOw",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/pl_cover_izakaya_1790626403507.jpg",
        "cover": {
            "hook": "IZAKAYA MASTERY",
            "jp": "",
            "tag": " Showa Pub Etiquette • Shadowing"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. The First Drink Order",
                "spoken_text": "",
                "en": "To start, two draft beers please!",
                "tip": "'' (for starters) is the quintessential Japanese izakaya opener.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "toriaezu", "pos": "Adverb", "meaning": "For starters / To begin with"},
                    {"orig": "", "kana": "", "romaji": "nama biiru", "pos": "Noun", "meaning": "Draft beer"},
                    {"orig": "", "kana": "", "romaji": "futatsu", "pos": "Counter", "meaning": "Two items"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu!", "pos": "Polite Request", "meaning": "Please!"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Izakaya Ordering Culture Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "toriaezu", "pos": "Adverb", "meaning": "For starters / First of all"},
                    {"orig": "", "kana": "", "romaji": "nama biiru", "pos": "Noun", "meaning": "Draft beer (short:  nama)"},
                    {"orig": "", "kana": "", "romaji": "futatsu", "pos": "Counter", "meaning": "Two (native counter)"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu", "pos": "Polite Request", "meaning": "Please give us"}
                ],
                "grammar_title": ":  (The Opening Order)",
                "grammar_bullets": [
                    ("1. Cultural Norm:", "In Japanese pubs, ordering drinks right away eases the kitchen and starts the table vibe."),
                    ("2. Counting Drinks:", " (1),  (2),  (3), or [Number]  (hai)."),
                    ("3. Non-Alcoholic Starter:", "' (Uuron-cha hitotsu)' for Oolong tea."),
                    ("4. Table Charge ():", "Expect a small mandatory appetizer called 'Otoushi' served with drinks.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down this classic Tokyo izakaya order."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Adverb: for starters, or first of all.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Draft beer, often shortened to Nama.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Native Japanese counter for two items.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Please give us.", "card_idx": 3},
                    {"speaker": "en", "text": "Izakaya cultural spotlight: The first drink rule.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Ordering your first drink immediately helps the kitchen and starts the table toast.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Yakitori Seasoning Drill",
                "spoken_text": "",
                "en": "Assorted yakitori platter with salt seasoning, please.",
                "tip": "Staff will ask '' (salt or sweet tare sauce). ' (shio)' highlights the chicken flavor.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "yakitori", "pos": "Noun", "meaning": "Grilled chicken skewers"},
                    {"orig": "", "kana": "", "romaji": "moriawase o", "pos": "Noun + Obj", "meaning": "Assorted combo platter"},
                    {"orig": "", "kana": "", "romaji": "shio de", "pos": "Noun + Part.", "meaning": "With salt seasoning"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Food Seasoning Choice Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "yakitori", "pos": "Noun", "meaning": "Grilled chicken skewers"},
                    {"orig": "", "kana": "", "romaji": "moriawase", "pos": "Noun", "meaning": "Chef's assortment combo"},
                    {"orig": "", "kana": "", "romaji": "shio", "pos": "Noun", "meaning": "Salt seasoning"},
                    {"orig": "", "kana": "", "romaji": "tare", "pos": "Noun", "meaning": "Sweet savory soy glaze"}
                ],
                "grammar_title": ":  (Salt) vs  (Tare Sauce)",
                "grammar_bullets": [
                    ("1. Salt Choice ():", "Crisp, light, highlights the natural char and quality of the meat."),
                    ("2. Tare Choice ():", "Rich, sweet soy-mirin glaze, great for liver, meatballs (tsukune), and beer."),
                    ("3. Platter Order:", "' (Moriawase)' gives you 5-6 assorted cuts chosen by the chef."),
                    ("4. Ordering Combo:", "'5 (Shio de go-hon)' = 5 skewers with salt.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down ordering yakitori skewers."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Grilled chicken skewers.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Chef's assortment combo platter.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Salt seasoning.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Sweet savory soy glaze.", "card_idx": 3},
                    {"speaker": "en", "text": "Seasoning choice spotlight: Shio versus Tare.", "is_spotlight": True},
                    {"speaker": "ja", "text": "5", "is_spotlight": True},
                    {"speaker": "en", "text": "Salt highlights the pure flavor and crisp char of the meat.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. The Check & Receipt Drill",
                "spoken_text": "",
                "en": "The bill and formal receipt, please.",
                "tip": "' (okaikei)' means bill, while ' (ryoushuusho)' is a tax receipt.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "okaikei to", "pos": "Noun + And", "meaning": "The bill and"},
                    {"orig": "", "kana": "", "romaji": "ryoushuusho o", "pos": "Noun + Obj", "meaning": "Formal receipt"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },
    {
        "episode_number": 4,
        "folder_name": "E04-Akiba_Pilgrimage-v1.0",
        "slug": "akiba_pilgrimage",
        "title": "Akihabara Pilgrimage: Figures, Merch & Manga Tax-Free",
        "yt_title": "Akihabara Anime & Manga Shopping Japanese!  Tax-Free & Rare Merch (EP. 04)",
        "category": "Akihabara Shopping • Anime Protocol",
        "level": "JLPT N3-N2",
        "district": "Akihabara ()",
        "youtube_id": "iaGo6ey75Ws",
        "bg_image": "/Users/kilvonwu/.gemini/antigravity/brain/a1123288-34fb-45bc-a705-3090b9af2bbb/akiba_neon_manga_1790602623116.jpg",
        "cover": {
            "hook": "AKIBA MANGA HUNT",
            "jp": "",
            "tag": " Tax-Free & Figures • Shadowing"
        },
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Manga & Novel Finding",
                "spoken_text": "",
                "en": "Where are the original manga/novels for this season's new anime?",
                "tip": "Use ' (gensaku)' to ask for the original book source of any anime series.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "konki no", "pos": "Noun + Part.", "meaning": "This season's"},
                    {"orig": "", "kana": "", "romaji": "shinsaku anime no", "pos": "Noun + Part.", "meaning": "New anime release's"},
                    {"orig": "", "kana": "", "romaji": "gensaku wa", "pos": "Noun + Topic", "meaning": "Original source work"},
                    {"orig": "", "kana": "", "romaji": "doko ni", "pos": "Question", "meaning": "Where at"},
                    {"orig": "", "kana": "", "romaji": "arimasu ka?", "pos": "Verb + Q", "meaning": "Is located?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Otaku Shopping Terminology Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "konki", "pos": "Noun", "meaning": "Current broadcast season (Quarter)"},
                    {"orig": "", "kana": "", "romaji": "shinsaku", "pos": "Noun", "meaning": "New release work"},
                    {"orig": "", "kana": "", "romaji": "gensaku", "pos": "Noun", "meaning": "Original source manga / light novel"},
                    {"orig": "", "kana": "", "romaji": "doko ni arimasu ka", "pos": "Question", "meaning": "Where is it located?"}
                ],
                "grammar_title": ":  (Original Work) & ",
                "grammar_bullets": [
                    ("1. '' Meaning:", "Points to the original manga or light novel that inspired the anime adaptation."),
                    ("2. Asking Floor Staff:", "'[Anime Name] ' (Where is the book section for X?)."),
                    ("3. Light Novel vs Manga:", "' (Ranobe)' for light novels; ' (Tankoubon)' for manga volumes."),
                    ("4. Location Tip:", "Major Akiba bookstores group new season anime originals on the ground floor.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down shopping for anime books in Akihabara."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Current broadcast anime season.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "New release work.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Original source manga or light novel.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Where is it located?", "card_idx": 3},
                    {"speaker": "en", "text": "Akihabara shopping spotlight: Asking for source books.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Use Gensaku when looking for original books adapted into anime.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Pre-order Perks & Store Bonus",
                "spoken_text": "",
                "en": "Does this limited edition still come with the store purchase bonus perk?",
                "tip": "' (tokuten)' refers to exclusive gifts like acrylic stands, badges, or illustration cards.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kochira no", "pos": "Pronoun", "meaning": "This one's"},
                    {"orig": "", "kana": "", "romaji": "genteiban,", "pos": "Noun", "meaning": "Limited edition"},
                    {"orig": "", "kana": "", "romaji": "kounyuu tokuten wa", "pos": "Noun + Topic", "meaning": "Purchase bonus perk"},
                    {"orig": "", "kana": "", "romaji": "mada", "pos": "Adverb", "meaning": "Still / Yet"},
                    {"orig": "", "kana": "", "romaji": "tsukimasu ka?", "pos": "Verb + Q", "meaning": "Does it come with?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Exclusive Bonus Merch Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "genteiban", "pos": "Noun", "meaning": "Limited collector's edition"},
                    {"orig": "", "kana": "", "romaji": "kounyuu tokuten", "pos": "Noun", "meaning": "Store purchase bonus / gift"},
                    {"orig": "", "kana": "", "romaji": "mada", "pos": "Adverb", "meaning": "Still / remaining in stock"},
                    {"orig": "", "kana": "", "romaji": "tsukimasu ka", "pos": "Verb + Q", "meaning": "Does it attach / include?"}
                ],
                "grammar_title": ":  (Tokuten) & ",
                "grammar_bullets": [
                    ("1. Store Exclusives:", "Animate, Gamers, Toranoana each have different exclusive ''."),
                    ("2. First-Come Basis:", "' (While supplies last)' — ask staff before purchasing."),
                    ("3. Acrylic Stands ():", "Acronym for 'Acrylic Stand ()'. Highly coveted!"),
                    ("4. Bonus Check:", "Staff will check their register counter stash to see if bonus perks remain.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down asking for exclusive store bonus merch."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Limited collector's edition.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Store purchase bonus gift.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Still, or remaining in stock.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Does it come included?", "card_idx": 3},
                    {"speaker": "en", "text": "Bonus perk spotlight: Exclusive Tokuten items.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Bonus perks are first-come first-served, so always check with staff before checkout.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Tax-Free Exemption Checkout Drill",
                "spoken_text": "",
                "en": "Could you process tax-free exemption, please? I have my passport.",
                "tip": "Present your passport with tourist entry visa for 10% consumption tax refund over 5,000 JPY.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "menzei tetsuzuki o", "pos": "Noun + Obj", "meaning": "Tax-free procedure"},
                    {"orig": "", "kana": "", "romaji": "onegai dekimasu ka?", "pos": "Polite Potential", "meaning": "Could I request?"},
                    {"orig": "", "kana": "", "romaji": "pasupooto o", "pos": "Noun + Obj", "meaning": "Passport"},
                    {"orig": "", "kana": "", "romaji": "motte imasu.", "pos": "Verb Phrase", "meaning": "I have / hold"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    }
]

def generate_metadata_markdown(ep: dict, total_duration_s: float, chapter_timestamps: list) -> str:
    ep_num = ep["episode_number"]
    yt_title = ep["yt_title"]
    folder_name = ep["folder_name"]
    
    chapters_formatted = "\n".join([f"{ts} - {title}" for ts, title in chapter_timestamps])
    
    key_phrases = "\n".join([
        f"• {s.get('spoken_text', '')} ({s.get('tokens', [{}])[0].get('romaji', '')}) — {s.get('en', '')}"
        for s in ep['slides'] if s.get('type') == 'follow_along'
    ])
    
    grammar_points = "\n".join([
        f"• {s.get('grammar_title', '')}"
        for s in ep['slides'] if s.get('type') == 'breakdown'
    ])

    return f"""#  YouTube Launch Package: {folder_name}
# {yt_title}

##  Release Directory Information
- **Standard Release Directory**: `docs/youtube_releases/{folder_name}/`
- **Episode Identifier**: `EP. {ep_num:02d}` (`{folder_name}`)
- **Target Category**: `{ep['category']}`
- **JLPT Level**: `{ep['level']}`
- **District / Setting**: `{ep['district']}`
- **Video Asset**: `video.mp4` (1080p Full HD, 30.0 fps, {total_duration_s:.1f}s)
- **Thumbnail Asset**: `thumbnail.jpg` (1920x1080 High-CTR Serialized Cover)
- **Metadata Document**: `metadata.md` (This launch package)
- **Structured Manifest**: `script.json` (Machine-readable bilingual script)

---

##  YouTube Video Title (Copy & Paste)

```
{yt_title}
```

---

##  YouTube Description Box (Copy & Paste Ready)

```markdown
{yt_title}

Learn authentic Tokyo Japanese as spoken by locals! In this episode, we dive into {ep['title']} in {ep['district']}.

Master high-frequency phrases, pitch accent patterns, and cultural nuances with real-time millisecond karaoke follow-along highlighting and bilingual teamwork breakdowns (Native Tokyo Voice + English Explanations).

⏱ CHAPTER TIMESTAMPS:
{chapters_formatted}

 KEY PHRASES COVERED:
{key_phrases}

 GRAMMAR & NUANCE SPOTLIGHTS:
{grammar_points}

 TAKE YOUR JAPANESE TO THE NEXT LEVEL:
Practice interactive speech shadowing with instant pitch accent scoring on TokyoFlow for iOS:
 Download on the App Store: TokyoFlow - Japanese Speaking (https://apps.apple.com/app/tokyoflow-japanese-speaking/id6740000000)
 Official Website: https://tokyoflow.app

 Subscribe to TokyoFlow Japanese for weekly real-life Tokyo Japanese micro-lessons!
#TokyoFlow #LearnJapanese #JapaneseSpeaking #TokyoTravel #JLPT #JapaneseShadowing #{ep['slug'].replace('_', '')}
```

---

##  Pinned Comment (Copy & Paste)

```markdown
 What Tokyo scenario do you want us to cover next? Let us know in the comments below!
 Practice this lesson with native VoiceBank audio & speech shadowing scoring in the TokyoFlow iOS app: https://apps.apple.com/app/tokyoflow-japanese-speaking/id6740000000
```

---

##  YouTube SEO Tags (Comma Separated)

```
learn japanese, tokyo japanese, japanese conversation, {ep['slug'].replace('_', ' ')}, tokyo travel japanese, japanese pronunciation, JLPT, JLPT {ep['level']}, japanese listening practice, japanese shadowing, tokyoflow, study japanese, anime japanese, travel tokyo, tokyo metro, japanese speaking app
```
"""

async def package_episode(ep: dict):
    ep_num = ep["episode_number"]
    folder_name = ep["folder_name"]
    ep_label = f"EP. {ep_num:02d}"
    release_dir = os.path.join("docs", "youtube_releases", folder_name)
    os.makedirs(release_dir, exist_ok=True)
    
    print(f"\n==========================================")
    print(f" Packaging {folder_name}")
    print(f"==========================================")

    workdir = f"tmp/videogen/{folder_name}"
    os.makedirs(workdir, exist_ok=True)
    
    segment_videos = []
    chapter_timestamps = []
    current_time_elapsed = 0.0
    
    for idx, slide in enumerate(ep["slides"]):
        seg_prefix = f"{workdir}/seg_{idx:02d}"
        audio_path = f"{seg_prefix}.m4a"
        video_path = f"{seg_prefix}.mp4"
        s_type = slide.get("type", "follow_along")
        
        # Calculate timestamp formatted mm:ss
        ts_min = int(current_time_elapsed // 60)
        ts_sec = int(current_time_elapsed % 60)
        ts_str = f"{ts_min:02d}:{ts_sec:02d}"
        chapter_title = slide.get("chapter", f"Part {idx+1}")
        chapter_timestamps.append((ts_str, chapter_title))

        if s_type == "follow_along":
            spoken_text = slide["spoken_text"]
            await synthesize_speech(spoken_text, audio_path, lang="ja", rate="-6%", pitch="+3Hz")
            duration = get_audio_duration(audio_path)
            
            tokens = slide.get("tokens", [])
            aligned_tokens = align_sentence_tokens_with_audio(audio_path, tokens)
            
            render_follow_along_video_clip(
                tokens=aligned_tokens,
                category_label=ep.get("category", "Tokyo Scenario"),
                title_label=f"{ep_label} • {ep['title']}",
                english_meaning=slide.get("en", ""),
                pro_tip=slide.get("tip", ""),
                chapter_label=chapter_title,
                ep_label=ep_label,
                audio_path=audio_path,
                duration=duration,
                out_mp4_path=video_path,
                fps=30
            )
            seg_dur = duration + 0.3
            current_time_elapsed += seg_dur
            print(f"   Follow-Along Segment {idx+1}/{len(ep['slides'])} rendered ({duration:.1f}s)")

        elif s_type == "breakdown":
            vocab_list = slide.get("vocab", [])
            grammar_title = slide.get("grammar_title", "Grammar Point")
            grammar_bullets = slide.get("grammar_bullets", [])
            teamwork_cues = slide.get("teamwork_cues", [])
            
            # Build Bilingual Teamwork Audio (Nanami JA + Andrew EN)
            tw_res = await build_teamwork_breakdown_audio(
                cues=teamwork_cues,
                out_final_path=audio_path,
                tmp_dir=f"{workdir}/tw_{idx:02d}"
            )
            duration = tw_res["total_duration"]
            timings = tw_res["timings"]
            
            render_breakdown_video_clip(
                sentence_ja=slide.get("sentence_ja", ""),
                vocab_list=vocab_list,
                grammar_title=grammar_title,
                grammar_bullets=grammar_bullets,
                category_label=ep.get("category", "Tokyo Scenario"),
                chapter_label=chapter_title,
                ep_label=ep_label,
                timings=timings,
                audio_path=audio_path,
                duration=duration,
                out_mp4_path=video_path,
                fps=30
            )
            seg_dur = duration + 0.3
            current_time_elapsed += seg_dur
            print(f"   Bilingual Teamwork Breakdown Segment {idx+1}/{len(ep['slides'])} rendered ({duration:.1f}s)")

        elif s_type == "outro":
            spoken_text = slide["spoken_text"]
            await synthesize_speech(spoken_text, audio_path, lang="ja", rate="+15%", pitch="+3Hz")
            dur_audio = get_audio_duration(audio_path)
            duration = max(dur_audio + 0.35, 3.4)
            
            frame = render_outro_frame(ep_label=ep_label)
            render_static_video_clip(frame, audio_path, duration, video_path, fps=30)
            current_time_elapsed += duration
            print(f"   Natural Unclipped Outro Segment {idx+1}/{len(ep['slides'])} rendered ({duration:.1f}s)")

        segment_videos.append(video_path)

    target_video = os.path.join(release_dir, "video.mp4")
    concat_videos_seamless(segment_videos, target_video)
    
    # Mirror to output/videos/
    os.makedirs("output/videos", exist_ok=True)
    shutil.copyfile(target_video, f"output/videos/{folder_name}.mp4")
    shutil.copyfile(target_video, f"output/videos/tokyoflow_v{ep_num:02d}_{ep['slug']}.mp4")
    
    final_duration = get_audio_duration(target_video)
    print(f"   Full HD 1080p video assembled: {target_video} ({final_duration:.1f}s)")

    # 2. Render High-CTR Serialized Thumbnail using Thumbnail Skill standard
    target_thumb = os.path.join(release_dir, "thumbnail.jpg")
    cov = ep["cover"]
    generate_serialized_thumbnail(
        ep_num=ep_num,
        english_hook=cov["hook"],
        japanese_key_phrase=cov["jp"],
        bottom_tag=cov["tag"],
        bg_image_path=ep.get("bg_image", ""),
        output_path=target_thumb
    )
    # Mirror thumbnail
    os.makedirs("docs/youtube_assets/thumbnails", exist_ok=True)
    shutil.copyfile(target_thumb, f"docs/youtube_assets/thumbnails/{folder_name}_thumb.jpg")
    print(f"   1920x1080 Serialized Thumbnail saved: {target_thumb}")

    # 3. Write Complete Launch Metadata Package
    target_meta = os.path.join(release_dir, "metadata.md")
    with open(target_meta, "w", encoding="utf-8") as f:
        f.write(generate_metadata_markdown(ep, final_duration, chapter_timestamps))
    print(f"   Launch metadata written: {target_meta}")

    # 4. Write Structured Script Manifest JSON
    target_script = os.path.join(release_dir, "script.json")
    with open(target_script, "w", encoding="utf-8") as f:
        json.dump(ep, f, ensure_ascii=False, indent=2)
    print(f"   Script manifest written: {target_script}")

async def main():
    for ep in EPISODES:
        await package_episode(ep)
    print("\n All 4 Episodes successfully upgraded with Bilingual Teamwork & Natural Tokyo Nanami Voice!")

if __name__ == "__main__":
    asyncio.run(main())
