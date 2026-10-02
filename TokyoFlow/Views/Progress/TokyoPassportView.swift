import SwiftUI

public struct TokyoPassportView: View {
    @EnvironmentObject var userProfile: UserProfile
    @ObservedObject var dataManager = DataManager.shared
    @ObservedObject var notificationService = NotificationService.shared
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showMessageCenter: Bool = false

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Profile Passport Card
                        VStack(alignment: .leading, spacing: 14) {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(languageManager.isEnglish ? "TOKYO RESIDENCE PASSPORT" : "东京定居学习护照")
                                        .font(.system(size: 10, weight: .bold))
                                        .foregroundColor(.accentColor)
                                        .tracking(2.0)
                                    Text(languageManager.isEnglish ? "Year 1 Tokyo Explorer" : "第1年 • 东京探索者")
                                        .font(.title2)
                                        .fontWeight(.bold)
                                }
                                Spacer()
                                Image(systemName: "person.crop.circle.badge.checkmark")
                                    .font(.system(size: 40))
                                    .foregroundColor(.accentColor)
                            }

                            Divider()

                            HStack(spacing: 20) {
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(languageManager.isEnglish ? "CURRENT DAY" : "当前天数")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundColor(.secondary)
                                    Text(languageManager.isEnglish ? "Day \(userProfile.currentDay) / 365" : "第 \(userProfile.currentDay) / 365 天")
                                        .font(.headline)
                                        .fontWeight(.heavy)
                                }

                                VStack(alignment: .leading, spacing: 2) {
                                    Text(languageManager.isEnglish ? "STREAK" : "连续打卡")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundColor(.secondary)
                                    HStack(spacing: 4) {
                                        Image(systemName: "flame.fill")
                                            .foregroundColor(.orange)
                                        Text("\(userProfile.streakCount) " + (languageManager.isEnglish ? "Days" : "天"))
                                            .font(.headline)
                                            .fontWeight(.heavy)
                                    }
                                }

                                VStack(alignment: .leading, spacing: 2) {
                                    Text(languageManager.isEnglish ? "CAN-DO LEVEL" : "标准等级")
                                        .font(.system(size: 9, weight: .bold))
                                        .foregroundColor(.secondary)
                                    Text("JF A1-A2")
                                        .font(.headline)
                                        .fontWeight(.heavy)
                                        .foregroundColor(.green)
                                }
                            }
                        }
                        .padding(20)
                        .background(.ultraThinMaterial)
                        .cornerRadius(18)
                        .shadow(color: Color.black.opacity(0.04), radius: 10, x: 0, y: 2)
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Message & 21:00 Nightly Summary Center Quick Tile
                        Button(action: { showMessageCenter = true }) {
                            HStack(spacing: 14) {
                                ZStack {
                                    Circle()
                                        .fill(LinearGradient(colors: [.purple, .blue], startPoint: .topLeading, endPoint: .bottomTrailing))
                                        .frame(width: 44, height: 44)
                                    Image(systemName: "moon.stars.fill")
                                        .font(.system(size: 20))
                                        .foregroundColor(.yellow)
                                }

                                VStack(alignment: .leading, spacing: 3) {
                                    HStack {
                                        Text(languageManager.isEnglish ? "Inbox & 21:00 Daily Summary" : "消息与 21:00 晚报中心")
                                            .font(.subheadline)
                                            .fontWeight(.bold)
                                            .foregroundColor(.primary)

                                        if notificationService.unreadCount > 0 {
                                            Text("\(notificationService.unreadCount) " + (languageManager.isEnglish ? "Unread" : "未读"))
                                                .font(.system(size: 10, weight: .heavy))
                                                .foregroundColor(.white)
                                                .padding(.horizontal, 6)
                                                .padding(.vertical, 2)
                                                .background(Capsule().fill(Color.red))
                                        }
                                    }

                                    Text(languageManager.isEnglish ? "Check nightly reports, bonus TP, and spaced recall reminders" : "每晚的个性化学习报告、奖励TP与复习提醒")
                                        .font(.caption2)
                                        .foregroundColor(.secondary)
                                        .lineLimit(1)
                                }

                                Spacer()

                                Image(systemName: "chevron.right")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            .padding(14)
                            .background(.ultraThinMaterial)
                            .cornerRadius(16)
                            .padding(.horizontal)
                        }
                        .buttonStyle(.plain)

                        // 1-Year Roadmap Milestone Tracker
                        VStack(alignment: .leading, spacing: 14) {
                            Text(languageManager.isEnglish ? "1-YEAR ROADMAP & QUARTERLY GOALS" : "年度路线图与季度目标")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                                .tracking(1.2)
                                .padding(.horizontal)

                            ForEach(OneYearRoadmap.quarters) { quarter in
                                QuarterMilestoneCard(
                                    quarter: quarter,
                                    isCurrent: quarter.quarterNumber == 1
                                )
                                .padding(.horizontal)
                            }
                        }

                        // Japan Foundation Can-Do Standards Checklist
                        VStack(alignment: .leading, spacing: 14) {
                            Text(languageManager.isEnglish ? "JAPAN FOUNDATION CAN-DO COMPETENCY" : "国际日本语能力标准 (JF CAN-DO)")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                                .tracking(1.2)
                                .padding(.horizontal)

                            VStack(spacing: 10) {
                                CanDoItemRow(
                                    code: "A1.1",
                                    title: languageManager.isEnglish ? "Tokyo Commute & IC Card" : "东京通勤与IC卡充值",
                                    desc: languageManager.isEnglish ? "Can buy transit tickets and recharge Suica at ticket machines." : "能够熟练在自动售票机购票并为Suica/西瓜卡充值。",
                                    isDone: userProfile.completedScenarioIds.contains("scenario_01_morning_train")
                                )
                                CanDoItemRow(
                                    code: "A1.2",
                                    title: languageManager.isEnglish ? "Convenience Store Checkout" : "便利店顺畅结账",
                                    desc: languageManager.isEnglish ? "Can handle bento heating, utensil requests, and bag options smoothly." : "能够从容应对便当加热、餐具需求与塑料袋确认。",
                                    isDone: userProfile.completedScenarioIds.contains("scenario_02_kombini_morning")
                                )
                                CanDoItemRow(
                                    code: "A2.1",
                                    title: languageManager.isEnglish ? "Ramen & Food Customization" : "拉面食券与定制暗号",
                                    desc: languageManager.isEnglish ? "Can read ticket vending machines and specify noodle texture/oil." : "能够看懂食券机并准确告知店主面条软硬、汤底咸度与油脂量。",
                                    isDone: userProfile.completedScenarioIds.contains("scenario_03_ramen_ticket_machine")
                                )
                                CanDoItemRow(
                                    code: "A2.2",
                                    title: languageManager.isEnglish ? "Izakaya Table & Split Bills" : "居酒屋点单与结账礼仪",
                                    desc: languageManager.isEnglish ? "Can order opening drinks ('toriaezu nama') and manage group bill payment." : "能够熟练点先发饮品、理解前菜小菜机制并应对AA制结账。",
                                    isDone: userProfile.completedScenarioIds.contains("scenario_04_izakaya_table_booking")
                                )
                                CanDoItemRow(
                                    code: "B1.1",
                                    title: languageManager.isEnglish ? "Postal Redelivery Logistics" : "快递不在票与再配送实操",
                                    desc: languageManager.isEnglish ? "Can decode missed delivery notices (不在票) and schedule time windows." : "能够读懂快递不在票并成功通过电话/网页预约指定派送时段。",
                                    isDone: userProfile.completedScenarioIds.contains("scenario_07_post_office_delivery")
                                )
                            }
                            .padding()
                            .background(.ultraThinMaterial)
                            .cornerRadius(16)
                            .padding(.horizontal)
                        }

                        // App Settings
                        VStack(alignment: .leading, spacing: 12) {
                            Text(languageManager.isEnglish ? "STUDY SETTINGS" : "学习偏好设置")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                                .tracking(1.2)
                                .padding(.horizontal)

                            VStack(spacing: 12) {
                                Toggle(isOn: $userProfile.furiganaEnabled) {
                                    Label(languageManager.isEnglish ? "Ruby Furigana Reading" : "显示假名注音 (振假名)", systemImage: "character.phonetic")
                                }

                                Divider()

                                Toggle(isOn: $userProfile.romajiEnabled) {
                                    Label(languageManager.isEnglish ? "Show Romaji Subtitles" : "显示罗马音字幕 (Romaji)", systemImage: "textformat")
                                }

                                Divider()

                                HStack {
                                    Label(languageManager.isEnglish ? "Voice Playback Speed" : "语音播放语速", systemImage: "speedometer")
                                    Spacer()
                                    Text(String(format: "%.2fx", userProfile.speechRate))
                                        .font(.footnote)
                                        .foregroundColor(.secondary)
                                }
                                Slider(value: $userProfile.speechRate, in: 0.35...0.65, step: 0.05)
                            }
                            .padding()
                            .background(.ultraThinMaterial)
                            .cornerRadius(16)
                            .padding(.horizontal)
                        }
                    }
                    .padding(.bottom, 24)
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Tokyo Passport" : "东京学习档案与护照")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(action: {
                        UIImpactFeedbackGenerator(style: .light).impactOccurred()
                        languageManager.toggleEnglishChinese()
                    }) {
                        HStack(spacing: 4) {
                            Text(languageManager.isEnglish ? "EN" : "中文")
                                .font(.caption2)
                                .fontWeight(.heavy)
                        }
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.accentColor.opacity(0.15))
                        .foregroundColor(.accentColor)
                        .cornerRadius(8)
                    }
                }
            }
            .sheet(isPresented: $showMessageCenter) {
                TokyoMessageCenterView()
            }
        }
    }
}

