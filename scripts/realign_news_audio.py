import json
import os
import subprocess
import re

NEWS_JSON_PATH = "TokyoFlow/Resources/daily_news.json"
AUDIO_DIR = "TokyoFlow/Resources/Audio"
VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
MANIFEST_PATH = os.path.join(VOICEBANK_DIR, "voice_bank_manifest.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VOICEBANK_DIR, exist_ok=True)

manifest = {}
if os.path.exists(MANIFEST_PATH):
    manifest = json.load(open(MANIFEST_PATH, "r", encoding="utf-8"))

news_data = json.load(open(NEWS_JSON_PATH, "r", encoding="utf-8"))

def get_audio_duration(file_path):
    res = subprocess.run(["afinfo", file_path], capture_output=True, text=True)
    for line in res.stdout.splitlines():
        if "estimated duration" in line:
            # e.g. "estimated duration: 5.432000 sec"
            m = re.search(r"estimated duration:\s*([\d\.]+)\s*sec", line)
            if m:
                return float(m.group(1))
    return 0.0

def create_silence_aiff(duration_sec, out_path):
    # Use sox or ffmpeg or afconvert or python wave
    # We can use python wave module to generate a pure silence 44.1kHz stereo AIFF/WAV
    import wave
    import struct
    n_samples = int(duration_sec * 44100)
    with wave.open(out_path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        silence_bytes = b'\x00\x00\x00\x00' * n_samples
        w.writeframes(silence_bytes)

for article in news_data:
    article_id = article["id"]
    output_audio_name = f"{article_id}.m4a"
    final_output_path = os.path.join(AUDIO_DIR, output_audio_name)

    print(f"\nProcessing {article_id}: {article['title']}")
    sentences = article["contentSentences"]

    temp_files = []
    current_time = 0.0
    pause_duration = 0.6  # 600ms natural breath pause between sentences

    silence_wav = f"/tmp/silence_{pause_duration}s.wav"
    create_silence_aiff(pause_duration, silence_wav)

    for idx, sent in enumerate(sentences):
        sent_id = sent["id"]
        japanese_text = sent["japanese"]
        
        # Clean text for speech
        clean_text = sent.get("furigana", japanese_text)
        # Using japanese text directly with Kyoko (Tokyo native newsreader style)
        # Kyoko has standard NHK Tokyo accent pitch
        temp_sent_aiff = f"/tmp/{article_id}_{sent_id}.aiff"
        temp_sent_m4a = f"/tmp/{article_id}_{sent_id}.m4a"

        # News broadcast speed: 175 wpm (clean standard Tokyo NHK pace)
        subprocess.run(["say", "-v", "Kyoko", "-r", "175", "-o", temp_sent_aiff, japanese_text], check=True)
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", temp_sent_aiff, temp_sent_m4a], check=True)

        sent_duration = get_audio_duration(temp_sent_m4a)
        start_time = round(current_time, 2)
        end_time = round(current_time + sent_duration, 2)

        sent["startTimeSec"] = start_time
        sent["endTimeSec"] = end_time

        print(f"  Sentence {sent_id} [{start_time}s - {end_time}s] ({sent_duration:.2f}s): {japanese_text[:25]}...")

        # Also register single sentence in VoiceBank
        vb_name = f"news_{article_id}_{sent_id}.m4a"
        vb_path = os.path.join(VOICEBANK_DIR, vb_name)
        subprocess.run(["cp", temp_sent_m4a, vb_path], check=True)
        manifest[japanese_text] = vb_name

        temp_files.append(temp_sent_aiff)
        if idx < len(sentences) - 1:
            temp_files.append(silence_wav)
            current_time = end_time + pause_duration
        else:
            current_time = end_time

        if os.path.exists(temp_sent_m4a):
            os.remove(temp_sent_m4a)

    # Stitch all sentences into one seamless news broadcast audio file
    # We can use sox if available, or ffmpeg, or afconvert
    # Let's check ffmpeg or python wave concatenation
    concat_wav = f"/tmp/{article_id}_full.wav"
    
    # We can convert all temp aiff/wav to a single wav using python wave
    import wave
    with wave.open(concat_wav, 'wb') as outfile:
        # read first file to get parameters
        first = True
        for f in temp_files:
            # Convert aiff to wav if needed using afconvert
            wav_temp = f if f.endswith(".wav") else f + ".wav"
            if not f.endswith(".wav"):
                subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@44100", f, wav_temp], check=True)
            
            with wave.open(wav_temp, 'rb') as infile:
                if first:
                    outfile.setparams(infile.getparams())
                    first = False
                outfile.writeframes(infile.readframes(infile.getnframes()))
            
            if not f.endswith(".wav") and os.path.exists(wav_temp):
                os.remove(wav_temp)

    # Convert stitched WAV to AAC M4A
    subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", concat_wav, final_output_path], check=True)
    print(f"  ✅ Saved stitched news audio: {final_output_path} (Total duration: {get_audio_duration(final_output_path):.2f}s)")

    # Cleanup temp
    for f in temp_files:
        if os.path.exists(f) and f != silence_wav:
            os.remove(f)
    if os.path.exists(concat_wav):
        os.remove(concat_wav)

# Save updated daily_news.json
with open(NEWS_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
print("✅ Successfully updated daily_news.json with exact millisecond timestamps!")

# Save updated voice_bank_manifest.json
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print(f"✅ Saved voice bank manifest with {len(manifest)} entries!")
