import SwiftUI

public struct TokyoLeaderboardView: View {
    @ObservedObject var gamification = GamificationService.shared
    @Environment(\.dismiss) private var dismiss

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // League Tier Banner
                        HStack(spacing: 14) {
                            Image(systemName: gamification.currentLeague.icon)
                                .font(.system(size: 32))
                                .foregroundColor(.yellow)

                            VStack(alignment: .leading, spacing: 2) {
                                Text(gamification.currentLeague.rawValue)
                                    .font(.system(size: 16, weight: .black))
                                Text("Top 3 learners promote to next Tokyo League!")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Top 3 Podium
                        HStack(alignment: .bottom, spacing: 12) {
                            // Rank 2 (Silver)
                            if gamification.leaderboardUsers.count > 1 {
                                PodiumColumnView(user: gamification.leaderboardUsers[1], rankColor: .gray, height: 100)
                            }

                            // Rank 1 (Gold)
                            if gamification.leaderboardUsers.count > 0 {
                                PodiumColumnView(user: gamification.leaderboardUsers[0], rankColor: .yellow, height: 130)
                            }

                            // Rank 3 (Bronze)
                            if gamification.leaderboardUsers.count > 2 {
                                PodiumColumnView(user: gamification.leaderboardUsers[2], rankColor: .orange, height: 85)
                            }
                        }
                        .padding(.horizontal)

                        // Full Leaderboard List
                        VStack(spacing: 10) {
                            ForEach(gamification.leaderboardUsers) { user in
                                LeaderboardUserRowView(user: user)
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 30)
                }
            }
            .navigationTitle("Tokyo League Ranking")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}

public struct PodiumColumnView: View {
    public let user: LeaderboardUser
    public let rankColor: Color
    public let height: CGFloat

    public var body: some View {
        VStack(spacing: 6) {
            Text(user.avatar)
                .font(.system(size: 28))

            Text(user.name)
                .font(.system(size: 11, weight: .bold))
                .lineLimit(1)

            Text("\(user.points) XP")
                .font(.system(size: 10, weight: .semibold))
                .foregroundColor(.secondary)

            ZStack {
                RoundedRectangle(cornerRadius: 14)
                    .fill(rankColor.opacity(0.2))
                    .frame(height: height)

                VStack(spacing: 2) {
                    Text("#\(user.rank)")
                        .font(.system(size: 20, weight: .black, design: .rounded))
                        .foregroundColor(rankColor)
                }
            }
        }
        .frame(maxWidth: .infinity)
    }
}

public struct LeaderboardUserRowView: View {
    public let user: LeaderboardUser

    public var body: some View {
        HStack(spacing: 12) {
            Text("#\(user.rank)")
                .font(.system(size: 14, weight: .black))
                .foregroundColor(user.isCurrentUser ? .accentColor : .secondary)
                .frame(width: 28)

            Text(user.avatar)
                .font(.title3)

            VStack(alignment: .leading, spacing: 2) {
                HStack(spacing: 4) {
                    Text(user.name)
                        .font(.system(size: 14, weight: user.isCurrentUser ? .black : .bold))
                    if user.isCurrentUser {
                        Text("(You)")
                            .font(.system(size: 10, weight: .bold))
                            .foregroundColor(.accentColor)
                    }
                }

                Text(user.title)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }

            Spacer()

            HStack(spacing: 4) {
                Image(systemName: "flame.fill")
                    .foregroundColor(.red)
                    .font(.caption2)
                Text("\(user.streak)d")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }

            Text("\(user.points) XP")
                .font(.system(size: 14, weight: .bold))
                .foregroundColor(user.isCurrentUser ? .accentColor : .primary)
        }
        .padding(14)
        .background(user.isCurrentUser ? Color.accentColor.opacity(0.18) : Color.white.opacity(0.08))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(user.isCurrentUser ? Color.accentColor : Color.clear, lineWidth: 1.5)
        )
    }
}
