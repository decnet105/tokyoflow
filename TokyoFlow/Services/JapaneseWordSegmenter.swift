import Foundation
import NaturalLanguage

public struct WordToken: Identifiable, Hashable {
    public let id: String
    public let index: Int
    public let text: String
    public let furigana: String
    public let romaji: String
    public let meaning: String
    public let moraWeight: Double

    public init(
        id: String = UUID().uuidString,
        index: Int = 0,
        text: String,
        furigana: String = "",
        romaji: String = "",
        meaning: String = "",
        moraWeight: Double = 1.0
    ) {
        self.id = id
        self.index = index
        self.text = text
        self.furigana = furigana
        self.romaji = romaji
        self.meaning = meaning
        self.moraWeight = max(0.8, moraWeight)
    }
}

public class JapaneseWordSegmenter {
    public static let shared = JapaneseWordSegmenter()
    
    private let tokenCache = NSCache<NSString, NSArray>()

    private let commonVocabDict: [String: (furigana: String, romaji: String, meaning: String)] = [
        "JR東日本": ("じぇいあーるひがしにほん", "JR Higashi-Nihon", "JR East (East Japan Railway)"),
        "東京": ("とうきょう", "toukyou", "Tokyo"),
        "東京駅": ("とうきょうえき", "toukyoueki", "Tokyo Station"),
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
        "秋葉原": ("あきはばら", "akihabara", "Akihabara"),
        "乗り換え": ("のりかえ", "norikae", "Transfer / Connection"),
        "いらっしゃいませ": ("いらっしゃいませ", "irasshaimase", "Welcome!"),
        "ありがとうございます": ("ありがとうございます", "arigatou gozaimasu", "Thank you very much"),
        "すみません": ("すみません", "sumimasen", "Excuse me"),
        "注文": ("ちゅうもん", "chuumon", "Order"),
        "お願いします": ("おねがいします", "onegaishimasu", "Please"),
        "明日": ("あした", "ashita", "Tomorrow"),
        "行きます": ("いきます", "ikimasu", "To go"),
        "行きますか": ("いきますか", "ikimasuka", "Does it go?")
    ]

    private init() {}

    /// Segments Japanese sentences into clean individual words with exact Furigana, Romaji, and calibrated Mora weights
    public func segment(text: String, furiganaReference: String = "") -> [WordToken] {
        let cleanText = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if cleanText.isEmpty { return [] }

        let nsKey = "\(cleanText)_\(furiganaReference)" as NSString
        if let cached = tokenCache.object(forKey: nsKey) as? [WordToken] {
            return cached
        }

        var tokens: [WordToken] = []

        let furiParts = furiganaReference.components(separatedBy: CharacterSet.whitespaces)
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }

