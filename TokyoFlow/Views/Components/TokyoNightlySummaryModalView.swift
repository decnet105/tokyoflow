import SwiftUI

/// TokyoNightlySummaryModalView displays an engaging, rewarding 9:00 PM (21:00) Nightly Study Report
/// summarizing daily study duration, TP earned, streak records, golden sentence listening with karaoke flow,
/// and bedtime micro-review.
public struct TokyoNightlySummaryModalView: View {
    public let message: TokyoAppMessage
    @Environment(\.dismiss) private var dismiss
    @ObservedObject private var gamification = GamificationService.shared
    @ObservedObject private var audioService = AudioService.shared
    @ObservedObject private var voiceBank = TokyoVoiceBankService.shared
    @State private var isRewardClaimed: Bool = false

    public init(message: TokyoAppMessage) {
        self.message = message
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Header Banner
                        VStack(spacing: 8) {
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(
                                            colors: [Color.purple.opacity(0.8), Color.blue.opacity(0.8)],
                                            startPoint: .topLeading,
                                            endPoint: .bottomTrailing
                                        )
                                    )
                                    .frame(width: 72, height: 72)
                                    .shadow(color: Color.purple.opacity(0.5), radius: 12, y: 4)

                                Image(systemName: "moon.stars.fill")
                                    .font(.system(size: 34))
                                    .foregroundColor(.yellow)
                            }

                            Text("21:00 今夜の学習レポート")
                                .font(.system(size: 22, weight: .black, design: .rounded))
                                .foregroundColor(.primary)

                            Text(message.formattedDate)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding(.top, 10)

                        // Key Stats Grid
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            statCard(title: "今日学習", value: "\(message.minutesLearned ?? 15) 分", icon: "clock.fill", color: .blue)
                            statCard(title: "獲得TP", value: "+\(message.tpEarned ?? 45) TP", icon: "sparkles", color: .orange)
                            statCard(title: "連続修行", value: "\(message.streak ?? 4) 日目", icon: "flame.fill", color: .red)
                        }
                        .padding(.horizontal)

                        // Golden Sentence of the Day with Live Karaoke Highlight
                        if let sent = message.goldenSentence {
                            VStack(alignment: .leading, spacing: 12) {
                                HStack {
                                    Label("今夜の黄金フレーズ", systemImage: "quote.opening")
                                        .font(.system(size: 13, weight: .bold))
                                        .foregroundColor(.accentColor)
                                    Spacer()
                                    Button(action: {
                                        if voiceBank.isPlayingNativeAudio {
                                            voiceBank.stop()
                                        } else {
                                            voiceBank.playPhraseOrFallback(key: sent, fallbackText: sent)
                                        }
                                    }) {
                                        HStack(spacing: 4) {
                                            Image(systemName: voiceBank.isPlayingNativeAudio ? "waveform" : "speaker.wave.2.fill")
                                            Text(voiceBank.isPlayingNativeAudio ? "再生中" : "Native Audio")
                                                .font(.caption2)
                                                .fontWeight(.bold)
                                        }
                                        .foregroundColor(.white)
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 6)
                                        .background(Color.accentColor)
                                        .cornerRadius(12)
                                    }
                                }

                                TokyoKaraokeSentenceView(
                                    sentenceJa: sent,
                                    furiganaText: message.goldenSentenceFurigana ?? sent,
                                    translation: message.goldenSentenceMeaning ?? "",
                                    showFurigana: true,
                                    fontScale: 1.05
                                )
                                .padding(12)
                                .background(Color.primary.opacity(0.04))
                                .cornerRadius(12)
                            }
                            .padding(16)
                            .background(.ultraThinMaterial)
                            .cornerRadius(18)
                            .padding(.horizontal)
                        }

                        // Detailed Evaluation & Bedtime Study Tip
                        VStack(alignment: .leading, spacing: 10) {
                            Text("就寝前3分・記憶定着アドバイス")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(.primary)

                            Text(message.body)
                                .font(.system(size: 13))
                                .foregroundColor(.secondary)
                                .lineSpacing(4)
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(18)
                        .padding(.horizontal)

                        // Bottom Completion Action Button
                        Button(action: {
                            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
                            if !isRewardClaimed {
                                gamification.addRewards(tp: 20, exp: 30)
                                isRewardClaimed = true
                            }
                            NotificationService.shared.markAsRead(id: message.id)
                            dismiss()
                        }) {
                            HStack(spacing: 8) {
                                Image(systemName: isRewardClaimed ? "checkmark.circle.fill" : "gift.fill")
                                Text(isRewardClaimed ? "日報確認完了" : "本日の修行を完了 (+20 TP)")
                                    .font(.system(size: 16, weight: .heavy))
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                            .background(
                                LinearGradient(
                                    colors: [Color.purple, Color.blue],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(16)
                            .shadow(color: Color.purple.opacity(0.4), radius: 8, y: 4)
                        }
                        .padding(.horizontal)
                        .padding(.top, 4)
                        .padding(.bottom, 24)
                    }
                }
            }
            .navigationTitle("9:00 PM Study Summary")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("閉じる") { dismiss() }
                }
            }
        }
    }

    private func statCard(title: String, value: String, icon: String, color: Color) -> some View {
        VStack(spacing: 6) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(color)
            Text(value)
                .font(.system(size: 16, weight: .black, design: .rounded))
                .foregroundColor(.primary)
            Text(title)
                .font(.system(size: 10, weight: .semibold))
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
        .background(.ultraThinMaterial)
        .cornerRadius(14)
    }
}
