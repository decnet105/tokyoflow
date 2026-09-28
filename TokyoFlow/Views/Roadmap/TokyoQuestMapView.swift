import SwiftUI

public struct TokyoQuestMapView: View {
    @ObservedObject var dataManager = DataManager.shared
    @ObservedObject var themeManager = ThemeManager.shared
    @ObservedObject var gamification = GamificationService.shared
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedStage: QuestStage? = nil
    @State private var showThemePicker = false
    @State private var showDailyMissions = false
    @State private var showLeaderboard = false

    private let worlds = QuestProgressManager.worlds

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                // Background Layer (Theme wallpaper or soft clean gradient)
                MangaThemeBackgroundView()

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 24) {
                        // Top Player Stats Ribbon
                        VStack(spacing: 12) {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("TOKYO JOURNEY QUEST")
                                        .font(.system(size: 10, weight: .bold))
                                        .foregroundColor(.accentColor)
                                        .tracking(2.0)
                                    Text("Tokyo Mastery Map")
                                        .font(.system(size: 24, weight: .black, design: .rounded))
                                }

                                Spacer()

                                Button(action: { showThemePicker = true }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: "paintpalette.fill")
                                        Text("Theme")
                                            .font(.caption)
                                            .fontWeight(.bold)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(12)
                                }
                            }

                            // Quick Action Hub (Check-in & Leaderboard & Streak)
                            HStack(spacing: 10) {
                                Button(action: { showDailyMissions = true }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: gamification.isTodayCheckedIn ? "checkmark.circle.fill" : "flame.fill")
                                            .foregroundColor(gamification.isTodayCheckedIn ? .green : .red)
                                        Text(gamification.isTodayCheckedIn ? "\(gamification.streakDays)d Streak" : "Check In")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(.primary)
                                    }
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 8)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(12)
                                }
                                .buttonStyle(.plain)

                                Button(action: { showLeaderboard = true }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "trophy.fill")
                                            .foregroundColor(.yellow)
                                        Text("Rank #3")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(.primary)
                                    }
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 8)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(12)
                                }
                                .buttonStyle(.plain)

                                HStack(spacing: 6) {
                                    Image(systemName: "crown.fill")
                                        .foregroundColor(.yellow)
                                    Text("Lv.\(max(1, userProfile.completedScenarioIds.count * 2))")
                                        .font(.system(size: 12, weight: .bold))
                                }
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 8)
                                .background(.ultraThinMaterial)
                                .cornerRadius(12)
                            }
                        }
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // 🌟 Real-World Adaptive Scene Learning Hub Card
                        TokyoContextHubCardView()
                            .padding(.horizontal)

                        // Quest Worlds Path
                        ForEach(worlds) { world in
                            WorldSectionView(
                                world: world,
                                completedScenarioIds: userProfile.completedScenarioIds,
                                onSelectStage: { stage in
                                    selectedStage = stage
                                }
                            )
                        }
                    }
                    .padding(.bottom, 40)
                }
            }
            .navigationTitle("Tokyo Quest")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $showThemePicker) {
                ThemePickerSheet()
            }
            .sheet(isPresented: $showDailyMissions) {
                DailyMissionSheet()
            }
            .sheet(isPresented: $showLeaderboard) {
                TokyoLeaderboardView(isEmbedded: false)
            }
            .sheet(item: $selectedStage) { stage in
                StageLauncherModal(stage: stage)
            }
        }
    }
}

public struct WorldSectionView: View {
    public let world: TokyoQuestWorld
    public let completedScenarioIds: Set<String>
    public let onSelectStage: (QuestStage) -> Void

    private var worldColor: Color {
        Color(hex: world.themeColorHex)
    }

    public var body: some View {
        VStack(spacing: 20) {
            // World Title Banner
            VStack(spacing: 4) {
                HStack(spacing: 8) {
                    Text(world.nameJa)
                        .font(.system(size: 18, weight: .heavy, design: .rounded))
                        .foregroundColor(.primary)

                    Text(world.jfLevel)
                        .font(.system(size: 10, weight: .bold))
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(worldColor.opacity(0.15))
                        .foregroundColor(worldColor)
                        .cornerRadius(6)
                }

                Text(world.name)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(.ultraThinMaterial)
            .cornerRadius(16)
            .shadow(color: Color.black.opacity(0.04), radius: 6, x: 0, y: 2)

            // Sequential Winding Stage Nodes
            VStack(spacing: 24) {
                ForEach(Array(world.stages.enumerated()), id: \.offset) { index, stage in
                    let isUnlocked = stage.stageNumber <= max(1, completedScenarioIds.count + 1)
                    let isCompleted = completedScenarioIds.contains(stage.targetContentId) || (stage.stageNumber < completedScenarioIds.count + 1)

                    HStack {
                        if index % 2 == 1 { Spacer(minLength: 50) }

                        Button(action: {
                            if isUnlocked {
                                onSelectStage(stage)
                            }
                        }) {
                            StageNodeCircle(
                                stage: stage,
                                worldColor: worldColor,
                                isUnlocked: isUnlocked,
                                isCompleted: isCompleted
                            )
                        }
                        .buttonStyle(.plain)
                        .disabled(!isUnlocked)

                        if index % 2 == 0 { Spacer(minLength: 50) }
                    }
                    .padding(.horizontal, 28)
                }
            }
        }
    }
}

public struct StageNodeCircle: View {
    public let stage: QuestStage
    public let worldColor: Color
    public let isUnlocked: Bool
    public let isCompleted: Bool

