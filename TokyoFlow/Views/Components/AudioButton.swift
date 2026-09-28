import SwiftUI

public struct AudioButton: View {
    public let textToSpeak: String
    public let rate: Float
    @ObservedObject private var audioService = AudioService.shared

    public init(textToSpeak: String, rate: Float = 0.50) {
        self.textToSpeak = textToSpeak
        self.rate = rate
    }

    private var isCurrentlyPlaying: Bool {
        audioService.isSpeaking && audioService.currentSpeakingText == textToSpeak
    }

    public var body: some View {
        Button(action: {
            #if os(iOS)
            let generator = UIImpactFeedbackGenerator(style: .light)
            generator.impactOccurred()
            #endif
            if isCurrentlyPlaying {
                audioService.stop()
            } else {
                audioService.speak(text: textToSpeak, rate: rate)
            }
        }) {
            ZStack {
                Circle()
                    .fill(isCurrentlyPlaying ? Color.accentColor : Color.accentColor.opacity(0.12))
                    .frame(width: 36, height: 36)

                Image(systemName: isCurrentlyPlaying ? "waveform" : "speaker.wave.2.fill")
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(isCurrentlyPlaying ? .white : .accentColor)
            }
        }
        .buttonStyle(.plain)
    }
}
