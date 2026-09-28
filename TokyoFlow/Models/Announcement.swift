import Foundation

public struct ListeningQuiz: Codable {
    public let question: String
    public let options: [String]
    public let correctIndex: Int
}

public struct Announcement: Identifiable, Codable {
    public let id: String
    public let location: String
    public let soundType: String // train_chime_and_voice, door_chime_and_voice, store_door_chime, conductor_voice
    public let title: String
    public let titleJa: String
    public let chimeType: String
    public let japanese: String
    public let furigana: String
    public let romaji: String
    public let english: String
    public let chinese: String
    public let audioPrompt: String
    public let listeningQuiz: ListeningQuiz?
}
