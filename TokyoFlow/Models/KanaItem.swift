import Foundation

public enum KanaCategory: String, CaseIterable, Identifiable {
    case seion = "Seion (清音 46)"
    case dakuon = "Dakuon (浊音/半浊音 25)"
    case yoon = "Yoon (拗音 33)"

    public var id: String { rawValue }
}

public struct KanaExampleWord: Identifiable, Hashable, Codable {
    public var id: String { japanese }
    public let japanese: String
    public let romaji: String
    public let english: String

    public init(japanese: String, romaji: String, english: String) {
        self.japanese = japanese
        self.romaji = romaji
        self.english = english
    }
}

public struct KanaItem: Identifiable, Hashable, Codable {
    public let id: String
    public let hiragana: String
    public let katakana: String
    public let romaji: String
    public let row: String
    public let column: String
    public let exampleWords: [KanaExampleWord]
    public let mnemonic: String

    public init(
        id: String,
        hiragana: String,
        katakana: String,
        romaji: String,
        row: String,
        column: String,
        exampleWords: [KanaExampleWord],
        mnemonic: String
    ) {
        self.id = id
        self.hiragana = hiragana
        self.katakana = katakana
        self.romaji = romaji
        self.row = row
        self.column = column
        self.exampleWords = exampleWords
        self.mnemonic = mnemonic
    }

    /// Returns the non-repeating daily example word for today (rotates each day of the week, no duplicates within 7 days)
    public var dailyExampleWord: KanaExampleWord {
        guard !exampleWords.isEmpty else {
            return KanaExampleWord(japanese: hiragana, romaji: romaji, english: "Japanese Kana")
        }
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let index = (dayOfYear - 1) % exampleWords.count
        return exampleWords[index]
    }

    /// Returns the example word for an offset day (e.g. 0 = today, 1 = tomorrow, -1 = yesterday)
    public func exampleWordForDay(dayOffset: Int) -> KanaExampleWord {
        guard !exampleWords.isEmpty else {
            return KanaExampleWord(japanese: hiragana, romaji: romaji, english: "Japanese Kana")
        }
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let targetIndex = ((dayOfYear - 1 + dayOffset) % exampleWords.count + exampleWords.count) % exampleWords.count
        return exampleWords[targetIndex]
    }

    // Backwards compatibility properties
    public var exampleWordJa: String {
        return dailyExampleWord.japanese
    }
    public var exampleWordRomaji: String {
        return dailyExampleWord.romaji
    }
    public var exampleWordEn: String {
        return dailyExampleWord.english
    }
}

public struct KanaDataManager {
    public static let shared = KanaDataManager()

    public let seionList: [KanaItem] = [
        KanaItem(
            id: "a",
            hiragana: "あ",
            katakana: "ア",
            romaji: "a",
            row: "あ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "ありがとう", romaji: "arigatou", english: "Thank you (谢谢/感谢)"),
                KanaExampleWord(japanese: "あさ (朝)", romaji: "asa", english: "Morning (早晨/清晨)"),
                KanaExampleWord(japanese: "あめ (雨)", romaji: "ame", english: "Rain / Candy (下雨/雨水)"),
                KanaExampleWord(japanese: "あき (秋)", romaji: "aki", english: "Autumn (秋天/秋季)"),
                KanaExampleWord(japanese: "あたま (頭)", romaji: "atama", english: "Head (头部/脑筋)"),
                KanaExampleWord(japanese: "あか (赤)", romaji: "aka", english: "Red color (红色)"),
                KanaExampleWord(japanese: "あんない (案内)", romaji: "annai", english: "Guidance / Info (指引/向导)")
            ],
            mnemonic: "Looks like an Apple with a stem"
        ),

