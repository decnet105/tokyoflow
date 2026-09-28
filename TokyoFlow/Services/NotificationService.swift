import Foundation
import UserNotifications
import Combine

public class NotificationService: NSObject, ObservableObject, UNUserNotificationCenterDelegate {
    public static let shared = NotificationService()

    @Published public var isAuthorized: Bool = false
    @Published public var dailyReminderHour: Int = 21 // 9:00 PM
    @Published public var dailyReminderMinute: Int = 0

    private override init() {
        super.init()
        UNUserNotificationCenter.current().delegate = self
        checkAuthorizationStatus()
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
                    print("✅ NotificationService: Notifications authorized. Scheduled 9:00 PM daily reminder.")
                } else if let error = error {
                    print("⚠️ NotificationService: Authorization failed: \(error)")
                }
                completion?(granted)
            }
        }
    }

    /// Schedules a recurring local push notification at 9:00 PM (21:00) every day in user's local timezone
    public func scheduleDailyEveningReminder() {
        let center = UNUserNotificationCenter.current()
        let identifier = "tokyoflow.daily.evening.reminder"

        // Remove previous to avoid duplicates
        center.removePendingNotificationRequests(withIdentifiers: [identifier])

        let content = UNMutableNotificationContent()
        content.title = "🎌 東京日本語修行・今日の学習レポート"

        let streak = GamificationService.shared.streakDays
        let tp = GamificationService.shared.tokyoPoints
        let minutes = GamificationService.shared.dailyMinutesLearned

        if minutes > 0 {
            content.body = "今日もお疲れ様でした！本日は \(minutes) 分間学習 (連続 \(streak) 日目🔥・\(tp) TP)。就寝前の3分間で今日の耳トレを復習しましょう！"
        } else {
            content.body = "今夜の東京散歩に出かけましょう！寝る前の3分間で今日の五十音・ニュースをチェック (連続 \(streak) 日記録中🔥)"
        }

        content.sound = .default
        content.badge = 1

        var dateComponents = DateComponents()
        dateComponents.hour = dailyReminderHour // 21 (9:00 PM)
        dateComponents.minute = dailyReminderMinute // 00

        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: true)
        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)

        center.add(request) { error in
            if let error = error {
                print("⚠️ NotificationService: Failed to schedule reminder: \(error)")
            } else {
                print("🔔 NotificationService: Successfully scheduled daily notification for \(self.dailyReminderHour):00 PM")
            }
        }
    }

    // MARK: - UNUserNotificationCenterDelegate
    public func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification,
        withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void
    ) {
        // Show banner even when app is currently open in foreground
        completionHandler([.banner, .sound, .badge])
    }
}
