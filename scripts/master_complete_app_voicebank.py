import asyncio
import os
import re
import json
import hashlib
import subprocess
import edge_tts
import time
import glob

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
VOICE = "ja-JP-NanamiNeural"

os.makedirs(VOICEBANK_DIR, exist_ok=True)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Collect all Japanese strings from resources and codebase
jp_kana_regex = re.compile(r'[\u3040-\u30ff]')
jp_any_regex = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff]')

speech_targets = set()

# 1. jlpt_grammar.json
if os.path.exists("TokyoFlow/Resources/jlpt_grammar.json"):
    with open("TokyoFlow/Resources/jlpt_grammar.json") as f:
        grammars = json.load(f)
    for g in grammars:
        speech_targets.add(g["title"])
        for part in g["title"].replace("〜", "").replace("~", "").split("/"):
            if part.strip(): speech_targets.add(part.strip())
        for sent in g.get("sentences", []):
            speech_targets.add(sent["japanese"])
            speech_targets.add(sent["audioKey"])
        if g.get("quiz"):
            speech_targets.add(g["quiz"]["question"])
            for opt in g["quiz"]["options"]:
                speech_targets.add(opt)

# 2. jlpt_dictionary.json
if os.path.exists("TokyoFlow/Resources/jlpt_dictionary.json"):
    with open("TokyoFlow/Resources/jlpt_dictionary.json") as f:
        words = json.load(f)
    for w in words:
        if w.get("kanji"): speech_targets.add(w["kanji"])
        if w.get("reading"): speech_targets.add(w["reading"])
        if w.get("exampleJa"): speech_targets.add(w["exampleJa"])
        if w.get("collocation"):
            for c in w["collocation"].split("/"):
                if c.strip(): speech_targets.add(c.strip())

# 3. scenarios.json
if os.path.exists("TokyoFlow/Resources/scenarios.json"):
    with open("TokyoFlow/Resources/scenarios.json") as f:
        scenarios = json.load(f)
    for sc in scenarios:
        for d in sc.get("dialogue", []):
            if d.get("japanese"): speech_targets.add(d["japanese"])
        for v in sc.get("keyVocabulary", []):
            if v.get("japanese"): speech_targets.add(v["japanese"])
            if v.get("reading"): speech_targets.add(v["reading"])

# 4. announcements.json
if os.path.exists("TokyoFlow/Resources/announcements.json"):
    with open("TokyoFlow/Resources/announcements.json") as f:
        announcements = json.load(f)
    for ann in announcements:
        if ann.get("japanese"): speech_targets.add(ann["japanese"])
        if ann.get("listeningQuiz"):
            for opt in ann["listeningQuiz"].get("options", []):
                speech_targets.add(opt)

# 5. dojo_battles.json
if os.path.exists("TokyoFlow/Resources/dojo_battles.json"):
    with open("TokyoFlow/Resources/dojo_battles.json") as f:
        battles = json.load(f)
    for b in battles:
        if b.get("ninjaComboPhrase"): speech_targets.add(b["ninjaComboPhrase"])
        for r in b.get("rounds", []):
            if r.get("clerkPrompt"): speech_targets.add(r["clerkPrompt"])
            for opt in r.get("options", []):
                if opt.get("text"): speech_targets.add(opt["text"])

# 6. manga_lessons.json
if os.path.exists("TokyoFlow/Resources/manga_lessons.json"):
    with open("TokyoFlow/Resources/manga_lessons.json") as f:
        mangas = json.load(f)
    for m in mangas:
        for p in m.get("panels", []):
            if p.get("japanese"): speech_targets.add(p["japanese"])
            if p.get("soundEffect"): speech_targets.add(p["soundEffect"])

# 7. daily_news.json
if os.path.exists("TokyoFlow/Resources/daily_news.json"):
    with open("TokyoFlow/Resources/daily_news.json") as f:
        news = json.load(f)
    for n in news:
        if n.get("title"): speech_targets.add(n["title"])
        for s in n.get("contentSentences", []):
            if s.get("japanese"): speech_targets.add(s["japanese"])
        for v in n.get("vocabulary", []):
            if v.get("word"): speech_targets.add(v["word"])
            if v.get("reading"): speech_targets.add(v["reading"])

# 8. Scan Swift files for all Japanese phrases
for sf in glob.glob("TokyoFlow/**/*.swift", recursive=True):
    with open(sf, "r", encoding="utf-8") as f:
        content = f.read()
    # Find all string literals containing Japanese characters
    for match in re.findall(r'\"([^\"]*[\u3040-\u30ff\u4e00-\u9fff][^\"]*)\"', content):
        clean_match = match.strip()
        if len(clean_match) >= 1 and not clean_match.startswith("http"):
            speech_targets.add(clean_match)

# Clean and normalize text items
def clean_for_speech(text):
    # Remove grammar brackets like 〜 or ~
    t = text.replace("〜", "").replace("~", "").strip()
    # If it contains multiple options separated by /, take the first or full
    return t

items_to_generate = []
for text in speech_targets:
    raw = text.strip()
    if not raw: continue
    
    # Check if already present in manifest
    clean = clean_for_speech(raw)
    norm = re.sub(r'[？?！!。、…〜~「」()（）\[\]【】\s]', '', raw)
    
    if raw in manifest or clean in manifest or norm in manifest:
        # Already covered
        continue
    
    # Generate unique filename hash
    h = hashlib.md5(raw.encode('utf-8')).hexdigest()[:10]
    filename = f"v_app_{h}.m4a"
    items_to_generate.append((raw, clean if clean else raw, filename))

print(f"🎯 Total new speech items to generate: {len(items_to_generate)}")

sem = asyncio.Semaphore(12)
completed = 0
total = len(items_to_generate)

async def generate_audio(raw_key, text_to_speak, filename):
    global completed
    target_path = os.path.join(VOICEBANK_DIR, filename)
    temp_mp3 = f"/tmp/speech_gen_{filename}.mp3"
    
    # Text to send to TTS engine
    # Clean underscores or fill-in blanks like ___
    spoken_text = text_to_speak.replace("___", "").replace("...", "").strip()
    if not spoken_text:
        spoken_text = raw_key
        
    async with sem:
        try:
            comm = edge_tts.Communicate(spoken_text, VOICE, rate="+0%")
            await comm.save(temp_mp3)
            
            subprocess.run([
                "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_mp3,
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                target_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
                
            completed += 1
            if completed % 20 == 0 or completed == total:
                print(f"  [{completed}/{total}] Generated: {filename} for '{raw_key}'")
        except Exception as e:
            print(f"  ❌ Error for '{raw_key}': {e}")

async def main():
    if items_to_generate:
        t0 = time.time()
        tasks = [generate_audio(raw, clean, fn) for raw, clean, fn in items_to_generate]
        await asyncio.gather(*tasks)
        t1 = time.time()
        print(f"\n✨ Generated {completed} new voice files in {t1-t0:.2f}s!")
    
    # Update manifest with all keys & aliases
    for raw, clean, fn in items_to_generate:
        manifest[raw] = fn
        manifest[clean] = fn
        norm = re.sub(r'[？?！!。、…〜~「」()（）\[\]【】\s]', '', raw)
        if norm:
            manifest[norm] = fn
        # If contains slash
        if "/" in raw:
            for part in raw.split("/"):
                p_clean = clean_for_speech(part)
                if p_clean:
                    manifest[part.strip()] = fn
                    manifest[p_clean] = fn
                    
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Updated {MANIFEST_PATH}, total mapped keys: {len(manifest)}")

if __name__ == "__main__":
    asyncio.run(main())
