import Foundation

public enum LearningContextMode: String, CaseIterable, Identifiable, Codable {
    case commute = "Morning Commute"
    case coffeeBreak = "5-Min Coffee Break"
    case deepEvening = "Evening Deep Study"
    case travelSurvival = "Travel & Survival Sprint"
    case bedtimeImmersion = "Bedtime Radio Flow"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .commute: return "tram.fill"
        case .coffeeBreak: return "cup.and.saucer.fill"
        case .deepEvening: return "moon.stars.fill"
        case .travelSurvival: return "airplane.departure"
        case .bedtimeImmersion: return "headphones"
        }
    }

    public var badgeColorHex: String {
        switch self {
        case .commute: return "#3B82F6"      // Blue
        case .coffeeBreak: return "#F59E0B"  // Amber
        case .deepEvening: return "#8B5CF6"  // Purple
        case .travelSurvival: return "#EF4444" // Red
        case .bedtimeImmersion: return "#10B981" // Emerald
        }
    }

    public var targetDuration: String {
        switch self {
        case .commute: return "~6 min"
        case .coffeeBreak: return "~3 min"
        case .deepEvening: return "~12 min"
        case .travelSurvival: return "~5 min"
        case .bedtimeImmersion: return "~15 min"
        }
    }

    public var tagline: String {
        switch self {
        case .commute: return "Audio & reading flow for trains, buses & walking"
        case .coffeeBreak: return "3-second reaction drills & rapid spaced recall"
        case .deepEvening: return "Full video breakdown, grammar nuances & manga"
        case .travelSurvival: return "Golden phrases for kombini, izakaya & tax-free"
        case .bedtimeImmersion: return "Gentle ambient city audio & passive radio flow"
        }
    }
}

public enum JLPTLevelTrack: String, CaseIterable, Identifiable, Codable {
    case n5 = "JLPT N5 (Beginner Foundation)"
    case n4 = "JLPT N4 (Elementary Mastery)"
    case n3 = "JLPT N3 (Intermediate Bridge)"
    case n2 = "JLPT N2 (Business Fluency)"
    case n1 = "JLPT N1 (Native & Nuance)"

    public var id: String { rawValue }
    
    public var shortLabel: String {
        switch self {
        case .n5: return "N5"
        case .n4: return "N4"
        case .n3: return "N3"
        case .n2: return "N2"
        case .n1: return "N1"
        }
    }

    public var badgeColorHex: String {
        switch self {
        case .n5: return "#10B981"
        case .n4: return "#06B6D4"
        case .n3: return "#3B82F6"
        case .n2: return "#8B5CF6"
        case .n1: return "#EC4899"
        }
    }
}

public enum LearningCurriculumTrack: Equatable, Codable {
    case scenario(LearningContextMode)
    case jlpt(JLPTLevelTrack)
}

public enum LearningFocusMode: String, CaseIterable, Identifiable, Codable {
    case practicalFluency = "Tokyo Living Fluency"
    case examSprint = "JLPT Exam & Trap Mastery"

    public var id: String { rawValue }
    
    public var icon: String {
        switch self {
        case .practicalFluency: return "sparkles"
        case .examSprint: return "graduationcap.fill"
        }
    }
}

public enum PackageStepType: String, Codable {
    case kanaAccent = "Kana & Tone Baseline"
    case spacedVocab = "Essential Vocab Recall"
    case grammarFormula = "Grammar Blueprint"
    case goldenSentence = "Real-World Tokyo Phrase"
    case scenarioVideo = "YouTube Masterclass"
    case newsShadowing = "News Broadcast"
    case dojoReaction = "3-Second Reaction Dojo"
    case examTrapQuiz = "JLPT Exam Trap Drill"
}


public struct LearningPackageItem: Identifiable, Codable {
    public let id: String
    public let type: PackageStepType
    public let title: String
    public let subtitle: String
    public let japaneseText: String
    public let furiganaText: String
    public let englishMeaning: String
    public let pitchAccent: String?
    public let audioKey: String
    public let youtubeVideoId: String?
    public let tip: String?
    public let connectionRule: String?
    public let collocation: String?
    public let quizOptions: [String]?
    public let quizCorrectIndex: Int?
    public let quizExplanation: String?
    public var isCompleted: Bool = false

    public init(
        id: String = UUID().uuidString,
        type: PackageStepType,
        title: String,
        subtitle: String,
        japaneseText: String,
        furiganaText: String,
        englishMeaning: String,
        pitchAccent: String? = nil,
        audioKey: String,
        youtubeVideoId: String? = nil,
        tip: String? = nil,
        connectionRule: String? = nil,
        collocation: String? = nil,
        quizOptions: [String]? = nil,
        quizCorrectIndex: Int? = nil,
        quizExplanation: String? = nil,
        isCompleted: Bool = false
    ) {
        self.id = id
        self.type = type
        self.title = title
        self.subtitle = subtitle
        self.japaneseText = japaneseText
        self.furiganaText = furiganaText
        self.englishMeaning = englishMeaning
        self.pitchAccent = pitchAccent
        self.audioKey = audioKey
        self.youtubeVideoId = youtubeVideoId
        self.tip = tip
        self.connectionRule = connectionRule
        self.collocation = collocation
        self.quizOptions = quizOptions
        self.quizCorrectIndex = quizCorrectIndex
        self.quizExplanation = quizExplanation
        self.isCompleted = isCompleted
    }
}

public struct TokyoLearningPackage: Identifiable, Codable {
    public let id: String
    public let mode: LearningContextMode
    public let levelTrack: JLPTLevelTrack?
    public let focusMode: LearningFocusMode
    public let generatedDate: Date
    public let estimatedMinutes: Int
    public var items: [LearningPackageItem]
    public var currentItemIndex: Int = 0

    public init(
        id: String = UUID().uuidString,
        mode: LearningContextMode = .commute,
        levelTrack: JLPTLevelTrack? = nil,
        focusMode: LearningFocusMode = .practicalFluency,
        generatedDate: Date = Date(),
        estimatedMinutes: Int,
        items: [LearningPackageItem],
        currentItemIndex: Int = 0
    ) {
        self.id = id
        self.mode = mode
        self.levelTrack = levelTrack
        self.focusMode = focusMode
        self.generatedDate = generatedDate
        self.estimatedMinutes = estimatedMinutes
        self.items = items
        self.currentItemIndex = currentItemIndex
    }

    public var isAllCompleted: Bool {
        return items.allSatisfy { $0.isCompleted }
    }

    public var progress: Double {
        guard !items.isEmpty else { return 0.0 }
        let completed = items.filter { $0.isCompleted }.count
        return Double(completed) / Double(items.count)
    }
}
