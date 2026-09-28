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

                TokyoDuoAdaptiveLayout(duoSplitRatio: 0.48, minimumDuoWidth: 680) {
                    // Left Screen / Primary Pane: Video Player & Overview
                    ScrollView {
                        VStack(spacing: 14) {
                            TokyoFastVideoPlayerContainer(
                                videoId: lesson.youtubeVideoId,
                                title: lesson.title,
                                durationLabel: lesson.durationLabel
                            )

                            // Direct Launch in YouTube App Bar
                            Button(action: {
                                gamification.addRewards(tp: 10, exp: 20)
                                if UIApplication.shared.canOpenURL(lesson.youtubeAppUrl) {
                                    openURL(lesson.youtubeAppUrl)
                                } else {
                                    openURL(lesson.youtubeWatchUrl)
                                }
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "play.rectangle.fill")
                                        .foregroundColor(.red)
                                        .font(.headline)
                                    Text("Watch in YouTube App / Full Quality")
                                        .font(.system(size: 13, weight: .bold))
                                        .foregroundColor(.primary)
                                    Spacer()
                                    Image(systemName: "arrow.up.forward.app.fill")
                                        .foregroundColor(.red)
                                }
                                .padding(.horizontal, 14)
                                .padding(.vertical, 10)
                                .background(.ultraThinMaterial)
                                .cornerRadius(12)
                            }
                            .buttonStyle(.plain)

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

                                Divider()

                                HStack {
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
                                    Spacer()
                                }
                            }
                            .padding()
                            .background(.ultraThinMaterial)
                            .cornerRadius(16)
                        }
                        .padding(14)
                    }
                } secondaryContent: {
                    // Right Screen / Secondary Pane: Interactive Phrases, Chapters & Syllabus
                    ScrollView {
                        VStack(spacing: 14) {
                            Picker("Lesson Mode", selection: $selectedTab) {
                                Text("📑 Key Phrases (\(lesson.keyTakeaways.count))").tag(0)
                                Text("⏱ Chapters (\(lesson.chapters.count))").tag(1)
                                Text("💡 Syllabus").tag(2)
                            }
                            .pickerStyle(.segmented)

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
                                                AudioButton(textToSpeak: item.phrase)
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
                            } else if selectedTab == 1 {
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
                            } else {
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
                            }
                        }
                        .padding(14)
                    }
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
