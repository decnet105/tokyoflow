import SwiftUI

public struct TokyoCitizenChatView: View {
    public let persona: TokyoCitizenPersona

    @State private var messages: [ChatMessage] = []
    @State private var inputText: String = ""
    @State private var showFurigana: Bool = true
    @ObservedObject var audioService = AudioService.shared
    @ObservedObject var gamification = GamificationService.shared

    public init(persona: TokyoCitizenPersona) {
        self.persona = persona
        _messages = State(initialValue: persona.starterMessages)
    }

    public var body: some View {
        ZStack {
            MangaThemeBackgroundView()

            VStack(spacing: 0) {
                // Persona Profile Top Bar
                HStack(spacing: 12) {
                    Text(persona.avatar)
                        .font(.system(size: 36))

                    VStack(alignment: .leading, spacing: 2) {
                        HStack {
                            Text(persona.name)
                                .font(.system(size: 16, weight: .bold))
                            Text("(\(persona.role))")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }

                        Text(persona.description)
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .lineLimit(1)
                    }

                    Spacer()

                    Button(action: { showFurigana.toggle() }) {
                        Text("ふりがな")
                            .font(.system(size: 10, weight: .bold))
                            .padding(.horizontal, 8)
                            .padding(.vertical, 5)
                            .background(showFurigana ? Color.accentColor.opacity(0.25) : Color.gray.opacity(0.2))
                            .cornerRadius(8)
                    }
                }
                .padding()
                .background(.ultraThinMaterial)

                // Message List
                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(spacing: 14) {
                            ForEach(messages) { msg in
                                ChatBubbleRowView(message: msg, showFurigana: showFurigana) {
                                    audioService.speak(text: msg.textJapanese)
                                }
                                .id(msg.id)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: messages.count) { _ in
                        if let last = messages.last {
                            withAnimation {
                                proxy.scrollTo(last.id, anchor: .bottom)
                            }
                        }
                    }
                }

                // Quick Response Chips
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(quickResponsesForPersona(persona.id), id: \.self) { phrase in
                            Button(action: {
                                sendMessage(userText: phrase)
                            }) {
                                Text(phrase)
                                    .font(.caption)
                                    .fontWeight(.medium)
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 7)
                                    .background(.ultraThinMaterial)
                                    .cornerRadius(12)
                            }
                        }
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 6)
                }

