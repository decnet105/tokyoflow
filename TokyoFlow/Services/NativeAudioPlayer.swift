import Foundation
import AVFoundation
import Combine

public class NativeAudioPlayer: NSObject, ObservableObject, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    public static let shared = NativeAudioPlayer()

    private var audioPlayer: AVAudioPlayer?
    private var progressTimer: Timer?
    private var sentenceStopTimer: Timer?
    private var audioRecorder: AVAudioRecorder?
    private var userRecordingPlayer: AVAudioPlayer?
    private var activeSentencesQueue: [NewsSentence] = []

    @Published public var isPlayingRemoteAudio: Bool = false
    @Published public var currentTimeSec: Double = 0.0
    @Published public var durationSec: Double = 0.0
    @Published public var playbackRate: Float = 1.0
    @Published public var activeSentenceId: String? = nil

    // Shadowing Microphone Recording
    @Published public var isRecordingShadowing: Bool = false
    @Published public var isPlayingUserRecording: Bool = false
    @Published public var userAudioRecordingUrl: URL? = nil
    @Published public var recordingPowerLevels: [CGFloat] = [0.2, 0.2, 0.2, 0.2, 0.2]

    private var meterTimer: Timer?

    private override init() {
        super.init()
    }

    private func setupAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
            try session.setActive(true)
        } catch {
            print("Audio session error: \(error)")
        }
    }

    private func findAudioUrl(named fileName: String) -> URL? {
        let cleanName = fileName.replacingOccurrences(of: ".m4a", with: "")
                                .replacingOccurrences(of: ".mp3", with: "")

        // 1. Bundle lookup
        if let url = Bundle.main.url(forResource: cleanName, withExtension: "m4a") ??
                     Bundle.main.url(forResource: cleanName, withExtension: "mp3") ??
                     Bundle.main.url(forResource: fileName, withExtension: nil) {
            return url
        }

        // 2. Direct workspace path fallback
        let directPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/Audio/\(cleanName).m4a"
        if FileManager.default.fileExists(atPath: directPath) {
            return URL(fileURLWithPath: directPath)
        }

        return nil
    }

    // MARK: - Real News Audio Playback & Real-time Sentence Tracking
    public func playAudioUrl(_ urlString: String, sentences: [NewsSentence] = []) {
        stopAll()
        setupAudioSession()

        self.activeSentencesQueue = sentences

        guard let audioUrl = findAudioUrl(named: urlString) else {
            print("Audio file not found: \(urlString), falling back to synthesized sequence")
            fallbackToSynthesizerSequence(sentences: sentences)
            return
        }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: audioUrl)
            audioPlayer?.delegate = self
            audioPlayer?.enableRate = true
            audioPlayer?.rate = playbackRate
            audioPlayer?.prepareToPlay()
            audioPlayer?.play()

            self.isPlayingRemoteAudio = true
            self.durationSec = audioPlayer?.duration ?? 0.0

            startProgressTimer()
        } catch {
            print("Failed to init AVAudioPlayer: \(error)")
            fallbackToSynthesizerSequence(sentences: sentences)
        }
    }

    public func playSentence(_ sentence: NewsSentence, audioUrl: String) {
        stopAll()
        setupAudioSession()

        guard let localUrl = findAudioUrl(named: audioUrl) else {
            AudioService.shared.speak(text: sentence.japanese, style: .newsBroadcast, rate: playbackRate * 0.49)
            self.activeSentenceId = sentence.id
            return
        }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: localUrl)
            audioPlayer?.delegate = self
            audioPlayer?.enableRate = true
            audioPlayer?.rate = playbackRate
            audioPlayer?.currentTime = sentence.startTimeSec
            audioPlayer?.prepareToPlay()
            audioPlayer?.play()

            self.isPlayingRemoteAudio = true
            self.activeSentenceId = sentence.id

            let playDuration = max(1.0, (sentence.endTimeSec - sentence.startTimeSec) / Double(playbackRate))
            sentenceStopTimer?.invalidate()
            sentenceStopTimer = Timer.scheduledTimer(withTimeInterval: playDuration, repeats: false) { [weak self] _ in
                guard let self = self else { return }
                self.audioPlayer?.pause()
                self.isPlayingRemoteAudio = false
                self.activeSentenceId = nil
            }
        } catch {
            AudioService.shared.speak(text: sentence.japanese, style: .newsBroadcast, rate: playbackRate * 0.49)
            self.activeSentenceId = sentence.id
        }
    }

    private func startProgressTimer() {
        progressTimer?.invalidate()
        progressTimer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
            guard let self = self, let player = self.audioPlayer, self.isPlayingRemoteAudio else { return }
            let current = player.currentTime
            self.currentTimeSec = current

            // Match active sentence based on exact audio timestamps
            if let matched = self.activeSentencesQueue.first(where: { current >= $0.startTimeSec && current <= $0.endTimeSec }) {
                if self.activeSentenceId != matched.id {
                    self.activeSentenceId = matched.id
                }
            } else {
                if current > (self.activeSentencesQueue.last?.endTimeSec ?? 999.0) {
                    self.activeSentenceId = nil
                }
            }
        }
    }

    private func fallbackToSynthesizerSequence(sentences: [NewsSentence]) {
        guard !sentences.isEmpty else { return }
        isPlayingRemoteAudio = true
        var index = 0

        func playNext() {
            guard isPlayingRemoteAudio, index < sentences.count else {
                isPlayingRemoteAudio = false
                activeSentenceId = nil
                return
            }
            let s = sentences[index]
            activeSentenceId = s.id
            AudioService.shared.speak(text: s.japanese, style: .newsBroadcast, rate: playbackRate * 0.49) {
                index += 1
                playNext()
            }
        }
        playNext()
    }

    public func setSpeed(_ rate: Float) {
        playbackRate = rate
        if let player = audioPlayer, player.isPlaying {
            player.rate = rate
        }
    }

    public func stopAll() {
        progressTimer?.invalidate()
        progressTimer = nil

        sentenceStopTimer?.invalidate()
        sentenceStopTimer = nil

        audioPlayer?.stop()
        audioPlayer = nil
        AudioService.shared.stop()

        isPlayingRemoteAudio = false
        currentTimeSec = 0.0
        activeSentenceId = nil

        stopRecording()
        stopUserPlayback()
    }

    public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.isPlayingRemoteAudio = false
            self.activeSentenceId = nil
            self.progressTimer?.invalidate()
            self.progressTimer = nil
        }
    }

    // MARK: - Shadowing Microphone Voice Recording
    public func startRecordingSentence(id: String) {
        stopAll()

        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setCategory(.playAndRecord, mode: .default, options: [.defaultToSpeaker, .allowBluetooth])
            try audioSession.setActive(true)

            let docPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            let recordUrl = docPath.appendingPathComponent("shadowing_\(id).m4a")
            self.userAudioRecordingUrl = recordUrl

            let settings: [String: Any] = [
                AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
                AVSampleRateKey: 44100.0,
                AVNumberOfChannelsKey: 1,
                AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
            ]

            audioRecorder = try AVAudioRecorder(url: recordUrl, settings: settings)
            audioRecorder?.delegate = self
            audioRecorder?.isMeteringEnabled = true
            audioRecorder?.record()
            isRecordingShadowing = true

            startMeterTimer()
        } catch {
            print("Failed to start voice recording: \(error)")
        }
    }

    public func stopRecording() {
        guard isRecordingShadowing else { return }
        audioRecorder?.stop()
        audioRecorder = nil
        isRecordingShadowing = false
        stopMeterTimer()
    }

    public func playUserRecording() {
        guard let url = userAudioRecordingUrl, FileManager.default.fileExists(atPath: url.path) else { return }
        stopUserPlayback()

        do {
            userRecordingPlayer = try AVAudioPlayer(contentsOf: url)
            userRecordingPlayer?.delegate = self
            userRecordingPlayer?.play()
            isPlayingUserRecording = true
        } catch {
            print("Failed to play user recording: \(error)")
        }
    }

    public func stopUserPlayback() {
        userRecordingPlayer?.stop()
        userRecordingPlayer = nil
        isPlayingUserRecording = false
    }

    private func startMeterTimer() {
        meterTimer?.invalidate()
        meterTimer = Timer.scheduledTimer(withTimeInterval: 0.08, repeats: true) { [weak self] _ in
            guard let self = self, let recorder = self.audioRecorder, self.isRecordingShadowing else { return }
            recorder.updateMeters()
            let power = recorder.averagePower(forChannel: 0)
            let normalized = max(0.2, CGFloat((power + 50) / 50))
            self.recordingPowerLevels = (0..<5).map { _ in CGFloat.random(in: 0.3...normalized) }
        }
    }

    private func stopMeterTimer() {
        meterTimer?.invalidate()
        meterTimer = nil
        recordingPowerLevels = [0.2, 0.2, 0.2, 0.2, 0.2]
    }
}
