import SwiftUI

public struct TokyoScenarioYTPlayerView: View {
    public let lesson: TokyoScenarioVideoLesson
    @Environment(\.dismiss) private var dismiss
    @Environment(\.openURL) private var openURL
    @State private var selectedTab: Int = 0 // 0: Chapters, 1: Key Phrases, 2: Channel Info
    @ObservedObject private var audioService = AudioService.shared
    @ObservedObject private var gamification = GamificationService.shared

    public init(lesson: TokyoScenarioVideoLesson) {
        self.lesson = lesson
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 16) {
                        // YouTube Player Container
                        ZStack {
                            RoundedRectangle(cornerRadius: 16)
                                .fill(Color.black)
                                .aspectRatio(16/9, contentMode: .fit)

                            TokyoYouTubeWebView(videoId: lesson.youtubeVideoId)
                                .cornerRadius(16)
                        }
                        .padding(.horizontal)
                        .shadow(color: Color.black.opacity(0.25), radius: 10, x: 0, y: 5)

                        // Title & YouTube Channel Info Card
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text(lesson.levelBadge)
                                    .font(.system(size: 10, weight: .bold))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 4)
                                    .background(Color.orange.opacity(0.2))
                                    .foregroundColor(.orange)
                                    .cornerRadius(6)

                                Label(lesson.district, systemImage: "mappin.circle.fill")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                Spacer()

                                HStack(spacing: 4) {
                                    Image(systemName: "clock")
                                    Text(lesson.durationLabel)
                                }
                                .font(.caption2)
                                .foregroundColor(.secondary)
                            }

                            Text(lesson.title)
                                .font(.system(size: 17, weight: .bold))
                                .foregroundColor(.primary)

                            Text(lesson.titleJa)
                                .font(.subheadline)
                                .foregroundColor(.secondary)

                            // Channel badge and Open in YouTube CTA
                            HStack {
                                HStack(spacing: 8) {
                                    Circle()
                                        .fill(
                                            LinearGradient(
                                                colors: [Color.red, Color.orange],
                                                startPoint: .topLeading,
                                                endPoint: .bottomTrailing
                                            )
                                        )
                                        .frame(width: 32, height: 32)
                                        .overlay(
                                            Image(systemName: "play.tv.fill")
                                                .font(.system(size: 14))
                                                .foregroundColor(.white)
                                        )

                                    VStack(alignment: .leading, spacing: 1) {
                                        Text(lesson.channelName)
                                            .font(.system(size: 12, weight: .bold))
                                        Text("Official YouTube Channel")
                                            .font(.system(size: 10))
                                            .foregroundColor(.secondary)
                                    }
                                }

                                Spacer()

                                // Open in YouTube Button
                                Button(action: {
                                    gamification.addRewards(tp: 10, exp: 20)
                                    if UIApplication.shared.canOpenURL(lesson.youtubeAppUrl) {
                                        openURL(lesson.youtubeAppUrl)
                                    } else {
                                        openURL(lesson.youtubeWatchUrl)
                                    }
                                }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: "play.rectangle.fill")
                                            .foregroundColor(.red)
                                        Text("Play on YouTube")
                                            .font(.system(size: 11, weight: .bold))
                                            .foregroundColor(.primary)
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(Color.red.opacity(0.12))
                                    .cornerRadius(8)
                                }
                            }
                            .padding(.top, 4)
                        }
                        .padding()
                        .background(.ultraThinMaterial)
                        .cornerRadius(16)
                        .padding(.horizontal)

                        // Segmented Picker for Lesson Tabs
                        Picker("Lesson Mode", selection: $selectedTab) {
                            Text("📑 Key Phrases (\(lesson.keyTakeaways.count))").tag(0)
                            Text("⏱ Chapters (\(lesson.chapters.count))").tag(1)
                            Text("💡 Syllabus").tag(2)
                        }
                        .pickerStyle(.segmented)
                        .padding(.horizontal)

                        // Tab 0: Key Takeaway Flashcards
                        if selectedTab == 0 {
                            VStack(spacing: 12) {
                                ForEach(lesson.keyTakeaways) { item in
                                    VStack(alignment: .leading, spacing: 6) {
                                        HStack {
                                            VStack(alignment: .leading, spacing: 2) {
                                                Text(item.furigana)
                                                    .font(.system(size: 11))
                                                    .foregroundColor(.secondary)
                                                Text(item.phrase)
                                                    .font(.system(size: 16, weight: .bold))
                                                    .foregroundColor(.primary)
                                            }

                                            Spacer()

                                            Button(action: {
                                                audioService.speak(text: item.phrase)
                                            }) {
                                                Image(systemName: "speaker.wave.2.fill")
                                                    .font(.caption)
                                                    .foregroundColor(.white)
                                                    .padding(8)
                                                    .background(Color.accentColor)
                                                    .clipShape(Circle())
                                            }
                                        }

                                        Text(item.meaning)
                                            .font(.system(size: 13, weight: .semibold))
                                            .foregroundColor(.accentColor)

                                        Text(item.explanation)
                                            .font(.system(size: 12))
                                            .foregroundColor(.secondary)
                                            .padding(.top, 2)
                                    }
                                    .padding(14)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(14)
                                }
                            }
                            .padding(.horizontal)
                        } else if selectedTab == 1 {
                            // Tab 1: Timestamp Chapter Bookmarks
                            VStack(spacing: 10) {
                                ForEach(lesson.chapters) { ch in
                                    HStack(alignment: .top, spacing: 12) {
                                        Text(ch.timeString)
                                            .font(.system(size: 12, weight: .bold, design: .monospaced))
                                            .foregroundColor(.white)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(Color.accentColor)
                                            .cornerRadius(6)

                                        VStack(alignment: .leading, spacing: 2) {
                                            Text(ch.title)
                                                .font(.system(size: 14, weight: .bold))
                                                .foregroundColor(.primary)
                                            Text(ch.summary)
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }

                                        Spacer()
                                    }
                                    .padding(12)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(12)
                                }
                            }
                            .padding(.horizontal)
                        } else {
                            // Tab 2: Lesson Syllabus & Method
                            VStack(alignment: .leading, spacing: 12) {
                                Text("🎥 TokyoFlow Method: Learn In Context")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(.accentColor)

                                Text(lesson.summary)
                                    .font(.system(size: 13))
                                    .foregroundColor(.primary.opacity(0.9))

                                Divider()

                                Text("💡 3-Step High-Efficiency Learning Flow:")
                                    .font(.system(size: 13, weight: .bold))

                                Text("1. Immersive Listening: Watch genuine Tokyo native video with native pacing.")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                Text("2. Core Phrase Mastery: Study 1-second survival response phrases with instant pronunciation.")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                Text("3. Scenario Roleplay: Jump into the interactive Scenario drill to test your instincts.")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(16)
                            .background(.ultraThinMaterial)
                            .cornerRadius(14)
                            .padding(.horizontal)
                        }
                    }
                    .padding(.bottom, 30)
                }
            }
            .navigationTitle("Scenario Masterclass")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
