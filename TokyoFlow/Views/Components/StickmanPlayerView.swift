import SwiftUI

public struct StickmanFrame: Identifiable {
    public let id: Int
    public let title: String
    public let sceneType: String // hook, rule, mistake, shortcut, resolution, badge
    public let characterPose: String // confused, sweating, ninja_pose, confident, bowing, holding_bento
    public let dialogueBubble: String
    public let narrationJapanese: String
    public let narrationEnglish: String
    public let visualCue: String
    public let accentColor: Color
}

public struct StickmanPlayerView: View {
    public let scenarioTitle: String
    public let frames: [StickmanFrame]
    @State private var currentFrameIndex = 0
    @State private var isPlaying = false
    @State private var timer: Timer?
    @ObservedObject var audioService = AudioService.shared

    public init(scenarioTitle: String, frames: [StickmanFrame]) {
        self.scenarioTitle = scenarioTitle
        self.frames = frames
    }

    public var body: some View {
        VStack(spacing: 16) {
            // Player Top Header
            HStack {
                Label("60s Stickman Explainer", systemImage: "figure.walk.motion")
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.accentColor)
                Spacer()
                Text("Scene \(currentFrameIndex + 1) / \(frames.count)")
                    .font(.caption2)
                    .fontWeight(.bold)
                    .foregroundColor(.secondary)
            }

            let frame = frames[min(currentFrameIndex, frames.count - 1)]

            // Minimalist 2D Animation Stage Canvas
            ZStack {
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color.white)
                    .shadow(color: Color.black.opacity(0.08), radius: 10, x: 0, y: 3)
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.primary.opacity(0.1), lineWidth: 1.5)
                    )

                VStack(spacing: 12) {
                    // Scene Title & Type Pill
                    HStack {
                        Text("SCENE \(frame.id): \(frame.title)")
                            .font(.caption)
                            .fontWeight(.black)
                            .foregroundColor(frame.accentColor)

                        Spacer()

                        Text(frame.sceneType.uppercased())
                            .font(.system(size: 9, weight: .heavy))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(frame.accentColor.opacity(0.12))
                            .foregroundColor(frame.accentColor)
                            .cornerRadius(4)
                    }
                    .padding(.horizontal, 16)
                    .padding(.top, 12)

                    Spacer()

                    // Minimalist 2D Stickman Character Illustration
                    StickmanCanvas(pose: frame.characterPose, accentColor: frame.accentColor)
                        .frame(height: 140)

                    // In-Scene Speech Bubble
                    Text(frame.dialogueBubble)
                        .font(.system(size: 14, weight: .bold, design: .rounded))
                        .multilineTextAlignment(.center)
                        .foregroundColor(.black)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 8)
                        .background(Color.yellow.opacity(0.25))
                        .cornerRadius(10)
                        .padding(.horizontal, 20)

                    Spacer()

                    // Visual Cue Footer
                    Text(frame.visualCue)
                        .font(.system(size: 11))
                        .foregroundColor(.gray)
                        .italic()
                        .padding(.bottom, 10)
                }
            }
            .frame(height: 280)

            // Audio & Narration Subtitles
            VStack(alignment: .leading, spacing: 4) {
                HStack {
                    Text(frame.narrationJapanese)
                        .font(.subheadline)
                        .fontWeight(.semibold)
                        .foregroundColor(.primary)
                    Spacer()
                    AudioButton(textToSpeak: frame.narrationJapanese, rate: 0.52)
                }

                Text(frame.narrationEnglish)
                    .font(.footnote)
                    .foregroundColor(.secondary)
            }
            .padding(12)
            .background(Color(.secondarySystemGroupedBackground))
            .cornerRadius(12)

            // Playback Navigation Controls & Scrubber
            HStack(spacing: 16) {
                Button(action: previousFrame) {
                    Image(systemName: "backward.fill")
                        .font(.headline)
                        .foregroundColor(currentFrameIndex > 0 ? .primary : .secondary.opacity(0.4))
                }
                .disabled(currentFrameIndex == 0)

                Button(action: togglePlayPause) {
                    Image(systemName: isPlaying ? "pause.circle.fill" : "play.circle.fill")
                        .font(.system(size: 40))
                        .foregroundColor(.accentColor)
                }

                Button(action: nextFrame) {
                    Image(systemName: "forward.fill")
                        .font(.headline)
                        .foregroundColor(currentFrameIndex < frames.count - 1 ? .primary : .secondary.opacity(0.4))
                }
                .disabled(currentFrameIndex >= frames.count - 1)

                Spacer()

                // Frame Progress Dots
                HStack(spacing: 6) {
                    ForEach(0..<frames.count, id: \.self) { idx in
                        Circle()
                            .fill(idx == currentFrameIndex ? Color.accentColor : Color.secondary.opacity(0.3))
                            .frame(width: 8, height: 8)
                            .onTapGesture {
                                currentFrameIndex = idx
                            }
                    }
                }
            }
            .padding(.horizontal, 4)
        }
        .padding()
        .background(Color(.systemGroupedBackground))
        .cornerRadius(20)
    }

    private func togglePlayPause() {
        isPlaying.toggle()
        if isPlaying {
            startAutoPlay()
        } else {
            timer?.invalidate()
        }
    }

    private func startAutoPlay() {
        timer?.invalidate()
        // Speak current narration
        let frame = frames[currentFrameIndex]
        audioService.speak(text: frame.narrationJapanese, rate: 0.52)

        timer = Timer.scheduledTimer(withTimeInterval: 6.0, repeats: true) { _ in
            if currentFrameIndex < frames.count - 1 {
                currentFrameIndex += 1
                let next = frames[currentFrameIndex]
                audioService.speak(text: next.narrationJapanese, rate: 0.52)
            } else {
                isPlaying = false
                timer?.invalidate()
            }
        }
    }

    private func nextFrame() {
        if currentFrameIndex < frames.count - 1 {
            currentFrameIndex += 1
            let f = frames[currentFrameIndex]
            audioService.speak(text: f.narrationJapanese, rate: 0.52)
        }
    }

    private func previousFrame() {
        if currentFrameIndex > 0 {
            currentFrameIndex -= 1
            let f = frames[currentFrameIndex]
            audioService.speak(text: f.narrationJapanese, rate: 0.52)
        }
    }
}

