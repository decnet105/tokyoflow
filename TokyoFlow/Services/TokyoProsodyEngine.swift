import Foundation
import AVFoundation

public enum JapaneseVoiceStyle {
    case dailyConversational
    case newsBroadcast
    case storeClerkPolite
    case excitedManga
    case gentleWhisper
}

public struct TokyoProsodyEngine {

    /// Preprocesses raw Japanese text into prosodically segmented morae phrases with natural breath pauses
    public static func formatProsodyText(_ rawText: String, style: JapaneseVoiceStyle = .dailyConversational) -> String {
        var text = rawText.trimmingCharacters(in: .whitespacesAndNewlines)

        // 1. Particle Boundary Pause Insertion (アクセント句境界の自然なポーズ挿入)
        let particlePatterns: [(String, String)] = [
            ("ですが", "ですが、"),
            ("ですが、", "ですが、"),
            ("けれども", "けれども、"),
            ("なので", "なので、"),
            ("について", "について、"),
            ("につきましては", "につきましては、"),
            ("によると", "によると、"),
            ("からは", "からは、"),
            ("までは", "までは、"),
            ("には", "には、"),
            ("では", "では、"),
            ("まして", "まして、")
        ]

        for (pattern, replacement) in particlePatterns {
            text = text.replacingOccurrences(of: pattern, with: replacement)
        }

        // Clean up double punctuation
        text = text.replacingOccurrences(of: "、、", with: "、")
        text = text.replacingOccurrences(of: "。。", with: "。")
        text = text.replacingOccurrences(of: "！？", with: "！")

        return text
    }

    /// Determines optimal pitch and rate based on speaking style for maximum human naturalness
    public static func prosodySettings(for style: JapaneseVoiceStyle) -> (rate: Float, pitch: Float, preDelay: TimeInterval, postDelay: TimeInterval) {
        switch style {
        case .dailyConversational:
            // Relaxed, natural Japanese rhythm (~320 morae/min)
            return (rate: 0.48, pitch: 1.02, preDelay: 0.02, postDelay: 0.06)

        case .newsBroadcast:
            // Crisp, rhythmic Tokyo standard NHK broadcast cadence
            return (rate: 0.49, pitch: 0.99, preDelay: 0.03, postDelay: 0.08)

        case .storeClerkPolite:
            // Slightly elevated pitch for Japanese hospitality (接客トーン)
            return (rate: 0.47, pitch: 1.08, preDelay: 0.02, postDelay: 0.07)

        case .excitedManga:
            // Dynamic, lively anime cadence
            return (rate: 0.52, pitch: 1.15, preDelay: 0.01, postDelay: 0.05)

        case .gentleWhisper:
            // Soothing, calm
            return (rate: 0.44, pitch: 0.94, preDelay: 0.04, postDelay: 0.10)
        }
    }

    /// Selects the best available neural Japanese voice installed on iOS
    public static func findOptimalJapaneseNeuralVoice() -> AVSpeechSynthesisVoice? {
        let allVoices = AVSpeechSynthesisVoice.speechVoices()
        let jpVoices = allVoices.filter { $0.language.hasPrefix("ja") }

        // 1. Premium Neural Voice
        if let premium = jpVoices.first(where: { $0.quality == .premium || $0.identifier.localizedCaseInsensitiveContains("premium") }) {
            return premium
        }

        // 2. Enhanced Neural Voice (e.g. Kyoko / Otoya / Siri Enhanced)
        if let enhanced = jpVoices.first(where: { $0.quality == .enhanced || $0.identifier.localizedCaseInsensitiveContains("enhanced") }) {
            return enhanced
        }

        // 3. Named Natural Japanese Voices
        if let kyoko = jpVoices.first(where: { $0.name.localizedCaseInsensitiveContains("Kyoko") || $0.name.localizedCaseInsensitiveContains("Otoya") }) {
            return kyoko
        }

        // 4. Default ja-JP Voice
        return AVSpeechSynthesisVoice(language: "ja-JP") ?? AVSpeechSynthesisVoice(language: "ja")
    }
}
