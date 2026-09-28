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

# STEP 1: CLEAN UP BAD MAPPINGS
# Any multi-character word or word with parentheses that was mapped to a single-letter kana_xx.m4a must be deleted from manifest so it gets generated properly!
cleaned_bad = 0
for k, v in list(manifest.items()):
    if v.startswith("kana_") and (len(k) > 2 or "(" in k or "（" in k or any(c in k for c in "たのしいありがとうおはよう")):
        # Only keep single-letter kana in kana_xx.m4a
        if k not in ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
                     "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
                     "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
                     "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り",
                     "る", "れ", "ろ", "わ", "を", "ん", "が", "ぎ", "ぐ", "げ",
                     "ご", "ざ", "じ", "ず", "ぜ", "ぞ", "だ", "ぢ", "づ", "で",
                     "ど", "ば", "び", "ぶ", "べ", "ぼ", "ぱ", "ぴ", "ぷ", "ぺ",
                     "ぽ", "きゃ", "きゅ", "きょ", "しゃ", "しゅ", "しょ", "ちゃ",
                     "ちゅ", "ちょ", "にゃ", "にゅ", "にょ", "ひゃ", "ひゅ", "ひょ",
                     "みゃ", "みゅ", "みょ", "りゃ", "りゅ", "りょ", "ぎゃ", "ぎゅ",
                     "ぎょ", "じゃ", "じゅ", "じょ", "びゃ", "びゅ", "びょ", "ぴゃ",
                     "ぴゅ", "ぴょ", "ア", "イ", "ウ", "エ", "オ", "カ", "キ",
                     "ク", "ケ", "コ", "サ", "シ", "ス", "セ", "ソ", "タ", "チ",
                     "ツ", "テ", "ト", "ナ", "ニ", "ヌ", "ネ", "ノ", "ハ", "ヒ",
                     "フ", "ヘ", "ホ", "マ", "ミ", "ム", "メ", "モ", "ヤ", "ユ",
                     "ヨ", "ラ", "リ", "ル", "レ", "ロ", "ワ", "ヲ", "ン"]:
            del manifest[k]
            cleaned_bad += 1

print(f"Purged {cleaned_bad} incorrect single-letter kana mappings for full words.")

# STEP 2: PARSE ALL KANA WORDS ACCURATELY FROM KanaItem.swift
kana_swift_path = "TokyoFlow/Models/KanaItem.swift"
kana_swift = open(kana_swift_path, "r", encoding="utf-8").read()

# Match: KanaExampleWord(japanese: "たのしい (楽しい)", romaji: "tanoshii", english: "...")
kana_words_raw = re.findall(r'KanaExampleWord\(\s*japanese:\s*"([^"]+)",\s*romaji:\s*"([^"]+)"', kana_swift)
print(f"Extracted {len(kana_words_raw)} Kana example words from KanaItem.swift")

# STEP 3: EXTRACT ALL TEXT FROM ALL JSON RESOURCES
all_items_to_process = [] # list of (lookup_keys, speech_text, prefix_name)

# 3.1 Kana example words
for ja, ro in kana_words_raw:
    # ja could be "たのしい (楽しい)" or "あさ (朝)" or "ありがとう"
    # Extract primary kana and kanji inside parentheses
    m = re.match(r'^([^\(（\s]+)\s*[\(（]([^\)）]+)[\)）]', ja)
    keys = [ja, ro, ro.lower()]
    if m:
        primary_kana = m.group(1).strip()
        kanji_in_paren = m.group(2).strip()
        speech = primary_kana
        keys.extend([primary_kana, kanji_in_paren])
    else:
        speech = ja.strip()
        keys.append(speech)
    all_items_to_process.append((keys, speech, f"kw_{ro[:6]}"))

# 3.2 Kana letters themselves
kana_items = re.findall(r'KanaItem\(\s*id:\s*"([^"]+)",\s*hiragana:\s*"([^"]+)",\s*katakana:\s*"([^"]+)",\s*romaji:\s*"([^"]+)"', kana_swift)
for kid, hira, kata, rom in kana_items:
    keys = [hira, kata, rom, rom.lower(), f"kana_{kid}"]
    all_items_to_process.append((keys, hira, f"kana_{kid}"))

