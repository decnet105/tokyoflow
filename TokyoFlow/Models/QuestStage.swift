import Foundation

public struct QuestStage: Identifiable, Codable {
    public let id: Int
    public let stageNumber: Int
    public let worldId: Int
    public let worldName: String
    public let worldNameJa: String
    public let stageTitle: String
    public let stageTitleJa: String
    public let missionType: String // scenario, dojo_battle, manga_lab, audio_listening, boss_trial
    public let targetContentId: String
    public let jfLevel: String
    public let targetSkill: String
    public let iconName: String
    public let xpReward: Int

    public var isBossStage: Bool {
        return missionType == "boss_trial"
    }
}

public struct TokyoQuestWorld: Identifiable {
    public let id: Int
    public let worldNumber: Int
    public let name: String
    public let nameJa: String
    public let district: String
    public let jfLevel: String
    public let themeColorHex: String
    public let stages: [QuestStage]
}

public struct QuestProgressManager {
    public static let worlds: [TokyoQuestWorld] = [
        TokyoQuestWorld(
            id: 1,
            worldNumber: 1,
            name: "Shinjuku Station Labyrinth",
            nameJa: "ワールド1：新宿駅迷宮・切符とICカード",
            district: "Shinjuku",
            jfLevel: "JF A1",
            themeColorHex: "#0EA5E9",
            stages: [
                QuestStage(id: 1, stageNumber: 1, worldId: 1, worldName: "Shinjuku", worldNameJa: "新宿", stageTitle: "Yamanote Line Commute", stageTitleJa: "山手線の乗り方と切符購入", missionType: "scenario", targetContentId: "scenario_01_morning_train", jfLevel: "A1", targetSkill: "Transit & IC Card", iconName: "tram.fill", xpReward: 100),
                QuestStage(id: 2, stageNumber: 2, worldId: 1, worldName: "Shinjuku", worldNameJa: "新宿", stageTitle: "Train Approaching Chime", stageTitleJa: "接近放送と発車メロディ", missionType: "audio_listening", targetContentId: "announcement_01_yamanote_arrival", jfLevel: "A1", targetSkill: "Station Ear Training", iconName: "headphones", xpReward: 120),
                QuestStage(id: 3, stageNumber: 3, worldId: 1, worldName: "Shinjuku", worldNameJa: "新宿", stageTitle: "Shinjuku Gate Rush (Boss)", stageTitleJa: "改札ボス戦：タッチ失敗と窓口精算", missionType: "boss_trial", targetContentId: "scenario_01_morning_train", jfLevel: "A1", targetSkill: "Rush Hour Barrier Defense", iconName: "shield.fill", xpReward: 250)
            ]
        ),
        TokyoQuestWorld(
            id: 2,
            worldNumber: 2,
            name: "Shibuya Kombini Ninja",
            nameJa: "ワールド2：渋谷コンビニ忍者・連環5問",
            district: "Shibuya",
            jfLevel: "JF A1",
            themeColorHex: "#F59E0B",
            stages: [
                QuestStage(id: 4, stageNumber: 4, worldId: 2, worldName: "Shibuya", worldNameJa: "渋谷", stageTitle: "7-Eleven Morning Checkout", stageTitleJa: "コンビニ朝食：お弁当・袋・決済", missionType: "scenario", targetContentId: "scenario_02_kombini_morning", jfLevel: "A1", targetSkill: "Kombini Checkout", iconName: "cart.fill", xpReward: 100),
                QuestStage(id: 5, stageNumber: 5, worldId: 2, worldName: "Shibuya", worldNameJa: "渋谷", stageTitle: "FamilyMart Jingle Master", stageTitleJa: "ファミマ入店チャイムと店員挨拶", missionType: "audio_listening", targetContentId: "announcement_03_familymart_chime", jfLevel: "A1", targetSkill: "Store Audio Cues", iconName: "speaker.wave.2.fill", xpReward: 120),
                QuestStage(id: 6, stageNumber: 6, worldId: 2, worldName: "Shibuya", worldNameJa: "渋谷", stageTitle: "Kombini 5-Question Barrage (Boss)", stageTitleJa: "道場決戦：早口レジ連環5問3秒撃破", missionType: "boss_trial", targetContentId: "dojo_01_kombini_5_questions", jfLevel: "A1", targetSkill: "Speed Cashier Defense", iconName: "flame.fill", xpReward: 300)
            ]
        ),
        TokyoQuestWorld(
            id: 3,
            worldNumber: 3,
            name: "Ikebukuro Ramen & Gourmet",
            nameJa: "ワールド3：池袋ラーメン横丁・お好み暗号",
            district: "Ikebukuro",
            jfLevel: "JF A2",
            themeColorHex: "#EF4444",
            stages: [
                QuestStage(id: 7, stageNumber: 7, worldId: 3, worldName: "Ikebukuro", worldNameJa: "池袋", stageTitle: "Ramen Vending Machine", stageTitleJa: "家系食券機とお好み注文", missionType: "scenario", targetContentId: "scenario_03_ramen_ticket_machine", jfLevel: "A2", targetSkill: "Food Ticket Ordering", iconName: "fork.knife", xpReward: 150),
                QuestStage(id: 8, stageNumber: 8, worldId: 3, worldName: "Ikebukuro", worldNameJa: "池袋", stageTitle: "Gourmet Tasting SFX", stageTitleJa: "サクサク・ジュワッ！食レポ擬音", missionType: "manga_lab", targetContentId: "manga_03_gourmet_tokyo_food", jfLevel: "A2", targetSkill: "Texture Onomatopoeia", iconName: "sparkles", xpReward: 150),
                QuestStage(id: 9, stageNumber: 9, worldId: 3, worldName: "Ikebukuro", worldNameJa: "池袋", stageTitle: "Kaedama Refill Trial (Boss)", stageTitleJa: "大将戦：お好み暗号と替え玉バリカタ", missionType: "boss_trial", targetContentId: "dojo_02_ramen_cipher", jfLevel: "A2", targetSkill: "Chef Customization Cipher", iconName: "trophy.fill", xpReward: 350)
            ]
        ),
        TokyoQuestWorld(
            id: 4,
            worldNumber: 4,
            name: "Akihabara Manga & Slang Lab",
            nameJa: "ワールド4：秋葉原マンガ聖地・少年バトル擬音",
            district: "Akihabara",
            jfLevel: "JF A2",
            themeColorHex: "#8B5CF6",
            stages: [
                QuestStage(id: 10, stageNumber: 10, worldId: 4, worldName: "Akihabara", worldNameJa: "秋葉原", stageTitle: "Shōnen Battle SFX", stageTitleJa: "ドドド！バトル擬音と口語短縮", missionType: "manga_lab", targetContentId: "manga_01_shonen_battle_sfx", jfLevel: "A2", targetSkill: "Manga SFX Decoding", iconName: "book.pages.fill", xpReward: 160),
                QuestStage(id: 11, stageNumber: 11, worldId: 4, worldName: "Akihabara", worldNameJa: "秋葉原", stageTitle: "School Rom-Com Balloons", stageTitleJa: "日常学園ラブコメ：胸の鼓動とスラング", missionType: "manga_lab", targetContentId: "manga_02_slice_of_life_romcom", jfLevel: "A2", targetSkill: "Dialogue & Inner Monologue", iconName: "heart.text.square.fill", xpReward: 160),
                QuestStage(id: 12, stageNumber: 12, worldId: 4, worldName: "Akihabara", worldNameJa: "秋葉原", stageTitle: "Raw Tankobon Duel (Boss)", stageTitleJa: "ボス戦：原作単行本フリガナなし読破", missionType: "boss_trial", targetContentId: "manga_01_shonen_battle_sfx", jfLevel: "A2", targetSkill: "Raw Manga Comprehension", iconName: "bolt.shield.fill", xpReward: 400)
            ]
        ),
        TokyoQuestWorld(
            id: 5,
            worldNumber: 5,
            name: "Ginza Luxury & Tax-Free",
            nameJa: "ワールド5：銀座デパート・免税とサイズ確認",
            district: "Ginza",
            jfLevel: "JF A2-B1",
            themeColorHex: "#EC4899",
            stages: [
                QuestStage(id: 13, stageNumber: 13, worldId: 5, worldName: "Ginza", worldNameJa: "銀座", stageTitle: "Fitting Room Etiquette", stageTitleJa: "試着・サイズ確認・免税手続き", missionType: "scenario", targetContentId: "scenario_06_department_store_taxfree", jfLevel: "A2", targetSkill: "Shopping & Sizing", iconName: "bag.fill", xpReward: 180),
                QuestStage(id: 14, stageNumber: 14, worldId: 5, worldName: "Ginza", worldNameJa: "銀座", stageTitle: "Metro Ginza Line Chimes", stageTitleJa: "銀座線ドア閉め・駆け込み乗車警告", missionType: "audio_listening", targetContentId: "announcement_02_train_door_closing", jfLevel: "A2", targetSkill: "Metro Audio Navigation", iconName: "headphones", xpReward: 180),
                QuestStage(id: 15, stageNumber: 15, worldId: 5, worldName: "Ginza", worldNameJa: "銀座", stageTitle: "Tax-Free Counter Master (Boss)", stageTitleJa: "免税カウンター：パスポートと還付", missionType: "boss_trial", targetContentId: "scenario_06_department_store_taxfree", jfLevel: "A2-B1", targetSkill: "Tax Refund Fluency", iconName: "crown.fill", xpReward: 450)
            ]
        ),
        TokyoQuestWorld(
            id: 6,
            worldNumber: 6,
            name: "Shimbashi Izakaya Night",
            nameJa: "ワールド6：新橋ガード下・居酒屋の洗礼",
            district: "Shimbashi",
            jfLevel: "JF B1",
            themeColorHex: "#10B981",
            stages: [
                QuestStage(id: 16, stageNumber: 16, worldId: 6, worldName: "Shimbashi", worldNameJa: "新橋", stageTitle: "Izakaya Table Call", stageTitleJa: "とりあえず生！盛り合わせと注文", missionType: "scenario", targetContentId: "scenario_04_izakaya_table_booking", jfLevel: "B1", targetSkill: "Social Dining", iconName: "wineglass.fill", xpReward: 200),
                QuestStage(id: 17, stageNumber: 17, worldId: 6, worldName: "Shimbashi", worldNameJa: "新橋", stageTitle: "Otōshi & X Sign Duel (Boss)", stageTitleJa: "居酒屋ボス戦：お通し理解とX会計サイン", missionType: "boss_trial", targetContentId: "dojo_03_izakaya_table_charge", jfLevel: "B1", targetSkill: "Izakaya Mastery", iconName: "star.circle.fill", xpReward: 500)
            ]
        ),
        TokyoQuestWorld(
            id: 7,
            worldNumber: 7,
            name: "Tokyo Living Logistics",
            nameJa: "ワールド7：東京実務・不在票とシェアバイク",
            district: "Shimokitazawa",
            jfLevel: "JF B1",
            themeColorHex: "#6366F1",
            stages: [
                QuestStage(id: 18, stageNumber: 18, worldId: 7, worldName: "Shimokitazawa", worldNameJa: "下北沢", stageTitle: "Missed Package Redelivery", stageTitleJa: "不在票の再配達とゆうゆう窓口", missionType: "scenario", targetContentId: "scenario_07_post_office_delivery", jfLevel: "B1", targetSkill: "Logistics & Redelivery", iconName: "shippingbox.fill", xpReward: 220),
                QuestStage(id: 19, stageNumber: 19, worldId: 7, worldName: "Roppongi", worldNameJa: "六本木", stageTitle: "Docomo Share Bike Port", stageTitleJa: "赤チャリ（ドコモ・バイクシェア）とLUUP", missionType: "scenario", targetContentId: "scenario_05_docomo_bike_rental", jfLevel: "B1", targetSkill: "Mobility & Port Return", iconName: "bicycle", xpReward: 220)
            ]
        ),
        TokyoQuestWorld(
            id: 8,
            worldNumber: 8,
            name: "Grand Tokyo Fluency",
            nameJa: "ワールド8：大東京生活完全自立・最終試練",
            district: "Tokyo Metropolitan",
            jfLevel: "JF B1 Independent",
            themeColorHex: "#D97706",
            stages: [
                QuestStage(id: 20, stageNumber: 20, worldId: 8, worldName: "Tokyo", worldNameJa: "大東京", stageTitle: "Train Delay & Apology Ear Test", stageTitleJa: "急病人救護とお詫び放送の全聞き取り", missionType: "audio_listening", targetContentId: "announcement_04_train_delay_apology", jfLevel: "B1", targetSkill: "Emergency Transit Audio", iconName: "exclamationmark.triangle.fill", xpReward: 300),
                QuestStage(id: 21, stageNumber: 21, worldId: 8, worldName: "Tokyo", worldNameJa: "大東京", stageTitle: "Tokyo Master Grand Boss", stageTitleJa: "最終ボス戦：全シチュエーション無双", missionType: "boss_trial", targetContentId: "scenario_01_morning_train", jfLevel: "B1", targetSkill: "Full Tokyo Living Fluency", iconName: "crown.fill", xpReward: 1000)
            ]
        )
    ]
}
