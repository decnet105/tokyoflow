import Foundation

public struct RadioChapter: Identifiable, Hashable, Codable {
    public let id: String
    public let title: String
    public let titleJa: String
    public let startTimeSec: Double
    public let description: String

    public init(id: String, title: String, titleJa: String, startTimeSec: Double, description: String) {
        self.id = id
        self.title = title
        self.titleJa = titleJa
        self.startTimeSec = startTimeSec
        self.description = description
    }
}

public struct TokyoRadioStation: Identifiable, Hashable, Codable {
    public let id: String
    public let title: String
    public let titleJa: String
    public let subtitle: String
    public let durationSec: Double
    public let durationLabel: String
    public let audioFileName: String
    public let streamUrl: String?
    public let badge: String
    public let icon: String
    public let chapters: [RadioChapter]

    public init(
        id: String,
        title: String,
        titleJa: String,
        subtitle: String,
        durationSec: Double,
        durationLabel: String,
        audioFileName: String,
        streamUrl: String?,
        badge: String,
        icon: String,
        chapters: [RadioChapter]
    ) {
        self.id = id
        self.title = title
        self.titleJa = titleJa
        self.subtitle = subtitle
        self.durationSec = durationSec
        self.durationLabel = durationLabel
        self.audioFileName = audioFileName
        self.streamUrl = streamUrl
        self.badge = badge
        self.icon = icon
        self.chapters = chapters
    }
}

public struct TokyoRadioDataManager {
    public static let shared = TokyoRadioDataManager()

    public let stations: [TokyoRadioStation] = [
        TokyoRadioStation(
            id: "nhk_journal_55",
            title: "NHK Journal 55-Min Deep Immersion",
            titleJa: "NHKジャーナル 55分総合ニュース特報",
            subtitle: "Authentic 55-minute NHK radio broadcast with live news, Tokyo weather, economics, and cultural discussions.",
            durationSec: 3297.0, // 54:57
            durationLabel: "55 Mins (54:57)",
            audioFileName: "nhk_journal_55min.m4a",
            streamUrl: "https://www.nhk.or.jp/s-media/news/podcast/audio/e98935a7ab6c6c3ba9c1e8390f24d136_64k.mp3",
            badge: "NHK 55MIN FULL",
            icon: "antenna.radiowaves.left.and.right",
            chapters: [
                RadioChapter(id: "c1", title: "Headlines & Opening", titleJa: "オープニング・全国の主要ニュース", startTimeSec: 0.0, description: "Opening signature chimes and live headline summaries."),
                RadioChapter(id: "c2", title: "Tokyo Weather & Climate", titleJa: "台風・首都圏の気象情報", startTimeSec: 312.0, description: "Detailed weather forecast and train transit conditions."),
                RadioChapter(id: "c3", title: "Tokyo Living & Economy", titleJa: "暮らしと経済インサイト", startTimeSec: 940.0, description: "In-depth analysis of consumer trends and living in Japan."),
                RadioChapter(id: "c4", title: "Culture & Manga Feature", titleJa: "日本の文化・マンガ・芸術特集", startTimeSec: 1980.0, description: "Special feature on Japanese creators and cultural heritage."),
                RadioChapter(id: "c5", title: "Tomorrow's Outlook & Ending", titleJa: "明日の展望・エンディング", startTimeSec: 2790.0, description: "Final thoughts, sports wrap-up, and calm sign-off.")
            ]
        ),
        TokyoRadioStation(
            id: "tokyo_scenario_marathon_60",
            title: "Tokyo Living Scenario Marathon",
            titleJa: "東京暮らし・全場面ノンストップ連播",
            subtitle: "Continuous immersion marathon playing all 20+ Tokyo scenarios, station chimes, and convenience store dialogs in sequence.",
            durationSec: 3600.0,
            durationLabel: "60 Mins (Marathon)",
            audioFileName: "nhk_journal_55min.m4a",
            streamUrl: nil,
            badge: "60MIN MARATHON",
            icon: "tram.fill",
            chapters: [
                RadioChapter(id: "sc1", title: "Morning Commute & Shinjuku Station", titleJa: "朝の通勤・新宿駅ラッシュ", startTimeSec: 0.0, description: "Station melodies, ticket gates, and Yamanote announcements."),
                RadioChapter(id: "sc2", title: "Kombini & Lunch Order", titleJa: "コンビニ連環問・牛丼の注文", startTimeSec: 720.0, description: "7-Eleven cashiers, bento heating, and beef bowl customization."),
                RadioChapter(id: "sc3", title: "Afternoon Cafe & Akihabara Manga", titleJa: "喫茶店・秋葉原マンガ探訪", startTimeSec: 1560.0, description: "Ordering matcha latte, reading raw manga, and buying limited goods."),
                RadioChapter(id: "sc4", title: "Evening Izakaya & Supermarket", titleJa: "居酒屋乾杯・スーパー半額シール", startTimeSec: 2400.0, description: "Beer toast, Otoshi discussion, and 8PM grocery discount battles.")
            ]
        )
    ]
}
