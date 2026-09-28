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
        self.exampleWordEn = exampleWordEn
        self.mnemonic = mnemonic
    }
}

public struct KanaDataManager {
    public static let shared = KanaDataManager()

    public let seionList: [KanaItem] = [
        // A-row (あ行)
        KanaItem(id: "a", hiragana: "あ", katakana: "ア", romaji: "a", row: "あ行", column: "a", exampleWordJa: "ありがとう", exampleWordEn: "Thank you", mnemonic: "Looks like an Apple with a stem"),
        KanaItem(id: "i", hiragana: "い", katakana: "イ", romaji: "i", row: "あ行", column: "i", exampleWordJa: "いぬ (犬)", exampleWordEn: "Dog", mnemonic: "Two needles standing upright"),
        KanaItem(id: "u", hiragana: "う", katakana: "u", romaji: "u", row: "あ行", column: "u", exampleWordJa: "うどん", exampleWordEn: "Udon noodles", mnemonic: "A person bent over diving"),
        KanaItem(id: "e", hiragana: "え", katakana: "エ", romaji: "e", row: "あ行", column: "e", exampleWordJa: "えき (駅)", exampleWordEn: "Train Station", mnemonic: "An energetic running person"),
        KanaItem(id: "o", hiragana: "お", katakana: "オ", romaji: "o", row: "あ行", column: "o", exampleWordJa: "おにぎり", exampleWordEn: "Rice ball", mnemonic: "An origami shape"),

        // Ka-row (か行)
        KanaItem(id: "ka", hiragana: "か", katakana: "カ", romaji: "ka", row: "か行", column: "a", exampleWordJa: "かわいい", exampleWordEn: "Cute", mnemonic: "A person cutting a piece of wood"),
        KanaItem(id: "ki", hiragana: "き", katakana: "キ", romaji: "ki", row: "か行", column: "i", exampleWordJa: "きっぷ (切符)", exampleWordEn: "Train Ticket", mnemonic: "A golden key with two teeth"),
        KanaItem(id: "ku", hiragana: "く", katakana: "ク", romaji: "ku", row: "か行", column: "u", exampleWordJa: "くるま (車)", exampleWordEn: "Car", mnemonic: "A bird's open beak cuckooing"),
        KanaItem(id: "ke", hiragana: "け", katakana: "ケ", romaji: "ke", row: "か行", column: "e", exampleWordJa: "けいたい (携帯)", exampleWordEn: "Cell phone", mnemonic: "A shape of a wooden beer keg"),
        KanaItem(id: "ko", hiragana: "こ", katakana: "コ", romaji: "ko", row: "か行", column: "o", exampleWordJa: "コンビニ", exampleWordEn: "Convenience store", mnemonic: "Two koi fish swimming together"),

        // Sa-row (さ行)
        KanaItem(id: "sa", hiragana: "さ", katakana: "サ", romaji: "sa", row: "さ行", column: "a", exampleWordJa: "さくら (桜)", exampleWordEn: "Cherry blossom", mnemonic: "A signpost smiling"),
        KanaItem(id: "shi", hiragana: "し", katakana: "シ", romaji: "shi", row: "さ行", column: "i", exampleWordJa: "しんじゅく (新宿)", exampleWordEn: "Shinjuku", mnemonic: "A fish hook dipping into water"),
        KanaItem(id: "su", hiragana: "す", katakana: "ス", romaji: "su", row: "さ行", column: "u", exampleWordJa: "すいか (Suica)", exampleWordEn: "IC Card / Watermelon", mnemonic: "A straw swirling in soup"),
        KanaItem(id: "se", hiragana: "せ", katakana: "セ", romaji: "se", row: "さ行", column: "e", exampleWordJa: "せんせい (先生)", exampleWordEn: "Teacher", mnemonic: "A person resting on seven stones"),
        KanaItem(id: "so", hiragana: "そ", katakana: "ソ", romaji: "so", row: "さ行", column: "o", exampleWordJa: "そば", exampleWordEn: "Soba noodles", mnemonic: "A zig-zag stitching sewing needle"),

        // Ta-row (た行)
        KanaItem(id: "ta", hiragana: "た", katakana: "タ", romaji: "ta", row: "た行", column: "a", exampleWordJa: "たこやき", exampleWordEn: "Takoyaki", mnemonic: "Spells out the letters 'ta'"),
        KanaItem(id: "chi", hiragana: "ち", katakana: "チ", romaji: "chi", row: "た行", column: "i", exampleWordJa: "ちかてつ (地下鉄)", exampleWordEn: "Subway", mnemonic: "A cheerleader cheering with pom-poms"),
        KanaItem(id: "tsu", hiragana: "つ", katakana: "ツ", romaji: "tsu", row: "た行", column: "u", exampleWordJa: "つき (月)", exampleWordEn: "Moon", mnemonic: "A giant ocean tsunami wave"),
        KanaItem(id: "te", hiragana: "て", katakana: "テ", romaji: "te", row: "た行", column: "e", exampleWordJa: "てんぷら", exampleWordEn: "Tempura", mnemonic: "A tennis racket handle"),
        KanaItem(id: "to", hiragana: "と", katakana: "ト", romaji: "to", row: "た行", column: "o", exampleWordJa: "とうきょう (東京)", exampleWordEn: "Tokyo", mnemonic: "A thorn sticking into a toe"),

        // Na-row (な行)
        KanaItem(id: "na", hiragana: "な", katakana: "ナ", romaji: "na", row: "な行", column: "a", exampleWordJa: "なつ (夏)", exampleWordEn: "Summer", mnemonic: "A nun praying before a cross"),
        KanaItem(id: "ni", hiragana: "に", katakana: "ニ", romaji: "ni", row: "な行", column: "i", exampleWordJa: "にほん (日本)", exampleWordEn: "Japan", mnemonic: "A needle sewing two threads"),
        KanaItem(id: "nu", hiragana: "ぬ", katakana: "ヌ", romaji: "nu", row: "な行", column: "u", exampleWordJa: "ぬいぐるみ", exampleWordEn: "Plush doll", mnemonic: "Noodles with chopsticks"),
        KanaItem(id: "ne", hiragana: "ね", katakana: "ネ", romaji: "ne", row: "な行", column: "e", exampleWordJa: "ねこ (猫)", exampleWordEn: "Cat", mnemonic: "A cat curled with a looped tail"),
        KanaItem(id: "no", hiragana: "の", katakana: "ノ", romaji: "no", row: "な行", column: "o", exampleWordJa: "のみもの (飲み物)", exampleWordEn: "Beverage", mnemonic: "A forbidden 'No' sign circle"),

        // Ha-row (は行)
        KanaItem(id: "ha", hiragana: "は", katakana: "ハ", romaji: "ha", row: "は行", column: "a", exampleWordJa: "はなび (花火)", exampleWordEn: "Fireworks", mnemonic: "A person wearing a graduation hat"),
        KanaItem(id: "hi", hiragana: "ひ", katakana: "ヒ", romaji: "hi", row: "は行", column: "i", exampleWordJa: "ひかり (光)", exampleWordEn: "Shinkansen / Light", mnemonic: "He has a big smiling chin"),
        KanaItem(id: "fu", hiragana: "ふ", katakana: "フ", romaji: "fu", row: "は行", column: "u", exampleWordJa: "ふじさん (富士山)", exampleWordEn: "Mt. Fuji", mnemonic: "Mount Fuji with slopes"),
        KanaItem(id: "he", hiragana: "へ", katakana: "ヘ", romaji: "he", row: "は行", column: "e", exampleWordJa: "へや (部屋)", exampleWordEn: "Room", mnemonic: "Pointing up to heaven hill"),
        KanaItem(id: "ho", hiragana: "ほ", katakana: "ホ", romaji: "ho", row: "は行", column: "o", exampleWordJa: "ほん (本)", exampleWordEn: "Book", mnemonic: "A horse wearing a party hat"),

        // Ma-row (ま行)
        KanaItem(id: "ma", hiragana: "ま", katakana: "マ", romaji: "ma", row: "ま行", column: "a", exampleWordJa: "まんが (漫画)", exampleWordEn: "Manga", mnemonic: "A magical masquerade mask"),
        KanaItem(id: "mi", hiragana: "み", katakana: "ミ", romaji: "mi", row: "ま行", column: "i", exampleWordJa: "みず (水)", exampleWordEn: "Water", mnemonic: "Looks like the number 21 musical note"),
        KanaItem(id: "mu", hiragana: "む", katakana: "ム", romaji: "mu", row: "ま行", column: "u", exampleWordJa: "むりょう (無料)", exampleWordEn: "Free of charge", mnemonic: "A smiling cow going moo"),
        KanaItem(id: "me", hiragana: "め", katakana: "メ", romaji: "me", row: "ま行", column: "e", exampleWordJa: "めがね (眼鏡)", exampleWordEn: "Glasses", mnemonic: "An almond eye shape"),
        KanaItem(id: "mo", hiragana: "も", katakana: "モ", romaji: "mo", row: "ま行", column: "o", exampleWordJa: "もういちど", exampleWordEn: "Once more", mnemonic: "A fish hook catching more worms"),

        // Ya-row (や行)
        KanaItem(id: "ya", hiragana: "や", katakana: "ヤ", romaji: "ya", row: "や行", column: "a", exampleWordJa: "やま (山)", exampleWordEn: "Mountain", mnemonic: "A yak head with horns"),
        KanaItem(id: "yu", hiragana: "ゆ", katakana: "ユ", romaji: "yu", row: "や行", column: "u", exampleWordJa: "ゆめ (夢)", exampleWordEn: "Dream", mnemonic: "A goldfish swimming in a tub"),
        KanaItem(id: "yo", hiragana: "よ", katakana: "ヨ", romaji: "yo", row: "や行", column: "o", exampleWordJa: "よる (夜)", exampleWordEn: "Night", mnemonic: "A yo-yo dangling from a string"),

        // Ra-row (ら行)
        KanaItem(id: "ra", hiragana: "ら", katakana: "ラ", romaji: "ra", row: "ら行", column: "a", exampleWordJa: "ラーメン", exampleWordEn: "Ramen", mnemonic: "A rabbit sitting upright"),
        KanaItem(id: "ri", hiragana: "り", katakana: "リ", romaji: "ri", row: "ら行", column: "i", exampleWordJa: "りんご (林檎)", exampleWordEn: "Apple", mnemonic: "Two reeds swaying in river"),
        KanaItem(id: "ru", hiragana: "る", katakana: "ル", romaji: "ru", row: "ら行", column: "u", exampleWordJa: "るすばんです (留守番)", exampleWordEn: "Looking after house", mnemonic: "A kangaroo with a looped pouch"),
        KanaItem(id: "re", hiragana: "れ", katakana: "レ", romaji: "re", row: "ら行", column: "e", exampleWordJa: "れっしゃ (列車)", exampleWordEn: "Train", mnemonic: "A person resting against a wall"),
        KanaItem(id: "ro", hiragana: "ろ", katakana: "ロ", romaji: "ro", row: "ら行", column: "o", exampleWordJa: "ろうそく", exampleWordEn: "Candle", mnemonic: "A road looping without a knot"),

        // Wa-row & N (わ行・ん)
        KanaItem(id: "wa", hiragana: "わ", katakana: "ワ", romaji: "wa", row: "わ行", column: "a", exampleWordJa: "わさび", exampleWordEn: "Wasabi", mnemonic: "A graceful swan"),
        KanaItem(id: "wo", hiragana: "を", katakana: "ヲ", romaji: "wo", row: "わ行", column: "o", exampleWordJa: "〜をください", exampleWordEn: "Object Particle", mnemonic: "A person leaping over a hurdle"),
        KanaItem(id: "n", hiragana: "ん", katakana: "ン", romaji: "n", row: "わ行", column: "n", exampleWordJa: "にほん (日本)", exampleWordEn: "Nasal N sound", mnemonic: "Looks like lowercase letter 'n'")
    ]

