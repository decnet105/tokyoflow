import asyncio
import os
import json
import hashlib
import re
import subprocess
import time

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
DICT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"
TMP_DIR = "tmp/audio_synth_sentences"

os.makedirs(VOICEBANK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

VOICE_FEMALE = "ja-JP-NanamiNeural"
VOICE_MALE = "ja-JP-KeitaNeural"

MALE_EQ_FILTER = "equalizer=f=230:t=q:w=1.2:g=3.8,equalizer=f=3200:t=q:w=1.8:g=-2.5,equalizer=f=6500:t=q:w=2.0:g=-6.0,lowpass=f=8200,aresample=44100"
FEMALE_EQ_FILTER = "equalizer=f=300:t=q:w=1.2:g=1.5,equalizer=f=4000:t=q:w=1.5:g=1.0,equalizer=f=8000:t=q:w=2.0:g=-3.0,lowpass=f=9500,aresample=44100"

def normalize_key(text: str) -> str:
    return (text
            .replace("？", "")
            .replace("?", "")
            .replace("！", "")
            .replace("!", "")
            .replace("。", "")
            .replace("、", "")
            .replace("…", "")
            .replace("〜", "")
            .replace("~", "")
            .replace("「", "")
            .replace("」", "")
            .replace("(", "")
            .replace(")", "")
            .replace("（", "")
            .replace("）", "")
            .replace("[", "")
            .replace("]", "")
            .replace("【", "")
            .replace("】", "")
            .replace("#", "")
            .replace("　", "")
            .strip())

def clean_noise(text: str) -> str:
    if not text: return ""
    text = re.sub(r"^[※◆◇■□▲△▼▽★☆●○◎・\s]+", "", text)
    text = re.sub(r"^(対|同音|図|類|反|連|合|派|ム|EA|[A-Z])\s*(?=[一-龯ぁ-んァ-ン])", "", text)
    text = re.sub(r"^(Core\s+[Nn][1-5]\s+vocabulary:\s*)([A-Z]|EA|ム|対|※)\s*", r"\1", text)
    text = re.sub(r"^(「)([A-Z]|EA|ム|対|※)\s*", r"\1", text)
    text = re.sub(r"(usage\s+of\s+)([A-Z]|EA|ム|対|※)\s*", r"\1", text)
    return text.strip()

def make_filename(prefix: str, text: str) -> str:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]
    safe_text = re.sub(r'[^\w\-_]', '_', text)[:16]
    return f"{prefix}_{safe_text}_{h}.m4a"

async def synthesize_one(sem: asyncio.Semaphore, text: str, filename: str, is_male: bool = False):
    async with sem:
        out_path = os.path.join(VOICEBANK_DIR, filename)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            return text, filename

        tmp_mp3 = os.path.join(TMP_DIR, f"{hashlib.md5(text.encode()).hexdigest()}.mp3")
        voice = VOICE_MALE if is_male else VOICE_FEMALE

        import edge_tts
        max_retries = 3
        for attempt in range(max_retries):
            try:
                comm = edge_tts.Communicate(text, voice, rate="-3%", pitch="+1Hz" if not is_male else "-2Hz")
                await comm.save(tmp_mp3)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to synthesize: {text} ({e})")
                    return text, None
                await asyncio.sleep(0.5 * (attempt + 1))

        filt = MALE_EQ_FILTER if is_male else FEMALE_EQ_FILTER
        try:
            subprocess.run([
                "/opt/homebrew/bin/ffmpeg", "-y", "-i", tmp_mp3,
                "-af", filt,
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                out_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"❌ FFmpeg error for {text}: {e}")
            return text, None
        finally:
            if os.path.exists(tmp_mp3):
                os.remove(tmp_mp3)

        return text, filename

async def main():
    print("🚀 Step 1: Cleaning jlpt_dictionary.json noise...")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        words = json.load(f)

    for w in words:
        w["kanji"] = clean_noise(w.get("kanji", ""))
        w["reading"] = clean_noise(w.get("reading", ""))
        w["romaji"] = clean_noise(w.get("romaji", ""))
        w["meaning"] = clean_noise(w.get("meaning", ""))
        w["exampleJa"] = clean_noise(w.get("exampleJa", ""))
        w["exampleFurigana"] = clean_noise(w.get("exampleFurigana", ""))
        w["exampleZh"] = clean_noise(w.get("exampleZh", ""))
        w["exampleEn"] = clean_noise(w.get("exampleEn", ""))
        w["collocation"] = clean_noise(w.get("collocation", ""))

    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print(f"✅ Cleaned {len(words)} dictionary entries.")

    print("🚀 Step 2: Checking audio coverage in VoiceBank...")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_files = set(os.listdir(VOICEBANK_DIR))

    tasks = []
    sem = asyncio.Semaphore(30)
    seen_texts = set()

    for idx, w in enumerate(words):
        ex = w.get("exampleJa", "").strip()
        if ex and ex not in seen_texts:
            seen_texts.add(ex)
            # Check if ex in manifest and file exists
            if not (ex in manifest and manifest[ex] in existing_files):
                fn = make_filename("dict_ex", ex)
                is_male = (idx % 2 == 1)
                tasks.append(synthesize_one(sem, ex, fn, is_male))

    print(f"📊 Synthesizing {len(tasks)} missing example sentences concurrently...")

    completed = 0
    total = len(tasks)
    start_time = time.time()

    # Run in batches of 150
    batch_size = 150
    for i in range(0, total, batch_size):
        batch = tasks[i:i + batch_size]
        results = await asyncio.gather(*batch)
        for text, fn in results:
            if fn:
                manifest[text] = fn
                norm = normalize_key(text)
                if norm:
                    manifest[norm] = fn
        completed += len(batch)
        elapsed = time.time() - start_time
        speed = completed / max(0.1, elapsed)
        print(f"⚡️ Progress: {completed}/{total} ({completed/total*100:.1f}%) - {speed:.1f} sentences/sec")

    # Also ensure all word and reading aliases are in manifest
    print("🚀 Step 3: Registering all word & reading aliases in manifest...")
    for w in words:
        k = w.get("kanji", "").strip()
        r = w.get("reading", "").strip()
        ex = w.get("exampleJa", "").strip()

        audio_file = None
        for cand in [k, r]:
            if cand in manifest and manifest[cand] in existing_files:
                audio_file = manifest[cand]
                break

        if audio_file:
            if k:
                manifest[k] = audio_file
                manifest[normalize_key(k)] = audio_file
            if r:
                manifest[r] = audio_file
                manifest[normalize_key(r)] = audio_file

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"✅ Total voicebank keys in manifest: {len(manifest)}")

    # Audit 100% verification
    uncovered_words = 0
    uncovered_examples = 0
    for w in words:
        k = w.get("kanji", "").strip()
        r = w.get("reading", "").strip()
        ex = w.get("exampleJa", "").strip()

        if not ((k in manifest and manifest[k] in existing_files) or (r in manifest and manifest[r] in existing_files)):
            uncovered_words += 1
        if ex and not (ex in manifest and manifest[ex] in existing_files):
            uncovered_examples += 1

    print(f"🎉 FINAL AUDIT RESULTS:")
    print(f"  - Total words: {len(words)}")
    print(f"  - Uncovered words: {uncovered_words} ({'100% COVERED' if uncovered_words == 0 else 'FAIL'})")
    print(f"  - Uncovered sentences: {uncovered_examples} ({'100% COVERED' if uncovered_examples == 0 else 'FAIL'})")

if __name__ == "__main__":
    asyncio.run(main())
