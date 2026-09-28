import Foundation
import Combine

public class NHKNewsService: ObservableObject {
    public static let shared = NHKNewsService()

    @Published public var dailyNews: [DailyNewsItem] = []
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String? = nil

    private init() {
        loadBundledNews()
    }

    public func loadBundledNews() {
        if let url = Bundle.main.url(forResource: "daily_news", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let items = try? JSONDecoder().decode([DailyNewsItem].self, from: data) {
            self.dailyNews = items
            return
        }

        // Direct path lookup fallback
        let fallbackPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/daily_news.json"
        if let data = try? Data(contentsOf: URL(fileURLWithPath: fallbackPath)),
           let items = try? JSONDecoder().decode([DailyNewsItem].self, from: data) {
            self.dailyNews = items
        }
    }

    public func fetchLatestPublicNews() {
        isLoading = true
        errorMessage = nil

        // Simulating async network refresh from NHK Easy News feed with offline cached payload
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) { [weak self] in
            guard let self = self else { return }
            self.loadBundledNews()
            self.isLoading = false
        }
    }
}
