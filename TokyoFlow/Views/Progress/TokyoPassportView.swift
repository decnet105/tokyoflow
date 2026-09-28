import SwiftUI

public struct TokyoPassportView: View {
    @EnvironmentObject var userProfile: UserProfile
    @ObservedObject var dataManager = DataManager.shared

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Profile Passport Card
                    VStack(alignment: .leading, spacing: 14) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("TOKYO RESIDENCE PASSPORT")
                                    .font(.system(size: 10, weight: .bold))
                                    .foregroundColor(.accentColor)
                                    .tracking(2.0)
                                Text("Year 1 Tokyo Explorer")
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
                                Text("CURRENT DAY")
                                    .font(.system(size: 9, weight: .bold))
                                    .foregroundColor(.secondary)
                                Text("Day \(userProfile.currentDay) / 365")
                                    .font(.headline)
                                    .fontWeight(.heavy)
                            }

                            VStack(alignment: .leading, spacing: 2) {
                                Text("STREAK")
                                    .font(.system(size: 9, weight: .bold))
                                    .foregroundColor(.secondary)
                                HStack(spacing: 4) {
                                    Image(systemName: "flame.fill")
                                        .foregroundColor(.orange)
                                    Text("\(userProfile.streakCount) Days")
                                        .font(.headline)
                                        .fontWeight(.heavy)
                                }
                            }

                            VStack(alignment: .leading, spacing: 2) {
                                Text("CAN-DO LEVEL")
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
                    .background(Color(.secondarySystemGroupedBackground))
                    .cornerRadius(18)
                    .shadow(color: Color.black.opacity(0.04), radius: 10, x: 0, y: 2)
                    .padding(.horizontal)
                    .padding(.top, 8)

                    // 1-Year Roadmap Milestone Tracker
                    VStack(alignment: .leading, spacing: 14) {
                        Text("1-YEAR ROADMAP & QUARTERLY GOALS")
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
                        Text("JAPAN FOUNDATION CAN-DO COMPETENCY")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.secondary)
                            .tracking(1.2)
                            .padding(.horizontal)

                        VStack(spacing: 10) {
                            CanDoItemRow(
                                code: "A1.1",
                                title: "Tokyo Commute & IC Card",
                                desc: "Can buy transit tickets and recharge Suica at ticket machines.",
                                isDone: userProfile.completedScenarioIds.contains("scenario_01_morning_train")
                            )
                            CanDoItemRow(
                                code: "A1.2",
                                title: "Convenience Store Checkout",
                                desc: "Can handle bento heating, utensil requests, and bag options smoothly.",
                                isDone: userProfile.completedScenarioIds.contains("scenario_02_kombini_morning")
                            )
                            CanDoItemRow(
                                code: "A2.1",
                                title: "Ramen & Food Customization",
                                desc: "Can read ticket vending machines and specify noodle texture/oil.",
                                isDone: userProfile.completedScenarioIds.contains("scenario_03_ramen_ticket_machine")
                            )
                            CanDoItemRow(
                                code: "A2.2",
                                title: "Izakaya Table & Split Bills",
                                desc: "Can order opening drinks ('toriaezu nama') and manage group bill payment.",
                                isDone: userProfile.completedScenarioIds.contains("scenario_04_izakaya_table_booking")
                            )
                            CanDoItemRow(
                                code: "B1.1",
                                title: "Postal Redelivery Logistics",
                                desc: "Can decode missed delivery notices (不在票) and schedule time windows.",
                                isDone: userProfile.completedScenarioIds.contains("scenario_07_post_office_delivery")
                            )
                        }
                        .padding()
                        .background(Color(.secondarySystemGroupedBackground))
                        .cornerRadius(16)
                        .padding(.horizontal)
                    }

                    // App Settings
                    VStack(alignment: .leading, spacing: 12) {
                        Text("STUDY SETTINGS")
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.secondary)
                            .tracking(1.2)
                            .padding(.horizontal)

                        VStack(spacing: 12) {
                            Toggle(isOn: $userProfile.furiganaEnabled) {
                                Label("Ruby Furigana Reading", systemImage: "character.phonetic")
                            }

                            Divider()

                            Toggle(isOn: $userProfile.romajiEnabled) {
                                Label("Show Romaji Subtitles", systemImage: "textformat")
                            }

                            Divider()

                            HStack {
                                Label("Japanese TTS Speed", systemImage: "speedometer")
                                Spacer()
                                Text(String(format: "%.2fx", userProfile.speechRate))
                                    .font(.footnote)
                                    .foregroundColor(.secondary)
                            }
                            Slider(value: $userProfile.speechRate, in: 0.35...0.65, step: 0.05)
                        }
                        .padding()
                        .background(Color(.secondarySystemGroupedBackground))
                        .cornerRadius(16)
                        .padding(.horizontal)
                    }
                }
                .padding(.bottom, 24)
            }
            .navigationTitle("Tokyo Passport")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

public struct QuarterMilestoneCard: View {
    public let quarter: QuarterMilestone
    public let isCurrent: Bool

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
                    Text(quarter.name)
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
                    Text("Living: \(quarter.livingSkillsGoal)")
                        .font(.caption)
                        .foregroundColor(.primary.opacity(0.9))
                }

                HStack(alignment: .top, spacing: 6) {
                    Image(systemName: "book.fill")
                        .font(.caption2)
                        .foregroundColor(.purple)
                    Text("Manga: \(quarter.mangaGoal)")
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
