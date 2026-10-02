import SwiftUI

/// TokyoClassroomHomeView provides a clean, focused, classroom-style experience
/// featuring an elastic "Shide II" pull-down hero gesture to reveal the daily study package,
/// two dedicated tracks (5-Min Daily Practical Scenario vs JLPT 2 New + 3 Review Ebbinghaus Package),
/// and a structured syllabus roadmap.
public struct TokyoClassroomHomeView: View {
    @ObservedObject var packageEngine = TokyoLearningPackageEngine.shared
    @ObservedObject var gamification = GamificationService.shared
    @ObservedObject var notificationService = NotificationService.shared
    @ObservedObject var languageManager = LanguageManager.shared
    @EnvironmentObject var userProfile: UserProfile
    
    // Pull-Down Gesture State (Inspired by Shide II elastic drawer)
    @State private var pullOffset: CGFloat = 0
    @State private var isPullTriggered: Bool = false
    @State private var selectedJLPTLevel: String = "N5"
    
    // Active Package Sheets
    @State private var activeScenarioPackage: TokyoDailyScenarioPackage? = nil
    @State private var activeJLPTPackage: TokyoDailyJLPTPackage? = nil
    @State private var showMessageCenter: Bool = false
    @State private var showDailyMissions: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // 1. Shide II Elastic Pull-Down Capsule Indicator
                        pullDownHeroIndicator

                        // 2. Classroom Today Header (Student Day & Streak)
                        classroomStatusBanner

                        // 3. Track 1 Card: 5-Minute Practical Scenario Package
                        dailyScenarioPackageCard

                        // 4. Track 2 Card: JLPT 2 New + 3 Review (Ebbinghaus Spaced Repetition)
                        dailyJLPTEbbinghausCard

