import SwiftUI

/// TokyoDuoAdaptiveLayout provides a seamless two-pane responsive experience
/// optimized for iPhone Duo, foldable displays, iPad Split View, and landscape mode.
public struct TokyoDuoAdaptiveLayout<PrimaryContent: View, SecondaryContent: View>: View {
    public let primaryContent: PrimaryContent
    public let secondaryContent: SecondaryContent
    public var duoSplitRatio: CGFloat = 0.5 // Default 50/50 split
    public var minimumDuoWidth: CGFloat = 680

    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    public init(
        duoSplitRatio: CGFloat = 0.5,
        minimumDuoWidth: CGFloat = 680,
        @ViewBuilder primaryContent: () -> PrimaryContent,
        @ViewBuilder secondaryContent: () -> SecondaryContent
    ) {
        self.duoSplitRatio = duoSplitRatio
        self.minimumDuoWidth = minimumDuoWidth
        self.primaryContent = primaryContent()
        self.secondaryContent = secondaryContent()
    }

    public var body: some View {
        GeometryReader { geo in
            let isDuoMode = geo.size.width >= minimumDuoWidth || horizontalSizeClass == .regular

            if isDuoMode {
                // 📱📱 Duo Dual-Pane Mode: Side-by-Side Dual Screens with Hinge Divider
                HStack(spacing: 0) {
                    // Left Screen: Immersion & Video/Audio/Map Primary Pane
                    primaryContent
                        .frame(width: geo.size.width * duoSplitRatio)

                    // Duo Central Folding Hinge / Subtle Separation Line
                    Rectangle()
                        .fill(
                            LinearGradient(
                                colors: [
                                    Color.black.opacity(0.15),
                                    Color.accentColor.opacity(0.25),
                                    Color.black.opacity(0.15)
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                        .frame(width: 2)
                        .shadow(color: Color.black.opacity(0.2), radius: 2, x: 0, y: 0)

                    // Right Screen: Interactive Action Lab / Shadowing / Dojo Secondary Pane
                    secondaryContent
                        .frame(width: geo.size.width * (1.0 - duoSplitRatio) - 2)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                // 📱 Single Screen Mode: Vertical Fluid Layout
                ScrollView {
                    VStack(spacing: 16) {
                        primaryContent
                        secondaryContent
                    }
                }
            }
        }
    }
}