// Procedural 2D Stickman Drawing View
private struct StickmanCanvas: View {
    let pose: String
    let accentColor: Color

    var body: some View {
        Canvas { context, size in
            let midX = size.width / 2
            let headCenter = CGPoint(x: midX, y: 35)
            let headRadius: CGFloat = 16

            // Head (Hollow circle)
            var headPath = Path()
            headPath.addArc(center: headCenter, radius: headRadius, startAngle: .zero, endAngle: .degrees(360), clockwise: false)
            context.stroke(headPath, with: .color(.black), lineWidth: 3.5)

            // Torso (Spine)
            var spinePath = Path()
            spinePath.move(to: CGPoint(x: midX, y: headCenter.y + headRadius))
            spinePath.addLine(to: CGPoint(x: midX, y: 95))
            context.stroke(spinePath, with: .color(.black), lineWidth: 3.5)

            // Arms & Legs based on pose
            var limbsPath = Path()
            let shoulderY: CGFloat = 58
            let hipY: CGFloat = 95

            switch pose {
            case "ninja_pose", "confident":
                // Arms in dynamic pose
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX - 35, y: shoulderY - 15))
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX + 35, y: shoulderY - 25))

                // Legs wide stance
                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX - 25, y: 135))
                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX + 25, y: 135))

            case "bowing":
                // Bowing forward
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX - 15, y: shoulderY + 25))
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX + 15, y: shoulderY + 25))

                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX - 10, y: 135))
                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX + 10, y: 135))

            case "sweating", "confused":
                // Arms scratching head
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX - 25, y: shoulderY - 15))
                limbsPath.addLine(to: CGPoint(x: midX - 15, y: 35))

                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX + 25, y: shoulderY + 20))

                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX - 15, y: 135))
                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX + 15, y: 135))

            default:
                // Normal standing
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX - 25, y: shoulderY + 25))
                limbsPath.move(to: CGPoint(x: midX, y: shoulderY))
                limbsPath.addLine(to: CGPoint(x: midX + 25, y: shoulderY + 25))

                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX - 18, y: 135))
                limbsPath.move(to: CGPoint(x: midX, y: hipY))
                limbsPath.addLine(to: CGPoint(x: midX + 18, y: 135))
            }

            context.stroke(limbsPath, with: .color(.black), lineWidth: 3.5)
        }
    }
}
