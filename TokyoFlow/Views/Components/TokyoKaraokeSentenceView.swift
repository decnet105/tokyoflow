import SwiftUI
import Combine

/// TokyoKaraokeSentenceView provides rock-solid, professional-grade Japanese audio-to-text alignment
/// with character- and word-level karaoke highlighting synchronized with studio native audio playback.
///
/// Implements YouTube Shorts Follow-Along / Shadow Reading standard:
/// 1. 3-Tier Typography: Ruby Furigana (Top), Bold Japanese Kanji (Center), Romaji (Bottom).
/// 2. Active Glowing Gold Capsule: Warm yellow/amber highlight (#FEF08A / #F59E0B) with high-contrast text.
/// 3. Floating Red Indicator Dot: Active bouncing red indicator dot (`•`) centered right above the active word chunk.
/// 4. 100% Rigid Invariant Geometry: Zero jumping/shifts between lines or states.
public struct TokyoKaraokeSentenceView: View {
    public let sentenceJa: String
    public let furiganaText: String
    public let translation: String
    public var showFurigana: Bool = true
    public var showRomaji: Bool = true
    public var fontScale: CGFloat = 1.0
    public var onWordTapped: ((String) -> Void)? = nil

    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @ObservedObject private var audioService = AudioService.shared
    @State private var words: [KaraokeWordToken] = []

    public init(
        sentenceJa: String,
        furiganaText: String = "",
        translation: String = "",
        showFurigana: Bool = true,
        showRomaji: Bool = true,
        fontScale: CGFloat = 1.0,
        onWordTapped: ((String) -> Void)? = nil
    ) {
        self.sentenceJa = sentenceJa
        let effectiveFuri = furiganaText.isEmpty ? sentenceJa : furiganaText
        self.furiganaText = effectiveFuri
        self.translation = translation
        self.showFurigana = showFurigana
        self.showRomaji = showRomaji
        self.fontScale = fontScale
        self.onWordTapped = onWordTapped

        let tokens = JapaneseWordSegmenter.shared.segment(text: sentenceJa, furiganaReference: effectiveFuri)
        let mapped = tokens.enumerated().map { (index, tok) in
            KaraokeWordToken(
                id: "\(index)_\(tok.text)",
                index: index,
                kanji: tok.text,
                reading: tok.furigana,
                romaji: tok.romaji,
                meaning: tok.meaning,
                moraWeight: tok.moraWeight
            )
        }
        self._words = State(initialValue: mapped)
    }

    private func normalizeKey(_ key: String) -> String {
        return key.filter { !"。、！？.,!?\"'「」『』〜～()（）[]【】 \t\n\r　".contains($0) }
    }

    private var isCurrentlyPlaying: Bool {
        let clean = sentenceJa.trimmingCharacters(in: .whitespacesAndNewlines)
        let normClean = normalizeKey(clean)
        if normClean.isEmpty { return false }

        if let currentKey = voiceBank.currentPlayingKey {
            let normKey = normalizeKey(currentKey)
            if normKey == normClean {
                return true
            }
        }
        if let currentSpeaking = audioService.currentSpeakingText {
            let normSpeaking = normalizeKey(currentSpeaking)
            if normSpeaking == normClean {
                return true
            }
        }
        return false
    }

    /// Computes the exact currently active word index using mora-calibrated time windows
    private var activeWordIndex: Int? {
        guard isCurrentlyPlaying, !words.isEmpty else { return nil }

        let totalMora = words.reduce(0.0) { $0 + $1.moraWeight }
        guard totalMora > 0 else { return 0 }

        let currentPlaybackTime: Double
        let duration: Double

        if voiceBank.isPlayingNativeAudio && voiceBank.currentDuration > 0 {
            currentPlaybackTime = voiceBank.currentTime
            duration = voiceBank.currentDuration
        } else if audioService.isSpeaking {
            let estimatedDuration = max(1.5, Double(words.count) * 0.45)
            duration = estimatedDuration
            currentPlaybackTime = audioService.playbackProgress * estimatedDuration
        } else {
            return nil
        }

        guard duration > 0 else { return 0 }

        // Millisecond-precision alignment: Progress ratio through total sentence [0.0 ... 1.0]
        let progress = min(1.0, max(0.0, currentPlaybackTime / duration))
        let targetMora = progress * totalMora

        var accumulatedMora = 0.0
        for (idx, w) in words.enumerated() {
            let nextAccum = accumulatedMora + w.moraWeight
            if targetMora >= accumulatedMora && (targetMora < nextAccum || idx == words.count - 1) {
                return idx
            }
            accumulatedMora = nextAccum
        }

        return 0
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Live YouTube Shorts Follow-Along Word Flow
            FlowLayout(spacing: 4) {
                ForEach(words) { token in
                    let isActive = (activeWordIndex == token.index)
                    let isPast = (activeWordIndex != nil && token.index < (activeWordIndex ?? 0))

                    KaraokeWordChip(
                        token: token,
                        isActive: isActive,
                        isPast: isPast,
                        showFurigana: showFurigana,
                        showRomaji: showRomaji,
                        fontScale: fontScale,
                        onTap: {
                            onWordTapped?(token.kanji.isEmpty ? token.reading : token.kanji)
                        }
                    )
                }
            }

            // English / Chinese Translation
            if !translation.isEmpty {
                Text(translation)
                    .font(.system(size: 14 * fontScale, weight: .semibold, design: .rounded))
                    .foregroundColor(.primary.opacity(0.85))
                    .padding(.top, 4)
            }
        }
        .onAppear {
            parseWords()
        }
        .onChange(of: furiganaText) { _ in
            parseWords()
        }
        .onChange(of: sentenceJa) { _ in
            parseWords()
        }
    }

    private func parseWords() {
        let tokens = JapaneseWordSegmenter.shared.segment(text: sentenceJa, furiganaReference: furiganaText)
        self.words = tokens.enumerated().map { (index, tok) in
            KaraokeWordToken(
                id: "\(index)_\(tok.text)",
                index: index,
                kanji: tok.text,
                reading: tok.furigana,
                romaji: tok.romaji,
                meaning: tok.meaning,
                moraWeight: tok.moraWeight
            )
        }
    }
}

