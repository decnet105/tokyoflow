import Foundation

public struct QuarterMilestone: Identifiable {
    public let id: Int
    public let quarterNumber: Int
    public let name: String
    public let nameJa: String
    public let nameZh: String
    public let theme: String
    public let livingSkillsGoal: String
    public let livingSkillsGoalZh: String
    public let mangaGoal: String
    public let mangaGoalZh: String
    public let jfLevel: String
    public let weeksRange: String
    public let icon: String

    public func localizedName(isEnglish: Bool) -> String {
        return isEnglish ? name : nameZh
    }

    public func localizedLivingSkillsGoal(isEnglish: Bool) -> String {
        return isEnglish ? livingSkillsGoal : livingSkillsGoalZh
    }

    public func localizedMangaGoal(isEnglish: Bool) -> String {
        return isEnglish ? mangaGoal : mangaGoalZh
    }
}

public struct OneYearRoadmap {
    public static let quarters: [QuarterMilestone] = [
        QuarterMilestone(
            id: 1,
            quarterNumber: 1,
            name: "Survival & Commute",
            nameJa: "第1四半期：東京サバイバル・通勤とコンビニ",
            nameZh: "第1季度：东京生存实战・通勤与便利店",
            theme: "Core Transit, Kombini, Ramen, Food Orders & Basic Shōnen SFX",
            livingSkillsGoal: "Seamlessly navigate Tokyo trains, buy tickets, handle convenience store cashier dialogues, and order at ramen/izakaya counters.",
            livingSkillsGoalZh: "自如搭乘东京电车与地铁、购买车票充值交通卡、应对便利店收银连环提问、熟练进行拉面与居酒屋点餐。",
            mangaGoal: "Read Shōnen & Slice-of-Life sound effects (ドン, ドキドキ, ざわ) and understand spoken contractions (〜ちゃう, 〜なきゃ).",
            mangaGoalZh: "看懂少年热血与日常番拟声拟态词 (ドン、ドキドキ、ざわ) 并掌握常用口语缩略形 (〜ちゃう、〜なきゃ)。",
            jfLevel: "JF A1 (Starter)",
            weeksRange: "Weeks 1 - 13 (Days 1 - 90)",
            icon: "tram.fill"
        ),
        QuarterMilestone(
            id: 2,
            quarterNumber: 2,
            name: "Tokyo Neighborhoods & Social Living",
            nameJa: "第2四半期：東京の下町・買い物とサービス利用",
            nameZh: "第2季度：东京街区探索・购物与生活服务",
            theme: "Department Stores, Share Bikes, Cafes, Booking, Medical & Rom-Com Dialogue",
            livingSkillsGoal: "Fit clothes in department stores, claim tax refunds, rent Docomo bikes/LUUP, order custom drinks at cafes, and make doctor appointments.",
            livingSkillsGoalZh: "在商场试衣与退税、租赁Docomo共享单车/LUUP、在咖啡馆定制饮品、进行诊所就医预约。",
            mangaGoal: "Read Rom-com & Gourmet manga balloons, understand character emotional nuance, sentence-ending particles, and inner monologue.",
            mangaGoalZh: "阅读恋爱喜剧与美食漫画气泡对话，理解角色情绪语气助词与内心独白。",
            jfLevel: "JF A2 (Waystage)",
            weeksRange: "Weeks 14 - 26 (Days 91 - 180)",
            icon: "bag.fill"
        ),
        QuarterMilestone(
            id: 3,
            quarterNumber: 3,
            name: "City Logistics & Administration",
            nameJa: "第3四半期：役所・郵便・不動産とビジネス基礎",
            nameZh: "第3季度：城市行政实务・邮局与职场基础",
            theme: "Ward Office (区役所), Apartment Hunting, Missed Packages (不在票), Work Chats",
            livingSkillsGoal: "Handle apartment lease terms, redelivery slips, bank account setup, ward office residence registration, and polite workplace greetings (お疲れ様です).",
            livingSkillsGoalZh: "应对租房签约条款、快递不在票再配送申请、区役所住址登记、职场基本寒暄礼仪。",
            mangaGoal: "Read Seinen, Mystery, and Urban Fantasy manga with complex vocabulary and dialect expressions (Kansai-ben / Edokko).",
            mangaGoalZh: "阅读青年悬疑与都市幻想漫画中的复杂词汇与方言口语表达。",
            jfLevel: "JF A2-B1 (Threshold)",
            weeksRange: "Weeks 27 - 39 (Days 181 - 270)",
            icon: "building.2.crop.circle.fill"
        ),
        QuarterMilestone(
            id: 4,
            quarterNumber: 4,
            name: "Tokyo Fluency & Raw Manga Reading",
            nameJa: "第4四半期：東京生活の完全自立と原作漫画の読破",
            nameZh: "第4季度：东京自立流利・生肉漫画原著通读",
            theme: "Deep Cultural Conversations, Emergencies, Contract Negotiations, Full Manga Tankobon",
            livingSkillsGoal: "Navigate medical emergencies, negotiate contract renewals, participate in community matsuri festivals, and converse naturally in mixed registers.",
            livingSkillsGoalZh: "应对突发紧急求医、合同续签协商、融入社区祭典活动，并在各种场合自如切换敬语与简体。",
            mangaGoal: "Read raw, unadapted Japanese manga volumes without furigana or dictionary lookups, appreciating wordplay and authorial voice.",
            mangaGoalZh: "无字典生肉通读无假名注音的原作漫画单行本，领会双关梗与作者原汁原味的语感风格。",
            jfLevel: "JF B1 (Independent)",
            weeksRange: "Weeks 40 - 52 (Days 271 - 365)",
            icon: "book.fill"
        )
    ]
}
