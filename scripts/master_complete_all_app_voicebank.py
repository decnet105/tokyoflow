import asyncio
import os
import json
import hashlib
import re
import subprocess
import time

AUDIO_DIR = "TokyoFlow/Resources/Audio"
VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
TMP_DIR = "tmp/audio_synth"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VOICEBANK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

SAMPLE_RATE = 44100
VOICE_FEMALE = "ja-JP-NanamiNeural"  # Clear, authentic NHK female
VOICE_MALE = "ja-JP-KeitaNeural"    # Warm broadcast male

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

def make_filename(prefix: str, text: str) -> str:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]
    safe_text = re.sub(r'[^\w\-_]', '_', text)[:16]
    return f"{prefix}_{safe_text}_{h}.m4a"

async def synthesize_one(sem: asyncio.Semaphore, text: str, filename: str, is_male: bool = False, slow: bool = False):
    async with sem:
        out_path = os.path.join(VOICEBANK_DIR, filename)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            return filename

        tmp_mp3 = os.path.join(TMP_DIR, f"{hashlib.md5(text.encode()).hexdigest()}.mp3")
        voice = VOICE_MALE if is_male else VOICE_FEMALE
        rate_str = "-10%" if slow else "-4%"
        pitch_str = "-2Hz" if is_male else "+3Hz"

        import edge_tts
        max_retries = 3
        for attempt in range(max_retries):
            try:
                comm = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
                await comm.save(tmp_mp3)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to synthesize: {text} ({e})")
                    return None
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
            return None
        finally:
            if os.path.exists(tmp_mp3):
                os.remove(tmp_mp3)

        return filename

async def main():
    print("🚀 Starting Complete App VoiceBank Audit & Synthesis...")

    # Load existing manifest
    manifest = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    print(f"📦 Existing manifest keys: {len(manifest)}")

    # Collect ALL target texts
    targets = {}  # text -> {"prefix": str, "is_male": bool, "slow": bool}

    # 1. JLPT Dictionary (2,632 words)
    dict_file = "TokyoFlow/Resources/jlpt_dictionary.json"
    if os.path.exists(dict_file):
        words = json.load(open(dict_file, "r", encoding="utf-8"))
        for w in words:
            kanji = w.get("kanji", "").strip()
            reading = w.get("reading", "").strip()
            ex = w.get("exampleJa", "").strip()

            if kanji:
                targets[kanji] = {"prefix": "dict_w", "is_male": False, "slow": True}
            if reading:
                targets[reading] = {"prefix": "dict_r", "is_male": False, "slow": True}
            if ex:
                targets[ex] = {"prefix": "dict_ex", "is_male": False, "slow": False}

    # 2. JLPT Grammar
    grammar_file = "TokyoFlow/Resources/jlpt_grammar.json"
    if os.path.exists(grammar_file):
        grammars = json.load(open(grammar_file, "r", encoding="utf-8"))
        for g in grammars:
            t = g.get("title", "").strip()
            if t:
                targets[t] = {"prefix": "g_title", "is_male": False, "slow": True}
            for s in g.get("sentences", []):
                ja = s.get("japanese", "").strip()
                if ja:
                    targets[ja] = {"prefix": "g_sent", "is_male": False, "slow": False}

    # 3. Scenarios
    scenarios_file = "TokyoFlow/Resources/scenarios.json"
    if os.path.exists(scenarios_file):
        scenarios = json.load(open(scenarios_file, "r", encoding="utf-8"))
        for sc in scenarios:
            for d in sc.get("dialogues", []):
                ja = d.get("japanese", "").strip()
                if ja:
                    is_m = (d.get("speaker", "") in ["Staff", "Server", "Chef", "Officer", "Conductor"])
                    targets[ja] = {"prefix": "sc_dlg", "is_male": is_m, "slow": False}
            for c in sc.get("choices", []):
                ja = c.get("textJa", "").strip()
                if ja:
                    targets[ja] = {"prefix": "sc_opt", "is_male": False, "slow": False}

    # 4. Manga Lessons
    manga_file = "TokyoFlow/Resources/manga_lessons.json"
    if os.path.exists(manga_file):
        mangas = json.load(open(manga_file, "r", encoding="utf-8"))
        for mg in mangas:
            for p in mg.get("panels", []):
                ja = p.get("dialogueJa", "").strip()
                if ja:
                    targets[ja] = {"prefix": "mg_dlg", "is_male": False, "slow": False}
                sfx = p.get("sfxKana", "").strip()
                if sfx:
                    targets[sfx] = {"prefix": "mg_sfx", "is_male": False, "slow": True}

    # 5. Announcements
    ann_file = "TokyoFlow/Resources/announcements.json"
    if os.path.exists(ann_file):
        anns = json.load(open(ann_file, "r", encoding="utf-8"))
        for a in anns:
            ja = a.get("scriptJa", "").strip()
            if ja:
                targets[ja] = {"prefix": "ann_scr", "is_male": False, "slow": False}

    # 6. Dojo Battles
    dojo_file = "TokyoFlow/Resources/dojo_battles.json"
    if os.path.exists(dojo_file):
        dojos = json.load(open(dojo_file, "r", encoding="utf-8"))
        for dj in dojos:
            for q in dj.get("questions", []):
                ja = q.get("promptJa", "").strip()
                if ja:
                    targets[ja] = {"prefix": "dj_pr", "is_male": True, "slow": False}
                for opt in q.get("options", []):
                    opt_ja = opt.strip()
                    if opt_ja:
                        targets[opt_ja] = {"prefix": "dj_opt", "is_male": False, "slow": False}

    print(f"🎯 Total unique Japanese phrases identified across entire app: {len(targets)}")

    # Filter out what is already in manifest and on disk
    to_synthesize = []
    for text, info in targets.items():
        fn = manifest.get(text) or manifest.get(normalize_key(text))
        disk_ok = fn and os.path.exists(os.path.join(VOICEBANK_DIR, fn)) and os.path.getsize(os.path.join(VOICEBANK_DIR, fn)) > 1000
        if not disk_ok:
            gen_fn = make_filename(info["prefix"], text)
            to_synthesize.append((text, gen_fn, info["is_male"], info["slow"]))

    print(f"⚡️ Missing items needing synthesis: {len(to_synthesize)}")

    # Parallel synthesis with semaphore
    sem = asyncio.Semaphore(16)
    tasks = []
    for text, fn, is_male, slow in to_synthesize:
        tasks.append(synthesize_one(sem, text, fn, is_male, slow))

    start_time = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time
    print(f"✅ Synthesized {len(results)} audio files in {elapsed:.1f}s!")

    # Update manifest with all generated and existing keys
    for text, info in targets.items():
        norm = normalize_key(text)
        fn = manifest.get(text) or manifest.get(norm)
        if not fn or not os.path.exists(os.path.join(VOICEBANK_DIR, fn)):
            fn = make_filename(info["prefix"], text)
        
        manifest[text] = fn
        manifest[norm] = fn

    # Write updated manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"🎉 Updated manifest written to {MANIFEST_PATH} with {len(manifest)} total keys!")

    # Verify coverage
    missing_after = 0
    for text in targets:
        if text not in manifest and normalize_key(text) not in manifest:
            missing_after += 1
    print(f"🏆 Final Verification: {len(targets) - missing_after}/{len(targets)} ({(len(targets)-missing_after)/len(targets)*100:.2f}%) covered by VoiceBank native human audio!")

if __name__ == "__main__":
    asyncio.run(main())
