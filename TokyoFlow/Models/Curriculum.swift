import Foundation

public struct QuarterMilestone: Identifiable {
    public let id: Int
    public let quarterNumber: Int
    public let name: String
    public let nameJa: String
    public let theme: String
    public let livingSkillsGoal: String
    public let mangaGoal: String
    public let jfLevel: String
    public let weeksRange: String
    public let icon: String
}

public struct OneYearRoadmap {
    public static let quarters: [QuarterMilestone] = [
        QuarterMilestone(
            id: 1,
            quarterNumber: 1,
            name: "Survival & Commute",
            nameJa: "第1四半期：東京サバイバル・通勤とコンビニ",
            theme: "Core Transit, Kombini, Ramen, Food Orders & Basic Shōnen SFX",
            livingSkillsGoal: "Seamlessly navigate Tokyo trains, buy tickets, handle convenience store cashier dialogues, and order at ramen/izakaya counters.",
            mangaGoal: "Read Shōnen & Slice-of-Life sound effects (ドン, ドキドキ, ざわ) and understand spoken contractions (〜ちゃう, 〜なきゃ).",
            jfLevel: "JF A1 (Starter)",
            weeksRange: "Weeks 1 - 13 (Days 1 - 90)",
            icon: "tram.fill"
        ),
        QuarterMilestone(
            id: 2,
            quarterNumber: 2,
            name: "Tokyo Neighborhoods & Social Living",
            nameJa: "第2四半期：東京の下町・買い物とサービス利用",
            theme: "Department Stores, Share Bikes, Cafes, Booking, Medical & Rom-Com Dialogue",
            livingSkillsGoal: "Fit clothes in department stores, claim tax refunds, rent Docomo bikes/LUUP, order custom drinks at cafes, and make doctor appointments.",
            mangaGoal: "Read Rom-com & Gourmet manga balloons, understand character emotional nuance, sentence-ending particles, and inner monologue.",
            jfLevel: "JF A2 (Waystage)",
            weeksRange: "Weeks 14 - 26 (Days 91 - 180)",
            icon: "bag.fill"
        ),
        QuarterMilestone(
            id: 3,
            quarterNumber: 3,
            name: "City Logistics & Administration",
            nameJa: "第3四半期：役所・郵便・不動産とビジネス基礎",
            theme: "Ward Office (区役所), Apartment Hunting, Missed Packages (不在票), Work Chats",
            livingSkillsGoal: "Handle apartment lease terms, redelivery slips, bank account setup, ward office residence registration, and polite workplace greetings (お疲れ様です).",
            mangaGoal: "Read Seinen, Mystery, and Urban Fantasy manga with complex vocabulary and dialect expressions (Kansai-ben / Edokko).",
            jfLevel: "JF A2-B1 (Threshold)",
            weeksRange: "Weeks 27 - 39 (Days 181 - 270)",
            icon: "building.2.crop.circle.fill"
        ),
        QuarterMilestone(
            id: 4,
            quarterNumber: 4,
            name: "Tokyo Fluency & Raw Manga Reading",
            nameJa: "第4四半期：東京生活の完全自立と原作漫画の読破",
            theme: "Deep Cultural Conversations, Emergencies, Contract Negotiations, Full Manga Tankobon",
            livingSkillsGoal: "Navigate medical emergencies, negotiate contract renewals, participate in community matsuri festivals, and converse naturally in mixed registers.",
            mangaGoal: "Read raw, unadapted Japanese manga volumes without furigana or dictionary lookups, appreciating wordplay and authorial voice.",
            jfLevel: "JF B1 (Independent)",
            weeksRange: "Weeks 40 - 52 (Days 271 - 365)",
            icon: "book.fill"
        )
    ]
}
