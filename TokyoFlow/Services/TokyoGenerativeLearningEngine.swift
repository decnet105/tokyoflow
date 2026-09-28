import Foundation
import Combine

public class TokyoGenerativeLearningEngine: ObservableObject {
    public static let shared = TokyoGenerativeLearningEngine()

    @Published public var currentPlan: TokyoDestinationPlan? = nil
    @Published public var isGenerating: Bool = false
    @Published public var selectedPresetId: String = "shibuya"

    public let presetDestinations: [(id: String, name: String, ja: String, district: String, icon: String, tag: String)] = [
        ("shibuya", "Shibuya Crossing & Hachiko", "渋谷スクランブル交差点", "Shibuya (渋谷)", "figure.walk", "Wayfinding & Street"),
        ("akiba", "Akihabara Anime & Figures", "秋葉原アニメ街", "Akihabara (秋葉原)", "sparkles.tv.fill", "Merch & Questions"),
        ("shinjuku", "Shinjuku Omoide Yokocho", "新宿思い出横丁", "Shinjuku (新宿)", "wineglass.fill", "Ordering & Toast"),
        ("asakusa", "Sensoji Temple & Food Stalls", "浅草寺・仲見世通り", "Asakusa (浅草)", "building.columns.fill", "Prayers & Snacks"),
        ("ginza", "Ginza Department Stores", "銀座デパート免税", "Ginza (銀座)", "bag.fill", "Tax-Free & Sizing"),
        ("tsukiji", "Tsukiji Outer Seafood Market", "豊洲・築地海鮮市場", "Toyosu (豊洲)", "fork.knife", "Dining & Line-up"),
        ("roppongi", "Roppongi Hills Night View", "六本木ヒルズ展望台", "Roppongi (六本木)", "moon.stars.fill", "Tickets & Sightseeing"),
        ("haneda", "Haneda Airport Monorail", "羽田空港モノレール", "Haneda (羽田)", "airplane.arrival", "Transit Navigation")
    ]

