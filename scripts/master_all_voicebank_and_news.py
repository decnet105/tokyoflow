import os
import glob
import subprocess
import json

VOICEBANK_DIR = "TokyoFlow/Resources/Audio/VoiceBank"
AUDIO_DIR = "TokyoFlow/Resources/Audio"

# Studio-grade broadcast mastering filter:
# 1) Equalizer 280Hz +2.5dB (warm chest resonance)
# 2) Equalizer 3200Hz +1.2dB (clear vocal articulation)
# 3) Equalizer 7500Hz -3.0dB (de-harshing digital sibilance)
# 4) Lowpass 9500Hz (cuts harsh tinny synthesis harmonics)
# 5) High quality 256kbps 48kHz AAC mastering
ffmpeg_filter = "equalizer=f=280:t=q:w=1.2:g=2.5,equalizer=f=3200:t=q:w=2.0:g=1.2,equalizer=f=7500:t=q:w=2.5:g=-3.0,lowpass=f=9500,aresample=48000"

print("🎛️ Mastering all VoiceBank and News audio files with broadcast warmth & de-harshing filter...")

# 1. Master news files
for news_file in ["nhk_news_001.m4a", "nhk_news_002.m4a", "nhk_news_003.m4a"]:
    p = os.path.join(AUDIO_DIR, news_file)
    if os.path.exists(p):
        tmp_out = f"/tmp/mastered_{news_file}"
        try:
            subprocess.run([
                "/opt/homebrew/bin/ffmpeg", "-y", "-i", p,
                "-af", ffmpeg_filter,
                "-c:a", "aac", "-b:a", "256k",
                tmp_out
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["mv", tmp_out, p], check=True)
            print(f"  ✅ Mastered news audio: {news_file}")
        except Exception as e:
            print(f"Error mastering {news_file}: {e}")

# 2. Master VoiceBank files
all_m4a = glob.glob(os.path.join(VOICEBANK_DIR, "*.m4a"))
print(f"Mastering {len(all_m4a)} VoiceBank audio files...")

mastered_count = 0
for idx, p in enumerate(all_m4a):
    fname = os.path.basename(p)
    tmp_out = f"/tmp/vb_{fname}"
    try:
        subprocess.run([
            "/opt/homebrew/bin/ffmpeg", "-y", "-i", p,
            "-af", ffmpeg_filter,
            "-c:a", "aac", "-b:a", "256k",
            tmp_out
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["mv", tmp_out, p], check=True)
        mastered_count += 1
    except Exception as e:
        continue

print(f"🎉 Successfully mastered {mastered_count} audio files to studio-grade warm NHK standard!")
