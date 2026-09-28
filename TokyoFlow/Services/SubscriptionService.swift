import Foundation
import SwiftUI
import Combine

public enum SubscriptionPlan: String, CaseIterable, Identifiable {
    case monthly = "Monthly Plan"
    case annual = "Annual Pass (Best Value 🔥)"
    case lifetime = "Lifetime Master"

    public var id: String { rawValue }

    public var priceString: String {
        switch self {
        case .monthly: return "¥38 / 月 ($4.99/mo)"
        case .annual: return "¥238 / 年 ($2.49/mo, 省 50%)"
        case .lifetime: return "¥498 (终身买断)"
        }
    }

    public var badgeText: String? {
        switch self {
        case .annual: return "7天免费试用"
        case .lifetime: return "永久有效"
        default: return nil
        }
    }
}

public class SubscriptionService: ObservableObject {
    public static let shared = SubscriptionService()

    @AppStorage("tokyo_is_pro_subscriber") public var isPro: Bool = false
    @AppStorage("tokyo_free_daily_reviews_used") public var freeDailyReviewsUsed: Int = 0
    @AppStorage("tokyo_last_review_date_str") public var lastReviewDateStr: String = ""

    @Published public var showPaywallModal: Bool = false
    @Published public var selectedPlan: SubscriptionPlan = .annual

    private init() {}

    // MARK: - Freemium Access Control (60% Core Free + Pro Power Features)
    public func canAccessJLPTLevel(_ level: String) -> Bool {
        if isPro { return true }
        // N5 is 100% free for all users
        return level.uppercased() == "N5"
    }

    public func canAccessAdvancedScenarios(level: Int) -> Bool {
        if isPro { return true }
        // Levels 1-2 (JR Yamanote, Kombini, Ramen) are 100% free
        return level <= 2
    }

    public var maxFreeDailyReviews: Int {
        return 15
    }

    public var remainingFreeReviewsToday: Int {
        if isPro { return 9999 }
        checkDailyReset()
        return max(0, maxFreeDailyReviews - freeDailyReviewsUsed)
    }

    public func recordReviewUsed() {
        checkDailyReset()
        freeDailyReviewsUsed += 1
    }

    private func checkDailyReset() {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let today = formatter.string(from: Date())
        if lastReviewDateStr != today {
            lastReviewDateStr = today
            freeDailyReviewsUsed = 0
        }
    }

    // Mock purchase flow
    public func purchase(plan: SubscriptionPlan, completion: @escaping (Bool) -> Void) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            self.isPro = true
            self.showPaywallModal = false
            GamificationService.shared.addRewards(tp: 200, exp: 500)
            completion(true)
        }
    }

    public func restorePurchases(completion: @escaping (Bool) -> Void) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
            completion(self.isPro)
        }
    }
}
