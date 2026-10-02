import asyncio
import os
import json
import hashlib
import re
import subprocess
import time

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
ALIGNMENT_PATH = os.path.join(VOICEBANK_DIR, "sentence_alignment_manifest.json")
TMP_DIR = "tmp/audio_synth"

os.makedirs(VOICEBANK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

VOICE_FEMALE = "ja-JP-NanamiNeural"  # Clear, native Tokyo female
VOICE_MALE = "ja-JP-KeitaNeural"    # Broadcast male

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

async def synth_audio(sem: asyncio.Semaphore, text_to_speak: str, out_filename: str, is_male: bool = False, slow: bool = False):
    async with sem:
        out_path = os.path.join(VOICEBANK_DIR, out_filename)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            return out_filename

        tmp_mp3 = os.path.join(TMP_DIR, f"{hashlib.md5(text_to_speak.encode()).hexdigest()}_{int(time.time()*1000)%10000}.mp3")
        voice = VOICE_MALE if is_male else VOICE_FEMALE
        rate_str = "-10%" if slow else "-3%"
        pitch_str = "-2Hz" if is_male else "+3Hz"

        import edge_tts
        max_retries = 4
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
    print("🚀 Starting Complete 100% Native VoiceBank & Sentence Alignment Build...")

    manifest = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    # Load JLPT Dictionary
    dict_file = "TokyoFlow/Resources/jlpt_dictionary.json"
    words = json.load(open(dict_file, "r", encoding="utf-8"))
    print(f"📖 Loaded {len(words)} JLPT dictionary words")

    tasks = []
    sem = asyncio.Semaphore(20)
    mappings = [] # list of (key, filename)

    for w in words:
        wid = w["id"]
        kanji = w.get("kanji", "").strip()
        reading = w.get("reading", "").strip()
        example = w.get("exampleJa", "").strip()
        ex_furigana = w.get("exampleFurigana", "").strip()

        # Word audio
        speak_text = reading if reading else kanji
        w_fn = f"w_{wid}.m4a"
        tasks.append((speak_text, w_fn, False, True))

        if kanji:
            mappings.append((kanji, w_fn))
            mappings.append((normalize_key(kanji), w_fn))
        if reading:
            mappings.append((reading, w_fn))
            mappings.append((normalize_key(reading), w_fn))

        # Example sentence audio
        if example:
            ex_fn = f"ex_{wid}.m4a"
            tasks.append((example, ex_fn, False, False))
            mappings.append((example, ex_fn))
            mappings.append((normalize_key(example), ex_fn))
            if ex_furigana and ex_furigana != example:
                mappings.append((ex_furigana, ex_fn))
                mappings.append((normalize_key(ex_furigana), ex_fn))

    # Grammar
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

    # Scenarios
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

    # Deduplicate task list
    unique_tasks = {}
    for text, fn, is_m, slow in tasks:
        if fn not in unique_tasks:
            unique_tasks[fn] = (text, fn, is_m, slow)

    # Filter tasks to only those needing generation
    pending_tasks = []
    for fn, (text, _, is_m, slow) in unique_tasks.items():
        out_path = os.path.join(VOICEBANK_DIR, fn)
        if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
            pending_tasks.append((text, fn, is_m, slow))

    print(f"🎯 Total unique audio tasks: {len(unique_tasks)} | Pending synthesis: {len(pending_tasks)}")

    # Run in batches
    batch_size = 30
    for i in range(0, len(pending_tasks), batch_size):
        batch = pending_tasks[i:i+batch_size]
        print(f"🎙 Processing batch {i//batch_size + 1}/{(len(pending_tasks)-1)//batch_size + 1} ({len(batch)} items)...")
        coros = [synth_audio(sem, text, fn, is_m, slow) for text, fn, is_m, slow in batch]
        await asyncio.gather(*coros)

    # Update manifest
    for k, fn in mappings:
        if k:
            manifest[k] = fn

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    total_files = len([f for f in os.listdir(VOICEBANK_DIR) if f.endswith(".m4a")])
    print(f"✨ Finished! Total VoiceBank .m4a files: {total_files}")
    print(f"📜 Manifest total keys: {len(manifest)}")

if __name__ == "__main__":
    asyncio.run(main())
