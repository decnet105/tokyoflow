import Foundation
#if canImport(DeveloperToolsSupport)
import DeveloperToolsSupport
#endif

#if SWIFT_PACKAGE
private let resourceBundle = Foundation.Bundle.module
#else
private class ResourceBundleClass {}
private let resourceBundle = Foundation.Bundle(for: ResourceBundleClass.self)
#endif

// MARK: - Color Symbols -

@available(iOS 17.0, macOS 14.0, tvOS 17.0, watchOS 10.0, *)
extension DeveloperToolsSupport.ColorResource {

}

// MARK: - Image Symbols -

@available(iOS 17.0, macOS 14.0, tvOS 17.0, watchOS 10.0, *)
extension DeveloperToolsSupport.ImageResource {

    /// The "wallpaper_akiba_neon" asset catalog image resource.
    static let wallpaperAkibaNeon = DeveloperToolsSupport.ImageResource(name: "wallpaper_akiba_neon", bundle: resourceBundle)

    /// The "wallpaper_cozy_room" asset catalog image resource.
    static let wallpaperCozyRoom = DeveloperToolsSupport.ImageResource(name: "wallpaper_cozy_room", bundle: resourceBundle)

    /// The "wallpaper_liquid_glass" asset catalog image resource.
    static let wallpaperLiquidGlass = DeveloperToolsSupport.ImageResource(name: "wallpaper_liquid_glass", bundle: resourceBundle)

    /// The "wallpaper_rainy_cafe" asset catalog image resource.
    static let wallpaperRainyCafe = DeveloperToolsSupport.ImageResource(name: "wallpaper_rainy_cafe", bundle: resourceBundle)

    /// The "wallpaper_reading_cat" asset catalog image resource.
    static let wallpaperReadingCat = DeveloperToolsSupport.ImageResource(name: "wallpaper_reading_cat", bundle: resourceBundle)

    /// The "wallpaper_sunset" asset catalog image resource.
    static let wallpaperSunset = DeveloperToolsSupport.ImageResource(name: "wallpaper_sunset", bundle: resourceBundle)

    /// The "wallpaper_tokyo_subway" asset catalog image resource.
    static let wallpaperTokyoSubway = DeveloperToolsSupport.ImageResource(name: "wallpaper_tokyo_subway", bundle: resourceBundle)

    /// The "wallpaper_washi_paper" asset catalog image resource.
    static let wallpaperWashiPaper = DeveloperToolsSupport.ImageResource(name: "wallpaper_washi_paper", bundle: resourceBundle)

}

