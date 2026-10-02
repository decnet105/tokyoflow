import SwiftUI

public enum WordChipState: Equatable {
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
    public var showRomaji: Bool = false
    public var onSelectWordToShadow: ((WordToken) -> Void)? = nil

    @State private var words: [WordToken] = []
    @State private var selectedToken: WordToken? = nil
    @State private var showWordPopup: Bool = false
    @ObservedObject var audioService = AudioService.shared
    @ObservedObject var weakTracker = WeakWordTrackerService.shared

    public init(
        sentenceText: String,
        furiganaText: String = "",
        isActive: Bool = false,
        sentenceProgress: Double = 0.0,
        manualActiveWordIndex: Int? = nil,
        showFurigana: Bool = true,
        showRomaji: Bool = false,
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

    private var activeWordIndex: Int? {
        if let manual = manualActiveWordIndex { return manual }
        guard isActiveSentence && sentenceProgress > 0.0 && !words.isEmpty else { return nil }

        let totalWeight = words.reduce(0.0) { $0 + $1.moraWeight }
        guard totalWeight > 0 else { return 0 }

        var cumulative = 0.0
        let target = totalWeight * min(0.999, max(0.0, sentenceProgress))
        for (idx, w) in words.enumerated() {
            cumulative += w.moraWeight
            if cumulative >= target {
                return idx
            }
        }
        return max(0, words.count - 1)
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            // Elegant NHK Easy Japanese Flow Layout (Natural Text with Ruby Furigana)
            FlowLayout(spacing: 3) {
                ForEach(words) { token in
                    let isWordActive = (activeWordIndex == token.index)
                    let isWordPast = (activeWordIndex != nil && token.index < (activeWordIndex ?? 0))

                    NHKWordTokenView(
                        token: token,
                        isActive: isWordActive,
                        isPast: isWordPast,
                        showFurigana: showFurigana,
                        showRomaji: showRomaji,
                        onTap: {
                            selectedToken = token
                            showWordPopup = true
                            audioService.speak(text: token.text)
                            weakTracker.recordListen(word: token.text, reading: token.furigana, meaning: token.meaning)
                        }
                    )
                }
            }

            // Inline Word Dictionary Tooltip
            if showWordPopup, let tok = selectedToken {
                HStack(spacing: 10) {
                    Image(systemName: "character.bubble.fill")
                        .font(.body)
                        .foregroundColor(.accentColor)

                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 6) {
                            Text(tok.text)
                                .font(.system(size: 15, weight: .bold))
                            if !tok.furigana.isEmpty {
                                Text("[\(tok.furigana)]")
                                    .font(.system(size: 12, weight: .semibold))
                                    .foregroundColor(.accentColor)
                            }
                            if !tok.romaji.isEmpty {
                                Text("(\(tok.romaji))")
                                    .font(.system(size: 10, design: .monospaced))
                                    .foregroundColor(.secondary)
                            }
                        }

                        if !tok.meaning.isEmpty {
                            Text(tok.meaning)
                                .font(.system(size: 11))
                                .foregroundColor(.primary)
                        }
                    }

                    Spacer()

                    Button(action: {
                        audioService.speak(text: tok.text)
                    }) {
                        Image(systemName: "speaker.wave.2.fill")
                            .font(.caption2)
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
                .padding(8)
                .background(Color(UIColor.secondarySystemBackground).opacity(0.85))
                .cornerRadius(10)
                .transition(.opacity)
            }
        }
        .onAppear {
            if words.isEmpty {
                words = JapaneseWordSegmenter.shared.segment(text: sentenceText, furiganaReference: furiganaText)
            }
        }
    }
}

// MARK: - NHK Standard Ruby Text Word View (Stable Geometry, Zero Flashing)
public struct NHKWordTokenView: View {
    public let token: WordToken
    public let isActive: Bool
    public let isPast: Bool
    public let showFurigana: Bool
    public let showRomaji: Bool
    public let onTap: () -> Void

    public var body: some View {
        Button(action: onTap) {
            VStack(spacing: 0) {
                // Ruby Furigana Floating Above Kanji
                if showFurigana && !token.furigana.isEmpty {
                    Text(token.furigana)
                        .font(.system(size: 10, weight: isActive ? .bold : .regular))
                        .foregroundColor(isActive ? .orange : (isPast ? Color.accentColor.opacity(0.8) : .secondary))
                        .lineLimit(1)
                        .frame(height: 12)
                } else if showFurigana {
                    // Transparent spacer for uniform baseline alignment
                    Text(" ")
                        .font(.system(size: 10))
                        .frame(height: 12)
                }

                // Main Kanji / Kana Text
                Text(token.text)
                    .font(.system(size: 16, weight: isActive ? .black : (isPast ? .semibold : .medium), design: .default))
                    .foregroundColor(
                        isActive
                            ? .orange
                            : (isPast ? Color.accentColor : .primary)
                    )
                    .padding(.horizontal, 2)
                    .background(
                        isActive
                            ? Color.orange.opacity(0.18)
                            : (isPast ? Color.accentColor.opacity(0.08) : Color.clear)
                    )
                    .cornerRadius(4)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - Flow Layout for Wrapped Word Chips
public struct FlowLayout: Layout {
    public var spacing: CGFloat = 3

    public init(spacing: CGFloat = 3) {
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
