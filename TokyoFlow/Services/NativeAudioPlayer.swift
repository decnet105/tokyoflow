import Foundation
import AVFoundation
import Combine

public class NativeAudioPlayer: NSObject, ObservableObject, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    public static let shared = NativeAudioPlayer()

    private var avPlayer: AVPlayer?
    private var timeObserverToken: Any?
    private var audioRecorder: AVAudioRecorder?
    private var userRecordingPlayer: AVAudioPlayer?
    private var fallbackTimer: Timer?
    private var activeSentencesQueue: [NewsSentence] = []
    private var currentSentenceIndex: Int = 0

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

    private func ensureAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers, .defaultToSpeaker])
            try session.setActive(true)
        } catch {
            print("Audio session error: \(error)")
        }
    }

    // MARK: - Remote Human Audio Stream + Resilient Fallback
    public func playAudioUrl(_ urlString: String, sentences: [NewsSentence] = []) {
        stopAll()
        ensureAudioSession()

        self.activeSentencesQueue = sentences
        guard let url = URL(string: urlString) else {
            startSynthesizedSentenceFlow(sentences: sentences)
            return
        }

        let playerItem = AVPlayerItem(url: url)
        avPlayer = AVPlayer(playerItem: playerItem)
        avPlayer?.rate = playbackRate
        isPlayingRemoteAudio = true

        setupTimeObserver(sentences: sentences)
        avPlayer?.play()

        // Resilient fallback monitor: If remote audio fails or stalls after 1.5s, switch to local prosody engine
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
            guard let self = self, self.isPlayingRemoteAudio else { return }
            if self.currentTimeSec == 0.0 && self.avPlayer?.status != .readyToPlay {
                // Fallback to sentence-by-sentence broadcast
                self.startSynthesizedSentenceFlow(sentences: sentences)
            }
        }
    }

    public func playSentence(_ sentence: NewsSentence, audioUrl: String) {
        stopAll()
        ensureAudioSession()
        activeSentenceId = sentence.id
        isPlayingRemoteAudio = true

        // Play individual sentence via TokyoProsodyEngine news broadcast style
        AudioService.shared.speak(text: sentence.japanese, style: .newsBroadcast, rate: playbackRate * 0.49)

        // Automatically clear active state after sentence duration
        let duration = max(2.5, sentence.endTimeSec - sentence.startTimeSec) / Double(playbackRate)
        fallbackTimer?.invalidate()
        fallbackTimer = Timer.scheduledTimer(withTimeInterval: duration, repeats: false) { [weak self] _ in
            guard let self = self else { return }
            self.isPlayingRemoteAudio = false
        }
    }

    private func startSynthesizedSentenceFlow(sentences: [NewsSentence]) {
        guard !sentences.isEmpty else { return }
        stopAll()
        ensureAudioSession()

        isPlayingRemoteAudio = true
        currentSentenceIndex = 0
        playCurrentSentenceInQueue()
    }

    private func playCurrentSentenceInQueue() {
        guard isPlayingRemoteAudio, currentSentenceIndex < activeSentencesQueue.count else {
            isPlayingRemoteAudio = false
            activeSentenceId = nil
            return
        }

        let sentence = activeSentencesQueue[currentSentenceIndex]
        activeSentenceId = sentence.id
        currentTimeSec = sentence.startTimeSec
        durationSec = activeSentencesQueue.last?.endTimeSec ?? 20.0

        AudioService.shared.speak(text: sentence.japanese, style: .newsBroadcast, rate: playbackRate * 0.49)

        let duration = max(3.0, (sentence.endTimeSec - sentence.startTimeSec)) / Double(playbackRate)
        fallbackTimer?.invalidate()
        fallbackTimer = Timer.scheduledTimer(withTimeInterval: duration, repeats: false) { [weak self] _ in
            guard let self = self, self.isPlayingRemoteAudio else { return }
            self.currentSentenceIndex += 1
            self.playCurrentSentenceInQueue()
        }
    }

    private func setupTimeObserver(sentences: [NewsSentence]) {
        let interval = CMTime(seconds: 0.1, preferredTimescale: 600)
        timeObserverToken = avPlayer?.addPeriodicTimeObserver(forInterval: interval, queue: .main) { [weak self] time in
            guard let self = self else { return }
            let currentSec = CMTimeGetSeconds(time)
            self.currentTimeSec = currentSec

            if let duration = self.avPlayer?.currentItem?.duration {
                let dSec = CMTimeGetSeconds(duration)
                if !dSec.isNaN && dSec > 0 {
                    self.durationSec = dSec
                }
            }

            // Sync active sentence
            if let matched = sentences.first(where: { currentSec >= $0.startTimeSec && currentSec <= $0.endTimeSec }) {
                self.activeSentenceId = matched.id
            }
        }
    }

    public func togglePlayPause() {
        if isPlayingRemoteAudio {
            stopAll()
        } else {
            if !activeSentencesQueue.isEmpty {
                startSynthesizedSentenceFlow(sentences: activeSentencesQueue)
            }
        }
    }

    public func setSpeed(_ rate: Float) {
        playbackRate = rate
        if isPlayingRemoteAudio {
            avPlayer?.rate = rate
        }
    }

    public func stopAll() {
        fallbackTimer?.invalidate()
        fallbackTimer = nil

        if let token = timeObserverToken {
            avPlayer?.removeTimeObserver(token)
            timeObserverToken = nil
        }
        avPlayer?.pause()
        avPlayer = nil
        AudioService.shared.stop()
        isPlayingRemoteAudio = false
        currentTimeSec = 0.0
        activeSentenceId = nil

        stopRecording()
        stopUserPlayback()
    }

    // MARK: - Shadowing Microphone Voice Recorder
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

    public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.isPlayingUserRecording = false
        }
    }
}
