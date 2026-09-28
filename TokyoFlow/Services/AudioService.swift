import Foundation
import AVFoundation
import AudioToolbox
import Combine

public enum TokyoAmbienceType: String, CaseIterable, Identifiable {
    case none = "None"
    case yamanoteTrain = "JR Yamanote Line"
    case kombiniStore = "FamilyMart Chime"
    case izakayaBGM = "Shinjuku Izakaya"
    case tokyoRain = "Shibuya Rain"
    case templeZen = "Asakusa Temple"

    public var id: String { rawValue }

    public var icon: String {
        switch self {
        case .none: return "speaker.slash"
        case .yamanoteTrain: return "tram.fill"
        case .kombiniStore: return "cart.fill"
        case .izakayaBGM: return "wineglass.fill"
        case .tokyoRain: return "cloud.rain.fill"
        case .templeZen: return "bell.fill"
        }
    }
}

public class AudioService: NSObject, ObservableObject, AVSpeechSynthesizerDelegate {
    public static let shared = AudioService()

    private let synthesizer = AVSpeechSynthesizer()
    private let speechQueue = DispatchQueue(label: "com.tokyoflow.speechQueue", qos: .userInitiated)
    private var cachedJapaneseVoice: AVSpeechSynthesisVoice?
    private var waveformTimer: Timer?

    @Published public var isSpeaking: Bool = false
    @Published public var currentSpeakingText: String? = nil
    @Published public var audioPowerLevels: [CGFloat] = [0.2, 0.4, 0.7, 0.5, 0.3]
    @Published public var currentAmbience: TokyoAmbienceType = .none
    @Published public var useApplePCCEnhancedVoice: Bool = true

    private override init() {
        super.init()
        synthesizer.delegate = self
        setupAudioSessionAsync()
        prewarmJapaneseVoice()
    }

    private func setupAudioSessionAsync() {
        speechQueue.async {
            do {
                let session = AVAudioSession.sharedInstance()
                try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
                try session.setActive(true, options: .notifyOthersOnDeactivation)
            } catch {
                print("AudioSession setup warning: \(error)")
            }
        }
    }

    private func prewarmJapaneseVoice() {
        speechQueue.async {
            // Priority: Enhanced quality Japanese voices (Kyoko / Otoya / Siri)
            let allVoices = AVSpeechSynthesisVoice.speechVoices()
            let jpVoices = allVoices.filter { $0.language.hasPrefix("ja") }

            // Look for enhanced or premium voice first
            if let enhanced = jpVoices.first(where: { $0.quality == .enhanced || $0.identifier.contains("enhanced") || $0.identifier.contains("premium") }) {
                self.cachedJapaneseVoice = enhanced
            } else if let kyoko = jpVoices.first(where: { $0.name.contains("Kyoko") || $0.name.contains("Otoya") }) {
                self.cachedJapaneseVoice = kyoko
            } else {
                self.cachedJapaneseVoice = AVSpeechSynthesisVoice(language: "ja-JP") ?? AVSpeechSynthesisVoice(language: "ja")
            }
        }
    }

    public func speak(text: String, rate: Float = 0.51, pitch: Float = 1.02) {
        let cleanText = text.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !cleanText.isEmpty else { return }

        // Stop previous immediately
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }

        currentSpeakingText = cleanText
        isSpeaking = true
        startWaveformSimulation()

        speechQueue.async { [weak self] in
            guard let self = self else { return }

            let utterance = AVSpeechUtterance(string: cleanText)
            utterance.voice = self.cachedJapaneseVoice ?? AVSpeechSynthesisVoice(language: "ja-JP")
            utterance.rate = rate
            utterance.pitchMultiplier = pitch
            utterance.volume = 1.0
            utterance.preUtteranceDelay = 0.0
            utterance.postUtteranceDelay = 0.05

            DispatchQueue.main.async {
                self.synthesizer.speak(utterance)
            }
        }
    }

    public func stop() {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
            self.stopWaveformSimulation()
        }
    }

    public func setAmbience(_ type: TokyoAmbienceType) {
        currentAmbience = type
        if type != .none {
            AudioServicesPlaySystemSound(1057)
        }
    }

    private func startWaveformSimulation() {
        waveformTimer?.invalidate()
        waveformTimer = Timer.scheduledTimer(withTimeInterval: 0.08, repeats: true) { [weak self] _ in
            guard let self = self, self.isSpeaking else { return }
            self.audioPowerLevels = (0..<5).map { _ in CGFloat.random(in: 0.25...0.98) }
        }
    }

    private func stopWaveformSimulation() {
        waveformTimer?.invalidate()
        waveformTimer = nil
        audioPowerLevels = [0.2, 0.2, 0.2, 0.2, 0.2]
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
            self.stopWaveformSimulation()
        }
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
            self.stopWaveformSimulation()
        }
    }
}
