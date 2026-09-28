import SwiftUI

public struct TokyoRadioPlayerModalView: View {
    public let station: TokyoRadioStation

    @ObservedObject var radioService = TokyoRadioService.shared
    @Environment(\.dismiss) private var dismiss
    @State private var isDraggingSlider = false
    @State private var sliderValue: Double = 0.0
    @State private var selectedViewMode: Int = 1 // 0: Chapters, 1: Live Shadowing (Word-by-Word)
    @State private var showFurigana: Bool = true
    @State private var showRomaji: Bool = true

    public init(station: TokyoRadioStation) {
        self.station = station
    }

    private var allSentences: [NewsSentence] {
        station.chapters.flatMap { $0.transcriptSentences }
    }

    private var activeSentence: NewsSentence? {
        let cur = radioService.currentTimeSec
        guard let first = allSentences.first else { return nil }
        if cur < first.startTimeSec { return first }

        for (i, sent) in allSentences.enumerated() {
            let nextStart = (i + 1 < allSentences.count) ? allSentences[i + 1].startTimeSec : (sent.endTimeSec + 2.0)
            if cur >= sent.startTimeSec && cur < nextStart {
                return sent
            }
        }
        return allSentences.last
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(spacing: 20) {
                            // Radio Tuner Art Card
                            VStack(spacing: 14) {
                                ZStack {
                                    RoundedRectangle(cornerRadius: 24)
                                        .fill(
                                            LinearGradient(
                                                colors: [Color(hex: "#1E293B"), Color(hex: "#0F172A")],
                                                startPoint: .topLeading,
                                                endPoint: .bottomTrailing
                                            )
                                        )
                                        .frame(height: 180)
                                        .shadow(color: Color.black.opacity(0.2), radius: 12, x: 0, y: 6)

                                    VStack(spacing: 10) {
                                        HStack {
                                            HStack(spacing: 6) {
                                                Circle()
                                                    .fill(radioService.isPlaying ? Color.red : Color.gray)
                                                    .frame(width: 8, height: 8)
                                                Text(radioService.isPlaying ? "ON AIR • LIVE RADIO" : "OFF AIR")
                                                    .font(.system(size: 10, weight: .black))
                                                    .foregroundColor(radioService.isPlaying ? .red : .gray)
                                                    .tracking(1.5)
                                            }

                                            Spacer()

                                            Text(station.badge)
                                                .font(.system(size: 10, weight: .bold))
                                                .padding(.horizontal, 8)
                                                .padding(.vertical, 4)
                                                .background(Color.white.opacity(0.12))
                                                .foregroundColor(.white)
                                                .cornerRadius(6)
                                        }
                                        .padding(.horizontal, 18)

                                        // Animated Waveform Equalizer
                                        HStack(spacing: 5) {
                                            ForEach(0..<14) { idx in
                                                RoundedRectangle(cornerRadius: 3)
                                                    .fill(
                                                        LinearGradient(
                                                            colors: [Color.accentColor, Color.orange],
                                                            startPoint: .bottom,
                                                            endPoint: .top
                                                        )
                                                    )
                                                    .frame(
                                                        width: 5,
                                                        height: radioService.isPlaying
                                                        ? CGFloat.random(in: 15...55)
                                                        : 8
                                                    )
                                                    .animation(.easeInOut(duration: 0.15), value: radioService.currentTimeSec)
                                            }
                                        }
                                        .frame(height: 55)

                                        Text(radioService.activeChapter?.titleJa ?? station.titleJa)
                                            .font(.system(size: 14, weight: .bold))
                                            .foregroundColor(.white)
                                            .lineLimit(1)
                                            .padding(.horizontal, 18)
                                    }
                                }
                                .padding(.horizontal)

                                // Title & Description
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(station.title)
                                        .font(.system(size: 18, weight: .black, design: .rounded))

                                    Text(radioService.activeChapter?.description ?? station.subtitle)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .padding(.horizontal)
                            }
                            .padding(.top, 6)

                            // Scrub Bar & Timestamps
                            VStack(spacing: 4) {
                                Slider(
                                    value: Binding(
                                        get: { isDraggingSlider ? sliderValue : radioService.currentTimeSec },
                                        set: { newValue in
                                            sliderValue = newValue
                                            isDraggingSlider = true
                                        }
                                    ),
                                    in: 0...max(1.0, radioService.durationSec),
                                    onEditingChanged: { editing in
                                        if !editing {
                                            radioService.seek(to: sliderValue)
                                            isDraggingSlider = false
                                        }
                                    }
                                )
                                .tint(.accentColor)

                                HStack {
                                    Text(formatTime(isDraggingSlider ? sliderValue : radioService.currentTimeSec))
                                    Spacer()
                                    Text(formatTime(radioService.durationSec))
                                }
                                .font(.system(size: 11, weight: .semibold, design: .monospaced))
                                .foregroundColor(.secondary)
                            }
                            .padding(.horizontal)

                            // Playback Control Buttons
                            HStack(spacing: 26) {
                                // Rewind 15s
                                Button(action: { radioService.seek(by: -15) }) {
                                    Image(systemName: "gobackward.15")
                                        .font(.system(size: 24, weight: .semibold))
                                        .foregroundColor(.primary)
                                }

                                // Big Play / Pause Button
                                Button(action: {
                                    if radioService.currentStation?.id != station.id {
                                        radioService.playStation(station)
                                    } else {
                                        radioService.togglePlayPause()
                                    }
                                }) {
                                    ZStack {
                                        Circle()
                                            .fill(Color.accentColor)
                                            .frame(width: 66, height: 66)
                                            .shadow(color: Color.accentColor.opacity(0.3), radius: 8, x: 0, y: 4)

                                        Image(systemName: radioService.isPlaying ? "pause.fill" : "play.fill")
                                            .font(.system(size: 26, weight: .bold))
                                            .foregroundColor(.white)
                                    }
                                }

                                // Forward 15s
                                Button(action: { radioService.seek(by: 15) }) {
                                    Image(systemName: "goforward.15")
                                        .font(.system(size: 24, weight: .semibold))
                                        .foregroundColor(.primary)
                                }
                            }

                            // Utility Bar (Speed & Sleep Timer & Furigana Toggles)
                            HStack(spacing: 10) {
                                // Speed Menu
                                Menu {
                                    Button("0.8x (Relaxed)") { radioService.setSpeed(0.8) }
                                    Button("1.0x (Normal)") { radioService.setSpeed(1.0) }
                                    Button("1.2x (Brisk)") { radioService.setSpeed(1.2) }
                                    Button("1.5x (Speed Drill)") { radioService.setSpeed(1.5) }
                                } label: {
                                    HStack(spacing: 4) {
                                        Image(systemName: "speedometer")
                                        Text("\(String(format: "%.1fx", radioService.playbackRate))")
                                    }
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 7)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(10)
                                }

                                // Sleep Timer Menu
                                Menu {
                                    Button("Off") { radioService.setSleepTimer(minutes: nil) }
                                    Button("15 Minutes") { radioService.setSleepTimer(minutes: 15) }
                                    Button("30 Minutes") { radioService.setSleepTimer(minutes: 30) }
                                    Button("45 Minutes") { radioService.setSleepTimer(minutes: 45) }
                                    Button("60 Minutes") { radioService.setSleepTimer(minutes: 60) }
                                } label: {
                                    HStack(spacing: 4) {
                                        Image(systemName: "moon.stars.fill")
                                        if let rem = radioService.remainingSleepSeconds {
                                            Text("\(rem / 60)m left")
                                                .foregroundColor(.orange)
                                        } else {
                                            Text("Sleep")
                                        }
                                    }
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 7)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(10)
                                }

                                Spacer()

                                Button(action: { showFurigana.toggle() }) {
                                    Text("ふりがな")
                                        .font(.system(size: 10, weight: .bold))
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 6)
                                        .background(showFurigana ? Color.accentColor.opacity(0.25) : Color.gray.opacity(0.15))
                                        .cornerRadius(8)
                                }

