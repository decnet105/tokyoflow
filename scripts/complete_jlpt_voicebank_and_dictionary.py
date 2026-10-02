import asyncio
import os
import json
import hashlib
import re
import subprocess
import time
import pykakasi

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
DICT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"
GRAMMAR_PATH = "TokyoFlow/Resources/jlpt_grammar.json"
PBX_PATH = "TokyoFlow.xcodeproj/project.pbxproj"
TMP_DIR = "tmp/audio_synth_full"

os.makedirs(VOICEBANK_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)

VOICE_FEMALE = "ja-JP-NanamiNeural"
VOICE_MALE = "ja-JP-KeitaNeural"

MALE_EQ_FILTER = "equalizer=f=230:t=q:w=1.2:g=3.8,equalizer=f=3200:t=q:w=1.8:g=-2.5,equalizer=f=6500:t=q:w=2.0:g=-6.0,lowpass=f=8200,aresample=44100"
FEMALE_EQ_FILTER = "equalizer=f=300:t=q:w=1.2:g=1.5,equalizer=f=4000:t=q:w=1.5:g=1.0,equalizer=f=8000:t=q:w=2.0:g=-3.0,lowpass=f=9500,aresample=44100"

k = pykakasi.kakasi()

def to_ruby_sentence(text: str) -> str:
    if not text:
        return ""
    result = k.convert(text)
    parts = []
    for item in result:
        orig = item["orig"]
        hira = item["hira"]
        # If orig has Kanji and hira != orig
        if any("\u4e00" <= c <= "\u9fff" for c in orig) and hira != orig:
            parts.append(f"{orig}({hira})")
        else:
            parts.append(orig)
    return "".join(parts)

def make_filename(prefix: str, text: str) -> str:
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:10]
    safe_text = re.sub(r'[^\w\-_]', '_', text)[:16]
    return f"{prefix}_{safe_text}_{h}.m4a"

async def synthesize_one(sem: asyncio.Semaphore, text: str, filename: str, is_male: bool = False):
    async with sem:
        out_path = os.path.join(VOICEBANK_DIR, filename)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
            return text, filename

        tmp_mp3 = os.path.join(TMP_DIR, f"{hashlib.md5(text.encode()).hexdigest()}_{time.time_ns()}.mp3")
        voice = VOICE_MALE if is_male else VOICE_FEMALE

        import edge_tts
        max_retries = 3
        success = False
        for attempt in range(max_retries):
            try:
                comm = edge_tts.Communicate(text, voice, rate="-3%", pitch="+1Hz" if not is_male else "-2Hz")
                await comm.save(tmp_mp3)
                if os.path.exists(tmp_mp3) and os.path.getsize(tmp_mp3) > 100:
                    success = True
                    break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to synthesize: {text} ({e})")
                    return text, None
                await asyncio.sleep(0.5 * (attempt + 1))

        if not success:
            return text, None

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
                try:
                    os.remove(tmp_mp3)
                except Exception:
                    pass

        return text, filename

