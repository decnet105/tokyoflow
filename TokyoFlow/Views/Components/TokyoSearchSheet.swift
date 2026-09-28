import SwiftUI

public struct SearchResultItem: Identifiable {
    public let id: String
    public let title: String
    public let japanese: String
    public let reading: String
    public let translation: String
    public let category: String
    public let icon: String
}

public struct TokyoSearchSheet: View {
    @Environment(\.dismiss) var dismiss
    @ObservedObject var dataManager = DataManager.shared
    @State private var searchQuery: String = ""

    public init() {}

    private var allSearchableItems: [SearchResultItem] {
        var items: [SearchResultItem] = []

        // Scenarios
        for s in dataManager.scenarios {
            items.append(
                SearchResultItem(
                    id: "scenario_\(s.id)",
                    title: s.title,
                    japanese: s.titleJa,
                    reading: s.district,
                    translation: s.context,
                    category: "Scenario (\(s.district))",
                    icon: s.categoryIcon
                )
            )
            for v in s.keyVocabulary {
                items.append(
                    SearchResultItem(
                        id: "vocab_\(s.id)_\(v.word)",
                        title: v.word,
                        japanese: v.word,
                        reading: v.reading,
                        translation: v.meaning,
                        category: "Vocabulary (in \(s.district))",
                        icon: "character.book.closed.fill"
                    )
                )
            }
        }

        // Manga SFX
        for l in dataManager.mangaLessons {
            for p in l.panels {
                for sfx in p.sfx {
                    items.append(
                        SearchResultItem(
                            id: "sfx_\(sfx.japanese)",
                            title: sfx.japanese,
                            japanese: sfx.japanese,
                            reading: sfx.romaji,
                            translation: sfx.meaning,
                            category: "Manga SFX (\(l.genre))",
                            icon: "sparkles"
                        )
                    )
                }
            }
        }

        // Announcements
        for a in dataManager.announcements {
            items.append(
                SearchResultItem(
                    id: "ann_\(a.id)",
                    title: a.title,
                    japanese: a.japanese,
                    reading: a.romaji,
                    translation: a.english,
                    category: "Announcement (\(a.location))",
                    icon: "headphones"
                )
            )
        }

        return items
    }

    private var filteredResults: [SearchResultItem] {
        if searchQuery.trimmingCharacters(in: .whitespaces).isEmpty {
            return Array(allSearchableItems.prefix(15))
        }
        let q = searchQuery.lowercased()
        return allSearchableItems.filter {
            $0.title.lowercased().contains(q) ||
            $0.japanese.contains(q) ||
            $0.reading.lowercased().contains(q) ||
            $0.translation.lowercased().contains(q)
        }
    }

    public var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Search Input Bar
                HStack(spacing: 8) {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.secondary)
                    TextField("Search bento, ticket, platform, SFX...", text: $searchQuery)
                        .autocorrectionDisabled()
                        .textInputAutocapitalization(.never)
                    if !searchQuery.isEmpty {
                        Button(action: { searchQuery = "" }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .padding(12)
                .background(Color(.systemGray6))
                .cornerRadius(12)
                .padding()

                // Results List
                List(filteredResults) { item in
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Label(item.category, systemImage: item.icon)
                                    .font(.caption2)
                                    .fontWeight(.bold)
                                    .foregroundColor(.accentColor)
                            }
                            Text(item.japanese)
                                .font(.headline)
                            Text(item.reading)
                                .font(.caption)
                                .foregroundColor(.secondary)
                            Text(item.translation)
                                .font(.footnote)
                                .foregroundColor(.primary.opacity(0.85))
                                .lineLimit(2)
                        }
                        Spacer()
                        AudioButton(textToSpeak: item.japanese)
                    }
                    .padding(.vertical, 4)
                }
                .listStyle(.plain)
            }
            .navigationTitle("Tokyo Finder")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
