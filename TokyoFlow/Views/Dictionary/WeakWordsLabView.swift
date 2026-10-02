import SwiftUI

public struct WeakWordsLabView: View {
    @StateObject private var tracker = WeakWordTrackerService.shared
    @StateObject private var audioService = AudioService.shared
    @ObservedObject private var languageManager = LanguageManager.shared
    @Environment(\.dismiss) private var dismiss

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 16) {
                        // Header Insight Banner
                        VStack(spacing: 8) {
                            HStack {
                                Image(systemName: "bolt.heart.fill")
                                    .font(.title2)
                                    .foregroundColor(.red)
                                Text(languageManager.isEnglish ? "AI Weakness & Word Recovery Lab" : "AI 抗遗忘错题本与弱词实验室")
                                    .font(.system(size: 18, weight: .black, design: .rounded))
                                Spacer()
                                Text("\(tracker.masteredCount) " + (languageManager.isEnglish ? "Mastered" : "已掌握"))
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.green)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.green.opacity(0.15))
                                    .cornerRadius(8)
                            }

                            Text(languageManager.isEnglish ? "Automatically captures hesitated terms, replayed audio, and quiz mistakes across Kana, Scenarios, and NHK News for targeted spaced repetition." : "自动追踪假名、实战对话与新闻跟读中的重播、犹豫和答错词汇，进行艾宾浩斯强化复习。")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        if tracker.activeWeakWords.isEmpty {
                            VStack(spacing: 14) {
                                Image(systemName: "sparkles")
                                    .font(.system(size: 48))
                                    .foregroundColor(.orange)
                                Text(languageManager.isEnglish ? "No weak words yet!" : "暂无待复习弱词！")
                                    .font(.headline)
                                Text(languageManager.isEnglish ? "As you practice Kana, scenario dialogues, and news shadowing, unfamiliar words will automatically appear here for review." : "在假名练习、实战对话与新闻跟读中遇到的生词将自动沉淀至此。")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                    .multilineTextAlignment(.center)
                                    .padding(.horizontal, 30)
                            }
                            .padding(.top, 60)
                        } else {
                            LazyVStack(spacing: 12) {
                                ForEach(tracker.activeWeakWords) { item in
                                    WeakWordCardRow(
                                        item: item,
                                        isEnglish: languageManager.isEnglish,
                                        onPlayAudio: {
                                            audioService.speak(text: item.word, reading: item.reading)
                                            tracker.recordListen(word: item.word, reading: item.reading, meaning: item.meaning)
                                        },
                                        onMastered: {
                                            withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
                                                tracker.markMastered(word: item.word)
                                            }
                                        },
                                        onDelete: {
                                            withAnimation {
                                                tracker.removeWeakWord(word: item.word)
                                            }
                                        }
                                    )
                                }
                            }
                            .padding(.horizontal)
                            .padding(.bottom, 40)
                        }
                    }
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Weakness Drill Lab" : "抗遗忘错题本")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(languageManager.isEnglish ? "Done" : "完成") {
                        dismiss()
                    }
                    .fontWeight(.bold)
                }
            }
        }
    }
}

public struct WeakWordCardRow: View {
    public let item: WeakWordItem
    public var isEnglish: Bool = true
    public let onPlayAudio: () -> Void
    public let onMastered: () -> Void
    public let onDelete: () -> Void

    public var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                HStack(spacing: 8) {
                    Text(item.word)
                        .font(.system(size: 20, weight: .black, design: .rounded))
                    if !item.reading.isEmpty {
                        Text("[\(item.reading)]")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.accentColor)
                    }
                }

                if !item.romaji.isEmpty {
                    Text(item.romaji)
                        .font(.system(size: 12, weight: .medium, design: .monospaced))
                        .foregroundColor(.purple)
                }

                if !item.meaning.isEmpty {
                    Text(item.meaning)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                // AI Diagnostic Reason Tag
                Text(item.reason)
                    .font(.system(size: 10, weight: .bold))
                    .foregroundColor(.orange)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.orange.opacity(0.12))
                    .cornerRadius(6)
            }

            Spacer()

            // Audio Pronunciation Button
            Button(action: onPlayAudio) {
                Image(systemName: "speaker.wave.2.fill")
                    .font(.caption)
                    .foregroundColor(.white)
                    .padding(8)
                    .background(Color.accentColor)
                    .clipShape(Circle())
            }

            // Mark Mastered (+5TP) Button
            Button(action: onMastered) {
                HStack(spacing: 2) {
                    Image(systemName: "checkmark")
                    Text(isEnglish ? "Mastered" : "已掌握")
                }
                .font(.caption2)
                .fontWeight(.bold)
                .foregroundColor(.green)
                .padding(.horizontal, 8)
                .padding(.vertical, 6)
                .background(Color.green.opacity(0.15))
                .cornerRadius(8)
            }
        }
        .padding(14)
        .background(.ultraThinMaterial)
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.primary.opacity(0.06), lineWidth: 1)
        )
    }
}
