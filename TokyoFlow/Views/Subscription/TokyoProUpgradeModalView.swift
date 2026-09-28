import SwiftUI

public struct TokyoProUpgradeModalView: View {
    @StateObject private var subService = SubscriptionService.shared
    @ObservedObject private var gamification = GamificationService.shared
    @Environment(\.dismiss) private var dismiss
    @Environment(\.openURL) private var openURL
    @State private var isProcessing: Bool = false
    @State private var showSuccessAlert: Bool = false
    @State private var hasClaimedYTReward: Bool = false

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 20) {
                        // Hero Header
                        VStack(spacing: 8) {
                            ZStack {
                                Circle()
                                    .fill(
                                        LinearGradient(colors: [.red, .orange], startPoint: .topLeading, endPoint: .bottomTrailing)
                                    )
                                    .frame(width: 76, height: 76)
                                    .shadow(color: .red.opacity(0.3), radius: 12, y: 6)

                                Image(systemName: "play.tv.fill")
                                    .font(.system(size: 36))
                                    .foregroundColor(.white)
                            }

                            Text("TokyoFlow Full Access Plan")
                                .font(.system(size: 22, weight: .black, design: .rounded))
                                .foregroundColor(.primary)

                            Text("To empower Japanese learners worldwide, all core features are currently 100% free! Subscribe to our official YouTube channel to claim your early co-creator rewards.")
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 24)
                        }
                        .padding(.top, 16)

                        // 100% Free Full Power Checklist
                        VStack(spacing: 12) {
                            HStack {
                                Text("✨ All Core Features 100% Free")
                                    .font(.system(size: 14, weight: .black))
                                    .foregroundColor(.green)
                                Spacer()
                                Text("UNLIMITED")
                                    .font(.system(size: 10, weight: .bold))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.green.opacity(0.15))
                                    .foregroundColor(.green)
                                    .cornerRadius(6)
                            }

                            VStack(spacing: 8) {
                                perkRow(icon: "checkmark.seal.fill", title: "JLPT N1-N5 Lexicon & Flashcards", desc: "4,170 native audio pronunciations with pitch accent")
                                perkRow(icon: "checkmark.seal.fill", title: "NHK News Shadowing & 1-Hour Radio", desc: "Millisecond-precise audio sync with continuous flow")
                                perkRow(icon: "checkmark.seal.fill", title: "Next Destination? Generative UI", desc: "Dynamic survival Japanese generator for any Tokyo spot")
                                perkRow(icon: "checkmark.seal.fill", title: "Real-world Tokyo Scenarios & 3s Dojo", desc: "Transit, convenience stores, izakaya & emergency drills")
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // YouTube Official Channel Integration Card
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Image(systemName: "bell.badge.fill")
                                    .foregroundColor(.red)
                                    .font(.title3)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("Official YouTube Channel")
                                        .font(.system(size: 15, weight: .bold))
                                    Text("@TokyoFlowJapanese")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                Spacer()
                                Text("+500 TP")
                                    .font(.system(size: 11, weight: .black))
                                    .padding(.horizontal, 8)
                                    .padding(.vertical, 3)
                                    .background(Color.red.opacity(0.15))
                                    .foregroundColor(.red)
                                    .cornerRadius(8)
                            }

                            Text("Subscribe to our YouTube channel for immersive Tokyo video lessons and instantly receive 500 Tokyo Points + Early Pioneer Badge!")
                                .font(.footnote)
                                .foregroundColor(.secondary)

                            Button(action: {
                                if let url = URL(string: "https://www.youtube.com/@TokyoFlowJapanese") {
                                    openURL(url)
                                }
                                if !hasClaimedYTReward {
                                    gamification.addRewards(tp: 500, exp: 300)
                                    hasClaimedYTReward = true
                                    showSuccessAlert = true
                                }
                            }) {
                                HStack {
                                    Image(systemName: "play.rectangle.fill")
                                    Text(hasClaimedYTReward ? "Subscribed • Visit Channel" : "Subscribe & Claim 500 TP")
                                        .font(.system(size: 14, weight: .bold))
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 12)
                                .background(Color.red)
                                .cornerRadius(12)
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // Optional Coffee / Community Supporter Card
                        VStack(spacing: 10) {
                            Text("💖 Enjoying TokyoFlow? Support our creation")
                                .font(.system(size: 13, weight: .bold))
                                .foregroundColor(.secondary)

                            HStack(spacing: 12) {
                                Button(action: {
                                    subService.purchase(plan: .monthly) { _ in }
                                }) {
                                    VStack(spacing: 4) {
                                        Text("☕️ Buy Us a Coffee")
                                            .font(.system(size: 12, weight: .bold))
                                        Text("$1.99 / Support")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 10)
                                    .background(Color(.secondarySystemGroupedBackground))
                                    .cornerRadius(12)
                                }
                                .buttonStyle(.plain)

                                Button(action: {
                                    subService.purchase(plan: .lifetime) { _ in }
                                }) {
                                    VStack(spacing: 4) {
                                        Text("👑 Lifetime Supporter")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(.orange)
                                        Text("VIP Badge")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                    .frame(maxWidth: .infinity)
                                    .padding(.vertical, 10)
                                    .background(Color(.secondarySystemGroupedBackground))
                                    .cornerRadius(12)
                                }
                                .buttonStyle(.plain)
                            }
                        }
                        .padding(.horizontal)
                        .padding(.bottom, 30)
                    }
                }
            }
            .navigationTitle("TokyoFlow Growth Pass")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: { dismiss() }) {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundColor(.secondary)
                            .font(.title3)
                    }
                }
            }
            .alert("🎉 Rewards Claimed!", isPresented: $showSuccessAlert) {
                Button("Awesome") { dismiss() }
            } message: {
                Text("Successfully granted 500 Tokyo Points and 300 EXP! Thank you for supporting TokyoFlow.")
            }
        }
    }

    private func perkRow(icon: String, title: String, desc: String) -> some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: icon)
                .foregroundColor(.green)
                .font(.system(size: 16))
                .padding(.top, 2)
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundColor(.primary)
                Text(desc)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
        }
        .padding(.vertical, 2)
    }
}
