import SwiftUI

public struct JLPTDictionaryView: View {
    @StateObject private var dictService = JLPTDictionaryService.shared
    @StateObject private var subService = SubscriptionService.shared
    @StateObject private var audioService = AudioService.shared
    @StateObject private var weakTracker = WeakWordTrackerService.shared

    @State private var isFlashcardMode: Bool = false
    @State private var currentFlashcardIndex: Int = 0
    @State private var isFlashcardFlipped: Bool = false
    @State private var showWeakWordsSheet: Bool = false
    @State private var showUpgradeSheet: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 0) {
                    // Top Search & Mode Switcher Bar
                    VStack(spacing: 12) {
                        HStack(spacing: 10) {
                            // Search Field
                            HStack(spacing: 8) {
                                Image(systemName: "magnifyingglass")
                                    .foregroundColor(.secondary)
                                TextField("搜索汉字 / 假名 / 罗马音 / 含义...", text: $dictService.searchQuery)
                                    .font(.system(size: 14))
                                    .autocapitalization(.none)
                                    .disableAutocorrection(true)

                                if !dictService.searchQuery.isEmpty {
                                    Button(action: { dictService.searchQuery = "" }) {
                                        Image(systemName: "xmark.circle.fill")
                                            .foregroundColor(.secondary)
                                            .font(.caption)
                                    }
                                }
                            }
                            .padding(.horizontal, 12)
                            .padding(.vertical, 10)
                            .background(Color(UIColor.secondarySystemBackground).opacity(0.85))
                            .cornerRadius(14)

                            // Mode Toggle (Search vs Flashcard)
                            Button(action: {
                                withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
                                    isFlashcardMode.toggle()
                                    isFlashcardFlipped = false
                                }
                            }) {
                                HStack(spacing: 4) {
                                    Image(systemName: isFlashcardMode ? "text.book.closed.fill" : "rectangle.stack.fill")
                                    Text(isFlashcardMode ? "列表" : "背词")
                                        .font(.caption)
                                        .fontWeight(.bold)
                                }
                                .foregroundColor(.white)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 10)
                                .background(Color.accentColor)
                                .cornerRadius(14)
                            }
                        }

                        // JLPT Level Selector Chips
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 8) {
                                ForEach(JLPTLevelFilter.allCases) { lvl in
                                    let isSelected = dictService.selectedLevel == lvl
                                    let isLocked = !subService.canAccessJLPTLevel(lvl.shortName) && lvl != .all

                                    Button(action: {
                                        if isLocked {
                                            showUpgradeSheet = true
                                        } else {
                                            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                                                dictService.selectedLevel = lvl
                                                currentFlashcardIndex = 0
                                                isFlashcardFlipped = false
                                            }
                                        }
                                    }) {
                                        HStack(spacing: 4) {
                                            Text(lvl.rawValue)
                                                .font(.caption)
                                                .fontWeight(.bold)
                                            if isLocked {
                                                Image(systemName: "lock.fill")
                                                    .font(.system(size: 9))
                                                    .foregroundColor(.orange)
                                            }
                                        }
                                        .foregroundColor(isSelected ? .white : .primary)
                                        .padding(.horizontal, 12)
                                        .padding(.vertical, 7)
                                        .background(isSelected ? Color.accentColor : Color(UIColor.secondarySystemBackground).opacity(0.7))
                                        .cornerRadius(12)
                                    }
                                }
                            }
                            .padding(.horizontal, 2)
                        }
                    }
                    .padding(14)
                    .background(.ultraThinMaterial)
                    .cornerRadius(20)
                    .padding(.horizontal)
                    .padding(.top, 4)

                    // Content Area
                    if isFlashcardMode {
                        flashcardDeckView
                    } else {
                        wordListView
                    }
                }
            }
            .navigationTitle("JLPT 绿宝书词典")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { showWeakWordsSheet = true }) {
                        HStack(spacing: 4) {
                            Image(systemName: "bolt.heart.fill")
                                .foregroundColor(.red)
                            if !weakTracker.activeWeakWords.isEmpty {
                                Text("\(weakTracker.activeWeakWords.count)")
                                    .font(.caption2)
                                    .fontWeight(.black)
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.red)
                                    .clipShape(Capsule())
                            }
                        }
                    }
                }
            }
            .sheet(isPresented: $showWeakWordsSheet) {
                WeakWordsLabView()
            }
            .sheet(isPresented: $showUpgradeSheet) {
                TokyoProUpgradeModalView()
            }
        }
    }

    // MARK: - Word List Mode
    private var wordListView: some View {
        let words = dictService.filteredWords

        return ScrollView {
            LazyVStack(spacing: 12) {
                if words.isEmpty {
                    VStack(spacing: 12) {
                        Image(systemName: "character.book.closed")
                            .font(.system(size: 48))
                            .foregroundColor(.secondary)
                        Text("未找到相关单词")
                            .font(.headline)
                        Text("请尝试输入日语汉字、平假名或中文释义搜索")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 60)
                } else {
                    ForEach(words) { word in
                        JLPTWordCardView(
                            word: word,
                            isBookmarked: dictService.isBookmarked(id: word.id),
                            onPlayAudio: {
                                audioService.speak(text: word.kanji.isEmpty ? word.reading : word.kanji)
                                weakTracker.recordListen(word: word.kanji.isEmpty ? word.reading : word.kanji, reading: word.reading, meaning: word.meaning)
                            },
                            onPlayExample: {
                                audioService.speak(text: word.exampleJa)
                            },
                            onToggleBookmark: {
                                dictService.toggleBookmark(id: word.id)
                            }
                        )
                        .onAppear {
                            weakTracker.startDwell(word: word.kanji.isEmpty ? word.reading : word.kanji)
                        }
                        .onDisappear {
                            weakTracker.endDwell(word: word.kanji.isEmpty ? word.reading : word.kanji, reading: word.reading, meaning: word.meaning)
                        }
                    }
                }
            }
            .padding(.horizontal)
            .padding(.top, 10)
            .padding(.bottom, 40)
        }
    }

    // MARK: - Flashcard Memorization Mode
    private var flashcardDeckView: some View {
        let words = dictService.filteredWords

        return VStack(spacing: 20) {
            if words.isEmpty {
                Spacer()
                Text("当前分类暂无词卡")
                    .foregroundColor(.secondary)
                Spacer()
            } else {
                let currentWord = words[min(currentFlashcardIndex, words.count - 1)]

                // Card Progress
                HStack {
                    Text("第 \(currentFlashcardIndex + 1) / \(words.count) 词")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                    Spacer()
                    Text("点击卡片翻转查看释义与例句")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                .padding(.horizontal, 24)
                .padding(.top, 12)

                // Flippable Flashcard
                ZStack {
                    RoundedRectangle(cornerRadius: 24)
                        .fill(.ultraThinMaterial)
                        .shadow(color: Color.black.opacity(0.1), radius: 10, y: 5)
                        .overlay(
                            RoundedRectangle(cornerRadius: 24)
                                .stroke(Color.accentColor.opacity(0.3), lineWidth: 1.5)
                        )

                    VStack(spacing: 16) {
                        HStack {
                            Text(currentWord.level)
                                .font(.caption2)
                                .fontWeight(.black)
                                .foregroundColor(.white)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.accentColor)
                                .cornerRadius(8)

                            Text(currentWord.partOfSpeech)
                                .font(.caption2)
                                .foregroundColor(.secondary)

                            Spacer()

                            Text(currentWord.pitchAccent)
                                .font(.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.orange)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.orange.opacity(0.15))
                                .cornerRadius(8)
                        }

                        Spacer()

                        // Front Content (Kanji + Reading)
                        VStack(spacing: 8) {
                            Text(currentWord.kanji)
                                .font(.system(size: 38, weight: .black, design: .rounded))
                            Text(currentWord.reading)
                                .font(.system(size: 20, weight: .semibold))
                                .foregroundColor(.accentColor)
                            Text(currentWord.romaji)
                                .font(.system(size: 14, design: .monospaced))
                                .foregroundColor(.secondary)
                        }

                        // Back Content (Revealed on Tap)
                        if isFlashcardFlipped {
                            VStack(spacing: 12) {
                                Divider()

                                Text(currentWord.meaning)
                                    .font(.system(size: 18, weight: .bold))
                                    .foregroundColor(.primary)

                                VStack(alignment: .leading, spacing: 4) {
                                    Text(currentWord.exampleFurigana)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    Text(currentWord.exampleZh)
                                        .font(.caption)
                                        .foregroundColor(.primary)
                                }
                                .padding(10)
                                .background(Color(UIColor.secondarySystemBackground).opacity(0.6))
                                .cornerRadius(12)
                            }
                            .transition(.opacity.combined(with: .scale(scale: 0.95)))
                        }

                        Spacer()

                        // Audio button
                        Button(action: {
                            audioService.speak(text: currentWord.kanji.isEmpty ? currentWord.reading : currentWord.kanji)
                            weakTracker.recordListen(word: currentWord.kanji, reading: currentWord.reading, meaning: currentWord.meaning)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "speaker.wave.2.fill")
                                Text("真人发音")
                            }
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 8)
                            .background(Color.accentColor)
                            .cornerRadius(12)
                        }
                    }
                    .padding(24)
                }
                .frame(maxHeight: 380)
                .padding(.horizontal, 20)
                .onTapGesture {
                    withAnimation(.spring(response: 0.35, dampingFraction: 0.8)) {
                        isFlashcardFlipped.toggle()
                    }
                }

                // Bottom Navigation Buttons
                HStack(spacing: 20) {
                    Button(action: {
                        if currentFlashcardIndex > 0 {
                            withAnimation {
                                currentFlashcardIndex -= 1
                                isFlashcardFlipped = false
                            }
                        }
                    }) {
                        HStack {
                            Image(systemName: "arrow.left")
                            Text("上一个")
                        }
                        .font(.subheadline)
                        .fontWeight(.bold)
                        .foregroundColor(currentFlashcardIndex > 0 ? .primary : .secondary.opacity(0.5))
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(.ultraThinMaterial)
                        .cornerRadius(14)
                    }
                    .disabled(currentFlashcardIndex == 0)

                    Button(action: {
                        if currentFlashcardIndex < words.count - 1 {
                            withAnimation {
                                currentFlashcardIndex += 1
                                isFlashcardFlipped = false
                            }
                            GamificationService.shared.addRewards(tp: 2, exp: 5)
                        }
                    }) {
                        HStack {
                            Text("下一个 (+2TP)")
                            Image(systemName: "arrow.right")
                        }
                        .font(.subheadline)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 12)
                        .background(Color.accentColor)
                        .cornerRadius(14)
                    }
                }
                .padding(.horizontal, 20)
                .padding(.bottom, 20)
            }
        }
    }
}

