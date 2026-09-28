import Foundation
import AVFoundation
import MediaPlayer
import Combine

public class TokyoRadioService: NSObject, ObservableObject, AVAudioPlayerDelegate {
    public static let shared = TokyoRadioService()

    private var audioPlayer: AVAudioPlayer?
    private var progressTimer: Timer?
    private var sleepTimer: Timer?

    @Published public var currentStation: TokyoRadioStation? = nil
    @Published public var isPlaying: Bool = false
    @Published public var currentTimeSec: Double = 0.0
    @Published public var durationSec: Double = 0.0
    @Published public var playbackRate: Float = 1.0
    @Published public var activeChapter: RadioChapter? = nil
    @Published public var remainingSleepSeconds: Int? = nil
    @Published public var totalListenedSecondsToday: Double = 0.0
    @Published public var waveformLevels: [CGFloat] = [0.3, 0.5, 0.8, 0.4, 0.6]

    private var rewardTimer: Timer?

    private override init() {
        super.init()
        setupAudioSession()
        setupRemoteCommandCenter()
    }

    private func setupAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.playback, mode: .spokenAudio, options: [])
            try session.setActive(true)
        } catch {
            print("Audio session error: \(error)")
        }
    }

    private func setupRemoteCommandCenter() {
        let commandCenter = MPRemoteCommandCenter.shared()

        commandCenter.playCommand.isEnabled = true
        commandCenter.playCommand.addTarget { [weak self] _ in
            self?.resume()
            return .success
        }

        commandCenter.pauseCommand.isEnabled = true
        commandCenter.pauseCommand.addTarget { [weak self] _ in
            self?.pause()
            return .success
        }

        commandCenter.skipForwardCommand.isEnabled = true
        commandCenter.skipForwardCommand.preferredIntervals = [15]
        commandCenter.skipForwardCommand.addTarget { [weak self] _ in
            self?.seek(by: 15)
            return .success
        }

        commandCenter.skipBackwardCommand.isEnabled = true
        commandCenter.skipBackwardCommand.preferredIntervals = [15]
        commandCenter.skipBackwardCommand.addTarget { [weak self] _ in
            self?.seek(by: -15)
            return .success
        }
    }

    public func playStation(_ station: TokyoRadioStation, startAtChapter: RadioChapter? = nil) {
        stop()
        setupAudioSession()

        self.currentStation = station

        guard let localUrl = findAudioUrl(named: station.audioFileName) else {
            print("Radio audio file not found: \(station.audioFileName)")
            return
        }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: localUrl)
            audioPlayer?.delegate = self
            audioPlayer?.enableRate = true
            audioPlayer?.rate = playbackRate

            if let chapter = startAtChapter {
                audioPlayer?.currentTime = chapter.startTimeSec
                self.activeChapter = chapter
            } else {
                self.activeChapter = station.chapters.first
            }

            audioPlayer?.prepareToPlay()
            audioPlayer?.play()

            self.isPlaying = true
            self.durationSec = audioPlayer?.duration ?? station.durationSec

            startProgressTimer()
            startRewardTracking()
            updateNowPlayingInfo()
        } catch {
            print("Error playing radio station: \(error)")
        }
    }

    public func togglePlayPause() {
        if isPlaying {
            pause()
        } else {
            resume()
        }
    }

    public func pause() {
        audioPlayer?.pause()
        isPlaying = false
        updateNowPlayingInfo()
    }

    public func resume() {
        setupAudioSession()
        audioPlayer?.rate = playbackRate
        audioPlayer?.play()
        isPlaying = true
        startProgressTimer()
        startRewardTracking()
        updateNowPlayingInfo()
    }

    public func seek(to seconds: Double) {
        let clamped = max(0.0, min(durationSec, seconds))
        audioPlayer?.currentTime = clamped
        self.currentTimeSec = clamped
        syncActiveChapter(currentTime: clamped)
        updateNowPlayingInfo()
    }

    public func seek(by delta: Double) {
        guard let player = audioPlayer else { return }
        seek(to: player.currentTime + delta)
    }

    public func jumpToChapter(_ chapter: RadioChapter) {
        seek(to: chapter.startTimeSec)
        self.activeChapter = chapter
    }

    public func setSpeed(_ rate: Float) {
        self.playbackRate = rate
        if let player = audioPlayer, isPlaying {
            player.rate = rate
        }
        updateNowPlayingInfo()
    }

    public func setSleepTimer(minutes: Int?) {
        sleepTimer?.invalidate()
        sleepTimer = nil

        guard let mins = minutes, mins > 0 else {
            remainingSleepSeconds = nil
            return
        }

        var remaining = mins * 60
        remainingSleepSeconds = remaining

        sleepTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] t in
            guard let self = self else { return }
            remaining -= 1
            self.remainingSleepSeconds = remaining

            if remaining <= 0 {
                t.invalidate()
                self.sleepTimer = nil
                self.remainingSleepSeconds = nil
                self.pause()
            }
        }
    }

    public func stop() {
        progressTimer?.invalidate()
        progressTimer = nil

        rewardTimer?.invalidate()
        rewardTimer = nil

        audioPlayer?.stop()
        audioPlayer = nil

        isPlaying = false
        currentTimeSec = 0.0
        activeChapter = nil

        MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
    }

    private func startProgressTimer() {
        progressTimer?.invalidate()
        progressTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            guard let self = self, let player = self.audioPlayer, self.isPlaying else { return }
            let current = player.currentTime
            self.currentTimeSec = current
            self.syncActiveChapter(currentTime: current)
            self.waveformLevels = (0..<5).map { _ in CGFloat.random(in: 0.25...0.95) }
        }
    }

    private func syncActiveChapter(currentTime: Double) {
        guard let station = currentStation else { return }
        let sorted = station.chapters.sorted { $0.startTimeSec < $1.startTimeSec }
        if let current = sorted.last(where: { currentTime >= $0.startTimeSec }) {
            if activeChapter?.id != current.id {
                activeChapter = current
                updateNowPlayingInfo()
            }
        }
    }

    private func startRewardTracking() {
        rewardTimer?.invalidate()
        rewardTimer = Timer.scheduledTimer(withTimeInterval: 60.0, repeats: true) { [weak self] _ in
            guard let self = self, self.isPlaying else { return }
            self.totalListenedSecondsToday += 60.0
            // Award TP every 5 minutes (300 seconds)
            if Int(self.totalListenedSecondsToday) % 300 == 0 {
                GamificationService.shared.addRewards(tp: 15, exp: 25)
            }
        }
    }

    private func updateNowPlayingInfo() {
        guard let station = currentStation else { return }

        var info = [String: Any]()
        info[MPMediaItemPropertyTitle] = activeChapter?.titleJa ?? station.titleJa
        info[MPMediaItemPropertyArtist] = "NHK Radio & TokyoFlow (1-Hour Immersion)"
        info[MPMediaItemPropertyAlbumTitle] = station.title
        info[MPNowPlayingInfoPropertyElapsedPlaybackTime] = currentTimeSec
        info[MPMediaItemPropertyPlaybackDuration] = durationSec
        info[MPNowPlayingInfoPropertyPlaybackRate] = isPlaying ? Double(playbackRate) : 0.0

        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }

    private func findAudioUrl(named fileName: String) -> URL? {
        let cleanName = fileName.replacingOccurrences(of: ".m4a", with: "")
                                .replacingOccurrences(of: ".mp3", with: "")

        if let url = Bundle.main.url(forResource: cleanName, withExtension: "m4a") ??
                     Bundle.main.url(forResource: cleanName, withExtension: "mp3") ??
                     Bundle.main.url(forResource: fileName, withExtension: nil) {
            return url
        }

        let directPath = "/Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Resources/Audio/\(cleanName).m4a"
        if FileManager.default.fileExists(atPath: directPath) {
            return URL(fileURLWithPath: directPath)
        }

        return nil
    }

    public func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        DispatchQueue.main.async {
            self.isPlaying = false
            self.progressTimer?.invalidate()
            self.progressTimer = nil
        }
    }
}
