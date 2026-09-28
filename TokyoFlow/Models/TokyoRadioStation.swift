import Foundation

public struct RadioChapter: Identifiable, Hashable, Codable {
    public let id: String
    public let title: String
    public let titleJa: String
    public let startTimeSec: Double
    public let description: String
    public let transcriptSentences: [NewsSentence]

    public init(
        id: String,
        title: String,
        titleJa: String,
        startTimeSec: Double,
        description: String,
        transcriptSentences: [NewsSentence] = []
    ) {
        self.id = id
        self.title = title
        self.titleJa = titleJa
        self.startTimeSec = startTimeSec
        self.description = description
        self.transcriptSentences = transcriptSentences
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
                RadioChapter(
                    id: "c1",
                    title: "Headlines & Opening",
                    titleJa: "オープニング・全国の主要ニュース",
                    startTimeSec: 0.0,
                    description: "Opening signature chimes and live headline summaries.",
                    transcriptSentences: [
                        NewsSentence(id: "r1_1", japanese: "皆様こんばんは、NHKジャーナルです。", furigana: "みなさまこんばんは、えぬえいちけーじゃーなるです。", english: "Good evening everyone, this is NHK Journal.", startTimeSec: 0.0, endTimeSec: 15.0),
                        NewsSentence(id: "r1_2", japanese: "今夜の主なニュースをお伝えいたします。", furigana: "こんやのおもなにゅーすをおつたえいたします。", english: "We bring you tonight's major news headlines.", startTimeSec: 15.0, endTimeSec: 45.0),
                        NewsSentence(id: "r1_3", japanese: "JR東日本は、東京やその近くを走る電車の終電の時間を早めると発表しました。", furigana: "じぇいあーるひがしにほんは、とうきょうやそのちかくをはしるでんしゃのしゅうでんのじかんをはやめるとはっぴょうしました。", english: "JR East announced that it will advance the departure times of last trains operating in and around Tokyo.", startTimeSec: 45.0, endTimeSec: 120.0),
                        NewsSentence(id: "r1_4", japanese: "深夜の保守作業の時間を確保するのが主な理由です。", furigana: "しんやのほしゅさぎょうのじかんをかくほするのがおもなりゆうです。", english: "The primary reason is to secure adequate time for late-night maintenance operations.", startTimeSec: 120.0, endTimeSec: 300.0)
                    ]
                ),
                RadioChapter(
                    id: "c2",
                    title: "Tokyo Weather & Climate",
                    titleJa: "台風・首都圏の気象情報",
                    startTimeSec: 312.0,
                    description: "Detailed weather forecast and train transit conditions.",
                    transcriptSentences: [
                        NewsSentence(id: "r2_1", japanese: "気象庁によりますと、台風が関東地方に接近しています。", furigana: "きしょうちょうによりますと、たいふうがかんとうちほうにせっきんしています。", english: "According to the Meteorological Agency, a typhoon is approaching the Kanto region.", startTimeSec: 312.0, endTimeSec: 450.0),
                        NewsSentence(id: "r2_2", japanese: "東京の広い範囲で激しい雨が降る見込みです。", furigana: "とうきょうのひろいはんいではげしいあめがふるみこみです。", english: "Heavy rain is anticipated across widespread areas of Tokyo.", startTimeSec: 450.0, endTimeSec: 620.0),
                        NewsSentence(id: "r2_3", japanese: "土砂災害や河川の増水に警戒し、最新の交通情報をご確認ください。", furigana: "どしゃさいがいやかせんのぞうすいにけいかいし、さいしんのこうつうじょうほうをごかくにんください。", english: "Please stay alert for landslides and swollen rivers, and check the latest transit updates.", startTimeSec: 620.0, endTimeSec: 930.0)
                    ]
                ),
                RadioChapter(
                    id: "c3",
                    title: "Tokyo Living & Economy",
                    titleJa: "暮らしと経済インサイト",
                    startTimeSec: 940.0,
                    description: "In-depth analysis of consumer trends and living in Japan.",
                    transcriptSentences: [
                        NewsSentence(id: "r3_1", japanese: "先月日本を訪れた外国人観光客は過去最多を記録しました。", furigana: "せんげつにほんをおとずれたがいこくじんかんこうきゃくはかこさいたをきろくしました。", english: "The number of foreign tourists visiting Japan last month reached an all-time record high.", startTimeSec: 940.0, endTimeSec: 1250.0),
                        NewsSentence(id: "r3_2", japanese: "円安の影響で、買い物や飲食の消費が大きく伸びています。", furigana: "えんやすのえいきょうで、かいものやいんしょくのしょうひがおおきのびています。", english: "Driven by the weaker yen, retail shopping and dining expenditures have grown considerably.", startTimeSec: 1250.0, endTimeSec: 1600.0),
                        NewsSentence(id: "r3_3", japanese: "政府は観光地の混雑対策を進める方針です。", furigana: "せいふはかんこうちのこんざつたいさくをすすめるほうしんです。", english: "The government plans to advance countermeasures against congestion at major tourist destinations.", startTimeSec: 1600.0, endTimeSec: 1970.0)
                    ]
                ),
                RadioChapter(
                    id: "c4",
                    title: "Culture & Manga Feature",
                    titleJa: "日本の文化・マンガ・芸術特集",
                    startTimeSec: 1980.0,
                    description: "Special feature on Japanese creators and cultural heritage.",
                    transcriptSentences: [
                        NewsSentence(id: "r4_1", japanese: "世界中で日本のマンガやアニメの人気が高まっています。", furigana: "せかいじゅうでにほんのまんややあにめのにんきがたかまっています。", english: "Worldwide popularity of Japanese manga and anime continues to soar.", startTimeSec: 1980.0, endTimeSec: 2350.0),
                        NewsSentence(id: "r4_2", japanese: "秋葉原や原宿など、聖地を巡るファンが増加しています。", furigana: "あきはばらやはらじゅくなど、せいちをめぐるふぁんがぞうかしています。", english: "Fans embarking on pilgrimages to iconic cultural hotspots like Akihabara and Harajuku have increased.", startTimeSec: 2350.0, endTimeSec: 2780.0)
                    ]
                ),
                RadioChapter(
                    id: "c5",
                    title: "Tomorrow's Outlook & Ending",
                    titleJa: "明日の展望・エンディング",
                    startTimeSec: 2790.0,
                    description: "Final thoughts, sports wrap-up, and calm sign-off.",
                    transcriptSentences: [
                        NewsSentence(id: "r5_1", japanese: "以上、今夜のNHKジャーナルをお送りいたしました。", furigana: "いじょう、こんやのえぬえいちけーじゃーなるをおおくりいたしました。", english: "This concludes tonight's edition of NHK Journal.", startTimeSec: 2790.0, endTimeSec: 3050.0),
                        NewsSentence(id: "r5_2", japanese: "それでは皆様、どうぞ良い夜をお過ごしください。", furigana: "それではみなさま、どうぞよいよるをおすごしください。", english: "Until next time, we wish you all a pleasant and peaceful night.", startTimeSec: 3050.0, endTimeSec: 3297.0)
                    ]
                )
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
                RadioChapter(
                    id: "sc1",
                    title: "Morning Commute & Shinjuku Station",
                    titleJa: "朝の通勤・新宿駅ラッシュ",
                    startTimeSec: 0.0,
                    description: "Station melodies, ticket gates, and Yamanote announcements.",
                    transcriptSentences: [
                        NewsSentence(id: "sc1_1", japanese: "まもなく、2番線に山手線内回りがまいります。", furigana: "まもなく、にばんせんにやまのてせんうちまわりがまいります。", english: "The Yamanote Line Inner Loop train is now arriving on Track 2.", startTimeSec: 0.0, endTimeSec: 180.0),
                        NewsSentence(id: "sc1_2", japanese: "危険ですから、黄色い点字ブロックの内側までお下がりください。", furigana: "きけんですから、きいろいてんじぶろっくのうちがわまでおさがりください。", english: "For your safety, please wait behind the yellow braille textured line.", startTimeSec: 180.0, endTimeSec: 360.0),
                        NewsSentence(id: "sc1_3", japanese: "新宿駅での中央線への乗り換えは、階段を降りて向かいのホームです。", furigana: "しんじゅくえきでのちゅうおうせんへののりかえは、かいだんをおりてむかいのほーむです。", english: "To transfer to the Chuo Line at Shinjuku, proceed down the stairs to the opposite platform.", startTimeSec: 360.0, endTimeSec: 720.0)
                    ]
                ),
                RadioChapter(
                    id: "sc2",
                    title: "Kombini & Lunch Order",
                    titleJa: "コンビニ連環問・牛丼の注文",
                    startTimeSec: 720.0,
                    description: "7-Eleven cashiers, bento heating, and beef bowl customization.",
                    transcriptSentences: [
                        NewsSentence(id: "sc2_1", japanese: "いらっしゃいませ！お弁当温めますか？", furigana: "いらっしゃいませ！おべんとうあたためますか？", english: "Welcome! Would you like your bento warmed up?", startTimeSec: 720.0, endTimeSec: 980.0),
                        NewsSentence(id: "sc2_2", japanese: "温めてください。レジ袋は大丈夫です。", furigana: "あたためてください。れじぶくろはだいじょうぶです。", english: "Please warm it up. I don't need a shopping bag.", startTimeSec: 980.0, endTimeSec: 1250.0),
                        NewsSentence(id: "sc2_3", japanese: "お会計はSuicaでお願いします。", furigana: "おかいけいはすいかでおねがいします。", english: "I'd like to pay with my Suica card, please.", startTimeSec: 1250.0, endTimeSec: 1560.0)
                    ]
                ),
                RadioChapter(
                    id: "sc3",
                    title: "Afternoon Cafe & Akihabara Manga",
                    titleJa: "喫茶店・秋葉原マンガ探訪",
                    startTimeSec: 1560.0,
                    description: "Ordering matcha latte, reading raw manga, and buying limited goods.",
                    transcriptSentences: [
                        NewsSentence(id: "sc3_1", japanese: "アイス抹茶ラテを一つ、氷少なめでお願いします。", furigana: "あいすまっちゃらてをひとつ、こおりすくなめでおねがいします。", english: "One iced matcha latte with less ice, please.", startTimeSec: 1560.0, endTimeSec: 1950.0),
                        NewsSentence(id: "sc3_2", japanese: "今期の新作アニメの原作マンガはどこにありますか？", furigana: "こんきのしんさくあにめのげんさくまんがはどこにありますか？", english: "Where can I find the original manga for this season's new anime?", startTimeSec: 1950.0, endTimeSec: 2400.0)
                    ]
                ),
                RadioChapter(
                    id: "sc4",
                    title: "Evening Izakaya & Supermarket",
                    titleJa: "居酒屋乾杯・スーパー半額シール",
                    startTimeSec: 2400.0,
                    description: "Beer toast, Otoshi discussion, and 8PM grocery discount battles.",
                    transcriptSentences: [
                        NewsSentence(id: "sc4_1", japanese: "とりあえず生ビール二つとお刺身盛り合わせをお願いします！", furigana: "とりあえずなまびーるふたつとおさしみもりあわせをおねがいします！", english: "To start with, two draft beers and an assorted sashimi platter please!", startTimeSec: 2400.0, endTimeSec: 3000.0),
                        NewsSentence(id: "sc4_2", japanese: "お会計と領収書をお願いします。ごちそうさまでした！", furigana: "おかいけいとりょうしゅうしょをおねがいします。ごちそうさまでした！", english: "The bill and receipt please. Thank you for the delicious meal!", startTimeSec: 3000.0, endTimeSec: 3600.0)
                    ]
                )
            ]
        )
    ]
}
