import Foundation

public enum TokyoLeagueTier: String, CaseIterable, Identifiable, Codable {
    case bronze = "Bronze (浅草ブロンズ)"
    case silver = "Silver (上野シルバー)"
    case gold = "Gold (池袋ゴールド)"
    case platinum = "Platinum (新宿プラチナ)"
    case diamond = "Diamond (銀座ダイヤモンド)"
    case legend = "Shibuya Legend (渋谷レジェンド)"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .bronze: return "shield.fill"
        case .silver: return "shield.lefthalf.filled"
        case .gold: return "medal.fill"
        case .platinum: return "trophy.fill"
        case .diamond: return "sparkles"
        case .legend: return "crown.fill"
        }
    }
}

public struct LeaderboardUser: Identifiable, Codable, Hashable {
    public let id: String
    public let rank: Int
    public let name: String
    public let avatar: String
    public let title: String
    public let points: Int
    public let streak: Int
    public let isCurrentUser: Bool

    public init(id: String, rank: Int, name: String, avatar: String, title: String, points: Int, streak: Int, isCurrentUser: Bool = false) {
        self.id = id
        self.rank = rank
        self.name = name
        self.avatar = avatar
        self.title = title
        self.points = points
        self.streak = streak
        self.isCurrentUser = isCurrentUser
    }
}