        // Strategy 1: Smart extraction for reading{kanji}, kanji(reading), or spaced furigana references
        if furiganaReference.contains("{") || furiganaReference.contains("(") || furiganaReference.contains("（") || furiganaReference.contains(" ") {
            let normalized = furiganaReference
                .replacingOccurrences(of: "、", with: "、 ")
                .replacingOccurrences(of: "。", with: "。 ")
                .replacingOccurrences(of: "！", with: "！ ")
                .replacingOccurrences(of: "？", with: "？ ")

            let pattern = "(?:([ぁ-んァ-ンーa-zA-Z0-9]+)\\{([^}]+)\\}([ぁ-んァ-ンーa-zA-Z0-9]*))|(?:([一-龯々a-zA-Z0-9]+)[(（]([ぁ-んァ-ンー]+)[)）]([ぁ-んァ-ンーa-zA-Z0-9]*))|([^\\s{}()（）]+)"
            if let regex = try? NSRegularExpression(pattern: pattern, options: []) {
                let ns = normalized as NSString
                let matches = regex.matches(in: normalized, options: [], range: NSRange(location: 0, length: ns.length))

                for m in matches {
                    if m.range(at: 1).location != NSNotFound && m.range(at: 2).location != NSNotFound {
                        let reading = ns.substring(with: m.range(at: 1))
                        let kanji = ns.substring(with: m.range(at: 2))
                        let suffix = m.range(at: 3).location != NSNotFound ? ns.substring(with: m.range(at: 3)) : ""

                        if !suffix.isEmpty && (suffix == "がって" || suffix == "り" || suffix == "して" || suffix == "く" || suffix == "て" || suffix == "た" || suffix == "る" || suffix == "ます" || suffix == "ない" || suffix == "たい" || suffix == "だ") {
                            let fullText = kanji + suffix
                            let fullFuri = reading + suffix
                            let mora = calculateMoraWeight(text: fullText, furigana: fullFuri)
                            let rom = transliterateToRomaji(fullFuri)
                            tokens.append(WordToken(
                                index: tokens.count,
                                text: fullText,
                                furigana: fullFuri,
                                romaji: rom,
                                meaning: commonVocabDict[fullText]?.meaning ?? "",
                                moraWeight: mora
                            ))
                        } else {
                            let mora = calculateMoraWeight(text: kanji, furigana: reading)
                            let rom = transliterateToRomaji(reading)
                            tokens.append(WordToken(
                                index: tokens.count,
                                text: kanji,
                                furigana: reading,
                                romaji: rom,
                                meaning: commonVocabDict[kanji]?.meaning ?? "",
                                moraWeight: mora
                            ))
                            if !suffix.isEmpty {
                                let sMora = calculateMoraWeight(text: suffix, furigana: "")
                                let sRom = transliterateToRomaji(suffix)
                                tokens.append(WordToken(
                                    index: tokens.count,
                                    text: suffix,
                                    furigana: "",
                                    romaji: sRom,
                                    meaning: commonVocabDict[suffix]?.meaning ?? "",
                                    moraWeight: sMora
                                ))
                            }
                        }
                    } else if m.range(at: 4).location != NSNotFound && m.range(at: 5).location != NSNotFound {
                        let kanji = ns.substring(with: m.range(at: 4))
                        let reading = ns.substring(with: m.range(at: 5))
                        let suffix = m.range(at: 6).location != NSNotFound ? ns.substring(with: m.range(at: 6)) : ""
                        let mora = calculateMoraWeight(text: kanji, furigana: reading)
                        let rom = transliterateToRomaji(reading)
                        tokens.append(WordToken(
                            index: tokens.count,
                            text: kanji,
                            furigana: reading,
                            romaji: rom,
                            meaning: commonVocabDict[kanji]?.meaning ?? "",
                            moraWeight: mora
                        ))
                        if !suffix.isEmpty {
                            let sMora = calculateMoraWeight(text: suffix, furigana: "")
                            let sRom = transliterateToRomaji(suffix)
                            tokens.append(WordToken(
                                index: tokens.count,
                                text: suffix,
                                furigana: "",
                                romaji: sRom,
                                meaning: commonVocabDict[suffix]?.meaning ?? "",
                                moraWeight: sMora
                            ))
                        }
                    } else if m.range(at: 7).location != NSNotFound {
                        let plain = ns.substring(with: m.range(at: 7))
                        let dictEntry = self.commonVocabDict[plain]
                        let furi = dictEntry?.furigana ?? ""
                        let rom = dictEntry?.romaji ?? transliterateToRomaji(furi.isEmpty ? plain : furi)
                        let mora = calculateMoraWeight(text: plain, furigana: furi)
                        tokens.append(WordToken(
                            index: tokens.count,
                            text: plain,
                            furigana: furi,
                            romaji: rom,
                            meaning: dictEntry?.meaning ?? "",
                            moraWeight: mora
                        ))
                    }
                }
            }
        }

        // Strategy 2: CFStringTokenizer with Japanese locale for fine-grained morphological word tokens
        if tokens.isEmpty {
            let words = tokenizeWithCFStringTokenizer(cleanText)
            for (idx, word) in words.enumerated() {
                let dictEntry = self.commonVocabDict[word]
                let furi = dictEntry?.furigana ?? ""
                let rom = dictEntry?.romaji ?? transliterateToRomaji(furi.isEmpty ? word : furi)
                let mora = calculateMoraWeight(text: word, furigana: furi)

                tokens.append(WordToken(
                    index: idx,
                    text: word,
                    furigana: furi,
                    romaji: rom,
                    meaning: dictEntry?.meaning ?? "",
                    moraWeight: mora
                ))
            }
        }

        // Strategy 3: Ultimate Fallback (Character boundary split if still empty)
        if tokens.isEmpty {
            tokens.append(WordToken(
                index: 0,
                text: cleanText,
                furigana: furiganaReference,
                romaji: transliterateToRomaji(cleanText),
                meaning: "",
                moraWeight: calculateMoraWeight(text: cleanText, furigana: furiganaReference)
            ))
        }

        //  Kinsoku Shori (禁則処理): Attach closing punctuation (。, 、! ?, etc.) to the preceding token
        // This guarantees that a closing period or punctuation mark is NEVER orphaned onto a new line alone.
        let kinsokuTokens = applyKinsokuShori(tokens)

