import SwiftUI

/// TokyoDuoAdaptiveLayout provides a seamless two-pane responsive experience
/// optimized for iPhone Duo, foldable displays, iPad Split View, and landscape mode.
public struct TokyoDuoAdaptiveLayout<PrimaryContent: View, SecondaryContent: View, SingleContent: View>: View {
    public let primaryContent: PrimaryContent
    public let secondaryContent: SecondaryContent
    public let singleContent: SingleContent?
    public var duoSplitRatio: CGFloat = 0.5 // Default 50/50 split
    public var minimumDuoWidth: CGFloat = 680

    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    public init(
        duoSplitRatio: CGFloat = 0.5,
        minimumDuoWidth: CGFloat = 680,
        @ViewBuilder primaryContent: () -> PrimaryContent,
        @ViewBuilder secondaryContent: () -> SecondaryContent
    ) where SingleContent == PrimaryContent {
        self.duoSplitRatio = duoSplitRatio
        self.minimumDuoWidth = minimumDuoWidth
        self.primaryContent = primaryContent()
        self.secondaryContent = secondaryContent()
        self.singleContent = nil
    }

    public init(
        duoSplitRatio: CGFloat = 0.5,
        minimumDuoWidth: CGFloat = 680,
        @ViewBuilder primaryContent: () -> PrimaryContent,
        @ViewBuilder secondaryContent: () -> SecondaryContent,
        @ViewBuilder singleContent: () -> SingleContent
    ) {
        self.duoSplitRatio = duoSplitRatio
        self.minimumDuoWidth = minimumDuoWidth
        self.primaryContent = primaryContent()
        self.secondaryContent = secondaryContent()
        self.singleContent = singleContent()
    }

    public var body: some View {
        GeometryReader { geo in
            let isDuoMode = geo.size.width >= minimumDuoWidth || horizontalSizeClass == .regular

            if isDuoMode {
                //  Duo Dual-Pane Mode: Side-by-Side Dual Screens with Hinge Divider
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
                //  Single Screen Mode: Zero overhead direct view
                if let single = singleContent {
                    single
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    primaryContent
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
            }
        }
    }
}

/// A lazy wrapper that defers the creation of its child view until it is actually rendered.
/// This prevents SwiftUI's `NavigationLink(destination:)` from eagerly instantiating heavy destination views upfront,
/// ensuring instant tab switching and 120fps navigation responsiveness.
public struct LazyView<Content: View>: View {
    private let build: () -> Content

    public init(_ build: @autoclosure @escaping () -> Content) {
        self.build = build
    }

    public var body: Content {
        build()
    }
}
