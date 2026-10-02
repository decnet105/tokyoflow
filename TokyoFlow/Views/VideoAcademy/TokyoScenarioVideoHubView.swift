import SwiftUI

public struct TokyoScenarioVideoHubView: View {
    @StateObject private var videoManager = TokyoVideoLessonDataManager.shared
    @ObservedObject private var languageManager = LanguageManager.shared
    @State private var selectedLesson: TokyoScenarioVideoLesson? = nil
    @State private var filterCategory: String = "all"
    @State private var searchQuery: String = ""
    @Environment(\.openURL) private var openURL

    public init() {}

    private var filteredLessons: [TokyoScenarioVideoLesson] {
        videoManager.lessons.filter { lesson in
            let catMatch = (filterCategory == "all" || lesson.category == filterCategory)
            let q = searchQuery.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
            if q.isEmpty { return catMatch }
            return catMatch && (
                lesson.title.lowercased().contains(q) ||
                (lesson.titleZh?.lowercased().contains(q) ?? false) ||
                lesson.titleJa.lowercased().contains(q) ||
                lesson.district.lowercased().contains(q)
            )
        }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                    VStack(spacing: 16) {
                        // Hero Header Card
                        VStack(alignment: .leading, spacing: 10) {
                            HStack {
                                Label(languageManager.isEnglish ? "YOUTUBE SCENARIO ACADEMY" : "场景实战视频学院", systemImage: "play.tv.fill")
                                    .font(.system(size: 11, weight: .black))
                                    .foregroundColor(.red)
                                    .tracking(1.0)
                                Spacer()
                                Text(languageManager.isEnglish ? "In-App View • YouTube Flow" : "应用内无缝播放 • YouTube 沉浸流")
                                    .font(.system(size: 9, weight: .bold))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 3)
                                    .background(Color.red.opacity(0.15))
                                    .foregroundColor(.red)
                                    .cornerRadius(6)
                            }

                            Text(languageManager.isEnglish ? "Tokyo Scenario Native Video Lessons" : "东京实战场景原声视频课")
                                .font(.system(size: 20, weight: .black, design: .rounded))

                            Text(languageManager.isEnglish ? "Master 20+ authentic Tokyo situations (train announcements, kombini checkout, izakaya ordering, Akiba anime hunting) with natural Japanese audio & English breakdowns." : "掌握东京电车广播、便利店极速结账、居酒屋点餐AA制、秋叶原手办免税等20+地道场景，纯正真人原声与精讲拆解。")
                                .font(.caption)
                                .foregroundColor(.secondary)

                            // Channel Subscribe Banner
                            Button(action: {
                                if let url = URL(string: "https://www.youtube.com") {
                                    openURL(url)
                                }
                            }) {
                                HStack(spacing: 8) {
                                    Image(systemName: "bell.fill")
                                        .foregroundColor(.red)
                                    Text(languageManager.isEnglish ? "Subscribe to TokyoFlow Official YouTube" : "订阅 TokyoFlow 官方 YouTube 频道")
                                        .font(.system(size: 12, weight: .bold))
                                        .foregroundColor(.primary)
                                    Spacer()
                                    Image(systemName: "arrow.up.right.circle.fill")
                                        .foregroundColor(.red)
                                }
                                .padding(10)
                                .background(Color.red.opacity(0.08))
                                .cornerRadius(10)
                            }
                        }
                        .padding()
                        .background(.ultraThinMaterial)
                        .cornerRadius(18)
                        .padding(.horizontal)
                        .padding(.top, 6)

                        // Search Bar
                        HStack {
                            Image(systemName: "magnifyingglass")
                                .foregroundColor(.secondary)
                            TextField(languageManager.isEnglish ? "Search scenario video lessons..." : "搜索场景视频课程...", text: $searchQuery)
                            if !searchQuery.isEmpty {
                                Button(action: { searchQuery = "" }) {
                                    Image(systemName: "xmark.circle.fill")
                                        .foregroundColor(.secondary)
                                }
                            }
                        }
                        .padding(10)
                        .background(.ultraThinMaterial)
                        .cornerRadius(12)
                        .padding(.horizontal)

                        // Category Filter Chips
                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 8) {
                                categoryFilterButton(languageManager.isEnglish ? "All Scenarios" : "全部场景", category: "all")
                                categoryFilterButton(languageManager.isEnglish ? "Train & Subway" : "电车与地铁", category: "transit")
                                categoryFilterButton(languageManager.isEnglish ? "Kombini" : "便利店", category: "kombini")
                                categoryFilterButton(languageManager.isEnglish ? "Izakaya & Dining" : "居酒屋与餐饮", category: "dining")
                                categoryFilterButton(languageManager.isEnglish ? "Shopping & Anime" : "购物与动漫", category: "shopping")
                            }
                            .padding(.horizontal)
                        }

                        // Video Lessons Grid / List
                        VStack(spacing: 14) {
                            ForEach(filteredLessons) { lesson in
                                TokyoVideoHubCardView(lesson: lesson) {
                                    selectedLesson = lesson
                                }
                            }
                        }
                        .padding(.horizontal)
                        .padding(.bottom, 30)
                    }
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Video Academy" : "视频学院")
            .sheet(item: $selectedLesson) { lesson in
                TokyoScenarioYTPlayerView(lesson: lesson)
            }
        }
    }

    private func categoryFilterButton(_ title: String, category: String) -> some View {
        let isSelected = (filterCategory == category)
        return Button(action: { filterCategory = category }) {
            Text(title)
                .font(.caption)
                .fontWeight(.bold)
                .padding(.horizontal, 12)
                .padding(.vertical, 7)
                .background(isSelected ? Color.red : Color.gray.opacity(0.15))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(12)
        }
    }
}

