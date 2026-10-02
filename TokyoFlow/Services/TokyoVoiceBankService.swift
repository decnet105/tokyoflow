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
    @Published public var playbackProgress: Double = 0.0
    @Published public var currentTime: Double = 0.0
    @Published public var currentDuration: Double = 0.0
    private var progressTimer: Timer?

    private var isLoaded: Bool = false
    private var isLoading: Bool = false

    private override init() {
        super.init()
        // Asynchronous background pre-warming for instantaneous cold start
        loadManifestAsync()
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

    public func loadManifestAsync() {
        guard !isLoaded && !isLoading else { return }
        isLoading = true
        queue.async {
            self.loadManifest()
        }
    }

    public func loadManifest() {
        guard !isLoaded else { return }
        
        let possibleUrls = [
            Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json"),
            Bundle.main.url(forResource: "voice_bank_manifest", withExtension: "json", subdirectory: "VoiceBank"),
            Bundle.main.bundleURL.appendingPathComponent("voice_bank_manifest.json"),
            Bundle.main.resourceURL?.appendingPathComponent("voice_bank_manifest.json"),
            Bundle.main.bundleURL.appendingPathComponent("VoiceBank/voice_bank_manifest.json"),
            Bundle.main.resourceURL?.appendingPathComponent("VoiceBank/voice_bank_manifest.json")
        ].compactMap { $0 }

        for url in possibleUrls {
            if FileManager.default.fileExists(atPath: url.path),
               let data = try? Data(contentsOf: url),
               let dict = try? JSONSerialization.jsonObject(with: data) as? [String: String] {
                self.manifest = dict
                buildFastIndex(from: dict)
                self.isLoaded = true
                self.isLoading = false
                print(" TokyoVoiceBankService: Successfully loaded \(dict.count) native voice keys from Bundle.")
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
            self.isLoaded = true
            self.isLoading = false
            print(" TokyoVoiceBankService: Loaded \(dict.count) native voice keys from DevPath.")
        } else {
            self.isLoading = false
        }
    }

    private static let ignoredChars: Set<Character> = Set("。、！？.,!?\"'「」『』〜～()（）[]【】 \t\n\r　")

    private func buildFastIndex(from dict: [String: String]) {
        var fastMap: [String: String] = Dictionary(minimumCapacity: dict.count * 2)
        for (k, v) in dict {
            fastMap[k] = v
            let norm = normalizeKey(k)
            if norm != k && fastMap[norm] == nil {
                fastMap[norm] = v
            }
            let lower = k.lowercased()
            if lower != k && fastMap[lower] == nil {
                fastMap[lower] = v
            }
        }
        self.normalizedIndex = fastMap
    }

    private func normalizeKey(_ key: String) -> String {
        return String(key.filter { !Self.ignoredChars.contains($0) })
    }

    private func cleanFuriganaKanji(_ text: String) -> String {
        var result = ""
        result.reserveCapacity(text.count)
        var depth = 0
        for ch in text {
            if ch == "(" || ch == "（" {
                depth += 1
            } else if ch == ")" || ch == "）" {
                if depth > 0 { depth -= 1 }
            } else if depth == 0 {
                result.append(ch)
            }
        }
        return result
    }

    private static let furiganaReadingRegex: NSRegularExpression? = {
        return try? NSRegularExpression(pattern: "([一-龯々]+)[（(]([ぁ-んァ-ンー]+)[）)]", options: [])
    }()

    private func cleanFuriganaReading(_ text: String) -> String {
        guard let regex = Self.furiganaReadingRegex else { return text }
        let nsString = text as NSString
        let range = NSRange(location: 0, length: nsString.length)
        return regex.stringByReplacingMatches(in: text, options: [], range: range, withTemplate: "$2")
    }

    public func findAudioFilename(for text: String, reading: String? = nil) -> String? {
        let clean = text.trimmingCharacters(in: .whitespacesAndNewlines)
        if clean.isEmpty {
            if let r = reading?.trimmingCharacters(in: .whitespacesAndNewlines), !r.isEmpty {
                return findAudioFilename(for: r, reading: nil)
            }
            return nil
        }

        let nsKey = (reading != nil ? "\(clean)_\(reading!)" : clean) as NSString
        if let cached = queryCache.object(forKey: nsKey) {
            return (cached as String).isEmpty ? nil : (cached as String)
        }

        // Helper to resolve single string key
        let resolveSingle: (String) -> String? = { target in
            let c = target.trimmingCharacters(in: .whitespacesAndNewlines)
            if c.isEmpty { return nil }

            // 1. Direct O(1) exact match
            if let fn = self.manifest[c] ?? self.normalizedIndex[c] { return fn }

            // 2. Normalized O(1) match
            let norm = self.normalizeKey(c)
            if let fn = self.normalizedIndex[norm] { return fn }

            // 3. Furigana kanji-extracted O(1) match
            let fk = self.normalizeKey(self.cleanFuriganaKanji(c))
            if let fn = self.normalizedIndex[fk] { return fn }

            // 4. Furigana kana-reading O(1) match
            let fr = self.normalizeKey(self.cleanFuriganaReading(c))
            if let fn = self.normalizedIndex[fr] { return fn }

            // 5. Lowercased O(1) match
            let lower = c.lowercased()
            if let fn = self.normalizedIndex[lower] { return fn }

            // 6. Slash-delimited composite expression match (e.g., "A / B" patterns)
            if c.contains("/") {
                for part in c.split(separator: "/") {
                    let pStr = String(part).trimmingCharacters(in: .whitespacesAndNewlines)
                    if let fn = self.manifest[pStr] ?? self.normalizedIndex[pStr] ?? self.normalizedIndex[self.normalizeKey(pStr)] {
                        return fn
                    }
                }
            }

            // 7. Single-token symbol-stripped match ONLY (never return a 1-word fragment for a multi-word sentence)
            let tokens = c.components(separatedBy: CharacterSet(charactersIn: " ()（）[]【】/~〜・,、:：\n\t　 ")).filter { !$0.isEmpty }
            if tokens.count == 1, let tok = tokens.first {
                if let fn = self.manifest[tok] ?? self.normalizedIndex[tok] ?? self.normalizedIndex[self.normalizeKey(tok)] {
                    return fn
                }
            }
            return nil
        }

        if let match = resolveSingle(clean) {
            queryCache.setObject(match as NSString, forKey: nsKey)
            return match
        }

        // Secondary fallback: Try reading directly if provided
        if let r = reading?.trimmingCharacters(in: .whitespacesAndNewlines), !r.isEmpty, r != clean {
            if let match = resolveSingle(r) {
                queryCache.setObject(match as NSString, forKey: nsKey)
                return match
            }
        }

        // Cache negative result
        queryCache.setObject("" as NSString, forKey: nsKey)
        return nil
    }

    public func hasNativeAudio(for text: String, reading: String? = nil) -> Bool {
        return findAudioFilename(for: text, reading: reading) != nil
    }

    public func audioURL(for filename: String) -> URL? {
        let nsKey = filename as NSString
        if let cached = audioUrlCache.object(forKey: nsKey) {
            return cached as URL
        }

        let bareName = (filename as NSString).deletingPathExtension
        let ext = (filename as NSString).pathExtension

        let candidates = [
            Bundle.main.url(forResource: bareName, withExtension: ext),
            Bundle.main.url(forResource: filename, withExtension: nil),
            Bundle.main.bundleURL.appendingPathComponent(filename),
            Bundle.main.resourceURL?.appendingPathComponent(filename),
            Bundle.main.url(forResource: bareName, withExtension: ext, subdirectory: "VoiceBank"),
            Bundle.main.url(forResource: filename, withExtension: nil, subdirectory: "VoiceBank"),
            Bundle.main.bundleURL.appendingPathComponent("VoiceBank/\(filename)"),
            Bundle.main.resourceURL?.appendingPathComponent("VoiceBank/\(filename)"),
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
        reading: String? = nil,
        rate: Float? = nil,
        onFinished: (() -> Void)? = nil
    ) -> Bool {
        guard let filename = findAudioFilename(for: text, reading: reading),
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
            self.currentDuration = player.duration
            self.currentTime = 0.0
            self.playbackProgress = 0.0

            player.play()
            startProgressTracking()
            return true
        } catch {
            print("️ TokyoVoiceBankService: Playback error for \(filename): \(error)")
            return false
        }
    }

    public var activePlayerTime: Double {
        return audioPlayer?.currentTime ?? 0.0
    }

    public var activePlayerDuration: Double {
        return audioPlayer?.duration ?? 0.0
    }

    public var activePlayerIsPlaying: Bool {
        return audioPlayer?.isPlaying ?? false
    }

    private func startProgressTracking() {
        stopProgressTracking()
        DispatchQueue.main.async {
            // High-frequency 100Hz (10ms) progress update for true millisecond-level live karaoke tracking
            let timer = Timer(timeInterval: 0.01, repeats: true) { [weak self] _ in
                guard let self = self, let player = self.audioPlayer, player.isPlaying else { return }
                self.currentTime = player.currentTime
                let dur = player.duration
                self.currentDuration = dur
                if dur > 0 {
                    self.playbackProgress = min(1.0, max(0.0, player.currentTime / dur))
                }
            }
            RunLoop.main.add(timer, forMode: .common)
            self.progressTimer = timer
        }
    }

    private func stopProgressTracking() {
        progressTimer?.invalidate()
        progressTimer = nil
    }

    /// Plays native phrase with strict zero-TTS fallback
    public func playPhraseOrFallback(key: String, fallbackText: String) {
        if !playNativeAudio(text: key) {
            if !playNativeAudio(text: fallbackText) {
                let normKey = normalizeKey(key)
                if !playNativeAudio(text: normKey) {
                    let normFallback = normalizeKey(fallbackText)
                    if !playNativeAudio(text: normFallback) {
                        print("️ TokyoVoiceBankService: Native audio key not found: \(key) / \(fallbackText)")
                    }
                }
            }
        }
    }

    public func stop() {
        stopProgressTracking()
        if let player = audioPlayer, player.isPlaying {
            player.stop()
        }
        audioPlayer = nil
        isPlayingNativeAudio = false
        currentPlayingKey = nil
        playbackProgress = 0.0
        currentTime = 0.0
        let cb = onAudioFinished
        onAudioFinished = nil
        cb?()
    }

    // MARK: - AVAudioPlayerDelegate
    public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.stopProgressTracking()
            self.isPlayingNativeAudio = false
            self.currentPlayingKey = nil
            self.playbackProgress = 1.0
            self.audioPlayer = nil
            let cb = self.onAudioFinished
            self.onAudioFinished = nil
            cb?()
        }
    }
}
