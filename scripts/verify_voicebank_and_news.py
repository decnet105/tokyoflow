import json
import os
import re

manifest_path = "TokyoFlow/Resources/Audio/VoiceBank/voice_bank_manifest.json"
voicebank_dir = "TokyoFlow/Resources/Audio/VoiceBank"

manifest = json.load(open(manifest_path, "r", encoding="utf-8"))
print(f"Manifest total registered keys: {len(manifest)}")

missing_files = []
for k, v in manifest.items():
    p = os.path.join(voicebank_dir, v)
    if not os.path.exists(p):
        missing_files.append((k, v))

print(f"Missing audio files on disk from manifest: {len(missing_files)}")

# Check KanaItem.swift
kana_swift = open("TokyoFlow/Models/KanaItem.swift", "r", encoding="utf-8").read()
japanese_words = re.findall(r'japanese:\s*"([^"]+)"', kana_swift)
hiraganas = re.findall(r'hiragana:\s*"([^"]+)"', kana_swift)
katakanas = re.findall(r'katakana:\s*"([^"]+)"', kana_swift)

print(f"Kana items found: {len(japanese_words)} words, {len(hiraganas)} hiragana, {len(katakanas)} katakana")

missing_kana = []
for h in set(hiraganas + katakanas):
    if h not in manifest:
        missing_kana.append(h)

print(f"Missing Kana characters: {len(missing_kana)} -> {missing_kana}")

missing_words = []
for w in set(japanese_words):
    clean_w = re.sub(r'[\(（\[【].*?[\)）\]】]', '', w).strip()
    if clean_w not in manifest and w not in manifest:
        missing_words.append((w, clean_w))

print(f"Missing Kana example words: {len(missing_words)}")
if missing_words:
    for orig, clean in missing_words[:15]:
        print(f"   - {orig} (cleaned: {clean})")

# Check News
news_data = json.load(open("TokyoFlow/Resources/daily_news.json", "r", encoding="utf-8"))
missing_news_sentences = []
for article in news_data:
    for sent in article.get("contentSentences", []):
        jp = sent["japanese"]
        if jp not in manifest:
            missing_news_sentences.append(jp)

print(f"Missing News sentences in manifest: {len(missing_news_sentences)}")
