import SwiftUI

public enum AppMangaTheme: String, CaseIterable, Identifiable {
    case none = "Pure Clean (极简纯白 / 最优对比度)"
    case washiPaper = "Washi Rice Paper (日式和纸 / 柔和护眼)"
    case readingCat = "Cozy Bookroom (暖白书房 / 舒适阅读)"
    case morningMist = "Morning Mist (晨雾浅蓝 / 清新护眼)"
    case warmSepia = "Bookish Sepia (复古暖页 / 柔光阅读)"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .none: return "sun.max.fill"
        case .washiPaper: return "doc.plaintext.fill"
        case .readingCat: return "cat.fill"
        case .morningMist: return "cloud.sun.fill"
        case .warmSepia: return "book.closed.fill"
        }
    }

    public var assetName: String? {
        switch self {
        case .none, .morningMist, .warmSepia: return nil
        case .washiPaper: return "wallpaper_washi_paper"
        case .readingCat: return "wallpaper_reading_cat"
        }
    }

    public var resourceFileName: String? {
        switch self {
        case .none, .morningMist, .warmSepia: return nil
        case .washiPaper: return "washi_paper.jpg"
        case .readingCat: return "reading_cat.jpg"
        }
    }
}

public class ThemeManager: ObservableObject {
    public static let shared = ThemeManager()

    @AppStorage("selected_manga_theme") public var currentThemeRaw: String = AppMangaTheme.none.rawValue {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_blur_level") public var blurRadius: Double = 0.0 {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_dim_opacity") public var dimOpacity: Double = 0.05 {
        didSet {
            objectWillChange.send()
        }
    }

    public var currentTheme: AppMangaTheme {
        get {
            AppMangaTheme(rawValue: currentThemeRaw) ?? .none
        }
        set {
            currentThemeRaw = newValue.rawValue
        }
    }

    private init() {}
}

public struct MangaThemeBackgroundView: View {
    @ObservedObject var themeManager = ThemeManager.shared

    public init() {}

    public var body: some View {
        ZStack {
            switch themeManager.currentTheme {
            case .none:
                // Standard Clean iOS Grouped Background (Maximum Contrast & Readability)
                Color(uiColor: .systemGroupedBackground)
                    .ignoresSafeArea()

            case .washiPaper:
                // Authentic soft Japanese washi paper tint
                Color(hex: "#F9F7F2")
                    .ignoresSafeArea()

            case .readingCat:
                // Soft cream background with gentle warm hue
                Color(hex: "#FAF6EF")
                    .ignoresSafeArea()

            case .morningMist:
                // Ultra soft morning mist light gradient
                LinearGradient(
                    colors: [Color(hex: "#F4F7FA"), Color(hex: "#EBF0F5")],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()

            case .warmSepia:
                // Eye-comfort warm sepia book page tone
                LinearGradient(
                    colors: [Color(hex: "#FCFAF4"), Color(hex: "#F4EFE6")],
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()
            }
        }
    }
}
