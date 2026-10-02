import json
import pykakasi

k = pykakasi.kakasi()

def to_spaced_ruby(text: str) -> str:
    if not text:
        return ""
    result = k.convert(text)
    parts = []
    for item in result:
        orig = item["orig"]
        hira = item["hira"]
        if any("\u4e00" <= c <= "\u9fff" for c in orig) and hira != orig:
            parts.append(f"{orig}({hira})")
        else:
            parts.append(orig)
    return " ".join(parts)

def main():
    dict_path = "TokyoFlow/Resources/jlpt_dictionary.json"
    with open(dict_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    for w in words:
        ex = w.get("exampleJa", "").strip()
        if ex:
            w["exampleFurigana"] = to_spaced_ruby(ex)

    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"✅ Spaced ruby furigana generated for all {len(words)} dictionary items.")

if __name__ == "__main__":
    main()
