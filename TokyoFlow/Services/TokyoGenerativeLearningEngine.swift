import Foundation
import Combine

public class TokyoGenerativeLearningEngine: ObservableObject {
    public static let shared = TokyoGenerativeLearningEngine()

    @Published public var currentPlan: TokyoDestinationPlan? = nil
    @Published public var isGenerating: Bool = false
    @Published public var selectedPresetId: String = "shibuya"

    public let presetDestinations: [(id: String, name: String, ja: String, district: String, icon: String, tag: String)] = [
        ("shibuya", "涩谷十字路口与忠犬八公", "渋谷スクランブル交差点", "涩谷・Shibuya", "figure.walk", "潮流与问路"),
        ("akiba", "秋叶原动漫与限定手办", "秋葉原アニメ街", "秋叶原・Akihabara", "sparkles.tv.fill", "淘货与询问"),
        ("shinjuku", "新宿思出横丁居酒屋", "新宿思い出横丁", "新宿・Shinjuku", "wineglass.fill", "点菜与干杯"),
        ("asakusa", "浅草寺雷门与人形烧", "浅草寺・仲見世通り", "台东・Asakusa", "building.columns.fill", "参拜与小吃"),
        ("ginza", "银座百货专柜免税购物", "銀座デパート免税", "中央・Ginza", "bag.fill", "退税与试穿"),
        ("tsukiji", "筑地/丰洲海鲜市场刺身", "豊洲・築地海鮮市場", "江东・Toyosu", "fork.knife", "点餐与排队"),
        ("roppongi", "六本木森美术馆夜景", "六本木ヒルズ展望台", "港区・Roppongi", "moon.stars.fill", "购票与观景"),
        ("haneda", "羽田机场入境与乘车券", "羽田空港モノレール", "大田・Haneda", "airplane.arrival", "交通求助")
    ]

    private init() {
        // Load default plan
        generatePlan(for: "shibuya")
    }

