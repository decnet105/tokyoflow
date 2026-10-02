import Foundation

public enum LearningContextMode: String, CaseIterable, Identifiable, Codable {
    case commute = "Morning Commute"
    case coffeeBreak = "5-Min Coffee Break"
    case deepEvening = "Evening Deep Study"
    case travelSurvival = "Travel & Survival Sprint"
    case bedtimeImmersion = "Bedtime Radio Flow"

    public var id: String { rawValue }

    public func localizedName(isEnglish: Bool) -> String {
        switch self {
        case .commute: return isEnglish ? "Morning Commute" : "早高峰通勤"
        case .coffeeBreak: return isEnglish ? "5-Min Coffee Break" : "5分钟咖啡休息"
        case .deepEvening: return isEnglish ? "Evening Deep Study" : "晚间深度精进"
        case .travelSurvival: return isEnglish ? "Travel & Survival Sprint" : "赴日出行速通"
        case .bedtimeImmersion: return isEnglish ? "Bedtime Radio Flow" : "睡前电台伴学"
        }
    }

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

    public func localizedTagline(isEnglish: Bool) -> String {
        switch self {
        case .commute: return isEnglish ? "Audio & reading flow for trains, buses & walking" : "针对电车、公交及步行场景的听读流"
        case .coffeeBreak: return isEnglish ? "3-second reaction drills & rapid spaced recall" : "3秒极速反应训练与高频抗遗忘复习"
        case .deepEvening: return isEnglish ? "Full video breakdown, grammar nuances & manga" : "微课视频深度拆解、语法辨析与漫画精读"
        case .travelSurvival: return isEnglish ? "Golden phrases for kombini, izakaya & tax-free" : "便利店、居酒屋、免税退税黄金必备句"
        case .bedtimeImmersion: return isEnglish ? "Gentle ambient city audio & passive radio flow" : "沉浸式都市原声与电台慢速伴读"
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

    public func localizedLabel(isEnglish: Bool) -> String {
        switch self {
        case .n5: return isEnglish ? "N5 Foundation" : "N5 初级基石"
        case .n4: return isEnglish ? "N4 Elementary" : "N4 进阶巩固"
        case .n3: return isEnglish ? "N3 Intermediate" : "N3 中级过桥"
        case .n2: return isEnglish ? "N2 Business" : "N2 商务流利"
        case .n1: return isEnglish ? "N1 Nuance" : "N1 母语细微"
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

    public func localizedName(isEnglish: Bool) -> String {
        switch self {
        case .practicalFluency: return isEnglish ? "Tokyo Living Fluency" : "东京实战流利"
        case .examSprint: return isEnglish ? "JLPT Exam Mastery" : "JLPT 考点速通"
        }
    }
    
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

    public func localizedName(isEnglish: Bool) -> String {
        switch self {
        case .kanaAccent: return isEnglish ? "Kana & Tone" : "假名与声调"
        case .spacedVocab: return isEnglish ? "Spaced Vocab" : "抗遗忘词汇"
        case .grammarFormula: return isEnglish ? "Grammar Formula" : "句型文法"
        case .goldenSentence: return isEnglish ? "Tokyo Phrase" : "地道金句"
        case .scenarioVideo: return isEnglish ? "Video Lesson" : "情景微课"
        case .newsShadowing: return isEnglish ? "News Broadcast" : "新闻跟读"
        case .dojoReaction: return isEnglish ? "Reaction Dojo" : "极速反应"
        case .examTrapQuiz: return isEnglish ? "Trap Drill" : "避坑测验"
        }
    }
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
