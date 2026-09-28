import SwiftUI

public struct TokyoPackageRunnerView: View {
    @ObservedObject var engine = TokyoLearningPackageEngine.shared
    @ObservedObject var audioService = AudioService.shared
    @ObservedObject var gamification = GamificationService.shared
    @Environment(\.dismiss) private var dismiss
    @Environment(\.openURL) private var openURL

    @State private var currentIndex: Int = 0
    @State private var showCompletionCelebration: Bool = false
    @State private var selectedQuizOption: Int? = nil
    @State private var showQuizFeedback: Bool = false

    public init(startIndex: Int = 0) {
        self._currentIndex = State(initialValue: startIndex)
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                if let package = engine.currentPackage {
                    VStack(spacing: 0) {
                        // Top Mode & Step Progress Header
                        VStack(spacing: 10) {
                            HStack {
                                HStack(spacing: 6) {
                                    Image(systemName: package.mode.icon)
                                        .foregroundColor(Color(hex: package.mode.badgeColorHex))
                                    Text(headerBadgeTitle(package: package))
                                        .font(.system(size: 13, weight: .bold))
                                }
                                .padding(.horizontal, 10)
                                .padding(.vertical, 5)
                                .background(Color(hex: package.mode.badgeColorHex).opacity(0.15))
                                .cornerRadius(10)

                                Spacer()

                                Text("Step \(currentIndex + 1) of \(package.items.count)")
                                    .font(.system(size: 12, weight: .bold, design: .monospaced))
                                    .foregroundColor(.secondary)
                            }

                            // Progress Bar
                            GeometryReader { geo in
                                ZStack(alignment: .leading) {
                                    Capsule()
                                        .fill(Color.primary.opacity(0.08))
                                        .frame(height: 6)

                                    Capsule()
                                        .fill(
                                            LinearGradient(
                                                colors: [Color(hex: package.mode.badgeColorHex), Color.accentColor],
                                                startPoint: .leading,
                                                endPoint: .trailing
                                            )
                                        )
                                        .frame(width: max(8, geo.size.width * CGFloat(Double(currentIndex + 1) / Double(package.items.count))), height: 6)
                                        .animation(.spring(response: 0.35, dampingFraction: 0.75), value: currentIndex)
                                }
                            }
                            .frame(height: 6)
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)

                    TokyoDuoAdaptiveLayout(duoSplitRatio: 0.48) {
                        // Left Screen: Core Step Expression, Audio & Context Nuance
                        if currentIndex < package.items.count {
                            let item = package.items[currentIndex]

                            ScrollView {
                                VStack(spacing: 16) {
                                    // Step Category Badge
                                    HStack {
                                        Label(item.type.rawValue, systemImage: iconForType(item.type))
                                            .font(.system(size: 11, weight: .black))
                                            .foregroundColor(.accentColor)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(Color.accentColor.opacity(0.12))
                                            .cornerRadius(6)

                                        Spacer()

                                        if let pa = item.pitchAccent {
                                            Text(pa)
                                                .font(.system(size: 10, weight: .bold))
                                                .foregroundColor(.orange)
                                                .padding(.horizontal, 6)
                                                .padding(.vertical, 3)
                                                .background(Color.orange.opacity(0.15))
                                                .cornerRadius(6)
                                        }
                                    }

                                    // Connection Rule Display if Grammar Formula
                                    if let rule = item.connectionRule {
                                        HStack(spacing: 6) {
                                            Image(systemName: "arrow.triangle.merge")
                                                .font(.system(size: 11, weight: .bold))
                                                .foregroundColor(.blue)
                                            Text("Connection: \(rule)")
                                                .font(.system(size: 12, weight: .bold, design: .monospaced))
                                                .foregroundColor(.blue)
                                        }
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 6)
                                        .background(Color.blue.opacity(0.08))
                                        .cornerRadius(8)
                                    }

                                    // Primary Japanese Expression Display
                                    VStack(spacing: 8) {
                                        Text(item.furiganaText)
                                            .font(.system(size: 14))
                                            .foregroundColor(.secondary)
                                            .multilineTextAlignment(.center)

                                        Text(item.japaneseText)
                                            .font(.system(size: item.japaneseText.count > 15 ? 24 : 32, weight: .black, design: .rounded))
                                            .foregroundColor(.primary)
                                            .multilineTextAlignment(.center)
                                            .lineLimit(4)

                                        Text(item.englishMeaning)
                                            .font(.system(size: 15, weight: .semibold))
                                            .foregroundColor(.accentColor)
                                            .multilineTextAlignment(.center)
                                    }
                                    .padding(.vertical, 8)

                                    // Collocation Note if present
                                    if let col = item.collocation {
                                        HStack(spacing: 6) {
                                            Image(systemName: "link")
                                                .font(.system(size: 11))
                                                .foregroundColor(.teal)
                                            Text("Collocation: \(col)")
                                                .font(.system(size: 12, weight: .semibold))
                                                .foregroundColor(.teal)
                                        }
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 5)
                                        .background(Color.teal.opacity(0.1))
                                        .cornerRadius(8)
                                    }

                                    // VoiceBank Real Native Audio Button
                                    Button(action: {
                                        audioService.speak(text: item.audioKey)
                                    }) {
                                        HStack(spacing: 8) {
                                            Image(systemName: "speaker.wave.3.fill")
                                            Text("Listen Native Voice")
                                                .fontWeight(.bold)
                                        }
                                        .font(.system(size: 14))
                                        .foregroundColor(.white)
                                        .padding(.horizontal, 20)
                                        .padding(.vertical, 12)
                                        .background(
                                            LinearGradient(
                                                colors: [Color.accentColor, Color.blue],
                                                startPoint: .leading,
                                                endPoint: .trailing
                                            )
                                        )
                                        .cornerRadius(14)
                                        .shadow(color: Color.accentColor.opacity(0.3), radius: 6, y: 3)
                                    }

                                    // Practical Nuance / Etiquette Tip
                                    if let tip = item.tip {
                                        HStack(alignment: .top, spacing: 10) {
                                            Image(systemName: "lightbulb.fill")
                                                .foregroundColor(.yellow)
                                                .font(.headline)
                                                .padding(.top, 2)

                                            VStack(alignment: .leading, spacing: 2) {
                                                Text("Tokyo Context & Exam Nuance")
                                                    .font(.system(size: 12, weight: .bold))
                                                    .foregroundColor(.primary)
                                                Text(tip)
                                                    .font(.caption)
                                                    .foregroundColor(.secondary)
                                            }
                                            Spacer()
                                        }
                                        .padding(14)
                                        .background(Color.yellow.opacity(0.1))
                                        .cornerRadius(12)
                                    }
                                }
                                .padding(16)
                                .background(.ultraThinMaterial)
                                .cornerRadius(20)
                                .padding(12)
                            }
                        }
                    } secondaryContent: {
                        // Right Screen: Interactive Quiz / Video / Step Progress & Actions
                        if currentIndex < package.items.count {
                            let item = package.items[currentIndex]

                            VStack(spacing: 0) {
                                ScrollView {
                                    VStack(spacing: 16) {
                                        // Exam Trap Quiz Interactive Options if type == .examTrapQuiz
                                        if let options = item.quizOptions, let correctIdx = item.quizCorrectIndex {
                                            VStack(alignment: .leading, spacing: 10) {
                                                Text("Select the correct choice:")
                                                    .font(.system(size: 13, weight: .bold))
                                                    .foregroundColor(.secondary)

                                                ForEach(0..<options.count, id: \.self) { idx in
                                                    Button(action: {
                                                        if !showQuizFeedback {
                                                            selectedQuizOption = idx
                                                            showQuizFeedback = true
                                                        }
                                                    }) {
                                                        HStack {
                                                            Text("\(idx + 1). \(options[idx])")
                                                                .font(.system(size: 14, weight: .semibold))
                                                            Spacer()
                                                            if showQuizFeedback {
                                                                if idx == correctIdx {
                                                                    Image(systemName: "checkmark.circle.fill")
                                                                        .foregroundColor(.green)
                                                                } else if selectedQuizOption == idx {
                                                                    Image(systemName: "xmark.circle.fill")
                                                                        .foregroundColor(.red)
                                                                }
                                                            }
                                                        }
                                                        .padding(12)
                                                        .background(quizOptionBg(idx: idx, correctIdx: correctIdx))
                                                        .foregroundColor(.primary)
                                                        .cornerRadius(10)
                                                    }
                                                }

                                                if showQuizFeedback, let exp = item.quizExplanation {
                                                    VStack(alignment: .leading, spacing: 4) {
                                                        Text(selectedQuizOption == correctIdx ? "✅ 正解 (Correct!)" : "⚠️ Pitfall Alert")
                                                            .font(.system(size: 12, weight: .bold))
                                                            .foregroundColor(selectedQuizOption == correctIdx ? .green : .red)
                                                        Text(exp)
                                                            .font(.system(size: 12))
                                                            .foregroundColor(.primary.opacity(0.9))
                                                    }
                                                    .padding(10)
                                                    .frame(maxWidth: .infinity, alignment: .leading)
                                                    .background(Color(UIColor.secondarySystemBackground))
                                                    .cornerRadius(10)
                                                }
                                            }
                                            .padding(14)
                                            .background(Color.purple.opacity(0.06))
                                            .cornerRadius(16)
                                        }

                                        // Video Player if available
                                        if let vid = item.youtubeVideoId {
                                            VStack(spacing: 8) {
                                                TokyoFastVideoPlayerContainer(videoId: vid, title: item.title)

                                                Button(action: {
                                                    if let appUrl = URL(string: "youtube://watch?v=\(vid)"),
                                                       UIApplication.shared.canOpenURL(appUrl) {
                                                        openURL(appUrl)
                                                    } else if let url = URL(string: "https://www.youtube.com/watch?v=\(vid)") {
                                                        openURL(url)
                                                    }
                                                }) {
                                                    HStack(spacing: 6) {
                                                        Image(systemName: "play.rectangle.fill")
                                                            .foregroundColor(.red)
                                                        Text("Watch Full Lesson on YouTube App (0-Lag)")
                                                            .font(.caption)
                                                            .fontWeight(.bold)
                                                    }
                                                    .padding(8)
                                                    .background(Color.red.opacity(0.1))
                                                    .cornerRadius(8)
                                                }
                                            }
                                        }
                                    }
                                    .padding(14)
                                }

                                // Bottom Navigation Controls
                                HStack(spacing: 16) {
                                    if currentIndex > 0 {
                                        Button(action: {
                                            withAnimation {
                                                currentIndex -= 1
                                                selectedQuizOption = nil
                                                showQuizFeedback = false
                                            }
                                        }) {
                                            HStack {
                                                Image(systemName: "arrow.left")
                                                Text("Back")
                                            }
                                            .font(.subheadline)
                                            .fontWeight(.bold)
                                            .foregroundColor(.secondary)
                                            .padding(.vertical, 14)
                                            .frame(maxWidth: .infinity)
                                            .background(.ultraThinMaterial)
                                            .cornerRadius(14)
                                        }
                                    }

                                    Button(action: {
                                        handleStepCompletion(package: package)
                                    }) {
                                        HStack {
                                            Text(currentIndex == package.items.count - 1 ? "Complete Package 🎉" : "Next Step (+15 TP)")
                                            Image(systemName: currentIndex == package.items.count - 1 ? "checkmark.seal.fill" : "arrow.right")
                                        }
                                        .font(.subheadline)
                                        .fontWeight(.black)
                                        .foregroundColor(.white)
                                        .padding(.vertical, 14)
                                        .frame(maxWidth: .infinity)
                                        .background(LinearGradient(colors: [.accentColor, .blue], startPoint: .leading, endPoint: .trailing))
                                        .cornerRadius(14)
                                        .shadow(color: Color.accentColor.opacity(0.35), radius: 8, y: 3)
                                    }
                                }
                                .padding(.horizontal)
                                .padding(.bottom, 20)
                                .padding(.top, 8)
                                .background(.ultraThinMaterial)
                            }
                        }
                    }
                }
            }
        }
        .navigationTitle("Adaptive Context Flow")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Close") { dismiss() }
            }
        }
        .alert("🎉 Context Package Completed!", isPresented: $showCompletionCelebration) {
            Button("Collect Rewards & Finish") {
                dismiss()
            }
        } message: {
            Text("You mastered today's context flow!\n+50 Tokyo Points • +60 EXP\nStreak continued! 🔥")
        }
    }
}

    private func handleStepCompletion(package: TokyoLearningPackage) {
        engine.completeCurrentItem()

        if currentIndex < package.items.count - 1 {
            withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                currentIndex += 1
                selectedQuizOption = nil
                showQuizFeedback = false
            }
        } else {
            gamification.addRewards(tp: 50, exp: 60)
            showCompletionCelebration = true
        }
    }

    private func headerBadgeTitle(package: TokyoLearningPackage) -> String {
        if let lvl = package.levelTrack {
            return "\(lvl.shortLabel) Sprint"
        }
        return package.mode.rawValue
    }

    private func quizOptionBg(idx: Int, correctIdx: Int) -> Color {
        if showQuizFeedback {
            if idx == correctIdx {
                return Color.green.opacity(0.15)
            } else if selectedQuizOption == idx {
                return Color.red.opacity(0.15)
            }
        } else if selectedQuizOption == idx {
            return Color.blue.opacity(0.12)
        }
        return Color(UIColor.secondarySystemBackground)
    }

    private func iconForType(_ type: PackageStepType) -> String {
        switch type {
        case .kanaAccent: return "character.book.closed.fill"
        case .spacedVocab: return "brain.head.profile"
        case .grammarFormula: return "function"
        case .goldenSentence: return "bubble.left.and.bubble.right.fill"
        case .scenarioVideo: return "play.tv.fill"
        case .newsShadowing: return "headphones"
        case .dojoReaction: return "bolt.shield.fill"
        case .examTrapQuiz: return "checkmark.circle.badge.questionmark"
        }
    }
}
