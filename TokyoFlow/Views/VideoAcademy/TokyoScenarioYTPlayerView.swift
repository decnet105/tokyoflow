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
                        videoPrimaryPane
                            .padding(14)
                    }
                } secondaryContent: {
                    // Right Screen / Secondary Pane: Interactive Phrases, Chapters & Syllabus
                    ScrollView {
                        videoSecondaryPane
                            .padding(14)
                    }
                } singleContent: {
                    //  iPhone Single Screen: Unified stream with video + interactive tabs + action bar
                    ScrollView {
                        VStack(spacing: 16) {
                            videoPrimaryPane
                            videoSecondaryPane
                            
                            // Bottom Action Bar
                            Button(action: {
                                UIImpactFeedbackGenerator(style: .medium).impactOccurred()
                                gamification.addRewards(tp: 25, exp: 35)
                                dismiss()
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "checkmark.seal.fill")
                                    Text("Complete Masterclass Lesson (+25 TP)")
                                        .fontWeight(.heavy)
                                }
                                .font(.system(size: 15))
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 14)
                                .background(
                                    LinearGradient(
                                        colors: [Color.orange, Color.red],
                                        startPoint: .leading,
                                        endPoint: .trailing
                                    )
                                )
                                .cornerRadius(14)
                                .shadow(color: Color.orange.opacity(0.3), radius: 8, x: 0, y: 4)
                            }
                            .padding(.top, 8)
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

    private var videoPrimaryPane: some View {
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

                Text(lesson.localizedTitle)
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
                        Text(LanguageManager.shared.isEnglish ? "Official YouTube Channel" : "官方 YouTube 频道")
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
    }

    private var videoSecondaryPane: some View {
        VStack(spacing: 14) {
            Picker("Lesson Mode", selection: $selectedTab) {
                Text(LanguageManager.shared.isEnglish ? "Key Phrases (\(lesson.keyTakeaways.count))" : "核心金句 (\(lesson.keyTakeaways.count))").tag(0)
                Text(LanguageManager.shared.isEnglish ? "Chapters (\(lesson.chapters.count))" : "精讲章节 (\(lesson.chapters.count))").tag(1)
                Text(LanguageManager.shared.isEnglish ? "Syllabus" : "实战大纲").tag(2)
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

                            Text(item.localizedMeaning)
                                .font(.system(size: 13, weight: .semibold))
                                .foregroundColor(.accentColor)

                            Text(item.localizedExplanation)
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
                                Text(ch.localizedTitle)
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(.primary)
                                Text(ch.localizedSummary)
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
                    Text(LanguageManager.shared.isEnglish ? "TokyoFlow Method: Learn In Context" : "TokyoFlow 场景实战速通法则")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(.accentColor)

                    Text(lesson.localizedSummary)
                        .font(.system(size: 13))
                        .foregroundColor(.primary.opacity(0.9))

                    Divider()

                    Text(LanguageManager.shared.isEnglish ? "3-Step High-Efficiency Learning Flow:" : "3步高能速通闭环：")
                        .font(.system(size: 13, weight: .bold))

                    Text(LanguageManager.shared.isEnglish ? "1. Immersive Listening: Watch genuine Tokyo native video with native pacing." : "1. 沉浸式盲听：感知东京本土真实语速与抑扬顿挫。")
                        .font(.caption)
                        .foregroundColor(.secondary)

                    Text(LanguageManager.shared.isEnglish ? "2. Core Phrase Mastery: Study 1-second survival response phrases with instant pronunciation." : "2. 核心句内化：掌握1秒条件反射短语与真人发音。")
                        .font(.caption)
                        .foregroundColor(.secondary)

                    Text(LanguageManager.shared.isEnglish ? "3. Scenario Roleplay: Jump into the interactive Scenario drill to test your instincts." : "3. 场景实境演练：进入互动模拟检验你的临场反应。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding(16)
                .background(.ultraThinMaterial)
                .cornerRadius(14)
            }
        }
    }
}
