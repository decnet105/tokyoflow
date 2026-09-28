import SwiftUI

public struct DailyCheckInStreakCardView: View {
    @ObservedObject var gamification = GamificationService.shared
    @State private var showCheckInCelebration: Bool = false
    @State private var celebrationText: String = ""

    public init() {}

    public var body: some View {
        VStack(spacing: 16) {
            // Header: Streak & Punch In Action
            HStack(alignment: .center) {
                HStack(spacing: 12) {
                    ZStack {
                        Circle()
                            .fill(LinearGradient(colors: [.orange, .red], startPoint: .topLeading, endPoint: .bottomTrailing))
                            .frame(width: 48, height: 48)
                            .shadow(color: .orange.opacity(0.4), radius: 6, y: 3)

                        Image(systemName: "flame.fill")
                            .font(.system(size: 24))
                            .foregroundColor(.white)
                    }

                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 6) {
                            Text("\(gamification.streakDays) 天连续打卡")
                                .font(.system(size: 17, weight: .black, design: .rounded))
                            if gamification.streakDays >= 3 {
                                Text("🔥 x\(min(5, gamification.streakDays / 3 + 1)) 倍奖励")
                                    .font(.system(size: 10, weight: .bold))
                                    .foregroundColor(.orange)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.orange.opacity(0.15))
                                    .cornerRadius(6)
                            }
                        }

                        Text("碎片时间日积月累 · 征服东京生活日语")
                            .font(.system(size: 11))
                            .foregroundColor(.secondary)
                    }
                }

                Spacer()

