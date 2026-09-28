import asyncio
import os
import json
import subprocess
import edge_tts
import time

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")
VOICE = "ja-JP-NanamiNeural"

os.makedirs(VOICEBANK_DIR, exist_ok=True)

with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Build file -> optimal Japanese text
# Prefer Japanese kanji/kana over romaji
file_to_texts = {}
for k, v in manifest.items():
    file_to_texts.setdefault(v, []).append(k)

file_to_best_text = {}
for filename, keys in file_to_texts.items():
    # Pick the best text representation (prefer Japanese script over romaji)
    jp_keys = [k for k in keys if any('\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9faf' for c in k)]
    if jp_keys:
        # Pick the cleanest / most standard Japanese representation
        best = sorted(jp_keys, key=lambda x: (len(x), x))[0]
    else:
        best = sorted(keys, key=lambda x: (len(x), x))[0]
    file_to_best_text[filename] = best

print(f"🎙️ Starting neural VoiceBank regeneration for {len(file_to_best_text)} files using {VOICE}...")

sem = asyncio.Semaphore(16)
completed_count = 0
total_count = len(file_to_best_text)

async def process_entry(filename, text):
    global completed_count
    target_path = os.path.join(VOICEBANK_DIR, filename)
    temp_mp3 = f"/tmp/vb_neural_{filename}.mp3"
    
    async with sem:
        try:
            comm = edge_tts.Communicate(text, VOICE, rate="+0%")
            await comm.save(temp_mp3)

            # Convert to clean high-quality AAC m4a
            subprocess.run([
                "/opt/homebrew/bin/ffmpeg", "-y", "-i", temp_mp3,
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                target_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)

            completed_count += 1
            if completed_count % 100 == 0 or completed_count == total_count:
                print(f"  [{completed_count}/{total_count}] Processed: {filename} ('{text}')")
        except Exception as e:
            print(f"  ❌ Error processing {filename} ('{text}'): {e}")

async def main():
    t0 = time.time()
    tasks = [process_entry(fn, text) for fn, text in file_to_best_text.items()]
    await asyncio.gather(*tasks)
    t1 = time.time()
    print(f"\n🎉 Successfully regenerated all {completed_count}/{total_count} VoiceBank files in {t1-t0:.2f}s!")

if __name__ == "__main__":
    asyncio.run(main())
