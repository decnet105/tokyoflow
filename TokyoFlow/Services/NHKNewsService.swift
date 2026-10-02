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
        var baseItems: [DailyNewsItem] = []

        if let url = Bundle.main.url(forResource: "daily_news", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let items = try? JSONDecoder().decode([DailyNewsItem].self, from: data) {
            baseItems = items
        } else {
            // Direct path lookup fallback
            let fallbackPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/daily_news.json"
            if let data = try? Data(contentsOf: URL(fileURLWithPath: fallbackPath)),
               let items = try? JSONDecoder().decode([DailyNewsItem].self, from: data) {
                baseItems = items
            }
        }

        guard !baseItems.isEmpty else { return }

        //  Automatic Daily Rotation based on day of year
        let dayOfYear = Calendar.current.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let shift = dayOfYear % baseItems.count
        let rotated = Array(baseItems[shift..<baseItems.count]) + Array(baseItems[0..<shift])

        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd"

        self.dailyNews = rotated.enumerated().map { idx, item in
            let articleDate = Calendar.current.date(byAdding: .day, value: -idx, to: Date()) ?? Date()
            let dateString = dateFormatter.string(from: articleDate)
            
            return DailyNewsItem(
                id: item.id,
                title: item.title,
                titleFurigana: item.titleFurigana,
                publishDate: dateString,
                category: item.category,
                categoryIcon: item.categoryIcon,
                summary: item.summary,
                contentSentences: item.contentSentences,
                audioUrl: item.audioUrl,
                videoUrl: item.videoUrl,
                sourceName: item.sourceName,
                vocabulary: item.vocabulary,
                comprehensionQuiz: item.comprehensionQuiz
            )
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
