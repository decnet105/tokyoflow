import Foundation
import AVFoundation
import AudioToolbox
import Combine

public enum TokyoAmbienceType: String, CaseIterable, Identifiable {
    case none = "None (Silent)"
    case yamanote = "Yamanote Train Hum (山手線車内)"
    case izakaya = "Izakaya Night Chatter (居酒屋の賑わい)"
    case kombini = "Kombini Background (コンビニ店内)"
    case rain = "Tokyo Rainy Alley (雨の路地裏)"

    public var id: String { rawValue }
    public var icon: String {
        switch self {
        case .none: return "speaker.slash"
        case .yamanote: return "tram.fill"
        case .izakaya: return "fork.knife"
        case .kombini: return "cart.fill"
        case .rain: return "cloud.rain.fill"
        }
    }
}

public class AudioService: NSObject, ObservableObject, AVSpeechSynthesizerDelegate {
    public static let shared = AudioService()

    private let synthesizer = AVSpeechSynthesizer()
    private var waveformTimer: Timer?

    @Published public var isSpeaking: Bool = false
    @Published public var currentSpeakingText: String? = nil
    @Published public var audioPowerLevels: [CGFloat] = [0.2, 0.4, 0.7, 0.5, 0.3]
    @Published public var currentAmbience: TokyoAmbienceType = .none

    private override init() {
        super.init()
        synthesizer.delegate = self
        setupAudioSession()
    }

    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Failed to configure AVAudioSession: \(error)")
        }
    }

    public func speak(text: String, rate: Float = 0.50, pitch: Float = 1.0) {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
            stopWaveformSimulation()
        }

        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP") ?? AVSpeechSynthesisVoice(language: "ja")
        utterance.rate = rate
        utterance.pitchMultiplier = pitch
        utterance.volume = 1.0

        currentSpeakingText = text
        isSpeaking = true
        startWaveformSimulation()
        synthesizer.speak(utterance)
    }

    public func stop() {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        isSpeaking = false
        currentSpeakingText = nil
        stopWaveformSimulation()
    }

    public func setAmbience(_ type: TokyoAmbienceType) {
        currentAmbience = type
        if type != .none {
            // Play ambient confirmation chime
            AudioServicesPlaySystemSound(1057)
        }
    }

    private func startWaveformSimulation() {
        waveformTimer?.invalidate()
        waveformTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            guard let self = self, self.isSpeaking else { return }
            self.audioPowerLevels = (0..<5).map { _ in CGFloat.random(in: 0.15...0.95) }
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
