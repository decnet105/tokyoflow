import SwiftUI

public struct MangaPanelReaderView: View {
    public let lesson: MangaLesson
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedPanelIndex = 0
    @State private var expandedBalloonId: String? = nil
    @State private var activeBurstSFX: MangaSFX? = nil
    @State private var isRTLReadingMode = false

    public var body: some View {
        ZStack {
            MangaThemeBackgroundView()

            ScrollView {
                VStack(spacing: 24) {
                    // Header & Mode Switcher
                    VStack(alignment: .leading, spacing: 10) {
                        HStack {
                            Text(lesson.genre)
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.purple)
                            Spacer()
                            Text(lesson.difficulty)
                                .font(.caption2)
                                .fontWeight(.semibold)
                                .foregroundColor(.secondary)
                        }

                        Text(lesson.title)
                            .font(.title2)
                            .fontWeight(.bold)
                        Text(lesson.titleJa)
                            .font(.subheadline)
                            .foregroundColor(.secondary)

                        // Reading Mode & Furigana Toggles
                        HStack(spacing: 10) {
                            Button(action: { isRTLReadingMode.toggle() }) {
                                HStack(spacing: 4) {
                                    Image(systemName: isRTLReadingMode ? "arrow.left.and.right.righttriangle.left.righttriangle.right.fill" : "arrow.up.and.down.circle")
                                    Text(isRTLReadingMode ? "Tankobon RTL (右開き)" : "Vertical Scroll")
                                        .font(.caption)
                                        .fontWeight(.bold)
                                }
                                .padding(.horizontal, 10)
                                .padding(.vertical, 6)
                                .background(Color.purple.opacity(0.12))
                                .foregroundColor(.purple)
                                .cornerRadius(8)
                            }

                            Button(action: { userProfile.furiganaEnabled.toggle() }) {
                                HStack(spacing: 4) {
                                    Image(systemName: userProfile.furiganaEnabled ? "character.phonetic" : "character")
                                    Text("Furigana: \(userProfile.furiganaEnabled ? "ON" : "OFF")")
                                        .font(.caption)
                                        .fontWeight(.semibold)
                                }
                                .padding(.horizontal, 10)
                                .padding(.vertical, 6)
                                .background(Color.primary.opacity(0.08))
                                .cornerRadius(8)
                            }
                        }
                        .padding(.top, 4)
                    }
                    .padding()
                    .background(.ultraThinMaterial)
                    .cornerRadius(16)
                    .padding(.horizontal)

                    // Comic Panels Section (Vertical or RTL Horizontal Paging)
                    if isRTLReadingMode {
                        TabView(selection: $selectedPanelIndex) {
                            ForEach(Array(lesson.panels.enumerated()), id: \.offset) { index, panel in
                                InteractiveMangaFrame(
                                    panel: panel,
                                    showFurigana: userProfile.furiganaEnabled,
                                    expandedBalloonId: $expandedBalloonId,
                                    onSFXTap: { sfx in
                                        triggerSFXBurst(sfx)
                                    }
                                )
                                .padding(.horizontal)
                                .tag(index)
                            }
                        }
                        .tabViewStyle(.page(indexDisplayMode: .always))
                        .frame(height: 380)
                    } else {
                        VStack(spacing: 20) {
                            ForEach(lesson.panels) { panel in
                                InteractiveMangaFrame(
                                    panel: panel,
                                    showFurigana: userProfile.furiganaEnabled,
                                    expandedBalloonId: $expandedBalloonId,
                                    onSFXTap: { sfx in
                                        triggerSFXBurst(sfx)
                                    }
                                )
                                .padding(.horizontal)
                            }
                        }
                    }

                    // Manga Grammar & Spoken Contractions
                    VStack(alignment: .leading, spacing: 14) {
                        Text("MANGA COLLOQUIAL GRAMMAR")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.secondary)
                            .tracking(1.2)
                            .padding(.horizontal)

                        ForEach(lesson.grammarBreakdowns) { grammar in
                            VStack(alignment: .leading, spacing: 8) {
                                HStack {
                                    Text(grammar.pattern)
                                        .font(.headline)
                                        .foregroundColor(.purple)
                                    Spacer()
                                    AudioButton(textToSpeak: grammar.pattern)
                                }
                                Text(grammar.explanation)
                                    .font(.footnote)
                                    .foregroundColor(.primary.opacity(0.85))

                                HStack(alignment: .top, spacing: 6) {
                                    Text("Example:")
                                        .font(.caption2)
                                        .fontWeight(.bold)
                                        .foregroundColor(.secondary)
                                    Text(grammar.example)
                                        .font(.caption)
                                        .foregroundColor(.primary)
                                }
                                .padding(8)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(Color(.systemGray6))
                                .cornerRadius(8)
                            }
                            .padding()
                            .background(Color(.secondarySystemGroupedBackground))
                            .cornerRadius(14)
                            .padding(.horizontal)
                        }
                    }

                    // Complete Lesson Button
                    Button(action: {
                        userProfile.markMangaCompleted(lesson.id)
                        #if os(iOS)
                        let generator = UINotificationFeedbackGenerator()
                        generator.notificationOccurred(.success)
                        #endif
                    }) {
                        HStack {
                            Image(systemName: "checkmark.circle.fill")
                            Text(userProfile.completedMangaLessonIds.contains(lesson.id) ? "Lesson Mastered" : "Mark as Mastered")
                                .font(.headline)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(16)
                    }
                    .padding(.horizontal)
                    .padding(.bottom)
                }
                .padding(.vertical)
            }
            .navigationTitle("Manga Reader")
            .navigationBarTitleDisplayMode(.inline)

            // Dynamic Action Starburst Overlay
            if let burst = activeBurstSFX {
                ComicBurstOverlay(
                    sfxText: burst.japanese,
                    meaning: burst.meaning,
                    isPresented: Binding(
                        get: { activeBurstSFX != nil },
                        set: { if !$0 { activeBurstSFX = nil } }
                    )
                )
            }
        }
    }

    private func triggerSFXBurst(_ sfx: MangaSFX) {
        AudioService.shared.speak(text: sfx.japanese, rate: 0.58)
        withAnimation {
            activeBurstSFX = sfx
        }
    }
}