        KanaItem(
            id: "i",
            hiragana: "い",
            katakana: "イ",
            romaji: "i",
            row: "あ行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "いぬ (犬)", romaji: "inu", english: "Dog (小狗)"),
                KanaExampleWord(japanese: "いいえ", romaji: "iie", english: "No / You're welcome (不/不客气)"),
                KanaExampleWord(japanese: "いくら", romaji: "ikura", english: "How much (多少钱/鲑鱼子)"),
                KanaExampleWord(japanese: "いざかや (居酒屋)", romaji: "izakaya", english: "Izakaya Pub (居酒屋)"),
                KanaExampleWord(japanese: "いっしょに (一緒に)", romaji: "isshoni", english: "Together (一起)"),
                KanaExampleWord(japanese: "いま (今)", romaji: "ima", english: "Now / Right now (现在)"),
                KanaExampleWord(japanese: "いちばん (一番)", romaji: "ichiban", english: "Number one / Best (最/第一)")
            ],
            mnemonic: "Two needles standing upright"
        ),

        KanaItem(
            id: "u",
            hiragana: "う",
            katakana: "ウ",
            romaji: "u",
            row: "あ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "うどん", romaji: "udon", english: "Udon noodles (乌冬面)"),
                KanaExampleWord(japanese: "うみ (海)", romaji: "umi", english: "Sea / Ocean (大海)"),
                KanaExampleWord(japanese: "うしろ (後ろ)", romaji: "ushiro", english: "Behind / Back (后面)"),
                KanaExampleWord(japanese: "うえ (上)", romaji: "ue", english: "Above / Up (上面)"),
                KanaExampleWord(japanese: "うれしい (嬉しい)", romaji: "ureshii", english: "Happy / Glad (高兴/开心)"),
                KanaExampleWord(japanese: "うまい (旨い)", romaji: "umai", english: "Delicious / Good (美味/厉害)"),
                KanaExampleWord(japanese: "うけつけ (受付)", romaji: "uketsuke", english: "Reception desk (前台/接待处)")
            ],
            mnemonic: "A person bent over diving"
        ),

        KanaItem(
            id: "e",
            hiragana: "え",
            katakana: "エ",
            romaji: "e",
            row: "あ行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "えき (駅)", romaji: "eki", english: "Train Station (车站/电车站)"),
                KanaExampleWord(japanese: "えいが (映画)", romaji: "eiga", english: "Movie (电影)"),
                KanaExampleWord(japanese: "えのぐ (絵の具)", romaji: "enogu", english: "Paints / Color (颜料/水彩)"),
                KanaExampleWord(japanese: "えんぴつ (鉛筆)", romaji: "enpitsu", english: "Pencil (铅笔)"),
                KanaExampleWord(japanese: "えび (海老)", romaji: "ebi", english: "Shrimp / Prawn (虾)"),
                KanaExampleWord(japanese: "えがお (笑顔)", romaji: "egao", english: "Smiling face (笑脸/笑容)"),
                KanaExampleWord(japanese: "えきいん (駅員)", romaji: "ekiin", english: "Station attendant (车站工作人员)")
            ],
            mnemonic: "An energetic running person"
        ),

        KanaItem(
            id: "o",
            hiragana: "お",
            katakana: "オ",
            romaji: "o",
            row: "あ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "おにぎり", romaji: "onigiri", english: "Rice ball (饭团)"),
                KanaExampleWord(japanese: "おちゃ (お茶)", romaji: "ocha", english: "Green tea (绿茶/茶)"),
                KanaExampleWord(japanese: "おいしい (美味しい)", romaji: "oishii", english: "Delicious (好吃/美味)"),
                KanaExampleWord(japanese: "おねがい (お願い)", romaji: "onegai", english: "Please (拜托/请)"),
                KanaExampleWord(japanese: "おかいけい (お会計)", romaji: "okaikei", english: "Bill / Check (结账/买单)"),
                KanaExampleWord(japanese: "おと (音)", romaji: "oto", english: "Sound / Noise (声音)"),
                KanaExampleWord(japanese: "おみやげ (お土産)", romaji: "omiyage", english: "Souvenir / Gift (土特产/伴手礼)")
            ],
            mnemonic: "An origami shape"
        ),

        KanaItem(
            id: "ka",
            hiragana: "か",
            katakana: "カ",
            romaji: "ka",
            row: "か行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "かわいい", romaji: "kawaii", english: "Cute / Adorable (可爱)"),
                KanaExampleWord(japanese: "かさ (傘)", romaji: "kasa", english: "Umbrella (雨伞)"),
                KanaExampleWord(japanese: "かいさつ (改札)", romaji: "kaisatsu", english: "Ticket barrier (闸机/检票口)"),
                KanaExampleWord(japanese: "かばん (鞄)", romaji: "kaban", english: "Bag / Backpack (包/提包)"),
                KanaExampleWord(japanese: "からあげ (唐揚げ)", romaji: "karaage", english: "Fried chicken (日式炸鸡)"),
                KanaExampleWord(japanese: "カフェ", romaji: "kafe", english: "Cafe (咖啡馆)"),
                KanaExampleWord(japanese: "かんぱい (乾杯)", romaji: "kanpai", english: "Cheers! (干杯)")
            ],
            mnemonic: "A person cutting a piece of wood"
        ),

        KanaItem(
            id: "ki",
            hiragana: "き",
            katakana: "キ",
            romaji: "ki",
            row: "か行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "きっぷ (切符)", romaji: "kippu", english: "Train Ticket (车票)"),
                KanaExampleWord(japanese: "きっさてん (喫茶店)", romaji: "kissaten", english: "Classic Coffee shop (咖啡茶座)"),
                KanaExampleWord(japanese: "きょう (今日)", romaji: "kyou", english: "Today (今天)"),
                KanaExampleWord(japanese: "きのう (昨日)", romaji: "kinou", english: "Yesterday (昨天)"),
                KanaExampleWord(japanese: "きゅうこう (急行)", romaji: "kyuukou", english: "Express train (急行列车)"),
                KanaExampleWord(japanese: "きいろ (黄色)", romaji: "kiiro", english: "Yellow color (黄色)"),
                KanaExampleWord(japanese: "きもち (気持ち)", romaji: "kimochi", english: "Feeling / Mood (心情/感觉)")
            ],
            mnemonic: "A golden key with two teeth"
        ),

        KanaItem(
            id: "ku",
            hiragana: "く",
            katakana: "ク",
            romaji: "ku",
            row: "か行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "くるま (車)", romaji: "kuruma", english: "Car / Vehicle (汽车)"),
                KanaExampleWord(japanese: "くすり (薬)", romaji: "kusuri", english: "Medicine (药物/药品)"),
                KanaExampleWord(japanese: "くうこう (空港)", romaji: "kuukou", english: "Airport (机场)"),
                KanaExampleWord(japanese: "くだもの (果物)", romaji: "kudamono", english: "Fruit (水果)"),
                KanaExampleWord(japanese: "くつ (靴)", romaji: "kutsu", english: "Shoes (鞋子)"),
                KanaExampleWord(japanese: "くも (雲)", romaji: "kumo", english: "Cloud (云彩)"),
                KanaExampleWord(japanese: "クレジットカード", romaji: "kurejitto kaado", english: "Credit card (信用卡)")
            ],
            mnemonic: "A bird's open beak cuckooing"
        ),

        KanaItem(
            id: "ke",
            hiragana: "け",
            katakana: "ケ",
            romaji: "ke",
            row: "か行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "けいたい (携帯)", romaji: "keitai", english: "Mobile phone (手机)"),
                KanaExampleWord(japanese: "けしき (景色)", romaji: "keshiki", english: "Scenery / View (风景/景色)"),
                KanaExampleWord(japanese: "ケーキ", romaji: "keeki", english: "Cake (蛋糕)"),
                KanaExampleWord(japanese: "けっこん (結婚)", romaji: "kekkon", english: "Marriage (结婚)"),
                KanaExampleWord(japanese: "けっこう (結構)", romaji: "kekkou", english: "Fine / No thanks (挺好/不用了)"),
                KanaExampleWord(japanese: "けいさつ (警察)", romaji: "keisatsu", english: "Police (警察/交番)"),
                KanaExampleWord(japanese: "けむり (煙)", romaji: "kemuri", english: "Smoke (烟雾)")
            ],
            mnemonic: "A shape of a wooden beer keg"
        ),

        KanaItem(
            id: "ko",
            hiragana: "こ",
            katakana: "コ",
            romaji: "ko",
            row: "か行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "コンビニ", romaji: "konbini", english: "Convenience store (便利店)"),
                KanaExampleWord(japanese: "こうえん (公園)", romaji: "kouen", english: "Park (公园)"),
                KanaExampleWord(japanese: "コーヒー", romaji: "koohii", english: "Coffee (咖啡)"),
                KanaExampleWord(japanese: "こんばん (今晩)", romaji: "konban", english: "Tonight / This evening (今晚)"),
                KanaExampleWord(japanese: "ここ", romaji: "koko", english: "Here / This place (这里)"),
                KanaExampleWord(japanese: "こども (子供)", romaji: "kodomo", english: "Child / Kids (孩子)"),
                KanaExampleWord(japanese: "こころ (心)", romaji: "kokoro", english: "Heart / Mind (心灵/心情)")
            ],
            mnemonic: "Two koi fish swimming together"
        ),

        KanaItem(
            id: "sa",
            hiragana: "さ",
            katakana: "サ",
            romaji: "sa",
            row: "さ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "さくら (桜)", romaji: "sakura", english: "Cherry blossom (樱花)"),
                KanaExampleWord(japanese: "さかな (魚)", romaji: "sakana", english: "Fish (鱼/生鱼片)"),
                KanaExampleWord(japanese: "さいふ (財布)", romaji: "saifu", english: "Wallet (钱包)"),
                KanaExampleWord(japanese: "さようなら", romaji: "sayounara", english: "Goodbye (再见)"),
                KanaExampleWord(japanese: "さとう (砂糖)", romaji: "satou", english: "Sugar (白糖/砂糖)"),
                KanaExampleWord(japanese: "さんぽ (散歩)", romaji: "sanpo", english: "Stroll / Walk (散步)"),
                KanaExampleWord(japanese: "サービス", romaji: "saabisu", english: "Service / Free perk (服务/附赠)")
            ],
            mnemonic: "A signpost smiling"
        ),

        KanaItem(
            id: "shi",
            hiragana: "し",
            katakana: "シ",
            romaji: "shi",
            row: "さ行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "しんじゅく (新宿)", romaji: "shinjuku", english: "Shinjuku (新宿)"),
                KanaExampleWord(japanese: "しんかんせん (新幹線)", romaji: "shinkansen", english: "Bullet train (新干线)"),
                KanaExampleWord(japanese: "しぶや (渋谷)", romaji: "shibuya", english: "Shibuya (涩谷)"),
                KanaExampleWord(japanese: "しゃしん (写真)", romaji: "shashin", english: "Photo / Picture (照片)"),
                KanaExampleWord(japanese: "しゅうでん (終電)", romaji: "shuuden", english: "Last train of the night (末班车)"),
                KanaExampleWord(japanese: "しお (塩)", romaji: "shio", english: "Salt (食盐)"),
                KanaExampleWord(japanese: "しつれいします (失礼します)", romaji: "shitsurei shimasu", english: "Excuse me (打扰了/失礼了)")
            ],
            mnemonic: "A fish hook dipping into water"
        ),

        KanaItem(
            id: "su",
            hiragana: "す",
            katakana: "ス",
            romaji: "su",
            row: "さ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "すいか (Suica)", romaji: "suika", english: "Suica Card / Watermelon (西瓜卡/西瓜)"),
                KanaExampleWord(japanese: "すし (寿司)", romaji: "sushi", english: "Sushi (寿司)"),
                KanaExampleWord(japanese: "すみません", romaji: "sumimasen", english: "Excuse me / Sorry (不好意思/抱歉)"),
                KanaExampleWord(japanese: "スーパー", romaji: "suupaa", english: "Supermarket (超市)"),
                KanaExampleWord(japanese: "すき (好き)", romaji: "suki", english: "Like / Fond of (喜欢)"),
                KanaExampleWord(japanese: "すずしい (涼しい)", romaji: "suzushii", english: "Cool weather (凉爽)"),
                KanaExampleWord(japanese: "すこし (少し)", romaji: "sukoshi", english: "A little bit (稍微/一点)")
            ],
            mnemonic: "A straw swirling in soup"
        ),

        KanaItem(
            id: "se",
            hiragana: "せ",
            katakana: "セ",
            romaji: "se",
            row: "さ行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "せんせい (先生)", romaji: "sensei", english: "Teacher / Doctor (老师/前辈)"),
                KanaExampleWord(japanese: "せき (席)", romaji: "seki", english: "Seat / Table (座位)"),
                KanaExampleWord(japanese: "せんたく (洗濯)", romaji: "sentaku", english: "Laundry / Washing (洗衣服)"),
                KanaExampleWord(japanese: "せまい (狭い)", romaji: "semai", english: "Narrow / Cozy space (狭窄/小巧)"),
                KanaExampleWord(japanese: "せかい (世界)", romaji: "sekai", english: "World (世界)"),
                KanaExampleWord(japanese: "せつめい (説明)", romaji: "setsumei", english: "Explanation (说明/解释)"),
                KanaExampleWord(japanese: "セット (セット)", romaji: "setto", english: "Combo set / Meal set (套餐)")
            ],
            mnemonic: "A person resting on seven stones"
        ),

        KanaItem(
            id: "so",
            hiragana: "そ",
            katakana: "ソ",
            romaji: "so",
            row: "さ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "そば", romaji: "soba", english: "Soba noodles (荞麦面)"),
                KanaExampleWord(japanese: "そら (空)", romaji: "sora", english: "Sky (天空)"),
                KanaExampleWord(japanese: "そこ", romaji: "soko", english: "There / That place (那里)"),
                KanaExampleWord(japanese: "ソフトクリーム", romaji: "sofutokuriimu", english: "Soft serve ice cream (冰淇淋)"),
                KanaExampleWord(japanese: "そうですね", romaji: "sou desu ne", english: "I see / That's right (确实如此)"),
                KanaExampleWord(japanese: "そうじ (掃除)", romaji: "souji", english: "Cleaning (打扫/清洁)"),
                KanaExampleWord(japanese: "そと (外)", romaji: "soto", english: "Outside (外面/室外)")
            ],
            mnemonic: "A zig-zag stitching sewing needle"
        ),

        KanaItem(
            id: "ta",
            hiragana: "た",
            katakana: "タ",
            romaji: "ta",
            row: "た行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "たこやき", romaji: "takoyaki", english: "Takoyaki (章鱼小丸子)"),
                KanaExampleWord(japanese: "たべもの (食べ物)", romaji: "tabemono", english: "Food (食物)"),
                KanaExampleWord(japanese: "たいへん (大変)", romaji: "taihen", english: "Tough / Hard (辛苦/不容易)"),
                KanaExampleWord(japanese: "タクシー", romaji: "takushii", english: "Taxi (出租车)"),
                KanaExampleWord(japanese: "たのしい (楽しい)", romaji: "tanoshii", english: "Fun / Enjoyable (愉快/开心)"),
                KanaExampleWord(japanese: "たまご (卵)", romaji: "tamago", english: "Egg (鸡蛋)"),
                KanaExampleWord(japanese: "たかい (高い)", romaji: "takai", english: "High / Expensive (高/贵)")
            ],
            mnemonic: "Spells out the letters 'ta'"
        ),

        KanaItem(
            id: "chi",
            hiragana: "ち",
            katakana: "チ",
            romaji: "chi",
            row: "た行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "ちかてつ (地下鉄)", romaji: "chikatetsu", english: "Subway / Metro (地下铁)"),
                KanaExampleWord(japanese: "ちかい (近い)", romaji: "chikai", english: "Near / Close by (很近)"),
                KanaExampleWord(japanese: "チケット", romaji: "chiketto", english: "Ticket (入场券/票)"),
                KanaExampleWord(japanese: "ちず (地図)", romaji: "chizu", english: "Map (地图)"),
                KanaExampleWord(japanese: "ちゅうもん (注文)", romaji: "chuumon", english: "Order food (点单/点菜)"),
                KanaExampleWord(japanese: "ちょっと", romaji: "chotto", english: "A moment / A bit (稍等/稍微)"),
                KanaExampleWord(japanese: "ちから (力)", romaji: "chikara", english: "Strength / Power (力量)")
            ],
            mnemonic: "A cheerleader cheering with pom-poms"
        ),

        KanaItem(
            id: "tsu",
            hiragana: "つ",
            katakana: "ツ",
            romaji: "tsu",
            row: "た行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "つき (月)", romaji: "tsuki", english: "Moon / Month (月亮/月份)"),
                KanaExampleWord(japanese: "つくえ (机)", romaji: "tsukue", english: "Desk / Table (书桌)"),
                KanaExampleWord(japanese: "つぎ (次)", romaji: "tsugi", english: "Next (下一个/下一站)"),
                KanaExampleWord(japanese: "つめたい (冷たい)", romaji: "tsumetai", english: "Cold / Chilled drink (冰凉/冷)"),
                KanaExampleWord(japanese: "つかう (使う)", romaji: "tsukau", english: "To use (使用)"),
                KanaExampleWord(japanese: "つよい (強い)", romaji: "tsuyoi", english: "Strong (强劲/强烈)"),
                KanaExampleWord(japanese: "つうきん (通勤)", romaji: "tsuukin", english: "Commuting to work (通勤)")
            ],
            mnemonic: "A giant ocean tsunami wave"
        ),

        KanaItem(
            id: "te",
            hiragana: "て",
            katakana: "テ",
            romaji: "te",
            row: "た行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "てんぷら", romaji: "tenpura", english: "Tempura (天妇罗)"),
                KanaExampleWord(japanese: "てんき (天気)", romaji: "tenki", english: "Weather (天气)"),
                KanaExampleWord(japanese: "てがみ (手紙)", romaji: "tegami", english: "Letter (信件)"),
                KanaExampleWord(japanese: "テーブル", romaji: "teeburu", english: "Table (餐桌)"),
                KanaExampleWord(japanese: "てんいん (店員)", romaji: "ten'in", english: "Clerk / Store staff (店员)"),
                KanaExampleWord(japanese: "ていしょく (定食)", romaji: "teishoku", english: "Set meal (定食套餐)"),
                KanaExampleWord(japanese: "テレビ", romaji: "terebi", english: "Television (电视)")
            ],
            mnemonic: "A tennis racket handle"
        ),

        KanaItem(
            id: "to",
            hiragana: "と",
            katakana: "ト",
            romaji: "to",
            row: "た行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "とうきょう (東京)", romaji: "toukyou", english: "Tokyo (东京)"),
                KanaExampleWord(japanese: "ともだち (友達)", romaji: "tomodachi", english: "Friend (朋友)"),
                KanaExampleWord(japanese: "とりあえずにく", romaji: "toriaezu nama", english: "Beer for starters! (先来杯生啤！)"),
                KanaExampleWord(japanese: "トイレ", romaji: "toire", english: "Restroom (洗手间/厕所)"),
                KanaExampleWord(japanese: "となり (隣)", romaji: "tonari", english: "Next door / Beside (旁边/隔壁)"),
                KanaExampleWord(japanese: "とおり (通り)", romaji: "toori", english: "Street / Avenue (街道/马路)"),
                KanaExampleWord(japanese: "とけい (時計)", romaji: "tokei", english: "Clock / Watch (时钟/手表)")
            ],
            mnemonic: "A thorn sticking into a toe"
        ),

        KanaItem(
            id: "na",
            hiragana: "な",
            katakana: "ナ",
            romaji: "na",
            row: "な行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "なつ (夏)", romaji: "natsu", english: "Summer (夏天)"),
                KanaExampleWord(japanese: "なまえ (名前)", romaji: "namae", english: "Name (名字/姓名)"),
                KanaExampleWord(japanese: "なっとう (納豆)", romaji: "nattou", english: "Natto fermented beans (纳豆)"),
                KanaExampleWord(japanese: "なに (何)", romaji: "nani", english: "What? (什么)"),
                KanaExampleWord(japanese: "なか (中)", romaji: "naka", english: "Inside / Middle (里面/内部)"),
                KanaExampleWord(japanese: "ならぶ (並ぶ)", romaji: "narabu", english: "To line up / Queue (排队)"),
                KanaExampleWord(japanese: "なつかしい (懐かしい)", romaji: "natsukashii", english: "Nostalgic (令人怀念)")
            ],
            mnemonic: "A nun praying before a cross"
        ),

        KanaItem(
            id: "ni",
            hiragana: "に",
            katakana: "ニ",
            romaji: "ni",
            row: "な行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "にほん (日本)", romaji: "nihon", english: "Japan (日本)"),
                KanaExampleWord(japanese: "にく (肉)", romaji: "niku", english: "Meat (肉类)"),
                KanaExampleWord(japanese: "にちようび (日曜日)", romaji: "nichiyoubi", english: "Sunday (周日)"),
                KanaExampleWord(japanese: "にもつ (荷物)", romaji: "nimotsu", english: "Luggage / Package (行李/包裹)"),
                KanaExampleWord(japanese: "にぎやか (賑やか)", romaji: "nigiyaka", english: "Lively / Bustling (热闹/繁华)"),
                KanaExampleWord(japanese: "にんじん", romaji: "ninjin", english: "Carrot (胡萝卜)"),
                KanaExampleWord(japanese: "ニュース", romaji: "nyuusu", english: "News (新闻)")
            ],
            mnemonic: "A needle sewing two threads"
        ),

        KanaItem(
            id: "nu",
            hiragana: "ぬ",
            katakana: "ヌ",
            romaji: "nu",
            row: "な行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ぬいぐるみ", romaji: "nuigurumi", english: "Plush doll (玩偶/毛绒玩具)"),
                KanaExampleWord(japanese: "ぬるい (温い)", romaji: "nurui", english: "Lukewarm (温温的/不够烫)"),
                KanaExampleWord(japanese: "ぬぐ (脱ぐ)", romaji: "nugu", english: "To take off shoes/coat (脱鞋/脱衣服)"),
                KanaExampleWord(japanese: "ぬりえ (塗り絵)", romaji: "nurie", english: "Coloring book (涂色画)"),
                KanaExampleWord(japanese: "ぬま (沼)", romaji: "numa", english: "Pond / Obsession (沼泽/深陷爱好)"),
                KanaExampleWord(japanese: "ぬけみち (抜け道)", romaji: "nukemichi", english: "Shortcut alley (捷径/小道)"),
                KanaExampleWord(japanese: "ぬれたおる (濡れタオル)", romaji: "nure taoru", english: "Wet hand towel (湿毛巾)")
            ],
            mnemonic: "Noodles with chopsticks"
        ),

        KanaItem(
            id: "ne",
            hiragana: "ね",
            katakana: "ネ",
            romaji: "ne",
            row: "な行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "ねこ (猫)", romaji: "neko", english: "Cat (猫咪)"),
                KanaExampleWord(japanese: "ねつ (熱)", romaji: "netsu", english: "Fever / Heat (发烧/热情)"),
                KanaExampleWord(japanese: "ねだん (値段)", romaji: "nedan", english: "Price (价格/售价)"),
                KanaExampleWord(japanese: "ネット", romaji: "netto", english: "Internet (网络)"),
                KanaExampleWord(japanese: "ねる (寝る)", romaji: "neru", english: "To sleep / Go to bed (睡觉)"),
                KanaExampleWord(japanese: "ネギ", romaji: "negi", english: "Green onion (大葱)"),
                KanaExampleWord(japanese: "ねんまつ (年末)", romaji: "nenmatsu", english: "Year-end (年末/岁末)")
            ],
            mnemonic: "A cat curled with a looped tail"
        ),

        KanaItem(
            id: "no",
            hiragana: "の",
            katakana: "ノ",
            romaji: "no",
            row: "な行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "のみもの (飲み物)", romaji: "nomimono", english: "Beverage / Drink (饮料)"),
                KanaExampleWord(japanese: "のりかえ (乗り換え)", romaji: "norikae", english: "Train transfer (换乘/转车)"),
                KanaExampleWord(japanese: "のど (喉)", romaji: "nodo", english: "Throat (嗓子/喉咙)"),
                KanaExampleWord(japanese: "ノート", romaji: "nooto", english: "Notebook (笔记本)"),
                KanaExampleWord(japanese: "のる (乗る)", romaji: "noru", english: "To ride / Board train (乘坐/乘车)"),
                KanaExampleWord(japanese: "のり (海苔)", romaji: "nori", english: "Seaweed sheet (海苔)"),
                KanaExampleWord(japanese: "のんびり", romaji: "nonbiri", english: "Relaxed / Chill (悠闲/放松)")
            ],
            mnemonic: "A forbidden 'No' sign circle"
        ),

        KanaItem(
            id: "ha",
            hiragana: "は",
            katakana: "ハ",
            romaji: "ha",
            row: "は行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "はなび (花火)", romaji: "hanabi", english: "Fireworks (烟花/花火)"),
                KanaExampleWord(japanese: "はる (春)", romaji: "haru", english: "Spring (春天)"),
                KanaExampleWord(japanese: "はし (箸)", romaji: "hashi", english: "Chopsticks (筷子)"),
                KanaExampleWord(japanese: "はい", romaji: "hai", english: "Yes (是的/明白)"),
                KanaExampleWord(japanese: "はこ (箱)", romaji: "hako", english: "Box (盒子/箱子)"),
                KanaExampleWord(japanese: "はな (花)", romaji: "hana", english: "Flower (鲜花)"),
                KanaExampleWord(japanese: "はんぶん (半分)", romaji: "hanbun", english: "Half portion (一半)")
            ],
            mnemonic: "A person wearing a graduation hat"
        ),

        KanaItem(
            id: "hi",
            hiragana: "ひ",
            katakana: "ヒ",
            romaji: "hi",
            row: "は行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "ひかり (光)", romaji: "hikari", english: "Light / Shinkansen Hikari (光芒/光速)"),
                KanaExampleWord(japanese: "ひと (人)", romaji: "hito", english: "Person / People (人)"),
                KanaExampleWord(japanese: "ひるごはん (昼ご飯)", romaji: "hirugohan", english: "Lunch (午餐)"),
                KanaExampleWord(japanese: "ひだり (左)", romaji: "hidari", english: "Left side (左边)"),
                KanaExampleWord(japanese: "ひがし (東)", romaji: "higashi", english: "East (东面/东口)"),
                KanaExampleWord(japanese: "ひろい (広い)", romaji: "hiroi", english: "Spacious (宽敞)"),
                KanaExampleWord(japanese: "ひとつ (一つ)", romaji: "hitotsu", english: "One item (一个)")
            ],
            mnemonic: "He has a big smiling chin"
        ),

        KanaItem(
            id: "fu",
            hiragana: "ふ",
            katakana: "フ",
            romaji: "fu",
            row: "は行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ふじさん (富士山)", romaji: "fujisan", english: "Mt. Fuji (富士山)"),
                KanaExampleWord(japanese: "ふくろ (袋)", romaji: "fukuro", english: "Plastic / Paper bag (袋子/购物袋)"),
                KanaExampleWord(japanese: "ふゆ (冬)", romaji: "fuyu", english: "Winter (冬天)"),
                KanaExampleWord(japanese: "ふね (船)", romaji: "fune", english: "Boat / Ship (轮船)"),
                KanaExampleWord(japanese: "ふたつ (二つ)", romaji: "futatsu", english: "Two items (两个)"),
                KanaExampleWord(japanese: "ふざいひょう (不在票)", romaji: "fuzaihyou", english: "Missed delivery slip (不在通知单)"),
                KanaExampleWord(japanese: "ふつう (普通)", romaji: "futsuu", english: "Local train / Normal (普通列车/平常)")
            ],
            mnemonic: "Mount Fuji with slopes"
        ),

        KanaItem(
            id: "he",
            hiragana: "へ",
            katakana: "ヘ",
            romaji: "he",
            row: "は行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "へや (部屋)", romaji: "heya", english: "Room / Apartment (房间/宿舍)"),
                KanaExampleWord(japanese: "へんじ (返事)", romaji: "henji", english: "Reply / Answer (回复)"),
                KanaExampleWord(japanese: "へん (変)", romaji: "hen", english: "Strange / Unusual (奇怪)"),
                KanaExampleWord(japanese: "へいわ (平和)", romaji: "heiwa", english: "Peace (和平)"),
                KanaExampleWord(japanese: "へいき (平気)", romaji: "heiki", english: "All fine / No problem (没事/不在乎)"),
                KanaExampleWord(japanese: "へた (下手)", romaji: "heta", english: "Unskilled (不擅长)"),
                KanaExampleWord(japanese: "へる (減る)", romaji: "heru", english: "To decrease (减少)")
            ],
            mnemonic: "Pointing up to heaven hill"
        ),

        KanaItem(
            id: "ho",
            hiragana: "ほ",
            katakana: "ホ",
            romaji: "ho",
            row: "は行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ほん (本)", romaji: "hon", english: "Book (书本)"),
                KanaExampleWord(japanese: "ホテル", romaji: "hoteru", english: "Hotel (酒店)"),
                KanaExampleWord(japanese: "ホーム", romaji: "hoomu", english: "Train platform (月台/站台)"),
                KanaExampleWord(japanese: "ほっかいどう (北海道)", romaji: "hokkaidou", english: "Hokkaido (北海道)"),
                KanaExampleWord(japanese: "ほし (星)", romaji: "hoshi", english: "Star (星星)"),
                KanaExampleWord(japanese: "ほしい (欲しい)", romaji: "hoshii", english: "Want / Desire (想要)"),
                KanaExampleWord(japanese: "ほんとう (本当)", romaji: "hontou", english: "Really / Truly (真的吗/真实)")
            ],
            mnemonic: "A horse wearing a party hat"
        ),

        KanaItem(
            id: "ma",
            hiragana: "ま",
            katakana: "マ",
            romaji: "ma",
            row: "ま行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "まんが (漫画)", romaji: "manga", english: "Manga (漫画)"),
                KanaExampleWord(japanese: "まち (町)", romaji: "machi", english: "Town / City street (街道/城市)"),
                KanaExampleWord(japanese: "まつり (祭り)", romaji: "matsuri", english: "Festival (祭典/庙会)"),
                KanaExampleWord(japanese: "まど (窓)", romaji: "mado", english: "Window (窗户)"),
                KanaExampleWord(japanese: "まえ (前)", romaji: "mae", english: "Front / Before (前面)"),
                KanaExampleWord(japanese: "まぐろ (鮪)", romaji: "maguro", english: "Tuna fish (金枪鱼)"),
                KanaExampleWord(japanese: "まっすぐ", romaji: "massugu", english: "Straight ahead (一直走/笔直)")
            ],
            mnemonic: "A magical masquerade mask"
        ),

        KanaItem(
            id: "mi",
            hiragana: "み",
            katakana: "ミ",
            romaji: "mi",
            row: "ま行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "みず (水)", romaji: "mizu", english: "Water / Chilled water (凉水/清水)"),
                KanaExampleWord(japanese: "みせ (店)", romaji: "mise", english: "Shop / Restaurant (店铺)"),
                KanaExampleWord(japanese: "みち (道)", romaji: "michi", english: "Road / Path (道路)"),
                KanaExampleWord(japanese: "みぎ (右)", romaji: "migi", english: "Right side (右边)"),
                KanaExampleWord(japanese: "みなみ (南)", romaji: "minami", english: "South (南面/南口)"),
                KanaExampleWord(japanese: "みんな", romaji: "minna", english: "Everyone (大家)"),
                KanaExampleWord(japanese: "みどり (緑)", romaji: "midori", english: "Green color (绿色)")
            ],
            mnemonic: "Looks like the number 21 musical note"
        ),

        KanaItem(
            id: "mu",
            hiragana: "む",
            katakana: "ム",
            romaji: "mu",
            row: "ま行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "むりょう (無料)", romaji: "muryou", english: "Free of charge (免费)"),
                KanaExampleWord(japanese: "むずかしい (難しい)", romaji: "muzukashii", english: "Difficult (困难/复杂)"),
                KanaExampleWord(japanese: "むすめ (娘)", romaji: "musume", english: "Daughter (女儿)"),
                KanaExampleWord(japanese: "むかし (昔)", romaji: "mukashi", english: "Old times / Long ago (很久以前)"),
                KanaExampleWord(japanese: "むらさき (紫)", romaji: "murasaki", english: "Purple color (紫色)"),
                KanaExampleWord(japanese: "むし (虫)", romaji: "mushi", english: "Bug / Insect (昆虫)"),
                KanaExampleWord(japanese: "むかい (向かい)", romaji: "mukai", english: "Opposite side (正对面)")
            ],
            mnemonic: "A smiling cow going moo"
        ),

        KanaItem(
            id: "me",
            hiragana: "め",
            katakana: "メ",
            romaji: "me",
            row: "ま行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "めがね (眼鏡)", romaji: "megane", english: "Glasses (眼镜)"),
                KanaExampleWord(japanese: "メニュー", romaji: "menyuu", english: "Menu (菜单)"),
                KanaExampleWord(japanese: "め (目)", romaji: "me", english: "Eye (眼睛)"),
                KanaExampleWord(japanese: "めいし (名刺)", romaji: "meishi", english: "Business card (名片)"),
                KanaExampleWord(japanese: "メール", romaji: "meeru", english: "Email (电子邮件)"),
                KanaExampleWord(japanese: "めずらしい (珍しい)", romaji: "mezurashii", english: "Rare / Unique (罕见/稀奇)"),
                KanaExampleWord(japanese: "めん (麺)", romaji: "men", english: "Noodles (面条)")
            ],
            mnemonic: "An almond eye shape"
        ),

        KanaItem(
            id: "mo",
            hiragana: "も",
            katakana: "モ",
            romaji: "mo",
            row: "ま行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "もういちど", romaji: "mou ichido", english: "Once more (请再说一次)"),
                KanaExampleWord(japanese: "もの (物)", romaji: "mono", english: "Thing / Object (物品)"),
                KanaExampleWord(japanese: "もちろん", romaji: "mochiron", english: "Of course (当然/自然)"),
                KanaExampleWord(japanese: "もり (森)", romaji: "mori", english: "Forest (森林)"),
                KanaExampleWord(japanese: "もん (門)", romaji: "mon", english: "Gate (大门)"),
                KanaExampleWord(japanese: "もんだい (問題)", romaji: "mondai", english: "Problem / Question (问题)"),
                KanaExampleWord(japanese: "もつ (持つ)", romaji: "motsu", english: "To carry / Hold (拿/持有)")
            ],
            mnemonic: "A fish hook catching more worms"
        ),

        KanaItem(
            id: "ya",
            hiragana: "や",
            katakana: "ヤ",
            romaji: "ya",
            row: "や行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "やま (山)", romaji: "yama", english: "Mountain (大山)"),
                KanaExampleWord(japanese: "やさい (野菜)", romaji: "yasai", english: "Vegetables (蔬菜)"),
                KanaExampleWord(japanese: "やすみ (休み)", romaji: "yasumi", english: "Holiday / Day off (休息/放假)"),
                KanaExampleWord(japanese: "やすい (安い)", romaji: "yasui", english: "Cheap / Inexpensive (便宜)"),
                KanaExampleWord(japanese: "やくそく (約束)", romaji: "yakusoku", english: "Promise / Appointment (约定)"),
                KanaExampleWord(japanese: "やきとり (焼き鳥)", romaji: "yakitori", english: "Grilled chicken skewer (烤鸡肉串)"),
                KanaExampleWord(japanese: "やさしい (優しい)", romaji: "yasashii", english: "Kind / Gentle / Easy (亲切/温柔)")
            ],
            mnemonic: "A yak head with horns"
        ),

        KanaItem(
            id: "yu",
            hiragana: "ゆ",
            katakana: "ユ",
            romaji: "yu",
            row: "や行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ゆめ (夢)", romaji: "yume", english: "Dream (梦想/梦境)"),
                KanaExampleWord(japanese: "ゆうがた (夕方)", romaji: "yuugata", english: "Early evening (傍晚)"),
                KanaExampleWord(japanese: "ゆうびんきょく (郵便局)", romaji: "yuubinkyoku", english: "Post office (邮局)"),
                KanaExampleWord(japanese: "ゆき (雪)", romaji: "yuki", english: "Snow (雪花)"),
                KanaExampleWord(japanese: "ゆかた (浴衣)", romaji: "yukata", english: "Summer kimono (浴衣)"),
                KanaExampleWord(japanese: "ゆび (指)", romaji: "yubi", english: "Finger (手指)"),
                KanaExampleWord(japanese: "ゆっくり", romaji: "yukkuri", english: "Slowly / Take your time (慢慢来/从容)")
            ],
            mnemonic: "A goldfish swimming in a tub"
        ),

        KanaItem(
            id: "yo",
            hiragana: "よ",
            katakana: "ヨ",
            romaji: "yo",
            row: "や行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "よる (夜)", romaji: "yoru", english: "Night (夜晚)"),
                KanaExampleWord(japanese: "よやく (予約)", romaji: "yoyaku", english: "Reservation / Booking (预订/预约)"),
                KanaExampleWord(japanese: "ようこそ", romaji: "youkoso", english: "Welcome! (欢迎光临)"),
                KanaExampleWord(japanese: "よっつ (四つ)", romaji: "yottsu", english: "Four items (四个)"),
                KanaExampleWord(japanese: "よこ (横)", romaji: "yoko", english: "Beside / Horizontal (旁边/横向)"),
                KanaExampleWord(japanese: "よい (良い)", romaji: "yoi", english: "Good / Nice (好的)"),
                KanaExampleWord(japanese: "よむ (読む)", romaji: "yomu", english: "To read (阅读)")
            ],
            mnemonic: "A yo-yo dangling from a string"
        ),

        KanaItem(
            id: "ra",
            hiragana: "ら",
            katakana: "ラ",
            romaji: "ra",
            row: "ら行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "ラーメン", romaji: "raamen", english: "Ramen noodles (拉面)"),
                KanaExampleWord(japanese: "らいしゅう (来週)", romaji: "raishuu", english: "Next week (下周)"),
                KanaExampleWord(japanese: "ラジオ", romaji: "rajio", english: "Radio (收音机/广播)"),
                KanaExampleWord(japanese: "らいねん (来年)", romaji: "rainen", english: "Next year (明年)"),
                KanaExampleWord(japanese: "らく (楽)", romaji: "raku", english: "Easy / Comfortable (轻松/舒适)"),
                KanaExampleWord(japanese: "ライター", romaji: "raitaa", english: "Lighter (打火机)"),
                KanaExampleWord(japanese: "ランチ", romaji: "ranchi", english: "Lunch set (午市套餐)")
            ],
            mnemonic: "A rabbit sitting upright"
        ),

        KanaItem(
            id: "ri",
            hiragana: "り",
            katakana: "リ",
            romaji: "ri",
            row: "ら行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "りんご (林檎)", romaji: "ringo", english: "Apple (苹果)"),
                KanaExampleWord(japanese: "りょうしゅうしょ (領収書)", romaji: "ryoushuusho", english: "Official Receipt (发票/收据)"),
                KanaExampleWord(japanese: "りょこう (旅行)", romaji: "ryokou", english: "Travel / Trip (旅游)"),
                KanaExampleWord(japanese: "りゆう (理由)", romaji: "riyuu", english: "Reason (理由/原因)"),
                KanaExampleWord(japanese: "りょうり (料理)", romaji: "ryouri", english: "Cuisine / Cooking (料理/菜肴)"),
                KanaExampleWord(japanese: "りゅうがくせい (留学生)", romaji: "ryuugakusei", english: "International student (留学生)"),
                KanaExampleWord(japanese: "リアル", romaji: "riaru", english: "Real / Authentic (真实/逼真)")
            ],
            mnemonic: "Two reeds swaying in river"
        ),

        KanaItem(
            id: "ru",
            hiragana: "る",
            katakana: "ル",
            romaji: "ru",
            row: "ら行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "るすばん (留守番)", romaji: "rusuban", english: "House-sitting (看家)"),
                KanaExampleWord(japanese: "ルート", romaji: "ruuto", english: "Route / Navigation path (路线)"),
                KanaExampleWord(japanese: "ルール", romaji: "ruuru", english: "Rule / Etiquette (规则/规矩)"),
                KanaExampleWord(japanese: "ルーム", romaji: "ruumu", english: "Room (客房/房间)"),
                KanaExampleWord(japanese: "ルーズ", romaji: "ruuzu", english: "Loose / Relaxed (宽松)"),
                KanaExampleWord(japanese: "ルーレット", romaji: "ruuretto", english: "Roulette wheel (轮盘)"),
                KanaExampleWord(japanese: "ルーペ", romaji: "ruupe", english: "Magnifying glass (放大镜)")
            ],
            mnemonic: "A kangaroo with a looped pouch"
        ),

        KanaItem(
            id: "re",
            hiragana: "れ",
            katakana: "レ",
            romaji: "re",
            row: "ら行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "れっしゃ (列車)", romaji: "ressha", english: "Train (列车)"),
                KanaExampleWord(japanese: "レジ", romaji: "reji", english: "Cash register (收银台)"),
                KanaExampleWord(japanese: "レシート", romaji: "reshiito", english: "Store receipt (小票/收据)"),
                KanaExampleWord(japanese: "れんしゅう (練習)", romaji: "renshuu", english: "Practice (练习)"),
                KanaExampleWord(japanese: "レストラン", romaji: "resutoran", english: "Restaurant (西餐厅)"),
                KanaExampleWord(japanese: "れんらく (連絡)", romaji: "renraku", english: "Contact / Message (联络)"),
                KanaExampleWord(japanese: "れいぞうこ (冷蔵庫)", romaji: "reizouko", english: "Refrigerator (冰箱)")
            ],
            mnemonic: "A person resting against a wall"
        ),

        KanaItem(
            id: "ro",
            hiragana: "ろ",
            katakana: "ロ",
            romaji: "ro",
            row: "ら行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ろうそく", romaji: "rousoku", english: "Candle (蜡烛)"),
                KanaExampleWord(japanese: "ろく (六)", romaji: "roku", english: "Number 6 (数字六)"),
                KanaExampleWord(japanese: "ロッカー", romaji: "rokkaa", english: "Coin locker (储物柜)"),
                KanaExampleWord(japanese: "ロビー", romaji: "robii", english: "Lobby (酒店大堂)"),
                KanaExampleWord(japanese: "ローカル", romaji: "rookaru", english: "Local (当地/本地)"),
                KanaExampleWord(japanese: "ロールケーキ", romaji: "roorukeeki", english: "Swiss roll cake (蛋糕卷)"),
                KanaExampleWord(japanese: "ろじうら (路地裏)", romaji: "rojiura", english: "Back alley (后巷/胡同)")
            ],
            mnemonic: "A road looping without a knot"
        ),

        KanaItem(
            id: "wa",
            hiragana: "わ",
            katakana: "ワ",
            romaji: "wa",
            row: "わ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "わさび", romaji: "wasabi", english: "Wasabi (山葵/芥末)"),
                KanaExampleWord(japanese: "わたし (私)", romaji: "watashi", english: "I / Me (我)"),
                KanaExampleWord(japanese: "わかる (分かる)", romaji: "wakaru", english: "To understand (明白/理解)"),
                KanaExampleWord(japanese: "わすれもの (忘れ物)", romaji: "wasuremono", english: "Lost and found item (遗落物品)"),
                KanaExampleWord(japanese: "わりばし (割り箸)", romaji: "waribashi", english: "Disposable chopsticks (一次性筷子)"),
                KanaExampleWord(japanese: "わふう (和風)", romaji: "wafu", english: "Japanese style (日式风情)"),
                KanaExampleWord(japanese: "わらう (笑う)", romaji: "warau", english: "To laugh / Smile (笑/微笑)")
            ],
            mnemonic: "A graceful swan"
        ),

        KanaItem(
            id: "wo",
            hiragana: "を",
            katakana: "ヲ",
            romaji: "wo",
            row: "わ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "〜をください", romaji: "o kudasai", english: "Please give me... (请给我...)"),
                KanaExampleWord(japanese: "みずをのむ (水を飲む)", romaji: "mizu o nomu", english: "Drink water (喝水)"),
                KanaExampleWord(japanese: "きっぷをかう (切符を買う)", romaji: "kippu o kau", english: "Buy ticket (买车票)"),
                KanaExampleWord(japanese: "ドアをあける (ドアを開ける)", romaji: "doa o akeru", english: "Open door (开门)"),
                KanaExampleWord(japanese: "ほんをよむ (本を読む)", romaji: "hon o yomu", english: "Read book (看书)"),
                KanaExampleWord(japanese: "ごはんをたべる (ご飯を食べる)", romaji: "gohan o taberu", english: "Eat meal (吃饭)"),
                KanaExampleWord(japanese: "しゃしんをとる (写真を撮る)", romaji: "shashin o toru", english: "Take photo (拍照)")
            ],
            mnemonic: "A person leaping over a hurdle"
        ),

        KanaItem(
            id: "n",
            hiragana: "ん",
            katakana: "ン",
            romaji: "n",
            row: "わ行",
            column: "n",
            exampleWords: [
                KanaExampleWord(japanese: "にほん (日本)", romaji: "nihon", english: "Japan (日本)"),
                KanaExampleWord(japanese: "しんかんせん (新幹線)", romaji: "shinkansen", english: "Bullet train (新干线)"),
                KanaExampleWord(japanese: "かんぱい (乾杯)", romaji: "kanpai", english: "Cheers! (干杯)"),
                KanaExampleWord(japanese: "ぜんぶ (全部)", romaji: "zenbu", english: "All of it (全部)"),
                KanaExampleWord(japanese: "ほん (本)", romaji: "hon", english: "Book (书本)"),
                KanaExampleWord(japanese: "でんしゃ (電車)", romaji: "densha", english: "Train (电车)"),
                KanaExampleWord(japanese: "ラーメン", romaji: "raamen", english: "Ramen (拉面)")
            ],
            mnemonic: "Looks like lowercase letter 'n'"
        )
    ]

    public let dakuonList: [KanaItem] = [
        KanaItem(
            id: "ga",
            hiragana: "が",
            katakana: "ガ",
            romaji: "ga",
            row: "が行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "がっこう (学校)", romaji: "gakkou", english: "School (学校)"),
                KanaExampleWord(japanese: "外国 (がいこく)", romaji: "gaikoku", english: "Foreign country (外国)"),
                KanaExampleWord(japanese: "がんばって (頑張って)", romaji: "ganbatte", english: "Do your best! (加油)"),
                KanaExampleWord(japanese: "がいこくご (外国語)", romaji: "gaikokugo", english: "Foreign language (外语)"),
                KanaExampleWord(japanese: "がくせい (学生)", romaji: "gakusei", english: "Student (学生)"),
                KanaExampleWord(japanese: "がめん (画面)", romaji: "gamen", english: "Screen / Display (屏幕)"),
                KanaExampleWord(japanese: "がっか (学科)", romaji: "gakka", english: "Department / Subject (学科)")
            ],
            mnemonic: "Voiced か"
        ),

        KanaItem(
            id: "gi",
            hiragana: "ぎ",
            katakana: "ギ",
            romaji: "gi",
            row: "が行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "ぎゅうどん (牛丼)", romaji: "gyuudon", english: "Beef bowl (牛肉饭)"),
                KanaExampleWord(japanese: "ぎんざ (銀座)", romaji: "ginza", english: "Ginza district (银座)"),
                KanaExampleWord(japanese: "ぎんこう (銀行)", romaji: "ginkou", english: "Bank (银行)"),
                KanaExampleWord(japanese: "ぎゅうにゅう (牛乳)", romaji: "gyuunyuu", english: "Milk (牛奶)"),
                KanaExampleWord(japanese: "ぎょうざ (餃子)", romaji: "gyouza", english: "Gyoza dumplings (煎饺/饺子)"),
                KanaExampleWord(japanese: "ぎじゅつ (技術)", romaji: "gijutsu", english: "Technology / Technique (技术)"),
                KanaExampleWord(japanese: "ギター", romaji: "gitaa", english: "Guitar (吉他)")
            ],
            mnemonic: "Voiced き"
        ),

        KanaItem(
            id: "gu",
            hiragana: "ぐ",
            katakana: "グ",
            romaji: "gu",
            row: "が行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ぐんま (群馬)", romaji: "gunma", english: "Gunma (群马)"),
                KanaExampleWord(japanese: "グラス", romaji: "gurasu", english: "Drinking glass (玻璃杯)"),
                KanaExampleWord(japanese: "ぐあい (具合)", romaji: "guai", english: "Physical condition (健康状态)"),
                KanaExampleWord(japanese: "グループ", romaji: "guruupu", english: "Group (小组/团队)"),
                KanaExampleWord(japanese: "軍手 (ぐんて)", romaji: "gunte", english: "Cotton work gloves (劳保手套)"),
                KanaExampleWord(japanese: "グルメ", romaji: "gurume", english: "Gourmet food (美食)"),
                KanaExampleWord(japanese: "ぐんかん (軍艦巻き)", romaji: "gunkan", english: "Battleship sushi (军舰卷寿司)")
            ],
            mnemonic: "Voiced く"
        ),

        KanaItem(
            id: "ge",
            hiragana: "げ",
            katakana: "ゲ",
            romaji: "ge",
            row: "が行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "げんき (元気)", romaji: "genki", english: "Energetic / Well (有精神/健康)"),
                KanaExampleWord(japanese: "げんかん (玄関)", romaji: "genkan", english: "Entryway / Foyer (玄关)"),
                KanaExampleWord(japanese: "ゲーム", romaji: "geemu", english: "Game / Video game (游戏)"),
                KanaExampleWord(japanese: "げきじょう (劇場)", romaji: "gekijou", english: "Theater (剧场)"),
                KanaExampleWord(japanese: "げつようび (月曜日)", romaji: "getsuyoubi", english: "Monday (周一)"),
                KanaExampleWord(japanese: "げんざい (現在)", romaji: "genzai", english: "Present / Current time (现在)"),
                KanaExampleWord(japanese: "げんきん (現金)", romaji: "genkin", english: "Cash payment (现金)")
            ],
            mnemonic: "Voiced け"
        ),

        KanaItem(
            id: "go",
            hiragana: "ご",
            katakana: "ゴ",
            romaji: "go",
            row: "が行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ごはん (ご飯)", romaji: "gohan", english: "Rice / Meal (米饭/饭)"),
                KanaExampleWord(japanese: "ごご (午後)", romaji: "gogo", english: "Afternoon (下午)"),
                KanaExampleWord(japanese: "ごぜん (午前)", romaji: "gozen", english: "Morning (上午)"),
                KanaExampleWord(japanese: "ごみ (ゴミ)", romaji: "gomi", english: "Trash / Garbage (垃圾)"),
                KanaExampleWord(japanese: "ごちそうさま", romaji: "gochisousama", english: "Thank you for the meal (多谢款待)"),
                KanaExampleWord(japanese: "ごうけい (合計)", romaji: "goukei", english: "Total sum (合计)"),
                KanaExampleWord(japanese: "ごめんなさい", romaji: "gomennasai", english: "I'm sorry (对不起)")
            ],
            mnemonic: "Voiced こ"
        ),

        KanaItem(
            id: "za",
            hiragana: "ざ",
            katakana: "ザ",
            romaji: "za",
            row: "ざ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "ざっし (雑誌)", romaji: "zasshi", english: "Magazine (杂志)"),
                KanaExampleWord(japanese: "ざぶとん (座布団)", romaji: "zabuton", english: "Floor cushion (坐垫)"),
                KanaExampleWord(japanese: "ざんねん (残念)", romaji: "zannen", english: "Regrettable / What a pity (可惜/遗憾)"),
                KanaExampleWord(japanese: "ざるそば", romaji: "zarusoba", english: "Chilled soba on bamboo (竹笼荞麦面)"),
                KanaExampleWord(japanese: "ざいりょう (材料)", romaji: "zairyou", english: "Ingredients / Material (材料/食材)"),
                KanaExampleWord(japanese: "ざっか (雑貨)", romaji: "zakka", english: "Sundries / Daily goods (杂货/文创)"),
                KanaExampleWord(japanese: "ざんぎょう (残業)", romaji: "zangyou", english: "Overtime work (加班)")
            ],
            mnemonic: "Voiced さ"
        ),

        KanaItem(
            id: "ji",
            hiragana: "じ",
            katakana: "ジ",
            romaji: "ji",
            row: "ざ行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "じかん (時間)", romaji: "jikan", english: "Time / Hour (时间)"),
                KanaExampleWord(japanese: "じどうはんばいき (自動販売機)", romaji: "jidouhanbaiki", english: "Vending machine (自动售货机)"),
                KanaExampleWord(japanese: "じゆう (自由)", romaji: "jiyuu", english: "Freedom / Free choice (自由)"),
                KanaExampleWord(japanese: "じこ (事故)", romaji: "jiko", english: "Accident (事故)"),
                KanaExampleWord(japanese: "じしょ (辞書)", romaji: "jisho", english: "Dictionary (字典)"),
                KanaExampleWord(japanese: "じゅうしょ (住所)", romaji: "juusho", english: "Address (住址)"),
                KanaExampleWord(japanese: "じゅんび (準備)", romaji: "junbi", english: "Preparation (准备)")
            ],
            mnemonic: "Voiced し"
        ),

        KanaItem(
            id: "zu",
            hiragana: "ず",
            katakana: "ズ",
            romaji: "zu",
            row: "ざ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ずっと", romaji: "zutto", english: "All the time / By far (一直/非常)"),
                KanaExampleWord(japanese: "ずかん (図鑑)", romaji: "zukan", english: "Illustrated encyclopedia (图鉴/图册)"),
                KanaExampleWord(japanese: "ずぼん (ズボン)", romaji: "zubon", english: "Trousers / Pants (裤子)"),
                KanaExampleWord(japanese: "ずけい (図形)", romaji: "zukei", english: "Graphic figure (图形)"),
                KanaExampleWord(japanese: "ずじょう (頭上)", romaji: "zujou", english: "Overhead (头顶上方)"),
                KanaExampleWord(japanese: "ずるい", romaji: "zurui", english: "Sly / Unfair (狡猾/狡黠)"),
                KanaExampleWord(japanese: "ずし (逗子)", romaji: "zushi", english: "Zushi Beach (逗子海滩)")
            ],
            mnemonic: "Voiced す"
        ),

        KanaItem(
            id: "ze",
            hiragana: "ぜ",
            katakana: "ゼ",
            romaji: "ze",
            row: "ざ行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "ぜんぶ (全部)", romaji: "zenbu", english: "Everything / All (全部)"),
                KanaExampleWord(japanese: "ぜいこみ (税込)", romaji: "zeikomi", english: "Tax included (含税价)"),
                KanaExampleWord(japanese: "ぜったい (絶対)", romaji: "zettai", english: "Absolutely / Definitely (绝对)"),
                KanaExampleWord(japanese: "ぜんぜん (全然)", romaji: "zenzen", english: "Not at all (完全不)"),
                KanaExampleWord(japanese: "ぜひ (是非)", romaji: "zehi", english: "By all means / Please do (务必/一定)"),
                KanaExampleWord(japanese: "ゼロ", romaji: "zero", english: "Zero (零)"),
                KanaExampleWord(japanese: "ぜんこく (全国)", romaji: "zenkoku", english: "Nationwide (全国)")
            ],
            mnemonic: "Voiced せ"
        ),

        KanaItem(
            id: "zo",
            hiragana: "ぞ",
            katakana: "ゾ",
            romaji: "zo",
            row: "ざ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ぞう (象)", romaji: "zou", english: "Elephant (大象)"),
                KanaExampleWord(japanese: "ぞくぞく", romaji: "zokuzoku", english: "Thrilled / Shivering (阵阵发抖/兴奋)"),
                KanaExampleWord(japanese: "ぞうきん (雑巾)", romaji: "zoukin", english: "Cleaning rag (抹布)"),
                KanaExampleWord(japanese: "ぞくへん (続編)", romaji: "zokuhen", english: "Sequel chapter (续集)"),
                KanaExampleWord(japanese: "ゾーン", romaji: "zoon", english: "Zone / Area (区域)"),
                KanaExampleWord(japanese: "ぞうしき (雑色)", romaji: "zoushiki", english: "Mixed colors (杂色)"),
                KanaExampleWord(japanese: "ぞうぜい (増税)", romaji: "zouzei", english: "Tax hike (增税)")
            ],
            mnemonic: "Voiced そ"
        ),

        KanaItem(
            id: "da",
            hiragana: "だ",
            katakana: "ダ",
            romaji: "da",
            row: "だ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "だいじょうぶ (大丈夫)", romaji: "daijoubu", english: "All right / OK (没问题)"),
                KanaExampleWord(japanese: "だいがく (大学)", romaji: "daigaku", english: "University (大学)"),
                KanaExampleWord(japanese: "だんせい (男性)", romaji: "dansei", english: "Male / Gentlemen (男士)"),
                KanaExampleWord(japanese: "だれ (誰)", romaji: "dare", english: "Who? (谁)"),
                KanaExampleWord(japanese: "だんだん", romaji: "dandan", english: "Gradually (渐渐/逐步)"),
                KanaExampleWord(japanese: "だいどころ (台所)", romaji: "daidokoro", english: "Kitchen (厨房)"),
                KanaExampleWord(japanese: "ダイヤ", romaji: "daiya", english: "Train timetable (列车运行图)")
            ],
            mnemonic: "Voiced た"
        ),

        KanaItem(
            id: "de",
            hiragana: "で",
            katakana: "デ",
            romaji: "de",
            row: "だ行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "でんしゃ (電車)", romaji: "densha", english: "Train (电车)"),
                KanaExampleWord(japanese: "でぐち (出口)", romaji: "deguchi", english: "Exit (出口)"),
                KanaExampleWord(japanese: "でんわ (電話)", romaji: "denwa", english: "Telephone (电话)"),
                KanaExampleWord(japanese: "デザート", romaji: "dezaato", english: "Dessert (甜点)"),
                KanaExampleWord(japanese: "デパート", romaji: "depaato", english: "Department store (百货商场)"),
                KanaExampleWord(japanese: "できる (出来る)", romaji: "dekiru", english: "Can do / Possible (能够/可以)"),
                KanaExampleWord(japanese: "デート", romaji: "deeto", english: "Date / Romance (约会)")
            ],
            mnemonic: "Voiced て"
        ),

        KanaItem(
            id: "do",
            hiragana: "ど",
            katakana: "ド",
            romaji: "do",
            row: "だ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "どこ (何処)", romaji: "doko", english: "Where? (哪里)"),
                KanaExampleWord(japanese: "どうも", romaji: "doumo", english: "Thanks / Hello (多谢/你好)"),
                KanaExampleWord(japanese: "どようび (土曜日)", romaji: "doyoubi", english: "Saturday (周六)"),
                KanaExampleWord(japanese: "ドア", romaji: "doa", english: "Door (车门/房间门)"),
                KanaExampleWord(japanese: "どうぶつ (動物)", romaji: "doubutsu", english: "Animal (动物)"),
                KanaExampleWord(japanese: "どれ", romaji: "dore", english: "Which one? (哪一个)"),
                KanaExampleWord(japanese: "どうして", romaji: "doushite", english: "Why? (为什么)")
            ],
            mnemonic: "Voiced と"
        ),

        KanaItem(
            id: "ba",
            hiragana: "ば",
            katakana: "バ",
            romaji: "ba",
            row: "ば行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "ばしょ (場所)", romaji: "basho", english: "Place / Location (场所/地点)"),
                KanaExampleWord(japanese: "バス", romaji: "basu", english: "Bus (公交车/巴士)"),
                KanaExampleWord(japanese: "ばあい (場合)", romaji: "baai", english: "Case / Situation (情况)"),
                KanaExampleWord(japanese: "ばんごはん (晩ご飯)", romaji: "bangohan", english: "Dinner (晚餐)"),
                KanaExampleWord(japanese: "ばっぐ (バッグ)", romaji: "baggu", english: "Bag (包)"),
                KanaExampleWord(japanese: "ばくだん (爆弾)", romaji: "bakudan", english: "Bomb / Special onigiri (炸弹饭团)"),
                KanaExampleWord(japanese: "ばいきん (バイキン)", romaji: "baikin", english: "Germs (细菌)")
            ],
            mnemonic: "Voiced は"
        ),

        KanaItem(
            id: "bi",
            hiragana: "び",
            katakana: "ビ",
            romaji: "bi",
            row: "ば行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "ビール", romaji: "biiru", english: "Beer (啤酒)"),
                KanaExampleWord(japanese: "ビル", romaji: "biru", english: "Building / High-rise (大楼/大厦)"),
                KanaExampleWord(japanese: "びじゅつかん (美術館)", romaji: "bijutsukan", english: "Art Museum (美术馆)"),
                KanaExampleWord(japanese: "びょういん (病院)", romaji: "byouin", english: "Hospital (医院)"),
                KanaExampleWord(japanese: "びっくり", romaji: "bikkuri", english: "Surprised (吃惊/吓一跳)"),
                KanaExampleWord(japanese: "びよういん (美容院)", romaji: "biyouin", english: "Hair salon (美发店)"),
                KanaExampleWord(japanese: "ビニールぶくろ (ビニール袋)", romaji: "biniirubukuro", english: "Plastic shopping bag (塑料袋)")
            ],
            mnemonic: "Voiced ひ"
        ),

        KanaItem(
            id: "bu",
            hiragana: "ぶ",
            katakana: "ブ",
            romaji: "bu",
            row: "ば行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ぶんか (文化)", romaji: "bunka", english: "Culture (文化)"),
                KanaExampleWord(japanese: "ぶたにく (豚肉)", romaji: "butaniku", english: "Pork (猪肉)"),
                KanaExampleWord(japanese: "ぶどう (葡萄)", romaji: "budou", english: "Grape (葡萄)"),
                KanaExampleWord(japanese: "ぶちょう (部長)", romaji: "buchou", english: "Department Manager (部长/主管)"),
                KanaExampleWord(japanese: "ぶらぶら", romaji: "burabura", english: "Strolling around (闲逛/溜达)"),
                KanaExampleWord(japanese: "ぶぶん (部分)", romaji: "bubun", english: "Part / Section (部分)"),
                KanaExampleWord(japanese: "ぶっか (物価)", romaji: "bukka", english: "Cost of living (物价)")
            ],
            mnemonic: "Voiced ふ"
        ),

        KanaItem(
            id: "be",
            hiragana: "べ",
            katakana: "ベ",
            romaji: "be",
            row: "ば行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "べんり (便利)", romaji: "benri", english: "Convenient (方便/便利)"),
                KanaExampleWord(japanese: "べんとう (弁当)", romaji: "bentou", english: "Bento boxed lunch (便当)"),
                KanaExampleWord(japanese: "ベッド", romaji: "beddo", english: "Bed (床)"),
                KanaExampleWord(japanese: "べつ (別)", romaji: "betsu", english: "Separate / Different (分开/另外)"),
                KanaExampleWord(japanese: "べんきょう (勉強)", romaji: "benkyou", english: "Studying (学习)"),
                KanaExampleWord(japanese: "ベル", romaji: "beru", english: "Bell / Chime (门铃/铃声)"),
                KanaExampleWord(japanese: "べろ (舌)", romaji: "bero", english: "Tongue (舌头)")
            ],
            mnemonic: "Voiced へ"
        ),

        KanaItem(
            id: "bo",
            hiragana: "ぼ",
            katakana: "ボ",
            romaji: "bo",
            row: "ば行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ぼく (僕)", romaji: "boku", english: "I / Me (我)"),
                KanaExampleWord(japanese: "ぼうし (帽子)", romaji: "boushi", english: "Hat / Cap (帽子)"),
                KanaExampleWord(japanese: "ボタン", romaji: "botan", english: "Button (按钮/纽扣)"),
                KanaExampleWord(japanese: "ボールペン", romaji: "boorupen", english: "Ballpoint pen (圆珠笔)"),
                KanaExampleWord(japanese: "ぼうけん (冒険)", romaji: "bouken", english: "Adventure (冒险)"),
                KanaExampleWord(japanese: "ボトル", romaji: "botoru", english: "Bottle (瓶子)"),
                KanaExampleWord(japanese: "ぼんさい (盆栽)", romaji: "bonsai", english: "Bonsai miniature tree (盆栽)")
            ],
            mnemonic: "Voiced ほ"
        ),

        KanaItem(
            id: "pa",
            hiragana: "ぱ",
            katakana: "パ",
            romaji: "pa",
            row: "ぱ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "パン", romaji: "pan", english: "Bread / Pastry (面包)"),
                KanaExampleWord(japanese: "パスポート", romaji: "pasupooto", english: "Passport (护照)"),
                KanaExampleWord(japanese: "パトカー", romaji: "patokaa", english: "Police patrol car (警车)"),
                KanaExampleWord(japanese: "パスタ", romaji: "pasuta", english: "Pasta (意面)"),
                KanaExampleWord(japanese: "パーティー", romaji: "paatii", english: "Party (派对/聚会)"),
                KanaExampleWord(japanese: "パソコン", romaji: "pasokon", english: "Personal Computer (电脑/笔记本)"),
                KanaExampleWord(japanese: "パーク", romaji: "paaku", english: "Park / Theme park (公园/乐园)")
            ],
            mnemonic: "Plosive は"
        ),

        KanaItem(
            id: "pi",
            hiragana: "ぴ",
            katakana: "ピ",
            romaji: "pi",
            row: "ぱ行",
            column: "i",
            exampleWords: [
                KanaExampleWord(japanese: "ピンク", romaji: "pinku", english: "Pink color (粉色)"),
                KanaExampleWord(japanese: "ピアノ", romaji: "piano", english: "Piano (钢琴)"),
                KanaExampleWord(japanese: "ピザ", romaji: "piza", english: "Pizza (披萨)"),
                KanaExampleWord(japanese: "ビル (ピル)", romaji: "piru", english: "Pill (药片)"),
                KanaExampleWord(japanese: "ピクニック", romaji: "pikunikku", english: "Picnic (野餐)"),
                KanaExampleWord(japanese: "ピンポン", romaji: "pinpon", english: "Door chime / Table tennis (门铃/乒乓)"),
                KanaExampleWord(japanese: "ピース", romaji: "piisu", english: "Peace sign (和平手势/一块)")
            ],
            mnemonic: "Plosive ひ"
        ),

        KanaItem(
            id: "pu",
            hiragana: "ぷ",
            katakana: "プ",
            romaji: "pu",
            row: "ぱ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "プリン", romaji: "purin", english: "Caramel pudding (焦糖布丁)"),
                KanaExampleWord(japanese: "プレゼント", romaji: "purezento", english: "Present / Gift (礼物)"),
                KanaExampleWord(japanese: "プール", romaji: "puuru", english: "Swimming pool (游泳池)"),
                KanaExampleWord(japanese: "プロ", romaji: "puro", english: "Professional (专业人士)"),
                KanaExampleWord(japanese: "プラスチック", romaji: "purasuchikku", english: "Plastic (塑料制品)"),
                KanaExampleWord(japanese: "プラン", romaji: "puran", english: "Plan / Strategy (计划)"),
                KanaExampleWord(japanese: "プレート", romaji: "pureeto", english: "Plate / Platter (餐盘/招牌)")
            ],
            mnemonic: "Plosive ふ"
        ),

        KanaItem(
            id: "pe",
            hiragana: "ぺ",
            katakana: "ペ",
            romaji: "pe",
            row: "ぱ行",
            column: "e",
            exampleWords: [
                KanaExampleWord(japanese: "ペン", romaji: "pen", english: "Pen / Marker (笔/钢笔)"),
                KanaExampleWord(japanese: "ペットボトル", romaji: "pettobotoru", english: "PET plastic bottle (塑料饮料瓶)"),
                KanaExampleWord(japanese: "ページ", romaji: "peeji", english: "Page (页面/页码)"),
                KanaExampleWord(japanese: "ペア", romaji: "pea", english: "Pair / Couple (一对/双人)"),
                KanaExampleWord(japanese: "ペーパー", romaji: "peepaa", english: "Paper / Napkin (纸张/纸巾)"),
                KanaExampleWord(japanese: "ペコペコ", romaji: "pekopeko", english: "Starving hungry (肚子饿得咕咕叫)"),
                KanaExampleWord(japanese: "ペイント", romaji: "peinto", english: "Paint (油漆/绘画)")
            ],
            mnemonic: "Plosive へ"
        ),

        KanaItem(
            id: "po",
            hiragana: "ぽ",
            katakana: "ポ",
            romaji: "po",
            row: "ぱ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ポスト", romaji: "posuto", english: "Postbox / Mailbox (邮筒/邮箱)"),
                KanaExampleWord(japanese: "ポテト", romaji: "poteto", english: "French fries / Potato (薯条/土豆)"),
                KanaExampleWord(japanese: "ポケット", romaji: "poketto", english: "Pocket (口袋)"),
                KanaExampleWord(japanese: "ポイント", romaji: "pointo", english: "Points / Reward points (积分/要点)"),
                KanaExampleWord(japanese: "ポスター", romaji: "posutaa", english: "Poster (海报)"),
                KanaExampleWord(japanese: "ポップコーン", romaji: "poppukoon", english: "Popcorn (爆米花)"),
                KanaExampleWord(japanese: "ポリス", romaji: "porisu", english: "Police (警察)")
            ],
            mnemonic: "Plosive ほ"
        )
    ]

    public let yoonList: [KanaItem] = [
        KanaItem(
            id: "kya",
            hiragana: "きゃ",
            katakana: "キャ",
            romaji: "kya",
            row: "きゃ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "きゃく (客)", romaji: "kyaku", english: "Customer / Guest (客人)"),
                KanaExampleWord(japanese: "キャベツ", romaji: "kyabetsu", english: "Cabbage (卷心菜)"),
                KanaExampleWord(japanese: "キャンプ", romaji: "kyanpu", english: "Camping (露营)"),
                KanaExampleWord(japanese: "キャンディー", romaji: "kyandii", english: "Candy (糖果)"),
                KanaExampleWord(japanese: "キャッシャー", romaji: "kyasshaa", english: "Cashier counter (收银台)"),
                KanaExampleWord(japanese: "キャラ", romaji: "kyara", english: "Character / Anime figure (角色)"),
                KanaExampleWord(japanese: "キャンセル", romaji: "kyanseru", english: "Cancellation (取消/退订)")
            ],
            mnemonic: "き + ゃ"
        ),

        KanaItem(
            id: "kyu",
            hiragana: "きゅ",
            katakana: "キュ",
            romaji: "kyu",
            row: "きゃ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "きゅうこう (急行)", romaji: "kyuukou", english: "Express train (急行列车)"),
                KanaExampleWord(japanese: "きゅうり (胡瓜)", romaji: "kyuuri", english: "Cucumber (黄瓜)"),
                KanaExampleWord(japanese: "きゅうけい (休憩)", romaji: "kyuukei", english: "Break / Rest (休息)"),
                KanaExampleWord(japanese: "きゅうじつ (休日)", romaji: "kyuujitsu", english: "Day off / Holiday (休假日)"),
                KanaExampleWord(japanese: "きゅうしゅう (九州)", romaji: "kyuushuu", english: "Kyushu (九州)"),
                KanaExampleWord(japanese: "きゅうきゅうしゃ (救急車)", romaji: "kyuukyuusha", english: "Ambulance (救护车)"),
                KanaExampleWord(japanese: "きゅうりょう (給料)", romaji: "kyuuryou", english: "Salary / Paycheck (薪水/工资)")
            ],
            mnemonic: "き + ゅ"
        ),

        KanaItem(
            id: "kyo",
            hiragana: "きょ",
            katakana: "キョ",
            romaji: "kyo",
            row: "きゃ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "きょう (今日)", romaji: "kyou", english: "Today (今天)"),
                KanaExampleWord(japanese: "きょうと (京都)", romaji: "kyouto", english: "Kyoto (京都)"),
                KanaExampleWord(japanese: "きょうしつ (教室)", romaji: "kyoushitsu", english: "Classroom (教室)"),
                KanaExampleWord(japanese: "きょうみ (興味)", romaji: "kyoumi", english: "Interest / Curiosity (兴趣)"),
                KanaExampleWord(japanese: "きょり (距離)", romaji: "kyori", english: "Distance (距离)"),
                KanaExampleWord(japanese: "きょねん (去年)", romaji: "kyonen", english: "Last year (去年)"),
                KanaExampleWord(japanese: "きょうりょく (協力)", romaji: "kyouryoku", english: "Cooperation (协助/合作)")
            ],
            mnemonic: "き + ょ"
        ),

        KanaItem(
            id: "sha",
            hiragana: "しゃ",
            katakana: "シャ",
            romaji: "sha",
            row: "しゃ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "しゃしん (写真)", romaji: "shashin", english: "Photo (照片)"),
                KanaExampleWord(japanese: "しゃちょう (社長)", romaji: "shachou", english: "Company President (社长/总经理)"),
                KanaExampleWord(japanese: "しゃかい (社会)", romaji: "shakai", english: "Society (社会)"),
                KanaExampleWord(japanese: "シャワー", romaji: "shawaa", english: "Shower (淋浴)"),
                KanaExampleWord(japanese: "しゃせん (車線)", romaji: "shasen", english: "Traffic lane (车道)"),
                KanaExampleWord(japanese: "シャツ", romaji: "shatsu", english: "Shirt (衬衫)"),
                KanaExampleWord(japanese: "しゃりん (車輪)", romaji: "sharin", english: "Wheel (车轮)")
            ],
            mnemonic: "し + ゃ"
        ),

        KanaItem(
            id: "shu",
            hiragana: "しゅ",
            katakana: "シュ",
            romaji: "shu",
            row: "しゃ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "しゅうでん (終電)", romaji: "shuuden", english: "Last train (末班车)"),
                KanaExampleWord(japanese: "しゅくだい (宿題)", romaji: "shukudai", english: "Homework (作业)"),
                KanaExampleWord(japanese: "しゅみ (趣味)", romaji: "shumi", english: "Hobby (爱好)"),
                KanaExampleWord(japanese: "しゅうかん (週間)", romaji: "shuukan", english: "Week / Weekly (周/星期)"),
                KanaExampleWord(japanese: "しゅうまつ (週末)", romaji: "shuumatsu", english: "Weekend (周末)"),
                KanaExampleWord(japanese: "しゅっぱつ (出発)", romaji: "shuppatsu", english: "Departure (出发)"),
                KanaExampleWord(japanese: "しゅるい (種類)", romaji: "shurui", english: "Type / Variety (种类)")
            ],
            mnemonic: "し + ゅ"
        ),

        KanaItem(
            id: "sho",
            hiragana: "しょ",
            katakana: "ショ",
            romaji: "sho",
            row: "しゃ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "しょうひん (商品)", romaji: "shouhin", english: "Merchandise / Goods (商品)"),
                KanaExampleWord(japanese: "しょうゆ (醤油)", romaji: "shouyu", english: "Soy sauce (酱油)"),
                KanaExampleWord(japanese: "しょうしょう (少々)", romaji: "shoushou", english: "A moment please (请稍候)"),
                KanaExampleWord(japanese: "しょくどう (食堂)", romaji: "shokudou", english: "Dining hall / Canteen (食堂)"),
                KanaExampleWord(japanese: "しょくじ (食事)", romaji: "shokuji", english: "Meal (用餐)"),
                KanaExampleWord(japanese: "ショップ", romaji: "shoppu", english: "Shop / Store (商店)"),
                KanaExampleWord(japanese: "しょうてんがい (商店街)", romaji: "shoutengai", english: "Shopping street (商业街)")
            ],
            mnemonic: "し + ょ"
        ),

        KanaItem(
            id: "cha",
            hiragana: "ちゃ",
            katakana: "チャ",
            romaji: "cha",
            row: "ちゃ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "おちゃ (お茶)", romaji: "ocha", english: "Green tea (绿茶/茶水)"),
                KanaExampleWord(japanese: "ちゃわん (茶碗)", romaji: "chawan", english: "Rice bowl / Teacup (饭碗/茶碗)"),
                KanaExampleWord(japanese: "チャンス", romaji: "chansu", english: "Opportunity / Chance (机会)"),
                KanaExampleWord(japanese: "ちゃいろ (茶色)", romaji: "chairo", english: "Brown color (茶色/棕色)"),
                KanaExampleWord(japanese: "チャージ (チャージ)", romaji: "chaaji", english: "Recharge IC card (充值)"),
                KanaExampleWord(japanese: "チャーハン", romaji: "chaahan", english: "Fried rice (炒饭)"),
                KanaExampleWord(japanese: "チャーシュー", romaji: "chaashuu", english: "Chashu pork (叉烧肉)")
            ],
            mnemonic: "ち + ゃ"
        ),

        KanaItem(
            id: "chu",
            hiragana: "ちゅ",
            katakana: "チュ",
            romaji: "chu",
            row: "ちゃ行",
            column: "u",
            exampleWords: [
                KanaExampleWord(japanese: "ちゅうもん (注文)", romaji: "chuumon", english: "Food order (点单/订购)"),
                KanaExampleWord(japanese: "ちゅうしゃじょう (駐車場)", romaji: "chuushajou", english: "Parking lot (停车场)"),
                KanaExampleWord(japanese: "ちゅうごく (中国)", romaji: "chuugoku", english: "China (中国)"),
                KanaExampleWord(japanese: "ちゅうい (注意)", romaji: "chuui", english: "Caution / Attention (注意)"),
                KanaExampleWord(japanese: "ちゅうか (中華)", romaji: "chuuka", english: "Chinese cuisine (中华料理)"),
                KanaExampleWord(japanese: "ちゅうし (中止)", romaji: "chuushi", english: "Suspension / Cancelled (停运/中止)"),
                KanaExampleWord(japanese: "ちゅうしゃ (注射)", romaji: "chuusha", english: "Injection (打针)")
            ],
            mnemonic: "ち + ゅ"
        ),

        KanaItem(
            id: "cho",
            hiragana: "ちょ",
            katakana: "チョ",
            romaji: "cho",
            row: "ちゃ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "ちょっと", romaji: "chotto", english: "A moment / A little (稍等/稍微)"),
                KanaExampleWord(japanese: "ちょうど (丁度)", romaji: "choudo", english: "Exactly / Just right (正好/恰好)"),
                KanaExampleWord(japanese: "ちょうしょく (朝食)", romaji: "choushoku", english: "Breakfast (早餐)"),
                KanaExampleWord(japanese: "チョコ", romaji: "choko", english: "Chocolate (巧克力)"),
                KanaExampleWord(japanese: "ちょうさ (調査)", romaji: "chousa", english: "Survey / Investigation (调查)"),
                KanaExampleWord(japanese: "ちょうみりょう (調味料)", romaji: "choumiryou", english: "Seasoning / Condiment (调味料)"),
                KanaExampleWord(japanese: "ちょうじょう (頂上)", romaji: "choujou", english: "Summit / Mountaintop (山顶)")
            ],
            mnemonic: "ち + ょ"
        ),

        KanaItem(
            id: "nya",
            hiragana: "にゃ",
            katakana: "ニャ",
            romaji: "nya",
            row: "にゃ行",
            column: "a",
            exampleWords: [
                KanaExampleWord(japanese: "にゃんこ", romaji: "nyanko", english: "Kitty cat (猫咪)"),
                KanaExampleWord(japanese: "ニャーニャー", romaji: "nyaanyaa", english: "Meow meow sound (喵喵叫)"),
                KanaExampleWord(japanese: "にゃんダフル", romaji: "nyandaful", english: "Meow-nderful (妙极了)"),
                KanaExampleWord(japanese: "こねこ (子猫)", romaji: "koneko", english: "Kitten (小猫)"),
                KanaExampleWord(japanese: "にゃんこカフェ", romaji: "nyanko kafe", english: "Cat cafe (猫咪咖啡馆)"),
                KanaExampleWord(japanese: "にゃんこせんせい", romaji: "nyanko sensei", english: "Master Nyanko (猫咪老师)"),
                KanaExampleWord(japanese: "にゃんの手", romaji: "nyan no te", english: "Cat's helping paw (猫咪借力/帮忙)")
            ],
            mnemonic: "に + ゃ"
        ),

        KanaItem(
            id: "ryo",
            hiragana: "りょ",
            katakana: "リョ",
            romaji: "ryo",
            row: "りゃ行",
            column: "o",
            exampleWords: [
                KanaExampleWord(japanese: "りょうしゅうしょ (領収書)", romaji: "ryoushuusho", english: "Official receipt (发票/收据)"),
                KanaExampleWord(japanese: "りょこう (旅行)", romaji: "ryokou", english: "Travel / Journey (旅游/旅行)"),
                KanaExampleWord(japanese: "りょうり (料理)", romaji: "ryouri", english: "Cooking / Cuisine (料理/菜肴)"),
                KanaExampleWord(japanese: "りょうきん (料金)", romaji: "ryoukin", english: "Fee / Fare (车费/费用)"),
                KanaExampleWord(japanese: "りょうがえ (両替)", romaji: "ryougae", english: "Currency exchange (兑换外币)"),
                KanaExampleWord(japanese: "りょう (量)", romaji: "ryou", english: "Quantity / Portion (份量)"),
                KanaExampleWord(japanese: "りょかん (旅館)", romaji: "ryokan", english: "Traditional Ryokan inn (日式旅馆)")
            ],
            mnemonic: "り + ょ"
        )
    ]
}
