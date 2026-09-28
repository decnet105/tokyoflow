import SwiftUI

public struct TokyoScenarioVideoHubView: View {
    @StateObject private var videoManager = TokyoVideoLessonDataManager.shared
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
                                Label("YOUTUBE SCENARIO ACADEMY", systemImage: "play.tv.fill")
                                    .font(.system(size: 11, weight: .black))
                                    .foregroundColor(.red)
                                    .tracking(1.0)
                                Spacer()
                                Text("APP观看 • YT计流")
                                    .font(.system(size: 9, weight: .bold))
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 3)
                                    .background(Color.red.opacity(0.15))
                                    .foregroundColor(.red)
                                    .cornerRadius(6)
                            }

                            Text("东京场景原声视频精讲")
                                .font(.system(size: 20, weight: .black, design: .rounded))

                            Text("对标 YouTube Top3 日语教学精华，每集 8~12 分钟实景拆解东京 20+ 真实场景（电车广播、便利店、居酒屋、秋叶原等）。")
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
                                    Text("关注 TokyoFlow 官方 YouTube 频道")
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
                            TextField("搜索场景教学视频...", text: $searchQuery)
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
                                categoryFilterButton("全部场景", category: "all")
                                categoryFilterButton("交通电车", category: "transit")
                                categoryFilterButton("便利店", category: "kombini")
                                categoryFilterButton("居酒屋餐饮", category: "dining")
                                categoryFilterButton("购物动漫", category: "shopping")
                            }
                            .padding(.horizontal)
                        }

                        // Video Lessons Grid / List
                        VStack(spacing: 14) {
                            ForEach(filteredLessons) { lesson in
                                Button(action: {
                                    selectedLesson = lesson
                                }) {
                                    VStack(alignment: .leading, spacing: 0) {
                                        // Fake Thumbnail / Video Card Header
                                        ZStack(alignment: .bottomTrailing) {
                                            RoundedRectangle(cornerRadius: 14)
                                                .fill(
                                                    LinearGradient(
                                                        colors: [Color(hex: "#1E293B"), Color(hex: "#0F172A")],
                                                        startPoint: .topLeading,
                                                        endPoint: .bottomTrailing
                                                    )
                                                )
                                                .frame(height: 140)

                                            // Central Play Icon & District
                                            HStack {
                                                VStack(alignment: .leading, spacing: 4) {
                                                    HStack {
                                                        Image(systemName: lesson.thumbnailIcon)
                                                            .font(.caption)
                                                        Text(lesson.district)
                                                            .font(.system(size: 11, weight: .bold))
                                                    }
                                                    .foregroundColor(.white.opacity(0.8))

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
                                                        .shadow(color: Color.red.opacity(0.4), radius: 6, x: 0, y: 3)
                                                    Image(systemName: "play.fill")
                                                        .font(.system(size: 16, weight: .bold))
                                                        .foregroundColor(.white)
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

                                                Text("\(lesson.chapters.count) 个章节时间点")
                                                    .font(.caption2)
                                                    .foregroundColor(.secondary)
                                            }

                                            Text(lesson.title)
                                                .font(.system(size: 14, weight: .bold))
                                                .foregroundColor(.primary)
                                                .multilineTextAlignment(.leading)
                                                .lineLimit(2)

                                            Text(lesson.summary)
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
                        .padding(.horizontal)
                        .padding(.bottom, 30)
                    }
                }
            }
            .navigationTitle("YT 场景视频教学")
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
