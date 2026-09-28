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
    public var onSpeechFinished: (() -> Void)?

    @Published public var isSpeaking: Bool = false
    @Published public var currentSpeakingText: String? = nil
    @Published public var audioPowerLevels: [CGFloat] = [0.2, 0.4, 0.7, 0.5, 0.3]
    @Published public var currentAmbience: TokyoAmbienceType = .none
    @Published public var useApplePCCEnhancedVoice: Bool = true

    private override init() {
        super.init()
        synthesizer.delegate = self
        setupAudioSession()
        prewarmJapaneseVoice()
    }

    public func setupAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try session.setActive(true)
        } catch {
            print("AudioSession setup warning: \(error)")
        }
    }

    private func prewarmJapaneseVoice() {
        speechQueue.async {
            self.cachedJapaneseVoice = TokyoProsodyEngine.findOptimalJapaneseNeuralVoice()
        }
    }

    public func speak(
        text: String,
        style: JapaneseVoiceStyle = .dailyConversational,
        rate: Float? = nil,
        pitch: Float? = nil,
        onFinished: (() -> Void)? = nil
    ) {
        let cleanText = text.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !cleanText.isEmpty else {
            onFinished?()
            return
        }

        setupAudioSession()

        // Stop previous immediately
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }

        self.onSpeechFinished = onFinished
        self.currentSpeakingText = cleanText
        self.isSpeaking = true
        startWaveformSimulation()

        speechQueue.async { [weak self] in
            guard let self = self else { return }

            // Apply Tokyo Prosody Segmentation
            let prosodyText = TokyoProsodyEngine.formatProsodyText(cleanText, style: style)
            let settings = TokyoProsodyEngine.prosodySettings(for: style)

            let utterance = AVSpeechUtterance(string: prosodyText)
            utterance.voice = self.cachedJapaneseVoice ?? TokyoProsodyEngine.findOptimalJapaneseNeuralVoice()
            utterance.rate = rate ?? settings.rate
            utterance.pitchMultiplier = pitch ?? settings.pitch
            utterance.volume = 1.0
            utterance.preUtteranceDelay = settings.preDelay
            utterance.postUtteranceDelay = settings.postDelay

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
            let callback = self.onSpeechFinished
            self.onSpeechFinished = nil
            callback?()
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
            let callback = self.onSpeechFinished
            self.onSpeechFinished = nil
            callback?()
        }
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
            self.stopWaveformSimulation()
            let callback = self.onSpeechFinished
            self.onSpeechFinished = nil
            callback?()
        }
    }
}
