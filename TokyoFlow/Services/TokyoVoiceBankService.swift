import Foundation
import AVFoundation
import Combine

public class TokyoVoiceBankService: NSObject, ObservableObject, AVAudioPlayerDelegate {
    public static let shared = TokyoVoiceBankService()

    private var manifest: [String: String] = [:]
    private var audioPlayer: AVAudioPlayer?
    private var onAudioFinished: (() -> Void)?
    private let queue = DispatchQueue(label: "com.tokyoflow.voicebank", qos: .userInitiated)

    @Published public var isPlayingNativeAudio: Bool = false
    @Published public var currentPlayingKey: String? = nil

    private override init() {
        super.init()
        loadManifest()
    }

    private func loadManifest() {
        // Try Bundle resources first
        if let url = Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json", subdirectory: "VoiceBank") ??
                     Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                if let dict = try JSONSerialization.jsonObject(with: data) as? [String: String] {
                    self.manifest = dict
                    print("✅ TokyoVoiceBankService: Loaded \(dict.count) native voice keys from Bundle.")
                    return
                }
            } catch {
                print("⚠️ TokyoVoiceBankService: Error parsing manifest: \(error)")
            }
        }

        // Development fallback to direct file path
        let devPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/Audio/VoiceBank/voice_bank_manifest.json"
        if FileManager.default.fileExists(atPath: devPath),
           let data = try? Data(contentsOf: URL(fileURLWithPath: devPath)),
           let dict = try? JSONSerialization.jsonObject(with: data) as? [String: String] {
            self.manifest = dict
            print("✅ TokyoVoiceBankService: Loaded \(dict.count) native voice keys from DevPath.")
        }
    }

    public func normalizeKey(_ text: String) -> String {
        let stripped = text
            .replacingOccurrences(of: "？", with: "")
            .replacingOccurrences(of: "?", with: "")
            .replacingOccurrences(of: "！", with: "")
            .replacingOccurrences(of: "!", with: "")
            .replacingOccurrences(of: "。", with: "")
            .replacingOccurrences(of: "、", with: "")
            .replacingOccurrences(of: "…", with: "")
            .replacingOccurrences(of: "〜", with: "")
            .replacingOccurrences(of: "~", with: "")
            .replacingOccurrences(of: "「", with: "")
            .replacingOccurrences(of: "」", with: "")
            .replacingOccurrences(of: "(", with: "")
            .replacingOccurrences(of: ")", with: "")
            .replacingOccurrences(of: "（", with: "")
            .replacingOccurrences(of: "）", with: "")
            .replacingOccurrences(of: "#", with: "")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        return stripped
    }

    public func findAudioFilename(for text: String) -> String? {
        // 1. Direct match
        if let fn = manifest[text] { return fn }

        // 2. Normalized match
        let norm = normalizeKey(text)
        if let fn = manifest[norm] { return fn }

        // 3. Lowercased romaji
        let lower = text.lowercased().trimmingCharacters(in: .whitespacesAndNewlines)
        if let fn = manifest[lower] { return fn }

        // 4. Tokenized component match (e.g. "いぬ (犬)" -> check "いぬ", then "犬")
        let tokens = text.components(separatedBy: CharacterSet(charactersIn: " ()（）/~〜・,、:：")).filter { !$0.isEmpty }
        for tok in tokens {
            if let fn = manifest[tok] ?? manifest[normalizeKey(tok)] ?? manifest[tok.lowercased()] {
                return fn
            }
        }

        // 5. Substring match for particles or compound sentences
        for (key, fn) in manifest {
            if !key.isEmpty && key.count >= 2 && (text.contains(key) || norm.contains(key)) {
                return fn
            }
        }

        return nil
    }

    public func hasNativeAudio(for text: String) -> Bool {
        return findAudioFilename(for: text) != nil
    }

    public func audioURL(for filename: String) -> URL? {
        if let url = Bundle.main.url(forResource: (filename as NSString).deletingPathExtension,
                                     withExtension: (filename as NSString).pathExtension,
                                     subdirectory: "VoiceBank") ??
                     Bundle.main.url(forResource: filename, withExtension: nil) {
            return url
        }

        let devPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/Audio/VoiceBank/\(filename)"
        if FileManager.default.fileExists(atPath: devPath) {
            return URL(fileURLWithPath: devPath)
        }

        return nil
    }

    @discardableResult
    public func playNativeAudio(
        text: String,
        rate: Float? = nil,
        onFinished: (() -> Void)? = nil
    ) -> Bool {
        guard let filename = findAudioFilename(for: text),
              let url = audioURL(for: filename) else {
            return false
        }

        stop()

        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try session.setActive(true)

            let player = try AVAudioPlayer(contentsOf: url)
            player.delegate = self
            if let rate = rate, rate > 0 {
                player.enableRate = true
                player.rate = rate
            }
            player.prepareToPlay()

            self.audioPlayer = player
            self.onAudioFinished = onFinished
            self.currentPlayingKey = text
            self.isPlayingNativeAudio = true

            player.play()
            return true
        } catch {
            print("⚠️ TokyoVoiceBankService: Playback error for \(filename): \(error)")
            return false
        }
    }

    public func stop() {
        if let player = audioPlayer, player.isPlaying {
            player.stop()
        }
        audioPlayer = nil
        isPlayingNativeAudio = false
        currentPlayingKey = nil
        let cb = onAudioFinished
        onAudioFinished = nil
        cb?()
    }

    // MARK: - AVAudioPlayerDelegate
    public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.isPlayingNativeAudio = false
            self.currentPlayingKey = nil
            self.audioPlayer = nil
            let cb = self.onAudioFinished
            self.onAudioFinished = nil
            cb?()
        }
    }
}
