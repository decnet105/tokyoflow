import SwiftUI

@main
struct TokyoFlowApp: App {
    var body: some Scene {
        WindowGroup {
            MainTabView()
                .onAppear {
                    NotificationService.shared.requestNotificationPermission()
                }
        }
    }
}
