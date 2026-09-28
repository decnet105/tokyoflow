import Foundation

public struct DailyQuest: Identifiable, Codable, Hashable {
    public let id: String
    public let title: String
    public let subtitle: String
    public let icon: String
    public let rewardTP: Int
    public let rewardEXP: Int
    public var currentProgress: Int
    public let targetCount: Int
    public var isCompleted: Bool

    public init(
        id: String,
        title: String,
        subtitle: String,
        icon: String,
        rewardTP: Int,
        rewardEXP: Int,
        currentProgress: Int = 0,
        targetCount: Int = 1,
        isCompleted: Bool = false
    ) {
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.icon = icon
        self.rewardTP = rewardTP
        self.rewardEXP = rewardEXP
        self.currentProgress = currentProgress
        self.targetCount = targetCount
        self.isCompleted = isCompleted
    }
}

public struct TokyoResidentTier {
    public let level: Int
    public let titleJapanese: String
    public let titleEnglish: String
    public let minEXP: Int
    public let badgeIcon: String
    public let perks: [String]
}
