import Foundation

public struct GrammarSentence: Identifiable, Codable {
    public let id: String
    public let japanese: String
    public let furigana: String
    public let english: String
    public let chinese: String
    public let audioKey: String

    public init(
        id: String = UUID().uuidString,
        japanese: String,
        furigana: String,
        english: String,
        chinese: String,
        audioKey: String
    ) {
        self.id = id
        self.japanese = japanese
        self.furigana = furigana
        self.english = english
        self.chinese = chinese
        self.audioKey = audioKey
    }
}

public struct GrammarQuiz: Codable {
    public let question: String
    public let questionFurigana: String
    public let options: [String]
    public let correctIndex: Int
    public let explanationZh: String
    public let explanationEn: String

    public init(
        question: String,
        questionFurigana: String,
        options: [String],
        correctIndex: Int,
        explanationZh: String,
        explanationEn: String
    ) {
        self.question = question
        self.questionFurigana = questionFurigana
        self.options = options
        self.correctIndex = correctIndex
        self.explanationZh = explanationZh
        self.explanationEn = explanationEn
    }
}

public struct JLPTGrammarPoint: Identifiable, Codable {
    public let id: String
    public let title: String
    public let level: String         // N5, N4, N3, N2, N1
    public let romaji: String
    public let meaningZh: String
    public let meaningEn: String
    public let connectionRule: String
    public let nuanceExplanation: String
    public let scenarioTag: String   // transit, dining, shopping, business, daily, social, emergency
    public let examTip: String
    public let sentences: [GrammarSentence]
    public let quiz: GrammarQuiz?

    public init(
        id: String,
        title: String,
        level: String,
        romaji: String,
        meaningZh: String,
        meaningEn: String,
        connectionRule: String,
        nuanceExplanation: String,
        scenarioTag: String,
        examTip: String,
        sentences: [GrammarSentence],
        quiz: GrammarQuiz? = nil
    ) {
        self.id = id
        self.title = title
        self.level = level
        self.romaji = romaji
        self.meaningZh = meaningZh
        self.meaningEn = meaningEn
        self.connectionRule = connectionRule
        self.nuanceExplanation = nuanceExplanation
        self.scenarioTag = scenarioTag
        self.examTip = examTip
        self.sentences = sentences
        self.quiz = quiz
    }
}
