import SwiftUI

public struct MainTabView: View {
    @StateObject private var userProfile = UserProfile()
    @StateObject private var dataManager = DataManager.shared
    @StateObject private var gamification = GamificationService.shared
    @StateObject private var themeManager = ThemeManager.shared
    @ObservedObject private var notificationService = NotificationService.shared
    @ObservedObject private var languageManager = LanguageManager.shared
    @AppStorage("main_selected_tab_index") private var selectedTab: Int = 0

    public init() {}

    public var body: some View {
        TabView(selection: $selectedTab) {
            TokyoClassroomHomeView()
                .tabItem {
                    Label(languageManager.isEnglish ? "Classroom" : "今日・教室", systemImage: "graduationcap.fill")
                }
                .tag(0)

            TokyoQuestMapView()
                .tabItem {
                    Label(languageManager.isEnglish ? "Quest Map" : "进阶地图", systemImage: "map.fill")
                }
                .tag(1)

            TokyoMoreHubView()
                .tabItem {
                    Label(languageManager.isEnglish ? "Explore & Tools" : "探索与工具", systemImage: "square.grid.2x2.fill")
                }
                .tag(2)

            TokyoPassportView()
                .tabItem {
                    Label(languageManager.isEnglish ? "Passport" : "学习档案", systemImage: "person.text.rectangle.fill")
                }
                .tag(3)
        }
        .environmentObject(userProfile)
        .environmentObject(dataManager)
        .environmentObject(gamification)
        .environmentObject(themeManager)
        .sheet(isPresented: $notificationService.showNightlySummarySheet) {
            if let msg = notificationService.selectedSummaryMessage {
                TokyoNightlySummaryModalView(message: msg)
            }
        }
        .sheet(isPresented: $notificationService.showMessageCenterSheet) {
            TokyoMessageCenterView()
        }
        .tint(.accentColor)
    }
}