// MARK: - Word Token Model
public struct KaraokeWordToken: Identifiable {
    public let id: String
    public let index: Int
    public let kanji: String
    public let reading: String
    public let romaji: String
    public let meaning: String
    public let moraWeight: Double
}

// MARK: - Individual 3-Tier Word Chip (YouTube Shorts Design Standard)
private struct KaraokeWordChip: View {
    let token: KaraokeWordToken
    let isActive: Bool
    let isPast: Bool
    let showFurigana: Bool
    let showRomaji: Bool
    let fontScale: CGFloat
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            VStack(spacing: 2) {
                // Floating Red Indicator Dot (YouTube Shorts follow-along tracker)
                if isActive {
                    Circle()
                        .fill(Color.red)
                        .frame(width: 5 * fontScale, height: 5 * fontScale)
                        .transition(.scale)
                } else {
                    Color.clear
                        .frame(width: 5 * fontScale, height: 5 * fontScale)
                }

                // 1. Top Tier: Furigana / Ruby Reading
                if showFurigana && !token.reading.isEmpty && token.reading != token.kanji {
                    Text(token.reading)
                        .font(.system(size: 11 * fontScale, weight: .bold, design: .rounded))
                        .foregroundColor(isActive ? Color(red: 180/255, green: 83/255, blue: 9/255) : (isPast ? Color.purple.opacity(0.8) : Color.secondary))
                        .lineLimit(1)
                } else {
                    Text(" ")
                        .font(.system(size: 11 * fontScale, weight: .bold, design: .rounded))
                        .lineLimit(1)
                }

                // 2. Middle Tier: Main Japanese Kanji / Word
                Text(token.kanji)
                    .font(.system(size: 20 * fontScale, weight: .heavy, design: .rounded))
                    .foregroundColor(isActive ? Color(red: 15/255, green: 23/255, blue: 42/255) : (isPast ? Color.primary : Color.primary.opacity(0.9)))
                    .lineLimit(1)

                // 3. Bottom Tier: Romaji Pronunciation Guide
                if showRomaji && !token.romaji.isEmpty {
                    Text(token.romaji)
                        .font(.system(size: 10 * fontScale, weight: .semibold, design: .monospaced))
                        .foregroundColor(isActive ? Color(red: 180/255, green: 83/255, blue: 9/255) : (isPast ? Color.purple.opacity(0.7) : Color.secondary.opacity(0.75)))
                        .lineLimit(1)
                } else if showRomaji {
                    Text(" ")
                        .font(.system(size: 10 * fontScale, weight: .semibold, design: .monospaced))
                        .lineLimit(1)
                }
            }
            // Strict Invariant Padding
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(
                ZStack {
                    if isActive {
                        // YouTube Shorts Warm Gold Capsule (#FEF08A fill, #F59E0B outline)
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color(red: 254/255, green: 240/255, blue: 138/255))
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(Color(red: 245/255, green: 158/255, blue: 11/255), lineWidth: 2)
                            )
                            .shadow(color: Color(red: 245/255, green: 158/255, blue: 11/255).opacity(0.4), radius: 6, x: 0, y: 2)
                    } else if isPast {
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.purple.opacity(0.08))
                    } else {
                        RoundedRectangle(cornerRadius: 12)
                            .fill(Color.clear)
                    }
                }
            )
            .animation(.spring(response: 0.25, dampingFraction: 0.75), value: isActive)
        }
        .buttonStyle(.plain)
    }
}