    private init() {
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
                destinationName: prompt.isEmpty ? "Tokyo Free Exploration" : prompt,
                destinationJa: "東京カスタム探索",
                district: "Tokyo Area (東京)",
                categoryIcon: "sparkles",
                tag: "AI Real-Time Generation",
                overview: "Dynamically generated survival phrases, real-life roleplay dialogues, and cultural etiquette for your visit to '\(prompt)'.",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "すみません、ここはどこですか？",
                        furigana: "すみません、ここは どこですか？",
                        romaji: "sumimasen, koko wa doko desu ka?",
                        english: "Excuse me, where is this place?",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Fastest phrase to get orientation when lost in Tokyo.",
                        audioKey: "すみません"
                    ),
                    GenerativePhrase(
                        japanese: "これをお願いします。",
                        furigana: "これを おねがいします。",
                        romaji: "kore o onegaishimasu.",
                        english: "This one, please. / I'd like this.",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Universal phrase when pointing at menus, goods, or ticket screens.",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "クレジットカードは使えますか？",
                        furigana: "くれじっとかーどは つかえますか？",
                        romaji: "kurejitto kaado wa tsukaemasu ka?",
                        english: "Do you accept credit cards?",
                        pitchAccent: "③ Tail-high (Odaka)",
                        situationNote: "Confirm payment methods before checkout.",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "Staff", speakerRole: "Store Clerk", japanese: "いらっしゃいませ！何かお探しですか？", furigana: "いらっしゃいませ！なにか おさがしですか？", english: "Welcome! Are you looking for anything specific?", isUser: false),
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Traveler", japanese: "これと同じものはありますか？", furigana: "これと おなじものは ありますか？", english: "Do you have something identical to this?", isUser: true),
                    GenerativeDialogueTurn(speaker: "Staff", speakerRole: "Store Clerk", japanese: "かしこまりました。こちらへどうぞ！", furigana: "かしこまりました。こちらへ どうぞ！", english: "Certainly! Right this way, please.", isUser: false)
                ],
                culturalTips: [
                    "Keep your voice moderate in public places in Japan to avoid disturbing others.",
                    "Show your passport at checkout in tax-free shops for an instant 10% consumption tax refund.",
                    "Starting your request with a polite 'Sumimasen' (Excuse me) will always get friendly help."
                ],
                challengeMission: "Ask a local clerk a question in '\(prompt)' and thank them with 'Arigatō gozaimasu'!"
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
                destinationName: "Shibuya Crossing & Hachiko",
                destinationJa: "渋谷スクランブル交差点・ハチ公前",
                district: "Shibuya (渋谷)",
                categoryIcon: "figure.walk",
                tag: "Iconic Landmarks & Wayfinding",
                overview: "The world's busiest pedestrian intersection. Learn how to ask for the Hachiko statue exit, SHIBUYA SKY entrance, and photo spots.",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "ハチ公口はどちらですか？",
                        furigana: "はちこうぐちは どちらですか？",
                        romaji: "hachikou guchi wa dochira desu ka?",
                        english: "Which way is the Hachiko Exit?",
                        pitchAccent: "② Nakadaka",
                        situationNote: "Crucial question when navigating the vast Shibuya underground labyrinth.",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "写真を撮っていただけますか？",
                        furigana: "しゃしんを とって いただけますか？",
                        romaji: "shashin o totte itadakemasu ka?",
                        english: "Could you take a photo for us, please?",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Polite natural way to ask a passerby for a photo at landmarks.",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "スクランブルスクエアへはどう行けばいいですか？",
                        furigana: "すくらんぶる すくえあへは どう いけば いいですか？",
                        romaji: "sukuranburu sukuea e wa dou ikeba ii desu ka?",
                        english: "How can I get to Shibuya Scramble Square?",
                        pitchAccent: "① Atamadaka",
                        situationNote: "Ask directions to the observation deck skyscraper.",
                        audioKey: "すみません"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Traveler", japanese: "すみません、ハチ公の像はどこにありますか？", furigana: "すみません、はちこうの ぞうは どこに ありますか？", english: "Excuse me, where is the Hachiko statue?", isUser: true),
                    GenerativeDialogueTurn(speaker: "Passerby", speakerRole: "Tokyo Local", japanese: "あそこの緑の電車の向かい側ですよ！", furigana: "あそこの みどりの でんしゃの むかいがわですよ！", english: "It's right across from that green retired train car over there!", isUser: false),
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Traveler", japanese: "ありがとうございます！助かりました。", furigana: "ありがとうございます！たすかりました。", english: "Thank you so much! That was a big help.", isUser: true)
                ],
                culturalTips: [
                    "Green light lasts only about 45 seconds at Shibuya Crossing. Avoid stopping mid-scramble to block pedestrian flow.",
                    "Follow the yellow ceiling signs for 'ハチ公改札' (Hachiko Gate) before exiting the gates."
                ],
                challengeMission: "Ask a friendly local near Hachiko to take your photo and express gratitude in natural Japanese!"
            )

        case "akiba":
            return TokyoDestinationPlan(
                id: "akiba",
                destinationName: "Akihabara Anime & Figures",
                destinationJa: "秋葉原アニメ街・フィギュア探訪",
                district: "Akihabara (秋葉原)",
                categoryIcon: "sparkles.tv.fill",
                tag: "Anime Merch & Blind Boxes",
                overview: "The holy land of anime, gaming, and electronics. Master asking clerks about limited edition perks, figure condition, and checkout tax refunds.",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "これの在庫はまだありますか？",
                        furigana: "これの ざいこは まだ ありますか？",
                        romaji: "kore no zaiko wa mada arimasu ka?",
                        english: "Do you still have stock of this item in the back?",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Ask if they have brand new unopened stock of a display item.",
                        audioKey: "あります"
                    ),
                    GenerativePhrase(
                        japanese: "限定特典は付きますか？",
                        furigana: "げんてい とくてんは つきますか？",
                        romaji: "gentei tokuten wa tsukimasu ka?",
                        english: "Does this come with the limited edition bonus perk?",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Check for pre-order or purchase illustration postcards / acrylic stands.",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "箱を開けて中を確認してもいいですか？",
                        furigana: "はこを あけて なかを かくにんしても いいですか？",
                        romaji: "hako o akete naka o kakunin shitemo ii desu ka?",
                        english: "May I open the box to check the condition inside?",
                        pitchAccent: "① Atamadaka",
                        situationNote: "Crucial inspection permission at second-hand / hobby shops.",
                        audioKey: "いいですよ"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Anime Fan", japanese: "すみません、このフィギュアの未開封品はありますか？", furigana: "すみません、この ふぃぎゅあの みかいふうひんは ありますか？", english: "Excuse me, do you have an unopened new copy of this figure?", isUser: true),
                    GenerativeDialogueTurn(speaker: "Staff", speakerRole: "Anime Shop Clerk", japanese: "少々お待ちください……はい、ラスト1点ございます！", furigana: "しょうしょう おまちください……はい、らすと いってん ございます！", english: "Just a moment, please... Yes, we have our last one in stock!", isUser: false),
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Anime Fan", japanese: "よかった！これをお願いします。", furigana: "よかった！これを おねがいします。", english: "Great! I'll take this one, please.", isUser: true)
                ],
                culturalTips: [
                    "Rental display showcase items labeled '現状渡し' (As-is) are sold by individual collectors and cannot be returned.",
                    "Tax-free shopping requires purchases over ¥5,000 (pre-tax) and an original physical passport."
                ],
                challengeMission: "Hear the clerk say 'ラスト1点' (Last one in stock) and complete your tax-free purchase!"
            )

        case "shinjuku":
            return TokyoDestinationPlan(
                id: "shinjuku",
                destinationName: "Shinjuku Omoide Yokocho",
                destinationJa: "新宿思い出横丁・昭和風情",
                district: "Shinjuku (新宿)",
                categoryIcon: "wineglass.fill",
                tag: "Yakitori & Izakaya Culture",
                overview: "The most atmospheric Showa-era alley in west Shinjuku. Master ordering the mandatory first round of beer, salt vs tare sauce, and Otoshi appetizers.",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "とりあえず生ビール二つ！",
                        furigana: "とりあえず なまびーる ふたつ！",
                        romaji: "toriaezu nama biiru futatsu!",
                        english: "Two draft beers to start, please!",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "The universal golden opening line immediately upon sitting down at an Izakaya.",
                        audioKey: "乾杯"
                    ),
                    GenerativePhrase(
                        japanese: "焼き鳥盛り合わせを塩でお願いします。",
                        furigana: "やきとり もりあわせを しおで おねがいします。",
                        romaji: "yakitori moriawase o shio de onegaishimasu.",
                        english: "Assorted grilled chicken skewers, seasoned with salt, please.",
                        pitchAccent: "③ Odaka",
                        situationNote: "Salt (shio) lets you savor the authentic taste of grilled yakitori.",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "お会計をお願いします。",
                        furigana: "おかいけいを おねがいします。",
                        romaji: "okaikei o onegaishimasu.",
                        english: "Check / Bill, please.",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Raise your hand gently at your seat to request the final bill.",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "Master", speakerRole: "Izakaya Owner", japanese: "いらっしゃい！お飲み物は何にしますか？", furigana: "いらっしゃい！おのみものは なにに しますか？", english: "Welcome! What would you like to drink to start?", isUser: false),
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Customer", japanese: "とりあえず生中と、レモンサワーをください！", furigana: "とりあえず なまちゅうと、れもんさわーを ください！", english: "A medium draft beer and a lemon sour to start, please!", isUser: true),
                    GenerativeDialogueTurn(speaker: "Master", speakerRole: "Izakaya Owner", japanese: "あいよ！すぐにお持ちします！", furigana: "あいよ！すぐに おもちします！", english: "Right away! Coming right up!", isUser: false)
                ],
                culturalTips: [
                    "Izakayas automatically serve a small appetizer called 'Otoshi' (お通し), which acts as a standard table charge (¥300~¥500).",
                    "When clinking glasses for a toast ('Kanpai!'), placing the rim of your glass slightly lower than your host's shows deep respect."
                ],
                challengeMission: "Order 'Toriaezu nama' without opening the menu and toast with your friends like a true Tokyoite!"
            )

        default:
            return TokyoDestinationPlan(
                id: presetId,
                destinationName: "Sensoji Temple & Nakamise Street",
                destinationJa: "浅草寺・雷門・下町散策",
                district: "Asakusa (浅草)",
                categoryIcon: "building.columns.fill",
                tag: "Temple Etiquette & Local Snacks",
                overview: "Tokyo's oldest and most sacred Buddhist temple. Learn how to draw Omikuji fortune slips, toss 5-yen coins, and buy hot Ningyo-yaki cakes.",
                survivalPhrases: [
                    GenerativePhrase(
                        japanese: "おみくじはどこで引けますか？",
                        furigana: "おみくじは どこで ひけますか？",
                        romaji: "omikuji wa doko de hikemasu ka?",
                        english: "Where can I draw a fortune slip (Omikuji)?",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Look for the ¥100 honor-system coin box in the temple courtyard.",
                        audioKey: "こんにちは"
                    ),
                    GenerativePhrase(
                        japanese: "焼きたての人形焼をひとつください。",
                        furigana: "やきたての にんぎょうやきを ひとつ ください。",
                        romaji: "yakitate no ningyouyaki o hitotsu kudasai.",
                        english: "One freshly baked Ningyo-yaki cake, please.",
                        pitchAccent: "⓪ Flat (Heiban)",
                        situationNote: "Order traditional doll-shaped red bean sponge cakes along Nakamise street.",
                        audioKey: "お願いします"
                    ),
                    GenerativePhrase(
                        japanese: "このお守りのご利益は何ですか？",
                        furigana: "この おまもりの ごりやくは なんですか？",
                        romaji: "kono omamori no goriyaku wa nan desu ka?",
                        english: "What blessing is this amulet (Omamori) for?",
                        pitchAccent: "② Nakadaka",
                        situationNote: "Inquire about protective charms for health, romance, or academic success.",
                        audioKey: "ありがとうございます"
                    )
                ],
                scenarioDialogue: [
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Visitor", japanese: "すみません、お参りの作法を教えていただけますか？", furigana: "すみません、おまいりの さほうを おしえて いただけますか？", english: "Excuse me, could you teach me the proper way to pray here?", isUser: true),
                    GenerativeDialogueTurn(speaker: "Monk", speakerRole: "Temple Guide", japanese: "お賽銭を入れて、静かに手を合わせて一礼してください。", furigana: "おさいせんを いれて、しずかに てを あわせて いちれい してください。", english: "Toss a coin into the offering box, quietly press your palms together, and bow once.", isUser: false),
                    GenerativeDialogueTurn(speaker: "You", speakerRole: "Visitor", japanese: "わかりました。ありがとうございます。", furigana: "わかりました。ありがとうございます。", english: "Understood! Thank you very much.", isUser: true)
                ],
                culturalTips: [
                    "At Buddhist temples (like Sensoji), bow with hands pressed together ('Gasshō'). Do NOT clap your hands (clapping is for Shinto Shrines only).",
                    "If you draw a 'Bad Fortune' (Kyou), tie the slip to the designated metal racks to leave bad luck behind."
                ],
                challengeMission: "Toss a 5-yen coin ('Go-en' meaning good destiny) and complete an authentic prayer at Sensoji!"
            )
        }
    }
}
