import SwiftUI

public struct ScenarioDetailView: View {
    public let scenario: Scenario
    @EnvironmentObject var userProfile: UserProfile
    @State private var showRoleplayModal = false
    @State private var showTranslations = true
    @State private var playbackSpeed: Float = 0.50

    public var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header Details
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Label(scenario.district, systemImage: "mappin.circle.fill")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.accentColor)
                        Text("• \(scenario.timeOfDay)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Spacer()
                        Text("JF Can-Do: \(scenario.jfCanDoLevel)")
                            .font(.caption2)
                            .fontWeight(.bold)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.green.opacity(0.15))
                            .foregroundColor(.green)
                            .cornerRadius(8)
                    }

                    Text(scenario.title)
                        .font(.title2)
                        .fontWeight(.bold)

                    Text(scenario.titleJa)
                        .font(.headline)
                        .foregroundColor(.secondary)

                    Text(scenario.context)
                        .font(.subheadline)
                        .foregroundColor(.primary.opacity(0.85))
                        .padding(.top, 4)
                }
                .padding()
                .background(Color(.secondarySystemGroupedBackground))
                .cornerRadius(16)
                .padding(.horizontal)

                // Cultural Tip Card (Tokyo Native Insight)
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Image(systemName: "lightbulb.fill")
                            .foregroundColor(.amberGold)
                        Text("Tokyo Life Etiquette & Hack")
                            .font(.headline)
                            .foregroundColor(.amberGold)
                    }
                    Text(scenario.culturalTip)
                        .font(.footnote)
                        .foregroundColor(.primary.opacity(0.9))
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.amberGold.opacity(0.10))
                .cornerRadius(14)
                .padding(.horizontal)

                // Controls Bar (Furigana / Translation / Audio Speed)
                HStack(spacing: 12) {
                    Button(action: { userProfile.furiganaEnabled.toggle() }) {
                        HStack(spacing: 4) {
                            Image(systemName: userProfile.furiganaEnabled ? "character.phonetic" : "character")
                            Text("Furigana: \(userProfile.furiganaEnabled ? "ON" : "OFF")")
                                .font(.caption)
                                .fontWeight(.semibold)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color(.systemGray5))
                        .cornerRadius(10)
                    }

                    Button(action: { showTranslations.toggle() }) {
                        HStack(spacing: 4) {
                            Image(systemName: "translate")
                            Text("Translation: \(showTranslations ? "ON" : "OFF")")
                                .font(.caption)
                                .fontWeight(.semibold)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color(.systemGray5))
                        .cornerRadius(10)
                    }

                    Spacer()

                    Menu {
                        Button("Slow (0.40x)") { playbackSpeed = 0.40 }
                        Button("Normal (0.50x)") { playbackSpeed = 0.50 }
                        Button("Native Tokyo (0.58x)") { playbackSpeed = 0.58 }
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: "speedometer")
                            Text(String(format: "%.2fx", playbackSpeed))
                                .font(.caption)
                                .fontWeight(.semibold)
                        }
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color.accentColor.opacity(0.12))
                        .foregroundColor(.accentColor)
                        .cornerRadius(10)
                    }
                }
                .padding(.horizontal)

                // Dialogue Flow
                VStack(alignment: .leading, spacing: 14) {
                    Text("SITUATIONAL DIALOGUE")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                        .tracking(1.2)
                        .padding(.horizontal)

                    ForEach(scenario.dialogue) { line in
                        DialogueBubbleView(
                            line: line,
                            showFurigana: userProfile.furiganaEnabled,
                            showTranslation: showTranslations,
                            speed: playbackSpeed
                        )
                        .padding(.horizontal)
                    }
                }

                // Interactive Roleplay Challenge CTA
                if scenario.interactiveChallenge != nil {
                    Button(action: { showRoleplayModal = true }) {
                        HStack {
                            Image(systemName: "play.circle.fill")
                                .font(.title3)
                            VStack(alignment: .leading, spacing: 2) {
                                Text("Interactive Roleplay Challenge")
                                    .font(.headline)
                                Text("Test your response in this Tokyo scenario")
                                    .font(.caption)
                                    .opacity(0.9)
                            }
                            Spacer()
                            Image(systemName: "chevron.right")
                        }
                        .padding()
                        .background(Color.accentColor)
                        .foregroundColor(.white)
                        .cornerRadius(16)
                    }
                    .padding(.horizontal)
                }

                // Key Vocabulary Section
                VStack(alignment: .leading, spacing: 12) {
                    Text("KEY SURVIVAL VOCABULARY")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                        .tracking(1.2)
                        .padding(.horizontal)

                    ForEach(scenario.keyVocabulary) { vocab in
                        VocabularyRowView(vocab: vocab, context: scenario.title)
                            .padding(.horizontal)
                    }
                }
            }
            .padding(.vertical)
        }
        .navigationTitle(scenario.district)
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showRoleplayModal) {
            if let challenge = scenario.interactiveChallenge {
                InteractiveRoleplayView(scenario: scenario, challenge: challenge)
            }
        }
    }
}

