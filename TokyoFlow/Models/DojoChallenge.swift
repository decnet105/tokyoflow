import Foundation

public struct DojoOption: Identifiable, Codable {
    public var id: String { text }
    public let text: String
    public let isCorrect: Bool
    public let nuance: String
}

public struct DojoRound: Identifiable, Codable {
    public var id: Int { roundNumber }
    public let roundNumber: Int
    public let clerkPrompt: String
    public let clerkRomaji: String
    public let clerkEnglish: String
    public let options: [DojoOption]
}

public struct DojoBattle: Identifiable, Codable {
    public let id: String
    public let title: String
    public let titleJa: String
    public let difficulty: String
    public let location: String
    public let funTag: String
    public let scenarioSetup: String
    public let rounds: [DojoRound]
    public let ninjaComboPhrase: String
    public let ninjaComboExplanation: String
}
