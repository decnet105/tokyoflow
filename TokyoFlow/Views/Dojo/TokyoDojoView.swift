import SwiftUI

public struct TokyoDojoView: View {
    @ObservedObject var dataManager = DataManager.shared
    @State private var activeBattle: DojoBattle? = nil

    public init() {}

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
                                    Text("TOKYO SURVIVAL DOJO")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.red)
                                        .tracking(1.5)
                                    Text("Real-Life Speed Battles")
                                        .font(.system(size: 26, weight: .bold, design: .rounded))
                                }
                                Spacer()
                                Image(systemName: "flame.circle.fill")
                                    .font(.system(size: 38))
                                    .foregroundColor(.red)
                            }

                            Text("Survive iconic Tokyo daily life trials: The Kombini 5-Question Barrage, Ramen Vending Machine Ciphers, and Izakaya Mystery Charges!")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Battles Cards List
                        LazyVStack(spacing: 16) {
                            ForEach(dataManager.dojoBattles) { battle in
                                Button(action: { activeBattle = battle }) {
                                    DojoBattleCard(battle: battle)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 24)
                }
            }
            .navigationTitle("Survival Dojo")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(item: $activeBattle) { battle in
                DojoBattleGameView(battle: battle)
            }
        }
    }
}

public struct DojoBattleCard: View {
    public let battle: DojoBattle

    public var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(battle.funTag)
                    .font(.caption2)
                    .fontWeight(.heavy)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 3)
                    .background(Color.red.opacity(0.12))
                    .foregroundColor(.red)
                    .cornerRadius(6)

                Spacer()

                Text(battle.difficulty)
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.orange)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(battle.title)
                    .font(.headline)
                    .foregroundColor(.primary)

                Text(battle.titleJa)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            Text(battle.scenarioSetup)
                .font(.footnote)
                .foregroundColor(.primary.opacity(0.85))
                .lineLimit(2)

            Divider()

            HStack {
                Label("\(battle.rounds.count) Rapid Rounds", systemImage: "bolt.fill")
                    .font(.caption2)
                    .foregroundColor(.secondary)

                Spacer()

                HStack(spacing: 4) {
                    Text("Start Speed Trial")
                        .font(.caption)
                        .fontWeight(.bold)
                    Image(systemName: "chevron.right")
                        .font(.caption2)
                }
                .foregroundColor(.red)
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
    }
}

