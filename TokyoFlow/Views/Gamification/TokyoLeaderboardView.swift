import SwiftUI

public struct TokyoLeaderboardView: View {
    @ObservedObject var gamification = GamificationService.shared
    @Environment(\.dismiss) private var dismiss
    @State private var selectedLeaderboardType: Int = 0 // 0: Weekly League, 1: All-Time, 2: Friends
    public var isEmbedded: Bool = false

    public init(isEmbedded: Bool = false) {
        self.isEmbedded = isEmbedded
    }

    private var currentUsersList: [LeaderboardUser] {
        switch selectedLeaderboardType {
        case 0: return gamification.leaderboardUsers
        case 1: return gamification.allTimeLeaderboardUsers
        case 2: return gamification.friendsLeaderboardUsers
        default: return gamification.leaderboardUsers
        }
    }

    public var body: some View {
        if isEmbedded {
            mainLeaderboardContent
        } else {
            NavigationStack {
                ZStack {
                    MangaThemeBackgroundView()
                    mainLeaderboardContent
                }
                .navigationTitle("Tokyo League")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Close") { dismiss() }
                    }
                }
            }
        }
    }

    private var mainLeaderboardContent: some View {
        ScrollView(showsIndicators: false) {
            VStack(spacing: 20) {
                        // Leaderboard Scope Segmented Selector
                        Picker("Leaderboard Scope", selection: $selectedLeaderboardType) {
                            Text("Weekly League").tag(0)
                            Text("Hall of Fame").tag(1)
                            Text("Friends").tag(2)
                        }
                        .pickerStyle(.segmented)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // League Tier Banner & Weekly Reset Counter
                        VStack(spacing: 12) {
                            HStack(spacing: 14) {
                                ZStack {
                                    Circle()
                                        .fill(LinearGradient(colors: [.yellow.opacity(0.3), .orange.opacity(0.3)], startPoint: .topLeading, endPoint: .bottomTrailing))
                                        .frame(width: 50, height: 50)

                                    Image(systemName: gamification.currentLeague.icon)
                                        .font(.system(size: 26))
                                        .foregroundColor(.yellow)
                                }

                                VStack(alignment: .leading, spacing: 3) {
                                    HStack(spacing: 6) {
                                        Text(gamification.currentLeague.rawValue)
                                            .font(.system(size: 16, weight: .black))
                                        Text("Top 3 Promoted")
                                            .font(.system(size: 10, weight: .bold))
                                            .foregroundColor(.green)
                                            .padding(.horizontal, 6)
                                            .padding(.vertical, 2)
                                            .background(Color.green.opacity(0.15))
                                            .cornerRadius(6)
                                    }

                                    Text("Resets every Sun 24:00 · Top 3 promote & earn 500 TP")
                                        .font(.system(size: 11))
                                        .foregroundColor(.secondary)
                                }
                                Spacer()
                            }

                            Divider()

                            HStack {
                                HStack(spacing: 4) {
                                    Image(systemName: "clock.badge.exclamationmark")
                                        .foregroundColor(.orange)
                                    Text("Ends in: 2d 14h")
                                        .font(.system(size: 11, weight: .semibold))
                                        .foregroundColor(.secondary)
                                }

                                Spacer()

                                HStack(spacing: 4) {
                                    Image(systemName: "person.crop.circle.fill")
                                        .foregroundColor(.accentColor)
                                    Text("Your Rank: #3 (Promotion Zone)")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.accentColor)
                                }
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // Top 3 Podium (3D Elevation)
                        if currentUsersList.count >= 3 {
                            HStack(alignment: .bottom, spacing: 10) {
                                // Rank 2 (Silver)
                                PodiumColumnView(user: currentUsersList[1], rankColor: .gray, podiumHeight: 110, crownIcon: "2.circle.fill")

                                // Rank 1 (Gold)
                                PodiumColumnView(user: currentUsersList[0], rankColor: .yellow, podiumHeight: 145, crownIcon: "crown.fill")

                                // Rank 3 (Bronze)
                                PodiumColumnView(user: currentUsersList[2], rankColor: .orange, podiumHeight: 90, crownIcon: "3.circle.fill")
                            }
                            .padding(.horizontal)
                            .padding(.top, 6)
                        }

                        // Promotion / Demotion Zone Indicator Bar
                        HStack(spacing: 8) {
                            Circle()
                                .fill(Color.green)
                                .frame(width: 8, height: 8)
                            Text("Top 3 advance to Shinjuku Platinum League (Promotion Zone)")
                                .font(.system(size: 11, weight: .bold))
                                .foregroundColor(.green)
                            Spacer()
                        }
                        .padding(.horizontal, 20)

                        // Full Leaderboard List
                        VStack(spacing: 10) {
                            ForEach(Array(currentUsersList.enumerated()), id: \.element.id) { index, user in
                                LeaderboardUserRowView(user: user, position: index + 1)
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 30)
                }
            }
        }

public struct PodiumColumnView: View {
    public let user: LeaderboardUser
    public let rankColor: Color
    public let podiumHeight: CGFloat
    public let crownIcon: String

    public var body: some View {
        VStack(spacing: 6) {
            ZStack(alignment: .topTrailing) {
                Text(user.avatar)
                    .font(.system(size: 34))
                    .padding(8)
                    .background(user.isCurrentUser ? Color.accentColor.opacity(0.2) : Color.white.opacity(0.1))
                    .clipShape(Circle())
                    .overlay(
                        Circle()
                            .stroke(rankColor, lineWidth: user.rank == 1 ? 2.5 : 1.5)
                    )

                Image(systemName: crownIcon)
                    .font(.system(size: 14))
                    .foregroundColor(rankColor)
                    .offset(x: 4, y: -4)
            }

            Text(user.name)
                .font(.system(size: 12, weight: user.isCurrentUser ? .black : .bold))
                .foregroundColor(user.isCurrentUser ? .accentColor : .primary)
                .lineLimit(1)

            Text("\(user.points) XP")
                .font(.system(size: 11, weight: .black, design: .rounded))
                .foregroundColor(.secondary)

            // Podium Pedestal
            ZStack {
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [rankColor.opacity(0.25), rankColor.opacity(0.08)],
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .frame(height: podiumHeight)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(rankColor.opacity(0.4), lineWidth: 1.5)
                    )

                VStack(spacing: 4) {
                    Text("#\(user.rank)")
                        .font(.system(size: 24, weight: .black, design: .rounded))
                        .foregroundColor(rankColor)

                    HStack(spacing: 3) {
                        Image(systemName: "flame.fill")
                            .font(.system(size: 9))
                            .foregroundColor(.red)
                        Text("\(user.streak)d")
                            .font(.system(size: 10, weight: .bold))
                            .foregroundColor(.secondary)
                    }
                }
            }
        }
        .frame(maxWidth: .infinity)
    }
}

public struct LeaderboardUserRowView: View {
    public let user: LeaderboardUser
    public let position: Int

    public var isPromotionZone: Bool {
        return position <= 3
    }

    public var body: some View {
        HStack(spacing: 12) {
            // Rank Badge
            ZStack {
                if position <= 3 {
                    Circle()
                        .fill(position == 1 ? Color.yellow.opacity(0.2) : (position == 2 ? Color.gray.opacity(0.2) : Color.orange.opacity(0.2)))
                        .frame(width: 28, height: 28)
                    Text("\(position)")
                        .font(.system(size: 13, weight: .black))
                        .foregroundColor(position == 1 ? .yellow : (position == 2 ? .gray : .orange))
                } else {
                    Text("\(position)")
                        .font(.system(size: 13, weight: .black))
                        .foregroundColor(.secondary)
                        .frame(width: 28)
                }
            }

            Text(user.avatar)
                .font(.title3)

            VStack(alignment: .leading, spacing: 2) {
                HStack(spacing: 6) {
                    Text(user.name)
                        .font(.system(size: 14, weight: user.isCurrentUser ? .black : .bold))
                    if user.isCurrentUser {
                        Text("(You)")
                            .font(.system(size: 10, weight: .heavy))
                            .foregroundColor(.accentColor)
                            .padding(.horizontal, 4)
                            .padding(.vertical, 1)
                            .background(Color.accentColor.opacity(0.15))
                            .cornerRadius(4)
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
                .font(.system(size: 14, weight: .black, design: .rounded))
                .foregroundColor(user.isCurrentUser ? .accentColor : .primary)
        }
        .padding(14)
        .background(user.isCurrentUser ? Color.accentColor.opacity(0.18) : Color.white.opacity(0.08))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(user.isCurrentUser ? Color.accentColor : (isPromotionZone ? Color.green.opacity(0.3) : Color.clear), lineWidth: user.isCurrentUser ? 1.5 : 1)
        )
    }
}