// MARK: - Individual Word Row Card
public struct JLPTWordCardView: View {
    public let word: JLPTWord
    public let isBookmarked: Bool
    public let onPlayAudio: () -> Void
    public let onPlayExample: () -> Void
    public let onToggleBookmark: () -> Void

    public var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 2) {
                    HStack(spacing: 8) {
                        Text(word.kanji)
                            .font(.system(size: 20, weight: .black, design: .rounded))
                        Text("[\(word.reading)]")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.accentColor)
                        Text(word.romaji)
                            .font(.system(size: 12, design: .monospaced))
                            .foregroundColor(.secondary)
                    }

                    Text(word.meaning)
                        .font(.system(size: 14, weight: .semibold))
                        .foregroundColor(.primary)
                }

                Spacer()

                HStack(spacing: 8) {
                    Text(word.level)
                        .font(.system(size: 10, weight: .black))
                        .foregroundColor(.white)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 3)
                        .background(Color.accentColor)
                        .cornerRadius(6)

                    Text(word.pitchAccent)
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(.orange)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 3)
                        .background(Color.orange.opacity(0.15))
                        .cornerRadius(6)

                    Button(action: onToggleBookmark) {
                        Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                            .font(.subheadline)
                            .foregroundColor(isBookmarked ? .orange : .secondary)
                    }
                }
            }

            // Example Sentence with furigana
            HStack(alignment: .center, spacing: 8) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(word.exampleFurigana)
                        .font(.system(size: 12))
                        .foregroundColor(.secondary)
                    Text(word.exampleZh)
                        .font(.system(size: 12, weight: .medium))
                        .foregroundColor(.primary)
                }

                Spacer()

                // Play Example Audio
                Button(action: onPlayExample) {
                    Image(systemName: "bubble.left.and.bubble.right.fill")
                        .font(.caption)
                        .foregroundColor(.accentColor)
                        .padding(8)
                        .background(Color.accentColor.opacity(0.12))
                        .clipShape(Circle())
                }

                // Play Word Audio
                Button(action: onPlayAudio) {
                    Image(systemName: "speaker.wave.2.fill")
                        .font(.caption)
                        .foregroundColor(.white)
                        .padding(8)
                        .background(Color.accentColor)
                        .clipShape(Circle())
                }
            }
            .padding(10)
            .background(Color(UIColor.secondarySystemBackground).opacity(0.6))
            .cornerRadius(12)
        }
        .padding(14)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
        .overlay(
            RoundedRectangle(cornerRadius: 18)
                .stroke(Color.primary.opacity(0.06), lineWidth: 1)
        )
    }
}