# 3.3 All JSON resources
for fpath in glob.glob("TokyoFlow/Resources/*.json"):
    if "voice_bank_manifest" in fpath:
        continue
    try:
        data = json.load(open(fpath, "r", encoding="utf-8"))
        def rec_extract(obj):
            if isinstance(obj, str):
                s = obj.strip()
                if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in s):
                    # Clean speech text
                    speech = re.sub(r'\{[^\}]+\}', '', s) # ruby
                    m = re.match(r'^([\u3040-\u30ff\u4e00-\u9fffー〜]+)\s*[\(（]', speech)
                    if m:
                        speech = m.group(1).strip()
                    speech = re.sub(r'[\(（\[【][^\)）\]】]*[\)）\]】]', '', speech)
                    speech = re.sub(r'[・…~〜#*・✨🍜🌸🍶💼🎮⚡🔥⭐🎌🎙️🔊✅⚠️❌]+', ' ', speech)
                    speech = speech.strip(' "“”!！?？:：,，。 ')
                    if speech and any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in speech):
                        all_items_to_process.append(([s, speech], speech, "item"))
            elif isinstance(obj, dict):
                for v in obj.values(): rec_extract(v)
            elif isinstance(obj, list):
                for v in obj: rec_extract(v)
        rec_extract(data)
    except Exception as e:
        print(f"Error loading {fpath}: {e}")

# 3.4 All Swift files
for fpath in glob.glob("TokyoFlow/**/*.swift", recursive=True):
    try:
        content = open(fpath, "r", encoding="utf-8").read()
        literals = re.findall(r'"([^"\n]+)"', content)
        for lit in literals:
            s = lit.strip()
            if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in s):
                if len(s) < 140 and not s.startswith("http") and not s.startswith("/") and not s.startswith("com."):
                    speech = re.sub(r'\{[^\}]+\}', '', s)
                    speech = re.sub(r'[\(（\[【][^\)）\]】]*[\)）\]】]', '', speech)
                    speech = re.sub(r'[・…~〜#*・✨🍜🌸🍶💼🎮⚡🔥⭐🎌🎙️🔊✅⚠️❌]+', ' ', speech)
                    speech = speech.strip(' "“”!！?？:：,，。 ')
                    if speech and any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in speech):
                        all_items_to_process.append(([s, speech], speech, "swift"))
    except Exception as e:
        print(f"Error scanning {fpath}: {e}")

print(f"Total entries queued for generation: {len(all_items_to_process)}")

def get_hash_filename(speech_text, prefix):
    h = hashlib.md5(speech_text.encode('utf-8')).hexdigest()[:10]
    safe = re.sub(r'[^a-zA-Z0-9_]', '', prefix)[:8]
    if safe:
        return f"{safe}_{h}.m4a"
    return f"v_{h}.m4a"

new_count = 0
reused_count = 0

for keys, speech, prefix in all_items_to_process:
    if not speech or not any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff' for c in speech):
        continue

    # Check if speech already has a valid file
    existing_fn = manifest.get(speech)
    if existing_fn and os.path.exists(os.path.join(VOICEBANK_DIR, existing_fn)):
        # Make sure it's not a single-letter file for a multi-letter word
        if not (existing_fn.startswith("kana_") and len(speech) > 2):
            for k in keys:
                manifest[k] = existing_fn
            reused_count += 1
            continue

    fn = get_hash_filename(speech, prefix)
    out_m4a = os.path.join(VOICEBANK_DIR, fn)
    tmp_aiff = f"/tmp/tmp_{os.getpid()}_{hashlib.md5(speech.encode()).hexdigest()[:8]}.aiff"

    if not os.path.exists(out_m4a):
        try:
            # Kyoko at standard 175 wpm
            subprocess.run(["say", "-v", "Kyoko", "-r", "175", "-o", tmp_aiff, speech], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", tmp_aiff, out_m4a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(tmp_aiff):
                os.remove(tmp_aiff)
            new_count += 1
        except Exception as e:
            print(f"Error generating audio for '{speech}': {e}")
            continue

    for k in keys:
        manifest[k] = fn

# Save manifest
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n🎉 FULL VOICEBANK GENERATION COMPLETE!")
print(f"  - Newly generated: {new_count}")
print(f"  - Reused existing: {reused_count}")
print(f"  - Total active manifest keys: {len(manifest)}")

# Test Tanoshii explicitly
print(f"\nVerification of 'tanoshii' keys:")
for tk in ["たのしい (楽しい)", "たのしい", "楽しい", "tanoshii"]:
    fn = manifest.get(tk)
    exists = os.path.exists(os.path.join(VOICEBANK_DIR, fn)) if fn else False
    print(f"  '{tk}' -> {fn} (File exists: {exists})")
