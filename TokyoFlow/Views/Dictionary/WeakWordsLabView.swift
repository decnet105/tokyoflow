import SwiftUI

public struct WeakWordsLabView: View {
    @StateObject private var tracker = WeakWordTrackerService.shared
    @StateObject private var audioService = AudioService.shared
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
                                Text("AI Weakness & Word Recovery Lab")
                                    .font(.system(size: 18, weight: .black, design: .rounded))
                                Spacer()
                                Text("\(tracker.masteredCount) Mastered")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.green)
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.green.opacity(0.15))
                                    .cornerRadius(8)
                            }

                            Text("Automatically captures hesitated terms, replayed audio, and quiz mistakes across Kana, Scenarios, and NHK News for targeted spaced repetition.")
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
                                Text("No weak words yet!")
                                    .font(.headline)
                                Text("As you practice Kana, scenario dialogues, and news shadowing, unfamiliar words will automatically appear here for review.")
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
                                        onPlayAudio: {
                                            audioService.speak(text: item.word)
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
            .navigationTitle("Weakness Drill Lab")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
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
                    Text("Mastered")
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
