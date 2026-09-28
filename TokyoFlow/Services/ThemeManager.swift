import SwiftUI

public enum AppMangaTheme: String, CaseIterable, Identifiable {
    case sunset = "Shibuya Sunset (夕暮れの渋谷)"
    case cozyRoom = "Cozy Kotatsu Room (こたつマンガ部屋)"
    case akibaNeon = "Akihabara Night (秋葉原ネオン街)"
    case rainyCafe = "Rainy Kissaten (雨の喫茶店)"
    case minimalist = "Tokyo Metro Dark/Light (ミニマル)"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .sunset: return "sun.horizon.fill"
        case .cozyRoom: return "house.fill"
        case .akibaNeon: return "sparkles"
        case .rainyCafe: return "cloud.rain.fill"
        case .minimalist: return "circle.lefthalf.filled"
        }
    }

    public var assetName: String? {
        switch self {
        case .sunset: return "wallpaper_sunset"
        case .cozyRoom: return "wallpaper_cozy_room"
        case .akibaNeon: return "wallpaper_akiba_neon"
        case .rainyCafe: return "wallpaper_rainy_cafe"
        case .minimalist: return nil
        }
    }

    public var resourceFileName: String? {
        switch self {
        case .sunset: return "sunset.jpg"
        case .cozyRoom: return "cozy_room.jpg"
        case .akibaNeon: return "akiba_neon.jpg"
        case .rainyCafe: return "rainy_cafe.jpg"
        case .minimalist: return nil
        }
    }
}

public class ThemeManager: ObservableObject {
    public static let shared = ThemeManager()

    @AppStorage("selected_manga_theme") public var currentThemeRaw: String = AppMangaTheme.sunset.rawValue {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_blur_level") public var blurRadius: Double = 0.0 {
        didSet {
            objectWillChange.send()
        }
    }

    @AppStorage("theme_dim_opacity") public var dimOpacity: Double = 0.25 {
        didSet {
            objectWillChange.send()
        }
    }

    public var currentTheme: AppMangaTheme {
        get {
            AppMangaTheme(rawValue: currentThemeRaw) ?? .sunset
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
            if let assetName = themeManager.currentTheme.assetName,
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
            } else {
                // Clean gradient / neutral fallback
                LinearGradient(
                    colors: [
                        Color(hex: "#1E1B4B").opacity(0.85),
                        Color(hex: "#312E81").opacity(0.75),
                        Color(hex: "#0F172A").opacity(0.95)
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
