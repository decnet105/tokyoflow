import Foundation

public struct TokyoCitizenPersona: Identifiable, Hashable {
    public let id: String
    public let name: String
    public let nameJapanese: String
    public let role: String
    public let avatar: String
    public let description: String
    public let speechStyle: String
    public let tags: [String]
    public let starterMessages: [ChatMessage]

    public init(
        id: String,
        name: String,
        nameJapanese: String,
        role: String,
        avatar: String,
        description: String,
        speechStyle: String,
        tags: [String],
        starterMessages: [ChatMessage]
    ) {
        self.id = id
        self.name = name
        self.nameJapanese = nameJapanese
        self.role = role
        self.avatar = avatar
        self.description = description
        self.speechStyle = speechStyle
        self.tags = tags
        self.starterMessages = starterMessages
    }
}

public struct ChatMessage: Identifiable, Hashable, Codable {
    public let id: String
    public let senderName: String
    public let isUser: Bool
    public let textJapanese: String
    public let textFurigana: String
    public let textEnglish: String
    public let timestamp: Date
    public let audioUrl: String?

    public init(
        id: String = UUID().uuidString,
        senderName: String,
        isUser: Bool,
        textJapanese: String,
        textFurigana: String,
        textEnglish: String,
        timestamp: Date = Date(),
        audioUrl: String? = nil
    ) {
        self.id = id
        self.senderName = senderName
        self.isUser = isUser
        self.textJapanese = textJapanese
        self.textFurigana = textFurigana
        self.textEnglish = textEnglish
        self.timestamp = timestamp
        self.audioUrl = audioUrl
    }
}

public struct CommunityPost: Identifiable, Hashable {
    public let id: String
    public let authorName: String
    public let authorAvatar: String
    public let authorTier: String
    public let timestampText: String
    public let tag: String
    public let title: String
    public let content: String
    public var likesCount: Int
    public var commentsCount: Int
    public var isLiked: Bool

    public init(
        id: String,
        authorName: String,
        authorAvatar: String,
        authorTier: String,
        timestampText: String,
        tag: String,
        title: String,
        content: String,
        likesCount: Int,
        commentsCount: Int,
        isLiked: Bool = false
    ) {
        self.id = id
        self.authorName = authorName
        self.authorAvatar = authorAvatar
        self.authorTier = authorTier
        self.timestampText = timestampText
        self.tag = tag
        self.title = title
        self.content = content
        self.likesCount = likesCount
        self.commentsCount = commentsCount
        self.isLiked = isLiked
    }
}
