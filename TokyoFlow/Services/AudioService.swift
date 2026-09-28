import Foundation
import AVFoundation
import AudioToolbox

public class AudioService: NSObject, ObservableObject, AVSpeechSynthesizerDelegate {
    public static let shared = AudioService()

    private let synthesizer = AVSpeechSynthesizer()
    private var audioEngine: AVAudioEngine?
    private var tonePlayerNode: AVAudioPlayerNode?

    @Published public var isSpeaking: Bool = false
    @Published public var currentSpeakingText: String? = nil

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
        }

        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP") ?? AVSpeechSynthesisVoice(language: "ja")
        utterance.rate = rate
        utterance.pitchMultiplier = pitch
        utterance.volume = 1.0

        currentSpeakingText = text
        isSpeaking = true
        synthesizer.speak(utterance)
    }

    public func stop() {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        isSpeaking = false
        currentSpeakingText = nil
    }

    // Play synthesized train/store melody frequencies
    public func playTone(frequency: Double, duration: Double) {
        let systemSoundId: SystemSoundID = 1057 // standard clean UI tick
        AudioServicesPlaySystemSound(systemSoundId)
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
        }
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.currentSpeakingText = nil
        }
    }
}
