import json
import os
import re
import subprocess
import hashlib

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")

manifest = json.load(open(MANIFEST_PATH, "r", encoding="utf-8"))

kana_swift_path = "TokyoFlow/Models/KanaItem.swift"
kana_swift = open(kana_swift_path, "r", encoding="utf-8").read()

# Extract all Kana example words
kana_words_raw = re.findall(r'KanaExampleWord\(\s*japanese:\s*"([^"]+)",\s*romaji:\s*"([^"]+)"', kana_swift)
print(f"Total Kana example words to ensure 100% dedicated audio for: {len(kana_words_raw)}")

fixed_count = 0
for ja, ro in kana_words_raw:
    # ja could be "えび (海老)", "かさ (傘)", "外国 (がいこく)", etc.
    m = re.match(r'^([^\(（\s]+)\s*[\(（]([^\)）]+)[\)）]', ja)
    keys = [ja, ro, ro.lower()]
    if m:
        p1 = m.group(1).strip()
        p2 = m.group(2).strip()
        # If p1 is Kanji like "外国", and p2 is Kana "がいこく", speech is "がいこく" or "外国" (Kyoko reads 外国 as がいこく)
        speech = p1
        keys.extend([p1, p2])
    else:
        speech = ja.strip()
        keys.append(speech)

    # Check if currently mapped to kana_
    curr_fn = manifest.get(ja)
    needs_rebuild = False
    if not curr_fn or curr_fn.startswith("kana_") or not os.path.exists(os.path.join(VOICEBANK_DIR, curr_fn)):
        needs_rebuild = True

    if needs_rebuild:
        h = hashlib.md5(speech.encode('utf-8')).hexdigest()[:10]
        safe_ro = re.sub(r'[^a-zA-Z0-9_]', '', ro)[:8]
        fn = f"word_{safe_ro}_{h}.m4a"
        out_m4a = os.path.join(VOICEBANK_DIR, fn)
        tmp_aiff = f"/tmp/tmp_{os.getpid()}_{hashlib.md5(speech.encode()).hexdigest()[:8]}.aiff"

        try:
            # Generate pure natural Tokyo speech
            subprocess.run(["say", "-v", "Kyoko", "-r", "175", "-o", tmp_aiff, speech], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", tmp_aiff, out_m4a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(tmp_aiff):
                os.remove(tmp_aiff)
            fixed_count += 1
            print(f"  Fixed audio for: '{ja}' (speech: '{speech}') -> {fn}")
        except Exception as e:
            print(f"Error generating audio for '{speech}': {e}")
            continue

        for k in keys:
            manifest[k] = fn

# Save manifest
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"\n✅ Fixed {fixed_count} words! Manifest updated.")
