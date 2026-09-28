import Foundation
import AVFoundation
import Combine

public class TokyoVoiceBankService: NSObject, ObservableObject, AVAudioPlayerDelegate {
    public static let shared = TokyoVoiceBankService()

    private var manifest: [String: String] = [:]
    private var normalizedIndex: [String: String] = [:]
    private var queryCache = NSCache<NSString, NSString>()
    private var audioUrlCache = NSCache<NSString, NSURL>()
    
    private var audioPlayer: AVAudioPlayer?
    private var onAudioFinished: (() -> Void)?
    private let queue = DispatchQueue(label: "com.tokyoflow.voicebank", qos: .userInitiated)
    private var isAudioSessionConfigured: Bool = false

    @Published public var isPlayingNativeAudio: Bool = false
    @Published public var currentPlayingKey: String? = nil

    private override init() {
        super.init()
        loadManifest()
        prewarmAudioSessionAsync()
    }

    private func prewarmAudioSessionAsync() {
        queue.async {
            do {
                let session = AVAudioSession.sharedInstance()
                try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
                try session.setActive(true)
                self.isAudioSessionConfigured = true
            } catch {
                print("ℹ️ TokyoVoiceBankService: AudioSession prewarm notice: \(error)")
            }
        }
    }

    private func loadManifest() {
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
                buildFastIndex(from: dict)
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
            buildFastIndex(from: dict)
            print("✅ TokyoVoiceBankService: Loaded \(dict.count) native voice keys from DevPath.")
        }
    }

    private func buildFastIndex(from dict: [String: String]) {
        var fastMap: [String: String] = Dictionary(minimumCapacity: dict.count * 3)
        for (k, v) in dict {
            fastMap[k] = v
            let norm = normalizeKey(k)
            if fastMap[norm] == nil { fastMap[norm] = v }
            let lower = k.lowercased()
            if fastMap[lower] == nil { fastMap[lower] = v }
            let normLower = norm.lowercased()
            if fastMap[normLower] == nil { fastMap[normLower] = v }
        }
        self.normalizedIndex = fastMap
        self.queryCache.removeAllObjects()
    }

    public func cleanFuriganaKanji(_ text: String) -> String {
        var result = text
        let regex = try? NSRegularExpression(pattern: "[^{}]+{([^{}]+)}")
        if let regex = regex {
            result = regex.stringByReplacingMatches(in: text, range: NSRange(text.startIndex..., in: text), withTemplate: "$1")
        }
        return result
    }

    public func cleanFuriganaReading(_ text: String) -> String {
        var result = text
        let regex = try? NSRegularExpression(pattern: "([^{}]+){[^{}]+}")
        if let regex = regex {
            result = regex.stringByReplacingMatches(in: text, range: NSRange(text.startIndex..., in: text), withTemplate: "$1")
        }
        return result
    }

    public func normalizeKey(_ text: String) -> String {
        return text
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
            .replacingOccurrences(of: "[", with: "")
            .replacingOccurrences(of: "]", with: "")
            .replacingOccurrences(of: "【", with: "")
            .replacingOccurrences(of: "】", with: "")
            .replacingOccurrences(of: "#", with: "")
            .replacingOccurrences(of: "　", with: "")
            .trimmingCharacters(in: .whitespacesAndNewlines)
    }

    public func findAudioFilename(for text: String) -> String? {
        let clean = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if clean.isEmpty { return nil }

        let nsKey = clean as NSString
        if let cached = queryCache.object(forKey: nsKey) {
            return (cached as String).isEmpty ? nil : (cached as String)
        }

        // 1. Direct O(1) exact match
        if let fn = manifest[clean] ?? normalizedIndex[clean] {
            queryCache.setObject(fn as NSString, forKey: nsKey)
            return fn
        }

        // 2. Normalized O(1) match
        let norm = normalizeKey(clean)
        if let fn = normalizedIndex[norm] {
            queryCache.setObject(fn as NSString, forKey: nsKey)
            return fn
        }

        // 3. Furigana kanji-extracted O(1) match
        let fk = normalizeKey(cleanFuriganaKanji(clean))
        if let fn = normalizedIndex[fk] {
            queryCache.setObject(fn as NSString, forKey: nsKey)
            return fn
        }

        // 4. Furigana kana-reading O(1) match
        let fr = normalizeKey(cleanFuriganaReading(clean))
        if let fn = normalizedIndex[fr] {
            queryCache.setObject(fn as NSString, forKey: nsKey)
            return fn
        }

        // 5. Lowercased O(1) match
        let lower = clean.lowercased()
        if let fn = normalizedIndex[lower] {
            queryCache.setObject(fn as NSString, forKey: nsKey)
            return fn
        }

        // 6. Slash-delimited composite expression match
        if clean.contains("/") {
            for part in clean.split(separator: "/") {
                let pStr = String(part).trimmingCharacters(in: .whitespacesAndNewlines)
                if let fn = normalizedIndex[pStr] ?? normalizedIndex[normalizeKey(pStr)] {
                    queryCache.setObject(fn as NSString, forKey: nsKey)
                    return fn
                }
            }
        }

        // 7. Tokenized component match
        let tokens = clean.components(separatedBy: CharacterSet(charactersIn: " ()（）[]【】/~〜・,、:：\n\t　 ")).filter { !$0.isEmpty }
        for tok in tokens {
            if let fn = normalizedIndex[tok] ?? normalizedIndex[normalizeKey(tok)] {
                queryCache.setObject(fn as NSString, forKey: nsKey)
                return fn
            }
        }

        // Cache negative result
        queryCache.setObject("" as NSString, forKey: nsKey)
        return nil
    }

    public func hasNativeAudio(for text: String) -> Bool {
        return findAudioFilename(for: text) != nil
    }

    public func audioURL(for filename: String) -> URL? {
        let nsKey = filename as NSString
        if let cached = audioUrlCache.object(forKey: nsKey) {
            return cached as URL
        }

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
                audioUrlCache.setObject(url as NSURL, forKey: nsKey)
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
            if !isAudioSessionConfigured {
                let session = AVAudioSession.sharedInstance()
                try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
                try session.setActive(true)
                self.isAudioSessionConfigured = true
            }

            let player = try AVAudioPlayer(contentsOf: url)
            player.delegate = self
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

    public func playPhraseOrFallback(key: String, fallbackText: String) {
        if !playNativeAudio(text: key) {
            if !playNativeAudio(text: fallbackText) {
                AudioService.shared.speak(text: fallbackText)
            }
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
