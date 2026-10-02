import SwiftUI
import Combine

public struct TokyoScenarioDailyPackageView: View {
    public let package: TokyoDailyScenarioPackage
    @Environment(\.dismiss) private var dismiss
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @ObservedObject private var gamification = GamificationService.shared
    @ObservedObject private var languageManager = LanguageManager.shared
    
    @State private var currentStep: Int = 0 // 0: Dialogue, 1: Breakdown, 2: Video, 3: Golden Phrase
    @State private var timeRemainingSeconds: Int = 300 // 5-minute timebox
    @State private var timerActive: Bool = true
    @State private var showCelebration: Bool = false
    
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    public init(package: TokyoDailyScenarioPackage) {
        self.package = package
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 0) {
                    // Top Progress & 5-Min Timebox Header
                    headerBar

                    // Content Body
                    ScrollView {
                        VStack(spacing: 20) {
                            switch currentStep {
                            case 0:
                                stepOneDialogueView
                            case 1:
                                stepTwoAnalysisView
                            case 2:
                                stepThreeVideoView
                            case 3:
                                stepFourShadowingView
                            default:
                                EmptyView()
                            }
                        }
                        .padding(.horizontal)
                        .padding(.top, 16)
                        .padding(.bottom, 36)
                    }

                    // Bottom Navigation Action Ribbon
                    bottomActionBar
                }
            }
            .navigationTitle(package.title)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button(languageManager.isEnglish ? "Close" : "关闭") { dismiss() }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    HStack(spacing: 4) {
                        Image(systemName: "location.fill")
                            .font(.caption2)
                            .foregroundColor(.accentColor)
                        Text(package.locationTag)
                            .font(.caption2)
                            .fontWeight(.bold)
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.accentColor.opacity(0.12))
                    .cornerRadius(8)
                }
            }
            .onReceive(timer) { _ in
                if timerActive && timeRemainingSeconds > 0 {
                    timeRemainingSeconds -= 1
                }
            }
            .sheet(isPresented: $showCelebration) {
                completionModal
            }
        }
    }

    // MARK: - Header Bar
    private var headerBar: some View {
        VStack(spacing: 8) {
            HStack {
                // Step Indicator
                HStack(spacing: 6) {
                    ForEach(0..<4) { idx in
                        Circle()
                            .fill(idx <= currentStep ? Color.accentColor : Color.secondary.opacity(0.3))
                            .frame(width: 8, height: 8)
                    }
                    Text("Step \(currentStep + 1)/4")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                }

                Spacer()

                // 5-Min Countdown Timer
                HStack(spacing: 4) {
                    Image(systemName: "timer")
                        .foregroundColor(timeRemainingSeconds < 60 ? .red : .orange)
                    Text(timeFormatted(timeRemainingSeconds))
                        .font(.system(size: 13, weight: .bold, design: .monospaced))
                        .foregroundColor(timeRemainingSeconds < 60 ? .red : .primary)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color(UIColor.secondarySystemBackground))
                .cornerRadius(8)
            }

            // Step Category Title
            HStack {
                Text(stepTitle(currentStep))
                    .font(.caption)
                    .fontWeight(.heavy)
                    .foregroundColor(.accentColor)
                    .tracking(1.0)
                Spacer()
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 10)
        .background(Color(UIColor.secondarySystemBackground).opacity(0.85))
    }

    // MARK: - Step 1: Real-World Scenario Dialogue
    private var stepOneDialogueView: some View {
        VStack(alignment: .leading, spacing: 16) {
            VStack(alignment: .leading, spacing: 6) {
                Text(languageManager.isEnglish ? "1. Practical Scene Dialogue" : "1. 实战场景对话")
                    .font(.headline)
                    .fontWeight(.black)
                Text(languageManager.isEnglish ? (package.sceneSummaryEn.isEmpty ? package.sceneSummaryZh : package.sceneSummaryEn) : (package.sceneSummaryZh.isEmpty ? package.sceneSummaryEn : package.sceneSummaryZh))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            ForEach(package.sceneDialogue) { line in
                VStack(alignment: .leading, spacing: 6) {
                    HStack {
                        Text(line.speaker)
                            .font(.system(size: 11, weight: .heavy))
                            .foregroundColor(.purple)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.purple.opacity(0.12))
                            .cornerRadius(6)

                        Spacer()

                        Button {
                            voiceBank.playNativeAudio(text: line.japanese)
                        } label: {
                            Image(systemName: "speaker.wave.2.fill")
                                .font(.caption)
                                .foregroundColor(.accentColor)
                        }
                    }

                    TokyoKaraokeSentenceView(
                        sentenceJa: line.japanese,
                        furiganaText: line.furigana,
                        translation: languageManager.isEnglish ? line.english : (line.chinese.isEmpty ? line.english : line.chinese),
                        showFurigana: true,
                        fontScale: 1.05
                    )
                }
                .padding(14)
                .background(Color(UIColor.secondarySystemBackground).opacity(0.7))
                .cornerRadius(14)
            }
        }
    }

    // MARK: - Step 2: Vocabulary & Grammar Dissection
    private var stepTwoAnalysisView: some View {
        VStack(alignment: .leading, spacing: 16) {
            VStack(alignment: .leading, spacing: 4) {
                Text(languageManager.isEnglish ? "2. Vocabulary & Grammar Analysis" : "2. 核心语汇与文法精讲")
                    .font(.headline)
                    .fontWeight(.black)
                Text(languageManager.isEnglish ? "Practical grammar connections, Romaji, and nuanced usage" : "日常会话即学即用的文法句式与实战要点解析")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            ForEach(package.vocabGrammarAnalyses) { item in
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(item.japanese)
                                .font(.system(size: 18, weight: .black, design: .rounded))
                                .foregroundColor(.primary)

                            Text(item.romaji)
                                .font(.system(size: 12, weight: .semibold, design: .monospaced))
                                .foregroundColor(.purple)
                        }

                        Spacer()

                        Button {
                            voiceBank.playNativeAudio(text: item.japanese)
                        } label: {
                            Image(systemName: "speaker.wave.2.fill")
                                .font(.title3)
                                .foregroundColor(.accentColor)
                        }
                    }

                    Divider()

                    VStack(alignment: .leading, spacing: 6) {
                        HStack(alignment: .top) {
                            Text(languageManager.isEnglish ? "Meaning:" : "释义：")
                                .font(.system(size: 12, weight: .bold))
                                .foregroundColor(.secondary)
                            Text(languageManager.isEnglish ? item.englishMeaning : (item.chineseMeaning.isEmpty ? item.englishMeaning : item.chineseMeaning))
                                .font(.system(size: 13, weight: .semibold))
                                .foregroundColor(.primary)
                        }

                        let grammarText = languageManager.isEnglish ? item.grammarRule : (item.grammarRuleZh.isEmpty ? item.grammarRule : item.grammarRuleZh)
                        if !grammarText.isEmpty {
                            HStack(alignment: .top) {
                                Text(languageManager.isEnglish ? "Grammar:" : "句式要点：")
                                    .font(.system(size: 12, weight: .bold))
                                    .foregroundColor(.secondary)
                                Text(grammarText)
                                    .font(.system(size: 12))
                                    .foregroundColor(.purple)
                            }
                        }

                        let tipText = languageManager.isEnglish ? item.practicalTip : (item.practicalTipZh.isEmpty ? item.practicalTip : item.practicalTipZh)
                        if !tipText.isEmpty {
                            HStack(alignment: .top) {
                                Text(languageManager.isEnglish ? "Tokyo Tip:" : "实战贴士：")
                                    .font(.system(size: 12, weight: .bold))
                                    .foregroundColor(.secondary)
                                Text(tipText)
                                    .font(.system(size: 12))
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                }
                .padding(16)
                .background(Color(UIColor.secondarySystemBackground).opacity(0.85))
                .cornerRadius(16)
            }
        }
    }

    // MARK: - Step 3: Fast Native Video Lesson
    private var stepThreeVideoView: some View {
        VStack(alignment: .leading, spacing: 16) {
            VStack(alignment: .leading, spacing: 4) {
                Text(languageManager.isEnglish ? "3. Video Masterclass" : "3. 沉浸式场景视频精讲")
                    .font(.headline)
                    .fontWeight(.black)
                Text(package.videoTitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            TokyoFastVideoPlayerContainer(
                videoId: package.youtubeVideoId,
                title: package.videoTitle
            )

            VStack(alignment: .leading, spacing: 8) {
                Text(languageManager.isEnglish ? "Key Takeaways (5-Min Masterclass)" : "要点指引（5分钟速通极意）")
                    .font(.subheadline)
                    .fontWeight(.bold)
                Text(languageManager.isEnglish ? "1. Listen to native Tokyo pitch accents, cadence & natural pauses\n2. Shadow along with synced typography & subtitles\n3. Build authentic conversational intuition in real Tokyo contexts" : "1. 聆听东京母语原声的真实抑扬顿挫与声调停顿\n2. 紧随原文字幕进行影子跟读（即时声音复述训练）\n3. 结合东京街头实景建立自然语感与条件反射")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineSpacing(4)
            }
            .padding(14)
            .background(Color(UIColor.secondarySystemBackground).opacity(0.7))
            .cornerRadius(14)
        }
    }

    // MARK: - Step 4: YouTube Shorts Follow-Along Shadowing Sprint
    private var stepFourShadowingView: some View {
        VStack(alignment: .leading, spacing: 18) {
            VStack(alignment: .leading, spacing: 4) {
                Text(languageManager.isEnglish ? "4. Golden Phrase Shadowing (YT Shorts Standard)" : "4. 黄金核心句即时定着（跟读定着）")
                    .font(.headline)
                    .fontWeight(.black)
                Text(languageManager.isEnglish ? "Repeat aloud with native Japanese rhythm, pitch accent, and live recording review" : "紧随卡拉OK高亮开口跟读，录音对比真人发音，强化口语肌肉记忆")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            TokyoFollowAlongShadowingCardView(
                title: languageManager.isEnglish ? "GOLDEN PHRASE SHADOWING" : "黄金核心句跟读定着",
                subtitle: languageManager.isEnglish ? "Repeat aloud with native timing & pitch accent" : "跟随真人原声节奏与声调开口复述",
                categoryTag: "\(package.locationTag) • " + (languageManager.isEnglish ? "Daily Essential" : "今日核心必修"),
                sentenceJa: package.goldenSentence,
                furiganaText: package.goldenSentenceFurigana,
                translation: languageManager.isEnglish ? (package.goldenSentenceMeaning.isEmpty ? package.goldenSentenceMeaningZh : package.goldenSentenceMeaning) : (package.goldenSentenceMeaningZh.isEmpty ? package.goldenSentenceMeaning : package.goldenSentenceMeaningZh),
                romaji: package.goldenSentenceRomaji,
                proTip: languageManager.isEnglish ? "Pay attention to native Tokyo intonation and vocal cadence." : "注意东京标准语的句尾轻音与自然停顿连读。",
                onCompleted: {
                    UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
                    gamification.addRewards(tp: 20, exp: 30)
                }
            )
        }
    }

    // MARK: - Bottom Action Bar
    private var bottomActionBar: some View {
        HStack(spacing: 12) {
            if currentStep > 0 {
                Button {
                    withAnimation { currentStep -= 1 }
                } label: {
                    Image(systemName: "chevron.left")
                        .font(.headline)
                        .foregroundColor(.primary)
                        .frame(width: 48, height: 48)
                        .background(Color(UIColor.secondarySystemBackground))
                        .cornerRadius(14)
                }
            }

            Button {
                if currentStep < 3 {
                    withAnimation { currentStep += 1 }
                } else {
                    UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
                    gamification.addRewards(tp: 30, exp: 45)
                    gamification.recordMicroLearningTime(minutes: 5)
                    showCelebration = true
                }
            } label: {
                HStack(spacing: 8) {
                    Text(currentStep < 3 ? (LanguageManager.shared.isEnglish ? "Next Step" : "下一步") : (LanguageManager.shared.isEnglish ? "Complete Session (+30 TP)" : "完成今日学习 (+30 TP)"))
                        .font(.headline)
                        .fontWeight(.heavy)
                }
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(
                    LinearGradient(
                        colors: currentStep < 3 ? [Color.blue, Color.purple] : [Color.green, Color.teal],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .cornerRadius(14)
                .shadow(color: Color.purple.opacity(0.3), radius: 6, y: 3)
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 12)
        .background(.ultraThinMaterial)
    }

    // MARK: - Completion Modal
    private var completionModal: some View {
        VStack(spacing: 20) {
            Spacer()
            Image(systemName: "checkmark.seal.fill")
                .font(.system(size: 64))
                .foregroundColor(.green)

            Text(LanguageManager.shared.isEnglish ? "Scenario Sprint Completed" : "今日场景实战已通关")
                .font(.title2)
                .fontWeight(.black)

            Text(LanguageManager.shared.isEnglish ? "You've mastered today's Tokyo daily scenario \"\(package.title)\".\nEarned +30 TP & +45 EXP!" : "已通关今日东京实战场景「\(package.title)」！\n获得 +30 TP 与 +45 EXP 经验值奖励。")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 24)

            Button(LanguageManager.shared.isEnglish ? "Finish" : "完成并返回") {
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

    private func stepTitle(_ step: Int) -> String {
        let isEn = LanguageManager.shared.isEnglish
        switch step {
        case 0: return isEn ? "STEP 1/4 • SCENARIO DIALOGUE" : "第 1/4 步 • 实战场景对话"
        case 1: return isEn ? "STEP 2/4 • VOCAB & GRAMMAR" : "第 2/4 步 • 核心语汇与文法"
        case 2: return isEn ? "STEP 3/4 • VIDEO MASTERCLASS" : "第 3/4 步 • 视频大师课"
        case 3: return isEn ? "STEP 4/4 • SHADOWING SPRINT" : "第 4/4 步 • 黄金句跟读定着"
        default: return ""
        }
    }

    private func timeFormatted(_ totalSeconds: Int) -> String {
        let mins = totalSeconds / 60
        let secs = totalSeconds % 60
        return String(format: "%02d:%02d", mins, secs)
    }
}
