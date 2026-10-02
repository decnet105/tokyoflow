#!/usr/bin/env python3
"""
build_batch2_releases.py
Builds the 2nd Batch of 4 YouTube Micro-Lesson Releases for TokyoFlow Japanese (EP. 05 to EP. 08),
covering all 4 playlist categories (Transit, Kombini/Daily, Dining/Ramen, Shopping/Tax-Free)
strictly following the tokyoflow-video-factory and tokyoflow-thumbnail-factory skill standards.
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

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(res.stdout.strip())

async def build_teamwork_breakdown_audio(cues: list, out_final_path: str, tmp_dir: str) -> dict:
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
                
        if cue.get("is_spotlight", False):
            if spotlight_timings == (9999.0, 9999.0):
                spotlight_timings = (start_t, end_t)
            else:
                spotlight_timings = (spotlight_timings[0], end_t)
                
        seg_files.append(fn)
        current_time += dur + 0.15

    concat_txt = os.path.join(tmp_dir, "cues.txt")
    with open(concat_txt, "w") as f:
        for fn in seg_files:
            f.write(f"file '{os.path.abspath(fn)}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
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
            "cards": card_timings,
            "spotlight": spotlight_timings
        }
    }

def concat_videos_seamless(input_videos: list, final_output_path: str):
    workdir = os.path.dirname(final_output_path)
    concat_txt_path = os.path.join(workdir, "concat_list.txt")
    with open(concat_txt_path, "w") as f:
        for vid in input_videos:
            f.write(f"file '{os.path.abspath(vid)}'\n")

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

BATCH2_EPISODES = [
    # =========================================================================
    # EPISODE 05: CATEGORY 1 - TRANSIT & COMMUTE
    # =========================================================================
    {
        "episode_number": 5,
        "folder_name": "E05-Tokyo_Subway_Rush-v1.0",
        "slug": "tokyo_subway_rush",
        "title": "Tokyo Subway Hacks: Rapid vs Local Trains & Fare Adjustment",
        "yt_title": "Survive the Tokyo Subway!  Rapid vs Local & Fare Adjustment (EP. 05)",
        "category": "Transit & Commute • Tokyo Subway",
        "level": "JLPT N4-N3",
        "district": "Shinjuku & Otemachi ()",
        "cover_src": "/Users/kilvonwu/.gemini/antigravity/brain/05184417-05e5-4849-b75b-23838a5adf09/tokyoflow_thumb_ep05_1790725833742.jpg",
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Train Type Inquiry Drill",
                "spoken_text": "",
                "en": "Is this train a local all-stop or a rapid service?",
                "tip": "Crucial distinction! ' (kakueki)' stops everywhere; ' (kaisoku)' skips smaller stations.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kono", "pos": "Demonstrative", "meaning": "This"},
                    {"orig": "", "kana": "", "romaji": "densha wa", "pos": "Noun + Topic", "meaning": "Train"},
                    {"orig": "", "kana": "", "romaji": "kakueki-teisha desu ka,", "pos": "Noun + Copula Q", "meaning": "Is it a local train,"},
                    {"orig": "", "kana": "", "romaji": "soretomo", "pos": "Conjunction", "meaning": "Or else"},
                    {"orig": "", "kana": "", "romaji": "kaisoku desu ka?", "pos": "Noun + Copula Q", "meaning": "Is it rapid?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Transit Choice Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "kakueki teisha", "pos": "Noun", "meaning": "Local (stops at every station)"},
                    {"orig": "", "kana": "", "romaji": "soretomo", "pos": "Conjunction", "meaning": "Or / alternatively (between choices)"},
                    {"orig": "", "kana": "", "romaji": "kaisoku", "pos": "Noun", "meaning": "Rapid train service"},
                    {"orig": "", "kana": "", "romaji": "densha", "pos": "Noun", "meaning": "Electric train"},
                    {"orig": "", "kana": "", "romaji": "kono", "pos": "Prenoun Adj", "meaning": "This (near speaker)"}
                ],
                "grammar_title": ": AB",
                "grammar_bullets": [
                    ("1. Choice Questions:", "Used when asking someone to choose between alternative options."),
                    ("2. Formulation:", "[Option A]  [Option B] "),
                    ("3. Transit Context:", "Essential on multi-track platforms with express/local services."),
                    ("4. Pro-Tip:", "Abbreviated to ' (kakutei)' in colloquial daily Japanese.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down this essential train choice question."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Noun: local train stopping at every single station.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Conjunction: or else, used between two complete questions.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Noun: rapid service that skips smaller stops.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Noun: electric train.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "This train near us.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Choice questions with soretomo.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Would you like coffee, or tea? Perfect for polite choices.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Fare Adjustment Window Drill",
                "spoken_text": "",
                "en": "I can't exit due to insufficient balance, please adjust my fare.",
                "tip": "When Suica beeps red, go to the Fare Adjustment Machine () or window.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "zandaka-busoku de", "pos": "Noun + Cause", "meaning": "Due to low balance"},
                    {"orig": "", "kana": "", "romaji": "kaisatsu o", "pos": "Noun + Obj", "meaning": "Ticket gate"},
                    {"orig": "", "kana": "", "romaji": "derarenai node,", "pos": "Potential Neg + Reason", "meaning": "Because I can't exit,"},
                    {"orig": "", "kana": "", "romaji": "seisan o", "pos": "Noun + Obj", "meaning": "Fare adjustment"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Fare Adjustment Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "zandaka busoku", "pos": "Compound Noun", "meaning": "Insufficient balance on IC card"},
                    {"orig": "", "kana": "", "romaji": "kaisatsu", "pos": "Noun", "meaning": "Ticket gate / turnstile"},
                    {"orig": "", "kana": "", "romaji": "derarenai", "pos": "Potential Verb (Neg)", "meaning": "Cannot exit (from )"},
                    {"orig": "", "kana": "", "romaji": "node", "pos": "Conjunction", "meaning": "Because / since (objective reason)"},
                    {"orig": "", "kana": "", "romaji": "seisan", "pos": "Noun / Suru-Verb", "meaning": "Fare adjustment / settlement"}
                ],
                "grammar_title": ":  (Objective & Polite Reason)",
                "grammar_bullets": [
                    ("1. Polite Causation:", " sounds softer and more objective than  in service contexts."),
                    ("2. Connection:", "Short form verb/adj +  (e.g. )."),
                    ("3. Station Formula:", "State your issue +  +  for courteous customer assistance."),
                    ("4. Action:", "Station master will tap your card and charge the exact difference.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's examine how to handle ticket gate balance errors."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Compound noun: insufficient card balance.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Noun: ticket gates or turnstiles.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Potential negative verb: unable to leave or exit.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Conjunction: since or because, soft and polite.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Noun: fare adjustment calculation.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Stating reason politely with node.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Because there is no time, please hurry. Node keeps requests refined.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. IC Card Recharge Drill",
                "spoken_text": "Suica",
                "en": "Please charge 1,000 yen onto my Suica card.",
                "tip": "Say '[Amount] ' at ticket counters or convenience stores.",
                "tokens": [
                    {"orig": "Suica", "kana": "", "romaji": "Suica ni", "pos": "Noun + Target", "meaning": "Onto Suica"},
                    {"orig": "", "kana": "", "romaji": "sen-en", "pos": "Number + Currency", "meaning": "1,000 JPY"},
                    {"orig": "", "kana": "", "romaji": "chaaji shite", "pos": "Loanword Verb", "meaning": "Recharge / top up"},
                    {"orig": "", "kana": "", "romaji": "kudasai.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },

    # =========================================================================
    # EPISODE 06: CATEGORY 2 - KOMBINI & DAILY LIFE
    # =========================================================================
    {
        "episode_number": 6,
        "folder_name": "E06-Kombini_Coffee_ATM-v1.0",
        "slug": "kombini_coffee_atm",
        "title": "Tokyo Kombini Hacks: Self-Service Coffee & ATM Shipping",
        "yt_title": "Order Coffee Like a Tokyo Local!  Kombini Machine & ATM Hacks (EP. 06)",
        "category": "Kombini & Daily Life • Register Protocols",
        "level": "JLPT N5-N4",
        "district": "Roppongi ()",
        "cover_src": "/Users/kilvonwu/.gemini/antigravity/brain/05184417-05e5-4849-b75b-23838a5adf09/tokyoflow_thumb_ep06_1790725856366.jpg",
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Fresh Kombini Coffee Order",
                "spoken_text": "",
                "en": "One regular sized iced coffee, please.",
                "tip": "For iced coffee, grab the ice cup from the freezer section first and take it to the register!",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "aisu-koohii no", "pos": "Noun + Part.", "meaning": "Iced coffee's"},
                    {"orig": "", "kana": "", "romaji": "regyuraa-saizu o", "pos": "Noun + Obj", "meaning": "Regular size"},
                    {"orig": "", "kana": "", "romaji": "hitotsu", "pos": "Counter", "meaning": "One item"},
                    {"orig": "", "kana": "", "romaji": "kudasai.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Coffee Ordering Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "aisu koohii", "pos": "Katakana Noun", "meaning": "Iced coffee"},
                    {"orig": "", "kana": "", "romaji": "regyuraa saizu", "pos": "Katakana Noun", "meaning": "Regular size (Small in 7-11)"},
                    {"orig": "", "kana": "", "romaji": "hitotsu", "pos": "Native Counter", "meaning": "One item (general counter)"},
                    {"orig": "", "kana": "", "romaji": "kudasai", "pos": "Polite Request", "meaning": "Please give me"},
                    {"orig": "", "kana": "", "romaji": "hotto", "pos": "Katakana Noun", "meaning": "Hot beverage"}
                ],
                "grammar_title": ": []  [] ",
                "grammar_bullets": [
                    ("1. Standard Ordering Formula:", "[Item]  [Quantity]  — the universal ordering sentence."),
                    ("2. Counter Placement:", "The Japanese counter (, , ) directly precedes ."),
                    ("3. Size Lingo:", "R = Regular (), L = Large ()."),
                    ("4. Self-Service Machine:", "Press the blinking button matching your exact cup size.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down ordering fresh coffee at 7-Eleven and FamilyMart."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Iced coffee, available all year round.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Regular size cup, denoted by letter R.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Native counter for one item.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Please give me.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Hot coffee option.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: The universal ordering formula item plus counter plus kudasai.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Two onigiri please. Simple and effective anywhere in Japan.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Parcel Shipping at Kombini Drill",
                "spoken_text": "",
                "en": "I would like to send a parcel to this address, do you have a shipping slip?",
                "tip": "Yamato Transport () shipping slips are available at the counter ( = prepaid /  = COD).",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "takkyuubin o", "pos": "Noun + Obj", "meaning": "Express parcel delivery"},
                    {"orig": "", "kana": "", "romaji": "kono juusho e", "pos": "Noun + Direction", "meaning": "To this address"},
                    {"orig": "", "kana": "nost", "romaji": "okuritai no desu ga,", "pos": "Desire + Cushion", "meaning": "I'd like to send, so..."},
                    {"orig": "", "kana": "", "romaji": "denpyou wa", "pos": "Noun + Topic", "meaning": "Shipping slip voucher"},
                    {"orig": "", "kana": "", "romaji": "arimasu ka?", "pos": "Verb + Q", "meaning": "Do you have?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Shipping & Logistics Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "takkyuubin", "pos": "Noun", "meaning": "Courier delivery service (Yamato)"},
                    {"orig": "", "kana": "", "romaji": "juusho", "pos": "Noun", "meaning": "Postal address / residence"},
                    {"orig": "", "kana": "", "romaji": "okuritai", "pos": "Tai-form Verb", "meaning": "Want to send (from )"},
                    {"orig": "", "kana": "", "romaji": "no desu ga", "pos": "Polite Cushion", "meaning": "I'd like to, but... (soft opener)"},
                    {"orig": "", "kana": "", "romaji": "denpyou", "pos": "Noun", "meaning": "Waybill / delivery form slip"}
                ],
                "grammar_title": ":  (Soft Topic Opener)",
                "grammar_bullets": [
                    ("1. Polite Conversation Opener:", "Adding  softens requests and explains background smoothly."),
                    ("2. Formulation:", "Verb Tai-Stem +  (e.g. )."),
                    ("3. Cultural Nuance:", "Japanese people rarely state demands directly;  invites the staff to assist."),
                    ("4. Kombini Service:", "Staff will hand you a ballpoint pen and adhesive pouch.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's analyze how to send luggage or packages from convenience stores."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Courier parcel service, widely handled at kombini counters.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Destination postal address.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Desire form: I want to send.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Polite conversational cushion phrase.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "The shipping waybill slip.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Softening requests with tai no desu ga.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "I would like to store my luggage. Essential for hotel check-ins.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Utensil Request Drill",
                "spoken_text": "",
                "en": "Please include chopsticks and a straw.",
                "tip": "Staff may ask '' (Would you like chopsticks?).",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "o-hashi to", "pos": "Noun + Conj", "meaning": "Chopsticks and"},
                    {"orig": "", "kana": "", "romaji": "sutoroo o", "pos": "Noun + Obj", "meaning": "Straw"},
                    {"orig": "", "kana": "", "romaji": "hitotsu", "pos": "Counter", "meaning": "One each"},
                    {"orig": "", "kana": "", "romaji": "tsukete kudasai.", "pos": "Polite Request", "meaning": "Please attach/include"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },

    # =========================================================================
    # EPISODE 07: CATEGORY 3 - TOKYO DINING & STREET FOOD
    # =========================================================================
    {
        "episode_number": 7,
        "folder_name": "E07-Ramen_Ticket_Vending-v1.0",
        "slug": "ramen_ticket_vending",
        "title": "Tokyo Ramen Mastery: Ticket Machine & Custom Broth Orders",
        "yt_title": "Order Ramen Like a Pro in Tokyo!  Ticket Machine & Broth Hacks (EP. 07)",
        "category": "Tokyo Dining • Ramen Culture",
        "level": "JLPT N4-N3",
        "district": "Ikebukuro ()",
        "cover_src": "/Users/kilvonwu/.gemini/antigravity/brain/05184417-05e5-4849-b75b-23838a5adf09/tokyoflow_thumb_ep07_1790725937448.jpg",
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Custom Ramen Broth & Noodle Call",
                "spoken_text": "",
                "en": "Firm noodles, rich broth flavor, and light on the oil please.",
                "tip": "The sacred Iekei () ramen trinity:  (Firmness),  (Flavor),  (Oil).",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "men katame,", "pos": "Noun + Suffix", "meaning": "Noodles firm,"},
                    {"orig": "", "kana": "", "romaji": "aji koime,", "pos": "Noun + Suffix", "meaning": "Flavor rich,"},
                    {"orig": "", "kana": "", "romaji": "abura sukuname de", "pos": "Noun + Suffix + Part", "meaning": "Oil on the light side,"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Ramen Customization Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "men", "pos": "Noun", "meaning": "Noodles"},
                    {"orig": "", "kana": "", "romaji": "katame", "pos": "Suffix / Adj", "meaning": "Firm / al dente (from )"},
                    {"orig": "", "kana": "", "romaji": "aji", "pos": "Noun", "meaning": "Taste / seasoning richness"},
                    {"orig": "", "kana": "", "romaji": "koime", "pos": "Suffix / Adj", "meaning": "Strong / rich flavor (from )"},
                    {"orig": "", "kana": "", "romaji": "sukuname", "pos": "Suffix / Adj", "meaning": "Less / light amount (from )"}
                ],
                "grammar_title": ":  (Slightly / On the ... Side)",
                "grammar_bullets": [
                    ("1. Degree Modifier:", "Attaching  to adjective stems means 'somewhat' or 'on the ... side'."),
                    ("2. Custom Combinations:", " (firmer),  (softer),  (extra),  (less)."),
                    ("3. Counter Manners:", "Call out your preferences immediately upon handing over your ticket."),
                    ("4. Tokyo Standard:", "Most locals choose '' (men katame) so noodles don't get soggy.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's decode the famous ramen customization formula in Tokyo."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Noun: ramen noodles.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Adjective suffix: firm or al dente.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Noun: broth flavor intensity.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Rich, concentrated savory flavor.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Lighter quantity.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: The degree suffix me.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Large rice and extra scallions please. Me customizes your meal flawlessly.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Noodle Refill Call (Kaedama)",
                "spoken_text": "",
                "en": "Excuse me, one extra noodle refill please.",
                "tip": "At Tonkotsu ramen shops (e.g. Ichiran, Ippudo), order Kaedama before your soup gets cold!",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "sumimasen,", "pos": "Interjection", "meaning": "Excuse me,"},
                    {"orig": "", "kana": "", "romaji": "kaedama o", "pos": "Noun + Obj", "meaning": "Noodle refill"},
                    {"orig": "", "kana": "", "romaji": "hitotama", "pos": "Counter", "meaning": "One serving / ball"},
                    {"orig": "", "kana": "", "romaji": "tsuika de", "pos": "Noun + Manner", "meaning": "As an addition"},
                    {"orig": "", "kana": "", "romaji": "onegaishimasu.", "pos": "Polite Request", "meaning": "Please"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Kaedama & Refills Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "kaedama", "pos": "Compound Noun", "meaning": "Extra serving of noodles added to leftover soup"},
                    {"orig": "", "kana": "", "romaji": "hitotama", "pos": "Food Counter", "meaning": "One noodle portion ball"},
                    {"orig": "", "kana": "", "romaji": "tsuika", "pos": "Noun / Suru-Verb", "meaning": "Addition / supplement"},
                    {"orig": "", "kana": "", "romaji": "sumimasen", "pos": "Polite Call", "meaning": "Excuse me (to get attention)"},
                    {"orig": "", "kana": "", "romaji": "suupu", "pos": "Noun", "meaning": "Ramen broth"}
                ],
                "grammar_title": ": [] ",
                "grammar_bullets": [
                    ("1. Adding Extra Portions:", "Use [Item]  to add toppings or side dishes."),
                    ("2. Counter for Noodles:", "Noodles are counted as  (hitotama),  (futatama), or  (hantama = half)."),
                    ("3. Cultural Golden Rule:", "Do not drink all your broth if you intend to order a Kaedama refill!"),
                    ("4. Payment:", "Pay with coin on the counter or hand over a pre-bought ticket.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down ordering noodle refills at the counter."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "The famous Japanese term for extra noodle portions.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Counter for one full serving of ramen noodles.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Noun: addition or extra order.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Universal staff call.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Broth or soup base.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Requesting extra items with tsuika de.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Please add a seasoned egg as an extra topping. Perfect for customization.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Paper Bib Request Drill",
                "spoken_text": "",
                "en": "Could I please get a paper bib?",
                "tip": "Ramen broth splatters easily on clothes. Paper bibs () are free upon request!",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kami-epuron o", "pos": "Noun + Obj", "meaning": "Paper bib / apron"},
                    {"orig": "", "kana": "", "romaji": "ichi-mai", "pos": "Flat Counter", "meaning": "One flat sheet"},
                    {"orig": "", "kana": "", "romaji": "itadakemasu ka?", "pos": "Polite Potential", "meaning": "Could I receive?"}
                ]
            },
            {
                "type": "outro",
                "chapter": "06. Subscribe & Download",
                "spoken_text": "TokyoFlow"
            }
        ]
    },

    # =========================================================================
    # EPISODE 08: CATEGORY 4 - SHOPPING, ANIME & TAX-FREE
    # =========================================================================
    {
        "episode_number": 8,
        "folder_name": "E08-Ginza_TaxFree_Shopping-v1.0",
        "slug": "ginza_taxfree_shopping",
        "title": "Ginza Fashion Shopping: Sizing, Fitting Room & Tax-Free Refund",
        "yt_title": "Shop Like a Tokyo Stylist!  Fitting Room & Tax-Free Hacks (EP. 08)",
        "category": "Shopping & Tax-Free • Department Store",
        "level": "JLPT N4-N3",
        "district": "Ginza ()",
        "cover_src": "/Users/kilvonwu/.gemini/antigravity/brain/05184417-05e5-4849-b75b-23838a5adf09/tokyoflow_thumb_ep08_1790725951206.jpg",
        "slides": [
            {
                "type": "follow_along",
                "chapter": "01. Fitting Room Permission Drill",
                "spoken_text": "",
                "en": "May I try on this jacket?",
                "tip": "Always ask before entering the fitting room (). Remember to remove shoes at the step!",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kono", "pos": "Demonstrative", "meaning": "This"},
                    {"orig": "", "kana": "", "romaji": "jaketto o", "pos": "Noun + Obj", "meaning": "Jacket"},
                    {"orig": "", "kana": "", "romaji": "shichaku shite mo", "pos": "Te-form Verb", "meaning": "Even if I try on"},
                    {"orig": "", "kana": "", "romaji": "ii desu ka?", "pos": "Permission Q", "meaning": "Is it fine?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "02. Fitting Room Permission Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "shichaku", "pos": "Noun / Suru-Verb", "meaning": "Trying on clothes"},
                    {"orig": "", "kana": "", "romaji": "jaketto", "pos": "Katakana Noun", "meaning": "Jacket / blazer"},
                    {"orig": "", "kana": "", "romaji": "te mo ii", "pos": "Permission Formula", "meaning": "Is allowed / may do"},
                    {"orig": "", "kana": "", "romaji": "shichakushitsu", "pos": "Compound Noun", "meaning": "Fitting room"},
                    {"orig": "", "kana": "", "romaji": "saizu", "pos": "Noun", "meaning": "Size"}
                ],
                "grammar_title": ":  (Asking Permission Politely)",
                "grammar_bullets": [
                    ("1. Polite Permission:", "Verb Te-form +  is the universal polite permission formula."),
                    ("2. Formation:", " →  → "),
                    ("3. Shopping Etiquette:", "Staff will guide you to a numbered booth and provide a face cover ()."),
                    ("4. Inquiries:", "After trying on, say '' (I'll take this) or '' (I'll think about it).")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's analyze asking to try on clothes at Japanese fashion stores."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "Noun: trying on clothing garments.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Jacket or outerwear.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Permission formula: is it okay to do.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "The fitting room booth.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Garment sizing.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Asking polite permission with te mo ii desu ka.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "May I take a photo? Indispensable formula everywhere in Tokyo.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "03. Size Comparison Drill",
                "spoken_text": "",
                "en": "Do you have one size larger than this?",
                "tip": "Japanese sizing runs smaller than US/EU sizes. Use '' (one size up) or '' (one size down).",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "kore no", "pos": "Pronoun + Part.", "meaning": "This one's"},
                    {"orig": "", "kana": "", "romaji": "wan-saizu", "pos": "Katakana Noun", "meaning": "One size"},
                    {"orig": "", "kana": "", "romaji": "ookii mono wa", "pos": "Adj + Placeholder", "meaning": "Larger one (topic)"},
                    {"orig": "", "kana": "", "romaji": "arimasu ka?", "pos": "Verb + Q", "meaning": "Is there available?"}
                ]
            },
            {
                "type": "breakdown",
                "chapter": "04. Sizing & Alternatives Breakdown",
                "sentence_ja": "",
                "vocab": [
                    {"orig": "", "kana": "", "romaji": "wan saizu", "pos": "Katakana Noun", "meaning": "One single size increment"},
                    {"orig": "", "kana": "", "romaji": "ookii", "pos": "I-Adjective", "meaning": "Large / big in dimensions"},
                    {"orig": "", "kana": "", "romaji": "mono", "pos": "Noun Placeholder", "meaning": "Item / tangible object"},
                    {"orig": "", "kana": "", "romaji": "chiisai", "pos": "I-Adjective", "meaning": "Small / tight in dimensions"},
                    {"orig": "", "kana": "", "romaji": "irochigai", "pos": "Compound Noun", "meaning": "Different color variant"}
                ],
                "grammar_title": ": [] +  (Object Placeholder)",
                "grammar_bullets": [
                    ("1. Descriptive Placeholder:", "Connecting [I-Adj] +  acts as 'the [adj] one' (e.g.  = the bigger one)."),
                    ("2. Color Variant Formula:", " (Do you have this in a different color?)."),
                    ("3. Staff Response:", "Staff will check the stockroom: '' (I will check inventory)."),
                    ("4. Pro-Tip:", "Use 'M' (Emu saizu) or 'L' (Eru saizu) for specific letters.")
                ],
                "teamwork_cues": [
                    {"speaker": "en", "text": "Let's break down asking for different sizes and colors while shopping."},
                    {"speaker": "ja", "text": "", "card_idx": 0},
                    {"speaker": "en", "text": "One size tier difference.", "card_idx": 0},
                    {"speaker": "ja", "text": "", "card_idx": 1},
                    {"speaker": "en", "text": "Adjective: large or spacious.", "card_idx": 1},
                    {"speaker": "ja", "text": "", "card_idx": 2},
                    {"speaker": "en", "text": "Noun placeholder for item or object.", "card_idx": 2},
                    {"speaker": "ja", "text": "", "card_idx": 3},
                    {"speaker": "en", "text": "Small or tighter fitting.", "card_idx": 3},
                    {"speaker": "ja", "text": "", "card_idx": 4},
                    {"speaker": "en", "text": "Different color variation.", "card_idx": 4},
                    {"speaker": "en", "text": "Grammar spotlight: Object placeholder with mono.", "is_spotlight": True},
                    {"speaker": "ja", "text": "", "is_spotlight": True},
                    {"speaker": "en", "text": "Do you have a slightly cheaper one? Smooth and polite bargaining.", "is_spotlight": True}
                ]
            },
            {
                "type": "follow_along",
                "chapter": "05. Tax-Free Counter Finding Drill",
                "spoken_text": "",
                "en": "On which floor is the tax-free refund counter located?",
                "tip": "In major department stores (Matsuya, Isetan, Parco), the Tax-Free counter is often in the basement or top floor.",
                "tokens": [
                    {"orig": "", "kana": "", "romaji": "menzei-kauntaa wa", "pos": "Compound Noun + Topic", "meaning": "Tax-free counter"},
                    {"orig": "", "kana": "", "romaji": "dono furoa ni", "pos": "Question + Part", "meaning": "On which floor"},
                    {"orig": "", "kana": "", "romaji": "arimasu ka?", "pos": "Verb + Q", "meaning": "Is located?"}
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
    print(f" Packaging {folder_name} (EP. {ep_num:02d})")
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

    # 2. Copy the authentic High-CTR Thumbnail
    target_thumb = os.path.join(release_dir, "thumbnail.jpg")
    cover_src = ep["cover_src"]
    shutil.copyfile(cover_src, target_thumb)
    
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
    print(" Starting Batch 2 Production (EP. 05 to EP. 08)...")
    for ep in BATCH2_EPISODES:
        await package_episode(ep)
    print("\n Batch 2 Production Complete! 4 New Releases successfully assembled across 4 Playlist Categories!")

if __name__ == "__main__":
    asyncio.run(main())
