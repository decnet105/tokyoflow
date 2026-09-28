import Foundation
import AVFoundation
import Combine

public class NativeAudioPlayer: NSObject, ObservableObject, AVAudioPlayerDelegate, AVAudioRecorderDelegate {
    public static let shared = NativeAudioPlayer()

    private var avPlayer: AVPlayer?
    private var timeObserverToken: Any?
    private var audioRecorder: AVAudioRecorder?
    private var userRecordingPlayer: AVAudioPlayer?

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

    // MARK: - Remote Human Audio Stream
    public func playAudioUrl(_ urlString: String, sentences: [NewsSentence] = []) {
        guard let url = URL(string: urlString) else { return }

        // Stop existing
        stopAll()

        let playerItem = AVPlayerItem(url: url)
        avPlayer = AVPlayer(playerItem: playerItem)
        avPlayer?.rate = playbackRate
        isPlayingRemoteAudio = true

        setupTimeObserver(sentences: sentences)
        avPlayer?.play()
    }

    public func playSentence(_ sentence: NewsSentence, audioUrl: String) {
        if avPlayer == nil {
            guard let url = URL(string: audioUrl) else { return }
            avPlayer = AVPlayer(url: url)
        }

        let targetTime = CMTime(seconds: sentence.startTimeSec, preferredTimescale: 600)
        avPlayer?.seek(to: targetTime, toleranceBefore: .zero, toleranceAfter: .zero) { [weak self] _ in
            guard let self = self else { return }
            self.avPlayer?.rate = self.playbackRate
            self.avPlayer?.play()
            self.isPlayingRemoteAudio = true
            self.activeSentenceId = sentence.id
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
        guard let player = avPlayer else { return }
        if isPlayingRemoteAudio {
            player.pause()
            isPlayingRemoteAudio = false
        } else {
            player.rate = playbackRate
            player.play()
            isPlayingRemoteAudio = true
        }
    }

    public func setSpeed(_ rate: Float) {
        playbackRate = rate
        if isPlayingRemoteAudio {
            avPlayer?.rate = rate
        }
    }

    public func stopAll() {
        if let token = timeObserverToken {
            avPlayer?.removeTimeObserver(token)
            timeObserverToken = nil
        }
        avPlayer?.pause()
        avPlayer = nil
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
