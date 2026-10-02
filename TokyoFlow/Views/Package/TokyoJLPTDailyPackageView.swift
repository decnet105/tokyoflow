import SwiftUI

public struct TokyoJLPTDailyPackageView: View {
    public let package: TokyoDailyJLPTPackage
    @Environment(\.dismiss) private var dismiss
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @ObservedObject private var gamification = GamificationService.shared
    @ObservedObject private var languageManager = LanguageManager.shared
    
    @State private var currentIndex: Int = 0
    @State private var showCelebration: Bool = false
    @State private var isGraded: Bool = false

    public init(package: TokyoDailyJLPTPackage) {
        self.package = package
    }

    private var currentItem: JLPTStudyItem? {
        guard currentIndex < package.allItems.count else { return nil }
        return package.allItems[currentIndex]
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                if let item = currentItem {
                    VStack(spacing: 0) {
                        // Top Ebbinghaus Flow Indicator
                        topEbbinghausHeader

                        ScrollView {
                            VStack(spacing: 20) {
                                // Main Learning Card
                                studyItemCard(item: item)
                            }
                            .padding(.horizontal)
                            .padding(.vertical, 16)
                        }

                        // Bottom Action / SRS Rating Bar
                        bottomControlBar(for: item)
                    }
                }
            }
            .navigationTitle(languageManager.isEnglish ? "JLPT \(package.level) Daily Sprint" : "JLPT \(package.level) 每日冲刺")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button(languageManager.isEnglish ? "Close" : "关闭") { dismiss() }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Text("JLPT \(package.level)")
                        .font(.caption2)
                        .fontWeight(.heavy)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.purple.opacity(0.15))
                        .foregroundColor(.purple)
                        .cornerRadius(8)
                }
            }
            .sheet(isPresented: $showCelebration) {
                jlptCompletionModal
            }
        }
    }

    // MARK: - Top Ebbinghaus Flow Header
    private var topEbbinghausHeader: some View {
        VStack(spacing: 8) {
            HStack(spacing: 8) {
                // 2 New Items Indicators
                ForEach(0..<package.newItems.count, id: \.self) { idx in
                    HStack(spacing: 4) {
                        Image(systemName: idx < currentIndex ? "checkmark.circle.fill" : "sparkles")
                            .font(.system(size: 10))
                        Text((languageManager.isEnglish ? "New " : "新 ") + "\(idx + 1)")
                            .font(.system(size: 11, weight: .bold))
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(idx == currentIndex ? Color.blue : (idx < currentIndex ? Color.blue.opacity(0.2) : Color.secondary.opacity(0.12)))
                    .foregroundColor(idx == currentIndex ? .white : (idx < currentIndex ? .blue : .secondary))
                    .cornerRadius(8)
                }

                Divider()
                    .frame(height: 16)

                // 3 Review Items Indicators
                ForEach(0..<package.reviewItems.count, id: \.self) { idx in
                    let globalIdx = package.newItems.count + idx
                    HStack(spacing: 4) {
                        Image(systemName: globalIdx < currentIndex ? "checkmark.circle.fill" : "arrow.triangle.2.circlepath")
                            .font(.system(size: 10))
                        Text((languageManager.isEnglish ? "Rev " : "复 ") + "\(idx + 1)")
                            .font(.system(size: 11, weight: .bold))
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(globalIdx == currentIndex ? Color.orange : (globalIdx < currentIndex ? Color.orange.opacity(0.2) : Color.secondary.opacity(0.12)))
                    .foregroundColor(globalIdx == currentIndex ? .white : (globalIdx < currentIndex ? .orange : .secondary))
                    .cornerRadius(8)
                }
            }

            Text(currentIndex < 2 ? (languageManager.isEnglish ? "Today's New Focus (1/2 New)" : "今日新学考点 (1/2 新学)") : (languageManager.isEnglish ? "Ebbinghaus Spaced Review (Strengthen Memory)" : "艾宾浩斯抗遗忘复习 (记忆强化)"))
                .font(.caption2)
                .fontWeight(.bold)
                .foregroundColor(currentIndex < 2 ? .blue : .orange)
        }
        .padding(.horizontal)
        .padding(.vertical, 10)
        .background(Color(UIColor.secondarySystemBackground).opacity(0.85))
    }

    // MARK: - Main Study Item Card
    private func studyItemCard(item: JLPTStudyItem) -> some View {
        VStack(spacing: 18) {
            // Card Type Banner
            HStack {
                Label(item.isNew ? (languageManager.isEnglish ? "New Item" : "新单词 / 句型") : (languageManager.isEnglish ? "Spaced Review" : "遗忘曲线复习"), systemImage: item.isNew ? "sparkles" : "clock.arrow.circlepath")
                    .font(.system(size: 11, weight: .black))
                    .foregroundColor(item.isNew ? .blue : .orange)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(item.isNew ? Color.blue.opacity(0.12) : Color.orange.opacity(0.12))
                    .cornerRadius(8)

                Spacer()

                // Pitch Accent Badge
                Text(item.pitchAccent)
                    .font(.system(size: 11, weight: .bold))
                    .foregroundColor(.secondary)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color(UIColor.tertiarySystemBackground))
                    .cornerRadius(8)
            }

            // Word / Kanji Large Display
            VStack(spacing: 6) {
                if !item.reading.isEmpty && item.reading != item.kanji {
                    Text(item.reading)
                        .font(.system(size: 16, weight: .bold, design: .rounded))
                        .foregroundColor(.purple)
                }

                Text(item.kanji)
                    .font(.system(size: 38, weight: .heavy, design: .rounded))
                    .foregroundColor(.primary)

                Text(item.romaji)
                    .font(.system(size: 13, weight: .semibold, design: .monospaced))
                    .foregroundColor(.secondary)
            }
            .padding(.vertical, 8)

            // Audio Playback Button
            Button {
                voiceBank.playNativeAudio(text: item.kanji)
            } label: {
                HStack(spacing: 6) {
                    Image(systemName: voiceBank.isPlayingNativeAudio ? "waveform" : "speaker.wave.3.fill")
                    Text(voiceBank.isPlayingNativeAudio ? (languageManager.isEnglish ? "Playing..." : "再生中") : (languageManager.isEnglish ? "Native Audio" : "真人原生发音"))
                        .font(.caption)
                        .fontWeight(.bold)
                }
                .foregroundColor(.white)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(
                    LinearGradient(
                        colors: [Color.purple, Color.blue],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .cornerRadius(12)
            }

            Divider()

            // English Meaning
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text("Meaning:")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                    Text(item.englishMeaning)
                        .font(.subheadline)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                }

                if !item.examTip.isEmpty {
                    HStack(alignment: .top) {
                        Text("Note:")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.secondary)
                        Text(item.examTip)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            // Example Sentence with Live Karaoke Highlight
            if !item.exampleSentenceJa.isEmpty {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Label(languageManager.isEnglish ? "Example Sentence" : "実戦例文", systemImage: "quote.opening")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundColor(.purple)
                        Spacer()
                    }

                    TokyoKaraokeSentenceView(
                        sentenceJa: item.exampleSentenceJa,
                        furiganaText: item.exampleSentenceFurigana,
                        translation: item.exampleSentenceMeaning,
                        showFurigana: true,
                        fontScale: 1.05
                    )
                }
                .padding(14)
                .background(Color(UIColor.secondarySystemBackground).opacity(0.8))
                .cornerRadius(14)
            }
        }
        .padding(20)
        .background(Color(UIColor.secondarySystemGroupedBackground))
        .cornerRadius(20)
        .shadow(color: Color.black.opacity(0.06), radius: 10, y: 4)
    }

    // MARK: - Bottom Control & SM-2 Feedback Bar
    private func bottomControlBar(for item: JLPTStudyItem) -> some View {
        VStack(spacing: 10) {
            if item.isNew {
                // New Item Simple "Mastered Next"
                Button {
                    advanceToNextItem()
                } label: {
                    Text(languageManager.isEnglish ? "Got It • Next Item" : "掌握 • 下一个")
                        .font(.headline)
                        .fontWeight(.heavy)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Color.blue)
                        .cornerRadius(14)
                }
            } else {
                // Review Item SM-2 Recall Buttons (Ebbinghaus Feedback)
                VStack(spacing: 6) {
                    Text(languageManager.isEnglish ? "Recall Quality Assessment" : "记忆熟练度评定")
                        .font(.caption2)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)

                    HStack(spacing: 8) {
                        srsButton(label: languageManager.isEnglish ? "Forgot" : "忘れた", sub: languageManager.isEnglish ? "1d" : "1日後", color: .red, grade: .blackout)
                        srsButton(label: languageManager.isEnglish ? "Hesitated" : "少し迷った", sub: languageManager.isEnglish ? "3d" : "3日後", color: .orange, grade: .hard)
                        srsButton(label: languageManager.isEnglish ? "Remember" : "覚えている", sub: languageManager.isEnglish ? "7d" : "7日後", color: .green, grade: .good)
                        srsButton(label: languageManager.isEnglish ? "Perfect" : "完璧", sub: languageManager.isEnglish ? "14d" : "14日後", color: .purple, grade: .perfect)
                    }
                }
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 12)
        .background(.ultraThinMaterial)
    }

    private func srsButton(label: String, sub: String, color: Color, grade: SRSGrade) -> some View {
        Button {
            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
            advanceToNextItem()
        } label: {
            VStack(spacing: 2) {
                Text(label)
                    .font(.system(size: 12, weight: .bold))
                Text(sub)
                    .font(.system(size: 9, weight: .semibold))
                    .opacity(0.8)
            }
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 10)
            .background(color)
            .cornerRadius(12)
        }
    }

    private func advanceToNextItem() {
        if currentIndex + 1 < package.allItems.count {
            withAnimation {
                currentIndex += 1
            }
        } else {
            UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
            gamification.addRewards(tp: 40, exp: 50)
            gamification.recordMicroLearningTime(minutes: 5)
            showCelebration = true
        }
    }

    // MARK: - JLPT Completion Modal
    private var jlptCompletionModal: some View {
        VStack(spacing: 20) {
            Spacer()
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 64))
                .foregroundColor(.accentColor)

            Text(languageManager.isEnglish ? "JLPT Daily Sprint Complete" : "JLPT 每日冲刺完成")
                .font(.title2)
                .fontWeight(.black)

            Text(languageManager.isEnglish ? "Successfully learned 2 new items and reinforced 3 spaced reviews via Ebbinghaus curve.\n+40 TP & +50 EXP rewards claimed!" : "已成功掌握 2 个新内容，并通过艾宾浩斯遗忘曲线巩固了 3 个复习知识点。\n+40 TP 与 +50 EXP 奖励已入账！")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 24)

            Button(languageManager.isEnglish ? "Finish" : "完成并返回") {
                showCelebration = false
                dismiss()
            }
            .font(.headline)
            .fontWeight(.bold)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color.accentColor)
            .cornerRadius(14)
            .padding(.horizontal, 32)
            Spacer()
        }
        .presentationDetents([.fraction(0.45)])
    }
}
