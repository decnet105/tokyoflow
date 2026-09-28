import Foundation

public enum KanaCategory: String, CaseIterable, Identifiable {
    case seion = "Seion (清音 46)"
    case dakuon = "Dakuon (浊音/半浊音 25)"
    case yoon = "Yoon (拗音 33)"

    public var id: String { rawValue }
}

public struct KanaItem: Identifiable, Hashable, Codable {
    public let id: String
    public let hiragana: String
    public let katakana: String
    public let romaji: String
    public let row: String
    public let column: String
    public let exampleWordJa: String
    public let exampleWordRomaji: String
    public let exampleWordEn: String
    public let mnemonic: String

    public init(
        id: String,
        hiragana: String,
        katakana: String,
        romaji: String,
        row: String,
        column: String,
        exampleWordJa: String,
        exampleWordRomaji: String,
        exampleWordEn: String,
        mnemonic: String
    ) {
        self.id = id
        self.hiragana = hiragana
        self.katakana = katakana
        self.romaji = romaji
        self.row = row
        self.column = column
        self.exampleWordJa = exampleWordJa
        self.exampleWordRomaji = exampleWordRomaji
        self.exampleWordEn = exampleWordEn
        self.mnemonic = mnemonic
    }
}

public struct KanaDataManager {
    public static let shared = KanaDataManager()

