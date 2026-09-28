import SwiftUI

public struct KanaTableView: View {
    @State private var isKatakana: Bool = false
    @State private var selectedCategory: KanaCategory = .seion
    @State private var selectedKana: KanaItem? = nil
    @State private var showQuizSheet: Bool = false
    @State private var activeDialogueKana: KanaItem? = nil
    @State private var dialogueTimerToken: UUID = UUID()

    @ObservedObject var audioService = AudioService.shared
    @ObservedObject var gamification = GamificationService.shared

    private let kanaData = KanaDataManager.shared

    private var currentList: [KanaItem] {
        switch selectedCategory {
        case .seion: return kanaData.seionList
        case .dakuon: return kanaData.dakuonList
        case .yoon: return kanaData.yoonList
        }
    }

    private let columns = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack(alignment: .bottom) {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 16) {
                        // Top Mode Switcher Banner
                        VStack(spacing: 12) {
                            HStack {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("JAPANESE SYLLABARY")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.accentColor)
                                        .tracking(1.5)
                                    Text(isKatakana ? "Katakana Table (カタカナ)" : "Hiragana Table (ひらがな)")
                                        .font(.system(size: 22, weight: .black, design: .rounded))
                                }

                                Spacer()

                                // Hiragana / Katakana Toggle
                                Button(action: {
                                    withAnimation(.spring(response: 0.35, dampingFraction: 0.7)) {
                                        isKatakana.toggle()
                                    }
                                }) {
                                    HStack(spacing: 6) {
                                        Text(isKatakana ? "あ ひらがな" : "ア カタカナ")
                                            .font(.caption)
                                            .fontWeight(.bold)
                                        Image(systemName: "arrow.triangle.2.circlepath")
                                            .font(.caption2)
                                    }
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 7)
                                    .background(Color.accentColor)
                                    .cornerRadius(12)
                                }
                            }

                            // Category Selector
                            Picker("Category", selection: $selectedCategory) {
                                ForEach(KanaCategory.allCases) { cat in
                                    Text(cat.rawValue).tag(cat)
                                }
                            }
                            .pickerStyle(.segmented)
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.top, 4)

                        // 5-Column Grid Table
                        LazyVGrid(columns: columns, spacing: 10) {
                            ForEach(currentList) { item in
                                KanaCellView(
                                    item: item,
                                    isKatakana: isKatakana,
                                    isSelected: activeDialogueKana?.id == item.id,
                                    onTap: {
                                        playKana(item)
                                    },
                                    onLongPress: {
                                        selectedKana = item
                                    }
                                )
                            }
                        }
                        .padding(.horizontal)

                        // Bottom Quiz & Practice Card
                        HStack(spacing: 14) {
                            Image(systemName: "sparkles.rectangle.stack.fill")
                                .font(.system(size: 32))
                                .foregroundColor(.orange)

                            VStack(alignment: .leading, spacing: 2) {
                                Text("Kana Speed Quiz (五十音特训)")
                                    .font(.system(size: 15, weight: .bold))
                                Text("Test your ear and recognition speed to earn Tokyo Points!")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            Button(action: { showQuizSheet = true }) {
                                Text("Start Quiz")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 8)
                                    .background(Color.orange)
                                    .cornerRadius(10)
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.bottom, activeDialogueKana != nil ? 140 : 30)
                    }
                }

                // 5-Second Auto-Dismissing Manga Dialogue Box Toast
                if let kana = activeDialogueKana {
                    KanaSpeechBubbleDialogueView(
                        kana: kana,
                        isKatakana: isKatakana,
                        timerToken: dialogueTimerToken,
                        onPlayKana: {
                            audioService.speak(text: kana.hiragana, style: .dailyConversational)
                        },
                        onPlayWord: {
                            audioService.speak(text: kana.exampleWordJa)
                        },
                        onClose: {
                            withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                                activeDialogueKana = nil
                            }
                        }
                    )
                    .padding(.horizontal, 16)
                    .padding(.bottom, 12)
                    .transition(
                        .asymmetric(
                            insertion: .move(edge: .bottom).combined(with: .scale(scale: 0.92)).combined(with: .opacity),
                            removal: .opacity.combined(with: .scale(scale: 0.95))
                        )
                    )
                    .zIndex(100)
                }
            }
            .navigationTitle("五十音图 (Kana Table)")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(item: $selectedKana) { kana in
                KanaDetailModal(kana: kana, isKatakana: isKatakana)
            }
            .sheet(isPresented: $showQuizSheet) {
                KanaQuizSheet(isKatakana: isKatakana)
            }
        }
    }

    private func playKana(_ item: KanaItem) {
        audioService.speak(text: item.hiragana, style: .dailyConversational)
        gamification.addRewards(tp: 1, exp: 2)

        withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
            activeDialogueKana = item
            dialogueTimerToken = UUID()
        }
    }
}