    public let dakuonList: [KanaItem] = [
        // Ga-row (が行)
        KanaItem(id: "ga", hiragana: "が", katakana: "ガ", romaji: "ga", row: "が行", column: "a", exampleWordJa: "がっこう (学校)", exampleWordEn: "School", mnemonic: "Voiced か"),
        KanaItem(id: "gi", hiragana: "ぎ", katakana: "ギ", romaji: "gi", row: "が行", column: "i", exampleWordJa: "ぎゅうどん (牛丼)", exampleWordEn: "Beef bowl", mnemonic: "Voiced き"),
        KanaItem(id: "gu", hiragana: "ぐ", katakana: "グ", romaji: "gu", row: "が行", column: "u", exampleWordJa: "ぐんま (群馬)", exampleWordEn: "Gunma", mnemonic: "Voiced く"),
        KanaItem(id: "ge", hiragana: "げ", katakana: "ゲ", romaji: "ge", row: "が行", column: "e", exampleWordJa: "げんき (元気)", exampleWordEn: "Energetic", mnemonic: "Voiced け"),
        KanaItem(id: "go", hiragana: "ご", katakana: "ゴ", romaji: "go", row: "が行", column: "o", exampleWordJa: "ごはん (ご飯)", exampleWordEn: "Rice / Meal", mnemonic: "Voiced こ"),

        // Za-row (ざ行)
        KanaItem(id: "za", hiragana: "ざ", katakana: "ザ", romaji: "za", row: "ざ行", column: "a", exampleWordJa: "ざっし (雑誌)", exampleWordEn: "Magazine", mnemonic: "Voiced さ"),
        KanaItem(id: "ji", hiragana: "じ", katakana: "ジ", romaji: "ji", row: "ざ行", column: "i", exampleWordJa: "じかん (時間)", exampleWordEn: "Time", mnemonic: "Voiced し"),
        KanaItem(id: "zu", hiragana: "ず", katakana: "ズ", romaji: "zu", row: "ざ行", column: "u", exampleWordJa: "ずっと", exampleWordEn: "Always / Far", mnemonic: "Voiced す"),
        KanaItem(id: "ze", hiragana: "ぜ", katakana: "ゼ", romaji: "ze", row: "ざ行", column: "e", exampleWordJa: "ぜんぶ (全部)", exampleWordEn: "All / Everything", mnemonic: "Voiced せ"),
        KanaItem(id: "zo", hiragana: "ぞ", katakana: "ゾ", romaji: "zo", row: "ざ行", column: "o", exampleWordJa: "ぞう (象)", exampleWordEn: "Elephant", mnemonic: "Voiced そ"),

        // Da-row (だ行)
        KanaItem(id: "da", hiragana: "だ", katakana: "ダ", romaji: "da", row: "だ行", column: "a", exampleWordJa: "だいじょうぶ (大丈夫)", exampleWordEn: "All right / OK", mnemonic: "Voiced た"),
        KanaItem(id: "de", hiragana: "で", katakana: "デ", romaji: "de", row: "だ行", column: "e", exampleWordJa: "でんしゃ (電車)", exampleWordEn: "Electric train", mnemonic: "Voiced て"),
        KanaItem(id: "do", hiragana: "ど", katakana: "ド", romaji: "do", row: "だ行", column: "o", exampleWordJa: "どこ (何処)", exampleWordEn: "Where", mnemonic: "Voiced と"),

        // Ba-row (ば行)
        KanaItem(id: "ba", hiragana: "ば", katakana: "バ", romaji: "ba", row: "ば行", column: "a", exampleWordJa: "ばしょ (場所)", exampleWordEn: "Place", mnemonic: "Voiced は"),
        KanaItem(id: "bi", hiragana: "び", katakana: "ビ", romaji: "bi", row: "ば行", column: "i", exampleWordJa: "ビール", exampleWordEn: "Beer", mnemonic: "Voiced ひ"),
        KanaItem(id: "bu", hiragana: "ぶ", katakana: "ブ", romaji: "bu", row: "ば行", column: "u", exampleWordJa: "ぶんか (文化)", exampleWordEn: "Culture", mnemonic: "Voiced ふ"),
        KanaItem(id: "be", hiragana: "べ", katakana: "ベ", romaji: "be", row: "ば行", column: "e", exampleWordJa: "べんり (便利)", exampleWordEn: "Convenient", mnemonic: "Voiced へ"),
        KanaItem(id: "bo", hiragana: "ぼ", katakana: "ボ", romaji: "bo", row: "ば行", column: "o", exampleWordJa: "ぼく (僕)", exampleWordEn: "I / Me", mnemonic: "Voiced ほ"),

        // Pa-row (ぱ行)
        KanaItem(id: "pa", hiragana: "ぱ", katakana: "パ", romaji: "pa", row: "ぱ行", column: "a", exampleWordJa: "パン", exampleWordEn: "Bread", mnemonic: "Plosive は"),
        KanaItem(id: "pi", hiragana: "ぴ", katakana: "ピ", romaji: "pi", row: "ぱ行", column: "i", exampleWordJa: "ピンク", exampleWordEn: "Pink", mnemonic: "Plosive ひ"),
        KanaItem(id: "pu", hiragana: "ぷ", katakana: "プ", romaji: "pu", row: "ぱ行", column: "u", exampleWordJa: "ぷりん (プリン)", exampleWordEn: "Pudding", mnemonic: "Plosive ふ"),
        KanaItem(id: "pe", hiragana: "ぺ", katakana: "ペ", romaji: "pe", row: "ぱ行", column: "e", exampleWordJa: "ペン", exampleWordEn: "Pen", mnemonic: "Plosive へ"),
        KanaItem(id: "po", hiragana: "ぽ", katakana: "ポ", romaji: "po", row: "ぱ行", column: "o", exampleWordJa: "ポスト", exampleWordEn: "Postbox", mnemonic: "Plosive ほ")
    ]

