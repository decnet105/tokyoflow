import Foundation
import Combine

public struct SRSItem: Identifiable, Codable {
    public var id: String { japanese }
    public let japanese: String
    public let reading: String
    public let english: String
    public let context: String
    public var intervalDays: Int
    public var repetition: Int
    public var easeFactor: Double
    public var nextReviewDate: Date
    public var lastReviewedDate: Date?

    public init(japanese: String, reading: String, english: String, context: String) {
        self.japanese = japanese
        self.reading = reading
        self.english = english
        self.context = context
        self.intervalDays = 1
        self.repetition = 0
        self.easeFactor = 2.5
        self.nextReviewDate = Date()
        self.lastReviewedDate = nil
    }
}

public class UserProfile: ObservableObject {
    @Published public var currentDay: Int
    @Published public var streakCount: Int
    @Published public var completedScenarioIds: Set<String>
    @Published public var completedMangaLessonIds: Set<String>
    @Published public var masteredCanDoIds: Set<String>
    @Published public var bookmarkedPhrases: [SRSItem]
    @Published public var furiganaEnabled: Bool
    @Published public var romajiEnabled: Bool
    @Published public var translationLanguage: String // "en" or "zh"
    @Published public var speechRate: Float // 0.45 to 0.6

    public init() {
        self.currentDay = 1
        self.streakCount = 7
        self.completedScenarioIds = ["scenario_01_morning_train"]
        self.completedMangaLessonIds = ["manga_01_shonen_battle_sfx"]
        self.masteredCanDoIds = ["A1_transit_ticket", "A1_kombini_checkout"]
        self.bookmarkedPhrases = [
            SRSItem(japanese: "何番線ですか？", reading: "なんばんせんですか？", english: "Which platform is it?", context: "Train transit"),
            SRSItem(japanese: "袋は大丈夫です", reading: "ふくろはだいじょうぶです", english: "No plastic bag needed.", context: "Convenience store"),
            SRSItem(japanese: "とりあえず生で", reading: "とりあえずなまで", english: "Draft beer to start, please.", context: "Izakaya dining"),
            SRSItem(japanese: "領収書をお願いします", reading: "りょうしゅうしょをおねがいします", english: "Receipt please.", context: "Business / Shopping"),
            SRSItem(japanese: "〜ちゃう", reading: "〜ちゃう", english: "Casual contraction for 〜てしまう (accidental/completed)", context: "Manga colloquial")
        ]
        self.furiganaEnabled = true
        self.romajiEnabled = false
        self.translationLanguage = "en"
        self.speechRate = 0.50
    }

    public func markScenarioCompleted(_ id: String) {
        completedScenarioIds.insert(id)
        if completedScenarioIds.count % 2 == 0 {
            currentDay += 1
        }
    }

    public func markMangaCompleted(_ id: String) {
        completedMangaLessonIds.insert(id)
    }

    public func toggleBookmark(japanese: String, reading: String, english: String, context: String) {
        if let idx = bookmarkedPhrases.firstIndex(where: { $0.japanese == japanese }) {
            bookmarkedPhrases.remove(at: idx)
        } else {
            bookmarkedPhrases.append(SRSItem(japanese: japanese, reading: reading, english: english, context: context))
        }
    }

    public func isBookmarked(_ japanese: String) -> Bool {
        return bookmarkedPhrases.contains(where: { $0.japanese == japanese })
    }
}
