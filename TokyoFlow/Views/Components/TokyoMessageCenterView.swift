import SwiftUI

public struct TokyoMessageCenterView: View {
    @ObservedObject private var notificationService = NotificationService.shared
    @Environment(\.dismiss) private var dismiss
    @State private var selectedFilter: MessageFilter = .all
    @State private var activeSummaryForSheet: TokyoAppMessage? = nil

    public enum MessageFilter: String, CaseIterable, Identifiable {
        case all = "すべて"
        case summaries = "21:00日報"
        case system = "お知らせ"

        public var id: String { rawValue }
    }

    public init() {}

    public var filteredMessages: [TokyoAppMessage] {
        switch selectedFilter {
        case .all:
            return notificationService.messages
        case .summaries:
            return notificationService.messages.filter { $0.type == .nightlySummary }
        case .system:
            return notificationService.messages.filter { $0.type == .system || $0.type == .streakMilestone || $0.type == .scenarioUnlocked }
        }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 0) {
                    // Filter Picker & Actions
                    VStack(spacing: 12) {
                        Picker("Filter", selection: $selectedFilter) {
                            ForEach(MessageFilter.allCases) { filter in
                                Text(filter.rawValue).tag(filter)
                            }
                        }
                        .pickerStyle(.segmented)
                        .padding(.horizontal)

                        HStack {
                            Text("未読 \(notificationService.unreadCount) 件")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(notificationService.unreadCount > 0 ? .red : .secondary)

                            Spacer()

                            Button {
                                withAnimation {
                                    notificationService.markAllAsRead()
                                }
                            } label: {
                                Label("すべて既読にする", systemImage: "checkmark.circle")
                                    .font(.caption)
                                    .foregroundColor(.purple)
                            }

                            Button {
                                withAnimation {
                                    let summary = notificationService.generateTodayNightlySummary()
                                    activeSummaryForSheet = summary
                                }
                            } label: {
                                Label("今夜のまとめ作成", systemImage: "sparkles")
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.white)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 4)
                                    .background(Capsule().fill(Color.purple))
                            }
                        }
                        .padding(.horizontal)
                    }
                    .padding(.vertical, 8)
                    .background(Color(UIColor.secondarySystemBackground).opacity(0.8))

                    // Message List
                    if filteredMessages.isEmpty {
                        VStack(spacing: 16) {
                            Spacer()
                            Image(systemName: "tray.fill")
                                .font(.system(size: 56))
                                .foregroundColor(.secondary.opacity(0.5))
                            Text("メッセージはありません")
                                .font(.headline)
                                .foregroundColor(.secondary)
                            Text("毎晩21:00の学習レポートやお知らせがここに届きます")
                                .font(.caption)
                                .foregroundColor(.secondary.opacity(0.8))
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 40)
                            Spacer()
                        }
                    } else {
                        List {
                            ForEach(filteredMessages) { msg in
                                messageRow(for: msg)
                                    .listRowBackground(Color(UIColor.secondarySystemBackground).opacity(msg.isRead ? 0.4 : 0.9))
                                    .listRowInsets(EdgeInsets(top: 10, leading: 14, bottom: 10, trailing: 14))
                                    .onTapGesture {
                                        notificationService.markAsRead(id: msg.id)
                                        if msg.type == .nightlySummary {
                                            activeSummaryForSheet = msg
                                        }
                                    }
                            }
                            .onDelete { indexSet in
                                for idx in indexSet {
                                    let msg = filteredMessages[idx]
                                    notificationService.deleteMessage(id: msg.id)
                                }
                            }
                        }
                        .listStyle(.insetGrouped)
                    }
                }
            }
            .navigationTitle("メッセージセンター")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("閉じる") {
                        dismiss()
                    }
                    .fontWeight(.bold)
                }
            }
            .sheet(item: $activeSummaryForSheet) { summary in
                TokyoNightlySummaryModalView(message: summary)
            }
        }
    }

    private func messageRow(for msg: TokyoAppMessage) -> some View {
        HStack(alignment: .top, spacing: 14) {
            // Icon
            ZStack {
                Circle()
                    .fill(iconBackgroundColor(for: msg.type))
                    .frame(width: 44, height: 44)

                Image(systemName: iconName(for: msg.type))
                    .font(.system(size: 20))
                    .foregroundColor(.white)
            }

            // Body
            VStack(alignment: .leading, spacing: 4) {
                HStack {
                    Text(msg.title)
                        .font(.subheadline)
                        .fontWeight(msg.isRead ? .semibold : .black)
                        .foregroundColor(.primary)
                        .lineLimit(1)

                    Spacer()

                    if !msg.isRead {
                        Circle()
                            .fill(Color.red)
                            .frame(width: 8, height: 8)
                    }

                    Text(msg.formattedDate)
                        .font(.system(size: 11))
                        .foregroundColor(.secondary)
                }

                Text(msg.subtitle)
                    .font(.caption)
                    .fontWeight(.medium)
                    .foregroundColor(.purple)
                    .lineLimit(1)

                Text(msg.body)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)

                // Extra tags for 9 PM Summary
                if msg.type == .nightlySummary {
                    HStack(spacing: 8) {
                        if let mins = msg.minutesLearned {
                            Label("\(mins)分", systemImage: "clock")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(.blue)
                        }
                        if let tp = msg.tpEarned {
                            Label("+\(tp) TP", systemImage: "sparkles")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(.orange)
                        }
                        if let streak = msg.streak {
                            Label("\(streak)日連続", systemImage: "flame.fill")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(.red)
                        }

                        Spacer()

                        Text("レポートを見る ›")
                            .font(.system(size: 11, weight: .black))
                            .foregroundColor(.purple)
                    }
                    .padding(.top, 4)
                }
            }
        }
        .padding(.vertical, 4)
    }

    private func iconName(for type: TokyoMessageType) -> String {
        switch type {
        case .nightlySummary:
            return "moon.stars.fill"
        case .streakMilestone:
            return "flame.fill"
        case .scenarioUnlocked:
            return "trophy.fill"
        case .system:
            return "bell.fill"
        }
    }

    private func iconBackgroundColor(for type: TokyoMessageType) -> Color {
        switch type {
        case .nightlySummary:
            return Color.purple
        case .streakMilestone:
            return Color.red
        case .scenarioUnlocked:
            return Color.orange
        case .system:
            return Color.blue
        }
    }
}