// MARK: - 5-Second Comic Dialogue Speech Balloon Toast
public struct KanaSpeechBubbleDialogueView: View {
    public let kana: KanaItem
    public let isKatakana: Bool
    public let timerToken: UUID
    public let onPlayKana: () -> Void
    public let onPlayWord: () -> Void
    public let onClose: () -> Void

    @State private var timeRemaining: Double = 5.0
    private let timer = Timer.publish(every: 0.1, on: .main, in: .common).autoconnect()

    public var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // Dialogue Bubble Top Bar
            HStack(alignment: .center, spacing: 10) {
                // Kana Character Badge
                Button(action: onPlayKana) {
                    HStack(spacing: 5) {
                        Text(isKatakana ? kana.katakana : kana.hiragana)
                            .font(.system(size: 22, weight: .black, design: .rounded))
                            .foregroundColor(.accentColor)

                        Text("[\(kana.romaji)]")
                            .font(.system(size: 13, weight: .bold, design: .monospaced))
                            .foregroundColor(.secondary)

                        Image(systemName: "speaker.wave.1.fill")
                            .font(.system(size: 11))
                            .foregroundColor(.accentColor)
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 4)
                    .background(Color.accentColor.opacity(0.12))
                    .cornerRadius(10)
                }
                .buttonStyle(PlainButtonStyle())

                Text("📅 今日例词 (7天每日轮换)")
                    .font(.system(size: 11, weight: .bold))
                    .foregroundColor(.secondary)

                Spacer()

                // 5s Countdown Badge
                HStack(spacing: 4) {
                    Image(systemName: "timer")
                        .font(.system(size: 10))
                    Text(String(format: "%.1fs", max(0, timeRemaining)))
                        .font(.system(size: 11, weight: .bold, design: .monospaced))
                }
                .foregroundColor(.secondary)
                .padding(.horizontal, 8)
                .padding(.vertical, 3)
                .background(Color.primary.opacity(0.06))
                .cornerRadius(8)

                // Close Button
                Button(action: onClose) {
                    Image(systemName: "xmark.circle.fill")
                        .font(.system(size: 18))
                        .foregroundColor(.secondary.opacity(0.8))
                }
            }

            Divider()
                .opacity(0.35)

