import Foundation

public struct MangaSFX: Identifiable, Codable {
    public var id: String { japanese + romaji }
    public let japanese: String
    public let romaji: String
    public let meaning: String
    public let category: String // onomatopoeia_giseigo, onomatopoeia_gitaigo, sound_effect
    public let visualStyle: String
}

public struct MangaBalloon: Identifiable, Codable {
    public let id: String
    public let speaker: String
    public let bubbleType: String // screaming_jagged, speech_oval, thought_cloud
    public let japanese: String
    public let furigana: String
    public let romaji: String
    public let english: String
    public let chinese: String
    public let nuanceNotes: String
}

public struct MangaPanel: Identifiable, Codable {
    public let id: String
    public let panelNumber: Int
    public let sceneDescription: String
    public let sfx: [MangaSFX]
    public let balloons: [MangaBalloon]
}

public struct GrammarBreakdown: Identifiable, Codable {
    public var id: String { pattern }
    public let pattern: String
    public let explanation: String
    public let example: String
}

public struct MangaLesson: Identifiable, Codable {
    public let id: String
    public let genre: String
    public let title: String
    public let titleJa: String
    public let quarter: Int
    public let difficulty: String
    public let description: String
    public let panels: [MangaPanel]
    public let grammarBreakdowns: [GrammarBreakdown]
}