    public let seionList: [KanaItem] = [
        // A-row (あ行)
        KanaItem(id: "a", hiragana: "あ", katakana: "ア", romaji: "a", row: "あ行", column: "a", exampleWordJa: "ありがとう", exampleWordRomaji: "arigatou", exampleWordEn: "Thank you (谢谢)", mnemonic: "Looks like an Apple with a stem"),
        KanaItem(id: "i", hiragana: "い", katakana: "イ", romaji: "i", row: "あ行", column: "i", exampleWordJa: "いぬ (犬)", exampleWordRomaji: "inu", exampleWordEn: "Dog (小狗)", mnemonic: "Two needles standing upright"),
        KanaItem(id: "u", hiragana: "う", katakana: "ウ", romaji: "u", row: "あ行", column: "u", exampleWordJa: "うどん", exampleWordRomaji: "udon", exampleWordEn: "Udon noodles (乌冬面)", mnemonic: "A person bent over diving"),
        KanaItem(id: "e", hiragana: "え", katakana: "エ", romaji: "e", row: "あ行", column: "e", exampleWordJa: "えき (駅)", exampleWordRomaji: "eki", exampleWordEn: "Train Station (车站)", mnemonic: "An energetic running person"),
        KanaItem(id: "o", hiragana: "お", katakana: "オ", romaji: "o", row: "あ行", column: "o", exampleWordJa: "おにぎり", exampleWordRomaji: "onigiri", exampleWordEn: "Rice ball (饭团)", mnemonic: "An origami shape"),

        // Ka-row (か行)
        KanaItem(id: "ka", hiragana: "か", katakana: "カ", romaji: "ka", row: "か行", column: "a", exampleWordJa: "かわいい", exampleWordRomaji: "kawaii", exampleWordEn: "Cute (可爱)", mnemonic: "A person cutting a piece of wood"),
        KanaItem(id: "ki", hiragana: "き", katakana: "キ", romaji: "ki", row: "か行", column: "i", exampleWordJa: "きっぷ (切符)", exampleWordRomaji: "kippu", exampleWordEn: "Train Ticket (车票)", mnemonic: "A golden key with two teeth"),
        KanaItem(id: "ku", hiragana: "く", katakana: "ク", romaji: "ku", row: "か行", column: "u", exampleWordJa: "くるま (車)", exampleWordRomaji: "kuruma", exampleWordEn: "Car (汽车)", mnemonic: "A bird's open beak cuckooing"),
        KanaItem(id: "ke", hiragana: "け", katakana: "ケ", romaji: "ke", row: "か行", column: "e", exampleWordJa: "けいたい (携帯)", exampleWordRomaji: "keitai", exampleWordEn: "Cell phone (手机)", mnemonic: "A shape of a wooden beer keg"),
        KanaItem(id: "ko", hiragana: "こ", katakana: "コ", romaji: "ko", row: "か行", column: "o", exampleWordJa: "コンビニ", exampleWordRomaji: "konbini", exampleWordEn: "Convenience store (便利店)", mnemonic: "Two koi fish swimming together"),

        // Sa-row (さ行)
        KanaItem(id: "sa", hiragana: "さ", katakana: "サ", romaji: "sa", row: "さ行", column: "a", exampleWordJa: "さくら (桜)", exampleWordRomaji: "sakura", exampleWordEn: "Cherry blossom (樱花)", mnemonic: "A signpost smiling"),
        KanaItem(id: "shi", hiragana: "し", katakana: "シ", romaji: "shi", row: "さ行", column: "i", exampleWordJa: "しんじゅく (新宿)", exampleWordRomaji: "shinjuku", exampleWordEn: "Shinjuku (新宿)", mnemonic: "A fish hook dipping into water"),
        KanaItem(id: "su", hiragana: "す", katakana: "ス", romaji: "su", row: "さ行", column: "u", exampleWordJa: "すいか (Suica)", exampleWordRomaji: "suika", exampleWordEn: "Suica IC Card / Watermelon (西瓜卡)", mnemonic: "A straw swirling in soup"),
        KanaItem(id: "se", hiragana: "せ", katakana: "セ", romaji: "se", row: "さ行", column: "e", exampleWordJa: "せんせい (先生)", exampleWordRomaji: "sensei", exampleWordEn: "Teacher (老师)", mnemonic: "A person resting on seven stones"),
        KanaItem(id: "so", hiragana: "そ", katakana: "ソ", romaji: "so", row: "さ行", column: "o", exampleWordJa: "そば", exampleWordRomaji: "soba", exampleWordEn: "Soba noodles (荞麦面)", mnemonic: "A zig-zag stitching sewing needle"),

        // Ta-row (た行)
        KanaItem(id: "ta", hiragana: "た", katakana: "タ", romaji: "ta", row: "た行", column: "a", exampleWordJa: "たこやき", exampleWordRomaji: "takoyaki", exampleWordEn: "Takoyaki (章鱼烧)", mnemonic: "Spells out the letters 'ta'"),
        KanaItem(id: "chi", hiragana: "ち", katakana: "チ", romaji: "chi", row: "た行", column: "i", exampleWordJa: "ちかてつ (地下鉄)", exampleWordRomaji: "chikatetsu", exampleWordEn: "Subway (地下铁)", mnemonic: "A cheerleader cheering with pom-poms"),
        KanaItem(id: "tsu", hiragana: "つ", katakana: "ツ", romaji: "tsu", row: "た行", column: "u", exampleWordJa: "つき (月)", exampleWordRomaji: "tsuki", exampleWordEn: "Moon (月亮)", mnemonic: "A giant ocean tsunami wave"),
        KanaItem(id: "te", hiragana: "て", katakana: "テ", romaji: "te", row: "た行", column: "e", exampleWordJa: "てんぷら", exampleWordRomaji: "tenpura", exampleWordEn: "Tempura (天妇罗)", mnemonic: "A tennis racket handle"),
        KanaItem(id: "to", hiragana: "と", katakana: "ト", romaji: "to", row: "た行", column: "o", exampleWordJa: "とうきょう (東京)", exampleWordRomaji: "toukyou", exampleWordEn: "Tokyo (东京)", mnemonic: "A thorn sticking into a toe"),

        // Na-row (な行)
        KanaItem(id: "na", hiragana: "な", katakana: "ナ", romaji: "na", row: "な行", column: "a", exampleWordJa: "なつ (夏)", exampleWordRomaji: "natsu", exampleWordEn: "Summer (夏天)", mnemonic: "A nun praying before a cross"),
        KanaItem(id: "ni", hiragana: "に", katakana: "ニ", romaji: "ni", row: "な行", column: "i", exampleWordJa: "にほん (日本)", exampleWordRomaji: "nihon", exampleWordEn: "Japan (日本)", mnemonic: "A needle sewing two threads"),
        KanaItem(id: "nu", hiragana: "ぬ", katakana: "ヌ", romaji: "nu", row: "な行", column: "u", exampleWordJa: "ぬいぐるみ", exampleWordRomaji: "nuigurumi", exampleWordEn: "Plush doll (玩偶/毛绒玩具)", mnemonic: "Noodles with chopsticks"),
        KanaItem(id: "ne", hiragana: "ね", katakana: "ネ", romaji: "ne", row: "な行", column: "e", exampleWordJa: "ねこ (猫)", exampleWordRomaji: "neko", exampleWordEn: "Cat (猫咪)", mnemonic: "A cat curled with a looped tail"),
        KanaItem(id: "no", hiragana: "の", katakana: "ノ", romaji: "no", row: "な行", column: "o", exampleWordJa: "のみもの (飲み物)", exampleWordRomaji: "nomimono", exampleWordEn: "Beverage (饮料)", mnemonic: "A forbidden 'No' sign circle"),

        // Ha-row (は行)
        KanaItem(id: "ha", hiragana: "は", katakana: "ハ", romaji: "ha", row: "は行", column: "a", exampleWordJa: "はなび (花火)", exampleWordRomaji: "hanabi", exampleWordEn: "Fireworks (烟花)", mnemonic: "A person wearing a graduation hat"),
        KanaItem(id: "hi", hiragana: "ひ", katakana: "ヒ", romaji: "hi", row: "は行", column: "i", exampleWordJa: "ひかり (光)", exampleWordRomaji: "hikari", exampleWordEn: "Shinkansen / Light (光/光芒)", mnemonic: "He has a big smiling chin"),
        KanaItem(id: "fu", hiragana: "ふ", katakana: "フ", romaji: "fu", row: "は行", column: "u", exampleWordJa: "ふじさん (富士山)", exampleWordRomaji: "fujisan", exampleWordEn: "Mt. Fuji (富士山)", mnemonic: "Mount Fuji with slopes"),
        KanaItem(id: "he", hiragana: "へ", katakana: "ヘ", romaji: "he", row: "は行", column: "e", exampleWordJa: "へや (部屋)", exampleWordRomaji: "heya", exampleWordEn: "Room (房间)", mnemonic: "Pointing up to heaven hill"),
        KanaItem(id: "ho", hiragana: "ほ", katakana: "ホ", romaji: "ho", row: "は行", column: "o", exampleWordJa: "ほん (本)", exampleWordRomaji: "hon", exampleWordEn: "Book (书本)", mnemonic: "A horse wearing a party hat"),

        // Ma-row (ま行)
        KanaItem(id: "ma", hiragana: "ま", katakana: "マ", romaji: "ma", row: "ま行", column: "a", exampleWordJa: "まんが (漫画)", exampleWordRomaji: "manga", exampleWordEn: "Manga (漫画)", mnemonic: "A magical masquerade mask"),
        KanaItem(id: "mi", hiragana: "み", katakana: "ミ", romaji: "mi", row: "ま行", column: "i", exampleWordJa: "みず (水)", exampleWordRomaji: "mizu", exampleWordEn: "Water (水/凉水)", mnemonic: "Looks like the number 21 musical note"),
        KanaItem(id: "mu", hiragana: "む", katakana: "ム", romaji: "mu", row: "ま行", column: "u", exampleWordJa: "むりょう (無料)", exampleWordRomaji: "muryou", exampleWordEn: "Free of charge (免费)", mnemonic: "A smiling cow going moo"),
        KanaItem(id: "me", hiragana: "め", katakana: "メ", romaji: "me", row: "ま行", column: "e", exampleWordJa: "めがね (眼鏡)", exampleWordRomaji: "megane", exampleWordEn: "Glasses (眼镜)", mnemonic: "An almond eye shape"),
        KanaItem(id: "mo", hiragana: "も", katakana: "モ", romaji: "mo", row: "ま行", column: "o", exampleWordJa: "もういちど", exampleWordRomaji: "mou ichido", exampleWordEn: "Once more (请再说一遍)", mnemonic: "A fish hook catching more worms"),

        // Ya-row (や行)
        KanaItem(id: "ya", hiragana: "や", katakana: "ヤ", romaji: "ya", row: "や行", column: "a", exampleWordJa: "やま (山)", exampleWordRomaji: "yama", exampleWordEn: "Mountain (山)", mnemonic: "A yak head with horns"),
        KanaItem(id: "yu", hiragana: "ゆ", katakana: "ユ", romaji: "yu", row: "や行", column: "u", exampleWordJa: "ゆめ (夢)", exampleWordRomaji: "yume", exampleWordEn: "Dream (梦想)", mnemonic: "A goldfish swimming in a tub"),
        KanaItem(id: "yo", hiragana: "よ", katakana: "ヨ", romaji: "yo", row: "や行", column: "o", exampleWordJa: "よる (夜)", exampleWordRomaji: "yoru", exampleWordEn: "Night (夜晚)", mnemonic: "A yo-yo dangling from a string"),

        // Ra-row (ら行)
        KanaItem(id: "ra", hiragana: "ら", katakana: "ラ", romaji: "ra", row: "ら行", column: "a", exampleWordJa: "ラーメン", exampleWordRomaji: "raamen", exampleWordEn: "Ramen (拉面)", mnemonic: "A rabbit sitting upright"),
        KanaItem(id: "ri", hiragana: "り", katakana: "リ", romaji: "ri", row: "ら行", column: "i", exampleWordJa: "りんご (林檎)", exampleWordRomaji: "ringo", exampleWordEn: "Apple (苹果)", mnemonic: "Two reeds swaying in river"),
        KanaItem(id: "ru", hiragana: "る", katakana: "ル", romaji: "ru", row: "ら行", column: "u", exampleWordJa: "るすばん (留守番)", exampleWordRomaji: "rusuban", exampleWordEn: "Looking after house (看家)", mnemonic: "A kangaroo with a looped pouch"),
        KanaItem(id: "re", hiragana: "れ", katakana: "レ", romaji: "re", row: "ら行", column: "e", exampleWordJa: "れっしゃ (列車)", exampleWordRomaji: "ressha", exampleWordEn: "Train (列车)", mnemonic: "A person resting against a wall"),
        KanaItem(id: "ro", hiragana: "ろ", katakana: "ロ", romaji: "ro", row: "ら行", column: "o", exampleWordJa: "ろうそく", exampleWordRomaji: "rousoku", exampleWordEn: "Candle (蜡烛)", mnemonic: "A road looping without a knot"),

        // Wa-row & N (わ行・ん)
        KanaItem(id: "wa", hiragana: "わ", katakana: "ワ", romaji: "wa", row: "わ行", column: "a", exampleWordJa: "わさび", exampleWordRomaji: "wasabi", exampleWordEn: "Wasabi (山葵/芥末)", mnemonic: "A graceful swan"),
        KanaItem(id: "wo", hiragana: "を", katakana: "ヲ", romaji: "wo", row: "わ行", column: "o", exampleWordJa: "〜をください", exampleWordRomaji: "o kudasai", exampleWordEn: "Object Particle (请给我...)", mnemonic: "A person leaping over a hurdle"),
        KanaItem(id: "n", hiragana: "ん", katakana: "ン", romaji: "n", row: "わ行", column: "n", exampleWordJa: "にほん (日本)", exampleWordRomaji: "nihon", exampleWordEn: "Nasal N sound (鼻音n)", mnemonic: "Looks like lowercase letter 'n'")
    ]

