import SwiftUI

public struct NewsShadowingLabView: View {
    public let newsItem: DailyNewsItem

    @ObservedObject var nativeAudio = NativeAudioPlayer.shared
    @ObservedObject var gamification = GamificationService.shared
    @State private var showFurigana: Bool = true
    @State private var showEnglishTranslation: Bool = true
    @State private var selectedSentenceForRecording: NewsSentence? = nil
    @State private var selectedTab: Int = 0 // 0: Shadowing, 1: Vocabulary, 2: Quiz
    @State private var selectedQuizAnswer: Int? = nil
    @State private var showQuizFeedback: Bool = false
    @State private var isCompletedAwardGiven: Bool = false

    @Environment(\.dismiss) private var dismiss

    public init(newsItem: DailyNewsItem) {
        self.newsItem = newsItem
    }

    public var body: some View {
        ZStack {
            MangaThemeBackgroundView()

            VStack(spacing: 0) {
                // Top Header Card
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Label(newsItem.category, systemImage: newsItem.categoryIcon)
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.accentColor)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.accentColor.opacity(0.15))
                            .cornerRadius(8)

                        Spacer()

                        Text(newsItem.publishDate)
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }

                    Text(newsItem.title)
                        .font(.system(size: 18, weight: .black, design: .rounded))
                        .foregroundColor(.primary)

