import Foundation
import Combine

public enum JLPTLevelFilter: String, CaseIterable, Identifiable {
    case all = "All"
    case n5 = "N5 (Beginner)"
    case n4 = "N4 (Elementary)"
    case n3 = "N3 (Intermediate)"
    case n2 = "N2 (Business)"
    case n1 = "N1 (Advanced)"

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

    @Published public var allWords: [JLPTWord] = [] {
        didSet {
            rebuildIndexes()
            updateFilteredCache()
        }
    }
    
    @Published public var searchQuery: String = "" {
        didSet {
            updateFilteredCache()
        }
    }
    
    @Published public var selectedLevel: JLPTLevelFilter = .all {
        didSet {
            updateFilteredCache()
        }
    }
    
    @Published public var bookmarkedWordIds: Set<String> = []
    
    // High-performance caching & indexing
    private var levelBuckets: [String: [JLPTWord]] = [:]
    private var searchCache = NSCache<NSString, NSArray>()
    
    // Cached filtered results for instantaneous O(1) view access
    @Published public private(set) var cachedFilteredWords: [JLPTWord] = []
    
    // Pagination for ultra-smooth 120fps scrolling
    public let pageSize: Int = 40
    @Published public private(set) var displayedPageCount: Int = 1
    
    public var displayedWords: [JLPTWord] {
        let total = cachedFilteredWords.count
        let limit = min(total, displayedPageCount * pageSize)
        return Array(cachedFilteredWords.prefix(limit))
    }
    
    public var hasMoreWords: Bool {
        return displayedPageCount * pageSize < cachedFilteredWords.count
    }
    
    public func loadMoreWords() {
        if hasMoreWords {
            displayedPageCount += 1
        }
    }
    
    public func resetPagination() {
        displayedPageCount = 1
    }

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

    private func rebuildIndexes() {
        var buckets: [String: [JLPTWord]] = [
            "N5": [], "N4": [], "N3": [], "N2": [], "N1": []
        ]
        for word in allWords {
            buckets[word.level, default: []].append(word)
        }
        self.levelBuckets = buckets
        self.searchCache.removeAllObjects()
    }

    private func updateFilteredCache() {
        resetPagination()
        let q = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        let levelKey = selectedLevel.shortName
        let cacheKey = "\(levelKey)_\(q)" as NSString

        if let cached = searchCache.object(forKey: cacheKey) as? [JLPTWord] {
            self.cachedFilteredWords = cached
            return
        }

        // Determine candidate pool from partitioned bucket
        let candidates: [JLPTWord]
        if selectedLevel == .all {
            candidates = allWords
        } else {
            candidates = levelBuckets[levelKey] ?? []
        }

        let results: [JLPTWord]
        if q.isEmpty {
            results = candidates
        } else {
            results = candidates.filter { word in
                word.kanji.lowercased().contains(q) ||
                word.reading.lowercased().contains(q) ||
                word.romaji.lowercased().contains(q) ||
                word.meaning.lowercased().contains(q) ||
                word.exampleJa.lowercased().contains(q)
            }
        }

        searchCache.setObject(results as NSArray, forKey: cacheKey)
        self.cachedFilteredWords = results
    }

    public var filteredWords: [JLPTWord] {
        return cachedFilteredWords
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
