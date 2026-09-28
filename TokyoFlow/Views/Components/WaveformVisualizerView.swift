import SwiftUI

public struct WaveformVisualizerView: View {
    @ObservedObject var audioService = AudioService.shared
    public let height: CGFloat
    public let color: Color

    public init(height: CGFloat = 20, color: Color = .accentColor) {
        self.height = height
        self.color = color
    }

    public var body: some View {
        HStack(spacing: 3) {
            ForEach(0..<audioService.audioPowerLevels.count, id: \.self) { index in
                RoundedRectangle(cornerRadius: 2)
                    .fill(color)
                    .frame(
                        width: 3,
                        height: audioService.isSpeaking
                            ? max(4, height * audioService.audioPowerLevels[index])
                            : 4
                    )
                    .animation(.easeInOut(duration: 0.12), value: audioService.audioPowerLevels[index])
            }
        }
        .frame(height: height)
    }
}
