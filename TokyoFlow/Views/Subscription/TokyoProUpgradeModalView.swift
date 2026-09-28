import SwiftUI

public struct TokyoProUpgradeModalView: View {
    @StateObject private var subService = SubscriptionService.shared
    @Environment(\.dismiss) private var dismiss
    @State private var isProcessing: Bool = false
    @State private var showSuccessAlert: Bool = false

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
                                        LinearGradient(colors: [.orange, .red], startPoint: .topLeading, endPoint: .bottomTrailing)
                                    )
                                    .frame(width: 76, height: 76)
                                    .shadow(color: .orange.opacity(0.4), radius: 12, y: 6)

                                Image(systemName: "crown.fill")
                                    .font(.system(size: 38))
                                    .foregroundColor(.white)
                            }

                            Text("TokyoFlow PASS プレミアム")
                                .font(.system(size: 24, weight: .black, design: .rounded))
                                .foregroundColor(.primary)

                            Text("解锁全套 N1-N5 必备核心词库、无限制弱点 AI 诊断与全景东京场景")
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 24)
                        }
                        .padding(.top, 16)

                        // Freemium Balance Comparison Table
                        VStack(spacing: 12) {
                            Text("👑 免费版 (60%) 与 PASS 会员对比")
                                .font(.system(size: 14, weight: .bold))
                                .foregroundColor(.accentColor)

                            VStack(spacing: 8) {
                                comparisonRow(title: "五十音全图 & 7天不重复真人单词", free: "永久免费", pro: "永久免费", isHighlight: false)
                                comparisonRow(title: "每日 NHK 新闻跟读 & 1小时广播", free: "永久免费", pro: "永久免费", isHighlight: false)
                                comparisonRow(title: "基础生词本复习 (每日 15 词)", free: "支持", pro: "无限量", isHighlight: false)
                                comparisonRow(title: "JLPT N1-N5 必备核心词库 & 抽认卡", free: "仅限 N5", pro: "全级别 N1-N5", isHighlight: true)
                                comparisonRow(title: "AI 弱点诊断 (重听/停顿自动追踪)", free: "基础版", pro: "智能闭环分析", isHighlight: true)
                                comparisonRow(title: "全东京实景场景 & 3秒忍者道场", free: "前2关体验", pro: "全量解锁", isHighlight: true)
                                comparisonRow(title: "东京地铁 4K 壁纸 & 离线原生发音包", free: "基础壁纸", pro: "全量 4K + 离线", isHighlight: true)
                            }
                        }
                        .padding(16)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)

                        // Plan Selector Cards
                        VStack(spacing: 10) {
                            ForEach(SubscriptionPlan.allCases) { plan in
                                let isSelected = subService.selectedPlan == plan

                                Button(action: {
                                    withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
                                        subService.selectedPlan = plan
                                    }
                                }) {
                                    HStack {
                                        VStack(alignment: .leading, spacing: 2) {
                                            HStack(spacing: 6) {
                                                Text(plan.rawValue)
                                                    .font(.system(size: 15, weight: .bold))
                                                if let badge = plan.badgeText {
                                                    Text(badge)
                                                        .font(.system(size: 9, weight: .black))
                                                        .foregroundColor(.white)
                                                        .padding(.horizontal, 6)
                                                        .padding(.vertical, 2)
                                                        .background(Color.orange)
                                                        .cornerRadius(6)
                                                }
                                            }
                                            Text(plan.priceString)
                                                .font(.caption)
                                                .foregroundColor(isSelected ? .accentColor : .secondary)
                                        }

                                        Spacer()

                                        Image(systemName: isSelected ? "checkmark.circle.fill" : "circle")
                                            .font(.title3)
                                            .foregroundColor(isSelected ? .accentColor : .secondary)
                                    }
                                    .padding(14)
                                    .background(isSelected ? Color.accentColor.opacity(0.12) : Color(UIColor.secondarySystemBackground).opacity(0.6))
                                    .cornerRadius(16)
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 16)
                                            .stroke(isSelected ? Color.accentColor : Color.clear, lineWidth: 1.5)
                                    )
                                }
                            }
                        }
                        .padding(.horizontal)

                        // Subscribe Action Button
                        VStack(spacing: 10) {
                            Button(action: {
                                isProcessing = true
                                subService.purchase(plan: subService.selectedPlan) { success in
                                    isProcessing = false
                                    if success {
                                        showSuccessAlert = true
                                    }
                                }
                            }) {
                                HStack {
                                    if isProcessing {
                                        ProgressView()
                                            .tint(.white)
                                    } else {
                                        Image(systemName: "sparkles")
                                        Text(subService.selectedPlan == .annual ? "开始 7 天免费试用" : "立即升级 PASS")
                                            .font(.headline)
                                            .fontWeight(.bold)
                                    }
                                }
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .padding(.vertical, 15)
                                .background(
                                    LinearGradient(colors: [.orange, .red], startPoint: .leading, endPoint: .trailing)
                                )
                                .cornerRadius(16)
                                .shadow(color: .orange.opacity(0.3), radius: 10, y: 5)
                            }
                            .disabled(isProcessing)

                            // Restore & Terms
                            HStack(spacing: 16) {
                                Button("恢复购买") {
                                    subService.restorePurchases { _ in }
                                }
                                Text("•")
                                Button("隐私政策") {}
                                Text("•")
                                Button("使用条款") {}
                            }
                            .font(.caption2)
                            .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)
                        .padding(.bottom, 30)
                    }
                }
            }
            .navigationTitle("升级会员")
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
            .alert("🎉 升级成功！", isPresented: $showSuccessAlert) {
                Button("开启东京之旅") { dismiss() }
            } message: {
                Text("您已成功开通 TokyoFlow PASS，全量 JLPT 词库与高级场景已全部解锁！")
            }
        }
    }

    private func comparisonRow(title: String, free: String, pro: String, isHighlight: Bool) -> some View {
        HStack(alignment: .center) {
            Text(title)
                .font(.system(size: 12, weight: isHighlight ? .bold : .regular))
                .foregroundColor(.primary)
            Spacer()
            Text(free)
                .font(.system(size: 11))
                .foregroundColor(.secondary)
                .frame(width: 80, alignment: .trailing)
            Text(pro)
                .font(.system(size: 11, weight: .bold))
                .foregroundColor(isHighlight ? .orange : .accentColor)
                .frame(width: 80, alignment: .trailing)
        }
        .padding(.vertical, 3)
    }
}
