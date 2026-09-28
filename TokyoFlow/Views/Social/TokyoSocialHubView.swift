import SwiftUI

public struct TokyoSocialHubView: View {
    @State private var selectedTab: Int = 0 // 0: AI Citizens, 1: Community Board
    @State private var newPostText: String = ""
    @ObservedObject var gamification = GamificationService.shared

    public let personas: [TokyoCitizenPersona] = [
        TokyoCitizenPersona(
            id: "gal_sakura",
            name: "Sakura (サクラ)",
            nameJapanese: "渋谷ギャル・サクラ",
            role: "Shibuya Fashion & Slang",
            avatar: "🌸",
            description: "Talk about Shibuya trends, cafe culture, and trendy casual Japanese (タメ口・若者言葉).",
            speechStyle: "Casual / Trendy Gal Slang",
            tags: ["Shibuya", "Slang", "Cafe", "Pop Culture"],
            starterMessages: [
                ChatMessage(
                    senderName: "Sakura",
                    isUser: false,
                    textJapanese: "ヤッホー！今日渋谷で何か面白いことあった？",
                    textFurigana: "ヤッホー！ きょう しぶやで なにか おもしろいこと あった？",
                    textEnglish: "Yaho~! Did anything fun happen in Shibuya today?"
                )
            ]
        ),
        TokyoCitizenPersona(
            id: "master_kenji",
            name: "Master Kenji (健二)",
            nameJapanese: "居酒屋大将・健二",
            role: "Shinjuku Izakaya Master",
            avatar: "🍶",
            description: "Practice ordering dishes, asking for recommendations, table etiquette, and chatting with the chef.",
            speechStyle: "Warm Shitamachi / Friendly",
            tags: ["Izakaya", "Food", "Beer", "Shinjuku"],
            starterMessages: [
                ChatMessage(
                    senderName: "Master Kenji",
                    isUser: false,
                    textJapanese: "いらっしゃい！何杯飲む？今日のおすすめはマグロだよ！",
                    textFurigana: "いらっしゃい！ なんばい のむ？ きょうの おすすめは マグロだよ！",
                    textEnglish: "Welcome! What are you drinking? Today's recommendation is fresh tuna!"
                )
            ]
        ),
        TokyoCitizenPersona(
            id: "station_tanaka",
            name: "Officer Tanaka (田中さん)",
            nameJapanese: "新宿駅員・田中さん",
            role: "Tokyo Metro Station Staff",
            avatar: "💼",
            description: "Practice formal Keigo, asking for train transfers, lost items, and Suica / Pasmo trouble.",
            speechStyle: "Polite Keigo / Formal",
            tags: ["Station", "Keigo", "Transit", "Suica"],
            starterMessages: [
                ChatMessage(
                    senderName: "Station Staff Tanaka",
                    isUser: false,
                    textJapanese: "ご案内いたします。どちらの方面へお出かけですか？",
                    textFurigana: "ごあんない いたします。 どちらの ほうめんへ おでかけですか？",
                    textEnglish: "How may I assist you? Which direction are you heading toward?"
                )
            ]
        ),
        TokyoCitizenPersona(
            id: "otaku_ren",
            name: "Ren (レン)",
            nameJapanese: "秋葉原オタク・レン",
            role: "Akihabara Manga Expert",
            avatar: "🎮",
            description: "Chat about latest manga chapters, anime voice actors, doujinshi events, and Akiba deals.",
            speechStyle: "Enthusiastic Otaku Talk",
            tags: ["Manga", "Anime", "Akiba", "Figures"],
            starterMessages: [
                ChatMessage(
                    senderName: "Akiba Ren",
                    isUser: false,
                    textJapanese: "今期の新作アニメもう観た？原作マンガもめっちゃ熱いよ！",
                    textFurigana: "こんきの しんさく アニメ もう みた？ げんさく マンガも めっちゃ あついよ！",
                    textEnglish: "Have you watched this season's new anime yet? The original manga is fire!"
                )
            ]
        )
    ]