public struct DojoBattleGameView: View {
    public let battle: DojoBattle
    @Environment(\.dismiss) var dismiss
    @ObservedObject var gamification = GamificationService.shared
    @State private var currentRoundIndex = 0
    @State private var selectedOption: DojoOption? = nil
    @State private var isShowingFeedback = false
    @State private var score = 0
    @State private var comboCount = 0
    @State private var isBattleComplete = false
    @State private var roundDuration: Double = 14.0
    @State private var timeRemaining: Double = 14.0
    @State private var timerEnabled = true
    @State private var timer: Timer?

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 18) {
                    if !isBattleComplete {
                        let round = battle.rounds[currentRoundIndex]

                        // Progress & Combo Header
                        VStack(spacing: 6) {
                            HStack {
                                Text("Round \(currentRoundIndex + 1) of \(battle.rounds.count)")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.secondary)

                                Spacer()

                                if comboCount > 1 {
                                    HStack(spacing: 4) {
                                        Image(systemName: "flame.fill")
                                            .foregroundColor(.orange)
                                        Text("COMBO x\(comboCount)!")
                                            .font(.caption)
                                            .fontWeight(.heavy)
                                            .foregroundColor(.orange)
                                    }
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color.orange.opacity(0.15))
                                    .cornerRadius(8)
                                }

                                HStack(spacing: 4) {
                                    Image(systemName: "star.fill")
                                        .foregroundColor(.yellow)
                                    Text("Score: \(score)")
                                        .font(.caption)
                                        .fontWeight(.heavy)
                                }
                            }

                            // Countdown Progress Bar
                            if timerEnabled && !isShowingFeedback {
                                HStack {
                                    ProgressView(value: timeRemaining, total: roundDuration)
                                        .tint(timeRemaining > 4.0 ? .green : .red)
                                        .scaleEffect(x: 1, y: 1.5, anchor: .center)

                                    Text("\(Int(ceil(timeRemaining)))s")
                                        .font(.system(size: 12, weight: .bold, design: .monospaced))
                                        .foregroundColor(timeRemaining > 4.0 ? .secondary : .red)
                                        .frame(width: 32)
                                }
                            }
                        }
                        .padding(.horizontal)
                        .padding(.top, 4)

                        // Cashier / Chef Speech Bubble
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Image(systemName: "person.crop.circle.badge.exclamationmark.fill")
                                    .foregroundColor(.red)
                                Text("Incoming Tokyo Prompt:")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.red)
                                Spacer()
                                AudioButton(textToSpeak: round.clerkPrompt, rate: 0.48)
                            }

                            Text(round.clerkPrompt)
                                .font(.system(size: 20, weight: .bold, design: .rounded))
                                .foregroundColor(.primary)

                            Text(round.clerkRomaji)
                                .font(.caption)
                                .foregroundColor(.secondary)

                            Text(round.clerkEnglish)
                                .font(.footnote)
                                .foregroundColor(.primary.opacity(0.85))
                        }
                        .padding(18)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(.ultraThinMaterial)
                        .cornerRadius(18)
                        .padding(.horizontal)

                        // Multiple Choice Options with Audio Preview Buttons
                        VStack(spacing: 10) {
                            ForEach(round.options) { option in
                                DojoOptionRowView(
                                    option: option,
                                    selectedOption: selectedOption,
                                    isShowingFeedback: isShowingFeedback,
                                    onSelect: { handleAnswerSelected(option) },
                                    onAudio: {
                                        AudioService.shared.speak(text: option.text, style: .dailyConversational, rate: 0.48)
                                    }
                                )
                            }
                        }
                        .padding(.horizontal)

                        // Feedback Explanation
                        if isShowingFeedback, let option = selectedOption {
                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Image(systemName: option.isCorrect ? "sparkles" : "exclamationmark.triangle.fill")
                                        .foregroundColor(option.isCorrect ? .green : .orange)
                                    Text(option.isCorrect ? "Ninja Accuracy! (+ \(100 * max(1, comboCount)) pts)" : "Tokyo Etiquette Note:")
                                        .font(.headline)
                                        .foregroundColor(option.isCorrect ? .green : .orange)
                                }
                                Text(option.nuance)
                                    .font(.footnote)
                                    .foregroundColor(.primary.opacity(0.9))
                            }
                            .padding(14)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(option.isCorrect ? Color.green.opacity(0.15) : Color.orange.opacity(0.15))
                            .cornerRadius(14)
                            .padding(.horizontal)

                            Button(action: nextRound) {
                                Text(currentRoundIndex < battle.rounds.count - 1 ? "Next Round ➔" : "View Ninja Mastery 🏆")
                                    .font(.headline)
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.red)
                                    .foregroundColor(.white)
                                    .cornerRadius(14)
                            }
                            .padding(.horizontal)
                        }

                        Spacer()
                    } else {
                        // Battle Complete Summary
                        VStack(spacing: 20) {
                            Image(systemName: "trophy.fill")
                                .font(.system(size: 60))
                                .foregroundColor(.orange)

                            VStack(spacing: 6) {
                                Text("Dojo Battle Cleared!")
                                    .font(.title)
                                    .fontWeight(.heavy)
                                Text("Final Score: \(score) Points (Max Combo: \(comboCount))")
                                    .font(.headline)
                                    .foregroundColor(.secondary)
                            }

                            // Master Combo Card
                            VStack(alignment: .leading, spacing: 10) {
                                HStack {
                                    Image(systemName: "bolt.shield.fill")
                                        .foregroundColor(.red)
                                    Text("TOKYO NINJA COMBO PHRASE")
                                        .font(.caption)
                                        .fontWeight(.bold)
                                        .foregroundColor(.red)
                                    Spacer()
                                    AudioButton(textToSpeak: battle.ninjaComboPhrase, rate: 0.48)
                                }

                                Text(battle.ninjaComboPhrase)
                                    .font(.system(size: 20, weight: .black, design: .rounded))
                                    .foregroundColor(.primary)

                                Text(battle.ninjaComboExplanation)
                                    .font(.footnote)
                                    .foregroundColor(.secondary)
                            }
                            .padding(18)
                            .background(.ultraThinMaterial)
                            .cornerRadius(18)
                            .padding(.horizontal)

                            Spacer()

                            Button(action: {
                                gamification.incrementQuestProgress(id: "q_dojo_battle")
                                gamification.addRewards(tp: 80, exp: 100)
                                dismiss()
                            }) {
                                Text("Complete & Claim Rewards")
                                    .font(.headline)
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.red)
                                    .foregroundColor(.white)
                                    .cornerRadius(14)
                            }
                            .padding(.horizontal)
                            .padding(.bottom)
                        }
                        .padding(.top, 40)
                    }
                }
            }
            .navigationTitle(battle.titleJa)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Exit") {
                        timer?.invalidate()
                        dismiss()
                    }
                }
            }
            .onAppear {
                startRoundTimer()
            }
            .onDisappear {
                timer?.invalidate()
            }
        }
    }

    private func handleAnswerSelected(_ option: DojoOption) {
        timer?.invalidate()
        selectedOption = option
        isShowingFeedback = true

        if option.isCorrect {
            comboCount += 1
            score += 100 * comboCount
        } else {
            comboCount = 0
        }

        #if os(iOS)
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(option.isCorrect ? .success : .error)
        #endif
    }

    private func startRoundTimer() {
        guard timerEnabled else { return }
        timer?.invalidate()
        timeRemaining = roundDuration

        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            if timeRemaining > 0 {
                timeRemaining -= 0.1
            } else {
                timer?.invalidate()
                if selectedOption == nil {
                    // Timeout
                    let round = battle.rounds[currentRoundIndex]
                    let wrong = round.options.first(where: { !$0.isCorrect }) ?? round.options[0]
                    handleAnswerSelected(wrong)
                }
            }
        }
    }

    private func nextRound() {
        selectedOption = nil
        isShowingFeedback = false
        if currentRoundIndex < battle.rounds.count - 1 {
            currentRoundIndex += 1
            startRoundTimer()
        } else {
            isBattleComplete = true
        }
    }
}