    public let dakuonList: [KanaItem] = [
        // Ga-row (が行)
        KanaItem(id: "ga", hiragana: "が", katakana: "ガ", romaji: "ga", row: "が行", column: "a", exampleWordJa: "がっこう (学校)", exampleWordRomaji: "gakkou", exampleWordEn: "School (学校)", mnemonic: "Voiced か"),
        KanaItem(id: "gi", hiragana: "ぎ", katakana: "ギ", romaji: "gi", row: "が行", column: "i", exampleWordJa: "ぎゅうどん (牛丼)", exampleWordRomaji: "gyuudon", exampleWordEn: "Beef bowl (牛肉饭)", mnemonic: "Voiced き"),
        KanaItem(id: "gu", hiragana: "ぐ", katakana: "グ", romaji: "gu", row: "が行", column: "u", exampleWordJa: "ぐんま (群馬)", exampleWordRomaji: "gunma", exampleWordEn: "Gunma (群马)", mnemonic: "Voiced く"),
        KanaItem(id: "ge", hiragana: "げ", katakana: "ゲ", romaji: "ge", row: "が行", column: "e", exampleWordJa: "げんき (元気)", exampleWordRomaji: "genki", exampleWordEn: "Energetic / Healthy (有精神)", mnemonic: "Voiced け"),
        KanaItem(id: "go", hiragana: "ご", katakana: "ゴ", romaji: "go", row: "が行", column: "o", exampleWordJa: "ごはん (ご飯)", exampleWordRomaji: "gohan", exampleWordEn: "Rice / Meal (米饭/饭)", mnemonic: "Voiced こ"),

        // Za-row (ざ行)
        KanaItem(id: "za", hiragana: "ざ", katakana: "ザ", romaji: "za", row: "ざ行", column: "a", exampleWordJa: "ざっし (雑誌)", exampleWordRomaji: "zasshi", exampleWordEn: "Magazine (杂志)", mnemonic: "Voiced さ"),
        KanaItem(id: "ji", hiragana: "じ", katakana: "ジ", romaji: "ji", row: "ざ行", column: "i", exampleWordJa: "じかん (時間)", exampleWordRomaji: "jikan", exampleWordEn: "Time (时间)", mnemonic: "Voiced し"),
        KanaItem(id: "zu", hiragana: "ず", katakana: "ズ", romaji: "zu", row: "ざ行", column: "u", exampleWordJa: "ずっと", exampleWordRomaji: "zutto", exampleWordEn: "Always / Far (一直/非常)", mnemonic: "Voiced す"),
        KanaItem(id: "ze", hiragana: "ぜ", katakana: "ゼ", romaji: "ze", row: "ざ行", column: "e", exampleWordJa: "ぜんぶ (全部)", exampleWordRomaji: "zenbu", exampleWordEn: "All / Everything (全部)", mnemonic: "Voiced せ"),
        KanaItem(id: "zo", hiragana: "ぞ", katakana: "ゾ", romaji: "zo", row: "ざ行", column: "o", exampleWordJa: "ぞう (象)", exampleWordRomaji: "zou", exampleWordEn: "Elephant (大象)", mnemonic: "Voiced そ"),

        // Da-row (だ行)
        KanaItem(id: "da", hiragana: "だ", katakana: "ダ", romaji: "da", row: "だ行", column: "a", exampleWordJa: "だいじょうぶ (大丈夫)", exampleWordRomaji: "daijoubu", exampleWordEn: "All right / OK (没问题)", mnemonic: "Voiced た"),
        KanaItem(id: "de", hiragana: "で", katakana: "デ", romaji: "de", row: "だ行", column: "e", exampleWordJa: "でんしゃ (電車)", exampleWordRomaji: "densha", exampleWordEn: "Electric train (电车)", mnemonic: "Voiced て"),
        KanaItem(id: "do", hiragana: "ど", katakana: "ド", romaji: "do", row: "だ行", column: "o", exampleWordJa: "どこ (何処)", exampleWordRomaji: "doko", exampleWordEn: "Where (哪里)", mnemonic: "Voiced と"),

        // Ba-row (ば行)
        KanaItem(id: "ba", hiragana: "ば", katakana: "バ", romaji: "ba", row: "ば行", column: "a", exampleWordJa: "ばしょ (場所)", exampleWordRomaji: "basho", exampleWordEn: "Place / Location (场所)", mnemonic: "Voiced は"),
        KanaItem(id: "bi", hiragana: "び", katakana: "ビ", romaji: "bi", row: "ば行", column: "i", exampleWordJa: "ビール", exampleWordRomaji: "biiru", exampleWordEn: "Beer (啤酒)", mnemonic: "Voiced ひ"),
        KanaItem(id: "bu", hiragana: "ぶ", katakana: "ブ", romaji: "bu", row: "ば行", column: "u", exampleWordJa: "ぶんか (文化)", exampleWordRomaji: "bunka", exampleWordEn: "Culture (文化)", mnemonic: "Voiced ふ"),
        KanaItem(id: "be", hiragana: "べ", katakana: "ベ", romaji: "be", row: "ば行", column: "e", exampleWordJa: "べんり (便利)", exampleWordRomaji: "benri", exampleWordEn: "Convenient (方便)", mnemonic: "Voiced へ"),
        KanaItem(id: "bo", hiragana: "ぼ", katakana: "ボ", romaji: "bo", row: "ば行", column: "o", exampleWordJa: "ぼく (僕)", exampleWordRomaji: "boku", exampleWordEn: "I / Me (我)", mnemonic: "Voiced ほ"),

        // Pa-row (ぱ行)
        KanaItem(id: "pa", hiragana: "ぱ", katakana: "パ", romaji: "pa", row: "ぱ行", column: "a", exampleWordJa: "パン", exampleWordRomaji: "pan", exampleWordEn: "Bread (面包)", mnemonic: "Plosive は"),
        KanaItem(id: "pi", hiragana: "ぴ", katakana: "ピ", romaji: "pi", row: "ぱ行", column: "i", exampleWordJa: "ピンク", exampleWordRomaji: "pinku", exampleWordEn: "Pink (粉色)", mnemonic: "Plosive ひ"),
        KanaItem(id: "pu", hiragana: "ぷ", katakana: "プ", romaji: "pu", row: "ぱ行", column: "u", exampleWordJa: "プリン", exampleWordRomaji: "purin", exampleWordEn: "Pudding (布丁)", mnemonic: "Plosive ふ"),
        KanaItem(id: "pe", hiragana: "ぺ", katakana: "ペ", romaji: "pe", row: "ぱ行", column: "e", exampleWordJa: "ペン", exampleWordRomaji: "pen", exampleWordEn: "Pen (钢笔/笔)", mnemonic: "Plosive へ"),
        KanaItem(id: "po", hiragana: "ぽ", katakana: "ポ", romaji: "po", row: "ぱ行", column: "o", exampleWordJa: "ポスト", exampleWordRomaji: "posuto", exampleWordEn: "Postbox (邮筒)", mnemonic: "Plosive ほ")
    ]