    public func generatePlan(for presetId: String) {
        self.isGenerating = true
        self.selectedPresetId = presetId

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            self.currentPlan = self.buildPlan(for: presetId)
            self.isGenerating = false
        }
    }

    public func generateCustomPlan(userPrompt: String) {
        self.isGenerating = true
        self.selectedPresetId = "custom"

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.4) {
            let prompt = userPrompt.trimmingCharacters(in: .whitespacesAndNewlines)
            let plan = TokyoDestinationPlan(
                id: "custom_\(UUID().uuidString.prefix(6))",
                destinationName: prompt.isEmpty ? "东京自由行探索" : prompt,
                destinationJa: "東京カスタム探索",
                district: "东京・Custom Area",
                categoryIcon: "sparkles",
                tag: "AI 动态定制生成",
                overview: "为你实时定制「\(prompt)」场景下的核心生存句型、实况角色扮演及日式礼仪指南。",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "すみません、ここはどこですか？",
                        furigana: "すみません、ここは どこですか？",
                        romaji: "sumimasen, koko wa doko desu ka?",
                        chinese: "不好意思，请问这里是哪里？",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "迷路或确认当前位置时的最快速求助句型。",
                        audioKey: "すみません"
                    ),
                    GenerativePhrase(
                        japanese: "これをお願いします。",
                        furigana: "これを おねがいします。",
                        romaji: "kore o onegaishimasu.",
                        chinese: "请给我这个 / 请帮我办理这个。",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "手指菜单、商品或屏幕时的万能决定句型。",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "クレジットカードは使えますか？",
                        furigana: "くれじっとかーどは つかえますか？",
                        romaji: "kurejitto kaado wa tsukaemasu ka?",
                        chinese: "请问可以使用信用卡吗？",
                        pitchAccent: "③ 尾高型",
                        situationNote: "结账付款前确认支付方式。",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "店员", speakerRole: "現地スタッフ", japanese: "いらっしゃいませ！何かお探しですか？", furigana: "いらっしゃいませ！なにか おさがしですか？", chinese: "欢迎光临！请问在找什么呢？", isUser: false),
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "旅行者", japanese: "これと同じものはありますか？", furigana: "これと おなじものは ありますか？", chinese: "请问有和这个一样的吗？", isUser: true),
                    GenerativeDialogueTurn(speaker: "店员", speakerRole: "現地スタッフ", japanese: "かしこまりました。こちらへどうぞ！", furigana: "かしこまりました。こちらへ どうぞ！", chinese: "明白，请跟我往这边来！", isUser: false)
                ],
                culturalTips: [
                    "在日本公众场合交谈请保持轻声，避免影响他人。",
                    "进店消费通常需在收银台出示护照以享受免税（Tax-Free）。",
                    "遇到困难时只要礼貌说一句「すみません（不好意思）」，母语者都会热情回应。"
                ],
                challengeMission: "在「\(prompt)」完成一次地道日文问询并向店员说出「ありがとうございます！」"
            )
            self.currentPlan = plan
            self.isGenerating = false
        }
    }

    private func buildPlan(for presetId: String) -> TokyoDestinationPlan {
        switch presetId {
        case "shibuya":
            return TokyoDestinationPlan(
                id: "shibuya",
                destinationName: "涩谷十字路口与忠犬八公",
                destinationJa: "渋谷スクランブル交差点・ハチ公前",
                district: "涩谷・Shibuya",
                categoryIcon: "figure.walk",
                tag: "潮流与地标问路",
                overview: "世界人流量最大的十字路口。掌握如何向路人询问八公像出口、SHIBUYA SKY 展望台入口及网红拍照点。",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "ハチ公口はどちらですか？",
                        furigana: "はちこうぐちは どちらですか？",
                        romaji: "hachikou guchi wa dochira desu ka?",
                        chinese: "请问八公像出口在哪个方向？",
                        pitchAccent: "② 中高型",
                        situationNote: "走出涩谷站庞大地下迷宫时，最关键的寻路句型。",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "写真を撮っていただけますか？",
                        furigana: "しゃしんを とって いただけますか？",
                        romaji: "shashin o totte itadakemasu ka?",
                        chinese: "可以麻烦您帮我们拍张照片吗？",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "在十字路口或地标前请热心路人合影的极高礼貌表达。",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "スクランブルスクエアへはどう行けばいいですか？",
                        furigana: "すくらんぶる すくえあへは どう いけば いいですか？",
                        romaji: "sukuranburu sukuea e wa dou ikeba ii desu ka?",
                        chinese: "请问去 Scramble Square 展望大厦怎么走？",
                        pitchAccent: "① 头高型",
                        situationNote: "问询具体高楼与购物中心路线。",
                        audioKey: "すみません"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "旅行者", japanese: "すみません、ハチ公の像はどこにありますか？", furigana: "すみません、はちこうの ぞうは どこに ありますか？", chinese: "不好意思，请问八公铜像在哪里？", isUser: true),
                    GenerativeDialogueTurn(speaker: "路人", speakerRole: "渋谷の若者", japanese: "あそこの緑の電車の向かい側ですよ！", furigana: "あそこの みどりの でんしゃの むかいがわですよ！", chinese: "就在那边绿色退役电车的对面哦！", isUser: false),
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "旅行者", japanese: "ありがとうございます！助かりました。", furigana: "ありがとうございます！たすかりました。", chinese: "太感谢了！帮大忙了。", isUser: true)
                ],
                culturalTips: [
                    "穿过涩谷十字路口绿灯仅有约 45 秒，拍照时切勿驻足阻挡人流涌动。",
                    "在涩谷站内请紧跟头顶绿色「ハチ公改札」黄色指示牌，不要随意出站以免走冤枉路。"
                ],
                challengeMission: "成功在八公像前找到路人请其拍一张照片并表达感谢！"
            )

        case "akiba":
            return TokyoDestinationPlan(
                id: "akiba",
                destinationName: "秋叶原动漫与限定手办",
                destinationJa: "秋葉原アニメ街・フィギュア探訪",
                district: "秋叶原・Akihabara",
                categoryIcon: "sparkles.tv.fill",
                tag: "动漫淘货与盲盒",
                overview: "二次元与电气街圣地。掌握向店员询问限定特典、手办盲盒陈列柜及开箱验货的地道短语。",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "これの在庫はまだありますか？",
                        furigana: "これの ざいこは まだ ありますか？",
                        romaji: "kore no zaiko wa mada arimasu ka?",
                        chinese: "请问这个还有库存现货吗？",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "看到展柜心仪手办时确认是否有全新现货。",
                        audioKey: "あります"
                    ),
                    GenerativePhrase(
                        japanese: "限定特典は付きますか？",
                        furigana: "げんてい とくてんは つきますか？",
                        romaji: "gentei tokuten wa tsukimasu ka?",
                        chinese: "请问附送限定版购买特典吗？",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "购买原著漫画、CD或同人志时确认赠品。",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "箱を開けて中を確認してもいいですか？",
                        furigana: "はこを あけて なかを かくにんしても いいですか？",
                        romaji: "hako o akete naka o kakunin shitemo ii desu ka?",
                        chinese: "请问可以开盒确认手办状态吗？",
                        pitchAccent: "① 头高型",
                        situationNote: "中古二手店（如 Surugaya）购买二手手办时的验货许可。",
                        audioKey: "いいですよ"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "二次元粉丝", japanese: "すみません、このフィギュアの未開封品はありますか？", furigana: "すみません、この ふぃぎゅあの みかいふうひんは ありますか？", chinese: "不好意思，请问这款手办有未拆封的全新现货吗？", isUser: true),
                    GenerativeDialogueTurn(speaker: "店员", speakerRole: "アニメ店員", japanese: "少々お待ちください……はい、ラスト1点ございます！", furigana: "しょうしょう おまちください……はい、らすと いってん ございます！", chinese: "请稍等片刻……有的，正好剩最后一件！", isUser: false),
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "二次元粉丝", japanese: "よかった！これをお願いします。", furigana: "よかった！これを おねがいします。", chinese: "太好了！请帮我打包这件。", isUser: true)
                ],
                culturalTips: [
                    "秋叶原许多手办展示柜（Rental Box）为个人寄卖，标有「現状渡し」即不支持退换。",
                    "免税购物满 5000 日元（不含税）需在结账时主动出示护照。"
                ],
                challengeMission: "向秋叶原店员问出「ラスト1点（最后一件）」并完成免税结账！"
            )

        case "shinjuku":
            return TokyoDestinationPlan(
                id: "shinjuku",
                destinationName: "新宿思出横丁居酒屋",
                destinationJa: "新宿思い出横丁・昭和風情",
                district: "新宿・Shinjuku",
                categoryIcon: "wineglass.fill",
                tag: "烧鸟与日式干杯",
                overview: "新宿西口最具昭和复古气息的烧鸟一条街。掌握入座第一杯酒、烤串盐酱选择及Otoshi文化。",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "とりあえず生ビール二つ！",
                        furigana: "とりあえず なまびーる ふたつ！",
                        romaji: "toriaezu nama biiru futatsu!",
                        chinese: "先来两杯生啤！",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "居酒屋坐定后必须最先点的第一轮酒水。",
                        audioKey: "乾杯"
                    ),
                    GenerativePhrase(
                        japanese: "焼き鳥盛り合わせを塩でお願いします。",
                        furigana: "やきとり もりあわせを しおで おねがいします。",
                        romaji: "yakitori moriawase o shio de onegaishimasu.",
                        chinese: "烤鸡肉串拼盘，请帮我做盐烤口味。",
                        pitchAccent: "③ 尾高型",
                        situationNote: "不知道点单种时直接来拼盘，盐烤（塩）最考验食材原味。",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "お会計をお願いします。",
                        furigana: "おかいけいを おねがいします。",
                        romaji: "okaikei o onegaishimasu.",
                        chinese: "请结账买单。",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "用餐完毕在座位上举手向服务员示意结账。",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "店员", speakerRole: "居酒屋マスター", japanese: "いらっしゃい！お飲み物は何にしますか？", furigana: "いらっしゃい！おのみものは なにに しますか？", chinese: "欢迎！喝点什么酒水呢？", isUser: false),
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "客人", japanese: "とりあえず生中と、レモンサワーをください！", furigana: "とりあえず なまちゅうと、れもんさわーを ください！", chinese: "先来一杯中杯生啤，和一杯柠檬沙瓦！", isUser: true),
                    GenerativeDialogueTurn(speaker: "店员", speakerRole: "居酒屋マスター", japanese: "あいよ！すぐにお持ちします！", furigana: "あいよ！すぐに おもちします！", chinese: "好嘞！马上为您送上！", isUser: false)
                ],
                culturalTips: [
                    "日本居酒屋入座后会端上一小碟开胃菜（お通し / Otoshi），属于标准座位费制度（约300~500日元）。",
                    "桌上碰杯时，地位较低或晚辈可将杯沿稍低于对方杯沿以示敬意。"
                ],
                challengeMission: "在居酒屋不用看菜单，流畅喊出「とりあえず生中！」并与同伴干杯！"
            )

        default:
            return TokyoDestinationPlan(
                id: presetId,
                destinationName: "浅草寺雷门与仲见世商店街",
                destinationJa: "浅草寺・雷門・下町散策",
                district: "台东・Asakusa",
                categoryIcon: "building.columns.fill",
                tag: "寺庙参拜与下町小吃",
                overview: "东京最古老寺庙。掌握求签（おみくじ）、参拜投五日元硬币祈福以及在老铺点人形烧的规矩。",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "おみくじはどこで引けますか？",
                        furigana: "おみくじは どこで ひけますか？",
                        romaji: "omikuji wa doko de hikemasu ka?",
                        chinese: "请问在哪里可以抽御神签？",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "在浅草寺本堂前寻找 100 日元自主投币抽签处。",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "焼きたての人形焼をひとつください。",
                        furigana: "やきたての にんぎょうやきを ひとつ ください。",
                        romaji: "yakitate no ningyouyaki o hitotsu kudasai.",
                        chinese: "请给我一个刚出炉的热腾腾人形烧。",
                        pitchAccent: "⓪ 平板型",
                        situationNote: "仲见世商店街边走边买传统下町点心。",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "このお守りのご利益は何ですか？",
                        furigana: "この おまもりの ごりやくは なんですか？",
                        romaji: "kono omamori no goriyaku wa nan desu ka?",
                        chinese: "请问这个御守保佑的是什么愿望？",
                        pitchAccent: "② 中高型",
                        situationNote: "购买健康、学业或恋爱御守时的询问表达。",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "参拜者", japanese: "すみません、お参りの作法を教えていただけますか？", furigana: "すみません、おまいりの さほうを おしえて いただけますか？", chinese: "不好意思，可以教我一下参拜的正确礼仪吗？", isUser: true),
                    GenerativeDialogueTurn(speaker: "僧侣", speakerRole: "寺院スタッフ", japanese: "お賽銭を入れて、静かに手を合わせて一礼してください。", furigana: "おさいせんを いれて、しずかに てを あわせて いちれい してください。", chinese: "投入香油钱后，静静双手合十并鞠一躬即可。", isUser: false),
                    GenerativeDialogueTurn(speaker: "你", speakerRole: "参拜者", japanese: "わかりました。ありがとうございます。", furigana: "わかりました。ありがとうございます。", chinese: "明白了，非常感谢！", isUser: true)
                ],
                culturalTips: [
                    "日本寺庙（如浅草寺）参拜为「合掌一礼」，不同于神社的「二礼二拍手一礼」（切勿在寺庙拍手）。",
                    "抽到「凶」签不要带走，应系在寺内专用的挂签架上化解厄运。"
                ],
                challengeMission: "投入 5 日元（代表「ご縁 有缘」）完成一次庄严的浅草寺祈福！"
            )
        }
    }
}