public struct DojoOptionRowView: View {
    public let option: DojoOption
    public let selectedOption: DojoOption?
    public let isShowingFeedback: Bool
    public let onSelect: () -> Void
    public let onAudio: () -> Void

    private var isSelected: Bool {
        selectedOption?.id == option.id
    }

    private var iconName: String {
        if isSelected {
            return option.isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill"
        }
        return "circle"
    }

    private var iconColor: Color {
        if isSelected {
            return option.isCorrect ? .green : .red
        }
        return .secondary
    }

    private var backgroundColor: Color {
        if isSelected {
            return option.isCorrect ? Color.green.opacity(0.15) : Color.red.opacity(0.15)
        }
        return Color.white.opacity(0.1)
    }

    private var borderColor: Color {
        if isSelected {
            return option.isCorrect ? Color.green : Color.red
        }
        return Color.clear
    }

    public var body: some View {
        HStack(alignment: .center, spacing: 10) {
            Button(action: onSelect) {
                HStack(alignment: .center, spacing: 10) {
                    Image(systemName: iconName)
                        .font(.title3)
                        .foregroundColor(iconColor)

                    Text(option.text)
                        .font(.system(size: 15, weight: .semibold))
                        .foregroundColor(.primary)
                        .multilineTextAlignment(.leading)

                    Spacer()
                }
            }
            .buttonStyle(.plain)
            .disabled(isShowingFeedback)

            Button(action: onAudio) {
                Image(systemName: "speaker.wave.2.fill")
                    .font(.caption)
                    .foregroundColor(.accentColor)
                    .padding(10)
                    .background(Color.accentColor.opacity(0.12))
                    .clipShape(Circle())
            }
        }
        .padding(12)
        .background(backgroundColor)
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(borderColor, lineWidth: 1.5)
        )
    }
}

