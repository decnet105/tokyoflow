import Foundation

// MARK: - Track 1: 5-Minute Daily Scenario Package Model
public struct TokyoDailyScenarioPackage: Identifiable {
    public let id: String
    public let dayNumber: Int
    public let title: String
    public let subtitle: String
    public let locationTag: String
    public let durationSeconds: Int // Default: 300 (5 minutes)
    
    // Step 1: Scenario Context & Dialogue
    public let sceneDialogue: [DialogueLine]
    public let sceneSummaryZh: String
    public let sceneSummaryEn: String
    
    // Step 2: Vocabulary & Grammar Analysis (with Romaji and English)
    public let vocabGrammarAnalyses: [ScenarioAnalysisItem]
    
    // Step 3: YouTube Video Masterclass
    public let youtubeVideoId: String
    public let videoTitle: String
    public let videoThumbnailUrl: String
    
    // Step 4: Golden Practice Phrase for 30s Karaoke Shadowing
    public let goldenSentence: String
    public let goldenSentenceFurigana: String
    public let goldenSentenceRomaji: String
    public let goldenSentenceMeaning: String
    public let goldenSentenceMeaningZh: String
    
    public init(
        id: String = UUID().uuidString,
        dayNumber: Int,
        title: String,
        subtitle: String,
        locationTag: String,
        durationSeconds: Int = 300,
        sceneDialogue: [DialogueLine],
        sceneSummaryZh: String,
        sceneSummaryEn: String,
        vocabGrammarAnalyses: [ScenarioAnalysisItem],
        youtubeVideoId: String,
        videoTitle: String,
        videoThumbnailUrl: String = "",
        goldenSentence: String,
        goldenSentenceFurigana: String,
        goldenSentenceRomaji: String,
        goldenSentenceMeaning: String,
        goldenSentenceMeaningZh: String = ""
    ) {
        self.id = id
        self.dayNumber = dayNumber
        self.title = title
        self.subtitle = subtitle
        self.locationTag = locationTag
        self.durationSeconds = durationSeconds
        self.sceneDialogue = sceneDialogue
        self.sceneSummaryZh = sceneSummaryZh
        self.sceneSummaryEn = sceneSummaryEn
        self.vocabGrammarAnalyses = vocabGrammarAnalyses
        self.youtubeVideoId = youtubeVideoId
        self.videoTitle = videoTitle
        self.videoThumbnailUrl = videoThumbnailUrl
        self.goldenSentence = goldenSentence
        self.goldenSentenceFurigana = goldenSentenceFurigana
        self.goldenSentenceRomaji = goldenSentenceRomaji
        self.goldenSentenceMeaning = goldenSentenceMeaning
        self.goldenSentenceMeaningZh = goldenSentenceMeaningZh.isEmpty ? goldenSentenceMeaning : goldenSentenceMeaningZh
    }
}

public struct ScenarioAnalysisItem: Identifiable {
    public let id: String
    public let japanese: String
    public let furigana: String
    public let romaji: String
    public let englishMeaning: String
    public let chineseMeaning: String
    public let grammarRule: String
    public let grammarRuleZh: String
    public let practicalTip: String
    public let practicalTipZh: String
    
    public init(
        id: String = UUID().uuidString,
        japanese: String,
        furigana: String,
        romaji: String,
        englishMeaning: String,
        chineseMeaning: String = "",
        grammarRule: String = "",
        grammarRuleZh: String = "",
        practicalTip: String = "",
        practicalTipZh: String = ""
    ) {
        self.id = id
        self.japanese = japanese
        self.furigana = furigana
        self.romaji = romaji
        self.englishMeaning = englishMeaning
        self.chineseMeaning = chineseMeaning.isEmpty ? englishMeaning : chineseMeaning
        self.grammarRule = grammarRule
        self.grammarRuleZh = grammarRuleZh.isEmpty ? grammarRule : grammarRuleZh
        self.practicalTip = practicalTip
        self.practicalTipZh = practicalTipZh.isEmpty ? practicalTip : practicalTipZh
    }
}

// MARK: - Track 2: JLPT 2 New + 3 Review Ebbinghaus Package Model
public struct TokyoDailyJLPTPackage: Identifiable {
    public let id: String
    public let date: Date
    public let level: String // "N5", "N4", "N3", "N2", "N1"
    public let newItems: [JLPTStudyItem] // Strictly 2 NEW items
    public let reviewItems: [JLPTStudyItem] // Strictly 3 REVIEW items (SM-2 Spaced Repetition)
    
    public var allItems: [JLPTStudyItem] {
        return newItems + reviewItems
    }
    
    public init(
        id: String = UUID().uuidString,
        date: Date = Date(),
        level: String = "N5",
        newItems: [JLPTStudyItem],
        reviewItems: [JLPTStudyItem]
    ) {
        self.id = id
        self.date = date
        self.level = level
        self.newItems = newItems
        self.reviewItems = reviewItems
    }
}

public struct JLPTStudyItem: Identifiable, Hashable {
    public let id: String
    public let isNew: Bool // true = 2 New; false = 3 Review
    public let type: JLPTItemType
    public let kanji: String
    public let reading: String
    public let romaji: String
    public let englishMeaning: String
    public let pitchAccent: String
    public let exampleSentenceJa: String
    public let exampleSentenceFurigana: String
    public let exampleSentenceRomaji: String
    public let exampleSentenceMeaning: String
    public let examTip: String
    public var srsRepetition: Int
    public var srsEaseFactor: Double
    
    public enum JLPTItemType: String, Codable {
        case vocabulary = "Vocabulary (単語)"
        case grammarPattern = "Grammar Pattern (文法)"
        case keySentence = "Core Sentence (重要構文)"
    }
    
    public init(
        id: String = UUID().uuidString,
        isNew: Bool,
        type: JLPTItemType = .vocabulary,
        kanji: String,
        reading: String,
        romaji: String,
        englishMeaning: String,
        pitchAccent: String = "⓪ (Flat)",
        exampleSentenceJa: String = "",
        exampleSentenceFurigana: String = "",
        exampleSentenceRomaji: String = "",
        exampleSentenceMeaning: String = "",
        examTip: String = "",
        srsRepetition: Int = 0,
        srsEaseFactor: Double = 2.5
    ) {
        self.id = id
        self.isNew = isNew
        self.type = type
        self.kanji = kanji
        self.reading = reading
        self.romaji = romaji
        self.englishMeaning = englishMeaning
        self.pitchAccent = pitchAccent
        self.exampleSentenceJa = exampleSentenceJa
        self.exampleSentenceFurigana = exampleSentenceFurigana
        self.exampleSentenceRomaji = exampleSentenceRomaji
        self.exampleSentenceMeaning = exampleSentenceMeaning
        self.examTip = examTip
        self.srsRepetition = srsRepetition
        self.srsEaseFactor = srsEaseFactor
    }
}