            // Word, Romaji, Meaning, and Audio Button
            HStack(alignment: .center, spacing: 12) {
                VStack(alignment: .leading, spacing: 3) {
                    HStack(alignment: .firstTextBaseline, spacing: 8) {
                        Text(kana.exampleWordJa)
                            .font(.system(size: 20, weight: .black, design: .rounded))
                            .foregroundColor(.primary)

                        Text(kana.exampleWordRomaji)
                            .font(.system(size: 14, weight: .bold, design: .monospaced))
                            .foregroundColor(.accentColor)
                    }

                    Text(kana.exampleWordEn)
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(.secondary)
                        .lineLimit(1)
                }

                Spacer()

                // Listen to Native Audio Button
                Button(action: onPlayWord) {
                    HStack(spacing: 5) {
                        Image(systemName: "speaker.wave.2.fill")
                            .font(.system(size: 13, weight: .bold))
                        Text("原音")
                            .font(.system(size: 13, weight: .bold))
                    }
                    .foregroundColor(.white)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(
                        LinearGradient(
                            colors: [Color.accentColor, Color.accentColor.opacity(0.85)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .cornerRadius(12)
                    .shadow(color: Color.accentColor.opacity(0.3), radius: 4, x: 0, y: 2)
                }
            }

            // 5s Animated Linear Progress Bar
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule()
                        .fill(Color.primary.opacity(0.08))
                        .frame(height: 3.5)

                    Capsule()
                        .fill(
                            LinearGradient(
                                colors: [Color.accentColor, Color.orange],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .frame(width: geo.size.width * CGFloat(max(0, timeRemaining / 5.0)), height: 3.5)
                }
            }
            .frame(height: 3.5)
        }
        .padding(14)
        .background(
            RoundedRectangle(cornerRadius: 18)
                .fill(.ultraThinMaterial)
                .overlay(
                    RoundedRectangle(cornerRadius: 18)
                        .stroke(Color.accentColor.opacity(0.35), lineWidth: 1.5)
                )
                .shadow(color: Color.black.opacity(0.2), radius: 14, x: 0, y: 6)
        )
        .id(timerToken)
        .onAppear {
            timeRemaining = 5.0
        }
        .onReceive(timer) { _ in
            if timeRemaining > 0.1 {
                timeRemaining -= 0.1
            } else {
                onClose()
            }
        }
    }
}

public struct KanaCellView: View {
    public let item: KanaItem
    public let isKatakana: Bool
    public var isSelected: Bool = false
    public let onTap: () -> Void
    public let onLongPress: () -> Void

    public var body: some View {
        Button(action: onTap) {
            VStack(spacing: 2) {
                Text(isKatakana ? item.katakana : item.hiragana)
                    .font(.system(size: 26, weight: .bold, design: .rounded))
                    .foregroundColor(isSelected ? .accentColor : .primary)

                Text(item.romaji)
                    .font(.system(size: 11, weight: .semibold, design: .monospaced))
                    .foregroundColor(isSelected ? .accentColor : .secondary)
            }
            .frame(maxWidth: .infinity)
            .frame(height: 68)
            .background(isSelected ? Color.accentColor.opacity(0.15) : Color.clear)
            .background(.ultraThinMaterial)
            .cornerRadius(14)
            .overlay(
                RoundedRectangle(cornerRadius: 14)
                    .stroke(isSelected ? Color.accentColor : Color.accentColor.opacity(0.15), lineWidth: isSelected ? 2 : 1)
            )
        }
        .buttonStyle(PlainButtonStyle())
        .simultaneousGesture(LongPressGesture().onEnded { _ in
            onLongPress()
        })
    }
}

public struct KanaDetailModal: View {
    public let kana: KanaItem
    public let isKatakana: Bool
    @ObservedObject var audioService = AudioService.shared
    @Environment(\.dismiss) private var dismiss

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 24) {
                    // Big Character Display
                    VStack(spacing: 6) {
                        Text(isKatakana ? kana.katakana : kana.hiragana)
                            .font(.system(size: 88, weight: .black, design: .rounded))
                            .foregroundColor(.primary)

                        Text(kana.romaji)
                            .font(.system(size: 22, weight: .bold, design: .monospaced))
                            .foregroundColor(.accentColor)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 24)
                    .background(.ultraThinMaterial)
                    .cornerRadius(24)
                    .padding(.horizontal)

                    // Audio Playback Row
                    HStack(spacing: 16) {
                        Button(action: {
                            audioService.speak(text: kana.hiragana, style: .dailyConversational, rate: 0.8)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "tortoise.fill")
                                Text("Slow (0.8x)")
                            }
                            .font(.caption)
                            .fontWeight(.bold)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 10)
                            .background(Color.orange.opacity(0.18))
                            .foregroundColor(.orange)
                            .cornerRadius(12)
                        }