                    if showFurigana {
                        Text(newsItem.titleFurigana)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    // Audio Controls Bar
                    HStack(spacing: 14) {
                        Button(action: {
                            if nativeAudio.isPlayingRemoteAudio {
                                nativeAudio.stopAll()
                            } else {
                                nativeAudio.playAudioUrl(newsItem.audioUrl ?? "", sentences: newsItem.contentSentences)
                                gamification.incrementQuestProgress(id: "q_listen_news")
                            }
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: nativeAudio.isPlayingRemoteAudio ? "pause.fill" : "play.fill")
                                Text(nativeAudio.isPlayingRemoteAudio ? "Pause" : "Native Audio")
                                    .font(.system(size: 13, weight: .bold))
                            }
                            .foregroundColor(.white)
                            .padding(.horizontal, 14)
                            .padding(.vertical, 8)
                            .background(Color.accentColor)
                            .cornerRadius(12)
                        }

                        // Speed selector
                        Menu {
                            Button("0.75x (Slow)") { nativeAudio.setSpeed(0.75) }
                            Button("1.0x (Normal)") { nativeAudio.setSpeed(1.0) }
                            Button("1.25x (Fast)") { nativeAudio.setSpeed(1.25) }
                        } label: {
                            HStack(spacing: 2) {
                                Text("\(String(format: "%.2fx", nativeAudio.playbackRate))")
                                    .font(.system(size: 12, weight: .bold))
                                Image(systemName: "chevron.down")
                                    .font(.system(size: 9))
                            }
                            .padding(.horizontal, 10)
                            .padding(.vertical, 8)
                            .background(.ultraThinMaterial)
                            .cornerRadius(10)
                        }

                        Spacer()

                        // Furigana & Translation Toggles
                        Button(action: { showFurigana.toggle() }) {
                            Text("ふりがな")
                                .font(.system(size: 11, weight: .bold))
                                .padding(.horizontal, 8)
                                .padding(.vertical, 6)
                                .background(showFurigana ? Color.accentColor.opacity(0.25) : Color.gray.opacity(0.2))
                                .cornerRadius(8)
                        }

                        Button(action: { showEnglishTranslation.toggle() }) {
                            Text("EN")
                                .font(.system(size: 11, weight: .bold))
                                .padding(.horizontal, 8)
                                .padding(.vertical, 6)
                                .background(showEnglishTranslation ? Color.accentColor.opacity(0.25) : Color.gray.opacity(0.2))
                                .cornerRadius(8)
                        }
                    }
                }
                .padding()
                .background(.ultraThinMaterial)
                .cornerRadius(20)
                .padding(.horizontal)
                .padding(.top, 8)

                // Segmented Tab Picker
                Picker("Tab", selection: $selectedTab) {
                    Text("Shadowing 跟读").tag(0)
                    Text("Words 词汇 (\(newsItem.vocabulary.count))").tag(1)
                    Text("Quiz 测验").tag(2)
                }
                .pickerStyle(.segmented)
                .padding(.horizontal)
                .padding(.top, 12)

                // Tab Content
                if selectedTab == 0 {
                    shadowingSentenceListView
                } else if selectedTab == 1 {
                    vocabularyListView
                } else {
                    quizView
                }
            }
        }
        .navigationTitle("NHK News Shadowing")
        .navigationBarTitleDisplayMode(.inline)
        .onDisappear {
            nativeAudio.stopAll()
        }
    }

    private var shadowingSentenceListView: some View {
        ScrollView {
            VStack(spacing: 14) {
                ForEach(newsItem.contentSentences) { sentence in
                    let isActive = (nativeAudio.activeSentenceId == sentence.id)

                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text(sentence.id.uppercased())
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(isActive ? .accentColor : .secondary)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(isActive ? Color.accentColor.opacity(0.2) : Color.gray.opacity(0.15))
                                .cornerRadius(6)

                            Spacer()

                            // Individual Sentence Audio Play
                            Button(action: {
                                if let url = newsItem.audioUrl {
                                    nativeAudio.playSentence(sentence, audioUrl: url)
                                }
                            }) {
                                HStack(spacing: 4) {
                                    Image(systemName: isActive ? "waveform" : "speaker.wave.2.fill")
                                    Text("Listen")
                                        .font(.caption2)
                                }
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(isActive ? Color.accentColor : Color.gray.opacity(0.2))
                                .foregroundColor(isActive ? .white : .primary)
                                .cornerRadius(8)
                            }
                        }

                        // Japanese Text with highlight
                        Text(sentence.japanese)
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundColor(isActive ? .accentColor : .primary)
                            .lineSpacing(4)

                        if showFurigana {
                            Text(sentence.furigana)
                                .font(.system(size: 13))
                                .foregroundColor(.secondary)
                        }

                        if showEnglishTranslation {
                            Text(sentence.english)
                                .font(.system(size: 13, design: .rounded))
                                .foregroundColor(.secondary.opacity(0.85))
                        }

                        Divider()

                        // Shadowing Voice Recording Actions
                        HStack(spacing: 12) {
                            if nativeAudio.isRecordingShadowing && selectedSentenceForRecording?.id == sentence.id {
                                Button(action: {
                                    nativeAudio.stopRecording()
                                    gamification.incrementQuestProgress(id: "q_shadowing")
                                }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "stop.circle.fill")
                                            .foregroundColor(.red)
                                        Text("Stop Recording")
                                            .font(.caption)
                                            .fontWeight(.bold)
                                            .foregroundColor(.red)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.red.opacity(0.15))
                                    .cornerRadius(10)
                                }

                                // Waveform
                                HStack(spacing: 3) {
                                    ForEach(0..<5) { idx in
                                        RoundedRectangle(cornerRadius: 2)
                                            .fill(Color.red)
                                            .frame(width: 3, height: 16 * nativeAudio.recordingPowerLevels[idx])
                                    }
                                }
                            } else {
                                Button(action: {
                                    selectedSentenceForRecording = sentence
                                    nativeAudio.startRecordingSentence(id: sentence.id)
                                }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: "mic.fill")
                                        Text("Record Shadowing")
                                            .font(.caption)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.accentColor.opacity(0.15))
                                    .foregroundColor(.accentColor)
                                    .cornerRadius(10)
                                }
                            }

                            if selectedSentenceForRecording?.id == sentence.id && nativeAudio.userAudioRecordingUrl != nil && !nativeAudio.isRecordingShadowing {
                                Button(action: {
                                    if nativeAudio.isPlayingUserRecording {
                                        nativeAudio.stopUserPlayback()
                                    } else {
                                        nativeAudio.playUserRecording()
                                    }
                                }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: nativeAudio.isPlayingUserRecording ? "stop.fill" : "play.circle.fill")
                                        Text(nativeAudio.isPlayingUserRecording ? "Stop" : "My Voice")
                                            .font(.caption)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.green.opacity(0.15))
                                    .foregroundColor(.green)
                                    .cornerRadius(10)
                                }
                            }

                            Spacer()
                        }
                    }
                    .padding(14)
                    .background(.ultraThinMaterial)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(isActive ? Color.accentColor : Color.clear, lineWidth: 2)
                    )
                    .cornerRadius(16)
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 12)
        }
    }

    private var vocabularyListView: some View {
        ScrollView {
            VStack(spacing: 12) {
                ForEach(newsItem.vocabulary) { vocab in
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Text(vocab.word)
                                .font(.system(size: 18, weight: .bold))
                            Text("【\(vocab.reading)】")
                                .font(.system(size: 14))
                                .foregroundColor(.secondary)

                            Spacer()

                            Text(vocab.pitchAccent)
                                .font(.caption2)
                                .fontWeight(.bold)
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.orange.opacity(0.2))
                                .foregroundColor(.orange)
                                .cornerRadius(6)

                            Button(action: {
                                AudioService.shared.speak(text: vocab.word)
                            }) {
                                Image(systemName: "speaker.wave.2.fill")
                                    .font(.caption)
                                    .foregroundColor(.accentColor)
                            }
                        }

                        Text(vocab.meaning)
                            .font(.system(size: 14, weight: .medium))
                            .foregroundColor(.primary)

                        Text("例: \(vocab.example)")
                            .font(.system(size: 12))
                            .foregroundColor(.secondary)
                            .padding(.top, 2)
                    }
                    .padding(14)
                    .background(.ultraThinMaterial)
                    .cornerRadius(14)
                }
            }
            .padding()
        }
    }

    private var quizView: some View {
        ScrollView {
            VStack(spacing: 16) {
                ForEach(newsItem.comprehensionQuiz) { quiz in
                    VStack(alignment: .leading, spacing: 14) {
                        HStack {
                            Image(systemName: "questionmark.circle.fill")
                                .foregroundColor(.accentColor)
                            Text("Comprehension Check (内容理解)")
                                .font(.system(size: 14, weight: .bold))
                        }

                        Text(quiz.question)
                            .font(.system(size: 16, weight: .semibold))

                        VStack(spacing: 10) {
                            ForEach(0..<quiz.options.count, id: \.self) { idx in
                                Button(action: {
                                    selectedQuizAnswer = idx
                                    showQuizFeedback = true
                                    if idx == quiz.correctIndex && !isCompletedAwardGiven {
                                        isCompletedAwardGiven = true
                                        gamification.addRewards(tp: 30, exp: 50)
                                    }
                                }) {
                                    HStack {
                                        Text("\(["A", "B", "C", "D"][idx]).")
                                            .font(.caption)
                                            .fontWeight(.bold)
                                            .foregroundColor(.secondary)

                                        Text(quiz.options[idx])
                                            .font(.system(size: 14))
                                            .foregroundColor(.primary)

                                        Spacer()

                                        if showQuizFeedback {
                                            if idx == quiz.correctIndex {
                                                Image(systemName: "checkmark.circle.fill")
                                                    .foregroundColor(.green)
                                            } else if selectedQuizAnswer == idx {
                                                Image(systemName: "xmark.circle.fill")
                                                    .foregroundColor(.red)
                                            }
                                        }
                                    }
                                    .padding(12)
                                    .background(
                                        showQuizFeedback && idx == quiz.correctIndex
                                        ? Color.green.opacity(0.15)
                                        : (showQuizFeedback && selectedQuizAnswer == idx ? Color.red.opacity(0.15) : Color.white.opacity(0.08))
                                    )
                                    .cornerRadius(10)
                                }
                            }
                        }

                        if showQuizFeedback {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("解説 (Explanation):")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.secondary)
                                Text(quiz.explanation)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(10)
                            .background(Color.blue.opacity(0.1))
                            .cornerRadius(8)
                        }
                    }
                    .padding(16)
                    .background(.ultraThinMaterial)
                    .cornerRadius(16)
                }
            }
            .padding()
        }
    }
}
