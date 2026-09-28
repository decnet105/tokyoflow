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

def extract_japanese(obj):
    if isinstance(obj, str):
        s = obj.strip()
        if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in s):
            all_phrases.add(s)
    elif isinstance(obj, dict):
        for v in obj.values():
            extract_japanese(v)
    elif isinstance(obj, list):
        for v in obj:
            extract_japanese(v)

# 1. Load from all JSON files in Resources
for fpath in glob.glob("TokyoFlow/Resources/*.json"):
    if "voice_bank_manifest" in fpath:
        continue
    try:
        data = json.load(open(fpath, "r", encoding="utf-8"))
        extract_japanese(data)
        print(f"Loaded texts from {fpath}")
    except Exception as e:
        print(f"Error parsing {fpath}: {e}")

# 2. Load from Swift files (especially KanaItem.swift, DojoBattles, etc.)
for fpath in glob.glob("TokyoFlow/**/*.swift", recursive=True):
    try:
        content = open(fpath, "r", encoding="utf-8").read()
        literals = re.findall(r'"([^"\n]+)"', content)
        for lit in literals:
            s = lit.strip()
            if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in s):
                if len(s) < 140 and not s.startswith("http") and not s.startswith("/") and not s.startswith("com."):
                    all_phrases.add(s)
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

print(f"Total unique Japanese phrases/words found across entire app: {len(all_phrases)}")

def clean_for_speech(text):
    # Remove ruby markup like {渋谷} in まもなく、２ばんせん{番線}に
    cleaned = re.sub(r'\{[^\}]+\}', '', text)
    
    # Check if format is "いぬ (犬)" or "ありがとう (Thank you)"
    m = re.match(r'^([\u3040-\u30ff\u4e00-\u9fffー〜]+)\s*[\(（]', cleaned)
    if m:
        return m.group(1).strip()
    
    # Remove English translations in parentheses
    cleaned = re.sub(r'[\(（\[【][^\)）\]】]*[\)）\]】]', '', cleaned)
    cleaned = re.sub(r'[\r\n\t]+', ' ', cleaned)
    cleaned = re.sub(r'[・…~〜#*・✨🍜🌸🍶💼🎮⚡🔥⭐🎌🎙️🔊✅⚠️❌]+', ' ', cleaned)
    cleaned = cleaned.strip(' "“”!！?？:：,，。 ')
    return cleaned if cleaned else text

def get_hash_filename(text):
    h = hashlib.md5(text.encode('utf-8')).hexdigest()[:10]
    safe = re.sub(r'[^a-zA-Z0-9_]', '', text)[:8]
    if safe:
        return f"v_{safe}_{h}.m4a"
    return f"v_{h}.m4a"

generated_count = 0
existing_count = 0

for raw in sorted(all_phrases):
    speech_text = clean_for_speech(raw)
    if not speech_text or not any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in speech_text):
        continue

    # Check if raw or speech_text already mapped and exists on disk
    mapped_fn = manifest.get(raw) or manifest.get(speech_text)
    if mapped_fn and os.path.exists(os.path.join(VOICEBANK_DIR, mapped_fn)):
        manifest[raw] = mapped_fn
        manifest[speech_text] = mapped_fn
        existing_count += 1
        continue

    filename = get_hash_filename(speech_text)
    out_m4a = os.path.join(VOICEBANK_DIR, filename)
    tmp_aiff = f"/tmp/tmp_{os.getpid()}_{hashlib.md5(raw.encode()).hexdigest()[:8]}.aiff"

    if not os.path.exists(out_m4a):
        try:
            # Kyoko (standard NHK Tokyo accent) at natural 175 wpm
            subprocess.run(["say", "-v", "Kyoko", "-r", "175", "-o", tmp_aiff, speech_text], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", tmp_aiff, out_m4a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(tmp_aiff):
                os.remove(tmp_aiff)
            generated_count += 1
        except Exception as e:
            print(f"Error generating audio for '{speech_text}': {e}")
            continue

    manifest[raw] = filename
    manifest[speech_text] = filename

# Save updated manifest
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"✅ VoiceBank build complete: {generated_count} newly generated, {existing_count} reused. Total manifest keys: {len(manifest)}")
