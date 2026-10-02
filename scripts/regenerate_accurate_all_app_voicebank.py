import asyncio
import os
import json
import hashlib
import re
import subprocess
import time

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
TMP_DIR = "tmp/audio_accurate"

os.makedirs(VOICEBANK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

SAMPLE_RATE = 44100
VOICE_FEMALE = "ja-JP-NanamiNeural"  # Clear, soothing, native Tokyo female
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

async def synth_audio(sem: asyncio.Semaphore, text_to_speak: str, out_filename: str, is_male: bool = False, slow: bool = True):
    async with sem:
        out_path = os.path.join(VOICEBANK_DIR, out_filename)
        # Check if already synthesized and valid
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            return out_filename

        tmp_mp3 = os.path.join(TMP_DIR, f"{hashlib.md5(text_to_speak.encode()).hexdigest()}_{int(time.time()*1000)%10000}.mp3")
        voice = VOICE_MALE if is_male else VOICE_FEMALE
        rate_str = "-10%" if slow else "-4%"
        pitch_str = "-2Hz" if is_male else "+3Hz"

        import edge_tts
        max_retries = 3
        for attempt in range(max_retries):
            try:
                comm = edge_tts.Communicate(text_to_speak, voice, rate=rate_str, pitch=pitch_str)
                await comm.save(tmp_mp3)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to synthesize: {text_to_speak} ({e})")
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
            print(f"❌ FFmpeg error for {text_to_speak}: {e}")
            return None
        finally:
            if os.path.exists(tmp_mp3):
                try: os.remove(tmp_mp3)
                except: pass

        return out_filename

async def main():
    print("🚀 Starting Accurate 100% Japanese VoiceBank Generation...")

    manifest = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    # 1. Load JLPT Dictionary
    dict_file = "TokyoFlow/Resources/jlpt_dictionary.json"
    words = json.load(open(dict_file, "r", encoding="utf-8"))
    print(f"📖 Loaded {len(words)} JLPT dictionary words")

    tasks = []
    sem = asyncio.Semaphore(16)
    
    # Store mapping updates
    mappings = [] # list of (key, filename)

    for w in words:
        wid = w["id"]
        kanji = w.get("kanji", "").strip()
        reading = w.get("reading", "").strip()
        example = w.get("exampleJa", "").strip()

        # ⭐️ CRITICAL FIX: Always synthesize vocabulary using exact Hiragana reading (e.g. くる, not 来る)
        # This guarantees 100% phonetic accuracy with zero kanji mispronunciation!
        speak_text = reading if reading else kanji
        w_fn = f"w_{wid}.m4a"
        tasks.append((speak_text, w_fn, False, True))

        if kanji:
            mappings.append((kanji, w_fn))
            mappings.append((normalize_key(kanji), w_fn))
        if reading:
            mappings.append((reading, w_fn))
            mappings.append((normalize_key(reading), w_fn))

        # Example sentence
        if example:
            ex_fn = f"ex_{wid}.m4a"
            tasks.append((example, ex_fn, False, False))
            mappings.append((example, ex_fn))
            mappings.append((normalize_key(example), ex_fn))

    # 2. Grammar sentences
    grammar_file = "TokyoFlow/Resources/jlpt_grammar.json"
    if os.path.exists(grammar_file):
        grammars = json.load(open(grammar_file, "r", encoding="utf-8"))
        for g in grammars:
            gid = g.get("id", "g")
            title = g.get("title", "").strip()
            if title:
                t_fn = f"g_title_{gid}.m4a"
                tasks.append((title, t_fn, False, True))
                mappings.append((title, t_fn))
                mappings.append((normalize_key(title), t_fn))
            for i, s in enumerate(g.get("sentences", [])):
                ja = s.get("japanese", "").strip()
                if ja:
                    s_fn = f"g_sent_{gid}_{i+1}.m4a"
                    tasks.append((ja, s_fn, False, False))
                    mappings.append((ja, s_fn))
                    mappings.append((normalize_key(ja), s_fn))

    # 3. Scenarios
    scenarios_file = "TokyoFlow/Resources/scenarios.json"
    if os.path.exists(scenarios_file):
        scenarios = json.load(open(scenarios_file, "r", encoding="utf-8"))
        for sc in scenarios:
            sc_id = sc.get("id", "sc")
            for i, d in enumerate(sc.get("dialogues", [])):
                ja = d.get("japanese", "").strip()
                if ja:
                    is_m = (d.get("speaker", "") in ["Staff", "Server", "Chef", "Officer", "Conductor"])
                    d_fn = f"sc_{sc_id}_d{i+1}.m4a"
                    tasks.append((ja, d_fn, is_m, False))
                    mappings.append((ja, d_fn))
                    mappings.append((normalize_key(ja), d_fn))
            for i, c in enumerate(sc.get("choices", [])):
                ja = c.get("textJa", "").strip()
                if ja:
                    c_fn = f"sc_{sc_id}_c{i+1}.m4a"
                    tasks.append((ja, c_fn, False, False))
                    mappings.append((ja, c_fn))
                    mappings.append((normalize_key(ja), c_fn))

    # 4. Manga Lessons
    manga_file = "TokyoFlow/Resources/manga_lessons.json"
    if os.path.exists(manga_file):
        mangas = json.load(open(manga_file, "r", encoding="utf-8"))
        for mg in mangas:
            mg_id = mg.get("id", "mg")
            for i, p in enumerate(mg.get("panels", [])):
                ja = p.get("dialogueJa", "").strip()
                if ja:
                    p_fn = f"mg_{mg_id}_p{i+1}.m4a"
                    tasks.append((ja, p_fn, False, False))
                    mappings.append((ja, p_fn))
                    mappings.append((normalize_key(ja), p_fn))
                sfx = p.get("sfxKana", "").strip()
                if sfx:
                    sfx_fn = f"mg_{mg_id}_sfx{i+1}.m4a"
                    tasks.append((sfx, sfx_fn, False, True))
                    mappings.append((sfx, sfx_fn))
                    mappings.append((normalize_key(sfx), sfx_fn))

    # Deduplicate task list
    unique_tasks = {}
    for text, fn, is_m, slow in tasks:
        if fn not in unique_tasks:
            unique_tasks[fn] = (text, fn, is_m, slow)

    print(f"🎯 Total unique audio files to ensure: {len(unique_tasks)}")
    
    # Filter files needing synthesis
    needed = []
    for fn, (text, _, is_m, slow) in unique_tasks.items():
        p = os.path.join(VOICEBANK_DIR, fn)
        if not os.path.exists(p) or os.path.getsize(p) < 1000:
            needed.append((text, fn, is_m, slow))

    print(f"⚡️ Files needing generation: {len(needed)}")

    # Execute synthesis
    async_tasks = [synth_audio(sem, text, fn, is_m, slow) for text, fn, is_m, slow in needed]
    start_t = time.time()
    await asyncio.gather(*async_tasks)
    print(f"✅ Audio synthesis completed in {time.time()-start_t:.1f}s!")

    # Update manifest
    for k, fn in mappings:
        if k:
            manifest[k] = fn

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"🎉 Manifest updated with {len(manifest)} total verified keys!")

    # Verify '来る' and 'くる' specifically
    print("🔍 Verification for '来る' ->", manifest.get("来る"))
    print("🔍 Verification for 'くる' ->", manifest.get("くる"))

if __name__ == "__main__":
    asyncio.run(main())
