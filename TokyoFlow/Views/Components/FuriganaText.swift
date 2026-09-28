import SwiftUI

public struct FuriganaSegment: Identifiable {
    public var id: String { "\(kanji)_\(furigana)_\(raw)" }
    public let kanji: String
    public let furigana: String?
    public let raw: String
}

public struct FuriganaText: View {
    public let textWithFurigana: String
    public let fallbackText: String
    public let showFurigana: Bool
    public let font: Font
    public let textColor: Color

    public init(
        textWithFurigana: String,
        fallbackText: String = "",
        showFurigana: Bool = true,
        font: Font = .body,
        textColor: Color = .primary
    ) {
        self.textWithFurigana = textWithFurigana
        self.fallbackText = fallbackText.isEmpty ? textWithFurigana : fallbackText
        self.showFurigana = showFurigana
        self.font = font
        self.textColor = textColor
    }

    private var parsedSegments: [FuriganaSegment] {
        var segments: [FuriganaSegment] = []
        // Pattern matches: reading{Kanji} e.g. しぶや{渋谷}
        let pattern = "([^{}]+)\\{([^{}]+)\\}"
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return [FuriganaSegment(kanji: fallbackText, furigana: nil, raw: fallbackText)]
        }

        let nsString = textWithFurigana as NSString
        var lastEnd = 0

        let matches = regex.matches(in: textWithFurigana, options: [], range: NSRange(location: 0, length: nsString.length))

        for match in matches {
            if match.range.location > lastEnd {
                let plain = nsString.substring(with: NSRange(location: lastEnd, length: match.range.location - lastEnd))
                segments.append(FuriganaSegment(kanji: plain, furigana: nil, raw: plain))
            }

            let readingRange = match.range(at: 1)
            let kanjiRange = match.range(at: 2)

            let reading = nsString.substring(with: readingRange).trimmingCharacters(in: .whitespaces)
            let kanji = nsString.substring(with: kanjiRange).trimmingCharacters(in: .whitespaces)

            segments.append(FuriganaSegment(kanji: kanji, furigana: reading, raw: "\(reading){\(kanji)}"))
            lastEnd = match.range.location + match.range.length
        }

        if lastEnd < nsString.length {
            let trailing = nsString.substring(from: lastEnd)
            segments.append(FuriganaSegment(kanji: trailing, furigana: nil, raw: trailing))
        }

        return segments.isEmpty ? [FuriganaSegment(kanji: fallbackText, furigana: nil, raw: fallbackText)] : segments
    }

    public var body: some View {
        if !showFurigana {
            Text(cleanText(textWithFurigana))
                .font(font)
                .foregroundColor(textColor)
        } else {
            WrappingHStack(segments: parsedSegments, font: font, textColor: textColor)
        }
    }

    private func cleanText(_ str: String) -> String {
        let pattern = "([^{}]+)\\{([^{}]+)\\}"
        guard let regex = try? NSRegularExpression(pattern: pattern) else { return str }
        let range = NSRange(location: 0, length: str.utf16.count)
        return regex.stringByReplacingMatches(in: str, options: [], range: range, withTemplate: "$2")
    }
}

private struct WrappingHStack: View {
    let segments: [FuriganaSegment]
    let font: Font
    let textColor: Color

    var body: some View {
        // Layout segments horizontally with ruby furigana above kanji
        HStack(alignment: .bottom, spacing: 2) {
            ForEach(segments) { seg in
                if let furi = seg.furigana {
                    VStack(alignment: .center, spacing: 0) {
                        Text(furi)
                            .font(.system(size: 9, weight: .regular))
                            .foregroundColor(.secondary)
                            .lineLimit(1)
                        Text(seg.kanji)
                            .font(font)
                            .foregroundColor(textColor)
                    }
                } else {
                    Text(seg.kanji)
                        .font(font)
                        .foregroundColor(textColor)
                        .alignmentGuide(.bottom) { d in d[.bottom] }
                }
            }
        }
    }
}
