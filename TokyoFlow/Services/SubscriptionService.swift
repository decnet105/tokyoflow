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

    // MARK: - Community Growth Mode (100% Free Unlimited Access to build volume)
    public func canAccessJLPTLevel(_ level: String) -> Bool {
        // 100% Free access for all JLPT levels (N5-N1) during YouTube + Free App Growth Phase
        return true
    }

    public func canAccessAdvancedScenarios(level: Int) -> Bool {
        // 100% Free access to all Tokyo scenarios
        return true
    }

    public var maxFreeDailyReviews: Int {
        return 9999
    }

    public var remainingFreeReviewsToday: Int {
        return 9999
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
