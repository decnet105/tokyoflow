import SwiftUI

public enum AppMangaTheme: String, CaseIterable, Identifiable {
    case none = "Pure Clean (无背景)"
    case tokyoSubway = "Tokyo Metro (东京地铁站)"
    case washiPaper = "Washi Rice Paper (米紙白)"
    case readingCat = "Cozy Reading Cat (読書子猫)"
    case liquidGlass = "Liquid Glasses (流体ガラス)"
    case sunset = "Shibuya Sunset (夕暮れの渋谷)"
    case cozyRoom = "Cozy Kotatsu Room (こたつマンガ部屋)"
    case akibaNeon = "Akihabara Night (秋葉原ネオン街)"
    case rainyCafe = "Rainy Kissaten (雨の喫茶店)"
    case minimalist = "Tokyo Metro Minimal (ミニマル)"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .none: return "slash.circle"
        case .tokyoSubway: return "tram.fill"
        case .washiPaper: return "doc.plaintext.fill"
        case .readingCat: return "cat.fill"
        case .liquidGlass: return "drop.fill"
        case .sunset: return "sun.horizon.fill"
        case .cozyRoom: return "house.fill"
        case .akibaNeon: return "sparkles"
        case .rainyCafe: return "cloud.rain.fill"
        case .minimalist: return "circle.lefthalf.filled"
        }
    }

    public var assetName: String? {
        switch self {
        case .none, .minimalist: return nil
        case .tokyoSubway: return "wallpaper_tokyo_subway"
        case .washiPaper: return "wallpaper_washi_paper"
        case .readingCat: return "wallpaper_reading_cat"
        case .liquidGlass: return "wallpaper_liquid_glass"
        case .sunset: return "wallpaper_sunset"
        case .cozyRoom: return "wallpaper_cozy_room"
        case .akibaNeon: return "wallpaper_akiba_neon"
        case .rainyCafe: return "wallpaper_rainy_cafe"
        }
    }

    public var resourceFileName: String? {
        switch self {
        case .none, .minimalist: return nil
        case .tokyoSubway: return "tokyo_subway.jpg"
        case .washiPaper: return "washi_paper.jpg"
        case .readingCat: return "reading_cat.jpg"
        case .liquidGlass: return "liquid_glass.jpg"
        case .sunset: return "sunset.jpg"
        case .cozyRoom: return "cozy_room.jpg"
        case .akibaNeon: return "akiba_neon.jpg"
        case .rainyCafe: return "rainy_cafe.jpg"
        }
    }
}

public class ThemeManager: ObservableObject {
    public static let shared = ThemeManager()

    @AppStorage("selected_manga_theme") public var currentThemeRaw: String = AppMangaTheme.washiPaper.rawValue {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_blur_level") public var blurRadius: Double = 0.0 {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_dim_opacity") public var dimOpacity: Double = 0.15 {
        didSet {
            objectWillChange.send()
        }
    }

    public var currentTheme: AppMangaTheme {
        get {
            AppMangaTheme(rawValue: currentThemeRaw) ?? .washiPaper
        }
        set {
            currentThemeRaw = newValue.rawValue
        }
    }

    private init() {}
}

public struct MangaThemeBackgroundView: View {
    @ObservedObject var themeManager = ThemeManager.shared
    @State private var animateGlow: Bool = false

    public init() {}

    public var body: some View {
        ZStack {
            if themeManager.currentTheme.assetName != nil,
               let uiImage = loadThemeImage(theme: themeManager.currentTheme) {
                Image(uiImage: uiImage)
                    .resizable()
                    .scaledToFill()
                    .ignoresSafeArea()
                    .blur(radius: themeManager.blurRadius)
                    .overlay(
                        Color.black.opacity(themeManager.dimOpacity)
                            .ignoresSafeArea()
                    )

                // Dynamic ambient animations for interactive wallpapers
                if themeManager.currentTheme == .readingCat {
                    // Soft breathing sunlight aura & steam
                    RadialGradient(
                        colors: [Color.yellow.opacity(animateGlow ? 0.15 : 0.05), Color.clear],
                        center: .topTrailing,
                        startRadius: 50,
                        endRadius: 400
                    )
                    .ignoresSafeArea()
                    .animation(.easeInOut(duration: 3.5).repeatForever(autoreverses: true), value: animateGlow)
                    .onAppear { animateGlow = true }
                } else if themeManager.currentTheme == .liquidGlass {
                    // Moving chromatic fluid glow
                    RadialGradient(
                        colors: [
                            Color.cyan.opacity(animateGlow ? 0.22 : 0.10),
                            Color.purple.opacity(animateGlow ? 0.15 : 0.05),
                            Color.clear
                        ],
                        center: animateGlow ? .topLeading : .bottomTrailing,
                        startRadius: 80,
                        endRadius: 500
                    )
                    .ignoresSafeArea()
                    .animation(.easeInOut(duration: 4.0).repeatForever(autoreverses: true), value: animateGlow)
                    .onAppear { animateGlow = true }
                } else if themeManager.currentTheme == .tokyoSubway {
                    // Soft warm train lamp ambient glow
                    RadialGradient(
                        colors: [Color.orange.opacity(animateGlow ? 0.12 : 0.04), Color.clear],
                        center: .topLeading,
                        startRadius: 40,
                        endRadius: 450
                    )
                    .ignoresSafeArea()
                    .animation(.easeInOut(duration: 4.5).repeatForever(autoreverses: true), value: animateGlow)
                    .onAppear { animateGlow = true }
                } else if themeManager.currentTheme == .washiPaper {
                    // Subtle warm rice paper tint
                    Color(hex: "#FAF8F5").opacity(0.12)
                        .ignoresSafeArea()
                }
            } else if themeManager.currentTheme == .none {
                // Pure Clean / No Wallpaper: Standard iOS system background
                Color(uiColor: .systemGroupedBackground)
                    .ignoresSafeArea()
            } else {
                // Minimalist gradient fallback
                LinearGradient(
                    colors: [
                        Color(hex: "#F8FAFC"),
                        Color(hex: "#E2E8F0")
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
            }
        }
    }

    private func loadThemeImage(theme: AppMangaTheme) -> UIImage? {
        if let assetName = theme.assetName, let img = UIImage(named: assetName) {
            return img
        }
        if let fileName = theme.resourceFileName,
           let path = Bundle.main.path(forResource: fileName, ofType: nil, inDirectory: "Wallpapers"),
           let img = UIImage(contentsOfFile: path) {
            return img
        }
        if let fileName = theme.resourceFileName,
           let path = Bundle.main.path(forResource: fileName, ofType: nil),
           let img = UIImage(contentsOfFile: path) {
            return img
        }
        return nil
    }
}
