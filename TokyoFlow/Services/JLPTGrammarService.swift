import Foundation
import Combine

public class JLPTGrammarService: ObservableObject {
    public static let shared = JLPTGrammarService()

    private var isBuildingIndexesInBackground: Bool = false

    @Published public var allGrammar: [JLPTGrammarPoint] = [] {
        didSet {
            guard !isBuildingIndexesInBackground else { return }
            rebuildIndexes()
            updateFilteredCache()
        }
    }
    
    @Published public var selectedLevel: JLPTLevelFilter = .all {
        didSet {
            updateFilteredCache()
        }
    }
    
    @Published public var selectedScenarioTag: String? = nil {
        didSet {
            updateFilteredCache()
        }
    }
    
    @Published public var searchQuery: String = "" {
        didSet {
            updateFilteredCache()
        }
    }
    
    @Published public var bookmarkedGrammarIds: Set<String> = []
    @Published public var isLoaded: Bool = false
    
    private var levelBuckets: [String: [JLPTGrammarPoint]] = [:]
    private var searchIndex: [String: String] = [:]
    private var searchCache = NSCache<NSString, NSArray>()
    private let queue = DispatchQueue(label: "com.tokyoflow.grammar.service", qos: .userInitiated)
    private var isLoadingData: Bool = false
    
    @Published public private(set) var cachedFilteredGrammar: [JLPTGrammarPoint] = []

    private init() {
        loadBookmarks()
        loadGrammarDataAsync()
    }

    public func loadGrammarData() {
        guard !isLoaded else { return }
        if let url = Bundle.main.url(forResource: "jlpt_grammar", withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                let decoded = try JSONDecoder().decode([JLPTGrammarPoint].self, from: data)
                self.allGrammar = decoded
                self.isLoaded = true
                return
            } catch {
                print("️ JLPTGrammarService: Error decoding bundled json: \(error)")
            }
        }

        // Fallback local file system load for testing / preview
        let directPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/jlpt_grammar.json"
        if let data = try? Data(contentsOf: URL(fileURLWithPath: directPath)),
           let decoded = try? JSONDecoder().decode([JLPTGrammarPoint].self, from: data) {
            self.allGrammar = decoded
            self.isLoaded = true
        }
    }

    public func loadGrammarDataAsync() {
        guard !isLoaded && !isLoadingData else { return }
        isLoadingData = true

        queue.async {
            var grammar: [JLPTGrammarPoint]? = nil
            if let url = Bundle.main.url(forResource: "jlpt_grammar", withExtension: "json"),
               let data = try? Data(contentsOf: url),
               let decoded = try? JSONDecoder().decode([JLPTGrammarPoint].self, from: data) {
                grammar = decoded
            } else {
                let directPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/jlpt_grammar.json"
                if let data = try? Data(contentsOf: URL(fileURLWithPath: directPath)),
                   let decoded = try? JSONDecoder().decode([JLPTGrammarPoint].self, from: data) {
                    grammar = decoded
                }
            }

            if let items = grammar {
                var buckets: [String: [JLPTGrammarPoint]] = [
                    "N5": [], "N4": [], "N3": [], "N2": [], "N1": []
                ]
                var sIndex: [String: String] = Dictionary(minimumCapacity: items.count)
                for item in items {
                    buckets[item.level.uppercased(), default: []].append(item)
                    let sentText = item.sentences.map { "\($0.japanese) \($0.english)" }.joined(separator: " ")
                    sIndex[item.id] = "\(item.title) \(item.romaji) \(item.meaningEn) \(item.meaningZh) \(item.connectionRule) \(item.nuanceExplanation) \(item.examTip) \(sentText)".lowercased()
                }

                DispatchQueue.main.async {
                    self.levelBuckets = buckets
                    self.searchIndex = sIndex
                    self.isBuildingIndexesInBackground = true
                    self.allGrammar = items
                    self.isBuildingIndexesInBackground = false
                    self.updateFilteredCache()
                    self.isLoaded = true
                    self.isLoadingData = false
                }
            } else {
                DispatchQueue.main.async {
                    self.isLoadingData = false
                }
            }
        }
    }

    private func rebuildIndexes() {
        var buckets: [String: [JLPTGrammarPoint]] = [
            "N5": [], "N4": [], "N3": [], "N2": [], "N1": []
        ]
        var sIndex: [String: String] = Dictionary(minimumCapacity: allGrammar.count)
        for item in allGrammar {
            buckets[item.level.uppercased(), default: []].append(item)
            let sentText = item.sentences.map { "\($0.japanese) \($0.english)" }.joined(separator: " ")
            sIndex[item.id] = "\(item.title) \(item.romaji) \(item.meaningEn) \(item.meaningZh) \(item.connectionRule) \(item.nuanceExplanation) \(item.examTip) \(sentText)".lowercased()
        }
        self.levelBuckets = buckets
        self.searchIndex = sIndex
        self.searchCache.removeAllObjects()
    }

    private func updateFilteredCache() {
        let q = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        let levelKey = selectedLevel.shortName
        let tagKey = selectedScenarioTag ?? "all_tags"
        let cacheKey = "\(levelKey)_\(tagKey)_\(q)" as NSString

        if let cached = searchCache.object(forKey: cacheKey) as? [JLPTGrammarPoint] {
            self.cachedFilteredGrammar = cached
            return
        }

        let candidates: [JLPTGrammarPoint]
        if selectedLevel == .all {
            candidates = allGrammar
        } else {
            candidates = levelBuckets[levelKey] ?? []
        }

        let results = candidates.filter { item in
            let matchesScenario = (selectedScenarioTag == nil || selectedScenarioTag?.isEmpty == true || item.scenarioTag.lowercased() == selectedScenarioTag?.lowercased())
            guard matchesScenario else { return false }

            if q.isEmpty { return true }
            if let str = self.searchIndex[item.id] {
                return str.contains(q)
            }
            return item.title.lowercased().contains(q) ||
                   item.romaji.lowercased().contains(q) ||
                   item.meaningEn.lowercased().contains(q)
        }

        searchCache.setObject(results as NSArray, forKey: cacheKey)
        self.cachedFilteredGrammar = results
    }

    public var filteredGrammar: [JLPTGrammarPoint] {
        return cachedFilteredGrammar
    }

    public func toggleBookmark(id: String) {
        if bookmarkedGrammarIds.contains(id) {
            bookmarkedGrammarIds.remove(id)
        } else {
            bookmarkedGrammarIds.insert(id)
        }
        saveBookmarks()
    }

    public func isBookmarked(id: String) -> Bool {
        return bookmarkedGrammarIds.contains(id)
    }

    private func saveBookmarks() {
        let array = Array(bookmarkedGrammarIds)
        UserDefaults.standard.set(array, forKey: "tokyo_jlpt_bookmarked_grammar_ids")
    }

    private func loadBookmarks() {
        if let array = UserDefaults.standard.stringArray(forKey: "tokyo_jlpt_bookmarked_grammar_ids") {
            self.bookmarkedGrammarIds = Set(array)
        }
    }
}