public struct InteractiveMangaFrame: View {
    public let panel: MangaPanel
    public let showFurigana: Bool
    @Binding public var expandedBalloonId: String?
    public var onSFXTap: ((MangaSFX) -> Void)? = nil

    public var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            // Panel Header & Scene Setup
            HStack {
                Text("PANEL \(panel.panelNumber)")
                    .font(.caption2)
                    .fontWeight(.heavy)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.black)
                    .foregroundColor(.white)
                    .cornerRadius(4)

                Text(panel.sceneDescription)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .italic()
            }

            // Manga SFX Sound Effect Visual Banner
            HStack(spacing: 12) {
                ForEach(panel.sfx) { sfx in
                    SFXBadge(sfx: sfx, onTap: {
                        onSFXTap?(sfx)
                    })
                }
            }

            // Dialogue Balloons
            VStack(spacing: 10) {
                ForEach(panel.balloons) { balloon in
                    MangaSpeechBalloonView(
                        balloon: balloon,
                        showFurigana: showFurigana,
                        isExpanded: expandedBalloonId == balloon.id,
                        onTap: {
                            if expandedBalloonId == balloon.id {
                                expandedBalloonId = nil
                            } else {
                                expandedBalloonId = balloon.id
                            }
                        }
                    )
                }
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
        .overlay(
            RoundedRectangle(cornerRadius: 18)
                .stroke(Color.primary.opacity(0.12), lineWidth: 1.5)
        )
    }
}

public struct SFXBadge: View {
    public let sfx: MangaSFX
    public var onTap: (() -> Void)? = nil

    public var body: some View {
        Button(action: {
            onTap?()
        }) {
            HStack(spacing: 6) {
                Text(sfx.japanese)
                    .font(.system(size: 18, weight: .black, design: .serif))
                    .foregroundColor(.red)

                VStack(alignment: .leading, spacing: 0) {
                    Text(sfx.romaji)
                        .font(.system(size: 9, weight: .bold))
                        .foregroundColor(.secondary)
                    Text(sfx.meaning)
                        .font(.system(size: 10))
                        .foregroundColor(.primary)
                        .lineLimit(1)
                }

                Image(systemName: "sparkles")
                    .font(.caption2)
                    .foregroundColor(.orange)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 6)
            .background(Color.red.opacity(0.08))
            .cornerRadius(10)
        }
        .buttonStyle(.plain)
    }
}

public struct MangaSpeechBalloonView: View {
    public let balloon: MangaBalloon
    public let showFurigana: Bool
    public let isExpanded: Bool
    public let onTap: () -> Void
    @ObservedObject private var audioService = AudioService.shared

    public var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Button(action: onTap) {
                HStack(alignment: .top) {
                    VStack(alignment: .leading, spacing: 4) {
                        HStack(spacing: 6) {
                            Text(balloon.speaker)
                                .font(.caption2)
                                .fontWeight(.bold)
                                .foregroundColor(.purple)
                            if balloon.bubbleType == "thought_cloud" {
                                Text("(Inner Monologue)")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                            if audioService.isSpeaking && audioService.currentSpeakingText == balloon.japanese {
                                WaveformVisualizerView(height: 12, color: .purple)
                            }
                        }

                        FuriganaText(
                            textWithFurigana: balloon.furigana,
                            fallbackText: balloon.japanese,
                            showFurigana: showFurigana,
                            font: .system(size: 17, weight: .semibold)
                        )
                    }
                    Spacer()
                    AudioButton(textToSpeak: balloon.japanese)
                }
            }
            .buttonStyle(.plain)

            if isExpanded {
                VStack(alignment: .leading, spacing: 4) {
                    Divider()
                    Text(balloon.romaji)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text(balloon.english)
                        .font(.footnote)
                        .foregroundColor(.primary)
                    Text(balloon.chinese)
                        .font(.caption2)
                        .foregroundColor(.secondary)

                    HStack(alignment: .top, spacing: 4) {
                        Image(systemName: "info.circle")
                            .font(.caption2)
                            .foregroundColor(.purple)
                        Text(balloon.nuanceNotes)
                            .font(.caption)
                            .foregroundColor(.purple)
                    }
                    .padding(.top, 2)
                }
                .padding(.top, 4)
                .transition(.opacity.combined(with: .move(edge: .top)))
            }
        }
        .padding(14)
        .background(balloon.bubbleType == "thought_cloud" ? Color.blue.opacity(0.06) : Color(.systemGray6))
        .cornerRadius(14)
    }
}
