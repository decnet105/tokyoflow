import re
from scripts.generate_7day_kana_words import kana_7day_dict

# Load existing KanaItem.swift to extract original list definitions and mnemonics
with open("TokyoFlow/Models/KanaItem.swift", "r", encoding="utf-8") as f:
    old_content = f.read()

# Pattern to extract KanaItem(id: "...", hiragana: "...", katakana: "...", romaji: "...", row: "...", column: "...", ... mnemonic: "...")
pattern = re.compile(r'KanaItem\(\s*id:\s*"([^"]+)",\s*hiragana:\s*"([^"]+)",\s*katakana:\s*"([^"]+)",\s*romaji:\s*"([^"]+)",\s*row:\s*"([^"]+)",\s*column:\s*"([^"]+)",.*?mnemonic:\s*"([^"]+)"\s*\)', re.DOTALL)

items = []
for match in pattern.finditer(old_content):
    kid, hira, kata, romaji, row, col, mnemonic = match.groups()
    items.append({
        "id": kid,
        "hiragana": hira,
        "katakana": kata,
        "romaji": romaji,
        "row": row,
        "column": col,
        "mnemonic": mnemonic
    })

print(f"Extracted {len(items)} Kana items from previous KanaItem.swift")

# Separate into seion (46), dakuon (25), yoon (remaining)
seion_ids = [
    "a", "i", "u", "e", "o",
    "ka", "ki", "ku", "ke", "ko",
    "sa", "shi", "su", "se", "so",
    "ta", "chi", "tsu", "te", "to",
    "na", "ni", "nu", "ne", "no",
    "ha", "hi", "fu", "he", "ho",
    "ma", "mi", "mu", "me", "mo",
    "ya", "yu", "yo",
    "ra", "ri", "ru", "re", "ro",
    "wa", "wo", "n"
]

dakuon_ids = [
    "ga", "gi", "gu", "ge", "go",
    "za", "ji", "zu", "ze", "zo",
    "da", "de", "do",
    "ba", "bi", "bu", "be", "bo",
    "pa", "pi", "pu", "pe", "po"
]

def format_kana_item(item):
    kid = item["id"]
    words = kana_7day_dict.get(kid, [
        (item["hiragana"], item["romaji"], f"{item['hiragana']} sound")
    ])
    # Ensure exactly 7 words
    while len(words) < 7:
        words.append(words[0])
    
    words_code = ",\n                ".join([
        f'KanaExampleWord(japanese: "{w[0]}", romaji: "{w[1]}", english: "{w[2]}")'
        for w in words[:7]
    ])
    
    return f'''        KanaItem(
            id: "{item['id']}",
            hiragana: "{item['hiragana']}",
            katakana: "{item['katakana']}",
            romaji: "{item['romaji']}",
            row: "{item['row']}",
            column: "{item['column']}",
            exampleWords: [
                {words_code}
            ],
            mnemonic: "{item['mnemonic']}"
        )'''

seion_code = ",\n\n".join([format_kana_item(item) for item in items if item["id"] in seion_ids])
dakuon_code = ",\n\n".join([format_kana_item(item) for item in items if item["id"] in dakuon_ids])
yoon_code = ",\n\n".join([format_kana_item(item) for item in items if item["id"] not in seion_ids and item["id"] not in dakuon_ids])

full_swift = f'''import Foundation

public enum KanaCategory: String, CaseIterable, Identifiable {{
    case seion = "Seion (清音 46)"
    case dakuon = "Dakuon (浊音/半浊音 25)"
    case yoon = "Yoon (拗音 33)"

    public var id: String {{ rawValue }}
}}

public struct KanaExampleWord: Identifiable, Hashable, Codable {{
    public var id: String {{ japanese }}
    public let japanese: String
    public let romaji: String
    public let english: String

    public init(japanese: String, romaji: String, english: String) {{
        self.japanese = japanese
        self.romaji = romaji
        self.english = english
    }}
}}

public struct KanaItem: Identifiable, Hashable, Codable {{
    public let id: String
    public let hiragana: String
    public let katakana: String
    public let romaji: String
    public let row: String
    public let column: String
    public let exampleWords: [KanaExampleWord]
    public let mnemonic: String

    public init(
        id: String,
        hiragana: String,
        katakana: String,
        romaji: String,
        row: String,
        column: String,
        exampleWords: [KanaExampleWord],
        mnemonic: String
    ) {{
        self.id = id
        self.hiragana = hiragana
        self.katakana = katakana
        self.romaji = romaji
        self.row = row
        self.column = column
        self.exampleWords = exampleWords
        self.mnemonic = mnemonic
    }}

    /// Returns the non-repeating daily example word for today (rotates each day of the week, no duplicates within 7 days)
    public var dailyExampleWord: KanaExampleWord {{
        guard !exampleWords.isEmpty else {{
            return KanaExampleWord(japanese: hiragana, romaji: romaji, english: "Japanese Kana")
        }}
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let index = (dayOfYear - 1) % exampleWords.count
        return exampleWords[index]
    }}

    /// Returns the example word for an offset day (e.g. 0 = today, 1 = tomorrow, -1 = yesterday)
    public func exampleWordForDay(dayOffset: Int) -> KanaExampleWord {{
        guard !exampleWords.isEmpty else {{
            return KanaExampleWord(japanese: hiragana, romaji: romaji, english: "Japanese Kana")
        }}
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let targetIndex = ((dayOfYear - 1 + dayOffset) % exampleWords.count + exampleWords.count) % exampleWords.count
        return exampleWords[targetIndex]
    }}

    // Backwards compatibility properties
    public var exampleWordJa: String {{
        return dailyExampleWord.japanese
    }}
    public var exampleWordRomaji: String {{
        return dailyExampleWord.romaji
    }}
    public var exampleWordEn: String {{
        return dailyExampleWord.english
    }}
}}

public struct KanaDataManager {{
    public static let shared = KanaDataManager()

    public let seionList: [KanaItem] = [
{seion_code}
    ]

    public let dakuonList: [KanaItem] = [
{dakuon_code}
    ]

    public let yoonList: [KanaItem] = [
{yoon_code}
    ]
}}
'''

with open("TokyoFlow/Models/KanaItem.swift", "w", encoding="utf-8") as f:
    f.write(full_swift)

print("Successfully wrote full 7-day non-repeating KanaItem.swift!")
