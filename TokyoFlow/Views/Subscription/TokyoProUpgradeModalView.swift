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

                            Text("TokyoFlow 免费全能成长计划")
                                .font(.system(size: 22, weight: .black, design: .rounded))
                                .foregroundColor(.primary)

                            Text("为了快速冲体量与服务广大日语学习者，App 内全量功能当前 100% 免费开放！关注官方 YouTube 频道即可领取早期共创福利。")
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 24)
                        }
                        .padding(.top, 16)

                        // 100% Free Full Power Checklist
                        VStack(spacing: 12) {
                            HStack {
                                Text("✨ 当前全部核心功能 100% 免费开放")
                                    .font(.system(size: 14, weight: .black))
                                    .foregroundColor(.green)
                                Spacer()
                                Text("无限制畅学")
                                    .font(.system(size: 10, weight: .bold))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(Color.green.opacity(0.15))
                                    .foregroundColor(.green)
                                    .cornerRadius(6)
                            }

                            VStack(spacing: 8) {
                                perkRow(icon: "checkmark.seal.fill", title: "JLPT N1-N5 词库 & 抽认卡", desc: "4,170 个原生母语发音全量免费查背")
                                perkRow(icon: "checkmark.seal.fill", title: "NHK 慢速原声跟读 & 1小时电台", desc: "毫秒级发音同步对齐与智能滚屏")
                                perkRow(icon: "checkmark.seal.fill", title: "次はどこへ行く？Generative UI", desc: "全东京任意目的地实战句型即时动态生成")
                                perkRow(icon: "checkmark.seal.fill", title: "全东京实景场景 & 3秒道场", desc: "电车/便利店/居酒屋等真实生活全关卡")
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
                                    Text("关注 YouTube 官方教学频道")
                                        .font(.system(size: 15, weight: .bold))
                                    Text("TokyoFlow Japanese / TokyoFlow 日语")
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

                            Text("前往 YouTube 关注我们的官方频道，不仅能获取最新东京实景教学视频，还可以一键领取 500 Tokyo Points 与「早期共创先锋」勋章！")
                                .font(.footnote)
                                .foregroundColor(.secondary)

                            Button(action: {
                                if let url = URL(string: "https://www.youtube.com") {
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
                                    Text(hasClaimedYTReward ? "已关注并领取奖励 • 前往频道" : "立即关注并领取 500 TP 奖励")
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
                            Text("💖 喜欢 TokyoFlow？支持我们持续创作")
                                .font(.system(size: 13, weight: .bold))
                                .foregroundColor(.secondary)

                            HStack(spacing: 12) {
                                Button(action: {
                                    subService.purchase(plan: .monthly) { _ in }
                                }) {
                                    VStack(spacing: 4) {
                                        Text("☕️ 请喝一杯咖啡")
                                            .font(.system(size: 12, weight: .bold))
                                        Text("¥12 / 鼓励创作")
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
                                        Text("👑 成为终身共创者")
                                            .font(.system(size: 12, weight: .bold))
                                            .foregroundColor(.orange)
                                        Text("专属 VIP 勋章")
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
            .navigationTitle("免费全能计划")
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
            .alert("🎉 奖励已到账！", isPresented: $showSuccessAlert) {
                Button("太棒了") { dismiss() }
            } message: {
                Text("已成功发放 500 Tokyo Points 与 300 经验值！感谢您对 TokyoFlow Japanese 官方频道的支持。")
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
