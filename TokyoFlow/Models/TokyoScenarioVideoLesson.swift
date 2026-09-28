import Foundation

public struct VideoChapterBookmark: Identifiable, Hashable, Codable {
    public var id: String { timeString }
    public let timeString: String
    public let timeSeconds: Double
    public let title: String
    public let summary: String

    public init(timeString: String, timeSeconds: Double, title: String, summary: String) {
        self.timeString = timeString
        self.timeSeconds = timeSeconds
        self.title = title
        self.summary = summary
    }
}

public struct VideoKeyTakeaway: Identifiable, Hashable, Codable {
    public var id: String { phrase }
    public let phrase: String
    public let furigana: String
    public let meaning: String
    public let explanation: String

    public init(phrase: String, furigana: String, meaning: String, explanation: String) {
        self.phrase = phrase
        self.furigana = furigana
        self.meaning = meaning
        self.explanation = explanation
    }
}

public struct TokyoScenarioVideoLesson: Identifiable, Hashable, Codable {
    public let id: String
    public let episodeNumber: Int
    public let scenarioId: String
    public let title: String
    public let titleJa: String
    public let channelName: String
    public let youtubeVideoId: String
    public let durationLabel: String
    public let levelBadge: String // N5-N4, N3, N2-N1
    public let district: String
    public let category: String
    public let thumbnailIcon: String
    public let summary: String
    public let chapters: [VideoChapterBookmark]
    public let keyTakeaways: [VideoKeyTakeaway]

    public var episodeLabel: String {
        String(format: "EP. %02d", episodeNumber)
    }

    public var youtubeWatchUrl: URL {
        URL(string: "https://www.youtube.com/watch?v=\(youtubeVideoId)") ?? URL(string: "https://www.youtube.com")!
    }

    public var youtubeAppUrl: URL {
        URL(string: "youtube://www.youtube.com/watch?v=\(youtubeVideoId)") ?? youtubeWatchUrl
    }
}

public class TokyoVideoLessonDataManager: ObservableObject {
    public static let shared = TokyoVideoLessonDataManager()