    public var body: some View {
        HStack(spacing: 14) {
            ZStack {
                // Outer glow ring
                Circle()
                    .fill(isUnlocked ? (stage.isBossStage ? Color.red : worldColor) : Color(.systemGray4))
                    .frame(width: stage.isBossStage ? 66 : 56, height: stage.isBossStage ? 66 : 56)
                    .shadow(color: isUnlocked ? (stage.isBossStage ? Color.red.opacity(0.5) : worldColor.opacity(0.4)) : Color.clear, radius: 8, x: 0, y: 3)

                Circle()
                    .fill(Color.white)
                    .frame(width: stage.isBossStage ? 56 : 46, height: stage.isBossStage ? 56 : 46)

                if isUnlocked {
                    Image(systemName: isCompleted ? "checkmark.seal.fill" : stage.iconName)
                        .font(.system(size: stage.isBossStage ? 22 : 18, weight: .bold))
                        .foregroundColor(isCompleted ? .green : (stage.isBossStage ? .red : worldColor))
                } else {
                    Image(systemName: "lock.fill")
                        .font(.system(size: 16))
                        .foregroundColor(.gray)
                }
            }

            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 6) {
                    Text("STAGE \(stage.stageNumber)")
                        .font(.system(size: 9, weight: .heavy))
                        .foregroundColor(isUnlocked ? worldColor : .secondary)

                    if stage.isBossStage {
                        Text("BOSS")
                            .font(.system(size: 8, weight: .black))
                            .padding(.horizontal, 4)
                            .padding(.vertical, 1)
                            .background(Color.red)
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }

                    if isCompleted {
                        Text("⭐⭐⭐")
                            .font(.system(size: 9))
                    }
                }

                Text(stage.stageTitleJa)
                    .font(.system(size: 14, weight: .bold))
                    .foregroundColor(isUnlocked ? .primary : .secondary)

                Text(stage.targetSkill)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(.ultraThinMaterial)
            .cornerRadius(12)
        }
    }
}

public struct StageLauncherModal: View {
    public let stage: QuestStage
    @Environment(\.dismiss) var dismiss
    @ObservedObject var dataManager = DataManager.shared

    public var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                // Header
                VStack(spacing: 8) {
                    Image(systemName: stage.iconName)
                        .font(.system(size: 44))
                        .foregroundColor(stage.isBossStage ? .red : .accentColor)

                    Text(stage.stageTitleJa)
                        .font(.title2)
                        .fontWeight(.black)

                    Text(stage.stageTitle)
                        .font(.subheadline)
                        .foregroundColor(.secondary)

                    HStack(spacing: 8) {
                        Text("World: \(stage.worldNameJa)")
                            .font(.caption)
                            .fontWeight(.semibold)
                        Text("• JF \(stage.jfLevel)")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.green)
                        Text("• +\(stage.xpReward) XP")
                            .font(.caption)
                            .fontWeight(.heavy)
                            .foregroundColor(.orange)
                    }
                    .padding(.top, 4)
                }
                .padding()

                Divider().padding(.horizontal)

                // Content Launcher
                VStack(spacing: 12) {
                    if let scenario = dataManager.scenarios.first(where: { $0.id == stage.targetContentId }) {
                        ScenarioCard(scenario: scenario, isCompleted: false)
                            .padding(.horizontal)
                        NavigationLink(destination: ScenarioDetailView(scenario: scenario)) {
                            Text("Launch Scenario Challenge ➔")
                                .font(.headline)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.accentColor)
                                .foregroundColor(.white)
                                .cornerRadius(14)
                        }
                        .padding(.horizontal)
                    } else if let battle = dataManager.dojoBattles.first(where: { $0.id == stage.targetContentId }) {
                        DojoBattleCard(battle: battle)
                            .padding(.horizontal)
                        NavigationLink(destination: DojoBattleGameView(battle: battle)) {
                            Text("Enter Dojo Speed Duel ➔")
                                .font(.headline)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.red)
                                .foregroundColor(.white)
                                .cornerRadius(14)
                        }
                        .padding(.horizontal)
                    } else if let manga = dataManager.mangaLessons.first(where: { $0.id == stage.targetContentId }) {
                        MangaLessonCard(lesson: manga, isCompleted: false)
                            .padding(.horizontal)
                        NavigationLink(destination: MangaPanelReaderView(lesson: manga)) {
                            Text("Read Manga Panels ➔")
                                .font(.headline)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.purple)
                                .foregroundColor(.white)
                                .cornerRadius(14)
                        }
                        .padding(.horizontal)
                    } else {
                        Text("Ready to start this Tokyo milestone.")
                            .font(.footnote)
                            .foregroundColor(.secondary)
                    }
                }

                Spacer()
            }
            .navigationTitle("Stage \(stage.stageNumber)")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
            }
        }
    }
}

