import SwiftUI

public struct MainTabView: View {
    @StateObject private var userProfile = UserProfile()
    @StateObject private var dataManager = DataManager.shared

    public init() {}

    public var body: some View {
        TabView {
            TokyoQuestMapView()
                .tabItem {
                    Label("Quest Map", systemImage: "flag.2.crossed.fill")
                }

            ScenarioMapView()
                .tabItem {
                    Label("Scenarios", systemImage: "map.fill")
                }

            TokyoDojoView()
                .tabItem {
                    Label("Dojo Battles", systemImage: "flame.fill")
                }

            MangaLabView()
                .tabItem {
                    Label("Manga Lab", systemImage: "book.pages.fill")
                }

            TokyoAudioLabView()
                .tabItem {
                    Label("Audio Lab", systemImage: "headphones")
                }

            SurvivalCheatSheetView()
                .tabItem {
                    Label("Survival Kit", systemImage: "bolt.shield.fill")
                }

            TokyoPassportView()
                .tabItem {
                    Label("Passport", systemImage: "person.text.rectangle.fill")
                }
        }
        .environmentObject(userProfile)
        .environmentObject(dataManager)
        .tint(.accentColor)
    }
}
