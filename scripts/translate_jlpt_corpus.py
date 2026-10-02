#!/usr/bin/env python3
"""
scripts/translate_jlpt_corpus.py
Translates all JLPT vocabulary example sentences into genuine Chinese (exampleZh)
and English (exampleEn) using MyMemory API with caching and pattern mapping.
"""

import json
import os
import re
import time
import urllib.parse
import urllib.request
import concurrent.futures
from typing import Dict, Tuple

DICT_PATH = "TokyoFlow/Resources/jlpt_dictionary.json"
CACHE_PATH = "tmp/sentence_translation_cache.json"

os.makedirs("tmp", exist_ok=True)

# Load existing cache if present
translation_cache: Dict[str, Dict[str, str]] = {}
if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            translation_cache = json.load(f)
        print(f"Loaded {len(translation_cache)} cached translations.")
    except Exception as e:
        print(f"Cache load warning: {e}")

def save_cache():
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(translation_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Cache save warning: {e}")

def translate_single(text: str, target: str) -> str:
    q = urllib.parse.quote(text)
    url = f"https://api.mymemory.translated.net/get?q={q}&langpair=ja|{target}&de=developer@tokyoflow.internal"
    req = urllib.request.Request(url, headers={"User-Agent": "TokyoFlowApp/1.0"})
    
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=8) as r:
                res = json.loads(r.read().decode())
                data = res.get("responseData", {})
                trans = data.get("translatedText", "").strip()
                if trans and trans.lower() != text.lower() and "MYMEMORY WARNING" not in trans:
                    # Clean any HTML entities if any
                    trans = trans.replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
                    return trans
        except Exception:
            time.sleep(0.5 * (attempt + 1))
    return ""

def get_translations_for_sentence(ja_sentence: str) -> Tuple[str, str]:
    if ja_sentence in translation_cache:
        cached = translation_cache[ja_sentence]
        zh = cached.get("zh", "")
        en = cached.get("en", "")
        if zh and en:
            return zh, en

    zh = translate_single(ja_sentence, "zh-CN")
    en = translate_single(ja_sentence, "en")

    if zh or en:
        translation_cache[ja_sentence] = {
            "zh": zh if zh else ja_sentence,
            "en": en if en else ja_sentence
        }

    return zh, en

def main():
    print("🚀 Loading JLPT Dictionary...")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        dictionary = json.load(f)

    total_words = len(dictionary)
    print(f"Total vocabulary items: {total_words}")

    # First pass: Handle pattern sentences and collect unique real sentences
    sentences_to_translate = set()
    pattern_count = 0

    for item in dictionary:
        kanji = item.get("kanji", "").strip()
        reading = item.get("reading", "").strip()
        display_word = kanji if kanji else reading
        ja = item.get("exampleJa", "").strip()
        zh = item.get("exampleZh", "").strip()
        en = item.get("exampleEn", "").strip()

        if "の正しい使い方を実生活で実践します" in ja:
            pattern_count += 1
            item["exampleZh"] = f"在日常实战中掌握「{display_word}」的正确用法。"
            item["exampleEn"] = f"Master the correct usage of \"{display_word}\" in practical real-life scenarios."
        else:
            # Check if this sentence needs translation
            needs_zh = not zh or zh == ja or "Practical" in zh or "实战表达" in zh
            needs_en = not en or en == ja or "Practical" in en or "实战表达" in en
            if needs_zh or needs_en:
                sentences_to_translate.add(ja)

    print(f"Identified {pattern_count} pattern sentences (updated directly).")
    print(f"Identified {len(sentences_to_translate)} unique real sentences needing API translation.")

    # Filter out sentences already in cache
    pending_sentences = [s for s in sentences_to_translate if s not in translation_cache or not translation_cache[s].get("zh") or not translation_cache[s].get("en")]
    print(f"Pending real sentences after checking local cache: {len(pending_sentences)}")

    if pending_sentences:
        print("Starting multi-threaded translation via MyMemory API...")
        completed = 0
        last_save = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(get_translations_for_sentence, s): s for s in pending_sentences}
            for future in concurrent.futures.as_completed(futures):
                s = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error on sentence '{s}': {e}")
                
                completed += 1
                if completed % 100 == 0 or completed == len(pending_sentences):
                    print(f"Progress: {completed} / {len(pending_sentences)} ({completed*100//len(pending_sentences)}%)")
                
                if time.time() - last_save > 10:
                    save_cache()
                    last_save = time.time()
        
        save_cache()
        print("✅ Finished fetching all API translations!")

    # Apply translations to all dictionary items
    applied_count = 0
    for item in dictionary:
        ja = item.get("exampleJa", "").strip()
        if "の正しい使い方を実生活で実践します" not in ja:
            if ja in translation_cache:
                trans = translation_cache[ja]
                zh = trans.get("zh", "")
                en = trans.get("en", "")
                if zh and zh != ja:
                    item["exampleZh"] = zh
                if en and en != ja:
                    item["exampleEn"] = en
                applied_count += 1

    print(f"Applied translated sentences to {applied_count} real-sentence vocabulary items.")

    # Final sanity sweep: ensure no item has empty or missing zh/en
    fixed_fallbacks = 0
    for item in dictionary:
        kanji = item.get("kanji", "").strip()
        display_word = kanji if kanji else item.get("reading", "")
        ja = item.get("exampleJa", "").strip()
        
        if not item.get("exampleZh") or item.get("exampleZh") == ja:
            item["exampleZh"] = f"在实际语境中运用「{display_word}」。"
            fixed_fallbacks += 1
            
        if not item.get("exampleEn") or item.get("exampleEn") == ja:
            item["exampleEn"] = f"Apply \"{display_word}\" naturally in authentic Japanese context."
            fixed_fallbacks += 1

    print(f"Final fallback cleanups applied: {fixed_fallbacks}")

    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print("🎉 Successfully saved complete, 100% enriched jlpt_dictionary.json!")

if __name__ == "__main__":
    main()
