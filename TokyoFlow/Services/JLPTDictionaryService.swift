import Foundation
import Combine

public enum JLPTLevelFilter: String, CaseIterable, Identifiable {
    case all = "All (全部)"
    case n5 = "N5 (初级)"
    case n4 = "N4 (基础)"
    case n3 = "N3 (进阶)"
    case n2 = "N2 (商务)"
    case n1 = "N1 (高级)"

    public var id: String { rawValue }

    public var shortName: String {
        switch self {
        case .all: return "ALL"
        case .n5: return "N5"
        case .n4: return "N4"
        case .n3: return "N3"
        case .n2: return "N2"
        case .n1: return "N1"
        }
    }
}

public class JLPTDictionaryService: ObservableObject {
    public static let shared = JLPTDictionaryService()

    @Published public var allWords: [JLPTWord] = []
    @Published public var searchQuery: String = ""
    @Published public var selectedLevel: JLPTLevelFilter = .all
    @Published public var bookmarkedWordIds: Set<String> = []

    private init() {
        loadDictionary()
        loadBookmarks()
    }

    public func loadDictionary() {
        if let url = Bundle.main.url(forResource: "jlpt_dictionary", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let list = try? JSONDecoder().decode([JLPTWord].self, from: data) {
            self.allWords = list
            return
        }

        // Direct path fallback for development
        let devPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/jlpt_dictionary.json"
        if FileManager.default.fileExists(atPath: devPath),
           let data = try? Data(contentsOf: URL(fileURLWithPath: devPath)),
           let list = try? JSONDecoder().decode([JLPTWord].self, from: data) {
            self.allWords = list
        }
    }

    public var filteredWords: [JLPTWord] {
        return allWords.filter { word in
            // Filter by level
            let levelMatch: Bool = {
                switch selectedLevel {
                case .all: return true
                case .n5: return word.level == "N5"
                case .n4: return word.level == "N4"
                case .n3: return word.level == "N3"
                case .n2: return word.level == "N2"
                case .n1: return word.level == "N1"
                }
            }()

            guard levelMatch else { return false }

            let q = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
            if q.isEmpty { return true }

            return word.kanji.lowercased().contains(q) ||
                   word.reading.lowercased().contains(q) ||
                   word.romaji.lowercased().contains(q) ||
                   word.meaning.lowercased().contains(q) ||
                   word.exampleJa.lowercased().contains(q)
        }
    }

    public func toggleBookmark(id: String) {
        if bookmarkedWordIds.contains(id) {
            bookmarkedWordIds.remove(id)
        } else {
            bookmarkedWordIds.insert(id)
        }
        saveBookmarks()
    }

    public func isBookmarked(id: String) -> Bool {
        return bookmarkedWordIds.contains(id)
    }

    private func saveBookmarks() {
        let array = Array(bookmarkedWordIds)
        UserDefaults.standard.set(array, forKey: "tokyo_jlpt_bookmarked_word_ids")
    }

    private func loadBookmarks() {
        if let array = UserDefaults.standard.stringArray(forKey: "tokyo_jlpt_bookmarked_word_ids") {
            self.bookmarkedWordIds = Set(array)
        }
    }
}
