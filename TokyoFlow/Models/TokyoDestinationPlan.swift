import Foundation

public struct GenerativePhrase: Identifiable, Hashable, Codable {
    public var id: String { japanese }
    public let japanese: String
    public let furigana: String
    public let romaji: String
    public let english: String
    public var chinese: String { english }
    public let pitchAccent: String // e.g., "① Atamadaka", "⓪ Heiban"
    public let situationNote: String
    public let audioKey: String

    public init(japanese: String, furigana: String, romaji: String, english: String, pitchAccent: String, situationNote: String, audioKey: String) {
        self.japanese = japanese
        self.furigana = furigana
        self.romaji = romaji
        self.english = english
        self.pitchAccent = pitchAccent
        self.situationNote = situationNote
        self.audioKey = audioKey
    }

    public init(japanese: String, furigana: String, romaji: String, chinese: String, pitchAccent: String, situationNote: String, audioKey: String) {
        self.init(japanese: japanese, furigana: furigana, romaji: romaji, english: chinese, pitchAccent: pitchAccent, situationNote: situationNote, audioKey: audioKey)
    }
}

public struct GenerativeDialogueTurn: Identifiable, Hashable, Codable {
    public var id: String { "\(speaker)_\(japanese)" }
    public let speaker: String
    public let speakerRole: String // "Staff", "Station Clerk", "You (Learner)"
    public let japanese: String
    public let furigana: String
    public let english: String
    public var chinese: String { english }
    public let isUser: Bool

    public init(speaker: String, speakerRole: String, japanese: String, furigana: String, english: String, isUser: Bool) {
        self.speaker = speaker
        self.speakerRole = speakerRole
        self.japanese = japanese
        self.furigana = furigana
        self.english = english
        self.isUser = isUser
    }

    public init(speaker: String, speakerRole: String, japanese: String, furigana: String, chinese: String, isUser: Bool) {
        self.init(speaker: speaker, speakerRole: speakerRole, japanese: japanese, furigana: furigana, english: chinese, isUser: isUser)
    }
}

public struct TokyoDestinationPlan: Identifiable, Hashable, Codable {
    public let id: String
    public let destinationName: String
    public let destinationJa: String
    public let district: String
    public let categoryIcon: String
    public let tag: String
    public let overview: String
    public let survivalPhrases: [GenerativePhrase]
    public let scenarioDialogue: [GenerativeDialogueTurn]
    public let culturalTips: [String]
    public let challengeMission: String

    public init(
        id: String,
        destinationName: String,
        destinationJa: String,
        district: String,
        categoryIcon: String,
        tag: String,
        overview: String,
        survivalPhrases: [GenerativePhrase],
        scenarioDialogue: [GenerativeDialogueTurn],
        culturalTips: [String],
        challengeMission: String
    ) {
        self.id = id
        self.destinationName = destinationName
        self.destinationJa = destinationJa
        self.district = district
        self.categoryIcon = categoryIcon
        self.tag = tag
        self.overview = overview
        self.survivalPhrases = survivalPhrases
        self.scenarioDialogue = scenarioDialogue
        self.culturalTips = culturalTips
        self.challengeMission = challengeMission
    }
}
