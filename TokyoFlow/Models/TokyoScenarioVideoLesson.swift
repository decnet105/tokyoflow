import Foundation

public struct VideoChapterBookmark: Identifiable, Hashable, Codable {
    public var id: String { timeString }
    public let timeString: String
    public let timeSeconds: Double
    public let title: String
    public let titleZh: String?
    public let summary: String
    public let summaryZh: String?

    public init(timeString: String, timeSeconds: Double, title: String, titleZh: String? = nil, summary: String, summaryZh: String? = nil) {
        self.timeString = timeString
        self.timeSeconds = timeSeconds
        self.title = title
        self.titleZh = titleZh
        self.summary = summary
        self.summaryZh = summaryZh
    }

    public var localizedTitle: String {
        if LanguageManager.shared.isEnglish {
            return title
        } else {
            return titleZh ?? title
        }
    }

    public var localizedSummary: String {
        if LanguageManager.shared.isEnglish {
            return summary
        } else {
            return summaryZh ?? summary
        }
    }
}

public struct VideoKeyTakeaway: Identifiable, Hashable, Codable {
    public var id: String { phrase }
    public let phrase: String
    public let furigana: String
    public let meaning: String
    public let meaningZh: String?
    public let explanation: String
    public let explanationZh: String?

    public init(phrase: String, furigana: String, meaning: String, meaningZh: String? = nil, explanation: String, explanationZh: String? = nil) {
        self.phrase = phrase
        self.furigana = furigana
        self.meaning = meaning
        self.meaningZh = meaningZh
        self.explanation = explanation
        self.explanationZh = explanationZh
    }

    public var localizedMeaning: String {
        if LanguageManager.shared.isEnglish {
            return meaning
        } else {
            return meaningZh ?? meaning
        }
    }

    public var localizedExplanation: String {
        if LanguageManager.shared.isEnglish {
            return explanation
        } else {
            return explanationZh ?? explanation
        }
    }
}

public struct TokyoScenarioVideoLesson: Identifiable, Hashable, Codable {
    public let id: String
    public let episodeNumber: Int
    public let scenarioId: String
    public let title: String
    public let titleJa: String
    public let titleZh: String?
    public let channelName: String
    public let youtubeVideoId: String
    public let durationLabel: String
    public let levelBadge: String // N5-N4, N3, N2-N1
    public let district: String
    public let category: String
    public let thumbnailIcon: String
    public let summary: String
    public let summaryZh: String?
    public let chapters: [VideoChapterBookmark]
    public let keyTakeaways: [VideoKeyTakeaway]

    public init(
        id: String,
        episodeNumber: Int,
        scenarioId: String,
        title: String,
        titleJa: String,
        titleZh: String? = nil,
        channelName: String,
        youtubeVideoId: String,
        durationLabel: String,
        levelBadge: String,
        district: String,
        category: String,
        thumbnailIcon: String,
        summary: String,
        summaryZh: String? = nil,
        chapters: [VideoChapterBookmark],
        keyTakeaways: [VideoKeyTakeaway]
    ) {
        self.id = id
        self.episodeNumber = episodeNumber
        self.scenarioId = scenarioId
        self.title = title
        self.titleJa = titleJa
        self.titleZh = titleZh
        self.channelName = channelName
        self.youtubeVideoId = youtubeVideoId
        self.durationLabel = durationLabel
        self.levelBadge = levelBadge
        self.district = district
        self.category = category
        self.thumbnailIcon = thumbnailIcon
        self.summary = summary
        self.summaryZh = summaryZh
        self.chapters = chapters
        self.keyTakeaways = keyTakeaways
    }

    public var localizedTitle: String {
        if LanguageManager.shared.isEnglish {
            return title
        } else {
            return titleZh ?? title
        }
    }

    public var localizedSummary: String {
        if LanguageManager.shared.isEnglish {
            return summary
        } else {
            return summaryZh ?? summary
        }
    }

    public var episodeLabel: String {
        String(format: "EP. %02d", episodeNumber)
    }

    public var hqThumbnailUrl: URL? {
        URL(string: "https://img.youtube.com/vi/\(youtubeVideoId)/hqdefault.jpg")
    }