    @State private var communityPosts: [CommunityPost] = [
        CommunityPost(
            id: "p1",
            authorName: "TokyoExplorer",
            authorAvatar: "⚡",
            authorTier: "下町常連 (Lv.45)",
            timestampText: "2h ago",
            tag: "Food Tip 🍜",
            title: "一蘭 (Ichiran) 怎么点单最像当地人？",
            content: "在填写口味定制纸（オーダー用紙）时：味の濃さ选「基本」、こってり度选「あっさり」、麺のかたさ选「超かため」最推荐！",
            likesCount: 24,
            commentsCount: 8
        ),
        CommunityPost(
            id: "p2",
            authorName: "MangaLover_JP",
            authorAvatar: "🌸",
            authorTier: "留学生 (Lv.18)",
            timestampText: "5h ago",
            tag: "Manga 📖",
            title: "今天在 NHK 原音新闻跟读打卡成功！",
            content: "听完「JRダイヤ改正」的新闻，把『終電』和『乗り遅れ』的录音对比练了3遍，发音终于达到90分以上了！🔥",
            likesCount: 19,
            commentsCount: 4
        ),
        CommunityPost(
            id: "p3",
            authorName: "AkibaWalker",
            authorAvatar: "🎮",
            authorTier: "ワーホリ滞在者 (Lv.8)",
            timestampText: "1d ago",
            tag: "Living 💡",
            title: "便利店加热的终极一句话",
            content: "店员问『温めますか？』直接回『あ、お願いします（hai, onegaishimasu）』就可以，超简单自然！",
            likesCount: 42,
            commentsCount: 12
        )
    ]

