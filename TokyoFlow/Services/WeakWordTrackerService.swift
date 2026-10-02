import Foundation
import Combine

public struct WeakWordItem: Identifiable, Codable, Hashable {
    public let id: String
    public let word: String
    public let reading: String
    public let romaji: String
    public let meaning: String
    public var reason: String // " Replayed 3 times", "⏱️ Hesitated 5.4s", " Quiz mistake"
    public var listenCount: Int
    public var dwellSeconds: Double
    public var mistakeCount: Int
    public var dateAdded: Date
    public var isMastered: Bool

    public init(
        word: String,
        reading: String,
        romaji: String = "",
        meaning: String = "",
        reason: String,
        listenCount: Int = 1,
        dwellSeconds: Double = 0.0,
        mistakeCount: Int = 0,
        dateAdded: Date = Date(),
        isMastered: Bool = false
    ) {
        self.id = word
        self.word = word
        self.reading = reading
        self.romaji = romaji
        self.meaning = meaning
        self.reason = reason
        self.listenCount = listenCount
        self.dwellSeconds = dwellSeconds
        self.mistakeCount = mistakeCount
        self.dateAdded = dateAdded
        self.isMastered = isMastered
    }
}

public class WeakWordTrackerService: ObservableObject {
    public static let shared = WeakWordTrackerService()

    @Published public var weakWords: [WeakWordItem] = []
    private var sessionListenCounters: [String: Int] = [:]
    private var wordDwellStartTimes: [String: Date] = [:]

    private let storageKey = "tokyo_user_weak_words_list_v1"

    private init() {
        loadWeakWords()
    }

    // MARK: - Behavior Tracking Triggers
    /// Record when user plays pronunciation (if repeated >= 2 times in session -> flagged)
    public func recordListen(word: String, reading: String = "", meaning: String = "") {
        let clean = word.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !clean.isEmpty else { return }

        let count = (sessionListenCounters[clean] ?? 0) + 1
        sessionListenCounters[clean] = count

        if count >= 2 {
            addOrUpdateWeakWord(
                word: clean,
                reading: reading,
                meaning: meaning,
                reason: "Replayed \(count) times",
                incrementListen: true
            )
        }
    }

    /// Record start of dwelling on a word/card
    public func startDwell(word: String) {
        let clean = word.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !clean.isEmpty else { return }
        wordDwellStartTimes[clean] = Date()
    }

    /// Record end of dwelling on a word/card (if dwell > 4.0s -> flagged)
    public func endDwell(word: String, reading: String = "", meaning: String = "") {
        let clean = word.trimmingCharacters(in: .whitespacesAndNewlines)
        guard let start = wordDwellStartTimes[clean] else { return }
        wordDwellStartTimes.removeValue(forKey: clean)

        let duration = Date().timeIntervalSince(start)
        if duration >= 4.0 {
            addOrUpdateWeakWord(
                word: clean,
                reading: reading,
                meaning: meaning,
                reason: String(format: "Hesitated %.1fs", duration),
                dwellSec: duration
            )
        }
    }

    /// Record a quiz or dialogue mistake
    public func recordMistake(word: String, reading: String = "", meaning: String = "") {
        let clean = word.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !clean.isEmpty else { return }

        addOrUpdateWeakWord(
            word: clean,
            reading: reading,
            meaning: meaning,
            reason: "Quiz mistake, needs review",
            incrementMistake: true
        )
    }

    public func markMastered(word: String) {
        if let idx = weakWords.firstIndex(where: { $0.word == word }) {
            weakWords[idx].isMastered = true
            GamificationService.shared.addRewards(tp: 5, exp: 10)
            saveWeakWords()
        }
    }

    public func removeWeakWord(word: String) {
        weakWords.removeAll(where: { $0.word == word })
        saveWeakWords()
    }

    private func addOrUpdateWeakWord(
        word: String,
        reading: String,
        meaning: String,
        reason: String,
        incrementListen: Bool = false,
        dwellSec: Double = 0.0,
        incrementMistake: Bool = false
    ) {
        if let idx = weakWords.firstIndex(where: { $0.word == word }) {
            var item = weakWords[idx]
            if incrementListen { item.listenCount += 1 }
            if dwellSec > 0 { item.dwellSeconds += dwellSec }
            if incrementMistake { item.mistakeCount += 1 }
            item.reason = reason
            item.isMastered = false // Re-activate for review
            weakWords[idx] = item
        } else {
            let romaji = JapaneseWordSegmenter.shared.transliterateToRomaji(reading.isEmpty ? word : reading)
            let newItem = WeakWordItem(
                word: word,
                reading: reading,
                romaji: romaji,
                meaning: meaning,
                reason: reason,
                listenCount: incrementListen ? 2 : 1,
                dwellSeconds: dwellSec,
                mistakeCount: incrementMistake ? 1 : 0
            )
            weakWords.insert(newItem, at: 0)
        }
        saveWeakWords()
    }

    public var activeWeakWords: [WeakWordItem] {
        return weakWords.filter { !$0.isMastered }
    }

    public var masteredCount: Int {
        return weakWords.filter { $0.isMastered }.count
    }

    private func saveWeakWords() {
        if let data = try? JSONEncoder().encode(weakWords) {
            UserDefaults.standard.set(data, forKey: storageKey)
        }
    }

    private func loadWeakWords() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let list = try? JSONDecoder().decode([WeakWordItem].self, from: data) {
            self.weakWords = list
        }
    }
}
