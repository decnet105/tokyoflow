import SwiftUI

public enum WordChipState {
    case upcoming
    case active
    case past
}

public struct SegmentedSentenceWordFlowView: View {
    public let sentenceText: String
    public let furiganaText: String
    public var isActiveSentence: Bool = false
    public var sentenceProgress: Double = 0.0 // 0.0 to 1.0 (relative to sentence duration)
    public var manualActiveWordIndex: Int? = nil
    public var showFurigana: Bool = true
    public var showRomaji: Bool = true
    public var onSelectWordToShadow: ((WordToken) -> Void)? = nil

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
        sentenceProgress: Double = 0.0,
        manualActiveWordIndex: Int? = nil,
        showFurigana: Bool = true,
        showRomaji: Bool = true,
        onSelectWordToShadow: ((WordToken) -> Void)? = nil
    ) {
        self.sentenceText = sentenceText
        self.furiganaText = furiganaText
        self.isActiveSentence = isActive
        self.sentenceProgress = sentenceProgress
        self.manualActiveWordIndex = manualActiveWordIndex
        self.showFurigana = showFurigana
        self.showRomaji = showRomaji
        self.onSelectWordToShadow = onSelectWordToShadow
    }

    private var computedActiveWordIndex: Int? {
        if let manual = manualActiveWordIndex { return manual }
        guard isActiveSentence && sentenceProgress > 0.0 else { return nil }

        let totalWeight = words.reduce(0) { $0 + $1.moraWeight }
        guard totalWeight > 0 else { return 0 }

        var cumulative = 0
        let target = Double(totalWeight) * min(0.999, max(0.0, sentenceProgress))
        for (idx, w) in words.enumerated() {
            cumulative += w.moraWeight
            if Double(cumulative) >= target {
                return idx
            }
        }
        return max(0, words.count - 1)
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Dynamic Word-by-Word Flow Layout
            FlowLayout(spacing: 6) {
                ForEach(words) { token in
                    let state: WordChipState = {
                        guard let activeIdx = computedActiveWordIndex else {
                            return .upcoming
                        }
                        if token.index == activeIdx {
                            return .active
                        } else if token.index < activeIdx {
                            return .past
                        } else {
                            return .upcoming
                        }
                    }()

                    WordChipView(
                        token: token,
                        state: state,
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
                HStack(spacing: 10) {
                    Image(systemName: "character.bubble.fill")
                        .font(.title3)
                        .foregroundColor(.accentColor)

                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 6) {
                            Text(tok.text)
                                .font(.system(size: 16, weight: .black, design: .rounded))
                            if !tok.furigana.isEmpty {
                                Text("[\(tok.furigana)]")
                                    .font(.system(size: 13, weight: .bold))
                                    .foregroundColor(.accentColor)
                            }
                            if !tok.romaji.isEmpty {
                                Text("(\(tok.romaji))")
                                    .font(.system(size: 11, design: .monospaced))
                                    .foregroundColor(.secondary)
                            }
                        }

                        if !tok.meaning.isEmpty {
                            Text(tok.meaning)
                                .font(.system(size: 12))
                                .foregroundColor(.primary)
                        }
                    }

                    Spacer()

                    // Play Word Native Pronunciation
                    Button(action: {
                        audioService.speak(text: tok.text)
                    }) {
                        HStack(spacing: 4) {
                            Image(systemName: "speaker.wave.2.fill")
                            Text("发音")
                        }
                        .font(.system(size: 11, weight: .bold))
                        .foregroundColor(.white)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color.accentColor)
                        .cornerRadius(10)
                    }

                    // Dismiss Button
                    Button(action: { showWordPopup = false }) {
                        Image(systemName: "xmark.circle.fill")
                            .font(.title3)
                            .foregroundColor(.secondary)
                    }
                }
                .padding(12)
                .background(.ultraThinMaterial)
                .cornerRadius(14)
                .overlay(
                    RoundedRectangle(cornerRadius: 14)
                        .stroke(Color.accentColor.opacity(0.3), lineWidth: 1)
                )
                .transition(.opacity.combined(with: .scale(scale: 0.95)))
            }
        }
        .animation(.spring(response: 0.28, dampingFraction: 0.72), value: computedActiveWordIndex)
    }
}

// MARK: - Interactive Word Chip with Karaoke States
public struct WordChipView: View {
    public let token: WordToken
    public let state: WordChipState
    public let showFurigana: Bool
    public let showRomaji: Bool
    public let onTap: () -> Void

    public var body: some View {
        Button(action: onTap) {
            VStack(spacing: 1) {
                // Ruby Furigana
                if showFurigana && !token.furigana.isEmpty {
                    Text(token.furigana)
                        .font(.system(size: 10, weight: state == .active ? .bold : .regular))
                        .foregroundColor(
                            state == .active
                                ? .white.opacity(0.95)
                                : (state == .past ? Color.accentColor.opacity(0.8) : .secondary)
                        )
                        .lineLimit(1)
                }

                // Main Kanji / Kana Text
                Text(token.text)
                    .font(.system(size: 16, weight: state == .active ? .black : (state == .past ? .bold : .semibold), design: .rounded))
                    .foregroundColor(
                        state == .active
                            ? .white
                            : (state == .past ? Color.accentColor : .primary)
                    )

                // Romaji Subtitle
                if showRomaji && !token.romaji.isEmpty {
                    Text(token.romaji)
                        .font(.system(size: 9, weight: .regular, design: .monospaced))
                        .foregroundColor(
                            state == .active
                                ? .white.opacity(0.85)
                                : (state == .past ? Color.accentColor.opacity(0.7) : .secondary.opacity(0.8))
                        )
                        .lineLimit(1)
                }
            }
            .padding(.horizontal, 7)
            .padding(.vertical, 5)
            .background(
                Group {
                    switch state {
                    case .active:
                        LinearGradient(
                            colors: [Color.accentColor, Color.orange.opacity(0.9)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    case .past:
                        Color.accentColor.opacity(0.16)
                    case .upcoming:
                        Color.primary.opacity(0.05)
                    }
                }
            )
            .cornerRadius(10)
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(
                        state == .active
                            ? Color.white.opacity(0.6)
                            : (state == .past ? Color.accentColor.opacity(0.4) : Color.clear),
                        lineWidth: state == .active ? 1.5 : 1
                    )
            )
            .scaleEffect(state == .active ? 1.08 : 1.0)
            .shadow(
                color: state == .active ? Color.accentColor.opacity(0.4) : Color.clear,
                radius: 5,
                y: 2
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
