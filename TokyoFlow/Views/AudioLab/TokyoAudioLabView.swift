import SwiftUI

public struct TokyoAudioLabView: View {
    @ObservedObject var dataManager = DataManager.shared
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedAnnouncementId: String? = nil
    @State private var selectedQuizAnswers: [String: Int] = [:]
    @State private var showQuizFeedback: [String: Bool] = [:]

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Banner
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("TOKYO AUDIO LAB")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(.teal)
                                    .tracking(1.5)
                                Text("Station & Store Listening")
                                    .font(.system(size: 26, weight: .bold, design: .rounded))
                            }
                            Spacer()
                            Image(systemName: "headphones.circle.fill")
                                .font(.system(size: 36))
                                .foregroundColor(.teal)
                        }

                        Text("Train your ear to high-speed native Japanese station chimes, train approaching announcements, in-store jingles, and delay apologies.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.horizontal)
                    .padding(.top, 8)

                    // Announcements List
                    LazyVStack(spacing: 16) {
                        ForEach(dataManager.announcements) { ann in
                            AnnouncementCard(
                                announcement: ann,
                                showFurigana: userProfile.furiganaEnabled,
                                selectedQuizAnswer: Binding(
                                    get: { selectedQuizAnswers[ann.id] },
                                    set: { selectedQuizAnswers[ann.id] = $0 }
                                ),
                                showFeedback: Binding(
                                    get: { showQuizFeedback[ann.id] ?? false },
                                    set: { showQuizFeedback[ann.id] = $0 }
                                )
                            )
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.bottom, 24)
            }
            .navigationTitle("Audio Lab")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

public struct AnnouncementCard: View {
    public let announcement: Announcement
    public let showFurigana: Bool
    @Binding public var selectedQuizAnswer: Int?
    @Binding public var showFeedback: Bool

    public var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            // Header
            HStack {
                Label(announcement.location, systemImage: "speaker.wave.3.fill")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.teal)
                Spacer()
                AudioButton(textToSpeak: announcement.audioPrompt, rate: 0.52)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(announcement.title)
                    .font(.headline)
                Text(announcement.titleJa)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            // Japanese text & furigana
            VStack(alignment: .leading, spacing: 6) {
                FuriganaText(
                    textWithFurigana: announcement.furigana,
                    fallbackText: announcement.japanese,
                    showFurigana: showFurigana,
                    font: .system(size: 15, weight: .medium)
                )

                Text(announcement.romaji)
                    .font(.caption2)
                    .foregroundColor(.secondary)

                Text(announcement.english)
                    .font(.footnote)
                    .foregroundColor(.primary.opacity(0.85))
                    .padding(.top, 2)

                Text(announcement.chinese)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            .padding(12)
            .background(Color(.systemGray6))
            .cornerRadius(12)

            // Listening Comprehension Quiz
            if let quiz = announcement.listeningQuiz {
                VStack(alignment: .leading, spacing: 10) {
                    Text("🎧 Listening Check")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.teal)

                    Text(quiz.question)
                        .font(.subheadline)
                        .fontWeight(.semibold)

                    VStack(spacing: 8) {
                        ForEach(Array(quiz.options.enumerated()), id: \.offset) { idx, option in
                            Button(action: {
                                selectedQuizAnswer = idx
                                showFeedback = true
                            }) {
                                HStack {
                                    Image(systemName: selectedQuizAnswer == idx
                                          ? (idx == quiz.correctIndex ? "checkmark.circle.fill" : "xmark.circle.fill")
                                          : "circle")
                                        .foregroundColor(selectedQuizAnswer == idx
                                                         ? (idx == quiz.correctIndex ? .green : .red)
                                                         : .secondary)
                                    Text(option)
                                        .font(.footnote)
                                        .foregroundColor(.primary)
                                    Spacer()
                                }
                                .padding(10)
                                .background(
                                    selectedQuizAnswer == idx
                                    ? (idx == quiz.correctIndex ? Color.green.opacity(0.12) : Color.red.opacity(0.12))
                                    : Color(.systemBackground)
                                )
                                .cornerRadius(10)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                }
                .padding(12)
                .background(Color.teal.opacity(0.08))
                .cornerRadius(12)
            }
        }
        .padding(16)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.04), radius: 8, x: 0, y: 2)
    }
}
