import Foundation

public struct DailyNewsItem: Identifiable, Codable, Hashable {
    public let id: String
    public let title: String
    public let titleFurigana: String
    public let publishDate: String
    public let category: String
    public let categoryIcon: String
    public let summary: String
    public let contentSentences: [NewsSentence]
    public let audioUrl: String?
    public let videoUrl: String?
    public let sourceName: String
    public let vocabulary: [NewsVocab]
    public let comprehensionQuiz: [NewsQuiz]

    public init(
        id: String,
        title: String,
        titleFurigana: String,
        publishDate: String,
        category: String,
        categoryIcon: String,
        summary: String,
        contentSentences: [NewsSentence],
        audioUrl: String?,
        videoUrl: String?,
        sourceName: String,
        vocabulary: [NewsVocab],
        comprehensionQuiz: [NewsQuiz]
    ) {
        self.id = id
        self.title = title
        self.titleFurigana = titleFurigana
        self.publishDate = publishDate
        self.category = category
        self.categoryIcon = categoryIcon
        self.summary = summary
        self.contentSentences = contentSentences
        self.audioUrl = audioUrl
        self.videoUrl = videoUrl
        self.sourceName = sourceName
        self.vocabulary = vocabulary
        self.comprehensionQuiz = comprehensionQuiz
    }
}

public struct NewsSentence: Identifiable, Codable, Hashable {
    public let id: String
    public let japanese: String
    public let furigana: String
    public let english: String
    public let startTimeSec: Double
    public let endTimeSec: Double

    public init(id: String, japanese: String, furigana: String, english: String, startTimeSec: Double, endTimeSec: Double) {
        self.id = id
        self.japanese = japanese
        self.furigana = furigana
        self.english = english
        self.startTimeSec = startTimeSec
        self.endTimeSec = endTimeSec
    }
}

public struct NewsVocab: Identifiable, Codable, Hashable {
    public let id: String
    public let word: String
    public let reading: String
    public let pitchAccent: String
    public let meaning: String
    public let example: String

    public init(id: String, word: String, reading: String, pitchAccent: String, meaning: String, example: String) {
        self.id = id
        self.word = word
        self.reading = reading
        self.pitchAccent = pitchAccent
        self.meaning = meaning
        self.example = example
    }
}

public struct NewsQuiz: Identifiable, Codable, Hashable {
    public let id: String
    public let question: String
    public let options: [String]
    public let correctIndex: Int
    public let explanation: String

    public init(id: String, question: String, options: [String], correctIndex: Int, explanation: String) {
        self.id = id
        self.question = question
        self.options = options
        self.correctIndex = correctIndex
        self.explanation = explanation
    }
}