                // Input Bar
                HStack(spacing: 10) {
                    TextField("Type Japanese or English reply...", text: $inputText)
                        .padding(.horizontal, 14)
                        .padding(.vertical, 10)
                        .background(.ultraThinMaterial)
                        .cornerRadius(16)
                        .onSubmit {
                            if !inputText.isEmpty {
                                sendMessage(userText: inputText)
                                inputText = ""
                            }
                        }

                    Button(action: {
                        if !inputText.isEmpty {
                            sendMessage(userText: inputText)
                            inputText = ""
                        }
                    }) {
                        Image(systemName: "paperplane.fill")
                            .font(.system(size: 16, weight: .bold))
                            .foregroundColor(.white)
                            .frame(width: 42, height: 42)
                            .background(Color.accentColor)
                            .clipShape(Circle())
                    }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                .background(.ultraThinMaterial)
            }
        }
        .navigationTitle(persona.nameJapanese)
        .navigationBarTitleDisplayMode(.inline)
    }

    private func sendMessage(userText: String) {
        let userMsg = ChatMessage(
            senderName: "You",
            isUser: true,
            textJapanese: userText,
            textFurigana: userText,
            textEnglish: ""
        )
        messages.append(userMsg)
        gamification.addRewards(tp: 10, exp: 15)

        // Generate Persona Reply
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
            let reply = generatePersonaReply(for: persona.id, input: userText)
            messages.append(reply)
            audioService.speak(text: reply.textJapanese)
        }
    }

    private func quickResponsesForPersona(_ id: String) -> [String] {
        switch id {
        case "gal_sakura":
            return ["マジで！？", "それめっちゃエモい！", "渋谷のおすすめカフェ教えて！", "今日これからタピオカ行く？"]
        case "master_kenji":
            return ["生ビールとおすすめで！", "お通し何ですか？", "お会計お願いします！", "ごちそうさまでした！"]
        case "station_tanaka":
            return ["山手線は何番線ですか？", "Suicaのチャージはどこですか？", "終電は何時ですか？", "ありがとうございます！"]
        default:
            return ["新作マンガ買った？", "聖地巡礼行こう！", "秋葉原で一番安い店は？", "おすすめのアニメ教えて！"]
        }
    }

    private func generatePersonaReply(for id: String, input: String) -> ChatMessage {
        switch id {
        case "gal_sakura":
            return ChatMessage(
                senderName: "Sakura",
                isUser: false,
                textJapanese: "わかる〜！それ超ヤバくない！？今度センター街で語ろ！",
                textFurigana: "わかる〜！それ ちょう やばくない！？ こんど センターがいで かたろ！",
                textEnglish: "Totally! Isn't that crazy cool?! Let's chat more at Center-gai next time!"
            )
        case "master_kenji":
            return ChatMessage(
                senderName: "Master Kenji",
                isUser: false,
                textJapanese: "へいお待ち！まずは冷えたビールと焼き鳥盛り合わせでどうだい？",
                textFurigana: "へい おまち！ まずは ひえた ビールと やきとり もりあわせで どうだい？",
                textEnglish: "Coming right up! How about starting with cold beer and an assorted yakitori platter?"
            )
        case "station_tanaka":
            return ChatMessage(
                senderName: "Station Staff Tanaka",
                isUser: false,
                textJapanese: "かしこまりました。2番線の内回り電車をご利用ください。お気をつけて！",
                textFurigana: "かしこまりました。にばんせんの うちまわり でんしゃを ごりようください。おきをつけて！",
                textEnglish: "Understood. Please take the inner loop train on Platform 2. Have a safe journey!"
            )
        default:
            return ChatMessage(
                senderName: "Akiba Ren",
                isUser: false,
                textJapanese: "それ最高ですね！ラジオ会館の3階に限定版がまだ残ってましたよ！",
                textFurigana: "それ さいこうですね！ ラジオかいかんの さんかいに げんていばんが まだ のこってましたよ！",
                textEnglish: "That's awesome! They still had the limited edition on the 3rd floor of Radio Kaikan!"
            )
        }
    }
}

public struct ChatBubbleRowView: View {
    public let message: ChatMessage
    public let showFurigana: Bool
    public let onSpeak: () -> Void

    public var body: some View {
        HStack(alignment: .bottom, spacing: 8) {
            if message.isUser {
                Spacer()
            }

            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                Text(message.textJapanese)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundColor(message.isUser ? .white : .primary)

                if showFurigana && !message.textFurigana.isEmpty && message.textFurigana != message.textJapanese {
                    Text(message.textFurigana)
                        .font(.system(size: 11))
                        .foregroundColor(message.isUser ? .white.opacity(0.8) : .secondary)
                }

                if !message.textEnglish.isEmpty {
                    Text(message.textEnglish)
                        .font(.system(size: 12))
                        .foregroundColor(message.isUser ? .white.opacity(0.9) : .secondary)
                        .padding(.top, 2)
                }

                if !message.isUser {
                    Button(action: onSpeak) {
                        HStack(spacing: 3) {
                            Image(systemName: "speaker.wave.2.fill")
                            Text("Listen")
                        }
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(.accentColor)
                        .padding(.top, 2)
                    }
                }
            }
            .padding(12)
            .background(message.isUser ? Color.accentColor : Color.white.opacity(0.12))
            .cornerRadius(16)

            if !message.isUser {
                Spacer()
            }
        }
    }
}
