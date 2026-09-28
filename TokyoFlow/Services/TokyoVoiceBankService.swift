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
        // 1. Check Bundle resources first
        let possibleUrls = [
            Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json", subdirectory: "VoiceBank"),
            Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json"),
            Bundle.main.resourceURL?.appendingPathComponent("VoiceBank/voice_bank_manifest.json"),
            Bundle.main.bundleURL.appendingPathComponent("VoiceBank/voice_bank_manifest.json")
        ].compactMap { $0 }

        for url in possibleUrls {
            if FileManager.default.fileExists(atPath: url.path),
               let data = try? Data(contentsOf: url),
               let dict = try? JSONSerialization.jsonObject(with: data) as? [String: String] {
                self.manifest = dict
                print("✅ TokyoVoiceBankService: Successfully loaded \(dict.count) native voice keys from Bundle.")
                return
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
        let clean = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if clean.isEmpty { return nil }

        // 1. Direct exact match
        if let fn = manifest[clean] { return fn }

        // 2. Normalized match (stripped of punctuation/quotes)
        let norm = normalizeKey(clean)
        if let fn = manifest[norm] { return fn }

        // 3. Lowercased romaji / ASCII match
        let lower = clean.lowercased()
        if let fn = manifest[lower] { return fn }

        // 4. Tokenized component match (e.g. "ありがとう (Thank you)" -> "ありがとう")
        let tokens = clean.components(separatedBy: CharacterSet(charactersIn: " ()（）[]【】/~〜・,、:：")).filter { !$0.isEmpty }
        for tok in tokens {
            if let fn = manifest[tok] ?? manifest[normalizeKey(tok)] ?? manifest[tok.lowercased()] {
                return fn
            }
        }

        // 5. Prefix match for full phrases (e.g. "すみません、山手線..." matching sentence key)
        if clean.count >= 4 {
            for (key, fn) in manifest {
                if key.count >= 4 && (clean.hasPrefix(key) || norm.hasPrefix(key)) {
                    return fn
                }
            }
        }

        return nil
    }

    public func hasNativeAudio(for text: String) -> Bool {
        return findAudioFilename(for: text) != nil
    }

    public func audioURL(for filename: String) -> URL? {
        let bareName = (filename as NSString).deletingPathExtension
        let ext = (filename as NSString).pathExtension

        let candidates = [
            Bundle.main.url(forResource: bareName, withExtension: ext, subdirectory: "VoiceBank"),
            Bundle.main.url(forResource: filename, withExtension: nil, subdirectory: "VoiceBank"),
            Bundle.main.url(forResource: bareName, withExtension: ext),
            Bundle.main.url(forResource: filename, withExtension: nil),
            Bundle.main.resourceURL?.appendingPathComponent("VoiceBank/\(filename)"),
            Bundle.main.bundleURL.appendingPathComponent("VoiceBank/\(filename)"),
            URL(fileURLWithPath: "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/Audio/VoiceBank/\(filename)")
        ].compactMap { $0 }

        for url in candidates {
            if FileManager.default.fileExists(atPath: url.path) {
                return url
            }
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
            // Only adjust rate if it's explicitly within a standard playback speed range (0.75x - 2.0x)
            if let r = rate, r >= 0.7 && r <= 2.0 {
                player.enableRate = true
                player.rate = r
            } else {
                player.enableRate = false
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