public struct DialogueBubbleView: View {
    public let line: DialogueLine
    public let showFurigana: Bool
    public let showTranslation: Bool
    public let speed: Float

    public var body: some View {
        HStack(alignment: .top, spacing: 10) {
            if line.isLearner {
                Spacer(minLength: 20)
            }

            VStack(alignment: line.isLearner ? .trailing : .leading, spacing: 6) {
                HStack(spacing: 6) {
                    Text(line.speaker)
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)

                    RegisterPill(register: line.register)

                    if !line.isLearner {
                        AudioButton(textToSpeak: line.audioPrompt, rate: speed)
                    }
                }

                VStack(alignment: line.isLearner ? .trailing : .leading, spacing: 4) {
                    FuriganaText(
                        textWithFurigana: line.furigana,
                        fallbackText: line.japanese,
                        showFurigana: showFurigana,
                        font: .system(size: 16, weight: .medium)
                    )

                    if showTranslation {
                        Text(line.romaji)
                            .font(.system(size: 12, design: .monospaced))
                            .foregroundColor(.secondary)
                        Text(line.english)
                            .font(.footnote)
                            .foregroundColor(.primary.opacity(0.85))
                        Text(line.chinese)
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }
                }
                .padding(14)
                .background(line.isLearner ? Color.accentColor.opacity(0.12) : Color(.secondarySystemGroupedBackground))
                .cornerRadius(16)

                if line.isLearner {
                    AudioButton(textToSpeak: line.audioPrompt, rate: speed)
                }
            }

            if !line.isLearner {
                Spacer(minLength: 20)
            }
        }
    }
}

public struct VocabularyRowView: View {
    public let vocab: KeyVocabulary
    public let context: String
    @EnvironmentObject var userProfile: UserProfile

    public var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 8) {
                    Text(vocab.word)
                        .font(.headline)
                    Text("【\(vocab.reading)】")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    Text(vocab.type)
                        .font(.caption2)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color(.systemGray5))
                        .cornerRadius(4)
                }
                Text(vocab.meaning)
                    .font(.footnote)
                    .foregroundColor(.secondary)
            }
            Spacer()
            AudioButton(textToSpeak: vocab.word)
            Button(action: {
                userProfile.toggleBookmark(
                    japanese: vocab.word,
                    reading: vocab.reading,
                    english: vocab.meaning,
                    context: context
                )
            }) {
                Image(systemName: userProfile.isBookmarked(vocab.word) ? "bookmark.fill" : "bookmark")
                    .foregroundColor(userProfile.isBookmarked(vocab.word) ? .orange : .secondary)
            }
        }
        .padding(12)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(12)
    }
}

extension Color {
    static let amberGold = Color(hex: "#D97706")
}
