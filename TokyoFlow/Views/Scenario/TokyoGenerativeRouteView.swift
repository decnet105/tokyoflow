import SwiftUI

public struct TokyoGenerativeRouteView: View {
    @StateObject private var engine = TokyoGenerativeLearningEngine.shared
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @ObservedObject private var gamification = GamificationService.shared
    @State private var customPrompt: String = ""
    @State private var showCustomInput: Bool = false
    @State private var showFurigana: Bool = true
    @State private var copiedPhrase: String? = nil

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Header Banner
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Label("NEXT DESTINATION • GENERATIVE LEARNING", systemImage: "sparkles")
                                    .font(.system(size: 10, weight: .black))
                                    .foregroundColor(.accentColor)
                                    .tracking(1.5)
                                Spacer()
                                Text("AI Dynamic")
                                    .font(.system(size: 10, weight: .bold))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.accentColor.opacity(0.12))
                                    .foregroundColor(.accentColor)
                                    .cornerRadius(6)
                            }

                            Text("Next Tokyo Destination?")
                                .font(.system(size: 22, weight: .black, design: .rounded))

                            Text("Select a popular Tokyo hotspot or enter a custom destination to dynamically generate survival phrases, native audio, situational dialogues, and etiquette tips.")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Preset Destination Horizontal Carousel
                        VStack(alignment: .leading, spacing: 10) {
                            HStack {
                                Text("Popular Tokyo Spots")
                                    .font(.system(size: 13, weight: .bold))
                                Spacer()
                                Button(action: { showCustomInput.toggle() }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: showCustomInput ? "xmark.circle.fill" : "plus.circle.fill")
                                        Text(showCustomInput ? "Close Custom" : "Custom Spot")
                                    }
                                    .font(.system(size: 12, weight: .bold))
                                    .foregroundColor(.accentColor)
                                }
                            }
                            .padding(.horizontal)

                            ScrollView(.horizontal, showsIndicators: false) {
                                HStack(spacing: 10) {
                                    ForEach(engine.presetDestinations, id: \.id) { dest in
                                        Button(action: {
                                            engine.generatePlan(for: dest.id)
                                            gamification.addRewards(tp: 5, exp: 10)
                                        }) {
                                            HStack(spacing: 6) {
                                                Image(systemName: dest.icon)
                                                    .font(.system(size: 13))
                                                VStack(alignment: .leading, spacing: 1) {
                                                    Text(dest.name)
                                                        .font(.system(size: 12, weight: .bold))
                                                    Text(dest.district)
                                                        .font(.system(size: 9))
                                                        .foregroundColor(.secondary)
                                                }
                                            }
                                            .padding(.horizontal, 12)
                                            .padding(.vertical, 8)
                                            .background(engine.selectedPresetId == dest.id ? Color.accentColor : Color(.secondarySystemGroupedBackground))
                                            .foregroundColor(engine.selectedPresetId == dest.id ? .white : .primary)
                                            .cornerRadius(14)
                                            .shadow(color: Color.black.opacity(0.03), radius: 4, x: 0, y: 1)
                                        }
                                        .buttonStyle(.plain)
                                    }
                                }
                                .padding(.horizontal)
                            }
                        }

                        // Custom Prompt Input Bar
                        if showCustomInput {
                            VStack(alignment: .leading, spacing: 8) {
                                Text("Enter your desired spot or situation:")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                HStack {
                                    Image(systemName: "magnifyingglass")
                                        .foregroundColor(.secondary)
                                    TextField("e.g., Odaiba Gundam, Harajuku Crepe, Tokyo Tower night view...", text: $customPrompt)
                                        .textFieldStyle(.plain)
                                    if !customPrompt.isEmpty {
                                        Button("Generate") {
                                            engine.generateCustomPlan(userPrompt: customPrompt)
                                            gamification.addRewards(tp: 10, exp: 15)
                                        }
                                        .font(.system(size: 12, weight: .bold))
                                        .foregroundColor(.accentColor)
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 4)
                                        .background(Color.accentColor.opacity(0.15))
                                        .cornerRadius(8)
                                    }
                                }
                                .padding(10)
                                .background(Color(.secondarySystemGroupedBackground))
                                .cornerRadius(12)
                            }
                            .padding(.horizontal)
                            .transition(.opacity.combined(with: .move(edge: .top)))
                        }

                        // Dynamic Content Area
                        if engine.isGenerating {
                            VStack(spacing: 12) {
                                ProgressView()
                                    .scaleEffect(1.2)
                                Text("Generating real-time Tokyo learning roadmap...")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 40)
                        } else if let plan = engine.currentPlan {
                            VStack(spacing: 18) {
                                // Destination Summary Card
                                VStack(alignment: .leading, spacing: 10) {
                                    HStack {
                                        Image(systemName: plan.categoryIcon)
                                            .foregroundColor(.accentColor)
                                            .font(.title3)
                                        VStack(alignment: .leading, spacing: 2) {
                                            Text(plan.destinationName)
                                                .font(.headline)
                                                .fontWeight(.bold)
                                            Text(plan.destinationJa)
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }
                                        Spacer()
                                        Text(plan.tag)
                                            .font(.system(size: 10, weight: .bold))
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 3)
                                            .background(Color.green.opacity(0.15))
                                            .foregroundColor(.green)
                                            .cornerRadius(8)
                                    }

                                    Text(plan.overview)
                                        .font(.footnote)
                                        .foregroundColor(.secondary)

                                    // Challenge Mission Box
                                    HStack(spacing: 6) {
                                        Image(systemName: "flag.fill")
                                            .foregroundColor(.orange)
                                            .font(.caption)
                                        Text("Field Mission: \(plan.challengeMission)")
                                            .font(.system(size: 11, weight: .medium))
                                            .foregroundColor(.primary)
                                    }
                                    .padding(8)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(Color.orange.opacity(0.10))
                                    .cornerRadius(8)
                                }
                                .padding(16)
                                .background(Color(.secondarySystemGroupedBackground))
                                .cornerRadius(16)

                                // Section 1: Must-Know Survival Phrases
                                VStack(alignment: .leading, spacing: 12) {
                                    HStack {
                                        Label("1-Second Survival Phrases", systemImage: "sparkles")
                                            .font(.system(size: 14, weight: .bold))
                                        Spacer()
                                        Button(action: { showFurigana.toggle() }) {
                                            Text(showFurigana ? "Hide Furigana" : "Show Furigana")
                                                .font(.caption2)
                                                .foregroundColor(.accentColor)
                                        }
                                    }

                                    ForEach(plan.survivalPhrases) { phrase in
                                        GenerativePhraseCard(phrase: phrase, showFurigana: showFurigana)
                                    }
                                }

                                // Section 2: Real Situational Dialogue
                                VStack(alignment: .leading, spacing: 12) {
                                    Label("Situational Roleplay Dialogue", systemImage: "bubble.left.and.bubble.right.fill")
                                        .font(.system(size: 14, weight: .bold))

                                    VStack(spacing: 8) {
                                        ForEach(plan.scenarioDialogue) { turn in
                                            GenerativeDialogueBubble(turn: turn, showFurigana: showFurigana)
                                        }
                                    }
                                }

                                // Section 3: Cultural Do's & Don'ts
                                VStack(alignment: .leading, spacing: 8) {
                                    Label("Tokyo Field Etiquette & Pro-Tips", systemImage: "exclamationmark.shield.fill")
                                        .font(.system(size: 14, weight: .bold))
                                        .foregroundColor(.primary)

                                    VStack(alignment: .leading, spacing: 6) {
                                        ForEach(plan.culturalTips, id: \.self) { tip in
                                            HStack(alignment: .top, spacing: 6) {
                                                Image(systemName: "checkmark.circle.fill")
                                                    .foregroundColor(.green)
                                                    .font(.caption)
                                                    .padding(.top, 2)
                                                Text(tip)
                                                    .font(.caption)
                                                    .foregroundColor(.secondary)
                                            }
                                        }
                                    }
                                    .padding(12)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .background(Color(.secondarySystemGroupedBackground))
                                    .cornerRadius(12)
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                    .padding(.bottom, 30)
                }
            }
            .navigationTitle("Next Destination")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

