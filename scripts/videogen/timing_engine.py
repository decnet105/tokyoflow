#!/usr/bin/env python3
"""
TokyoFlow Japanese • Millisecond Timing & Word Alignment Engine
Uses Whisper word-level timestamps and PyKakasi tokenization to extract
exact millisecond start/end timestamps for both Japanese and English audio clips.
"""

import os
import re
import pykakasi
import whisper

_kakasi = pykakasi.kakasi()
_whisper_model = None

def get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")
    return _whisper_model

def extract_tokens_from_text(sentence: str, custom_tokens: list = None) -> list:
    if custom_tokens:
        return custom_tokens
    
    res = _kakasi.convert(sentence)
    tokens = []
    for item in res:
        orig = item['orig']
        hira = item['hira']
        romaji = item['hepburn']
        clean = orig.replace('','').replace('','').replace('','').replace('','').strip()
        tokens.append({
            'orig': orig,
            'kana': hira if orig != hira else '',
            'romaji': romaji if clean else '',
            'raw_kana': hira
        })
    return tokens

def align_sentence_tokens_with_audio(audio_path: str, tokens: list) -> list:
    """
    Transcribes audio with Whisper word timestamps and aligns each token
    with an anticipatory 80ms lead time for crisp visual synchronization.
    """
    model = get_whisper_model()
    transcription = model.transcribe(audio_path, word_timestamps=True, language="ja")
    
    whisper_words = []
    for seg in transcription.get("segments", []):
        whisper_words.extend(seg.get("words", []))
        
    w_idx = 0
    total_w = len(whisper_words)
    aligned_tokens = []
    
    for tok in tokens:
        orig = tok["orig"]
        clean_orig = re.sub(r"[\s、。！？・「」『』（）,\.!\?]", "", orig)
        
        if not clean_orig:
            prev_end = aligned_tokens[-1]["end"] if aligned_tokens else 0.0
            aligned_tokens.append({
                **tok,
                "start": prev_end,
                "end": prev_end
            })
            continue
            
        matched_words = []
        matched_chars = ""
        
        while w_idx < total_w:
            w_item = whisper_words[w_idx]
            w_text = re.sub(r"[\s、。！？・「」『』（）,\.!\?]", "", w_item["word"])
            matched_words.append(w_item)
            matched_chars += w_text
            w_idx += 1
            if len(matched_chars) >= len(clean_orig):
                break
                
        if matched_words:
            # 80ms anticipatory lead offset for instant audio-visual sync
            start_t = max(0.0, float(matched_words[0]["start"]) - 0.08)
            end_t = float(matched_words[-1]["end"]) + 0.05
        else:
            prev_end = aligned_tokens[-1]["end"] if aligned_tokens else 0.0
            start_t = prev_end
            end_t = start_t + 0.5
            
        aligned_tokens.append({
            **tok,
            "start": start_t,
            "end": end_t
        })
        
    return aligned_tokens

def align_breakdown_with_english_audio(
    audio_path: str,
    vocab_count: int,
    grammar_title: str,
    total_duration: float
) -> dict:
    """
    Analyzes English explanation audio to determine time windows for
    highlighting each vocabulary card and the grammar spotlight box.
    """
    model = get_whisper_model()
    transcription = model.transcribe(audio_path, word_timestamps=True, language="en")
    segments = transcription.get("segments", [])
    
    # If segments exist, map roughly: first segments = vocab cards, remaining = grammar spotlight
    timings = {
        "active_vocab_idx": {}, # map (start, end) -> idx
        "spotlight_window": (0.0, 0.0)
    }
    
    if len(segments) >= 2:
        # First 1-2 seconds is intro
        intro_end = segments[0]["end"]
        # Last segment is usually grammar spotlight
        spotlight_start = segments[-1]["start"]
        timings["spotlight_window"] = (spotlight_start - 0.1, total_duration)
        
        # Middle time is distributed across vocab cards
        vocab_time_total = max(1.0, spotlight_start - intro_end)
        per_card = vocab_time_total / max(1, vocab_count)
        
        for i in range(vocab_count):
            c_start = intro_end + i * per_card
            c_end = intro_end + (i + 1) * per_card
            timings["active_vocab_idx"][i] = (c_start, c_end)
    else:
        # Fallback distribution
        midpoint = total_duration * 0.6
        per_card = midpoint / max(1, vocab_count)
        for i in range(vocab_count):
            timings["active_vocab_idx"][i] = (i * per_card, (i + 1) * per_card)
        timings["spotlight_window"] = (midpoint, total_duration)
        
    return timings