public struct QuarterMilestoneCard: View {
    public let quarter: QuarterMilestone
    public let isCurrent: Bool
    @ObservedObject var languageManager = LanguageManager.shared

    public var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                ZStack {
                    Circle()
                        .fill(isCurrent ? Color.accentColor : Color(.systemGray5))
                        .frame(width: 32, height: 32)
                    Text("\(quarter.quarterNumber)")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(isCurrent ? .white : .primary)
                }

                VStack(alignment: .leading, spacing: 2) {
                    Text(quarter.localizedName(isEnglish: languageManager.isEnglish))
                        .font(.headline)
                    Text(quarter.nameJa)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                Text(quarter.jfLevel)
                    .font(.caption2)
                    .fontWeight(.bold)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.green.opacity(0.12))
                    .foregroundColor(.green)
                    .cornerRadius(8)
            }

            VStack(alignment: .leading, spacing: 6) {
                HStack(alignment: .top, spacing: 6) {
                    Image(systemName: "house.fill")
                        .font(.caption2)
                        .foregroundColor(.accentColor)
                    Text(languageManager.isEnglish ? "Living: \(quarter.livingSkillsGoal)" : "生活实务：\(quarter.livingSkillsGoalZh)")
                        .font(.caption)
                        .foregroundColor(.primary.opacity(0.9))
                }

                HStack(alignment: .top, spacing: 6) {
                    Image(systemName: "book.fill")
                        .font(.caption2)
                        .foregroundColor(.purple)
                    Text(languageManager.isEnglish ? "Manga: \(quarter.mangaGoal)" : "漫画理解：\(quarter.mangaGoalZh)")
                        .font(.caption)
                        .foregroundColor(.primary.opacity(0.9))
                }
            }
            .padding(10)
            .background(Color(.systemGray6))
            .cornerRadius(10)
        }
        .padding(16)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(isCurrent ? Color.accentColor : Color.clear, lineWidth: 1.5)
        )
    }
}

public struct CanDoItemRow: View {
    public let code: String
    public let title: String
    public let desc: String
    public let isDone: Bool

    public var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: isDone ? "checkmark.circle.fill" : "circle")
                .font(.title3)
                .foregroundColor(isDone ? .green : .secondary)

            VStack(alignment: .leading, spacing: 2) {
                HStack {
                    Text(code)
                        .font(.caption2)
                        .fontWeight(.heavy)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.green.opacity(0.12))
                        .foregroundColor(.green)
                        .cornerRadius(4)

                    Text(title)
                        .font(.subheadline)
                        .fontWeight(.semibold)
                }

                Text(desc)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
        }
    }
}
