#!/usr/bin/env python3
"""
TokyoFlow Japanese • English VoiceBank Builder
Synthesizes English natural pedagogical explanations for all scenarios and grammar points.
Saves assets to `TokyoFlow/Resources/Audio/EnglishVoiceBank/` with manifest.
"""

import os
import sys
import json
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), "videogen"))
from voice_engine import synthesize_speech

EN_VOICEBANK_DIR = "TokyoFlow/Resources/Audio/EnglishVoiceBank"
MANIFEST_PATH = os.path.join(EN_VOICEBANK_DIR, "english_voice_manifest.json")

os.makedirs(EN_VOICEBANK_DIR, exist_ok=True)

ENGLISH_EXPLANATIONS = [
    {
        "key": "ep01_breakdown_01",
        "text": "Let's break down this train announcement. 'Mamonaku' means shortly or very soon. 'Ni-ban sen ni' means on platform 2. 'Yamanote-sen uchi-mawari' is the Yamanote inner loop line. And 'mairimasu' is the humble verb for 'coming', used in JR broadcasts to show supreme respect to passengers."
    },
    {
        "key": "ep01_breakdown_02",
        "text": "In this platform safety announcement, 'kiiroi' means yellow, 'tenji burokku' refers to the tactile warning blocks, and 'uchigawa made' means behind the line. 'Osagari kudasai' is the polite imperative form, widely used across Japanese transit for commuter safety."
    },
    {
        "key": "ep02_breakdown_01",
        "text": "This is the most common question at Tokyo convenience stores. If you want your bento heated, answer 'Onegaishimasu' or 'Atatamete kudasai'. If you prefer it as is, simply say 'Daijoubu desu'."
    },
    {
        "key": "ep02_breakdown_02",
        "text": "'Daijoubu desu' is the universal, polite way to decline in Japanese. Combined with a slight head nod, it naturally means 'No thank you, I am fine without a bag'."
    },
    {
        "key": "ep03_breakdown_01",
        "text": "'Toriaezu' means 'for starters' or 'first of all'. In Japanese izakaya pub culture, ordering your first drink immediately upon sitting down helps the kitchen and sets a cheerful mood for the table."
    },
    {
        "key": "ep03_breakdown_02",
        "text": "When ordering yakitori skewers, the staff will always ask if you prefer 'shio' which is salt, or 'tare' which is sweet savory soy glaze. Salt brings out the pure flavor of the meat."
    },
    {
        "key": "ep04_breakdown_01",
        "text": "'Gensaku' is a key shopping term in Akihabara, referring to the original manga or light novel that inspired an anime adaptation. Look for the 'Gensaku' section on the main floor."
    },
    {
        "key": "ep04_breakdown_02",
        "text": "'Tokuten' refers to exclusive store bonus items like acrylic stands, badges, or illustration cards. Always ask if bonus perks are still in stock before making your purchase."
    }
]

async def build_english_voicebank():
    print("🎙️ Building TokyoFlow Studio English VoiceBank...")
    manifest = {}
    
    for item in ENGLISH_EXPLANATIONS:
        key = item["key"]
        text = item["text"]
        out_fn = f"{key}.m4a"
        out_path = os.path.join(EN_VOICEBANK_DIR, out_fn)
        
        await synthesize_speech(text, out_path, lang="en")
        manifest[key] = {
            "file": out_fn,
            "text": text
        }
        print(f"  ✓ English Voice generated: {out_fn}")
        
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    print(f"✨ English VoiceBank complete! Manifest saved to: {MANIFEST_PATH}")

if __name__ == "__main__":
    asyncio.run(build_english_voicebank())
