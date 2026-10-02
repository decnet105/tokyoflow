import SwiftUI

public struct JLPTDictionaryView: View {
    @StateObject private var dictService = JLPTDictionaryService.shared
    @StateObject private var subService = SubscriptionService.shared
    @StateObject private var audioService = AudioService.shared
    @StateObject private var weakTracker = WeakWordTrackerService.shared

    @State private var selectedLexiconTab: Int = 0 // 0: Vocabulary, 1: Grammar Lab
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
                    // Segment Tab Picker: Vocabulary vs Grammar Lab
                    Picker("Lexicon Type", selection: $selectedLexiconTab) {
                        Text("Vocabulary").tag(0)
                        Text("Grammar Lab").tag(1)
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal, 16)
                    .padding(.top, 8)

                    if selectedLexiconTab == 1 {
                        JLPTGrammarLabView()
                    } else {
                        vocabLexiconBody
                    }
                }
            }
            .navigationTitle(selectedLexiconTab == 0 ? "JLPT Core Lexicon" : "Grammar Blueprint Lab")

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

    private var vocabLexiconBody: some View {
        TokyoDuoAdaptiveLayout(duoSplitRatio: 0.48) {
            // Left Screen: Search Bar, Level Chips & Word List
            VStack(spacing: 0) {
                VStack(spacing: 12) {
                    HStack(spacing: 10) {
                        // Search Field
                        HStack(spacing: 8) {
                            Image(systemName: "magnifyingglass")
                                .foregroundColor(.secondary)
                            TextField("Search Kanji / Kana / Romaji / Meaning...", text: $dictService.searchQuery)
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
                                Text(isFlashcardMode ? "List" : "Cards")
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
                .background(Color(UIColor.secondarySystemGroupedBackground))
                .cornerRadius(20)
                .padding(.horizontal)
                .padding(.top, 4)

                if isFlashcardMode {
                    flashcardDeckView
                } else {
                    wordListView
                }
            }
        } secondaryContent: {
            // Right Screen on iPad / Duo: Flashcard Memorization Deck & Active Drill
            flashcardDeckView
        }
    }

    // MARK: - Word List Mode

    private var wordListView: some View {
        let words = dictService.displayedWords

        return ScrollView {
            LazyVStack(spacing: 12) {
                if !dictService.isLoaded && dictService.allWords.isEmpty {
                    // Shimmer skeleton loading placeholder for instant responsiveness
                    ForEach(0..<6, id: \.self) { _ in
                        VStack(alignment: .leading, spacing: 10) {
                            HStack {
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(Color(UIColor.tertiarySystemFill))
                                    .frame(width: 80, height: 22)
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(Color(UIColor.tertiarySystemFill))
                                    .frame(width: 60, height: 16)
                                Spacer()
                                RoundedRectangle(cornerRadius: 6)
                                    .fill(Color(UIColor.tertiarySystemFill))
                                    .frame(width: 40, height: 20)
                            }
                            RoundedRectangle(cornerRadius: 6)
                                .fill(Color(UIColor.tertiarySystemFill))
                                .frame(maxWidth: .infinity, maxHeight: 16)
                        }
                        .padding(14)
                        .background(Color(UIColor.secondarySystemGroupedBackground))
                        .cornerRadius(18)
                    }
                } else if dictService.cachedFilteredWords.isEmpty {
                    VStack(spacing: 12) {
                        Image(systemName: "character.book.closed")
                            .font(.system(size: 48))
                            .foregroundColor(.secondary)
                        Text("No matching vocabulary")
                            .font(.headline)
                        Text("Try searching by Japanese Kanji, Hiragana, Romaji, or English meaning.")
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
                                audioService.speak(text: word.kanji.isEmpty ? word.reading : word.kanji, reading: word.reading)
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
                            if word == words.last && dictService.hasMoreWords {
                                dictService.loadMoreWords()
                            }
                        }
                    }

                    if dictService.hasMoreWords {
                        Button(action: { dictService.loadMoreWords() }) {
                            HStack(spacing: 6) {
                                ProgressView()
                                    .scaleEffect(0.8)
                                Text("Showing \(words.count) of \(dictService.cachedFilteredWords.count) words • Tap to load more")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 8)
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
                Text("No cards available in this level")
                    .foregroundColor(.secondary)
                Spacer()
            } else {
                let currentWord = words[min(currentFlashcardIndex, words.count - 1)]

                // Card Progress
                HStack {
                    Text("Card \(currentFlashcardIndex + 1) / \(words.count)")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.secondary)
                    Spacer()
                    Text("Tap card to flip & reveal meaning")
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

                                Text(currentWord.localizedMeaning(isEnglish: LanguageManager.shared.isEnglish))
                                    .font(.system(size: 18, weight: .bold))
                                    .foregroundColor(.primary)

                                VStack(alignment: .leading, spacing: 4) {
                                    Text(currentWord.exampleFurigana)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                    Text(LanguageManager.shared.isEnglish ? (currentWord.exampleEn.isEmpty ? currentWord.exampleZh : currentWord.exampleEn) : (currentWord.exampleZh.isEmpty ? currentWord.exampleEn : currentWord.exampleZh))
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
                            audioService.speak(text: currentWord.kanji.isEmpty ? currentWord.reading : currentWord.kanji, reading: currentWord.reading)
                            weakTracker.recordListen(word: currentWord.kanji, reading: currentWord.reading, meaning: currentWord.meaning)
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "speaker.wave.2.fill")
                                Text("Listen")
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
                            Text("Previous")
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
                            Text("Next (+2TP)")
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

                    Text(word.localizedMeaning(isEnglish: LanguageManager.shared.isEnglish))
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

            // Example Sentence with Live Karaoke Word Flow Highlighting
            HStack(alignment: .center, spacing: 8) {
                TokyoKaraokeSentenceView(
                    sentenceJa: word.exampleJa,
                    furiganaText: word.exampleFurigana,
                    translation: LanguageManager.shared.isEnglish ? (word.exampleEn.isEmpty ? word.exampleZh : word.exampleEn) : (word.exampleZh.isEmpty ? word.exampleEn : word.exampleZh),
                    showFurigana: true,
                    fontScale: 0.95,
                    onWordTapped: { token in
                        TokyoVoiceBankService.shared.playPhraseOrFallback(key: token, fallbackText: token)
                    }
                )

                Spacer()

                // Play Example Audio (Triggers Native VoiceBank + Live Karaoke Glow)
                Button(action: onPlayExample) {
                    Image(systemName: "bubble.left.and.bubble.right.fill")
                        .font(.caption)
                        .foregroundColor(.accentColor)
                        .padding(8)
                        .background(Color.accentColor.opacity(0.15))
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
        .background(Color(UIColor.secondarySystemGroupedBackground))
        .cornerRadius(18)
        .overlay(
            RoundedRectangle(cornerRadius: 18)
                .stroke(Color(UIColor.separator).opacity(0.3), lineWidth: 1)
        )
    }
}
