import SwiftUI
import Combine

public class GamificationService: ObservableObject {
    public static let shared = GamificationService()

    @AppStorage("tokyo_points_balance") public var tokyoPoints: Int = 380
    @AppStorage("user_exp_total") public var totalEXP: Int = 850
    @AppStorage("last_checkin_datestr") public var lastCheckinDateStr: String = ""
    @AppStorage("streak_days_count") public var streakDays: Int = 3
    @AppStorage("longest_streak_count") public var longestStreak: Int = 7
    @AppStorage("total_checkin_count") public var totalCheckins: Int = 14
    @AppStorage("daily_micro_learning_minutes") public var dailyMinutesLearned: Int = 12
    @AppStorage("daily_micro_learning_goal") public var dailyGoalMinutes: Int = 20
    @AppStorage("checked_in_dates_json") private var checkedInDatesJSON: String = "[]"

    @Published public var dailyQuests: [DailyQuest] = []
    @Published public var leaderboardUsers: [LeaderboardUser] = []
    @Published public var allTimeLeaderboardUsers: [LeaderboardUser] = []
    @Published public var friendsLeaderboardUsers: [LeaderboardUser] = []
    @Published public var currentLeague: TokyoLeagueTier = .gold
    @Published public var showLevelUpAlert: Bool = false
    @Published public var newUnlockedTier: TokyoResidentTier? = nil
    @Published public var justCheckedInSuccess: Bool = false

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

