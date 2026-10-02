#!/usr/bin/env python3
"""
TokyoFlow Japanese • Dual-Language Voice Synthesis Engine
Provides ultra-natural human voice synthesis:
- Japanese: `ja-JP-NanamiNeural` (Tokyo standard native speaker, relaxed natural cadence: rate="-6%", pitch="+3Hz")
- English: `en-US-AndrewNeural` (Young, energetic, natural conversational educator: rate="+2%", pitch="+0Hz")
"""

import os
import subprocess
import asyncio
import edge_tts

VOICE_JA_FEMALE = "ja-JP-NanamiNeural"
VOICE_JA_MALE = "ja-JP-KeitaNeural"
VOICE_EN_EXPLAINER = "en-US-AndrewNeural"

async def synthesize_speech(
    text: str,
    out_path: str,
    lang: str = "ja",
    rate: str = None,
    pitch: str = None
):
    """
    Synthesizes speech with edge_tts and normalizes output audio to 44.1kHz stereo AAC.
    Preserves Nanami's signature natural Tokyo cadence and sweetness.
    """
    if lang == "en":
        voice = VOICE_EN_EXPLAINER
        r = rate or "+2%"
        p = pitch or "+0Hz"
    elif lang == "ja_male":
        voice = VOICE_JA_MALE
        r = rate or "-4%"
        p = pitch or "-2Hz"
    else:
        voice = VOICE_JA_FEMALE
        r = rate or "-6%"
        p = pitch or "+3Hz"

    tmp_path = out_path + ".raw.mp3"
    comm = edge_tts.Communicate(text, voice, rate=r, pitch=p)
    await comm.save(tmp_path)

    # Clean 44.1kHz stereo conversion with high fidelity
    cmd = [
        "ffmpeg", "-y",
        "-i", tmp_path,
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-ac", "2",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
