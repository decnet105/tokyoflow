import SwiftUI

public struct MangaLabView: View {
    @ObservedObject var dataManager = DataManager.shared
    @EnvironmentObject var userProfile: UserProfile
    @State private var showSFXSoundboard = false

    public var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // Header Banner
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("MANGA READING LAB")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(.purple)
                                    .tracking(1.5)
                                Text("Read Raw Manga in 1 Year")
                                    .font(.system(size: 26, weight: .bold, design: .rounded))
                            }
                            Spacer()
                            Button(action: { showSFXSoundboard = true }) {
                                HStack(spacing: 6) {
                                    Image(systemName: "speaker.wave.3.fill")
                                    Text("SFX Soundboard")
                                        .font(.system(size: 12, weight: .bold))
                                }
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(Color.purple.opacity(0.12))
                                .foregroundColor(.purple)
                                .cornerRadius(20)
                            }
                        }

                        Text("Decode authentic manga onomatopoeia (擬音・擬態語), speech bubble layouts, casual contractions (〜ちゃう, 〜なきゃ), and character speech styles.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.horizontal)
                    .padding(.top, 8)

                    // Manga Lessons List
                    LazyVStack(spacing: 16) {
                        ForEach(dataManager.mangaLessons) { lesson in
                            NavigationLink(destination: MangaPanelReaderView(lesson: lesson)) {
                                MangaLessonCard(lesson: lesson, isCompleted: userProfile.completedMangaLessonIds.contains(lesson.id))
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.bottom, 24)
            }
            .navigationTitle("Manga Lab")
            .navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $showSFXSoundboard) {
                SFXDictionaryView()
            }
        }
    }
}

public struct MangaLessonCard: View {
    public let lesson: MangaLesson
    public let isCompleted: Bool

    public var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(lesson.genre)
                    .font(.caption)
                    .fontWeight(.bold)
                    .foregroundColor(.purple)
                Spacer()
                Text(lesson.difficulty)
                    .font(.system(size: 10, weight: .bold))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 3)
                    .background(Color.purple.opacity(0.12))
                    .foregroundColor(.purple)
                    .cornerRadius(6)
            }

            Text(lesson.title)
                .font(.headline)
                .foregroundColor(.primary)

            Text(lesson.titleJa)
                .font(.subheadline)
                .foregroundColor(.secondary)

            Text(lesson.description)
                .font(.footnote)
                .foregroundColor(.secondary)
                .lineLimit(2)

            HStack {
                HStack(spacing: 12) {
                    Label("\(lesson.panels.count) Panels", systemImage: "rectangle.split.3x1.fill")
                    Label("\(lesson.grammarBreakdowns.count) Slang Rules", systemImage: "sparkles")
                }
                .font(.caption2)
                .foregroundColor(.secondary)

                Spacer()

                if isCompleted {
                    HStack(spacing: 4) {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                        Text("Mastered")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.green)
                    }
                } else {
                    HStack(spacing: 4) {
                        Text("Read Panels")
                            .font(.caption)
                            .fontWeight(.semibold)
                        Image(systemName: "chevron.right")
                            .font(.caption2)
                    }
                    .foregroundColor(.purple)
                }
            }
        }
        .padding(16)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.04), radius: 8, x: 0, y: 2)
    }
}
