import SwiftUI

public struct ThemePickerSheet: View {
    @ObservedObject var themeManager = ThemeManager.shared
    @Environment(\.dismiss) private var dismiss

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Header
                        VStack(alignment: .leading, spacing: 4) {
                            Text("CUSTOMIZE MANGA THEME")
                                .font(.system(size: 11, weight: .bold))
                                .foregroundColor(.accentColor)
                                .tracking(1.5)
                            Text("Tokyo Anime Wallpapers")
                                .font(.system(size: 22, weight: .black, design: .rounded))
                            Text("Select an HD anime atmosphere wallpaper to immerse yourself in Tokyo life.")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Theme Cards Grid
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
                            ForEach(AppMangaTheme.allCases) { theme in
                                Button(action: {
                                    themeManager.currentTheme = theme
                                }) {
                                    ThemeCardThumbnailView(
                                        theme: theme,
                                        isSelected: themeManager.currentTheme == theme
                                    )
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                        .padding(.horizontal)

                        // Visual Adjustments (Blur & Dim)
                        VStack(alignment: .leading, spacing: 14) {
                            Text("Atmosphere Adjustments")
                                .font(.system(size: 14, weight: .bold))

                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Text("Background Blur")
                                        .font(.caption)
                                    Spacer()
                                    Text("\(Int(themeManager.blurRadius)) pt")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                }
                                Slider(value: $themeManager.blurRadius, in: 0...20, step: 1)
                            }

                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Text("Background Dim / Contrast")
                                        .font(.caption)
                                    Spacer()
                                    Text("\(Int(themeManager.dimOpacity * 100))%")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                }
                                Slider(value: $themeManager.dimOpacity, in: 0.05...0.7, step: 0.05)
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                    }
                    .padding(.bottom, 30)
                }
            }
            .navigationTitle("Theme & Wallpapers")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}

public struct ThemeCardThumbnailView: View {
    public let theme: AppMangaTheme
    public let isSelected: Bool

    public var body: some View {
        VStack(spacing: 8) {
            ZStack {
                if let assetName = theme.assetName,
                   let img = UIImage(named: assetName) ?? loadFallback(fileName: theme.resourceFileName) {
                    Image(uiImage: img)
                        .resizable()
                        .scaledToFill()
                        .frame(height: 140)
                        .clipped()
                        .cornerRadius(14)
                } else {
                    RoundedRectangle(cornerRadius: 14)
                        .fill(theme == .none ? Color(.secondarySystemGroupedBackground) : Color.gray.opacity(0.2))
                        .frame(height: 140)
                        .overlay(
                            VStack(spacing: 6) {
                                Image(systemName: theme.icon)
                                    .font(.system(size: 32, weight: .semibold))
                                    .foregroundColor(.accentColor)
                                Text(theme == .none ? "无背景 (Clean)" : "Minimal")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(.secondary)
                            }
                        )
                }

                if isSelected {
                    RoundedRectangle(cornerRadius: 14)
                        .stroke(Color.accentColor, lineWidth: 3.5)

                    VStack {
                        HStack {
                            Spacer()
                            Image(systemName: "checkmark.circle.fill")
                                .foregroundColor(.accentColor)
                                .font(.title3)
                                .padding(8)
                        }
                        Spacer()
                    }
                }
            }
            .frame(height: 140)

            Text(theme.rawValue.components(separatedBy: " (").first ?? theme.rawValue)
                .font(.system(size: 12, weight: .bold))
                .foregroundColor(.primary)
                .lineLimit(1)
        }
        .padding(8)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
    }

    private func loadFallback(fileName: String?) -> UIImage? {
        guard let fileName = fileName else { return nil }
        if let path = Bundle.main.path(forResource: fileName, ofType: nil, inDirectory: "Wallpapers"),
           let img = UIImage(contentsOfFile: path) {
            return img
        }
        if let path = Bundle.main.path(forResource: fileName, ofType: nil),
           let img = UIImage(contentsOfFile: path) {
            return img
        }
        return nil
    }
}
