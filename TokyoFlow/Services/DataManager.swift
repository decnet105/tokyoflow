import Foundation

public class DataManager: ObservableObject {
    public static let shared = DataManager()

    @Published public var scenarios: [Scenario] = []
    @Published public var mangaLessons: [MangaLesson] = []
    @Published public var announcements: [Announcement] = []
    @Published public var dojoBattles: [DojoBattle] = []
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String? = nil

    private var scenarioMap: [String: Scenario] = [:]
    private var mangaMap: [String: MangaLesson] = [:]
    private var isLoaded: Bool = false
    private var isLoadingData: Bool = false
    private let queue = DispatchQueue(label: "com.tokyoflow.datamanager", qos: .userInitiated)

    private init() {
        loadAllDataAsync()
    }

    public func loadAllDataAsync() {
        guard !isLoaded && !isLoadingData else { return }
        isLoadingData = true

        queue.async {
            let sc: [Scenario] = self.loadJson(filename: "scenarios") ?? []
            let mg: [MangaLesson] = self.loadJson(filename: "manga_lessons") ?? []
            let an: [Announcement] = self.loadJson(filename: "announcements") ?? []
            let dj: [DojoBattle] = self.loadJson(filename: "dojo_battles") ?? []

            var sMap: [String: Scenario] = [:]
            for s in sc { sMap[s.id] = s }

            var mMap: [String: MangaLesson] = [:]
            for m in mg { mMap[m.id] = m }

            DispatchQueue.main.async {
                self.scenarios = sc
                self.mangaLessons = mg
                self.announcements = an
                self.dojoBattles = dj
                self.scenarioMap = sMap
                self.mangaMap = mMap
                self.isLoading = false
                self.isLoaded = true
                self.isLoadingData = false
            }
        }
    }

    public func loadAllData() {
        isLoading = true
        scenarios = loadJson(filename: "scenarios") ?? []
        mangaLessons = loadJson(filename: "manga_lessons") ?? []
        announcements = loadJson(filename: "announcements") ?? []
        dojoBattles = loadJson(filename: "dojo_battles") ?? []
        
        var sMap: [String: Scenario] = [:]
        for s in scenarios { sMap[s.id] = s }
        self.scenarioMap = sMap

        var mMap: [String: MangaLesson] = [:]
        for m in mangaLessons { mMap[m.id] = m }
        self.mangaMap = mMap

        isLoading = false
    }

    private func loadJson<T: Decodable>(filename: String) -> T? {
        let bundles = [Bundle.main, Bundle(for: DataManager.self)]
        
        for bundle in bundles {
            if let url = bundle.url(forResource: filename, withExtension: "json") {
                do {
                    let data = try Data(contentsOf: url)
                    let decoder = JSONDecoder()
                    return try decoder.decode(T.self, from: data)
                } catch {
                    print("Error decoding \(filename).json from bundle: \(error)")
                }
            }
        }

        // Fallback to relative path lookup for tests/previews
        let localPath = "TokyoFlow/Resources/\(filename).json"
        let fileURL = URL(fileURLWithPath: localPath)
        if FileManager.default.fileExists(atPath: fileURL.path) {
            do {
                let data = try Data(contentsOf: fileURL)
                let decoder = JSONDecoder()
                return try decoder.decode(T.self, from: data)
            } catch {
                print("Error decoding \(filename).json from file: \(error)")
            }
        }

        return nil
    }

    public func scenario(for id: String) -> Scenario? {
        return scenarioMap[id] ?? scenarios.first { $0.id == id }
    }

    public func mangaLesson(for id: String) -> MangaLesson? {
        return mangaMap[id] ?? mangaLessons.first { $0.id == id }
    }
}