                        Button(action: {
                            audioService.speak(text: kana.hiragana, style: .dailyConversational)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "speaker.wave.2.fill")
                                Text("Natural Voice (1.0x)")
                            }
                            .font(.caption)
                            .fontWeight(.bold)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 10)
                            .background(Color.accentColor)
                            .foregroundColor(.white)
                            .cornerRadius(12)
                        }
                    }

                    // 7-Day Non-Repeating Weekly Vocabulary Schedule
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Image(systemName: "calendar.badge.clock")
                                .foregroundColor(.accentColor)
                            Text("7-Day Daily Rotating Vocabulary (一周每日一换):")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                        }

                        let dayNames = ["周一 (Mon)", "周二 (Tue)", "周三 (Wed)", "周四 (Thu)", "周五 (Fri)", "周六 (Sat)", "周日 (Sun)"]
                        VStack(spacing: 8) {
                            ForEach(0..<min(7, kana.exampleWords.count), id: \.self) { idx in
                                let word = kana.exampleWords[idx]
                                let isToday = (idx == ((Calendar.current.ordinality(of: .day, in: .year, for: Date()) ?? 1) - 1) % 7)

                                HStack(spacing: 10) {
                                    Text(dayNames[idx])
                                        .font(.system(size: 10, weight: .bold))
                                        .foregroundColor(isToday ? .accentColor : .secondary)
                                        .frame(width: 62, alignment: .leading)

                                    VStack(alignment: .leading, spacing: 1) {
                                        HStack(spacing: 6) {
                                            Text(word.japanese)
                                                .font(.system(size: 14, weight: .bold))
                                                .foregroundColor(.primary)
                                            Text("[\(word.romaji)]")
                                                .font(.system(size: 11, weight: .semibold, design: .monospaced))
                                                .foregroundColor(.accentColor)
                                        }
                                        Text(word.english)
                                            .font(.system(size: 11))
                                            .foregroundColor(.secondary)
                                            .lineLimit(1)
                                    }

                                    Spacer()

                                    if isToday {
                                        Text("今日")
                                            .font(.system(size: 9, weight: .heavy))
                                            .foregroundColor(.white)
                                            .padding(.horizontal, 6)
                                            .padding(.vertical, 2)
                                            .background(Color.accentColor)
                                            .cornerRadius(6)
                                    }

                                    Button(action: {
                                        audioService.speak(text: word.japanese)
                                    }) {
                                        Image(systemName: "speaker.wave.2.fill")
                                            .font(.system(size: 11))
                                            .foregroundColor(.white)
                                            .padding(6)
                                            .background(Color.accentColor)
                                            .clipShape(Circle())
                                    }
                                }
                                .padding(8)
                                .background(isToday ? Color.accentColor.opacity(0.12) : Color.white.opacity(0.05))
                                .cornerRadius(10)
                            }
                        }

                        Divider()

                        Text("💡 记忆口诀: \(kana.mnemonic)")
                            .font(.footnote)
                            .foregroundColor(.secondary)
                    }
                    .padding(14)
                    .background(.ultraThinMaterial)
                    .cornerRadius(18)
                    .padding(.horizontal)

                    Spacer()
                }
                .padding(.top, 20)
            }
            .navigationTitle("Kana Master Details")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}

public struct KanaQuizSheet: View {
    public let isKatakana: Bool
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var audioService = AudioService.shared
    @ObservedObject var gamification = GamificationService.shared

    @State private var currentQuestionIndex = 0
    @State private var score = 0
    @State private var isAnswered = false
    @State private var selectedOption: String? = nil
    @State private var quizQuestions: [KanaQuizQuestion] = []

    public struct KanaQuizQuestion: Identifiable {
        public let id = UUID()
        public let targetKana: KanaItem
        public let options: [String]
        public let correctOption: String
    }

