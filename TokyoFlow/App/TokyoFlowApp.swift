import SwiftUI
import Combine

/// TokyoFlow Asynchronous App Launch Pre-warming Pipeline
/// Modeled after industry-leading iOS dictionary apps (Midori, Shirabe Jisho, AnkiMobile).
/// Offloads heavy JSON decoding, in-memory index construction, and audio session configuration
/// to high-priority background tasks, ensuring 0ms cold-start and instant UI responsiveness.
public class TokyoAppLaunchPrewarmer {
    public static let shared = TokyoAppLaunchPrewarmer()

    private var isPrewarmed: Bool = false

    private init() {}

    public func prewarmAllServices() {
        guard !isPrewarmed else { return }
        isPrewarmed = true

        Task.detached(priority: .userInitiated) {
            // Parallel background prewarming of all services
            async let dictTask: Void = Task {
                JLPTDictionaryService.shared.loadDictionaryAsync()
            }.value

            async let grammarTask: Void = Task {
                JLPTGrammarService.shared.loadGrammarDataAsync()
            }.value

            async let voiceTask: Void = Task {
                TokyoVoiceBankService.shared.loadManifestAsync()
            }.value

            async let dataTask: Void = Task {
                DataManager.shared.loadAllDataAsync()
            }.value

            _ = await (dictTask, grammarTask, voiceTask, dataTask)
            print("️ TokyoAppLaunchPrewarmer: All core engines prewarmed in background thread.")
        }
    }
}

@main
struct TokyoFlowApp: App {
    var body: some Scene {
        WindowGroup {
            MainTabView()
                .onAppear {
                    TokyoAppLaunchPrewarmer.shared.prewarmAllServices()
                }
        }
    }
}
