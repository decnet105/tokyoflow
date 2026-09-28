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
            title: "NHK Journal Deep Immersion",
            titleJa: "NHKジャーナル 総合ニュース特報",
            subtitle: "Authentic NHK radio broadcast with verbatim transcript, Tokyo weather, economics, culture, and precise word-by-word shadowing.",
            durationSec: 138.6,
            durationLabel: "2 Mins (2:18)",
            audioFileName: "nhk_journal_55min.m4a",
            streamUrl: nil,
            badge: "NHK VERBATIM",
            icon: "antenna.radiowaves.left.and.right",
            chapters: [
                RadioChapter(
                    id: "c1",
                    title: "Headlines & Opening",
                    titleJa: "オープニング・全国の主要ニュース",
                    startTimeSec: 0.0,
                    description: "Opening signature broadcast chimes and national headlines.",
                    transcriptSentences: [
                        NewsSentence(id: "r1_1", japanese: "皆様こんばんは。NHKジャーナル、夜の総合ニュースです。", furigana: "みなさまこんばんは。えぬえいちけーじゃーなる、よるのそうごうにゅーすです。", english: "Good evening everyone. This is NHK Journal with tonight's comprehensive evening news.", startTimeSec: 0.0, endTimeSec: 6.576),
                        NewsSentence(id: "r1_2", japanese: "今夜の主なニュースをお伝えいたします。", furigana: "こんやのおもなにゅーすをおつたえいたします。", english: "We bring you tonight's major headlines.", startTimeSec: 7.176, endTimeSec: 10.992),
                        NewsSentence(id: "r1_3", japanese: "JR東日本は、東京やその近くを走る電車の終電の時間を早めると発表しました。", furigana: "じぇいあーるひがしにほんは、とうきょうやそのちかくをはしるでんしゃのしゅうでんのじかんをはやめるとはっぴょうしました。", english: "JR East announced that it will advance the last train times for trains operating in and around Tokyo.", startTimeSec: 11.592, endTimeSec: 19.872),
                        NewsSentence(id: "r1_4", japanese: "山手線や中央線など多くの主要路線で、終電が15分から30分程度早くなります。", furigana: "やまのてせいやちゅうおうせんなどおおくのしゅようろせんで、しゅうでんがじゅうごふんからさんじゅっぷんていどはやくなります。", english: "On major lines including the Yamanote and Chuo Lines, final departures will be 15 to 30 minutes earlier.", startTimeSec: 20.472, endTimeSec: 29.088),
                        NewsSentence(id: "r1_5", japanese: "深夜に線路を点検・修繕する作業員の安全と働く時間を確保するための措置です。", furigana: "しんやにせんろをてんけん・しゅうぜんするさぎょういんのあんぜんとはたらくじかんをかくほするためのそちです。", english: "This measure is to secure safe working hours for crews inspecting and repairing tracks overnight.", startTimeSec: 29.688, endTimeSec: 37.608)
                    ]
                ),
                RadioChapter(
                    id: "c2",
                    title: "Tokyo Weather & Climate",
                    titleJa: "台風・首都圏の気象情報",
                    startTimeSec: 38.808,
                    description: "Detailed Tokyo weather forecast, typhoon alerts, and transit operations.",
                    transcriptSentences: [
                        NewsSentence(id: "r2_1", japanese: "続いて、気象庁からの首都圏の気象情報をお伝えします。", furigana: "つづいて、きしょうちょうからのしゅとけんのきしょうじょうほうをおつたえします。", english: "Next is the metropolitan weather update from the Japan Meteorological Agency.", startTimeSec: 38.808, endTimeSec: 43.896),
                        NewsSentence(id: "r2_2", japanese: "南の海上に発生した大型の台風が、明日の夜にかけて関東地方に接近する見込みです。", furigana: "みなみのかいじょうにはっせいしたおおがたのたいふうが、あすのよるにかけてかんとうちほうにせっきんするみこみです。", english: "A large typhoon formed over southern waters is expected to approach the Kanto region by tomorrow evening.", startTimeSec: 44.496, endTimeSec: 52.08),
                        NewsSentence(id: "r2_3", japanese: "東京の広い範囲で非常に強い風と激しい雨が予想されています。", furigana: "とうきょうのひろいはんいでひじょうにつよいかぜとはげしいあめがよそうされています。", english: "Extremely strong winds and heavy rainfall are anticipated across widespread parts of Tokyo.", startTimeSec: 52.68, endTimeSec: 57.912),
                        NewsSentence(id: "r2_4", japanese: "土砂災害や低い土地の浸水に警戒し、最新の交通情報を確認してください。", furigana: "どしゃさいがいやひくいとちのしんすいにけいかいし、さいしんのこうつうじょうほうをごかくにんください。", english: "Please stay alert for landslides and flooded lowlands, and check the latest transit updates.", startTimeSec: 58.512, endTimeSec: 65.112)
                    ]
                ),
                RadioChapter(
                    id: "c3",
                    title: "Tokyo Living & Economy",
                    titleJa: "暮らしと経済インサイト",
                    startTimeSec: 66.312,
                    description: "In-depth look at Tokyo convenience stores and food waste reduction.",
                    transcriptSentences: [
                        NewsSentence(id: "r3_1", japanese: "暮らしのニュースです。東京都内のコンビニ各社で、食品ロス削減の取り組みが広がっています。", furigana: "くらしのにゅーすです。とうきょうとないのこんびにかくしゃで、しょくひんろすさくげんのとりくみがひろがっています。", english: "In lifestyle news: Convenience store chains across Tokyo are expanding food loss reduction initiatives.", startTimeSec: 66.312, endTimeSec: 75.0),
                        NewsSentence(id: "r3_2", japanese: "消費期限が近づいたおにぎりやサンドイッチに「エコ値引きシール」が貼られ、安く購入できます。", furigana: "しょうひきげんがちかづいたおにぎりやさんどいっちに「えこねびきしーる」がはられ、やすくこうにゅうできます。", english: "Eco-discount stickers are applied to onigiri and sandwiches near expiration, allowing bargain purchases.", startTimeSec: 75.6, endTimeSec: 83.808),
                        NewsSentence(id: "r3_3", japanese: "お店は廃棄するゴミを減らすことができ、利用者からも節約になると好評です。", furigana: "おみせははいきするごみをへらすことができ、りようしゃからもせつやくになるとこうひょうです。", english: "Stores can reduce discarded waste, and shoppers praise it as an effective way to save money.", startTimeSec: 84.408, endTimeSec: 91.248)
                    ]
                ),
                RadioChapter(
                    id: "c4",
                    title: "Culture & Manga Feature",
                    titleJa: "日本の文化・秋葉原マンガ特集",
                    startTimeSec: 92.448,
                    description: "Special report on Akihabara manga festival and overseas fans.",
                    transcriptSentences: [
                        NewsSentence(id: "r4_1", japanese: "文化の話題です。東京・秋葉原で、国内外の人気マンガが集まる秋のイベントが始まりました。", furigana: "ぶんかのわだいです。とうきょう・あきはばらで、こくないがいのにんきまんががあつまるあきのいべんとがはじまりました。", english: "In culture news: An autumn festival featuring popular domestic and international manga has begun in Akihabara.", startTimeSec: 92.448, endTimeSec: 100.632),
                        NewsSentence(id: "r4_2", japanese: "会場には限定グッズや原画の展示コーナーが並び、多くのファンで賑わっています。", furigana: "かいじょうにはげんていぐっずやげんがのてんじこーなーがならび、おおくのふぁんでにぎわっています。", english: "Limited edition goods and original artwork exhibition booths are lined up, bustling with enthusiastic fans.", startTimeSec: 101.232, endTimeSec: 107.616),
                        NewsSentence(id: "r4_3", japanese: "訪れた外国人観光客は、「生で日本のマンガ文化に触れられて感動した」と笑顔で話していました。", furigana: "おとずれたがいこくじんかんこうきゃくは、「なまでにほんのまんがぶんかにふれられてかんどうした」とえがおではなしていました。", english: "Visiting international tourists smiled and said they were deeply moved to experience Japanese manga culture live.", startTimeSec: 108.216, endTimeSec: 115.992)
                    ]
                ),
                RadioChapter(
                    id: "c5",
                    title: "Tomorrow's Outlook & Ending",
                    titleJa: "明日の展望・エンディング",
                    startTimeSec: 117.192,
                    description: "Final review, sports wrap-up, and relaxing night sign-off.",
                    transcriptSentences: [
                        NewsSentence(id: "r5_1", japanese: "以上、今夜のNHKジャーナル総合ニュースをお送りいたしました。", furigana: "いじょう、こんやのえぬえいちけーじゃーなるそうごうにゅーすをおおくりいたしました。", english: "This concludes tonight's edition of the NHK Journal comprehensive evening news.", startTimeSec: 117.192, endTimeSec: 123.168),
                        NewsSentence(id: "r5_2", japanese: "明日は各地で雨が強まる見込みですので、お出かけの際は足元に十分ご注意ください。", furigana: "あすはかくちであめがつよまるみこみですので、おでかけのさいはあしもとにじゅうぶんごちゅういください。", english: "Rain is expected to strengthen across various regions tomorrow; please take care of your footing when going out.", startTimeSec: 123.768, endTimeSec: 131.52),
                        NewsSentence(id: "r5_3", japanese: "それでは皆様、どうぞ良い夜をお過ごしください。おやすみなさい。", furigana: "それではみなさま、どうぞよいよるをおすごしください。おやすみなさい。", english: "We wish you all a pleasant and restful evening. Good night.", startTimeSec: 132.12, endTimeSec: 138.6)
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
