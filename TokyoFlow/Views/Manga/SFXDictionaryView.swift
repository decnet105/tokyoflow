import SwiftUI

public struct OnomatopoeiaItem: Identifiable {
    public var id: String { japanese }
    public let japanese: String
    public let reading: String
    public let english: String
    public let category: String
    public let exampleManga: String
}

public struct SFXDictionaryView: View {
    @Environment(\.dismiss) var dismiss
    @State private var selectedCategory: String = "all"

    private let sfxList: [OnomatopoeiaItem] = [
        OnomatopoeiaItem(japanese: "ドキドキ", reading: "doki-doki", english: "Heart thumping / nervous excitement", category: "Heart & Emotion", exampleManga: "Rom-com & confession scenes"),
        OnomatopoeiaItem(japanese: "ざわ… ざわ…", reading: "zawa... zawa...", english: "Murmuring uneasiness / crowd tension", category: "Atmosphere", exampleManga: "Kaiji / psychological thrillers"),
        OnomatopoeiaItem(japanese: "ドンッ！", reading: "DON!", english: "Loud impact / dramatic revelation", category: "Action & Impact", exampleManga: "One Piece / shōnen climax panels"),
        OnomatopoeiaItem(japanese: "サクサク", reading: "saku-saku", english: "Crisp, crunchy texture (fried food / cookies)", category: "Food & Texture", exampleManga: "Oishinbo / Solitary Gourmet"),
        OnomatopoeiaItem(japanese: "ジュワッ", reading: "juwa!", english: "Sizzling juices bursting out / grilling meat", category: "Food & Texture", exampleManga: "Yakiniku & gourmet scenes"),
        OnomatopoeiaItem(japanese: "ギラギラ", reading: "gira-gira", english: "Blinding glare / aggressive intense stare", category: "Visual & Sight", exampleManga: "Battle manga eye close-ups"),
        OnomatopoeiaItem(japanese: "ニコニコ", reading: "niko-niko", english: "Warm beaming smile", category: "Heart & Emotion", exampleManga: "Slice of life wholesome moments"),
        OnomatopoeiaItem(japanese: "イライラ", reading: "ira-ira", english: "Irritated / losing patience", category: "Heart & Emotion", exampleManga: "Comedic anger / vein popping"),
        OnomatopoeiaItem(japanese: "ザーザー", reading: "zā-zā", english: "Pouring heavy rainfall", category: "Weather & Nature", exampleManga: "Rainy melodrama scenes"),
        OnomatopoeiaItem(japanese: "コソコソ", reading: "koso-koso", english: "Whispering / sneaking stealthily", category: "Atmosphere", exampleManga: "Ninja / espionage / gossip")
    ]

    private var categories: [String] {
        ["all", "Heart & Emotion", "Action & Impact", "Food & Texture", "Atmosphere", "Visual & Sight", "Weather & Nature"]
    }

    private var filteredList: [OnomatopoeiaItem] {
        if selectedCategory == "all" { return sfxList }
        return sfxList.filter { $0.category == selectedCategory }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 16) {
                    // Category Filter
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(categories, id: \.self) { cat in
                                Button(action: { selectedCategory = cat }) {
                                    Text(cat == "all" ? "All SFX" : cat)
                                        .font(.caption)
                                        .fontWeight(.semibold)
                                        .padding(.horizontal, 12)
                                        .padding(.vertical, 6)
                                        .background(selectedCategory == cat ? Color.purple : Color.primary.opacity(0.08))
                                        .foregroundColor(selectedCategory == cat ? .white : .primary)
                                        .cornerRadius(16)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.top, 8)

                    // List
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(filteredList) { sfx in
                                HStack {
                                    VStack(alignment: .leading, spacing: 4) {
                                        HStack(spacing: 8) {
                                            Text(sfx.japanese)
                                                .font(.system(size: 20, weight: .bold, design: .serif))
                                                .foregroundColor(.purple)
                                            Text("(\(sfx.reading))")
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }
                                        Text(sfx.english)
                                            .font(.footnote)
                                            .foregroundColor(.primary)
                                        Text("Common in: \(sfx.exampleManga)")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                    Spacer()
                                    AudioButton(textToSpeak: sfx.japanese)
                                }
                                .padding(14)
                                .background(.ultraThinMaterial)
                                .cornerRadius(14)
                                .shadow(color: Color.black.opacity(0.03), radius: 6, x: 0, y: 2)
                            }
                        }
                        .padding(.horizontal)
                        .padding(.bottom, 24)
                    }
                }
            }
            .navigationTitle("Manga SFX Soundboard")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
