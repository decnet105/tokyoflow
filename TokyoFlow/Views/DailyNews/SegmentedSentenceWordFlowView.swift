import SwiftUI

public struct SegmentedSentenceWordFlowView: View {
    public let sentenceText: String
    public let furiganaText: String
    public var isActive: Bool = false
    public var showFurigana: Bool = true
    public var showRomaji: Bool = true

    @State private var selectedToken: WordToken? = nil
    @State private var showWordPopup: Bool = false
    @ObservedObject var audioService = AudioService.shared

    private var words: [WordToken] {
        JapaneseWordSegmenter.shared.segment(text: sentenceText, furiganaReference: furiganaText)
    }

    public init(
        sentenceText: String,
        furiganaText: String = "",
        isActive: Bool = false,
        showFurigana: Bool = true,
        showRomaji: Bool = true
    ) {
        self.sentenceText = sentenceText
        self.furiganaText = furiganaText
        self.isActive = isActive
        self.showFurigana = showFurigana
        self.showRomaji = showRomaji
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            // Word Flow Layout
            FlowLayout(spacing: 6) {
                ForEach(words) { token in
                    WordChipView(
                        token: token,
                        isActive: isActive,
                        showFurigana: showFurigana,
                        showRomaji: showRomaji,
                        onTap: {
                            selectedToken = token
                            showWordPopup = true
                            audioService.speak(text: token.text)
                        }
                    )
                }
            }

            // Word Gloss Popup Drawer
            if showWordPopup, let tok = selectedToken {
                HStack(spacing: 8) {
                    Image(systemName: "character.bubble.fill")
                        .foregroundColor(.accentColor)

                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 6) {
                            Text(tok.text)
                                .font(.system(size: 15, weight: .bold))
                            if !tok.furigana.isEmpty {
                                Text("[\(tok.furigana)]")
                                    .font(.caption)
                                    .foregroundColor(.accentColor)
                            }
                            if !tok.romaji.isEmpty {
                                Text("(\(tok.romaji))")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                        }

                        if !tok.meaning.isEmpty {
                            Text(tok.meaning)
                                .font(.caption)
                                .foregroundColor(.primary)
                        }
                    }

                    Spacer()

                    Button(action: {
                        audioService.speak(text: tok.text)
                    }) {
                        Image(systemName: "speaker.wave.2.fill")
                            .font(.caption)
                            .foregroundColor(.white)
                            .padding(6)
                            .background(Color.accentColor)
                            .clipShape(Circle())
                    }

                    Button(action: { showWordPopup = false }) {
                        Image(systemName: "xmark.circle.fill")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                .padding(10)
                .background(Color.accentColor.opacity(0.12))
                .cornerRadius(12)
                .transition(.opacity.combined(with: .scale(scale: 0.95)))
            }
        }
    }
}

// MARK: - Interactive Word Chip
public struct WordChipView: View {
    public let token: WordToken
    public let isActive: Bool
    public let showFurigana: Bool
    public let showRomaji: Bool
    public let onTap: () -> Void

    public var body: some View {
        Button(action: onTap) {
            VStack(spacing: 1) {
                if showFurigana && !token.furigana.isEmpty {
                    Text(token.furigana)
                        .font(.system(size: 10, weight: .regular))
                        .foregroundColor(isActive ? .accentColor.opacity(0.8) : .secondary)
                        .lineLimit(1)
                }

                Text(token.text)
                    .font(.system(size: 16, weight: isActive ? .bold : .semibold, design: .rounded))
                    .foregroundColor(isActive ? .accentColor : .primary)

                if showRomaji && !token.romaji.isEmpty {
                    Text(token.romaji)
                        .font(.system(size: 9, weight: .regular, design: .monospaced))
                        .foregroundColor(.secondary.opacity(0.8))
                        .lineLimit(1)
                }
            }
            .padding(.horizontal, 6)
            .padding(.vertical, 4)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(isActive ? Color.accentColor.opacity(0.15) : Color.primary.opacity(0.04))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(isActive ? Color.accentColor.opacity(0.5) : Color.clear, lineWidth: 1)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - Flow Layout for Wrapped Word Chips
public struct FlowLayout: Layout {
    public var spacing: CGFloat = 6

    public init(spacing: CGFloat = 6) {
        self.spacing = spacing
    }

    public func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let width = proposal.width ?? 0
        var currentX: CGFloat = 0
        var currentY: CGFloat = 0
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if currentX + size.width > width && currentX > 0 {
                currentX = 0
                currentY += rowHeight + spacing
                rowHeight = 0
            }
            currentX += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }

        return CGSize(width: width, height: currentY + rowHeight)
    }

    public func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var currentX = bounds.minX
        var currentY = bounds.minY
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if currentX + size.width > bounds.maxX && currentX > bounds.minX {
                currentX = bounds.minX
                currentY += rowHeight + spacing
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: currentX, y: currentY), proposal: .unspecified)
            currentX += size.width + spacing
            rowHeight = max(rowHeight, size.height)
        }
    }
}