    public init() {}

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 12) {
                    // Custom Glass Pill Tab Selector (Spacious & Clean)
                    HStack(spacing: 12) {
                        Button(action: {
                            withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
                                selectedTab = 0
                            }
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "person.2.wave.2.fill")
                                    .font(.system(size: 13, weight: .bold))
                                Text("AI 住民会話")
                                    .font(.system(size: 14, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 10)
                            .background(selectedTab == 0 ? Color.accentColor : Color.primary.opacity(0.08))
                            .foregroundColor(selectedTab == 0 ? .white : .primary)
                            .cornerRadius(12)
                            .shadow(color: selectedTab == 0 ? Color.accentColor.opacity(0.3) : Color.clear, radius: 4, y: 2)
                        }
                        .buttonStyle(.plain)

                        Button(action: {
                            withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
                                selectedTab = 1
                            }
                        }) {
                            HStack(spacing: 6) {
                                Image(systemName: "bubble.left.and.bubble.right.fill")
                                    .font(.system(size: 13, weight: .bold))
                                Text("東京掲示板")
                                    .font(.system(size: 14, weight: .bold))
                            }
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 10)
                            .background(selectedTab == 1 ? Color.accentColor : Color.primary.opacity(0.08))
                            .foregroundColor(selectedTab == 1 ? .white : .primary)
                            .cornerRadius(12)
                            .shadow(color: selectedTab == 1 ? Color.accentColor.opacity(0.3) : Color.clear, radius: 4, y: 2)
                        }
                        .buttonStyle(.plain)
                    }
                    .padding(.horizontal)
                    .padding(.top, 8)

                    if selectedTab == 0 {
                        citizenPersonaListView
                    } else {
                        communityBoardView
                    }
                }
            }
            .navigationTitle("Tokyo Social")
            .navigationBarTitleDisplayMode(.inline)
        }
    }

    private var citizenPersonaListView: some View {
        ScrollView {
            VStack(spacing: 16) {
                // Info Banner
                HStack(spacing: 14) {
                    Image(systemName: "sparkles.rectangle.stack.fill")
                        .font(.title2)
                        .foregroundColor(.accentColor)

                    VStack(alignment: .leading, spacing: 4) {
                        Text("Practice Conversational Japanese")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.primary)
                        Text("Chat with Tokyo native personas, hear natural voices, and build confidence.")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
                .padding(14)
                .background(.ultraThinMaterial)
                .cornerRadius(16)
                .padding(.horizontal)
                .padding(.top, 4)

                ForEach(personas) { persona in
                    NavigationLink(destination: TokyoCitizenChatView(persona: persona)) {
                        PersonaCardView(persona: persona)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
            .padding(.horizontal)
            .padding(.bottom, 24)
        }
    }

    private var communityBoardView: some View {
        ScrollView {
            VStack(spacing: 14) {
                ForEach($communityPosts) { $post in
                    VStack(alignment: .leading, spacing: 10) {
                        HStack(spacing: 10) {
                            Text(post.authorAvatar)
                                .font(.title3)

                            VStack(alignment: .leading, spacing: 2) {
                                HStack(spacing: 6) {
                                    Text(post.authorName)
                                        .font(.system(size: 14, weight: .bold))
                                    Text(post.authorTier)
                                        .font(.caption2)
                                        .foregroundColor(.accentColor)
                                }
                                Text(post.timestampText)
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }

                            Spacer()

                            Text(post.tag)
                                .font(.caption2)
                                .fontWeight(.bold)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.accentColor.opacity(0.15))
                                .cornerRadius(8)
                        }

                        Text(post.title)
                            .font(.system(size: 16, weight: .bold))

                        Text(post.content)
                            .font(.system(size: 13))
                            .foregroundColor(.secondary)

                        Divider()

                        HStack(spacing: 20) {
                            Button(action: {
                                if post.isLiked {
                                    post.likesCount -= 1
                                    post.isLiked = false
                                } else {
                                    post.likesCount += 1
                                    post.isLiked = true
                                    gamification.addRewards(tp: 5, exp: 5)
                                }
                            }) {
                                HStack(spacing: 4) {
                                    Image(systemName: post.isLiked ? "heart.fill" : "heart")
                                        .foregroundColor(post.isLiked ? .red : .secondary)
                                    Text("\(post.likesCount)")
                                        .font(.caption)
                                        .foregroundColor(post.isLiked ? .red : .secondary)
                                }
                            }

                            HStack(spacing: 4) {
                                Image(systemName: "bubble.right")
                                    .foregroundColor(.secondary)
                                Text("\(post.commentsCount) replies")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            Spacer()
                        }
                    }
                    .padding(16)
                    .background(.ultraThinMaterial)
                    .cornerRadius(18)
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 8)
        }
    }
}

public struct PersonaCardView: View {
    public let persona: TokyoCitizenPersona

    public var body: some View {
        HStack(alignment: .top, spacing: 14) {
            Text(persona.avatar)
                .font(.system(size: 38))
                .padding(8)
                .background(Color.primary.opacity(0.06))
                .clipShape(Circle())

            VStack(alignment: .leading, spacing: 6) {
                HStack(alignment: .center) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(persona.name)
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.primary)
                        Text(persona.nameJapanese)
                            .font(.system(size: 11))
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    Text(persona.speechStyle)
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(.accentColor)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 4)
                        .background(Color.accentColor.opacity(0.12))
                        .cornerRadius(8)
                }

                Text(persona.description)
                    .font(.system(size: 13))
                    .foregroundColor(.secondary)
                    .lineSpacing(2)
                    .fixedSize(horizontal: false, vertical: true)

                HStack(spacing: 6) {
                    ForEach(persona.tags, id: \.self) { tag in
                        Text("#\(tag)")
                            .font(.system(size: 10, weight: .medium))
                            .foregroundColor(.primary.opacity(0.7))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.primary.opacity(0.05))
                            .cornerRadius(4)
                    }
                }
                .padding(.top, 2)
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(18)
        .shadow(color: Color.black.opacity(0.04), radius: 6, x: 0, y: 2)
    }
}
