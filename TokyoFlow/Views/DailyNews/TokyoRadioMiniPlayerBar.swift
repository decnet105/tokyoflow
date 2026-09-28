import SwiftUI

public struct TokyoRadioMiniPlayerBar: View {
    @ObservedObject var radioService = TokyoRadioService.shared
    @State private var showFullPlayer = false

    public init() {}

    public var body: some View {
        if let station = radioService.currentStation {
            Button(action: { showFullPlayer = true }) {
                HStack(spacing: 12) {
                    ZStack {
                        Circle()
                            .fill(Color.accentColor)
                            .frame(width: 40, height: 40)
                        Image(systemName: radioService.isPlaying ? "waveform" : "antenna.radiowaves.left.and.right")
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.white)
                    }

                    VStack(alignment: .leading, spacing: 2) {
                        Text(radioService.activeChapter?.titleJa ?? station.titleJa)
                            .font(.system(size: 13, weight: .bold))
                            .foregroundColor(.primary)
                            .lineLimit(1)

                        Text("NHK Radio Immersion • \(station.durationLabel)")
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    // Play/Pause Button
                    Button(action: {
                        radioService.togglePlayPause()
                    }) {
                        Image(systemName: radioService.isPlaying ? "pause.circle.fill" : "play.circle.fill")
                            .font(.system(size: 32))
                            .foregroundColor(.accentColor)
                    }
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 8)
                .background(.ultraThinMaterial)
                .cornerRadius(18)
                .shadow(color: Color.black.opacity(0.12), radius: 8, x: 0, y: 3)
                .padding(.horizontal)
                .padding(.bottom, 4)
            }
            .buttonStyle(PlainButtonStyle())
            .sheet(isPresented: $showFullPlayer) {
                TokyoRadioPlayerModalView(station: station)
            }
        }
    }
}