    public var maxResThumbnailUrl: URL? {
        URL(string: "https://img.youtube.com/vi/\(youtubeVideoId)/maxresdefault.jpg")
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

    @Published public var lessons: [TokyoScenarioVideoLesson] = []
    @Published public var isSyncing: Bool = false
    @Published public var lastSyncDate: Date? = nil

    private let cacheKey = "tokyoflow_cached_video_lessons_v1"
    private let remoteManifestURL = URL(string: "https://raw.githubusercontent.com/tokyoflow/tokyoflow-assets/main/catalog/lessons.json")

    private init() {
        loadCachedOrBuiltInLessons()
    }

    public func lesson(for scenarioId: String) -> TokyoScenarioVideoLesson? {
        return lessons.first { $0.scenarioId == scenarioId }
    }

    // MARK: - Local Cache & Built-in Fallbacks
    private func loadCachedOrBuiltInLessons() {
        if let data = UserDefaults.standard.data(forKey: cacheKey),
           let cached = try? JSONDecoder().decode([TokyoScenarioVideoLesson].self, from: data),
           !cached.isEmpty {
            self.lessons = cached
        } else {
            self.lessons = builtInDefaultLessons
        }
    }

    private func saveToLocalCache(_ newLessons: [TokyoScenarioVideoLesson]) {
        if let data = try? JSONEncoder().encode(newLessons) {
            UserDefaults.standard.set(data, forKey: cacheKey)
        }
    }

    // MARK: - Dynamic Cloud Sync (No App Store Update Required)
    @MainActor
    public func fetchRemoteLessons() async {
        guard let url = remoteManifestURL else { return }
        isSyncing = true
        defer { isSyncing = false }

        do {
            var request = URLRequest(url: url)
            request.timeoutInterval = 10.0
            request.cachePolicy = .reloadIgnoringLocalCacheData

            let (data, response) = try await URLSession.shared.data(for: request)
            if let httpRes = response as? HTTPURLResponse, httpRes.statusCode == 200 {
                let remoteLessons = try JSONDecoder().decode([TokyoScenarioVideoLesson].self, from: data)
                if !remoteLessons.isEmpty {
                    self.lessons = remoteLessons
                    self.lastSyncDate = Date()
                    saveToLocalCache(remoteLessons)
                    print(" TokyoVideoLessonDataManager: Successfully synced \(remoteLessons.count) dynamic lessons from cloud.")
                }
            }
        } catch {
            print("ℹ️ TokyoVideoLessonDataManager: Using local/cached lessons (Cloud manifest unreachable or offline: \(error.localizedDescription))")
        }
    }

    // MARK: - Built-in Default Lessons (100% Valid YouTube IDs)
    public var builtInDefaultLessons: [TokyoScenarioVideoLesson] {
        return [
            TokyoScenarioVideoLesson(
                id: "yt_yamanote_01",
                episodeNumber: 1,
                scenarioId: "s_yamanote_rush",
                title: "EP. 01 • Tokyo Metro & Yamanote Line Platform Broadcasts",
                titleJa: "山手線ラッシュ・乗り換えアナウンス完全攻略",
                titleZh: "EP. 01 • 东京地铁与山手线站台广播完全攻略",
                channelName: "TokyoFlow Japanese",
                youtubeVideoId: "yN6dTC-LBz8",
                durationLabel: "00:34",
                levelBadge: "JLPT N4-N3",
                district: "Shinjuku (新宿)",
                category: "transit",
                thumbnailIcon: "tram.fill",
                summary: "Deconstruct Shinjuku Station morning rush departure melodies, tactile yellow paving warnings, inner/outer loop announcements, and natural wayfinding phrases.",
                summaryZh: "深度解析新宿站早高峰发车音乐、黄色盲道安全警示、内环/外环进站广播与1秒自然问路句型。",
                chapters: [
                    VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Platform Train Arrival", titleZh: "列车进站广播解析", summary: "Shinjuku Station Platform 2 Yamanote Loop live transit announcement breakdown", summaryZh: "新宿站2号站台山手线内环实况广播逐句精讲"),
                    VideoChapterBookmark(timeString: "00:09", timeSeconds: 9, title: "Tactile Warning Blocks", titleZh: "黄色盲道安全退后提醒", summary: "Safety announcement behind yellow braille tiles", summaryZh: "公共安全播报「请退至黄色盲道内侧」句式解析"),
                    VideoChapterBookmark(timeString: "00:19", timeSeconds: 19, title: "1-Second Wayfinding", titleZh: "1秒换乘问路黄金公式", summary: "Instant golden phrases to ask station staff for Chuo Line / Sobu Line transfers", summaryZh: "在庞大交通枢纽中向站务员询问中央线/总武线换乘站台的速效公式"),
                    VideoChapterBookmark(timeString: "00:27", timeSeconds: 27, title: "Shadowing & Recap", titleZh: "影子跟读与声调复述", summary: "Sample-accurate native pitch accent repetition drill", summaryZh: "地道东京音调实时复述训练")
                ],
                keyTakeaways: [
                    VideoKeyTakeaway(
                        phrase: "まもなく、2番線に山手線内回りがまいります。",
                        furigana: "まもなく、にばんせんに やまのてせん うちまわりが まいります。",
                        meaning: "The Yamanote Line inner loop will soon arrive at track 2.",
                        meaningZh: "2号站台即将有山手线内环列车进站。",
                        explanation: "'Mairimasu' is the humble form of 'kimasu' (to come), standard JR automated announcement grammar.",
                        explanationZh: "「まいります」是「来ます」的谦让语，属于JR标准自动广播用语。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "黄色い点字ブロックの内側までお下がりください。",
                        furigana: "きいろい てんじぶろっくの うちがわまで おさがりください。",
                        meaning: "Please stand back behind the yellow tactile braille blocks.",
                        meaningZh: "请退到黄色盲道砖的内侧等候。",
                        explanation: "'O-sagari kudasai' is a polite public safety request.",
                        explanationZh: "「お下がりください」是极其礼貌的公共安全指引要求。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "中央線への乗り換えはどのホームですか？",
                        furigana: "ちゅうおうせんへの のりかえは どのほーむですか？",
                        meaning: "Which platform is the transfer for the Chuo Line?",
                        meaningZh: "请问换乘中央线是在哪个站台？",
                        explanation: "Essential formula when lost inside massive transit hubs.",
                        explanationZh: "在大型电车站迷路时最直接实用的问路句型。"
                    )
                ]
            ),
            TokyoScenarioVideoLesson(
                id: "yt_kombini_02",
                episodeNumber: 2,
                scenarioId: "s_kombini_register",
                title: "EP. 02 • Convenience Store Survival: 7-Eleven Rapid Checkout",
                titleJa: "コンビニレジ連環問・お弁当温め・袋不要",
                titleZh: "EP. 02 • 日本便利店生存指南：7-Eleven极速结账连环问",
                channelName: "TokyoFlow Japanese",
                youtubeVideoId: "6er1tWAH_oQ",
                durationLabel: "00:25",
                levelBadge: "JLPT N5-N4",
                district: "Shibuya (渋谷)",
                category: "kombini",
                thumbnailIcon: "cart.fill",
                summary: "From 'Obentō atatamemasu ka?' to 'Reji-bukuro wa go-riyō desu ka?', decode all rapid-fire Japanese convenience store register questions and 1-second natural responses.",
                summaryZh: "从「便当要加热吗？」到「需要塑料袋吗？」，完全破解日本便利店收银台连环提问与1秒自然回应。",
                chapters: [
                    VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Register Inquiries", titleZh: "收银连环问开篇", summary: "Live breakdown of the rapid checkout questions at Japanese 7-Eleven", summaryZh: "日本7-Eleven收银员语速拆解"),
                    VideoChapterBookmark(timeString: "00:07", timeSeconds: 7, title: "Microwave Heating & Bags", titleZh: "便当加热与塑料袋", summary: "Proper register nuances of 'Atatamete kudasai' vs 'Daijōbu desu'", summaryZh: "「请加热」与礼貌婉拒「不需要袋子」的语感差异"),
                    VideoChapterBookmark(timeString: "00:15", timeSeconds: 15, title: "Suica Payment", titleZh: "Suica/移动支付指定", summary: "Suica, PayPay, and cashless payment designation formulas", summaryZh: "使用西瓜卡、PayPay及无现金支付的指定句式"),
                    VideoChapterBookmark(timeString: "00:20", timeSeconds: 20, title: "Checkout Roleplay Drill", titleZh: "实景角色扮演演练", summary: "Immersive checkout dialogue practice", summaryZh: "沉浸式结账模拟互动")
                ],
                keyTakeaways: [
                    VideoKeyTakeaway(
                        phrase: "お弁当温めますか？",
                        furigana: "おべんとう あたためますか？",
                        meaning: "Would you like your bento heated up in the microwave?",
                        meaningZh: "便当需要用微波炉加热吗？",
                        explanation: "Standard staff question. Reply 'Atatamete kudasai' (Please heat it) or 'Sono mama de daijōbu desu' (As-is is fine).",
                        explanationZh: "店员必问句。回答「温めてください」（请加热）或「そのままで大丈夫です」（不用了，直接这样就好）。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "レジ袋は大丈夫です。",
                        furigana: "れじぶくろは だいじょうぶです。",
                        meaning: "I'm fine without a plastic bag (I have my own).",
                        meaningZh: "不需要塑料袋（我有自备袋）。",
                        explanation: "'Daijōbu desu' with a gentle nod is the polite, natural way to decline.",
                        explanationZh: "轻微点头并说「大丈夫です」是礼貌婉拒的标准地道表达。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "Suicaでお願いします。",
                        furigana: "すいかで おねがいします。",
                        meaning: "With Suica (IC card), please.",
                        meaningZh: "请用Suica（西瓜卡）结账。",
                        explanation: "Universal payment designation formula.",
                        explanationZh: "结账时指定支付方式的通用句型（〇〇でおねがいします）。"
                    )
                ]
            ),
            TokyoScenarioVideoLesson(
                id: "yt_izakaya_03",
                episodeNumber: 3,
                scenarioId: "s_izakaya_toast",
                title: "EP. 03 • Izakaya Mastery: Showa Pub Ordering, Otoshi & Toasting",
                titleJa: "居酒屋注文・お通し文化・とりあえず生！",
                titleZh: "EP. 03 • 居酒屋实战秘籍：入座点单、小菜文化与干杯礼仪",
                channelName: "TokyoFlow Japanese",
                youtubeVideoId: "B4sN_BkLcOw",
                durationLabel: "00:26",
                levelBadge: "JLPT N4-N3",
                district: "Shinjuku Omoide Yokocho (思い出横丁)",
                category: "dining",
                thumbnailIcon: "wineglass.fill",
                summary: "The golden rule of ordering 'Toriaezu nama!' first, Otoshi appetizer customs, salt vs tare sauce for yakitori skewers, and asking for the final bill.",
                summaryZh: "居酒屋「先来杯生啤！」黄金开场法则、前菜（お通し）规矩、烤串选盐味还是酱汁、以及买单开发票技巧。",
                chapters: [
                    VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Entering the Izakaya", titleZh: "入座与热毛巾", summary: "Hot towels (Oshibori) and ordering 'Toriaezu nama!'", summaryZh: "接热毛巾与「先来杯生啤！」开场口诀"),
                    VideoChapterBookmark(timeString: "00:07", timeSeconds: 7, title: "Yakitori Salt vs Tare", titleZh: "烤串盐味与酱汁选择", summary: "Choosing between Shio (Salt) and Tare (Sweet Soy Sauce)", summaryZh: "盐味（塩）与甜酱油酱汁（タレ）的区分与选择技巧"),
                    VideoChapterBookmark(timeString: "00:14", timeSeconds: 14, title: "The Art of Kanpai!", titleZh: "干杯与碰杯礼仪", summary: "Glass rim etiquette and saying 'Otsukaresama desu!'", summaryZh: "酒杯高度礼节与「辛苦啦」干杯祝词"),
                    VideoChapterBookmark(timeString: "00:20", timeSeconds: 20, title: "Bill & Receipt Request", titleZh: "买单与开具发票", summary: "Mastering 'O-kaikei' and 'Ryōshūsho' phrases", summaryZh: "结账买单与索取正式发票的敬语表达")
                ],
                keyTakeaways: [
                    VideoKeyTakeaway(
                        phrase: "とりあえず生ビール二つお願いします！",
                        furigana: "とりあえず なまびーる ふたつ おねがいします！",
                        meaning: "Two draft beers to start, please!",
                        meaningZh: "先来两杯生啤酒，谢谢！",
                        explanation: "The iconic opening order phrase at every Japanese izakaya pub.",
                        explanationZh: "日本居酒屋最经典的开场点酒口令。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "焼き鳥は塩とタレ、どちらにしますか？",
                        furigana: "やきとりは しおと たれ、どちらにしますか？",
                        meaning: "Would you like your yakitori skewers with salt or sweet tare sauce?",
                        meaningZh: "烤串要盐烤还是酱烤呢？",
                        explanation: "Standard server question. Shio highlights ingredient freshness.",
                        explanationZh: "服务员标准提问。盐烤突显食材原味，酱烤口感浓郁。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "お会計と領収書をお願いします。",
                        furigana: "おかいけいと りょうしゅうしょを おねがいします。",
                        meaning: "The check and an official receipt, please.",
                        meaningZh: "请结账，并开一张正式收据（发票）。",
                        explanation: "Polite phrase to settle the bill and request a company receipt.",
                        explanationZh: "买单并索取公司报销发票的标准礼貌用语。"
                    )
                ]
            ),
            TokyoScenarioVideoLesson(
                id: "yt_akiba_04",
                episodeNumber: 4,
                scenarioId: "s_akiba_manga",
                title: "EP. 04 • Akihabara Pilgrimage: Figures, Merch & Manga Tax-Free",
                titleJa: "秋葉原アニメ・限定グッズ・同人誌探訪",
                titleZh: "EP. 04 • 秋叶原圣地巡礼：手办、限定谷子与漫画免税",
                channelName: "TokyoFlow Japanese",
                youtubeVideoId: "iaGo6ey75Ws",
                durationLabel: "00:30",
                levelBadge: "JLPT N3-N2",
                district: "Akihabara (秋葉原)",
                category: "shopping",
                thumbnailIcon: "sparkles.tv.fill",
                summary: "Explore multi-story Akihabara hobby towers, ask clerks for new season anime original light novels, pre-order bonuses, unopened mint figure box inspections, and tax-free counter processing.",
                summaryZh: "探索秋叶原多层动漫大楼，向店员寻找当季新番原作轻小说、预购特典确认、全新手办验盒与免税柜台办理。",
                chapters: [
                    VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "Akiba Tower Exploration", titleZh: "动漫大楼楼层导览", summary: "Reading hobby building floor directories and navigating specialty character floors", summaryZh: "看懂动漫大楼各层分类及特色专区"),
                    VideoChapterBookmark(timeString: "00:08", timeSeconds: 8, title: "Locating Manga & Novels", titleZh: "寻找新番原作漫画", summary: "Asking store clerks for current season anime original tankobon and light novels", summaryZh: "向店员询问当季热门新番单行本与轻小说"),
                    VideoChapterBookmark(timeString: "00:16", timeSeconds: 16, title: "Pre-order Perks & Boxes", titleZh: "限定特典与盲盒确认", summary: "Clarifying limited edition bonus postcards, acrylic stands, and blind badges", summaryZh: "确认是否附带限定明信片、亚克力立牌等独家特典"),
                    VideoChapterBookmark(timeString: "00:24", timeSeconds: 24, title: "Tax-Free Processing", titleZh: "免税手续办理流程", summary: "Passport presentation and tax-exemption seal procedure", summaryZh: "出示护照与消费满5,000日元免税办理实操")
                ],
                keyTakeaways: [
                    VideoKeyTakeaway(
                        phrase: "今期の新作アニメの原作はどこにありますか？",
                        furigana: "こんきの しんさくあにめの げんさくは どこに ありますか？",
                        meaning: "Where are the original manga/novels for this season's new anime?",
                        meaningZh: "请问这季度新番动画的原作放在哪里？",
                        explanation: "The most practical book-finding phrase in anime specialty bookstores like Animate and Toranoana.",
                        explanationZh: "在Animate或虎之穴等动漫书店中最实用的寻书句型。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "購入特典はまだ付きますか？",
                        furigana: "こうにゅうとくてんは まだ つきますか？",
                        meaning: "Does this still come with the purchase bonus perk?",
                        meaningZh: "现在购买还会附赠特典礼品吗？",
                        explanation: "Essential phrase to confirm remaining exclusive merchandise gifts before purchasing.",
                        explanationZh: "结账前确认限量赠品/特典是否还有库存的必备短语。"
                    ),
                    VideoKeyTakeaway(
                        phrase: "免税手続きをお願いできますか？",
                        furigana: "めんぜいてつづきを おねがいできますか？",
                        meaning: "Could you process tax-free exemption, please?",
                        meaningZh: "可以帮我办理免税手续吗？",
                        explanation: "Standard phrase at checkout when spending over 5,000 JPY on taxable goods.",
                        explanationZh: "在商场/药妆店消费满额时向收银员提出退税的标准敬语。"
                    )
                ]
            )
        ]
    }
}
