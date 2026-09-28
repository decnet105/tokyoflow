import SwiftUI

public struct MainTabView: View {
    @StateObject private var userProfile = UserProfile()
    @StateObject private var dataManager = DataManager.shared
    @StateObject private var gamification = GamificationService.shared
    @StateObject private var themeManager = ThemeManager.shared

    public init() {}

    public var body: some View {
        TabView {
            TokyoQuestMapView()
                .tabItem {
                    Label("Quest Map", systemImage: "flag.2.crossed.fill")
                }

            KanaTableView()
                .tabItem {
                    Label("Kana 五十音", systemImage: "character.book.closed.fill")
                }

            JLPTDictionaryView()
                .tabItem {
                    Label("词典 / 背词", systemImage: "text.book.closed.fill")
                }

            DailyNewsFeedView()
                .tabItem {
                    Label("Daily News", systemImage: "newspaper.fill")
                }

            ScenarioMapView()
                .tabItem {
                    Label("Scenarios", systemImage: "map.fill")
                }

            TokyoGenerativeRouteView()
                .tabItem {
                    Label("Next 目的地", systemImage: "sparkles.rectangle.stack.fill")
                }

            TokyoScenarioVideoHubView()
                .tabItem {
                    Label("YT 场景视频", systemImage: "play.tv.fill")
                }

            TokyoDojoView()
                .tabItem {
                    Label("Dojo Battles", systemImage: "flame.fill")
                }

            MangaLabView()
                .tabItem {
                    Label("Manga Lab", systemImage: "book.pages.fill")
                }

            TokyoSocialHubView()
                .tabItem {
                    Label("Tokyo Social", systemImage: "bubble.left.and.bubble.right.fill")
                }

            TokyoPassportView()
                .tabItem {
                    Label("Passport", systemImage: "person.text.rectangle.fill")
                }
        }
        .environmentObject(userProfile)
        .environmentObject(dataManager)
        .environmentObject(gamification)
        .environmentObject(themeManager)
        .tint(.accentColor)
    }
}