    public let yoonList: [KanaItem] = [
        KanaItem(id: "kya", hiragana: "きゃ", katakana: "キャ", romaji: "kya", row: "きゃ行", column: "a", exampleWordJa: "きゃく (客)", exampleWordEn: "Customer / Guest", mnemonic: "き + ゃ"),
        KanaItem(id: "kyu", hiragana: "きゅ", katakana: "キュ", romaji: "kyu", row: "きゃ行", column: "u", exampleWordJa: "きゅうこう (急行)", exampleWordEn: "Express train", mnemonic: "き + ゅ"),
        KanaItem(id: "kyo", hiragana: "きょ", katakana: "キョ", romaji: "kyo", row: "きゃ行", column: "o", exampleWordJa: "きょう (今日)", exampleWordEn: "Today", mnemonic: "き + ょ"),

        KanaItem(id: "sha", hiragana: "しゃ", katakana: "シャ", romaji: "sha", row: "しゃ行", column: "a", exampleWordJa: "しゃしん (写真)", exampleWordEn: "Photo", mnemonic: "し + ゃ"),
        KanaItem(id: "shu", hiragana: "しゅ", katakana: "シュ", romaji: "shu", row: "しゃ行", column: "u", exampleWordJa: "しゅうでん (終電)", exampleWordEn: "Last train", mnemonic: "し + ゅ"),
        KanaItem(id: "sho", hiragana: "しょ", katakana: "ショ", romaji: "sho", row: "しゃ行", column: "o", exampleWordJa: "しょうひひん (消費品)", exampleWordEn: "Goods", mnemonic: "し + ょ"),

        KanaItem(id: "cha", hiragana: "ちゃ", katakana: "チャ", romaji: "cha", row: "ちゃ行", column: "a", exampleWordJa: "おちゃ (お茶)", exampleWordEn: "Green tea", mnemonic: "ち + ゃ"),
        KanaItem(id: "chu", hiragana: "ちゅ", katakana: "チュ", romaji: "chu", row: "ちゃ行", column: "u", exampleWordJa: "ちゅうもん (注文)", exampleWordEn: "Order", mnemonic: "ち + ゅ"),
        KanaItem(id: "cho", hiragana: "ちょ", katakana: "チョ", romaji: "cho", row: "ちゃ行", column: "o", exampleWordJa: "ちょっと", exampleWordEn: "A little / Excuse me", mnemonic: "ち + ょ"),

        KanaItem(id: "nya", hiragana: "にゃ", katakana: "ニャ", romaji: "nya", row: "にゃ行", column: "a", exampleWordJa: "にゃんこ", exampleWordEn: "Kitty cat", mnemonic: "に + ゃ"),
        KanaItem(id: "ryo", hiragana: "りょ", katakana: "リョ", romaji: "ryo", row: "りゃ行", column: "o", exampleWordJa: "りょうしゅうしょ (領収書)", exampleWordEn: "Receipt", mnemonic: "り + ょ")
    ]
}
