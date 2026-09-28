import Foundation
import Combine

public class JLPTGrammarService: ObservableObject {
    public static let shared = JLPTGrammarService()

    @Published public var allGrammar: [JLPTGrammarPoint] = []
    @Published public var selectedLevel: JLPTLevelFilter = .all
    @Published public var selectedScenarioTag: String? = nil
    @Published public var searchQuery: String = ""
    @Published public var bookmarkedGrammarIds: Set<String> = []

    private init() {
        loadGrammarData()
    }

    public func loadGrammarData() {
        if let url = Bundle.main.url(forResource: "jlpt_grammar", withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                let decoded = try JSONDecoder().decode([JLPTGrammarPoint].self, from: data)
                self.allGrammar = decoded
                return
            } catch {
                print("⚠️ JLPTGrammarService: Error decoding bundled json: \(error)")
            }
        }

        // Fallback local file system load for testing / preview
        let directPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/jlpt_grammar.json"
        if let data = try? Data(contentsOf: URL(fileURLWithPath: directPath)),
           let decoded = try? JSONDecoder().decode([JLPTGrammarPoint].self, from: data) {
            self.allGrammar = decoded
            print("✅ JLPTGrammarService: Loaded \(decoded.count) grammar points from direct path.")
        }
    }


    public var filteredGrammar: [JLPTGrammarPoint] {
        allGrammar.filter { item in
            // Level Filter
            let matchesLevel: Bool
            switch selectedLevel {
            case .all: matchesLevel = true
            case .n5: matchesLevel = (item.level.uppercased() == "N5")
            case .n4: matchesLevel = (item.level.uppercased() == "N4")
            case .n3: matchesLevel = (item.level.uppercased() == "N3")
            case .n2: matchesLevel = (item.level.uppercased() == "N2")
            case .n1: matchesLevel = (item.level.uppercased() == "N1")
            }

            // Scenario Filter
            let matchesScenario: Bool
            if let tag = selectedScenarioTag, !tag.isEmpty {
                matchesScenario = (item.scenarioTag.lowercased() == tag.lowercased())
            } else {
                matchesScenario = true
            }

            // Search Query Filter
            let matchesQuery: Bool
            let q = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
            if q.isEmpty {
                matchesQuery = true
            } else {
                matchesQuery = item.title.lowercased().contains(q) ||
                               item.meaningZh.lowercased().contains(q) ||
                               item.meaningEn.lowercased().contains(q) ||
                               item.romaji.lowercased().contains(q) ||
                               item.connectionRule.lowercased().contains(q)
            }

            return matchesLevel && matchesScenario && matchesQuery
        }
    }

    public func toggleBookmark(id: String) {
        if bookmarkedGrammarIds.contains(id) {
            bookmarkedGrammarIds.remove(id)
        } else {
            bookmarkedGrammarIds.insert(id)
        }
    }

    public func isBookmarked(id: String) -> Bool {
        bookmarkedGrammarIds.contains(id)
    }
}