public struct GenerativePhraseCard: View {
    public let phrase: GenerativePhrase
    public let showFurigana: Bool
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @ObservedObject private var gamification = GamificationService.shared

    public var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 2) {
                    if showFurigana {
                        Text(phrase.furigana)
                            .font(.system(size: 11))
                            .foregroundColor(.secondary)
                    }

                    Text(phrase.japanese)
                        .font(.system(size: 16, weight: .bold))
                        .foregroundColor(.primary)

                    Text(phrase.english)
                        .font(.system(size: 13))
                        .foregroundColor(.secondary)
                }

                Spacer()

                // Audio Play Button
                Button(action: {
                    voiceBank.playPhraseOrFallback(key: phrase.audioKey, fallbackText: phrase.japanese)
                    gamification.addRewards(tp: 2, exp: 5)
                    WeakWordTrackerService.shared.recordListen(word: phrase.japanese, reading: phrase.furigana, meaning: phrase.english)
                }) {
                    ZStack {
                        Circle()
                            .fill(Color.accentColor.opacity(0.12))
                            .frame(width: 36, height: 36)
                        Image(systemName: "speaker.wave.2.fill")
                            .font(.system(size: 14))
                            .foregroundColor(.accentColor)
                    }
                }
            }

            HStack {
                Text(phrase.pitchAccent)
                    .font(.system(size: 10, weight: .bold))
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.blue.opacity(0.12))
                    .foregroundColor(.blue)
                    .cornerRadius(4)

                Text(phrase.situationNote)
                    .font(.system(size: 10))
                    .foregroundColor(.secondary)
            }
        }
        .padding(12)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

public struct GenerativeDialogueBubble: View {
    public let turn: GenerativeDialogueTurn
    public let showFurigana: Bool
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared

    public var body: some View {
        HStack {
            if turn.isUser { Spacer() }

            VStack(alignment: turn.isUser ? .trailing : .leading, spacing: 2) {
                Text("\(turn.speaker) (\(turn.speakerRole))")
                    .font(.system(size: 10, weight: .bold))
                    .foregroundColor(.secondary)

                VStack(alignment: turn.isUser ? .trailing : .leading, spacing: 2) {
                    if showFurigana {
                        Text(turn.furigana)
                            .font(.system(size: 10))
                            .foregroundColor(.secondary)
                    }

                    Text(turn.japanese)
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(turn.isUser ? .white : .primary)

                    Text(turn.english)
                        .font(.system(size: 11))
                        .foregroundColor(turn.isUser ? Color.white.opacity(0.85) : .secondary)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
                .background(turn.isUser ? Color.accentColor : Color(.secondarySystemGroupedBackground))
                .cornerRadius(14)
                .onTapGesture {
                    voiceBank.playPhraseOrFallback(key: turn.japanese, fallbackText: turn.japanese)
                }
            }

            if !turn.isUser { Spacer() }
        }
    }
}
