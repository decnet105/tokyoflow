import SwiftUI

public struct DailyNewsFeedView: View {
    @ObservedObject var newsService = NHKNewsService.shared
    @ObservedObject var gamification = GamificationService.shared
    @State private var selectedCategory: String = "All"
    @State private var showMissions = false
    @State private var showLeaderboard = false

    let categories = ["All", "Tokyo Transit (交通)", "Manga & Culture (文化)", "Tokyo Life (暮らし)"]

    public init() {}

    public var filteredNews: [DailyNewsItem] {
        if selectedCategory == "All" {
            return newsService.dailyNews
        }
        return newsService.dailyNews.filter { $0.category == selectedCategory }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Top Daily Habit & Rewards Card
                        VStack(spacing: 12) {
                            HStack {
                                HStack(spacing: 8) {
                                    Text(gamification.currentTier.badgeIcon.contains(".") ? "🏆" : "🌸")
                                        .font(.title2)
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(gamification.currentTier.titleJapanese)
                                            .font(.system(size: 13, weight: .black))
                                            .foregroundColor(.primary)
                                        Text("Level \(gamification.currentTier.level) • \(gamification.totalEXP) EXP")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                }

                                Spacer()

                                // Tokyo Points Chip
                                HStack(spacing: 4) {
                                    Image(systemName: "yensign.circle.fill")
                                        .foregroundColor(.yellow)
                                    Text("\(gamification.tokyoPoints) TP")
                                        .font(.system(size: 13, weight: .bold))
                                }
                                .padding(.horizontal, 10)
                                .padding(.vertical, 6)
                                .background(.ultraThinMaterial)
                                .cornerRadius(12)

                                // Daily Mission Button
                                Button(action: { showMissions = true }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: "list.bullet.clipboard.fill")
                                            .foregroundColor(.accentColor)
                                        Text("Tasks")
                                            .font(.caption)
                                            .fontWeight(.bold)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.accentColor.opacity(0.15))
                                    .cornerRadius(12)
                                }
                            }

                            // EXP Progress Bar
                            VStack(alignment: .leading, spacing: 4) {
                                HStack {
                                    Text("Next Tier: \(gamification.nextTier?.titleJapanese ?? "Max Level")")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                    Spacer()
                                    Text("\(Int(gamification.progressToNextTier * 100))%")
                                        .font(.caption2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.accentColor)
                                }

                                ProgressView(value: gamification.progressToNextTier)
                                    .tint(.accentColor)
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // Real Radio / Human Native Voice Banner
                        HStack(spacing: 14) {
                            Image(systemName: "mic.badge.waveform")
                                .font(.system(size: 32))
                                .foregroundColor(.pink)

                            VStack(alignment: .leading, spacing: 4) {
                                HStack(spacing: 6) {
                                    Text("NHK NEWS WEB EASY")
                                        .font(.system(size: 10, weight: .black))
                                        .foregroundColor(.pink)
                                        .tracking(1.5)

                                    Text("100% Native Human Audio")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundColor(.green)
                                        .padding(.horizontal, 6)
                                        .padding(.vertical, 2)
                                        .background(Color.green.opacity(0.15))
                                        .cornerRadius(6)
                                }

                                Text("Daily Tokyo Ear Training & Shadowing")
                                    .font(.system(size: 15, weight: .bold))

                                Text("Real Japanese broadcast speed, ruby furigana, and microphone voice comparison.")
                                    .font(.system(size: 12))
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // Category Pills
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 8) {
                                ForEach(categories, id: \.self) { cat in
                                    Button(action: { selectedCategory = cat }) {
                                        Text(cat)
                                            .font(.caption)
                                            .fontWeight(.bold)
                                            .padding(.horizontal, 12)
                                            .padding(.vertical, 8)
                                            .background(selectedCategory == cat ? Color.accentColor : Color.gray.opacity(0.15))
                                            .foregroundColor(selectedCategory == cat ? .white : .primary)
                                            .cornerRadius(12)
                                    }
                                }
                            }
                            .padding(.horizontal)
                        }

                        // News Article Feed
                        VStack(spacing: 14) {
                            ForEach(filteredNews) { item in
                                NavigationLink(destination: NewsShadowingLabView(newsItem: item)) {
                                    DailyNewsCardView(item: item)
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.vertical, 12)
                }
                .refreshable {
                    newsService.fetchLatestPublicNews()
                }
            }
            .navigationTitle("Tokyo Daily News")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(action: { showLeaderboard = true }) {
                        Image(systemName: "trophy.fill")
                            .foregroundColor(.yellow)
                    }
                }
            }
            .sheet(isPresented: $showMissions) {
                DailyMissionSheet()
            }
            .sheet(isPresented: $showLeaderboard) {
                TokyoLeaderboardView()
            }
        }
    }
}

public struct DailyNewsCardView: View {
    public let item: DailyNewsItem

    public var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Label(item.category, systemImage: item.categoryIcon)
                    .font(.caption2)
                    .fontWeight(.bold)
                    .foregroundColor(.accentColor)

                Spacer()

                HStack(spacing: 4) {
                    Image(systemName: "waveform")
                        .foregroundColor(.green)
                    Text("Human Audio")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }

            Text(item.title)
                .font(.system(size: 16, weight: .bold))
                .foregroundColor(.primary)
                .multilineTextAlignment(.leading)

            Text(item.summary)
                .font(.system(size: 13))
                .foregroundColor(.secondary)
                .lineLimit(2)
                .multilineTextAlignment(.leading)

            HStack {
                Text(item.sourceName)
                    .font(.caption2)
                    .foregroundColor(.secondary)

                Spacer()

                HStack(spacing: 4) {
                    Text("Start Shadowing")
                        .font(.caption)
                        .fontWeight(.bold)
                    Image(systemName: "chevron.right")
                        .font(.caption2)
                }
                .foregroundColor(.accentColor)
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
    }
}
