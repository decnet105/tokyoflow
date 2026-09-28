import SwiftUI

public struct TokyoRadioPlayerModalView: View {
    public let station: TokyoRadioStation

    @ObservedObject var radioService = TokyoRadioService.shared
    @Environment(\.dismiss) private var dismiss
    @State private var isDraggingSlider = false
    @State private var sliderValue: Double = 0.0
    @State private var showSleepTimerMenu = false

    public init(station: TokyoRadioStation) {
        self.station = station
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 24) {
                        // Radio Tuner Art Card
                        VStack(spacing: 16) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 24)
                                    .fill(
                                        LinearGradient(
                                            colors: [Color(hex: "#1E293B"), Color(hex: "#0F172A")],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(height: 200)
                                    .shadow(color: Color.black.opacity(0.2), radius: 12, x: 0, y: 6)

                                VStack(spacing: 12) {
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
                                    .padding(.horizontal, 20)

                                    // Animated Waveform Equilizer
                                    HStack(spacing: 6) {
                                        ForEach(0..<12) { idx in
                                            RoundedRectangle(cornerRadius: 3)
                                                .fill(
                                                    LinearGradient(
                                                        colors: [Color.accentColor, Color.pink],
                                                        startPoint: .bottom,
                                                        endPoint: .top
                                                    )
                                                )
                                                .frame(
                                                    width: 6,
                                                    height: radioService.isPlaying
                                                    ? CGFloat.random(in: 18...65)
                                                    : 10
                                                )
                                                .animation(.easeInOut(duration: 0.12), value: radioService.currentTimeSec)
                                        }
                                    }
                                    .frame(height: 70)

                                    Text(radioService.activeChapter?.titleJa ?? station.titleJa)
                                        .font(.system(size: 15, weight: .bold))
                                        .foregroundColor(.white)
                                        .lineLimit(1)
                                        .padding(.horizontal, 20)
                                }
                            }
                            .padding(.horizontal)

                            // Title & Description
                            VStack(alignment: .leading, spacing: 6) {
                                Text(station.title)
                                    .font(.system(size: 20, weight: .black, design: .rounded))

                                Text(radioService.activeChapter?.description ?? station.subtitle)
                                    .font(.footnote)
                                    .foregroundColor(.secondary)
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal)
                        }
                        .padding(.top, 8)

                        // Scrub Bar & Timestamps
                        VStack(spacing: 6) {
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
                        HStack(spacing: 28) {
                            // Rewind 15s
                            Button(action: { radioService.seek(by: -15) }) {
                                Image(systemName: "gobackward.15")
                                    .font(.system(size: 26, weight: .semibold))
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
                                        .frame(width: 72, height: 72)
                                        .shadow(color: Color.accentColor.opacity(0.3), radius: 10, x: 0, y: 5)

                                    Image(systemName: radioService.isPlaying ? "pause.fill" : "play.fill")
                                        .font(.system(size: 28, weight: .bold))
                                        .foregroundColor(.white)
                                }
                            }

                            // Forward 15s
                            Button(action: { radioService.seek(by: 15) }) {
                                Image(systemName: "goforward.15")
                                    .font(.system(size: 26, weight: .semibold))
                                    .foregroundColor(.primary)
                            }
                        }

                        // Utility Bar (Speed & Sleep Timer)
                        HStack(spacing: 16) {
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
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(.ultraThinMaterial)
                                .cornerRadius(12)
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
                                        Text("Sleep Timer")
                                    }
                                }
                                .font(.caption)
                                .fontWeight(.bold)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(.ultraThinMaterial)
                                .cornerRadius(12)
                            }
                        }

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
