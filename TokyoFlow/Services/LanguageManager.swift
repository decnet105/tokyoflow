import SwiftUI

public enum AppLanguage: String, CaseIterable, Identifiable, Codable {
    case english = "en"
    case simplifiedChinese = "zh-Hans"
    case traditionalChinese = "zh-Hant"
    case spanish = "es"
    case korean = "ko"
    case french = "fr"
    case german = "de"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .english: return "English (English)"
        case .simplifiedChinese: return "简体中文 (Simplified Chinese)"
        case .traditionalChinese: return "繁體中文 (Traditional Chinese)"
        case .spanish: return "Español (Spanish)"
        case .korean: return "한국어 (Korean)"
        case .french: return "Français (French)"
        case .german: return "Deutsch (German)"
        }
    }

    public var flagIcon: String {
        switch self {
        case .english: return "🇺🇸"
        case .simplifiedChinese: return "🇨🇳"
        case .traditionalChinese: return "🇹🇼"
        case .spanish: return "🇪🇸"
        case .korean: return "🇰🇷"
        case .french: return "🇫🇷"
        case .german: return "🇩🇪"
        }
    }
}

public class LanguageManager: ObservableObject {
    public static let shared = LanguageManager()

    @AppStorage("app_preferred_learning_language") public var currentLanguageRaw: String = AppLanguage.english.rawValue {
        didSet {
            objectWillChange.send()
        }
    }

    public var currentLanguage: AppLanguage {
        get {
            AppLanguage(rawValue: currentLanguageRaw) ?? .english
        }
        set {
            currentLanguageRaw = newValue.rawValue
        }
    }

    private init() {}

    /// Extensible translation lookup table for future multi-language scaling
    public func localized(_ key: String, default defaultVal: String? = nil) -> String {
        // Fallback directly to English base string
        return defaultVal ?? key
    }
}
