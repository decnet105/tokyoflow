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
            scenarioId: "s_yamanote_rush",
            title: "【东京电车现场】山手线高峰换乘与站台广播彻底解密",
            titleJa: "山手線ラッシュ・乗り換えアナウンス完全攻略",
            channelName: "TokyoFlow Japanese / TokyoFlow 日语",
            youtubeVideoId: "6dxbsPYp654",
            durationLabel: "10:45",
            levelBadge: "JLPT N4-N3",
            district: "新宿・Shinjuku",
            category: "transit",
            thumbnailIcon: "tram.fill",
            summary: "实景拆解新宿站早高峰发车音乐、点字盲道警示广播、内环外环路线辨析，以及面对列车延误时的地道问路短语。",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "现场还原", summary: "新宿站山手线2号站台实景广播声效还原"),
                VideoChapterBookmark(timeString: "02:30", timeSeconds: 150, title: "核心语法", summary: "「〜がまいります」尊他语与敬语动词拆解"),
                VideoChapterBookmark(timeString: "05:40", timeSeconds: 340, title: "站台地道口语", summary: "问路与换乘中央线的1秒金句"),
                VideoChapterBookmark(timeString: "08:15", timeSeconds: 495, title: "跟读与角色扮演", summary: "母语声调逐句Shadowing跟读训练")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "まもなく、2番線に山手線内回りがまいります。", furigana: "まもなく、にばんせんに やまのてせん うちまわりが まいります。", meaning: "2号站台内环山手线即将进站。", explanation: "「まいります」是「来ます」的谦逊语/郑重语表达，JR电车广播标准句。"),
                VideoKeyTakeaway(phrase: "黄色い点字ブロックの内側までお下がりください。", furigana: "きいろい てんじぶろっくの うちがわまで おさがりください。", meaning: "请退到黄色盲道线内侧候车。", explanation: "「お下がりください」为极其礼貌的劝告要求。"),
                VideoKeyTakeaway(phrase: "中央線への乗り換えはどのホームですか？", furigana: "ちゅうおうせんへの のりかえは どのほーむですか？", meaning: "请问换乘中央线在哪个站台？", explanation: "快速向站务员求助的高频口语句型。")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_kombini_02",
            scenarioId: "s_kombini_register",
            title: "【便利店攻防战】日本7-11结账连环问与微波炉加热全攻略",
            titleJa: "コンビニレジ連環問・お弁当温め・袋不要",
            channelName: "TokyoFlow Japanese / TokyoFlow 日语",
            youtubeVideoId: "bOcegXJ3_Qo",
            durationLabel: "08:20",
            levelBadge: "JLPT N5-N4",
            district: "涩谷・Shibuya",
            category: "kombini",
            thumbnailIcon: "cart.fill",
            summary: "从「お弁当温めますか？」到「レジ袋はご利用ですか？」，拆解日本便利店收银台所有高频选项与1秒自然回复方案。",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "收银实景连环问", summary: "便利店员快速语速四连问实录"),
                VideoChapterBookmark(timeString: "02:10", timeSeconds: 130, title: "加热与塑料袋", summary: "「温めてください」「大丈夫です」的正确语感"),
                VideoChapterBookmark(timeString: "04:50", timeSeconds: 290, title: "电子支付与积分", summary: "Suica与PayPay刷卡礼仪"),
                VideoChapterBookmark(timeString: "06:40", timeSeconds: 400, title: "结账角色实战", summary: "沉浸式结账跟读演练")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "お弁当温めますか？", furigana: "おべんとう あたためますか？", meaning: "便当需要加热吗？", explanation: "便利店标准服务用语。回复「温めてください」或「そのままで大丈夫です」。"),
                VideoKeyTakeaway(phrase: "レジ袋は大丈夫です。", furigana: "れじぶくろは だいじょうぶです。", meaning: "不用塑料袋了（我有自带）。", explanation: "「大丈夫です」在口语中表示委婉拒绝。"),
                VideoKeyTakeaway(phrase: "Suicaでお願いします。", furigana: "すいかで おねがいします。", meaning: "请用Suica西瓜卡结账。", explanation: "指定付款方式的万能句型。")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_izakaya_03",
            scenarioId: "s_izakaya_toast",
            title: "【居酒屋江湖】日本昭和居酒屋点菜点单、开胃菜与干杯礼仪",
            titleJa: "居酒屋注文・お通し文化・とりあえず生！",
            channelName: "TokyoFlow Japanese / TokyoFlow 日语",
            youtubeVideoId: "M2i5zH7aWqk",
            durationLabel: "12:15",
            levelBadge: "JLPT N4-N3",
            district: "新宿・Shinjuku Omoide Yokocho",
            category: "dining",
            thumbnailIcon: "wineglass.fill",
            summary: "入座先点「とりあえず生！」的黄金法则、Otoshi开胃菜文化、加单刺身烤串与最后结账开发票的完整流程。",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "居酒屋入座", summary: "毛巾（おしぼり）与第一轮酒水"),
                VideoChapterBookmark(timeString: "03:15", timeSeconds: 195, title: "热门菜品点单", summary: "烤鸡肉串盐烤（塩）与酱烤（タレ）的区分"),
                VideoChapterBookmark(timeString: "07:00", timeSeconds: 420, title: "酒席互动干杯", summary: "杯沿位置与「お疲れ様でした！」"),
                VideoChapterBookmark(timeString: "09:45", timeSeconds: 585, title: "结账与发票", summary: "「お会計」与「領収書」地道说法")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "とりあえず生ビール二つお願いします！", furigana: "とりあえず なまびーる ふたつ おねがいします！", meaning: "先来两杯生啤！", explanation: "居酒屋最地道的开场点酒句型。"),
                VideoKeyTakeaway(phrase: "焼き鳥は塩とタレ、どちらにしますか？", furigana: "やきとりは しおと たれ、どちらにしますか？", meaning: "烤鸡肉串要盐烤还是酱汁烤？", explanation: "店员必问搭配问题。"),
                VideoKeyTakeaway(phrase: "お会計と領収書をお願いします。", furigana: "おかいけいと りょうしゅうしょを おねがいします。", meaning: "请买单并开具发票。", explanation: "正式买单与公司报销凭证请求。")
            ]
        ),
        TokyoScenarioVideoLesson(
            id: "yt_akiba_04",
            scenarioId: "s_akiba_manga",
            title: "【秋叶原朝圣】动漫周边淘货、限定手办问询与同人展会实战",
            titleJa: "秋葉原アニメ・限定グッズ・同人誌探訪",
            channelName: "TokyoFlow Japanese / TokyoFlow 日语",
            youtubeVideoId: "N1vM-N12345",
            durationLabel: "09:50",
            levelBadge: "JLPT N3-N2",
            district: "秋叶原・Akihabara",
            category: "shopping",
            thumbnailIcon: "sparkles.tv.fill",
            summary: "深入秋叶原各大动漫店铺，向店员询问「这季新番原著漫画在几楼？」、「是否有会场限定特典？」。",
            chapters: [
                VideoChapterBookmark(timeString: "00:00", timeSeconds: 0, title: "秋叶原探店", summary: "动漫大厦楼层索引阅读"),
                VideoChapterBookmark(timeString: "02:40", timeSeconds: 160, title: "寻找新番原作", summary: "原作漫画与轻小说所在分区询问"),
                VideoChapterBookmark(timeString: "05:30", timeSeconds: 330, title: "限定特典与预订", summary: "预约特典与盲盒手办用语"),
                VideoChapterBookmark(timeString: "08:00", timeSeconds: 480, title: "粉丝交流演练", summary: "与同好交流喜好作品的自然短语")
            ],
            keyTakeaways: [
                VideoKeyTakeaway(phrase: "今期の新作アニメの原作はどこにありますか？", furigana: "こんきの しんさくあにめの げんさくは どこに ありますか？", meaning: "请问这季度新作动画的原作在哪里？", explanation: "动漫书店最实用的寻书句型。"),
                VideoKeyTakeaway(phrase: "購入特典はまだ付きますか？", furigana: "こうにゅうとくてんは まだ つきますか？", meaning: "请问现在买还附送购买特典吗？", explanation: "确认限定赠品的标准问法。")
            ]
        )
    ]

    public func lesson(for scenarioId: String) -> TokyoScenarioVideoLesson? {
        return lessons.first { $0.scenarioId == scenarioId }
    }
}
