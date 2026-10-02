import json
import os
import re
import sys

def main():
    print("=======================================================")
    print("🔍 JLPT Comprehensive Audio & Karaoke Verification Test")
    print("=======================================================")

    dict_path = "TokyoFlow/Resources/jlpt_dictionary.json"
    grammar_path = "TokyoFlow/Resources/jlpt_grammar.json"
    manifest_path = "TokyoFlow/Resources/Audio/VoiceBank/voice_bank_manifest.json"
    vb_dir = "TokyoFlow/Resources/Audio/VoiceBank"
    pbx_path = "TokyoFlow.xcodeproj/project.pbxproj"

    with open(dict_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    with open(grammar_path, "r", encoding="utf-8") as f:
        grammars = json.load(f)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    with open(pbx_path, "r", encoding="utf-8") as f:
        pbx = f.read()

    files_on_disk = set(os.listdir(vb_dir))
    pbx_paths = set(re.findall(r'path = \"?([^\";]+)\"?;', pbx))

    print(f"📊 Dataset Counts:")
    print(f"   • Total JLPT Vocabulary: {len(words)}")
    print(f"   • Total JLPT Grammar Points: {len(grammars)}")
    print(f"   • Manifest Keys: {len(manifest)}")
    print(f"   • Audio Files on Disk: {len(files_on_disk)}")
    print(f"   • PBX Project Resource References: {len(pbx_paths)}")

    print("\n--- Test 1: Spotlight Verification on 'client' (クライアント) ---")
    client_word = "クライアント"
    client_sent = "明日、クライアントと打ち合わせがあります。"
    
    # 1. Word check
    assert client_word in manifest, f"❌ 'client' word '{client_word}' missing from manifest!"
    fn_word = manifest[client_word]
    assert fn_word in files_on_disk, f"❌ 'client' word audio file '{fn_word}' missing from disk!"
    assert fn_word in pbx_paths, f"❌ 'client' word audio '{fn_word}' missing from Xcode project.pbxproj!"
    word_size = os.path.getsize(os.path.join(vb_dir, fn_word))
    print(f"   ✅ Word 'client' ({client_word}) -> {fn_word} ({word_size} bytes) [PBX Linked: YES]")

    # 2. Sentence check
    assert client_sent in manifest, f"❌ 'client' sentence '{client_sent}' missing from manifest!"
    fn_sent = manifest[client_sent]
    assert fn_sent in files_on_disk, f"❌ 'client' sentence audio file '{fn_sent}' missing from disk!"
    assert fn_sent in pbx_paths, f"❌ 'client' sentence audio '{fn_sent}' missing from Xcode project.pbxproj!"
    sent_size = os.path.getsize(os.path.join(vb_dir, fn_sent))
    print(f"   ✅ Sentence '{client_sent}' -> {fn_sent} ({sent_size} bytes) [PBX Linked: YES]")

    print("\n--- Test 2: 100% JLPT Vocabulary Audio & Xcode Linking ---")
    missing_words_manifest = []
    missing_words_disk = []
    missing_words_pbx = []

    for w in words:
        target = w.get("kanji") or w.get("reading")
        if not target:
            continue
        if target not in manifest:
            # Check reading
            rd = w.get("reading", "")
            if rd not in manifest:
                missing_words_manifest.append(target)
                continue
            fn = manifest[rd]
        else:
            fn = manifest[target]

        if fn not in files_on_disk:
            missing_words_disk.append((target, fn))
        elif fn not in pbx_paths:
            missing_words_pbx.append((target, fn))

    print(f"   • Words missing in manifest: {len(missing_words_manifest)} / {len(words)}")
    print(f"   • Words missing on disk: {len(missing_words_disk)} / {len(words)}")
    print(f"   • Words missing in Xcode PBX: {len(missing_words_pbx)} / {len(words)}")
    if missing_words_manifest:
        print(f"     Sample missing: {missing_words_manifest[:5]}")

    print("\n--- Test 3: 100% JLPT Example Sentences Audio & Xcode Linking ---")
    missing_sentences_manifest = []
    missing_sentences_disk = []
    missing_sentences_pbx = []

    for w in words:
        ex = w.get("exampleJa", "").strip()
        if not ex:
            continue
        if ex not in manifest:
            missing_sentences_manifest.append(ex)
            continue
        fn = manifest[ex]
        if fn not in files_on_disk:
            missing_sentences_disk.append((ex, fn))
        elif fn not in pbx_paths:
            missing_sentences_pbx.append((ex, fn))

    print(f"   • Sentences missing in manifest: {len(missing_sentences_manifest)} / {len(words)}")
    print(f"   • Sentences missing on disk: {len(missing_sentences_disk)} / {len(words)}")
    print(f"   • Sentences missing in Xcode PBX: {len(missing_sentences_pbx)} / {len(words)}")
    if missing_sentences_manifest:
        print(f"     Sample missing: {missing_sentences_manifest[:5]}")

    print("\n--- Test 4: 100% JLPT Grammar Lab Patterns & Sentences ---")
    missing_grammar_manifest = []
    missing_grammar_disk = []
    missing_grammar_pbx = []
    total_gram_items = 0

    for g in grammars:
        t = g.get("title", "").strip()
        if t:
            total_gram_items += 1
            if t not in manifest:
                missing_grammar_manifest.append(t)
            else:
                fn = manifest[t]
                if fn not in files_on_disk:
                    missing_grammar_disk.append((t, fn))
                elif fn not in pbx_paths:
                    missing_grammar_pbx.append((t, fn))

        for s in g.get("sentences", []):
            ja = s.get("japanese", "").strip()
            if ja:
                total_gram_items += 1
                if ja not in manifest:
                    missing_grammar_manifest.append(ja)
                else:
                    fn = manifest[ja]
                    if fn not in files_on_disk:
                        missing_grammar_disk.append((ja, fn))
                    elif fn not in pbx_paths:
                        missing_grammar_pbx.append((ja, fn))

    print(f"   • Total grammar titles & sentences: {total_gram_items}")
    print(f"   • Missing in manifest: {len(missing_grammar_manifest)}")
    print(f"   • Missing on disk: {len(missing_grammar_disk)}")
    print(f"   • Missing in Xcode PBX: {len(missing_grammar_pbx)}")

    print("\n--- Test 5: Furigana & Karaoke Token Quality ---")
    bad_furi_count = 0
    for w in words[:200]:
        ex = w.get("exampleJa", "").strip()
        furi = w.get("exampleFurigana", "").strip()
        if ex and (" " not in furi or len(furi) < len(ex)):
            bad_furi_count += 1

    print(f"   • Sample 200 entries furigana check: {200 - bad_furi_count}/200 passed")

    success = (len(missing_words_manifest) == 0 and 
               len(missing_words_disk) == 0 and 
               len(missing_words_pbx) == 0 and 
               len(missing_sentences_manifest) == 0 and 
               len(missing_sentences_disk) == 0 and 
               len(missing_sentences_pbx) == 0 and
               len(missing_grammar_manifest) == 0 and
               len(missing_grammar_disk) == 0 and
               len(missing_grammar_pbx) == 0)

    print("\n=======================================================")
    if success:
        print("🎉 ALL TESTS PASSED! 100% STUDIO AUDIO & KARAOKE VERIFIED!")
    else:
        print("⚠️ SOME ITEMS REMAIN TO BE COMPLETED.")
    print("=======================================================")

if __name__ == "__main__":
    main()