    public let lessons: [TokyoScenarioVideoLesson] = [
        TokyoScenarioVideoLesson(
            id: "yt_yamanote_01",
            episodeNumber: 1,
            scenarioId: "s_yamanote_rush",
            title: "EP. 01 • Tokyo Metro & Yamanote Line Platform Broadcasts",
            titleJa: "山手線ラッシュ・乗り換えアナウンス完全攻略",
            channelName: "TokyoFlow Japanese",
            youtubeVideoId: "6dxbsPYp654",
            durationLabel: "10:45",
            levelBadge: "JLPT N4-N3",
            district: "Shinjuku (新宿)",
            category: "transit",
            thumbnailIcon: "tram.fill",
            summary: "Deconstruct Shinjuku Station morning rush departure melodies, tactile yellow paving warnings, inner/outer loop announcements, and natural wayfinding phrases.",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Real-Life Audio Immersion", summary: "Shinjuku Station Platform 2 Yamanote Loop live transit announcement breakdown"),
                VideoChapterBookmark(timeString: "02:30", timeSeconds: 150, title: "Core Grammar & Keigo", summary: "Deconstruct '~ga mairimasu' humble & polite verb mechanics in JR announcements"),
                VideoChapterBookmark(timeString: "05:40", timeSeconds: 340, title: "1-Second Wayfinding", summary: "Instant golden phrases to ask station staff for Chuo Line / Sobu Line transfers"),
                VideoChapterBookmark(timeString: "08:15", timeSeconds: 495, title: "Shadowing & Roleplay", summary: "Sample-accurate native pitch accent repetition drill")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "まもなく、2番線に山手線内回りがまいります。", furigana: "まもなく、にばんせんに やまのてせん うちまわりが まいります。", meaning: "The Yamanote Line inner loop will soon arrive at track 2.", explanation: "'Mairimasu' is the humble form of 'kimasu' (to come), standard JR automated announcement grammar."),
                VideoKeyTakeaway(phrase: "黄色い点字ブロックの内側までお下がりください。", furigana: "きいろい てんじぶろっくの うちがわまで おさがりください。", meaning: "Please stand back behind the yellow tactile braille blocks.", explanation: "'O-sagari kudasai' is a polite public safety request."),
                VideoKeyTakeaway(phrase: "中央線への乗り換えはどのホームですか？", furigana: "ちゅうおうせんへの のりかえは どのほーむですか？", meaning: "Which platform is the transfer for the Chuo Line?", explanation: "Essential formula when lost inside massive transit hubs.")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_kombini_02",
            episodeNumber: 2,
            scenarioId: "s_kombini_register",
            title: "EP. 02 • Convenience Store Survival: 7-Eleven Rapid Checkout",
            titleJa: "コンビニレジ連環問・お弁当温め・袋不要",
            channelName: "TokyoFlow Japanese",
            youtubeVideoId: "bOcegXJ3_Qo",
            durationLabel: "08:20",
            levelBadge: "JLPT N5-N4",
            district: "Shibuya (渋谷)",
            category: "kombini",
            thumbnailIcon: "cart.fill",
            summary: "From 'Obentō atatamemasu ka?' to 'Reji-bukuro wa go-riyō desu ka?', decode all rapid-fire Japanese convenience store register questions and 1-second natural responses.",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Register Rapid-Fire Questions", summary: "Live recording of the 4 rapid checkout questions at Japanese 7-Eleven/FamilyMart"),
                VideoChapterBookmark(timeString: "02:10", timeSeconds: 130, title: "Microwave Heating & Bags", summary: "Proper register nuances of 'Atatamete kudasai' vs 'Daijōbu desu'"),
                VideoChapterBookmark(timeString: "04:50", timeSeconds: 290, title: "Digital Payment & Points", summary: "Suica, PayPay, and credit card checkout formulas"),
                VideoChapterBookmark(timeString: "06:40", timeSeconds: 400, title: "Checkout Roleplay Drill", summary: "Immersive checkout dialogue practice")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "お弁当温めますか？", furigana: "おべんとう あたためますか？", meaning: "Would you like your bento heated up in the microwave?", explanation: "Standard staff question. Reply 'Atatamete kudasai' (Please heat it) or 'Sono mama de daijōbu desu' (As-is is fine)."),
                VideoKeyTakeaway(phrase: "レジ袋は大丈夫です。", furigana: "れじぶくろは だいじょうぶです。", meaning: "I'm fine without a plastic bag (I have my own).", explanation: "'Daijōbu desu' with a gentle nod is the polite, natural way to decline."),
                VideoKeyTakeaway(phrase: "Suicaでお願いします。", furigana: "すいかで おねがいします。", meaning: "With Suica (IC card), please.", explanation: "Universal payment designation formula.")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_izakaya_03",
            episodeNumber: 3,
            scenarioId: "s_izakaya_toast",
            title: "EP. 03 • Izakaya Mastery: Showa Pub Ordering, Otoshi & Toasting",
            titleJa: "居酒屋注文・お通し文化・とりあえず生！",
            channelName: "TokyoFlow Japanese",
            youtubeVideoId: "M2i5zH7aWqk",
            durationLabel: "12:15",
            levelBadge: "JLPT N4-N3",
            district: "Shinjuku Omoide Yokocho (思い出横丁)",
            category: "dining",
            thumbnailIcon: "wineglass.fill",
            summary: "The golden rule of ordering 'Toriaezu nama!' first, Otoshi appetizer customs, salt vs tare sauce for yakitori skewers, and asking for the final bill.",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Entering the Izakaya", summary: "Hot towels (Oshibori) and the first mandatory round of drinks"),
                VideoChapterBookmark(timeString: "03:15", timeSeconds: 195, title: "Yakitori Flavor Nuance", summary: "Choosing between Shio (Salt) and Tare (Sweet Soy Sauce)"),
                VideoChapterBookmark(timeString: "07:00", timeSeconds: 420, title: "The Art of Kanpai!", summary: "Glass rim etiquette and saying 'Otsukaresama desu!'"),
                VideoChapterBookmark(timeString: "09:45", timeSeconds: 585, title: "Bill & Official Receipt", summary: "Mastering 'O-kaikei' and 'Ryōshūsho' phrases")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "とりあえず生ビール二つお願いします！", furigana: "とりあえず なまびーる ふたつ おねがいします！", meaning: "Two draft beers to start, please!", explanation: "The iconic opening order phrase at every Japanese izakaya pub."),
                VideoKeyTakeaway(phrase: "焼き鳥は塩とタレ、どちらにしますか？", furigana: "やきとりは しおと たれ、どちらにしますか？", meaning: "Would you like your yakitori skewers with salt or sweet tare sauce?", explanation: "Standard server question. Shio highlights ingredient freshness."),
                VideoKeyTakeaway(phrase: "お会計と領収書をお願いします。", furigana: "おかいけいと りょうしゅうしょを おねがいします。", meaning: "The check and an official receipt, please.", explanation: "Polite phrase to settle the bill and request a company receipt.")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_akiba_04",
            episodeNumber: 4,
            scenarioId: "s_akiba_manga",
            title: "EP. 04 • Akihabara Pilgrimage: Figures, Merch & Manga Tax-Free",
            titleJa: "秋葉原アニメ・限定グッズ・同人誌探訪",
            channelName: "TokyoFlow Japanese",
            youtubeVideoId: "N1vM-N12345",
            durationLabel: "09:50",
            levelBadge: "JLPT N3-N2",
            district: "Akihabara (秋葉原)",
            category: "shopping",
            thumbnailIcon: "sparkles.tv.fill",
            summary: "Explore multi-story Akihabara hobby towers, ask clerks for new anime original light novels, pre-order bonuses, and rental box figure inspections.",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Akiba Tower Exploration", summary: "Reading hobby building floor directories"),
                VideoChapterBookmark(timeString: "02:40", timeSeconds: 160, title: "Locating Manga & Light Novels", summary: "Asking for current season anime original books"),
                VideoChapterBookmark(timeString: "05:30", timeSeconds: 330, title: "Pre-order Perks & Blind Boxes", summary: "Clarifying limited edition bonus postcards & badges"),
                VideoChapterBookmark(timeString: "08:00", timeSeconds: 480, title: "Fan Dialogue Practice", summary: "Natural conversational phrases with fellow collectors")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "今期の新作アニメの原作はどこにありますか？", furigana: "こんきの しんさくあにめの げんさくは どこに ありますか？", meaning: "Where are the original manga/novels for this season's new anime?", explanation: "The most useful book-finding phrase in anime specialty bookstores."),
                VideoKeyTakeaway(phrase: "購入特典はまだ付きますか？", furigana: "こうにゅうとくてんは まだ つきますか？", meaning: "Does this still come with the purchase bonus perk?", explanation: "Essential phrase to confirm remaining exclusive merchandise gifts.")
            ]
        )
    ]

    public func lesson(for scenarioId: String) -> TokyoScenarioVideoLesson? {
        return lessons.first { $0.scenarioId == scenarioId }
    }
}
