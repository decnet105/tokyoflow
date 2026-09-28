import Foundation

public enum DialogueRegister: String, Codable, CaseIterable {
    case keigo = "keigo"
    case polite = "polite"
    case casualPolite = "casual-polite"
    case casual = "casual"
    case slang = "slang"

    public var displayName: String {
        switch self {
        case .keigo: return "Keigo (敬語 / Respectful)"
        case .polite: return "Polite (丁寧語 / Desu-Masu)"
        case .casualPolite: return "Casual Polite (日常丁寧)"
        case .casual: return "Casual (タメ口 / Friend)"
        case .slang: return "Colloquial / Slang (口語・俗語)"
        }
    }

    public var badgeColorHex: String {
        switch self {
        case .keigo: return "#6366F1" // Indigo
        case .polite: return "#0EA5E9" // Sky Blue
        case .casualPolite: return "#10B981" // Emerald Green
        case .casual: return "#F59E0B" // Amber
        case .slang: return "#EC4899" // Pink
        }
    }
}

public struct DialogueLine: Identifiable, Codable {
    public let id: String
    public let speaker: String
    public let role: String // "learner", "native"
    public let japanese: String
    public let furigana: String
    public let romaji: String
    public let english: String
    public let chinese: String
    public let register: DialogueRegister
    public let audioPrompt: String

    public var isLearner: Bool {
        return role == "learner"
    }
}

public struct InteractiveOption: Identifiable, Codable {
    public var id: String { text }
    public let text: String
    public let furigana: String
    public let romaji: String
    public let isCorrect: Bool
    public let explanation: String
}

public struct InteractiveChallenge: Codable {
    public let prompt: String
    public let options: [InteractiveOption]
}

public struct KeyVocabulary: Identifiable, Codable {
    public var id: String { word }
    public let word: String
    public let reading: String
    public let romaji: String
    public let meaning: String
    public let type: String
}

public struct Scenario: Identifiable, Codable {
    public let id: String
    public let title: String
    public let titleJa: String
    public let category: String // transit, kombini, dining, services, shopping, living_services, office
    public let district: String // Shinjuku, Shibuya, Ginza, etc.
    public let timeOfDay: String
    public let quarter: Int
    public let week: Int
    public let day: Int
    public let jfCanDoLevel: String // A1, A2, B1
    public let jfCanDoDescription: String
    public let context: String
    public let culturalTip: String
    public let dialogue: [DialogueLine]
    public let interactiveChallenge: InteractiveChallenge?
    public let keyVocabulary: [KeyVocabulary]

    public var categoryIcon: String {
        switch category {
        case "transit": return "tram.fill"
        case "kombini": return "cart.fill"
        case "dining": return "fork.knife"
        case "services": return "bicycle"
        case "shopping": return "bag.fill"
        case "living_services": return "shippingbox.fill"
        case "office": return "briefcase.fill"
        default: return "building.2.fill"
        }
    }
}
