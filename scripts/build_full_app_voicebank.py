import json
import glob
import re
import os
import subprocess
import hashlib

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")

os.makedirs(VOICEBANK_DIR, exist_ok=True)

manifest = {}
if os.path.exists(MANIFEST_PATH):
    try:
        manifest = json.load(open(MANIFEST_PATH, "r", encoding="utf-8"))
    except Exception as e:
        print(f"Warning loading manifest: {e}")

all_phrases = set()

# 1. Load from JSON files
for fpath in glob.glob("TokyoFlow/Resources/Data/*.json"):
    try:
        data = json.load(open(fpath, "r", encoding="utf-8"))
        def extract(obj):
            if isinstance(obj, str):
                if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in obj):
                    all_phrases.add(obj.strip())
            elif isinstance(obj, dict):
                for v in obj.values(): extract(v)
            elif isinstance(obj, list):
                for v in obj: extract(v)
        extract(data)
    except Exception as e:
        print(f"Error parsing {fpath}: {e}")

# 2. Load from Swift files
for fpath in glob.glob("TokyoFlow/**/*.swift", recursive=True):
    try:
        content = open(fpath, "r", encoding="utf-8").read()
        literals = re.findall(r'\"([^\"]+)\"', content)
        for lit in literals:
            if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in lit):
                if len(lit) < 120 and not lit.startswith("http") and not lit.startswith("/"):
                    all_phrases.add(lit.strip())
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

print(f"Found {len(all_phrases)} unique Japanese phrases/words to process.")

def clean_for_speech(text):
    # Remove romaji/parentheses explanation like "いぬ (犬)" -> "いぬ", "えき (駅)" -> "えき"
    cleaned = text
    # Extract before parentheses if Japanese is outside
    m = re.match(r'^([\u3040-\u30ff\u4e00-\u9fffー〜]+)\s*[\(（]', text)
    if m:
        return m.group(1).strip()
    
    # Remove UI symbols, romaji, brackets
    cleaned = re.sub(r'[\(（\[【][^\)）\]】]*[\)）\]】]', '', cleaned)
    cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
    cleaned = re.sub(r'[・…~〜#*・✨🍜🌸🍶💼🎮⚡🔥⭐]+', '', cleaned)
    cleaned = cleaned.strip(' "“”!！?？:：,，。')
    return cleaned if cleaned else text

def get_hash_filename(text):
    h = hashlib.md5(text.encode('utf-8')).hexdigest()[:10]
    # Keep some readable chars if ASCII/Kana
    safe = re.sub(r'[^a-zA-Z0-9_]', '', text)[:8]
    if safe:
        return f"v_{safe}_{h}.m4a"
    return f"v_{h}.m4a"

generated_count = 0
for raw in sorted(all_phrases):
    speech_text = clean_for_speech(raw)
    if not speech_text or not any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in speech_text):
        continue

    # Check if already mapped and file exists
    existing_fn = manifest.get(raw) or manifest.get(speech_text)
    if existing_fn and os.path.exists(os.path.join(VOICEBANK_DIR, existing_fn)):
        manifest[raw] = existing_fn
        manifest[speech_text] = existing_fn
        continue

    filename = get_hash_filename(speech_text)
    out_m4a = os.path.join(VOICEBANK_DIR, filename)
    tmp_aiff = f"/tmp/tmp_{os.getpid()}_{hashlib.md5(raw.encode()).hexdigest()[:8]}.aiff"

    if not os.path.exists(out_m4a):
        try:
            # Use Kyoko (standard Tokyo native Japanese voice) at 170 wpm for clear crisp pronunciation
            subprocess.run(["say", "-v", "Kyoko", "-r", "175", "-o", tmp_aiff, speech_text], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", tmp_aiff, out_m4a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(tmp_aiff):
                os.remove(tmp_aiff)
            generated_count += 1
        except Exception as e:
            if os.path.exists(tmp_aiff):
                os.remove(tmp_aiff)
            continue

    manifest[raw] = filename
    manifest[speech_text] = filename

print(f"Generated {generated_count} new native voice audio files in {VOICEBANK_DIR}.")
print(f"Total manifest mappings: {len(manifest)}")

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("VoiceBank manifest successfully updated!")
