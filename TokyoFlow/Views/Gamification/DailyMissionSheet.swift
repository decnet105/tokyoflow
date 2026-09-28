import SwiftUI

public struct DailyMissionSheet: View {
    @ObservedObject var gamification = GamificationService.shared
    @Environment(\.dismiss) private var dismiss

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Streak & Daily Bonus Header
                        VStack(spacing: 12) {
                            HStack(spacing: 12) {
                                ZStack {
                                    Circle()
                                        .fill(Color.red.opacity(0.2))
                                        .frame(width: 54, height: 54)
                                    Image(systemName: "flame.fill")
                                        .font(.title)
                                        .foregroundColor(.red)
                                }

                                VStack(alignment: .leading, spacing: 2) {
                                    Text("\(gamification.streakDays) Days Streak!")
                                        .font(.system(size: 20, weight: .black, design: .rounded))
                                    Text("Keep your daily Tokyo immersion streak alive.")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                Spacer()
                            }

                            Divider()

                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Tokyo Points")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                    Text("\(gamification.tokyoPoints) TP")
                                        .font(.system(size: 16, weight: .bold))
                                        .foregroundColor(.yellow)
                                }

                                Spacer()

                                VStack(alignment: .trailing, spacing: 2) {
                                    Text("Total Experience")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                    Text("\(gamification.totalEXP) EXP")
                                        .font(.system(size: 16, weight: .bold))
                                        .foregroundColor(.accentColor)
                                }
                            }
                        }
                        .padding(18)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Daily Missions Header
                        HStack {
                            Text("DAILY MISSIONS (デイリー任務)")
                                .font(.system(size: 13, weight: .black))
                                .foregroundColor(.secondary)
                                .tracking(1.0)
                            Spacer()
                            Text("Resets at 00:00 JST")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)

                        // Quest Cards List
                        VStack(spacing: 12) {
                            ForEach(gamification.dailyQuests) { quest in
                                DailyQuestRowView(quest: quest) {
                                    gamification.completeQuest(id: quest.id)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 30)
                }
            }
            .navigationTitle("Daily Missions & Rewards")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}

public struct DailyQuestRowView: View {
    public let quest: DailyQuest
    public let onClaim: () -> Void

    public var body: some View {
        HStack(spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 14)
                    .fill(quest.isCompleted ? Color.green.opacity(0.15) : Color.accentColor.opacity(0.12))
                    .frame(width: 46, height: 46)

                Image(systemName: quest.icon)
                    .font(.title3)
                    .foregroundColor(quest.isCompleted ? .green : .accentColor)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(quest.title)
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(quest.isCompleted ? .secondary : .primary)

                Text(quest.subtitle)
                    .font(.system(size: 12))
                    .foregroundColor(.secondary)
                    .lineLimit(1)

                HStack(spacing: 8) {
                    HStack(spacing: 2) {
                        Image(systemName: "yensign.circle.fill")
                            .foregroundColor(.yellow)
                        Text("+\(quest.rewardTP)")
                    }
                    .font(.caption2)
                    .fontWeight(.bold)

                    HStack(spacing: 2) {
                        Image(systemName: "sparkles")
                            .foregroundColor(.blue)
                        Text("+\(quest.rewardEXP) EXP")
                    }
                    .font(.caption2)
                    .fontWeight(.bold)
                }
            }

            Spacer()

            if quest.isCompleted {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.green)
                    .font(.title2)
            } else if quest.currentProgress >= quest.targetCount {
                Button(action: onClaim) {
                    Text("Claim")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 8)
                        .background(Color.green)
                        .cornerRadius(12)
                }
            } else {
                Text("\(quest.currentProgress)/\(quest.targetCount)")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.secondary)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Color.gray.opacity(0.15))
                    .cornerRadius(10)
            }
        }
        .padding(14)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
    }
}
