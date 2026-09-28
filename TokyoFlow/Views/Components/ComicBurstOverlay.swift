import SwiftUI

public struct ComicBurstOverlay: View {
    public let sfxText: String
    public let meaning: String
    @Binding public var isPresented: Bool

    @State private var scale: CGFloat = 0.2
    @State private var rotation: Double = -15
    @State private var opacity: Double = 0.0

    public var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()
                .onTapGesture { dismissBurst() }

            // Dynamic Action Burst Lines
            ZStack {
                // Action star burst
                Circle()
                    .fill(
                        RadialGradient(
                            colors: [Color.yellow.opacity(0.9), Color.orange, Color.red],
                            center: .center,
                            startRadius: 20,
                            endRadius: 180
                        )
                    )
                    .frame(width: 320, height: 320)
                    .clipShape(ActionStarShape(points: 16))

                VStack(spacing: 8) {
                    Text(sfxText)
                        .font(.system(size: 64, weight: .black, design: .serif))
                        .foregroundColor(.white)
                        .shadow(color: .black, radius: 4, x: 2, y: 3)

                    Text(meaning)
                        .font(.headline)
                        .fontWeight(.heavy)
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 6)
                        .background(Color.black.opacity(0.8))
                        .cornerRadius(12)
                }
            }
            .scaleEffect(scale)
            .rotationEffect(.degrees(rotation))
            .opacity(opacity)
        }
        .onAppear {
            withAnimation(.spring(response: 0.35, dampingFraction: 0.6)) {
                scale = 1.0
                rotation = 0
                opacity = 1.0
            }
            #if os(iOS)
            let generator = UIImpactFeedbackGenerator(style: .heavy)
            generator.impactOccurred()
            #endif

            // Auto dismiss after 1.8s
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.8) {
                dismissBurst()
            }
        }
    }

    private func dismissBurst() {
        withAnimation(.easeOut(duration: 0.2)) {
            scale = 1.2
            opacity = 0
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
            isPresented = false
        }
    }
}

// Procedural Comic Action Star shape
private struct ActionStarShape: Shape {
    let points: Int

    func path(in rect: CGRect) -> Path {
        var path = Path()
        let center = CGPoint(x: rect.midX, y: rect.midY)
        let maxRadius = min(rect.width, rect.height) / 2
        let minRadius = maxRadius * 0.55
        let totalPoints = points * 2

        for i in 0..<totalPoints {
            let angle = (Double(i) * Double.pi) / Double(points) - Double.pi / 2
            let radius = i % 2 == 0 ? maxRadius : minRadius
            let x = center.x + CGFloat(cos(angle)) * radius
            let y = center.y + CGFloat(sin(angle)) * radius

            if i == 0 {
                path.move(to: CGPoint(x: x, y: y))
            } else {
                path.addLine(to: CGPoint(x: x, y: y))
            }
        }
        path.closeSubpath()
        return path
    }
}