def sync_voicebank_to_xcode():
    print("📦 Syncing all VoiceBank audio files to Xcode project.pbxproj...")
    with open(PBX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Find VoiceBank group ID
    group_match = re.search(r"([0-9A-F]{24})\s*/\*\s*VoiceBank\s*\*/\s*=\s*\{[^}]+children\s*=\s*\(([^)]+)\)", content)
    if not group_match:
        print("❌ Could not find VoiceBank group in pbxproj")
        return

    group_id = group_match.group(1)

    # Find Resources phase
    res_match = re.search(r"([0-9A-F]{24})\s*/\*\s*Resources\s*\*/\s*=\s*\{[^}]+isa\s*=\s*PBXResourcesBuildPhase;[^}]+files\s*=\s*\(([^)]+)\)", content)
    if not res_match:
        print("❌ Could not find Resources phase in pbxproj")
        return

    res_id = res_match.group(1)

    # Scan all files in VoiceBank
    all_vb_files = [f for f in os.listdir(VOICEBANK_DIR) if not f.startswith(".")]
    print(f"📁 Total files found in VoiceBank folder: {len(all_vb_files)}")

    # Extract already referenced files efficiently
    existing_paths = set(re.findall(r'path = \"?([^\";]+)\"?;', content))

    files_to_add = [f for f in all_vb_files if f not in existing_paths]
    print(f"➕ Files to add to Xcode project: {len(files_to_add)}")

    if not files_to_add:
        print("✅ All files already synced in Xcode project!")
        return

    def gen_id(seed: str) -> str:
        return hashlib.md5(seed.encode("utf-8")).hexdigest()[:24].upper()

    pbx_build_files = []
    pbx_file_refs = []
    group_children_entries = []
    res_phase_entries = []

    for fn in files_to_add:
        file_id = gen_id(f"fileref_{fn}")
        build_id = gen_id(f"buildfile_{fn}")
        file_type = "text.json" if fn.endswith(".json") else "audio.m4a"

        pbx_build_files.append(f"\t\t{build_id} /* {fn} in Resources */ = {{isa = PBXBuildFile; fileRef = {file_id} /* {fn} */; }};\n")
        pbx_file_refs.append(f"\t\t{file_id} /* {fn} */ = {{isa = PBXFileReference; lastKnownFileType = {file_type}; path = \"{fn}\"; sourceTree = \"<group>\"; }};\n")
        group_children_entries.append(f"\t\t\t\t{file_id} /* {fn} */,\n")
        res_phase_entries.append(f"\t\t\t\t{build_id} /* {fn} in Resources */,\n")

    # Insert into PBXBuildFile section
    build_file_section_pos = content.find("/* Begin PBXBuildFile section */")
    if build_file_section_pos != -1:
        insert_pos = content.find("\n", build_file_section_pos) + 1
        content = content[:insert_pos] + "".join(pbx_build_files) + content[insert_pos:]

    # Insert into PBXFileReference section
    file_ref_section_pos = content.find("/* Begin PBXFileReference section */")
    if file_ref_section_pos != -1:
        insert_pos = content.find("\n", file_ref_section_pos) + 1
        content = content[:insert_pos] + "".join(pbx_file_refs) + content[insert_pos:]

    # Insert into VoiceBank group children
    group_pattern = f"({group_id}\\s*/\\*\\s*VoiceBank\\s*\\*/\\s*=\\s*\\{{[^}}]+children\\s*=\\s*\\()"
    content = re.sub(group_pattern, r"\1\n" + "".join(group_children_entries), content, count=1)

    # Insert into Resources phase files
    res_pattern = f"({res_id}\\s*/\\*\\s*Resources\\s*\\*/\\s*=\\s*\\{{[^}}]+files\\s*=\\s*\\()"
    content = re.sub(res_pattern, r"\1\n" + "".join(res_phase_entries), content, count=1)

    with open(PBX_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🎉 Successfully registered {len(files_to_add)} files directly into {PBX_PATH}!")

async def main():
    print("🚀 Step 1: Upgrading dictionary Furigana to Ruby-annotated standard...")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        words = json.load(f)

    updated_count = 0
    for w in words:
        ex = w.get("exampleJa", "").strip()
        if ex:
            new_furi = to_ruby_sentence(ex)
            if w.get("exampleFurigana") != new_furi:
                w["exampleFurigana"] = new_furi
                updated_count += 1

    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print(f"✅ Updated {updated_count} exampleFurigana in jlpt_dictionary.json.")

    print("🚀 Step 2: Checking and preparing synthesis tasks...")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_files = set(os.listdir(VOICEBANK_DIR))
    sem = asyncio.Semaphore(25)
    tasks = []
    seen_texts = set()

    # Dictionary words
    for idx, w in enumerate(words):
        kanji = w.get("kanji", "").strip()
        reading = w.get("reading", "").strip()
        target = kanji or reading
        if target and target not in seen_texts:
            seen_texts.add(target)
            if not (target in manifest and manifest[target] in existing_files):
                fn = make_filename("word_jlpt", target)
                tasks.append(synthesize_one(sem, target, fn, is_male=(idx % 2 == 1)))

        if reading and reading not in seen_texts:
            seen_texts.add(reading)
            if not (reading in manifest and manifest[reading] in existing_files):
                fn = make_filename("word_jlpt_rd", reading)
                tasks.append(synthesize_one(sem, reading, fn, is_male=(idx % 2 == 1)))

    # Dictionary example sentences
    for idx, w in enumerate(words):
        ex = w.get("exampleJa", "").strip()
        if ex and ex not in seen_texts:
            seen_texts.add(ex)
            if not (ex in manifest and manifest[ex] in existing_files):
                fn = make_filename("sent_jlpt", ex)
                tasks.append(synthesize_one(sem, ex, fn, is_male=(idx % 2 == 1)))

    # Grammar patterns and sentences
    with open(GRAMMAR_PATH, "r", encoding="utf-8") as f:
        grammar_list = json.load(f)

    for idx, g in enumerate(grammar_list):
        t = g.get("title", "").strip()
        if t and t not in seen_texts:
            seen_texts.add(t)
            if not (t in manifest and manifest[t] in existing_files):
                fn = make_filename("gram_title", t)
                tasks.append(synthesize_one(sem, t, fn, is_male=(idx % 2 == 1)))
        for s in g.get("sentences", []):
            ja = s.get("japanese", "").strip()
            if ja and ja not in seen_texts:
                seen_texts.add(ja)
                if not (ja in manifest and manifest[ja] in existing_files):
                    fn = make_filename("gram_sent", ja)
                    tasks.append(synthesize_one(sem, ja, fn, is_male=(idx % 2 == 1)))

    total_tasks = len(tasks)
    print(f"📊 Total audio files to synthesize: {total_tasks}")

    if total_tasks > 0:
        batch_size = 100
        completed = 0
        t0 = time.time()
        for i in range(0, total_tasks, batch_size):
            batch = tasks[i:i + batch_size]
            results = await asyncio.gather(*batch)
            for text, fn in results:
                if fn:
                    manifest[text] = fn
            completed += len(batch)
            elapsed = time.time() - t0
            rate = completed / max(1.0, elapsed)
            remaining = (total_tasks - completed) / max(0.1, rate)
            print(f"⚡ Progress: {completed}/{total_tasks} ({completed*100/total_tasks:.1f}%) - ETA: {remaining:.0f}s")
            
            # Save manifest periodically
            with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Save final manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("✅ Manifest saved successfully!")

    # Step 3: Xcode project synchronization
    sync_voicebank_to_xcode()

if __name__ == "__main__":
    asyncio.run(main())