    public init(isKatakana: Bool) {
        self.isKatakana = isKatakana
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 20) {
                    if currentQuestionIndex < quizQuestions.count {
                        let q = quizQuestions[currentQuestionIndex]

                        // Progress
                        HStack {
                            Text("Question \(currentQuestionIndex + 1) / \(quizQuestions.count)")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                            Spacer()
                            Text("Score: \(score)")
                                .font(.caption)
                                .fontWeight(.heavy)
                                .foregroundColor(.accentColor)
                        }
                        .padding(.horizontal)

                        // Audio Question Prompt
                        VStack(spacing: 12) {
                            Button(action: {
                                audioService.speak(text: q.targetKana.hiragana, style: .dailyConversational)
                            }) {
                                ZStack {
                                    Circle()
                                        .fill(Color.accentColor)
                                        .frame(width: 80, height: 80)
                                    Image(systemName: "speaker.wave.3.fill")
                                        .font(.largeTitle)
                                        .foregroundColor(.white)
                                }
                            }

                            Text("Tap to listen, then select the matching kana:")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        .padding(.vertical, 20)

                        // 4 Options Grid
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
                            ForEach(q.options, id: \.self) { opt in
                                Button(action: {
                                    handleAnswer(selected: opt, correct: q.correctOption)
                                }) {
                                    Text(opt)
                                        .font(.system(size: 32, weight: .bold))
                                        .frame(maxWidth: .infinity)
                                        .frame(height: 74)
                                        .background(
                                            isAnswered && opt == q.correctOption
                                            ? Color.green.opacity(0.2)
                                            : (isAnswered && selectedOption == opt ? Color.red.opacity(0.2) : Color.white.opacity(0.12))
                                        )
                                        .cornerRadius(16)
                                        .overlay(
                                            RoundedRectangle(cornerRadius: 16)
                                                .stroke(
                                                    isAnswered && opt == q.correctOption
                                                    ? Color.green
                                                    : (isAnswered && selectedOption == opt ? Color.red : Color.clear),
                                                    lineWidth: 2
                                                )
                                        )
                                }
                                .disabled(isAnswered)
                            }
                        }
                        .padding(.horizontal)

                        Spacer()

                        if isAnswered {
                            Button(action: nextQuestion) {
                                Text(currentQuestionIndex < quizQuestions.count - 1 ? "Next Kana ➔" : "Finish Quiz 🏆")
                                    .font(.headline)
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.accentColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(16)
                            }
                            .padding(.horizontal)
                        }
                    } else {
                        // Quiz Finished
                        VStack(spacing: 20) {
                            Image(systemName: "trophy.fill")
                                .font(.system(size: 64))
                                .foregroundColor(.yellow)

                            Text("Kana Drill Completed!")
                                .font(.title)
                                .fontWeight(.black)

                            Text("You scored \(score) out of \(quizQuestions.count)!")
                                .font(.headline)
                                .foregroundColor(.secondary)

                            Button(action: {
                                gamification.addRewards(tp: score * 10, exp: score * 15)
                                dismiss()
                            }) {
                                Text("Claim +\(score * 10) TP & Finish")
                                    .font(.headline)
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.accentColor)
                                    .foregroundColor(.white)
                                    .cornerRadius(16)
                            }
                            .padding(.horizontal)
                        }
                        .padding(.top, 40)
                    }
                }
                .padding(.top, 10)
            }
            .navigationTitle("Kana Recognition Quiz")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Exit") { dismiss() }
                }
            }
            .onAppear {
                generateQuestions()
            }
        }
    }

    private func generateQuestions() {
        let all = KanaDataManager.shared.seionList.shuffled()
        var list: [KanaQuizQuestion] = []

        for i in 0..<min(6, all.count) {
            let target = all[i]
            let correctChar = isKatakana ? target.katakana : target.hiragana
            var wrongChars = all.filter { $0.id != target.id }.shuffled().prefix(3).map { isKatakana ? $0.katakana : $0.hiragana }
            wrongChars.append(correctChar)
            wrongChars.shuffle()

            list.append(KanaQuizQuestion(targetKana: target, options: wrongChars, correctOption: correctChar))
        }

        self.quizQuestions = list
        if let first = list.first {
            audioService.speak(text: first.targetKana.hiragana)
        }
    }

    private func handleAnswer(selected: String, correct: String) {
        selectedOption = selected
        isAnswered = true
        if selected == correct {
            score += 1
        }
    }

    private func nextQuestion() {
        isAnswered = false
        selectedOption = nil
        currentQuestionIndex += 1
        if currentQuestionIndex < quizQuestions.count {
            audioService.speak(text: quizQuestions[currentQuestionIndex].targetKana.hiragana)
        }
    }
}
