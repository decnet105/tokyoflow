import SwiftUI

/// TokyoMoreHubView provides a clean, Apple-style modular resource library
/// organizing all deep reference tools, media, and features into categorized modules.
public struct TokyoMoreHubView: View {
    @ObservedObject var notificationService = NotificationService.shared
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var searchText: String = ""

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 24) {
                        // Section 1: Core Reference & Vocabulary/Grammar
                        moduleSectionHeader(
                            title: languageManager.isEnglish ? "Core Tools & Lexicon" : "核心工具与词典",
                            subtitle: languageManager.isEnglish ? "Dictionaries, grammar blueprints & kana tables" : "随时查阅的词典、句型公式与五十音"
                        )
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            NavigationLink(destination: LazyView(JLPTDictionaryView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "JLPT Core Lexicon" : "JLPT 核心词典",
                                    subtitle: languageManager.isEnglish ? "2,632 Words • Studio Audio" : "2,632 词 • 原声例句",
                                    icon: "text.book.closed.fill",
                                    gradient: [Color.blue, Color.cyan]
                                )
                            }

                            NavigationLink(destination: LazyView(JLPTGrammarLabView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Grammar Blueprint Lab" : "JLPT 语法句型库",
                                    subtitle: languageManager.isEnglish ? "N5-N1 Formulas & Drills" : "N5-N1 公式与真题",
                                    icon: "list.bullet.rectangle.fill",
                                    gradient: [Color.purple, Color.indigo]
                                )
                            }

                            NavigationLink(destination: LazyView(KanaTableView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Kana Syllabary Table" : "五十音速记表",
                                    subtitle: languageManager.isEnglish ? "Hiragana • Katakana • Yoon" : "平假名 • 片假名 • 拗音",
                                    icon: "character.book.closed.fill",
                                    gradient: [Color.pink, Color.rosePink]
                                )
                            }

                            NavigationLink(destination: LazyView(WeakWordsLabView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Spaced Weak Words" : "抗遗忘错题本",
                                    subtitle: languageManager.isEnglish ? "Ebbinghaus Targeted Recall" : "艾宾浩斯弱词强化",
                                    icon: "brain.head.profile",
                                    gradient: [Color.orange, Color.yellow]
                                )
                            }
                        }

                        // Section 2: Immersive Media & Real Scenarios
                        moduleSectionHeader(
                            title: languageManager.isEnglish ? "Immersive Media & Field Drills" : "沉浸多媒体与实战演练",
                            subtitle: languageManager.isEnglish ? "Authentic Tokyo videos, NHK news & speed dojo" : "真实东京视频、新闻跟读与道场对决"
                        )
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            NavigationLink(destination: LazyView(ScenarioMapView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Tokyo Scenario Hub" : "东京实战场景库",
                                    subtitle: languageManager.isEnglish ? "76 Practical Life Scenarios" : "76 个日常用例",
                                    icon: "map.fill",
                                    gradient: [Color.teal, Color.green]
                                )
                            }

                            NavigationLink(destination: LazyView(TokyoScenarioVideoHubView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Video Masterclass" : "视频学院",
                                    subtitle: languageManager.isEnglish ? "Context Video Lessons" : "情景微课视频",
                                    icon: "play.tv.fill",
                                    gradient: [Color.red, Color.orange]
                                )
                            }

                            NavigationLink(destination: LazyView(DailyNewsFeedView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "NHK Daily News" : "NHK 每日新闻",
                                    subtitle: languageManager.isEnglish ? "Live Shadowing & Radio" : "实时跟读与电台",
                                    icon: "newspaper.fill",
                                    gradient: [Color.indigo, Color.blue]
                                )
                            }

                            NavigationLink(destination: LazyView(TokyoDojoView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Speed Dojo Reflex" : "道场极速决斗",
                                    subtitle: languageManager.isEnglish ? "3s Reflex Counter" : "3 秒条件反射",
                                    icon: "bolt.horizontal.fill",
                                    gradient: [Color.red, Color.purple]
                                )
                            }

                            NavigationLink(destination: LazyView(MangaLabView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Manga Lab" : "漫画实验室",
                                    subtitle: languageManager.isEnglish ? "Panels • Sound Effects" : "分镜阅读 • 拟声词",
                                    icon: "book.pages.fill",
                                    gradient: [Color.purple, Color.pink]
                                )
                            }

                            NavigationLink(destination: LazyView(TokyoGenerativeRouteView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "AI Route Generator" : "AI 目的地规划",
                                    subtitle: languageManager.isEnglish ? "Personalized Trails" : "个性化日语路线",
                                    icon: "sparkles.rectangle.stack.fill",
                                    gradient: [Color.blue, Color.purple]
                                )
                            }
                        }

                        // Section 3: Community & Profile
                        moduleSectionHeader(
                            title: languageManager.isEnglish ? "Community & Profile" : "社区与个人中心",
                            subtitle: languageManager.isEnglish ? "Tokyo resident chats, inbox & learning passport" : "东京居民交流、消息与个人护照"
                        )
                        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
                            NavigationLink(destination: LazyView(TokyoSocialHubView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Tokyo Citizen Lounge" : "东京社区交流",
                                    subtitle: languageManager.isEnglish ? "Izakaya & Kombini Talk" : "居酒屋 • 便利店漫谈",
                                    icon: "bubble.left.and.bubble.right.fill",
                                    gradient: [Color.cyan, Color.blue]
                                )
                            }

                            NavigationLink(destination: LazyView(TokyoPassportView())) {
                                moduleTile(
                                    title: languageManager.isEnglish ? "Study Passport & Goals" : "学习档案与护照",
                                    subtitle: languageManager.isEnglish ? "Streaks • Milestones" : "连续天数 • 进度设置",
                                    icon: "person.text.rectangle.fill",
                                    gradient: [Color.purple, Color.blue]
                                )
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 16)
                    .padding(.bottom, 32)
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Explore & Toolkit" : "探索与工具")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button(action: {
                        UIImpactFeedbackGenerator(style: .light).impactOccurred()
                        languageManager.toggleEnglishChinese()
                    }) {
                        HStack(spacing: 4) {
                            Image(systemName: "globe")
                                .font(.caption2)
                            Text(languageManager.isEnglish ? "EN" : "中文")
                                .font(.caption2)
                                .fontWeight(.bold)
                        }
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.accentColor.opacity(0.12))
                        .foregroundColor(.accentColor)
                        .cornerRadius(8)
                    }
                }
            }
        }
    }

    private func moduleSectionHeader(title: String, subtitle: String) -> some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(title)
                .font(.headline)
                .fontWeight(.black)
                .foregroundColor(.primary)

            Text(subtitle)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.top, 8)
    }

    private func moduleTile(title: String, subtitle: String, icon: String, gradient: [Color]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            ZStack {
                Circle()
                    .fill(
                        LinearGradient(
                            colors: gradient,
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 42, height: 42)

                Image(systemName: icon)
                    .font(.system(size: 18))
                    .foregroundColor(.white)
            }

            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.system(size: 14, weight: .bold, design: .rounded))
                    .foregroundColor(.primary)
                    .lineLimit(1)

                Text(subtitle)
                    .font(.system(size: 11))
                    .foregroundColor(.secondary)
                    .lineLimit(1)
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(UIColor.secondarySystemGroupedBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.04), radius: 6, y: 2)
    }
}

extension Color {
    static let rosePink = Color(red: 0.95, green: 0.35, blue: 0.55)
}
