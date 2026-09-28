import SwiftUI
import Combine

public class GamificationService: ObservableObject {
    public static let shared = GamificationService()

    @AppStorage("tokyo_points_balance") public var tokyoPoints: Int = 380
    @AppStorage("user_exp_total") public var totalEXP: Int = 850
    @AppStorage("last_checkin_datestr") private var lastCheckinDateStr: String = ""
    @AppStorage("streak_days_count") public var streakDays: Int = 3

    @Published public var dailyQuests: [DailyQuest] = []
    @Published public var leaderboardUsers: [LeaderboardUser] = []
    @Published public var currentLeague: TokyoLeagueTier = .gold
    @Published public var showLevelUpAlert: Bool = false
    @Published public var newUnlockedTier: TokyoResidentTier? = nil

    public let residentTiers: [TokyoResidentTier] = [
        TokyoResidentTier(level: 1, titleJapanese: "観光客 (Tourist)", titleEnglish: "Tokyo Explorer", minEXP: 0, badgeIcon: "airplane.departure", perks: ["Access to Shinjuku Quest", "Basic Survival Kit"]),
        TokyoResidentTier(level: 5, titleJapanese: "ワーホリ滞在者 (Working Holiday)", titleEnglish: "Tokyo Resident", minEXP: 500, badgeIcon: "tram.fill", perks: ["Unlock Kombini 5-Question Challenge", "Daily NHK News Audio"]),
        TokyoResidentTier(level: 10, titleJapanese: "留学生 (Student)", titleEnglish: "Tokyo Scholar", minEXP: 1500, badgeIcon: "book.closed.fill", perks: ["Unlock Ramen & Izakaya Scenarios", "Manga SFX Soundboard"]),
        TokyoResidentTier(level: 20, titleJapanese: "都内一人暮らし (Solo Resident)", titleEnglish: "Tokyo Local", minEXP: 3500, badgeIcon: "house.fill", perks: ["Supermarket Half-Price Night Battle", "Post Office Fuzaihyo"]),
        TokyoResidentTier(level: 50, titleJapanese: "下町常連 (Neighborhood Regular)", titleEnglish: "Tokyo Insider", minEXP: 10000, badgeIcon: "flame.fill", perks: ["Manga Raw Tankobon RTL Reader", "Platinum League"]),
        TokyoResidentTier(level: 100, titleJapanese: "東京の達人 (Tokyo Legend)", titleEnglish: "Tokyo Master", minEXP: 25000, badgeIcon: "crown.fill", perks: ["All Gold Badges", "Custom Manga Frame"])
    ]

    private init() {
        setupDailyQuests()
        setupLeaderboard()
    }

    public var currentTier: TokyoResidentTier {
        let sorted = residentTiers.sorted { $0.minEXP > $1.minEXP }
        return sorted.first { totalEXP >= $0.minEXP } ?? residentTiers[0]
    }

    public var nextTier: TokyoResidentTier? {
        let sorted = residentTiers.sorted { $0.minEXP < $1.minEXP }
        return sorted.first { $0.minEXP > totalEXP }
    }

    public var progressToNextTier: Double {
        guard let next = nextTier else { return 1.0 }
        let currentMin = currentTier.minEXP
        let range = Double(next.minEXP - currentMin)
        let current = Double(totalEXP - currentMin)
        return min(1.0, max(0.0, current / range))
    }

