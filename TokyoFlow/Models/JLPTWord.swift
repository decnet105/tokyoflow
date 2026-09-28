import Foundation

public struct JLPTWord: Identifiable, Hashable, Codable {
    public let id: String
    public let kanji: String
    public let reading: String
    public let romaji: String
    public let pitchAccent: String
    public let level: String // "N5", "N4", "N3", "N2", "N1"
    public let partOfSpeech: String
    public let meaning: String
    public let exampleJa: String
    public let exampleFurigana: String
    public let exampleZh: String
    public let exampleEn: String

    public init(
        id: String,
        kanji: String,
        reading: String,
        romaji: String,
        pitchAccent: String,
        level: String,
        partOfSpeech: String,
        meaning: String,
        exampleJa: String,
        exampleFurigana: String,
        exampleZh: String,
        exampleEn: String
    ) {
        self.id = id
        self.kanji = kanji
        self.reading = reading
        self.romaji = romaji
        self.pitchAccent = pitchAccent
        self.level = level
        self.partOfSpeech = partOfSpeech
        self.meaning = meaning
        self.exampleJa = exampleJa
        self.exampleFurigana = exampleFurigana
        self.exampleZh = exampleZh
        self.exampleEn = exampleEn
    }

    public var displayTitle: String {
        return kanji.isEmpty ? reading : kanji
    }
}
