import SwiftUI

public struct SurvivalPhraseItem: Identifiable {
    public var id: String { japanese }
    public let category: String
    public let japanese: String
    public let reading: String
    public let english: String
    public let chinese: String
    public let scenarioContext: String
}

public struct SurvivalCheatSheetView: View {
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedCategory: String = "all"
    @State private var showSRSDeck = false

    private let phrases: [SurvivalPhraseItem] = [
        SurvivalPhraseItem(category: "Transit", japanese: "〜は何番線ですか？", reading: "〜は なんばんせん ですか？", english: "Which platform number for [Location]?", chinese: "去某某地在几号站台？", scenarioContext: "Yamanote & Metro stations"),
        SurvivalPhraseItem(category: "Transit", japanese: "タッチできませんでした", reading: "タッチ できませんでした", english: "My IC card didn't tap properly.", chinese: "交通卡刚才没刷上。", scenarioContext: "Ticket barrier window"),
        SurvivalPhraseItem(category: "Kombini", japanese: "温めてください", reading: "あたたためてください", english: "Please warm this up.", chinese: "请帮我加热一下。", scenarioContext: "Bento / onigiri counter"),
        SurvivalPhraseItem(category: "Kombini", japanese: "袋は大丈夫です", reading: "ふくろは だいじょうぶです", english: "No plastic bag needed.", chinese: "不需要塑料袋。", scenarioContext: "Kombini checkout"),
        SurvivalPhraseItem(category: "Kombini", japanese: "一緒でいいです", reading: "いっしょで いいです", english: "Putting hot and cold items together is fine.", chinese: "冷热装一起就行。", scenarioContext: "Separate bag query"),
        SurvivalPhraseItem(category: "Dining", japanese: "とりあえず生で！", reading: "とりあえず なまで！", english: "Draft beer to start with!", chinese: "先来杯生啤！", scenarioContext: "Izakaya drink order"),
        SurvivalPhraseItem(category: "Dining", japanese: "お会計（お勘定）お願いします", reading: "おかいけい おねがいします", english: "Check/Bill please.", chinese: "请结账。", scenarioContext: "Restaurant table call"),
        SurvivalPhraseItem(category: "Dining", japanese: "アレルギーがあります", reading: "アレルギーが あります", english: "I have an allergy to...", chinese: "我对……过敏。", scenarioContext: "Menu dietary check"),
        SurvivalPhraseItem(category: "Shopping", japanese: "試着してもいいですか？", reading: "しちゃく しても いいですか？", english: "May I try this on?", chinese: "请问可以试穿一下吗？", scenarioContext: "Clothing boutique"),
        SurvivalPhraseItem(category: "Shopping", japanese: "免税できますか？", reading: "めんぜい できますか？", english: "Can I get tax-free refund?", chinese: "可以办理免税吗？", scenarioContext: "Tax-free shopping counter"),
        SurvivalPhraseItem(category: "Services", japanese: "不在票が入っていました", reading: "ふざいひょうが はいっていました", english: "I received a missed delivery slip.", chinese: "我收到了未妥投不在票。", scenarioContext: "Post office redelivery call"),
        SurvivalPhraseItem(category: "Emergency", japanese: "救急車をお願いします", reading: "きゅうきゅうしゃを おねがいします", english: "Please call an ambulance (119).", chinese: "请帮我叫救护车。", scenarioContext: "Medical emergency 119")
    ]

    private var categories: [String] {
        ["all", "Transit", "Kombini", "Dining", "Shopping", "Services", "Emergency"]
    }

    private var filteredPhrases: [SurvivalPhraseItem] {
        if selectedCategory == "all" { return phrases }
        return phrases.filter { $0.category == selectedCategory }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Header Banner
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text("SURVIVAL CHEAT SHEET")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.orange)
                                        .tracking(1.5)
                                    Text("1-Tap Tokyo Phrases")
                                        .font(.system(size: 26, weight: .bold, design: .rounded))
                                }
                                Spacer()
                                Button(action: { showSRSDeck = true }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "rectangle.stack.fill")
                                        Text("SRS Review (\(userProfile.bookmarkedPhrases.count))")
                                            .font(.system(size: 12, weight: .bold))
                                    }
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 8)
                                    .background(Color.orange.opacity(0.12))
                                    .foregroundColor(.orange)
                                    .cornerRadius(20)
                                }
                            }

                            Text("Instant, life-tested Japanese phrases for when you're standing in front of station gates, cashiers, or ramen counters.")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Categories
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 8) {
                                ForEach(categories, id: \.self) { cat in
                                    Button(action: { selectedCategory = cat }) {
                                        Text(cat == "all" ? "All Situations" : cat)
                                            .font(.caption)
                                            .fontWeight(.semibold)
                                            .padding(.horizontal, 12)
                                            .padding(.vertical, 6)
                                            .background(selectedCategory == cat ? Color.orange : Color.primary.opacity(0.08))
                                            .foregroundColor(selectedCategory == cat ? .white : .primary)
                                            .cornerRadius(16)
                                    }
                                }
                            }
                            .padding(.horizontal)
                        }

                        // Phrases List
                        LazyVStack(spacing: 12) {
                            ForEach(filteredPhrases) { phrase in
                                HStack(alignment: .top) {
                                    VStack(alignment: .leading, spacing: 4) {
                                        HStack {
                                            Text(phrase.category)
                                                .font(.caption2)
                                                .fontWeight(.bold)
                                                .padding(.horizontal, 6)
                                                .padding(.vertical, 2)
                                                .background(Color.orange.opacity(0.12))
                                                .foregroundColor(.orange)
                                                .cornerRadius(6)

                                            Text("• \(phrase.scenarioContext)")
                                                .font(.caption2)
                                                .foregroundColor(.secondary)
                                        }

                                        Text(phrase.japanese)
                                            .font(.headline)
                                            .foregroundColor(.primary)

                                        Text(phrase.reading)
                                            .font(.caption)
                                            .foregroundColor(.secondary)

                                        Text(phrase.english)
                                            .font(.footnote)
                                            .foregroundColor(.primary.opacity(0.9))

                                        Text(phrase.chinese)
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }

                                    Spacer()

                                    VStack(spacing: 12) {
                                        AudioButton(textToSpeak: phrase.japanese)
                                        Button(action: {
                                            userProfile.toggleBookmark(
                                                japanese: phrase.japanese,
                                                reading: phrase.reading,
                                                english: phrase.english,
                                                context: phrase.scenarioContext
                                            )
                                        }) {
                                            Image(systemName: userProfile.isBookmarked(phrase.japanese) ? "bookmark.fill" : "bookmark")
                                                .foregroundColor(userProfile.isBookmarked(phrase.japanese) ? .orange : .secondary)
                                        }
                                    }
                                }
                                .padding(14)
                                .background(.ultraThinMaterial)
                                .cornerRadius(14)
                                .shadow(color: Color.black.opacity(0.03), radius: 6, x: 0, y: 2)
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 24)
                }
            }
            .navigationTitle("Survival Kit")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $showSRSDeck) {
                FlashcardDeckView()
            }
        }
    }
}