    public func setupDailyQuests() {
        let todayStr = getTodayString()
        let isTodayCheckedIn = (lastCheckinDateStr == todayStr)

        self.dailyQuests = [
            DailyQuest(
                id: "q_checkin",
                title: "今日签到 (Daily Check-in)",
                subtitle: "保持连续打卡，领取今日 Tokyo Points",
                icon: "calendar.badge.clock",
                rewardTP: 50,
                rewardEXP: 50,
                currentProgress: isTodayCheckedIn ? 1 : 0,
                targetCount: 1,
                isCompleted: isTodayCheckedIn
            ),
            DailyQuest(
                id: "q_listen_news",
                title: "NHK 原音新闻 (Daily Real News)",
                subtitle: "完整收听 1 篇 NHK やさしい日本語真实新闻",
                icon: "headphones",
                rewardTP: 100,
                rewardEXP: 120,
                currentProgress: 0,
                targetCount: 1,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_dojo_battle",
                title: "道场秒答实战 (Speed Dojo Battle)",
                subtitle: "通关 1 次便利店或居酒屋连环问对决",
                icon: "bolt.shield.fill",
                rewardTP: 80,
                rewardEXP: 100,
                currentProgress: 0,
                targetCount: 1,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_shadowing",
                title: "原文录音跟读 (Native Shadowing)",
                subtitle: "使用麦克风录音跟读 3 个真实东京生活句子",
                icon: "mic.fill",
                rewardTP: 120,
                rewardEXP: 150,
                currentProgress: 0,
                targetCount: 3,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_manga_sfx",
                title: "漫画拟声词特训 (Manga SFX Lab)",
                subtitle: "学习并测试 5 个少年热血/日常拟声词",
                icon: "sparkles",
                rewardTP: 60,
                rewardEXP: 80,
                currentProgress: 0,
                targetCount: 5,
                isCompleted: false
            )
        ]
    }

    public func completeQuest(id: String) {
        if let idx = dailyQuests.firstIndex(where: { $0.id == id && !$0.isCompleted }) {
            dailyQuests[idx].currentProgress = dailyQuests[idx].targetCount
            dailyQuests[idx].isCompleted = true

            let rewardTP = dailyQuests[idx].rewardTP
            let rewardEXP = dailyQuests[idx].rewardEXP
            addRewards(tp: rewardTP, exp: rewardEXP)

            if id == "q_checkin" {
                recordDailyCheckin()
            }
        }
    }

    public func incrementQuestProgress(id: String, amount: Int = 1) {
        if let idx = dailyQuests.firstIndex(where: { $0.id == id && !$0.isCompleted }) {
            dailyQuests[idx].currentProgress += amount
            if dailyQuests[idx].currentProgress >= dailyQuests[idx].targetCount {
                dailyQuests[idx].isCompleted = true
                let rewardTP = dailyQuests[idx].rewardTP
                let rewardEXP = dailyQuests[idx].rewardEXP
                addRewards(tp: rewardTP, exp: rewardEXP)
            }
        }
    }

    public func addRewards(tp: Int, exp: Int) {
        let oldTier = currentTier
        tokyoPoints += tp
        totalEXP += exp

        let newTier = currentTier
        if newTier.level > oldTier.level {
            newUnlockedTier = newTier
            showLevelUpAlert = true
        }
        setupLeaderboard()
    }

    private func recordDailyCheckin() {
        let todayStr = getTodayString()
        if lastCheckinDateStr != todayStr {
            lastCheckinDateStr = todayStr
            streakDays += 1
        }
    }

    public func setupLeaderboard() {
        self.leaderboardUsers = [
            LeaderboardUser(id: "u1", rank: 1, name: "Kenji_Tokyo", avatar: "🍜", title: "下町常連", points: 2840, streak: 42),
            LeaderboardUser(id: "u2", rank: 2, name: "Yuki_Anime", avatar: "🌸", title: "留学生", points: 2310, streak: 28),
            LeaderboardUser(id: "u_me", rank: 3, name: "You (あなた)", avatar: "⚡", title: currentTier.titleJapanese.components(separatedBy: " ").first ?? "留学生", points: totalEXP, streak: streakDays, isCurrentUser: true),
            LeaderboardUser(id: "u3", rank: 4, name: "Takeshi99", avatar: "🚄", title: "ワーホリ滞在者", points: 790, streak: 12),
            LeaderboardUser(id: "u4", rank: 5, name: "Sakura_Manga", avatar: "🎨", title: "ワーホリ滞在者", points: 650, streak: 9),
            LeaderboardUser(id: "u5", rank: 6, name: "Alex_Akiba", avatar: "🎮", title: "観光客", points: 420, streak: 5)
        ]
    }

    private func getTodayString() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: Date())
    }
}
