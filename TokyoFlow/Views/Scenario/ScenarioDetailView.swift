import SwiftUI

public struct ScenarioDetailView: View {
    public let scenario: Scenario
    @EnvironmentObject var userProfile: UserProfile
    @State private var showRoleplayModal = false
    @State private var showStickmanExplainer = false
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

                    // Stickman 60s Explainer CTA Button
                    Button(action: { showStickmanExplainer = true }) {
                        HStack(spacing: 6) {
                            Image(systemName: "figure.walk.motion")
                            Text("Watch 60s Stickman Hack")
                                .font(.system(size: 12, weight: .bold))
                            Spacer()
                            Image(systemName: "play.fill")
                                .font(.system(size: 10))
                        }
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background(Color.orange.opacity(0.15))
                        .foregroundColor(.orange)
                        .cornerRadius(10)
                    }
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
        .sheet(isPresented: $showStickmanExplainer) {
            NavigationStack {
                ScrollView {
                    StickmanPlayerView(
                        scenarioTitle: scenario.title,
                        frames: sampleStickmanFrames(for: scenario)
                    )
                    .padding()
                }
                .navigationTitle(scenario.titleJa)
                .navigationBarTitleDisplayMode(.inline)
            }
        }
    }

    private func sampleStickmanFrames(for s: Scenario) -> [StickmanFrame] {
        return [
            StickmanFrame(
                id: 1,
                title: "The Situation Setup",
                sceneType: "hook",
                characterPose: "confused",
                dialogueBubble: "「\(s.context)」",
                narrationJapanese: "東京の現場に到着！店員や駅員が話しかけてくる。",
                narrationEnglish: "You arrived at the scene. Native Tokyo staff approaches.",
                visualCue: "Tokyo background environment",
                accentColor: .orange
            ),
            StickmanFrame(
                id: 2,
                title: "The Rapid Question",
                sceneType: "rule",
                characterPose: "sweating",
                dialogueBubble: "「\(s.dialogue.first?.japanese ?? "いらっしゃいませ！")」",
                narrationJapanese: "早口な日本語で質問される。焦らずパターンを見極めよう。",
                narrationEnglish: "Rapid Tokyo Japanese incoming. Recognize the 1-2 key keywords.",
                visualCue: "Incoming speech bubble analysis",
                accentColor: .red
            ),
            StickmanFrame(
                id: 3,
                title: "The Native Tokyo Shortcut",
                sceneType: "shortcut",
                characterPose: "ninja_pose",
                dialogueBubble: "「\(s.keyVocabulary.first?.word ?? "大丈夫です")」",
                narrationJapanese: "地元民の魔法のひと言！一瞬で状況をスマートに解決。",
                narrationEnglish: "Deliver the native 1-line shortcut response.",
                visualCue: "Magic checkmark shines",
                accentColor: .green
            ),
            StickmanFrame(
                id: 4,
                title: "Can-Do Mastery Stamp",
                sceneType: "badge",
                characterPose: "confident",
                dialogueBubble: "「\(s.jfCanDoLevel) 達成！」",
                narrationJapanese: "これであなたも東京ローカル！パスポートにスタンプ獲得。",
                narrationEnglish: "Scenario cleared smoothly like a true Tokyo resident!",
                visualCue: "Passport stamp animation",
                accentColor: .blue
            )
        ]
    }
}

public struct DialogueBubbleView: View {
    public let line: DialogueLine
    public let showFurigana: Bool
    public let showTranslation: Bool
    public let speed: Float
    @ObservedObject private var audioService = AudioService.shared

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

                    if audioService.isSpeaking && audioService.currentSpeakingText == line.audioPrompt {
                        WaveformVisualizerView(height: 14, color: .accentColor)
                    }

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
