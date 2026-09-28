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
    
    private let tokenCache = NSCache<NSString, NSArray>()

    private let commonVocabDict: [String: (furigana: String, romaji: String, meaning: String)] = [
        "JR東日本": ("じぇいあーるひがしにほん", "JR Higashi-Nihon", "JR East (East Japan Railway)"),
        "東京": ("とうきょう", "toukyou", "Tokyo"),
        "近く": ("ちかく", "chikaku", "Nearby / Close to"),
        "走る": ("はしる", "hashiru", "To run / operate"),
        "電車": ("でんしゃ", "densha", "Train"),
        "終電": ("しゅうでん", "shuuden", "Last train"),
        "時間": ("じかん", "jikan", "Time / Schedule"),
        "早める": ("はやめる", "hayameru", "To advance / make earlier"),
        "発表": ("はっぴょう", "happyou", "Announcement / Press release"),
        "山手線": ("やまのてせん", "yamanotesen", "Yamanote Line"),
        "中央線": ("ちゅうおうせん", "chuuousen", "Chuo Line"),
        "主な": ("おもな", "omona", "Main / Major"),
        "路線": ("ろせん", "rosen", "Train line / Route"),
        "深夜": ("しんや", "shinya", "Late night / Midnight"),
        "保守": ("ほしゅ", "hoshu", "Maintenance / Inspection"),
        "作業": ("さぎょう", "sagyou", "Work / Track operations"),
        "確保": ("かくほ", "kakuho", "Secure / Ensure"),
        "理由": ("りゆう", "riyuu", "Reason / Cause"),
        "台風": ("たいふう", "taifuu", "Typhoon"),
        "接近": ("せっきん", "sekkin", "Approaching / Drawing near"),
        "関東": ("かんとう", "kantou", "Kanto region"),
        "大雨": ("おおあめ", "ooame", "Heavy rain"),
        "注意": ("ちゅうい", "chuui", "Caution / Warning"),
        "呼びかけています": ("よびかけています", "yobikaketeimasu", "Urging / Calling for"),
        "気象庁": ("きしょうちょう", "kishouchou", "Japan Meteorological Agency"),
        "土砂災害": ("どしゃさいがい", "doshasagai", "Landslide / Mudslide hazard"),
        "警戒": ("けいかい", "keikai", "Vigilance / High alert"),
        "訪日": ("ほうにち", "hounichi", "Visiting Japan"),
        "外国人": ("がいこくじん", "gaikokujin", "Foreign travelers / Foreigners"),
        "観光客": ("かんこうきゃく", "kankoukyaku", "Tourists / Sightseers"),
        "過去最多": ("かこさいた", "kako saita", "Record high / All-time peak"),
        "円安": ("えんやす", "enyasu", "Weak yen / Yen depreciation"),
        "影響": ("えいきょう", "eikyou", "Impact / Influence"),
        "買い物": ("かいもの", "kaimono", "Shopping"),
        "消費": ("しょうひ", "shouhi", "Consumer spending / Consumption"),
        "拡大": ("かくだい", "kakudai", "Expansion / Increase"),
        "政府": ("せいふ", "seifu", "Government"),
        "観光地": ("かんこうち", "kankouchi", "Sightseeing destination"),
        "混雑": ("こんざつ", "konzatsu", "Congestion / Crowding"),
        "対策": ("たいさく", "taisaku", "Countermeasures / Policy steps"),
        "進める": ("すすめる", "susumeru", "To advance / promote"),
        "方針": ("ほうしん", "houshin", "Policy / Plan of action"),
        "温めてください": ("あたためてください", "atatamete kudasai", "Please heat this up"),
        "袋は大丈夫です": ("ふくろはだいじょうぶです", "fukuro wa daijoubu desu", "No bag needed, thank you"),
        "お会計": ("おかいけい", "okaikei", "Check / Bill, please"),
        "領収書": ("りょうしゅうしょ", "ryoushuusho", "Formal receipt"),
        "生ビール": ("なまびーる", "namabiiru", "Draft beer"),
        "新宿駅": ("しんじゅくえき", "shinjukueki", "Shinjuku Station"),
        "乗り換え": ("のりかえ", "norikae", "Transfer / Connection"),
        "いらっしゃいませ": ("いらっしゃいませ", "irasshaimase", "Welcome!"),
        "ありがとうございます": ("ありがとうございます", "arigatou gozaimasu", "Thank you very much")
    ]

    private init() {}

    /// Segments Japanese text into grammatical word tokens with furigana, romaji, contextual gloss, and mora duration weights
    public func segment(text: String, furiganaReference: String = "") -> [WordToken] {
        if text.isEmpty { return [] }

        let nsKey = text as NSString
        if let cached = tokenCache.object(forKey: nsKey) as? [WordToken] {
            return cached
        }

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

        tokenCache.setObject(tokens as NSArray, forKey: nsKey)
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
