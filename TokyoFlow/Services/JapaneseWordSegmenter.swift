import Foundation
import NaturalLanguage

public struct WordToken: Identifiable, Hashable {
    public let id: String
    public let index: Int
    public let text: String
    public let furigana: String
    public let romaji: String
    public let meaning: String
    public let moraWeight: Int

    public init(
        id: String = UUID().uuidString,
        index: Int = 0,
        text: String,
        furigana: String = "",
        romaji: String = "",
        meaning: String = "",
        moraWeight: Int = 1
    ) {
        self.id = id
        self.index = index
        self.text = text
        self.furigana = furigana
        self.romaji = romaji
        self.meaning = meaning
        self.moraWeight = max(1, moraWeight)
    }
}

public class JapaneseWordSegmenter {
    public static let shared = JapaneseWordSegmenter()

    private let commonVocabDict: [String: (furigana: String, romaji: String, meaning: String)] = [
        "JR東日本": ("じぇいあーるひがしにほん", "JR Higashi-Nihon", "JR East (JR东日本)"),
        "東京": ("とうきょう", "toukyou", "Tokyo (东京)"),
        "近く": ("ちかく", "chikaku", "Nearby (附近)"),
        "走る": ("はしる", "hashiru", "To run / operate (行驶)"),
        "電車": ("でんしゃ", "densha", "Train (电车)"),
        "終電": ("しゅうでん", "shuuden", "Last train (末班车)"),
        "時間": ("じかん", "jikan", "Time (时间)"),
        "早める": ("はやめる", "hayameru", "To advance / make earlier (提前)"),
        "発表": ("はっぴょう", "happyou", "Announcement (宣布/发表)"),
        "山手線": ("やまのてせん", "yamanotesen", "Yamanote Line (山手线)"),
        "中央線": ("ちゅうおうせん", "chuuousen", "Chuo Line (中央线)"),
        "主な": ("おもな", "omona", "Main / Major (主要的)"),
        "路線": ("ろせん", "rosen", "Train line / Route (路线)"),
        "深夜": ("しんや", "shinya", "Late night (深夜)"),
        "保守": ("ほしゅ", "hoshu", "Maintenance (维护/检修)"),
        "作業": ("さぎょう", "sagyou", "Work / Operations (作业)"),
        "確保": ("かくほ", "kakuho", "Secure / Ensure (确保)"),
        "理由": ("りゆう", "riyuu", "Reason (理由)"),
        "台風": ("たいふう", "taifuu", "Typhoon (台风)"),
        "接近": ("せっきん", "sekkin", "Approaching (接近)"),
        "関東": ("かんとう", "kantou", "Kanto region (关东地区)"),
        "大雨": ("おおあめ", "ooame", "Heavy rain (暴雨)"),
        "注意": ("ちゅうい", "chuui", "Caution (注意)"),
        "呼びかけています": ("よびかけています", "yobikaketeimasu", "Are calling for (呼吁)"),
        "気象庁": ("きしょうちょう", "kishouchou", "Meteorological Agency (气象厅)"),
        "土砂災害": ("どしゃさいがい", "doshasagai", "Landslide disaster (泥石流灾害)"),
        "警戒": ("けいかい", "keikai", "Vigilance / Alert (警戒)"),
        "訪日": ("ほうにち", "hounichi", "Visiting Japan (访日)"),
        "外国人": ("がいこくじん", "gaikokujin", "Foreigners (外国人)"),
        "観光客": ("かんこうきゃく", "kankoukyaku", "Tourists (游客)"),
        "過去最多": ("かこさいた", "kako saita", "Record high (历史最多)"),
        "円安": ("えんやす", "enyasu", "Weak yen (日元贬值)"),
        "影響": ("えいきょう", "eikyou", "Impact / Influence (影响)"),
        "買い物": ("かいもの", "kaimono", "Shopping (购物)"),
        "消費": ("しょうひ", "shouhi", "Consumption (消费)"),
        "拡大": ("かくだい", "kakudai", "Expansion (扩大)"),
        "政府": ("せいふ", "seifu", "Government (政府)"),
        "観光地": ("かんこうち", "kankouchi", "Sightseeing area (观光地)"),
        "混雑": ("こんざつ", "konzatsu", "Congestion (拥挤)"),
        "対策": ("たいさく", "taisaku", "Countermeasures (对策)"),
        "進める": ("すすめる", "susumeru", "To promote (推进)"),
        "方針": ("ほうしん", "houshin", "Policy (方针)"),
        "温めてください": ("あたためてください", "atatamete kudasai", "Please warm it up (请帮我加热)"),
        "袋は大丈夫です": ("ふくろはだいじょうぶです", "fukuro wa daijoubu desu", "No bag needed (不需要塑料袋)"),
        "お会計": ("おかいけい", "okaikei", "Check / Bill (结账)"),
        "領収書": ("りょうしゅうしょ", "ryoushuusho", "Receipt (发票)"),
        "生ビール": ("なまびーる", "namabiiru", "Draft beer (生啤酒)"),
        "新宿駅": ("しんじゅくえき", "shinjukueki", "Shinjuku Station (新宿站)"),
        "乗り換え": ("のりかえ", "norikae", "Transfer (换乘)"),
        "いらっしゃいませ": ("いらっしゃいませ", "irasshaimase", "Welcome (欢迎光临)"),
        "ありがとうございます": ("ありがとうございます", "arigatou gozaimasu", "Thank you very much (非常感谢)")
    ]

    private init() {}

    /// Segments Japanese text into grammatical word tokens with furigana, romaji, contextual gloss, and mora duration weights
    public func segment(text: String, furiganaReference: String = "") -> [WordToken] {
        if text.isEmpty { return [] }

        var tokens: [WordToken] = []
        let tokenizer = NLTokenizer(unit: .word)
        tokenizer.string = text
        tokenizer.setLanguage(.japanese)

        let range = text.startIndex..<text.endIndex
        var currentIndex = 0
        tokenizer.enumerateTokens(in: range) { tokenRange, _ in
            let word = String(text[tokenRange]).trimmingCharacters(in: .whitespacesAndNewlines)
            if !word.isEmpty && word != " " && word != "　" {
                let weight = max(1, word.count)
                if let dictEntry = self.commonVocabDict[word] {
                    tokens.append(WordToken(index: currentIndex, text: word, furigana: dictEntry.furigana, romaji: dictEntry.romaji, meaning: dictEntry.meaning, moraWeight: weight))
                } else {
                    let transliterated = self.transliterateToRomaji(word)
                    tokens.append(WordToken(index: currentIndex, text: word, furigana: "", romaji: transliterated, meaning: "", moraWeight: weight))
                }
                currentIndex += 1
            }
            return true
        }

        // Fallback if tokenizer returned empty
        if tokens.isEmpty {
            tokens.append(WordToken(index: 0, text: text, furigana: furiganaReference, romaji: transliterateToRomaji(text), meaning: "", moraWeight: max(1, text.count)))
        }

        return tokens
    }

    private func transliterateToRomaji(_ text: String) -> String {
        let mutableString = NSMutableString(string: text) as CFMutableString
        if CFStringTransform(mutableString, nil, kCFStringTransformMandarinLatin, false) {
            // Alternatively use Latin transform
        }
        return (mutableString as String).replacingOccurrences(of: "\n", with: " ")
    }
}