                        // 5. Classroom Syllabus & Milestone Progress
                        classroomSyllabusSection
                    }
                    .padding(.horizontal)
                    .padding(.bottom, 32)
                }
                .refreshable {
                    // Pull to refresh & trigger haptic feedback
                    UIImpactFeedbackGenerator(style: .medium).impactOccurred()
                    packageEngine.refreshPackage()
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Today's Classroom" : "今日教室")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button(action: { showDailyMissions = true }) {
                        HStack(spacing: 4) {
                            Image(systemName: gamification.isTodayCheckedIn ? "checkmark.circle.fill" : "flame.fill")
                                .foregroundColor(gamification.isTodayCheckedIn ? .green : .orange)
                            Text("\(gamification.streakDays)" + (languageManager.isEnglish ? "d Streak" : " 天连续"))
                                .font(.caption)
                                .fontWeight(.bold)
                        }
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(.ultraThinMaterial)
                        .cornerRadius(10)
                    }
                }

                ToolbarItem(placement: .topBarTrailing) {
                    HStack(spacing: 8) {
                        // Language Switcher Toggle
                        Button(action: {
                            UIImpactFeedbackGenerator(style: .light).impactOccurred()
                            languageManager.toggleEnglishChinese()
                        }) {
                            HStack(spacing: 4) {
                                Image(systemName: "globe")
                                    .font(.caption2)
                                Text(languageManager.isEnglish ? "EN" : "中文")
                                    .font(.caption2)
                                    .fontWeight(.bold)
                            }
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.accentColor.opacity(0.12))
                            .foregroundColor(.accentColor)
                            .cornerRadius(8)
                        }

                        Button(action: { showMessageCenter = true }) {
                            ZStack(alignment: .topTrailing) {
                                Image(systemName: notificationService.unreadCount > 0 ? "bell.badge.fill" : "bell.fill")
                                    .font(.body)
                                    .foregroundColor(notificationService.unreadCount > 0 ? .red : .primary)

                                if notificationService.unreadCount > 0 {
                                    Circle()
                                        .fill(Color.red)
                                        .frame(width: 8, height: 8)
                                        .offset(x: 2, y: -2)
                                }
                            }
                        }
                    }
                }
            }
            .sheet(item: $activeScenarioPackage) { pkg in
                TokyoScenarioDailyPackageView(package: pkg)
            }
            .sheet(item: $activeJLPTPackage) { pkg in
                TokyoJLPTDailyPackageView(package: pkg)
            }
            .sheet(isPresented: $showMessageCenter) {
                TokyoMessageCenterView()
            }
            .sheet(isPresented: $showDailyMissions) {
                DailyMissionSheet()
            }
        }
    }

    // MARK: - 1. Shide II Elastic Pull-Down Capsule
    private var pullDownHeroIndicator: some View {
        Button {
            UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
            activeScenarioPackage = packageEngine.generateTodayScenarioPackage()
        } label: {
            HStack(spacing: 8) {
                Image(systemName: "arrow.down.circle.fill")
                    .font(.system(size: 16, weight: .bold))
                    .foregroundColor(.white)

                Text(languageManager.isEnglish ? "Pull down or tap to launch Daily Session" : "下拉或轻触开启今日精进包")
                    .font(.system(size: 13, weight: .bold, design: .rounded))
                    .foregroundColor(.white)

                Spacer()

                Image(systemName: "play.circle.fill")
                    .font(.caption)
                    .foregroundColor(.white.opacity(0.8))
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 12)
            .background(
                LinearGradient(
                    colors: [Color.accentColor, Color.indigo],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            .cornerRadius(16)
            .shadow(color: Color.accentColor.opacity(0.25), radius: 6, y: 3)
        }
        .buttonStyle(.plain)
    }

    // MARK: - 2. Classroom Status Banner
    private var classroomStatusBanner: some View {
        HStack(spacing: 16) {
            VStack(alignment: .leading, spacing: 4) {
                Text(languageManager.isEnglish ? "TOKYO MASTERY CLASSROOM" : "东京精进教室")
                    .font(.system(size: 10, weight: .heavy))
                    .foregroundColor(.accentColor)
                    .tracking(1.5)

                Text(languageManager.isEnglish ? "Day \(userProfile.currentDay) • Today's Study Plan" : "第 \(userProfile.currentDay) 天 • 今日学习计划")
                    .font(.system(size: 20, weight: .black, design: .rounded))
                    .foregroundColor(.primary)

                Text(languageManager.isEnglish ? "Complete one curated track daily to achieve natural, effortless Japanese fluency." : "每天完成一条精选路线，自然掌握地道日语。")
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // TP Points Badge
            VStack(spacing: 2) {
                Text("\(gamification.tokyoPoints)")
                    .font(.system(size: 18, weight: .black, design: .rounded))
                    .foregroundColor(.orange)
                Text(languageManager.isEnglish ? "TP Points" : "TP 积分")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundColor(.secondary)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(.ultraThinMaterial)
            .cornerRadius(12)
        }
        .padding(16)
        .background(Color(UIColor.secondarySystemGroupedBackground).opacity(0.7))
        .cornerRadius(18)
    }

    // MARK: - 3. Track 1 Card: 5-Minute Practical Scenario Package
    private var dailyScenarioPackageCard: some View {
        let scenarioPkg = packageEngine.generateTodayScenarioPackage()

        return VStack(alignment: .leading, spacing: 14) {
            HStack {
                HStack(spacing: 6) {
                    Image(systemName: "tram.fill")
                        .foregroundColor(.blue)
                    Text(languageManager.isEnglish ? "Track 1 • Daily Context Scenario" : "路线 1 • 日常实战场景包")
                        .font(.caption)
                        .fontWeight(.black)
                        .foregroundColor(.blue)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color.blue.opacity(0.12))
                .cornerRadius(8)

                Spacer()

                HStack(spacing: 4) {
                    Image(systemName: "timer")
                    Text(languageManager.isEnglish ? "5-Min Sprint" : "5 分钟速通")
                        .font(.caption2)
                        .fontWeight(.heavy)
                }
                .foregroundColor(.orange)
            }

            VStack(alignment: .leading, spacing: 6) {
                Text(scenarioPkg.title)
                    .font(.system(size: 18, weight: .black, design: .rounded))
                    .foregroundColor(.primary)

                Text(scenarioPkg.subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            // Learning Elements Preview Pills
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 6) {
                    pillTag(icon: "message.fill", text: languageManager.isEnglish ? "Dialogue" : "对话拆解")
                    pillTag(icon: "textformat.abc", text: languageManager.isEnglish ? "Romaji & EN" : "罗马音与释义")
                    pillTag(icon: "play.tv.fill", text: languageManager.isEnglish ? "Video Lesson" : "情景微课")
                    pillTag(icon: "waveform", text: languageManager.isEnglish ? "Shadowing" : "30秒跟读")
                }
            }

            Divider()

            Button {
                UIImpactFeedbackGenerator(style: .medium).impactOccurred()
                activeScenarioPackage = scenarioPkg
            } label: {
                HStack {
                    Text(languageManager.isEnglish ? "Start Scenario Session (5 Mins)" : "开始今日实战场景（5分钟）")
                        .font(.system(size: 14, weight: .heavy))
                    Spacer()
                    Image(systemName: "arrow.right.circle.fill")
                }
                .foregroundColor(.white)
                .padding(.horizontal, 16)
                .padding(.vertical, 13)
                .background(
                    LinearGradient(
                        colors: [Color.blue, Color.cyan],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .cornerRadius(14)
                .shadow(color: Color.blue.opacity(0.3), radius: 6, y: 3)
            }
        }
        .padding(18)
        .background(Color(UIColor.secondarySystemGroupedBackground))
        .cornerRadius(20)
        .shadow(color: Color.black.opacity(0.04), radius: 10, y: 4)
    }

    // MARK: - 4. Track 2 Card: JLPT 2 New + 3 Review Ebbinghaus Package
    private var dailyJLPTEbbinghausCard: some View {
        let jlptPkg = packageEngine.generateTodayJLPTPackage(level: selectedJLPTLevel)

        return VStack(alignment: .leading, spacing: 14) {
            HStack {
                HStack(spacing: 6) {
                    Image(systemName: "book.fill")
                        .foregroundColor(.purple)
                    Text(languageManager.isEnglish ? "Track 2 • JLPT Ebbinghaus Sprint" : "路线 2 • JLPT 艾宾浩斯冲刺包")
                        .font(.caption)
                        .fontWeight(.black)
                        .foregroundColor(.purple)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background(Color.purple.opacity(0.12))
                .cornerRadius(8)

                Spacer()

                // Level Selector
                Menu {
                    ForEach(["N5", "N4", "N3", "N2", "N1"], id: \.self) { lvl in
                        Button(lvl) {
                            selectedJLPTLevel = lvl
                        }
                    }
                } label: {
                    HStack(spacing: 4) {
                        Text(selectedJLPTLevel)
                            .font(.caption)
                            .fontWeight(.bold)
                        Image(systemName: "chevron.down")
                            .font(.caption2)
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.purple.opacity(0.15))
                    .foregroundColor(.purple)
                    .cornerRadius(8)
                }
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(languageManager.isEnglish ? "JLPT \(selectedJLPTLevel) Spaced Memory Training" : "JLPT \(selectedJLPTLevel) 抗遗忘记忆训练")
                    .font(.system(size: 18, weight: .black, design: .rounded))
                    .foregroundColor(.primary)

                Text(languageManager.isEnglish ? "Ebbinghaus Golden Ratio: 2 New Items + 3 Spaced Reviews" : "艾宾浩斯黄金配比：2个新考点 + 3个周期复习")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            // Elements Breakdown
            HStack(spacing: 12) {
                HStack(spacing: 6) {
                    Circle().fill(Color.blue).frame(width: 8, height: 8)
                    Text(languageManager.isEnglish ? "2 New Items" : "2 个新考点")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                }

                HStack(spacing: 6) {
                    Circle().fill(Color.orange).frame(width: 8, height: 8)
                    Text(languageManager.isEnglish ? "3 Spaced Reviews" : "3 个周期复习")
                        .font(.caption)
                        .fontWeight(.bold)
                        .foregroundColor(.primary)
                }
            }
            .padding(10)
            .background(Color(UIColor.tertiarySystemBackground))
            .cornerRadius(10)

            Divider()

            Button {
                UIImpactFeedbackGenerator(style: .medium).impactOccurred()
                activeJLPTPackage = jlptPkg
            } label: {
                HStack {
                    Text(languageManager.isEnglish ? "Start JLPT \(selectedJLPTLevel) Session" : "开始今日 JLPT \(selectedJLPTLevel) 冲刺")
                        .font(.system(size: 14, weight: .heavy))
                    Spacer()
                    Image(systemName: "arrow.right.circle.fill")
                }
                .foregroundColor(.white)
                .padding(.horizontal, 16)
                .padding(.vertical, 13)
                .background(
                    LinearGradient(
                        colors: [Color.purple, Color.indigo],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .cornerRadius(14)
                .shadow(color: Color.purple.opacity(0.3), radius: 6, y: 3)
            }
        }
        .padding(18)
        .background(Color(UIColor.secondarySystemGroupedBackground))
        .cornerRadius(20)
        .shadow(color: Color.black.opacity(0.04), radius: 10, y: 4)
    }

    // MARK: - 5. Classroom Syllabus Overview
    private var classroomSyllabusSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(languageManager.isEnglish ? "Curriculum & Roadmap" : "系统化进阶路线")
                .font(.caption)
                .fontWeight(.heavy)
                .foregroundColor(.secondary)
                .tracking(1.0)

            VStack(spacing: 10) {
                syllabusRow(number: "1", title: languageManager.isEnglish ? "Tokyo Metro & Yamanote Line Rush" : "东京地铁・山手线通勤早高峰", isCompleted: true)
                syllabusRow(number: "2", title: languageManager.isEnglish ? "Convenience Store Checkout & Heating" : "便利店・结账与便当加热", isCompleted: true)
                syllabusRow(number: "3", title: languageManager.isEnglish ? "Shinjuku Izakaya: First Drink & Otōshi" : "新宿居酒屋・先来杯生啤与小菜", isCompleted: true)
                syllabusRow(number: "4", title: languageManager.isEnglish ? "Akihabara: Limited Figure Quest" : "秋叶原・限定手办与谷子巡礼", isCurrent: true)
                syllabusRow(number: "5", title: languageManager.isEnglish ? "Senso-ji Temple: Omikuji & Worship Etiquette" : "浅草寺・求签与神社参拜礼仪", isCompleted: false)
            }
        }
        .padding(.top, 4)
    }

    private func syllabusRow(number: String, title: String, isCompleted: Bool = false, isCurrent: Bool = false) -> some View {
        HStack(spacing: 12) {
            ZStack {
                Circle()
                    .fill(isCurrent ? Color.accentColor : (isCompleted ? Color.green : Color.secondary.opacity(0.2)))
                    .frame(width: 28, height: 28)

                if isCompleted {
                    Image(systemName: "checkmark")
                        .font(.system(size: 12, weight: .bold))
                        .foregroundColor(.white)
                } else {
                    Text(number)
                        .font(.system(size: 12, weight: .black))
                        .foregroundColor(isCurrent ? .white : .secondary)
                }
            }

            Text(title)
                .font(.subheadline)
                .fontWeight(isCurrent ? .heavy : .medium)
                .foregroundColor(isCurrent ? .primary : .secondary)

            Spacer()

            if isCurrent {
                Text(languageManager.isEnglish ? "TODAY" : "今日")
                    .font(.system(size: 9, weight: .heavy))
                    .foregroundColor(.white)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Capsule().fill(Color.accentColor))
            }
        }
        .padding(12)
        .background(Color(UIColor.secondarySystemGroupedBackground).opacity(isCurrent ? 0.9 : 0.5))
        .cornerRadius(12)
    }

    private func pillTag(icon: String, text: String) -> some View {
        HStack(spacing: 4) {
            Image(systemName: icon)
                .font(.system(size: 10))
            Text(text)
                .font(.system(size: 11, weight: .semibold))
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color(UIColor.tertiarySystemBackground))
        .cornerRadius(8)
    }
}
