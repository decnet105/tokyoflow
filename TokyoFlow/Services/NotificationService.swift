import Foundation
import UserNotifications
import Combine

public class NotificationService: NSObject, ObservableObject, UNUserNotificationCenterDelegate {
    public static let shared = NotificationService()

    @Published public var isAuthorized: Bool = false
    @Published public var dailyReminderHour: Int = 21 // 9:00 PM
    @Published public var dailyReminderMinute: Int = 0

    // Message Center Inbox & 9 PM Summary State
    @Published public var messages: [TokyoAppMessage] = []
    @Published public var selectedSummaryMessage: TokyoAppMessage? = nil
    @Published public var showNightlySummarySheet: Bool = false
    @Published public var showMessageCenterSheet: Bool = false

    public var unreadCount: Int {
        return messages.filter { !$0.isRead }.count
    }

    private let storageKey = "tokyoflow.inbox.messages.v1"

    private override init() {
        super.init()
        UNUserNotificationCenter.current().delegate = self
        loadStoredMessages()
        checkAuthorizationStatus()
    }

    // MARK: - Message Storage & Inbox Management

    private func loadStoredMessages() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode([TokyoAppMessage].self, from: data),
           !decoded.isEmpty {
            // Upgrade any older cached messages with verified native keys and spaced furigana
            self.messages = decoded.map { msg in
                if msg.type == .nightlySummary && (msg.goldenSentence?.contains("注文") == true) {
                    return TokyoAppMessage(
                        id: msg.id,
                        title: msg.title,
                        subtitle: msg.subtitle,
                        body: msg.body,
                        date: msg.date,
                        type: msg.type,
                        isRead: msg.isRead,
                        minutesLearned: msg.minutesLearned,
                        wordsLearned: msg.wordsLearned,
                        tpEarned: msg.tpEarned,
                        streak: msg.streak,
                        goldenSentence: "すみません、注文をお願いします。",
                        goldenSentenceFurigana: "すみません、 ちゅうもんを おねがいします。",
                        goldenSentenceMeaning: "Excuse me, I would like to order please."
                    )
                }
                return msg
            }
        } else {
            // Seed initial welcome message and past 9 PM digest
            self.seedDefaultMessages()
        }
    }

    public func saveMessages() {
        if let encoded = try? JSONEncoder().encode(messages) {
            UserDefaults.standard.set(encoded, forKey: storageKey)
        }
    }

    public func markAsRead(id: String) {
        if let idx = messages.firstIndex(where: { $0.id == id }) {
            messages[idx].isRead = true
            saveMessages()
        }
    }

    public func markAllAsRead() {
        for i in 0..<messages.count {
            messages[i].isRead = true
        }
        saveMessages()
    }

    public func deleteMessage(id: String) {
        messages.removeAll { $0.id == id }
        saveMessages()
    }

    private func seedDefaultMessages() {
        let calendar = Calendar.current
        let today = Date()
        let yesterday = calendar.date(byAdding: .day, value: -1, to: today) ?? today
        let twoDaysAgo = calendar.date(byAdding: .day, value: -2, to: today) ?? today

        let initial: [TokyoAppMessage] = [
            TokyoAppMessage(
                title: "今夜の学習レポート (21:00 日報)",
                subtitle: "本日の学習総括 • 連続4日達成！",
                body: "今日もお疲れ様でした！本日は 15 分間学習し、+45 TP を獲得しました。寝る前の耳トレに黄金フレーズ「すみません、注文をお願いします」を復習しましょう！",
                date: today,
                type: .nightlySummary,
                isRead: false,
                minutesLearned: 15,
                wordsLearned: 8,
                tpEarned: 45,
                streak: 4,
                goldenSentence: "すみません、注文をお願いします。",
                goldenSentenceFurigana: "すみません、ちゅうもんを おねがいします。",
                goldenSentenceMeaning: "Excuse me, I would like to order please."
            ),
            TokyoAppMessage(
                title: "昨日の学習レポート (21:00 日報)",
                subtitle: "昨日の学習振り返り • +30 TP",
                body: "昨日マスターしたフレーズ：「この電車は東京駅に行きますか」。通勤通学のスキマ時間を有効活用できています！",
                date: yesterday,
                type: .nightlySummary,
                isRead: true,
                minutesLearned: 12,
                wordsLearned: 6,
                tpEarned: 30,
                streak: 3,
                goldenSentence: "この電車は東京駅に行きますか。",
                goldenSentenceFurigana: "この でんしゃは とうきょうえきに いきますか。",
                goldenSentenceMeaning: "Does this train go to Tokyo Station?"
            ),
            TokyoAppMessage(
                title: "新着：秋葉原・聖地巡礼マスタークラス公開",
                subtitle: "Video Academy Episode 04 がアンロックされました",
                body: "アニメ・電気街の実践日本語を学べるエピソード04が公開されました。1分間のサバイバル表現を今すぐチェック！",
                date: twoDaysAgo,
                type: .scenarioUnlocked,
                isRead: true
            ),
            TokyoAppMessage(
                title: "東京フロー・学習効率アップの秘訣",
                subtitle: "「1秒反射」で身につく母語発音の活用法",
                body: "単語帳では例文の卡拉OKリアルタイムハイライトを活用して、音声の音節に合わせてシャドーイング（即時復唱）するのが最も効果的です。",
                date: twoDaysAgo,
                type: .system,
                isRead: true
            )
        ]

        self.messages = initial
        saveMessages()
    }

    /// Generates or refreshes today's 9 PM Nightly Summary
    public func generateTodayNightlySummary() -> TokyoAppMessage {
        let gamification = GamificationService.shared
        let streak = max(1, gamification.streakDays)
        let tp = max(15, gamification.tokyoPoints)
        let minutes = max(5, gamification.dailyMinutesLearned)

        let summary = TokyoAppMessage(
            id: "summary_\(Date().timeIntervalSince1970)",
            title: "今夜の学習レポート (21:00 日報)",
            subtitle: "本日の学習総括 • 連続 \(streak) 日記録中",
            body: "今日もお疲れ様でした！本日は \(minutes) 分間学習し、累計 \(tp) TP を獲得。寝る前の3分間で今日の耳トレをチェックしましょう！",
            date: Date(),
            type: .nightlySummary,
            isRead: false,
            minutesLearned: minutes,
            wordsLearned: max(5, streak * 2),
            tpEarned: tp,
            streak: streak,
            goldenSentence: "明日、電車で東京駅へ行きます。",
            goldenSentenceFurigana: "あした、でんしゃで とうきょうえきへ いきます。",
            goldenSentenceMeaning: "Tomorrow I will go to Tokyo Station by train."
        )

        // Prepend to messages if not already exists for today
        if !messages.contains(where: { Calendar.current.isDate($0.date, inSameDayAs: Date()) && $0.type == .nightlySummary }) {
            messages.insert(summary, at: 0)
            saveMessages()
        }

        return summary
    }

    public func checkAuthorizationStatus() {
        UNUserNotificationCenter.current().getNotificationSettings { settings in
            DispatchQueue.main.async {
                self.isAuthorized = settings.authorizationStatus == .authorized
                if self.isAuthorized {
                    self.scheduleDailyEveningReminder()
                }
            }
        }
    }

    public func requestNotificationPermission(completion: ((Bool) -> Void)? = nil) {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            DispatchQueue.main.async {
                self.isAuthorized = granted
                if granted {
                    self.scheduleDailyEveningReminder()
                    print(" NotificationService: Notifications authorized. Scheduled 9:00 PM daily reminder.")
                } else if let error = error {
                    print("️ NotificationService: Authorization failed: \(error)")
                }
                completion?(granted)
            }
        }
    }

    /// Schedules a recurring local push notification at 9:00 PM (21:00) every day in user's local timezone
    public func scheduleDailyEveningReminder() {
        let center = UNUserNotificationCenter.current()
        let identifier = "tokyoflow.daily.evening.reminder"

        center.removePendingNotificationRequests(withIdentifiers: [identifier])

        let content = UNMutableNotificationContent()
        content.title = "東京日本語修行・今夜21:00の学習レポート"

        let streak = GamificationService.shared.streakDays
        let tp = GamificationService.shared.tokyoPoints
        let minutes = GamificationService.shared.dailyMinutesLearned

        if minutes > 0 {
            content.body = "今日もお疲れ様でした！本日は \(minutes) 分間学習 (連続 \(streak) 日目・\(tp) TP)。タップして今夜の総括レポートを確認！"
        } else {
            content.body = "今夜の東京散歩に出かけましょう！寝る前の3分間で今日の耳トレをチェック (連続 \(streak) 日記録中)"
        }

        content.userInfo = ["action": "open_nightly_summary"]
        content.sound = .default
        content.badge = 1

        var dateComponents = DateComponents()
        dateComponents.hour = dailyReminderHour // 21 (9:00 PM)
        dateComponents.minute = dailyReminderMinute // 00

        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: true)
        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)

        center.add(request) { error in
            if let error = error {
                print("️ NotificationService: Failed to schedule reminder: \(error)")
            } else {
                print(" NotificationService: Successfully scheduled daily notification for \(self.dailyReminderHour):00 PM")
            }
        }
    }

    // MARK: - UNUserNotificationCenterDelegate
    public func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Foreground banner presentation
        completionHandler([.banner, .sound, .badge])
    }

    public func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse,
        withCompletionHandler completionHandler: @escaping () -> Void
    ) {
        // ⭐️ User tapped on notification banner -> Open 9 PM Nightly Summary Modal directly!
        DispatchQueue.main.async {
            let summary = self.generateTodayNightlySummary()
            self.selectedSummaryMessage = summary
            self.showNightlySummarySheet = true
        }
        completionHandler()
    }
}
