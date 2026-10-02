import Foundation

public enum TokyoMessageType: String, Codable, CaseIterable {
    case nightlySummary = "nightlySummary" //  21:00 Daily Learning Recap
    case streakMilestone = "streakMilestone" //  Streak Record
    case scenarioUnlocked = "scenarioUnlocked" //  New Scenario
    case system = "system" //  Study Tip & Update
}

public struct TokyoAppMessage: Identifiable, Codable, Hashable {
    public let id: String
    public let title: String
    public let subtitle: String
    public let body: String
    public let date: Date
    public let type: TokyoMessageType
    public var isRead: Bool

    // Nightly Summary Specific Analytics
    public let minutesLearned: Int?
    public let wordsLearned: Int?
    public let tpEarned: Int?
    public let streak: Int?
    public let goldenSentence: String?
    public let goldenSentenceFurigana: String?
    public let goldenSentenceMeaning: String?

    public init(
        id: String = UUID().uuidString,
        title: String,
        subtitle: String,
        body: String,
        date: Date = Date(),
        type: TokyoMessageType,
        isRead: Bool = false,
        minutesLearned: Int? = nil,
        wordsLearned: Int? = nil,
        tpEarned: Int? = nil,
        streak: Int? = nil,
        goldenSentence: String? = nil,
        goldenSentenceFurigana: String? = nil,
        goldenSentenceMeaning: String? = nil
    ) {
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.date = date
        self.type = type
        self.isRead = isRead
        self.minutesLearned = minutesLearned
        self.wordsLearned = wordsLearned
        self.tpEarned = tpEarned
        self.streak = streak
        self.goldenSentence = goldenSentence
        self.goldenSentenceFurigana = goldenSentenceFurigana
        self.goldenSentenceMeaning = goldenSentenceMeaning
    }

    public var formattedDate: String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "ja_JP")
        formatter.dateFormat = "M月d日 (E) HH:mm"
        return formatter.string(from: date)
    }

    public var iconName: String {
        switch type {
        case .nightlySummary: return "moon.stars.fill"
        case .streakMilestone: return "flame.fill"
        case .scenarioUnlocked: return "map.fill"
        case .system: return "bell.badge.fill"
        }
    }
}