                                Button(action: { showRomaji.toggle() }) {
                                    Text("Romaji")
                                        .font(.system(size: 10, weight: .bold))
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 6)
                                        .background(showRomaji ? Color.accentColor.opacity(0.25) : Color.gray.opacity(0.15))
                                        .cornerRadius(8)
                                }
                            }
                            .padding(.horizontal)

                            // Segmented View Mode Picker
                            Picker("View Mode", selection: $selectedViewMode) {
                                Text("🗣 Live Word Shadowing").tag(1)
                                Text("📻 Radio Chapters").tag(0)
                            }
                            .pickerStyle(.segmented)
                            .padding(.horizontal)

                            // Content based on mode
                            if selectedViewMode == 1 {
                                // Live Word-by-Word Shadowing List
                                VStack(alignment: .leading, spacing: 14) {
                                    HStack {
                                        Label("FOLLOW-ALONG SHADOWING", systemImage: "waveform.and.mic")
                                            .font(.system(size: 11, weight: .bold))
                                            .foregroundColor(.accentColor)
                                            .tracking(1.0)
                                        Spacer()
                                        Text("Tap words to hear pronunciation")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                    .padding(.horizontal)

                                    ForEach(station.chapters) { chapter in
                                        if !chapter.transcriptSentences.isEmpty {
                                            VStack(alignment: .leading, spacing: 10) {
                                                // Chapter Header
                                                HStack {
                                                    Text(chapter.titleJa)
                                                        .font(.system(size: 13, weight: .bold))
                                                        .foregroundColor(.accentColor)
                                                    Spacer()
                                                    Text(formatTime(chapter.startTimeSec))
                                                        .font(.system(size: 10, weight: .semibold, design: .monospaced))
                                                        .foregroundColor(.secondary)
                                                }
                                                .padding(.horizontal, 4)

                                                // Sentence cards
                                                ForEach(chapter.transcriptSentences) { sent in
                                                    let isCur = (activeSentence?.id == sent.id)
                                                    let rawDuration = max(0.1, sent.endTimeSec - sent.startTimeSec)
                                                    let effectiveDuration = max(0.1, rawDuration - 0.45)
                                                    let sentElapsed = max(0.0, radioService.currentTimeSec - sent.startTimeSec)
                                                    let sentProgress = isCur ? min(1.0, max(0.0, sentElapsed / effectiveDuration)) : 0.0

                                                    VStack(alignment: .leading, spacing: 8) {
                                                        HStack {
                                                            Text(sent.id.uppercased())
                                                                .font(.system(size: 9, weight: .heavy))
                                                                .foregroundColor(isCur ? .accentColor : .secondary)
                                                                .padding(.horizontal, 6)
                                                                .padding(.vertical, 2)
                                                                .background(isCur ? Color.accentColor.opacity(0.2) : Color.gray.opacity(0.15))
                                                                .cornerRadius(6)

                                                            if isCur {
                                                                Text("PLAYING NOW")
                                                                    .font(.system(size: 9, weight: .black))
                                                                    .foregroundColor(.accentColor)
                                                            }

                                                            Spacer()

                                                            Button(action: {
                                                                radioService.seek(to: sent.startTimeSec)
                                                            }) {
                                                                HStack(spacing: 3) {
                                                                    Image(systemName: "arrow.counterclockwise")
                                                                    Text("Jump")
                                                                }
                                                                .font(.system(size: 10, weight: .bold))
                                                                .foregroundColor(.accentColor)
                                                                .padding(.horizontal, 8)
                                                                .padding(.vertical, 4)
                                                                .background(Color.accentColor.opacity(0.12))
                                                                .cornerRadius(8)
                                                            }
                                                        }

                                                        // Dynamic Word-by-Word Flow with Real-time Karaoke Highlighting
                                                        SegmentedSentenceWordFlowView(
                                                            sentenceText: sent.japanese,
                                                            furiganaText: sent.furigana,
                                                            isActive: isCur,
                                                            sentenceProgress: sentProgress,
                                                            showFurigana: showFurigana,
                                                            showRomaji: showRomaji
                                                        )

                                                        Text(sent.english)
                                                            .font(.system(size: 12, design: .rounded))
                                                            .foregroundColor(.secondary.opacity(0.9))
                                                            .padding(.top, 2)
                                                    }
                                                    .padding(12)
                                                    .background(.ultraThinMaterial)
                                                    .cornerRadius(16)
                                                    .overlay(
                                                        RoundedRectangle(cornerRadius: 16)
                                                            .stroke(isCur ? Color.accentColor : Color.primary.opacity(0.08), lineWidth: isCur ? 2 : 1)
                                                    )
                                                    .id(sent.id)
                                                }
                                            }
                                            .padding(.horizontal)
                                        }
                                    }
                                }
                                .padding(.bottom, 30)
                            } else {
                                // Chapter Bookmarks List
                                VStack(alignment: .leading, spacing: 12) {
                                    Text("BROADCAST CHAPTERS (番組チャプター)")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.secondary)
                                        .tracking(1.0)

                                    VStack(spacing: 10) {
                                        ForEach(station.chapters) { ch in
                                            let isCurrent = (radioService.activeChapter?.id == ch.id)

                                            Button(action: {
                                                radioService.jumpToChapter(ch)
                                            }) {
                                                HStack(spacing: 12) {
                                                    ZStack {
                                                        Circle()
                                                            .fill(isCurrent ? Color.accentColor : Color.gray.opacity(0.15))
                                                            .frame(width: 32, height: 32)
                                                        Image(systemName: isCurrent ? "waveform" : "play.fill")
                                                            .font(.caption2)
                                                            .foregroundColor(isCurrent ? .white : .secondary)
                                                    }

                                                    VStack(alignment: .leading, spacing: 2) {
                                                        Text(ch.titleJa)
                                                            .font(.system(size: 14, weight: isCurrent ? .bold : .medium))
                                                            .foregroundColor(isCurrent ? .accentColor : .primary)
                                                        Text(ch.description)
                                                            .font(.caption2)
                                                            .foregroundColor(.secondary)
                                                            .lineLimit(1)
                                                    }

                                                    Spacer()

                                                    Text(formatTime(ch.startTimeSec))
                                                        .font(.system(size: 11, weight: .semibold, design: .monospaced))
                                                        .foregroundColor(.secondary)
                                                }
                                                .padding(12)
                                                .background(isCurrent ? Color.accentColor.opacity(0.12) : Color.white.opacity(0.06))
                                                .cornerRadius(14)
                                            }
                                            .buttonStyle(PlainButtonStyle())
                                        }
                                    }
                                }
                                .padding(.horizontal)
                                .padding(.bottom, 30)
                            }
                        }
                    }
                    .onChange(of: activeSentence?.id) { activeId in
                        if let activeId = activeId, selectedViewMode == 1 {
                            withAnimation(.easeInOut(duration: 0.35)) {
                                proxy.scrollTo(activeId, anchor: .center)
                            }
                        }
                    }
                }
            }
            .navigationTitle("NHK 1-Hour Radio")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    private func formatTime(_ seconds: Double) -> String {
        let total = Int(seconds)
        let mins = total / 60
        let secs = total % 60
        return String(format: "%02d:%02d", mins, secs)
    }
}
