import SwiftUI

public struct DailyNewsFeedView: View {
    @ObservedObject var newsService = NHKNewsService.shared
    @ObservedObject var gamification = GamificationService.shared
    @ObservedObject var radioService = TokyoRadioService.shared
    @State private var selectedCategory: String = "All"
    @State private var showMissions = false
    @State private var showLeaderboard = false
    @State private var selectedRadioStation: TokyoRadioStation? = nil

    private let radioData = TokyoRadioDataManager.shared
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

                VStack(spacing: 0) {
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

                            // 1-HOUR TOKYO IMMERSION RADIO HERO CARD
                            if let primaryStation = radioData.stations.first {
                                Button(action: {
                                    selectedRadioStation = primaryStation
                                }) {
                                    VStack(alignment: .leading, spacing: 14) {
                                        HStack {
                                            HStack(spacing: 6) {
                                                Image(systemName: "antenna.radiowaves.left.and.right")
                                                    .foregroundColor(.red)
                                                Text(primaryStation.badge)
                                                    .font(.system(size: 10, weight: .black))
                                                    .foregroundColor(.red)
                                                    .tracking(1.0)
                                            }
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(Color.red.opacity(0.15))
                                            .cornerRadius(8)

                                            Spacer()

                                            HStack(spacing: 4) {
                                                Image(systemName: "clock.fill")
                                                    .foregroundColor(.orange)
                                                Text(primaryStation.durationLabel)
                                                    .font(.caption2)
                                                    .fontWeight(.bold)
                                                    .foregroundColor(.orange)
                                            }
                                        }

                                        VStack(alignment: .leading, spacing: 4) {
                                            Text(primaryStation.titleJa)
                                                .font(.system(size: 17, weight: .black, design: .rounded))
                                                .foregroundColor(.primary)

                                            Text(primaryStation.subtitle)
                                                .font(.system(size: 12))
                                                .foregroundColor(.secondary)
                                                .lineLimit(2)
                                                .multilineTextAlignment(.leading)
                                        }

                                        Divider()

                                        HStack {
                                            HStack(spacing: 6) {
                                                Image(systemName: radioService.isPlaying && radioService.currentStation?.id == primaryStation.id ? "pause.circle.fill" : "play.circle.fill")
                                                    .font(.title2)
                                                    .foregroundColor(.accentColor)

                                                Text(radioService.isPlaying && radioService.currentStation?.id == primaryStation.id ? "Now Playing • Tap to Open" : "Start 1-Hour Radio Immersion")
                                                    .font(.caption)
                                                    .fontWeight(.bold)
                                                    .foregroundColor(.accentColor)
                                            }

                                            Spacer()

                                            Image(systemName: "chevron.right")
                                                .font(.caption2)
                                                .foregroundColor(.secondary)
                                        }
                                    }
                                    .padding(18)
                                    .background(
                                        LinearGradient(
                                            colors: [Color.accentColor.opacity(0.12), Color.pink.opacity(0.08)],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(22)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 22)
                                            .stroke(Color.accentColor.opacity(0.3), lineWidth: 1.5)
                                    )
                                    .padding(.horizontal)
                                }
                                .buttonStyle(PlainButtonStyle())
                            }

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

                    // Persistent Mini Player Bar
                    TokyoRadioMiniPlayerBar()
                }
            }
            .navigationTitle("Tokyo Daily News & Radio")
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
            .sheet(item: $selectedRadioStation) { station in
                TokyoRadioPlayerModalView(station: station)
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
                    Text("NHK Native Voice")
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