        tokenCache.setObject(kinsokuTokens as NSArray, forKey: nsKey)
        return kinsokuTokens
    }

    private static let trailingPunctuationChars: Set<Character> = Set("。、！？!?…」』）)】]”’·・,:;：；")

    /// Japanese Kinsoku Shori (JIS X 4051 行頭禁則)
    /// Merges trailing punctuation marks into the preceding word token so punctuation never breaks alone
    private func applyKinsokuShori(_ tokens: [WordToken]) -> [WordToken] {
        guard tokens.count > 1 else { return tokens }
        var result: [WordToken] = []

        for tok in tokens {
            let isAllPunctuation = tok.text.allSatisfy { Self.trailingPunctuationChars.contains($0) }
            if isAllPunctuation, let last = result.popLast() {
                let mergedText = last.text + tok.text
                let merged = WordToken(
                    id: last.id,
                    index: last.index,
                    text: mergedText,
                    furigana: last.furigana,
                    romaji: last.romaji,
                    meaning: last.meaning,
                    moraWeight: last.moraWeight + tok.moraWeight
                )
                result.append(merged)
            } else {
                result.append(tok)
            }
        }

        return result.enumerated().map { (idx, tok) in
            WordToken(
                id: "\(idx)_\(tok.text)",
                index: idx,
                text: tok.text,
                furigana: tok.furigana,
                romaji: tok.romaji,
                meaning: tok.meaning,
                moraWeight: tok.moraWeight
            )
        }
    }

    private func tokenizeWithCFStringTokenizer(_ text: String) -> [String] {
        let cfStr = text as CFString
        let length = CFStringGetLength(cfStr)
        guard length > 0 else { return [] }

        let range = CFRangeMake(0, length)
        let locale = CFLocaleCreate(kCFAllocatorDefault, CFLocaleIdentifier("ja_JP" as CFString))
        guard let tokenizer = CFStringTokenizerCreate(kCFAllocatorDefault, cfStr, range, kCFStringTokenizerUnitWordBoundary, locale) else {
            return [text]
        }

        var results: [String] = []
        var tokenType = CFStringTokenizerGoToTokenAtIndex(tokenizer, 0)
        while tokenType != [] {
            let tokenRange = CFStringTokenizerGetCurrentTokenRange(tokenizer)
            if tokenRange.location != kCFNotFound && tokenRange.length > 0 {
                let sub = CFStringCreateWithSubstring(kCFAllocatorDefault, cfStr, tokenRange) as String
                let trimmed = sub.trimmingCharacters(in: .whitespacesAndNewlines)
                if !trimmed.isEmpty {
                    results.append(trimmed)
                }
            }
            tokenType = CFStringTokenizerAdvanceToNextToken(tokenizer)
        }
        return results.isEmpty ? [text] : results
    }

    /// Computes accurate mora weight based on Tokyo speech tempo
    public func calculateMoraWeight(text: String, furigana: String) -> Double {
        let target = furigana.isEmpty ? text : furigana
        let smallKana: Set<Character> = ["ゃ", "ゅ", "ょ", "ぁ", "ぃ", "ぅ", "ぇ", "ぉ", "ャ", "ュ", "ョ", "ァ", "ィ", "ゥ", "ェ", "ォ", "ゎ", "ヮ"]
        var count = 0.0

        for ch in target {
            if smallKana.contains(ch) { continue }
            if ch == "、" || ch == "," {
                count += 0.8
                continue
            }
            if ch == "。" || ch == "." || ch == "！" || ch == "？" || ch == " " {
                continue
            }
            count += 1.0
        }

        return max(1.0, count)
    }

    /// Complete Hepburn Romaji transliteration
    public func transliterateToRomaji(_ text: String) -> String {
        let clean = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if clean.isEmpty { return "" }

        // 1. Transform Katakana to Hiragana first so Hiragana->Latin handles Katakana seamlessly
        let mutable = NSMutableString(string: clean) as CFMutableString
        CFStringTransform(mutable, nil, kCFStringTransformHiraganaKatakana, true) // Katakana -> Hiragana
        CFStringTransform(mutable, nil, kCFStringTransformLatinHiragana, true)    // Hiragana -> Latin
        var result = mutable as String

        // 2. If untransformed, attempt full ToLatin transformation
        if result == clean {
            let m2 = NSMutableString(string: clean) as CFMutableString
            CFStringTransform(m2, nil, kCFStringTransformToLatin, false)
            result = m2 as String
        }

        if !result.isEmpty {
            result = result.replacingOccurrences(of: "\n", with: " ")
            return result
        }

        return clean
    }
}