    public var isTodayCheckedIn: Bool {
        return lastCheckinDateStr == getTodayString()
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

    public var microLearningProgress: Double {
        return min(1.0, Double(dailyMinutesLearned) / Double(max(1, dailyGoalMinutes)))
    }

    public func getWeeklyCheckInStatus() -> [CheckInDayStatus] {
        let calendar = Calendar.current
        let today = Date()
        let weekday = calendar.component(.weekday, from: today) // Sunday = 1, Monday = 2...
        // Align to Monday start (Monday = 0 ... Sunday = 6)
        let mondayOffset = (weekday == 1 ? -6 : 2 - weekday)
        guard let mondayDate = calendar.date(byAdding: .day, value: mondayOffset, to: today) else {
            return []
        }

        let recordedDates = getCheckedInDatesSet()
        let dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        let dayNamesShort = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        let todayStr = getTodayString()

        var results: [CheckInDayStatus] = []
        for i in 0..<7 {
            if let date = calendar.date(byAdding: .day, value: i, to: mondayDate) {
                let dStr = formatDate(date)
                let isToday = (dStr == todayStr)
                let isPast = date < calendar.startOfDay(for: today)
                let isChecked = recordedDates.contains(dStr) || (isToday && isTodayCheckedIn)
                results.append(
                    CheckInDayStatus(
                        dayIndex: i,
                        dayName: dayNames[i],
                        dayNameShort: dayNamesShort[i],
                        dateString: dStr,
                        isToday: isToday,
                        isCheckedIn: isChecked,
                        isPast: isPast,
                        rewardTP: (i == 6 ? 100 : 50) // Weekend 7-day bonus
                    )
                )
            }
        }
        return results
    }

    @discardableResult
    public func punchInToday() -> Bool {
        let todayStr = getTodayString()
        if lastCheckinDateStr == todayStr {
            return false // already checked in
        }

        lastCheckinDateStr = todayStr
        streakDays += 1
        totalCheckins += 1
        if streakDays > longestStreak {
            longestStreak = streakDays
        }

        var datesSet = getCheckedInDatesSet()
        datesSet.insert(todayStr)
        saveCheckedInDatesSet(datesSet)

        // Give reward
        let streakBonus = min(100, streakDays * 10)
        let earnedTP = 50 + streakBonus
        let earnedEXP = 60 + streakBonus
        addRewards(tp: earnedTP, exp: earnedEXP)

        completeQuest(id: "q_checkin")
        justCheckedInSuccess = true
        return true
    }

    public func recordMicroLearningTime(minutes: Int) {
        dailyMinutesLearned += minutes
        addRewards(tp: minutes * 5, exp: minutes * 6)
        setupDailyQuests()
    }

    public func setupDailyQuests() {
        let todayStr = getTodayString()
        let isTodayChecked = (lastCheckinDateStr == todayStr)

        self.dailyQuests = [
            DailyQuest(
                id: "q_checkin",
                title: "Daily Check-in & Streak",
                subtitle: "Day \(streakDays) streak! Claim your daily Tokyo Points & EXP",
                icon: "calendar.badge.checkmark",
                rewardTP: 50,
                rewardEXP: 60,
                currentProgress: isTodayChecked ? 1 : 0,
                targetCount: 1,
                isCompleted: isTodayChecked
            ),
            DailyQuest(
                id: "q_micro_time",
                title: "20-Min Micro-Immersion",
                subtitle: "\(dailyMinutesLearned) / \(dailyGoalMinutes) minutes completed today",
                icon: "timer",
                rewardTP: 80,
                rewardEXP: 100,
                currentProgress: min(dailyGoalMinutes, dailyMinutesLearned),
                targetCount: dailyGoalMinutes,
                isCompleted: dailyMinutesLearned >= dailyGoalMinutes
            ),
            DailyQuest(
                id: "q_listen_news",
                title: "Daily NHK Real News",
                subtitle: "Listen through 1 NHK Easy Japanese broadcast",
                icon: "headphones",
                rewardTP: 100,
                rewardEXP: 120,
                currentProgress: 0,
                targetCount: 1,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_dojo_battle",
                title: "Speed Dojo Battle",
                subtitle: "Clear 1 Kombini or Izakaya rapid-fire drill",
                icon: "bolt.shield.fill",
                rewardTP: 80,
                rewardEXP: 100,
                currentProgress: 0,
                targetCount: 1,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_shadowing",
                title: "Native Shadowing Drill",
                subtitle: "Record and shadow 3 authentic Tokyo sentences",
                icon: "mic.fill",
                rewardTP: 120,
                rewardEXP: 150,
                currentProgress: 0,
                targetCount: 3,
                isCompleted: false
            ),
            DailyQuest(
                id: "q_manga_sfx",
                title: "Manga Onomatopoeia Lab",
                subtitle: "Master 5 shonen & daily life SFX terms",
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

            if id == "q_checkin" && !isTodayCheckedIn {
                punchInToday()
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

    public func setupLeaderboard() {
        // Weekly League
        self.leaderboardUsers = [
            LeaderboardUser(id: "u1", rank: 1, name: "Kenji_Tokyo", avatar: "KT", title: "下町常連 (Lv.48)", points: 2840, streak: 42),
            LeaderboardUser(id: "u2", rank: 2, name: "Yuki_Anime", avatar: "YA", title: "留学生 (Lv.25)", points: 2310, streak: 28),
            LeaderboardUser(id: "u_me", rank: 3, name: "You (あなた)", avatar: "YOU", title: currentTier.titleJapanese.components(separatedBy: " ").first ?? "留学生", points: totalEXP, streak: streakDays, isCurrentUser: true),
            LeaderboardUser(id: "u3", rank: 4, name: "Takeshi99", avatar: "TK", title: "ワーホリ滞在者 (Lv.12)", points: 790, streak: 12),
            LeaderboardUser(id: "u4", rank: 5, name: "Sakura_Manga", avatar: "SM", title: "ワーホリ滞在者 (Lv.9)", points: 650, streak: 9),
            LeaderboardUser(id: "u5", rank: 6, name: "Alex_Akiba", avatar: "AA", title: "観光客 (Lv.4)", points: 420, streak: 5),
            LeaderboardUser(id: "u6", rank: 7, name: "Mika_Shibuya", avatar: "MS", title: "観光客 (Lv.3)", points: 310, streak: 3)
        ]

        // All-Time Hall of Fame
        self.allTimeLeaderboardUsers = [
            LeaderboardUser(id: "at1", rank: 1, name: "Daiki_Master", avatar: "DM", title: "東京の達人 (Lv.100)", points: 34500, streak: 365),
            LeaderboardUser(id: "at2", rank: 2, name: "Sora_Shinjuku", avatar: "SS", title: "下町常連 (Lv.88)", points: 28900, streak: 210),
            LeaderboardUser(id: "at3", rank: 3, name: "Kenji_Tokyo", avatar: "KT", title: "下町常内 (Lv.65)", points: 19400, streak: 140),
            LeaderboardUser(id: "at4", rank: 4, name: "Ren_Akiba", avatar: "RA", title: "都内一人暮らし (Lv.40)", points: 12800, streak: 84),
            LeaderboardUser(id: "u_me_all", rank: 5, name: "You (あなた)", avatar: "YOU", title: currentTier.titleJapanese.components(separatedBy: " ").first ?? "留学生", points: totalEXP, streak: streakDays, isCurrentUser: true)
        ]

        // Friends Circle
        self.friendsLeaderboardUsers = [
            LeaderboardUser(id: "u_me_f", rank: 1, name: "You (あなた)", avatar: "YOU", title: currentTier.titleJapanese.components(separatedBy: " ").first ?? "留学生", points: totalEXP, streak: streakDays, isCurrentUser: true),
            LeaderboardUser(id: "f1", rank: 2, name: "Hiroshi_Study", avatar: "HS", title: "留学生 (Lv.15)", points: 720, streak: 5),
            LeaderboardUser(id: "f2", rank: 3, name: "Elena_JP", avatar: "EJ", title: "ワーホリ滞在者 (Lv.8)", points: 510, streak: 3)
        ]
    }

    private func getCheckedInDatesSet() -> Set<String> {
        guard let data = checkedInDatesJSON.data(using: .utf8),
              let list = try? JSONDecoder().decode([String].self, from: data) else {
            return []
        }
        return Set(list)
    }

    private func saveCheckedInDatesSet(_ dates: Set<String>) {
        if let data = try? JSONEncoder().encode(Array(dates)),
           let str = String(data: data, encoding: .utf8) {
            checkedInDatesJSON = str
        }
    }

    private func getTodayString() -> String {
        return formatDate(Date())
    }

    private func formatDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
    }
}

public struct CheckInDayStatus: Identifiable {
    public var id: String { dateString }
    public let dayIndex: Int
    public let dayName: String
    public let dayNameShort: String
    public let dateString: String
    public let isToday: Bool
    public let isCheckedIn: Bool
    public let isPast: Bool
    public let rewardTP: Int
}