    public let yoonList: [KanaItem] = [
        KanaItem(id: "kya", hiragana: "きゃ", katakana: "キャ", romaji: "kya", row: "きゃ行", column: "a", exampleWordJa: "きゃく (客)", exampleWordRomaji: "kyaku", exampleWordEn: "Customer / Guest (客人)", mnemonic: "き + ゃ"),
        KanaItem(id: "kyu", hiragana: "きゅ", katakana: "キュ", romaji: "kyu", row: "きゃ行", column: "u", exampleWordJa: "きゅうこう (急行)", exampleWordRomaji: "kyuukou", exampleWordEn: "Express train (急行列车)", mnemonic: "き + ゅ"),
        KanaItem(id: "kyo", hiragana: "きょ", katakana: "キョ", romaji: "kyo", row: "きゃ行", column: "o", exampleWordJa: "きょう (今日)", exampleWordRomaji: "kyou", exampleWordEn: "Today (今天)", mnemonic: "き + ょ"),

        KanaItem(id: "sha", hiragana: "しゃ", katakana: "シャ", romaji: "sha", row: "しゃ行", column: "a", exampleWordJa: "しゃしん (写真)", exampleWordRomaji: "shashin", exampleWordEn: "Photo (照片)", mnemonic: "し + ゃ"),
        KanaItem(id: "shu", hiragana: "しゅ", katakana: "シュ", romaji: "shu", row: "しゃ行", column: "u", exampleWordJa: "しゅうでん (終電)", exampleWordRomaji: "shuuden", exampleWordEn: "Last train (末班车)", mnemonic: "し + ゅ"),
        KanaItem(id: "sho", hiragana: "しょ", katakana: "ショ", romaji: "sho", row: "しゃ行", column: "o", exampleWordJa: "しょうひん (商品)", exampleWordRomaji: "shouhin", exampleWordEn: "Goods (商品)", mnemonic: "し + ょ"),

        KanaItem(id: "cha", hiragana: "ちゃ", katakana: "チャ", romaji: "cha", row: "ちゃ行", column: "a", exampleWordJa: "おちゃ (お茶)", exampleWordRomaji: "ocha", exampleWordEn: "Green tea (绿茶/茶)", mnemonic: "ち + ゃ"),
        KanaItem(id: "chu", hiragana: "ちゅ", katakana: "チュ", romaji: "chu", row: "ちゃ行", column: "u", exampleWordJa: "ちゅうもん (注文)", exampleWordRomaji: "chuumon", exampleWordEn: "Order (下单/点餐)", mnemonic: "ち + ゅ"),
        KanaItem(id: "cho", hiragana: "ちょ", katakana: "チョ", romaji: "cho", row: "ちゃ行", column: "o", exampleWordJa: "ちょっと", exampleWordRomaji: "chotto", exampleWordEn: "A little / Excuse me (稍等/稍微)", mnemonic: "ち + ょ"),

        KanaItem(id: "nya", hiragana: "にゃ", katakana: "ニャ", romaji: "nya", row: "にゃ行", column: "a", exampleWordJa: "にゃんこ", exampleWordRomaji: "nyanko", exampleWordEn: "Kitty cat (猫咪)", mnemonic: "に + ゃ"),
        KanaItem(id: "ryo", hiragana: "りょ", katakana: "リョ", romaji: "ryo", row: "りゃ行", column: "o", exampleWordJa: "りょうしゅうしょ (領収書)", exampleWordRomaji: "ryoushuusho", exampleWordEn: "Receipt (发票/收据)", mnemonic: "り + ょ")
    ]
}