// MARK: - Video Card Row Component
struct TokyoVideoHubCardView: View {
    let lesson: TokyoScenarioVideoLesson
    let onSelect: () -> Void

    var body: some View {
        Button(action: onSelect) {
            VStack(alignment: .leading, spacing: 0) {
                // Real YouTube HD Thumbnail & Video Card Header
                ZStack(alignment: .bottomTrailing) {
                    AsyncImage(url: lesson.hqThumbnailUrl) { phase in
                        if let img = phase.image {
                            img.resizable()
                               .aspectRatio(16/9, contentMode: .fill)
                        } else {
                            LinearGradient(
                                colors: [Color(hex: "#1E293B"), Color(hex: "#0F172A")],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        }
                    }
                    .frame(height: 160)
                    .clipped()
                    .cornerRadius(14)

                    // Vignette Gradient Overlay
                    LinearGradient(
                        colors: [Color.black.opacity(0.1), Color.black.opacity(0.75)],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                    .frame(height: 160)
                    .cornerRadius(14)

                    // Central Play Icon & District
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Image(systemName: lesson.thumbnailIcon)
                                    .font(.caption)
                                Text(lesson.district)
                                    .font(.system(size: 11, weight: .bold))
                            }
                            .foregroundColor(.white.opacity(0.9))

                            Text(lesson.titleJa)
                                .font(.system(size: 15, weight: .bold))
                                .foregroundColor(.white)
                                .lineLimit(1)
                        }
                        Spacer()

                        ZStack {
                            Circle()
                                .fill(Color.red)
                                .frame(width: 44, height: 44)
                                .shadow(color: Color.red.opacity(0.6), radius: 8, x: 0, y: 3)
                            Image(systemName: "play.fill")
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(.white)
                                .offset(x: 1)
                        }
                    }
                    .padding(14)

                    // Duration Badge
                    Text(lesson.durationLabel)
                        .font(.system(size: 10, weight: .bold, design: .monospaced))
                        .padding(.horizontal, 6)
                        .padding(.vertical, 3)
                        .background(Color.black.opacity(0.75))
                        .foregroundColor(.white)
                        .cornerRadius(4)
                        .padding(10)
                }

                // Card Footer
                VStack(alignment: .leading, spacing: 6) {
                    HStack {
                        Text(lesson.levelBadge)
                            .font(.system(size: 9, weight: .bold))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.orange.opacity(0.2))
                            .foregroundColor(.orange)
                            .cornerRadius(4)

                        Spacer()

                        Text(LanguageManager.shared.isEnglish ? "\(lesson.chapters.count) Chapters" : "\(lesson.chapters.count) 个精讲章节")
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }

                    Text(lesson.localizedTitle)
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(.primary)
                        .multilineTextAlignment(.leading)
                        .lineLimit(2)

                    Text(lesson.localizedSummary)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                        .multilineTextAlignment(.leading)
                }
                .padding(12)
            }
            .background(.ultraThinMaterial)
            .cornerRadius(16)
            .shadow(color: Color.black.opacity(0.04), radius: 6, x: 0, y: 2)
        }
        .buttonStyle(PlainButtonStyle())
    }
}