                // Punch In Button
                if gamification.isTodayCheckedIn {
                    HStack(spacing: 4) {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                        Text("今日已打卡")
                            .font(.system(size: 12, weight: .bold))
                            .foregroundColor(.green)
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(Color.green.opacity(0.12))
                    .cornerRadius(12)
                } else {
                    Button(action: handlePunchIn) {
                        HStack(spacing: 4) {
                            Image(systemName: "hand.tap.fill")
                            Text("今日打卡")
                                .fontWeight(.black)
                        }
                        .font(.system(size: 13))
                        .foregroundColor(.white)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 8)
                        .background(LinearGradient(colors: [.red, .orange], startPoint: .leading, endPoint: .trailing))
                        .cornerRadius(12)
                        .shadow(color: Color.red.opacity(0.35), radius: 5, y: 2)
                    }
                }
            }

            // 7-Day Weekly Streak Calendar Row
            let weekDays = gamification.getWeeklyCheckInStatus()
            HStack(spacing: 6) {
                ForEach(weekDays) { day in
                    VStack(spacing: 6) {
                        Text(day.dayNameShort)
                            .font(.system(size: 10, weight: .semibold))
                            .foregroundColor(day.isToday ? .accentColor : .secondary)

                        ZStack {
                            Circle()
                                .fill(
                                    day.isCheckedIn
                                        ? Color.green.opacity(0.2)
                                        : (day.isToday ? Color.accentColor.opacity(0.15) : Color.primary.opacity(0.04))
                                )
                                .frame(width: 38, height: 38)
                                .overlay(
                                    Circle()
                                        .stroke(
                                            day.isToday ? Color.accentColor : (day.isCheckedIn ? Color.green : Color.clear),
                                            lineWidth: day.isToday ? 2 : 1.5
                                        )
                                )

                            if day.isCheckedIn {
                                Image(systemName: "checkmark")
                                    .font(.system(size: 15, weight: .bold))
                                    .foregroundColor(.green)
                            } else if day.isToday {
                                Image(systemName: "flame.fill")
                                    .font(.system(size: 16))
                                    .foregroundColor(.orange)
                            } else {
                                Text("+\(day.rewardTP)")
                                    .font(.system(size: 9, weight: .bold))
                                    .foregroundColor(.secondary)
                            }
                        }

                        if day.isToday {
                            Text("Today")
                                .font(.system(size: 8, weight: .bold))
                                .foregroundColor(.accentColor)
                        } else {
                            Text("+\(day.rewardTP)P")
                                .font(.system(size: 8))
                                .foregroundColor(.secondary)
                        }
                    }
                    .frame(maxWidth: .infinity)
                }
            }
            .padding(.vertical, 4)

            Divider()

            // Micro-Learning Daily Fragmented Time Goal (今日碎片化学习进度)
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    HStack(spacing: 6) {
                        Image(systemName: "hourglass.circle.fill")
                            .foregroundColor(.accentColor)
                            .font(.system(size: 14))
                        Text("今日碎片学习目标")
                            .font(.system(size: 13, weight: .bold))
                    }

                    Spacer()

                    Text("\(gamification.dailyMinutesLearned) / \(gamification.dailyGoalMinutes) 分钟")
                        .font(.system(size: 13, weight: .black, design: .monospaced))
                        .foregroundColor(gamification.dailyMinutesLearned >= gamification.dailyGoalMinutes ? .green : .primary)
                }

                // Progress Bar
                GeometryReader { geo in
                    ZStack(alignment: .leading) {
                        Capsule()
                            .fill(Color.primary.opacity(0.08))
                            .frame(height: 8)

                        Capsule()
                            .fill(
                                LinearGradient(
                                    colors: gamification.dailyMinutesLearned >= gamification.dailyGoalMinutes
                                        ? [.green, .mint]
                                        : [.accentColor, .blue],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .frame(width: max(8, geo.size.width * CGFloat(gamification.microLearningProgress)), height: 8)
                            .animation(.spring(response: 0.4, dampingFraction: 0.7), value: gamification.microLearningProgress)
                    }
                }
                .frame(height: 8)

                // Micro-Learning Quick Actions (4 Quick 3-5min bites)
                HStack(spacing: 8) {
                    MicroLearningPill(icon: "character.book.closed.fill", label: "五十音 2分", color: .purple) {
                        gamification.recordMicroLearningTime(minutes: 2)
                    }
                    MicroLearningPill(icon: "headphones", label: "NHK听力 5分", color: .blue) {
                        gamification.recordMicroLearningTime(minutes: 5)
                    }
                    MicroLearningPill(icon: "storefront.fill", label: "场景实战 5分", color: .orange) {
                        gamification.recordMicroLearningTime(minutes: 5)
                    }
                    MicroLearningPill(icon: "mic.fill", label: "跟读录音 3分", color: .red) {
                        gamification.recordMicroLearningTime(minutes: 3)
                    }
                }
                .padding(.top, 4)
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(20)
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(Color.primary.opacity(0.08), lineWidth: 1)
        )
        .overlay(
            // Celebration Toast
            Group {
                if showCheckInCelebration {
                    VStack(spacing: 8) {
                        Image(systemName: "sparkles")
                            .font(.largeTitle)
                            .foregroundColor(.yellow)
                        Text(celebrationText)
                            .font(.system(size: 15, weight: .heavy))
                            .foregroundColor(.white)
                            .multilineTextAlignment(.center)
                    }
                    .padding(20)
                    .background(Color.black.opacity(0.85))
                    .cornerRadius(18)
                    .shadow(radius: 12)
                    .transition(.scale.combined(with: .opacity))
                }
            }
        )
    }

    private func handlePunchIn() {
        let success = gamification.punchInToday()
        if success {
            celebrationText = "🎉 打卡成功！\n连续打卡 \(gamification.streakDays) 天\n+50 TP  +60 EXP"
            withAnimation(.spring()) {
                showCheckInCelebration = true
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                withAnimation(.easeOut) {
                    showCheckInCelebration = false
                }
            }
        }
    }
}

public struct MicroLearningPill: View {
    public let icon: String
    public let label: String
    public let color: Color
    public let onQuickRecord: () -> Void

    public var body: some View {
        Button(action: onQuickRecord) {
            HStack(spacing: 4) {
                Image(systemName: icon)
                    .font(.system(size: 10))
                Text(label)
                    .font(.system(size: 10, weight: .bold))
            }
            .foregroundColor(color)
            .padding(.horizontal, 8)
            .padding(.vertical, 6)
            .frame(maxWidth: .infinity)
            .background(color.opacity(0.12))
            .cornerRadius(8)
        }
        .buttonStyle(.plain)
    }
}
