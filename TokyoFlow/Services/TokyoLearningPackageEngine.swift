import Foundation
import Combine
import SwiftUI

public class TokyoLearningPackageEngine: ObservableObject {
    public static let shared = TokyoLearningPackageEngine()

    @Published public var selectedTrack: LearningCurriculumTrack = .scenario(.commute) {
        didSet {
            refreshPackage()
        }
    }
    
    @Published public var selectedFocusMode: LearningFocusMode = .practicalFluency {
        didSet {
            refreshPackage()
        }
    }

    @Published public var currentPackage: TokyoLearningPackage?
    @Published public var isRunningPackage: Bool = false

    // Convenience property for backward compatibility
    public var selectedContextMode: LearningContextMode {
        get {
            if case .scenario(let mode) = selectedTrack {
                return mode
            }
            return .commute
        }
        set {
            selectedTrack = .scenario(newValue)
        }
    }

    private init() {
        refreshPackage()
    }

    public func refreshPackage() {
        switch selectedTrack {
        case .scenario(let mode):
            self.currentPackage = generatePackage(for: mode, focus: selectedFocusMode)
        case .jlpt(let level):
            self.currentPackage = generateLevelPackage(for: level, focus: selectedFocusMode)
        }
    }

    public func setTrack(_ track: LearningCurriculumTrack) {
        self.selectedTrack = track
    }

    public func setFocusMode(_ focus: LearningFocusMode) {
        self.selectedFocusMode = focus
    }

    // MARK: - Scenario-Driven Packaging
    public func generatePackage(for mode: LearningContextMode, focus: LearningFocusMode = .practicalFluency) -> TokyoLearningPackage {
        let dict = JLPTDictionaryService.shared
        let grammarService = JLPTGrammarService.shared
        let weakTracker = WeakWordTrackerService.shared
        let videoManager = TokyoVideoLessonDataManager.shared
        let newsService = NHKNewsService.shared

        var items: [LearningPackageItem] = []

        switch mode {
        case .commute:
            // 🚇 COMMUTE: Subways, transit broadcasts, station signs
            items.append(
                LearningPackageItem(
                    type: .kanaAccent,
                    title: "Kana & Tone Baseline",
                    subtitle: "Subway & Station Phonetics",
                    japaneseText: "えき (駅)",
                    furiganaText: "えき",
                    englishMeaning: "Train Station",
                    pitchAccent: "① (Head-High)",
                    audioKey: "駅",
                    tip: "Notice the initial high pitch on 'E', dropping on 'ki'."
                )
            )

            // High-Yield Spaced Vocab
            let reviewWord = weakTracker.activeWeakWords.first?.word ?? "乗り換え"
            let wordObj = dict.allWords.first(where: { $0.kanji == reviewWord || $0.kanji == "駅" })
            items.append(
                LearningPackageItem(
                    type: .spacedVocab,
                    title: "High-Yield Spaced Recall",
                    subtitle: "Transit High-Yield JLPT",
                    japaneseText: wordObj?.kanji ?? "乗り換え",
                    furiganaText: wordObj?.reading ?? "のりかえ",
                    englishMeaning: wordObj?.meaning ?? "Transfer / Connection",
                    pitchAccent: wordObj?.pitchAccent ?? "⓪ (Flat)",
                    audioKey: wordObj?.kanji ?? "乗り換え",
                    tip: "Essential for navigating Shinjuku & Shibuya maze corridors.",
                    collocation: wordObj?.collocation ?? "山手線に乗り換える"
                )
            )

            // Grammar Formula & Connection Pattern
            let grammar = grammarService.allGrammar.first(where: { $0.scenarioTag == "transit" }) ?? grammarService.allGrammar.first
            if let g = grammar {
                items.append(
                    LearningPackageItem(
                        type: focus == .examSprint ? .examTrapQuiz : .grammarFormula,
                        title: focus == .examSprint ? "JLPT Exam Trap Drill" : "Grammar Blueprint Pattern",
                        subtitle: "Transit & Courtesy Condition",
                        japaneseText: g.title,
                        furiganaText: g.romaji,
                        englishMeaning: g.meaningEn,
                        audioKey: g.title,
                        tip: g.nuanceExplanation,
                        connectionRule: g.connectionRule,
                        quizOptions: g.quiz?.options,
                        quizCorrectIndex: g.quiz?.correctIndex,
                        quizExplanation: g.quiz?.explanationZh
                    )
                )
            }


            // Real-world Broadcast / YouTube masterclass
            let ytLesson = videoManager.lessons.first(where: { $0.category == "transit" }) ?? videoManager.lessons.first
            let ytTitle = ytLesson?.titleJa ?? "山手線ラッシュ・乗り換えアナウンス完全攻略"
            items.append(
                LearningPackageItem(
                    type: .scenarioVideo,
                    title: "Video Masterclass",
                    subtitle: ytLesson?.title ?? "Tokyo Metro Platform Broadcasts",
                    japaneseText: ytTitle,
                    furiganaText: "やまのてせん らっしゅ",
                    englishMeaning: "Real-world audio breakdown of Tokyo transit corridors.",
                    audioKey: ytTitle,
                    youtubeVideoId: ytLesson?.youtubeVideoId ?? "kFhcEWNNkkc",
                    tip: "Watch native conductor gestures and platform chimes."
                )
            )

            // NHK Daily News Shadowing
            let news = newsService.dailyNews.first
            let newsTitle = news?.title ?? "JR東日本 終電時間を早める方針を発表"
            items.append(
                LearningPackageItem(
                    type: .newsShadowing,
                    title: "NHK Easy News Shadowing",
                    subtitle: "Tokyo Transit Update",
                    japaneseText: newsTitle,
                    furiganaText: news?.titleFurigana ?? "じぇいあーるひがしにほん しゅうでんじかんを はやめるほうしんを はっぴょう",
                    englishMeaning: news?.summary ?? "JR East announces updated train timetable.",
                    audioKey: newsTitle,
                    tip: "Shadow along at 1.0x native speed to train ear rhythm."
                )
            )

        case .coffeeBreak:
            // ☕️ COFFEE BREAK: 3-Second rapid reactions & quick memory test
            items.append(
                LearningPackageItem(
                    type: .dojoReaction,
                    title: "3-Second Instinct Drill",
                    subtitle: "Kombini Register Microwave",
                    japaneseText: "お弁当温めますか？",
                    furiganaText: "おべんとう あたためますか？",
                    englishMeaning: "Would you like your bento heated up?",
                    pitchAccent: "④ (Mid-High)",
                    audioKey: "お弁当温めますか？",
                    tip: "Golden 1-second response: 'あ、お願いします' or '大丈夫です'."
                )
            )

            let w1 = dict.allWords.first(where: { $0.level == "N5" })
            items.append(
                LearningPackageItem(
                    type: .spacedVocab,
                    title: "High-Yield Rapid Recall",
                    subtitle: "JLPT \(w1?.level ?? "N5") Core",
                    japaneseText: w1?.kanji ?? "私",
                    furiganaText: w1?.reading ?? "わたし",
                    englishMeaning: w1?.meaning ?? "I, me",
                    pitchAccent: w1?.pitchAccent ?? "⓪ (Flat)",
                    audioKey: w1?.kanji ?? "私",
                    tip: w1?.exampleEn ?? "I live in Tokyo."
                )
            )

            items.append(
                LearningPackageItem(
                    type: .dojoReaction,
                    title: "Izakaya Toast Formula",
                    subtitle: "Shinjuku Omoide Yokocho",
                    japaneseText: "とりあえず生ビール二つ！",
                    furiganaText: "とりあえず なまびーる ふたつ！",
                    englishMeaning: "Two draft beers to start, please!",
                    pitchAccent: "⓪ (Flat)",
                    audioKey: "とりあえず生ビール二つ！",
                    tip: "Always order drinks first before checking the food menu."
                )
            )

        case .deepEvening:
            // 🌙 EVENING DEEP STUDY: Full masterclass, grammar nuances & scenario roleplay
            let ep3 = videoManager.lessons.first(where: { $0.category == "dining" }) ?? videoManager.lessons.first
            let ep3Title = ep3?.titleJa ?? "居酒屋注文・お通し文化・とりあえず生！"

            items.append(
                LearningPackageItem(
                    type: .scenarioVideo,
                    title: "Featured Masterclass",
                    subtitle: ep3?.title ?? "Izakaya Mastery: Pub Ordering & Toasting",
                    japaneseText: ep3Title,
                    furiganaText: "いざかや ちゅうもん",
                    englishMeaning: "Complete breakdown of Otoshi appetizer rules and billing.",
                    audioKey: ep3Title,
                    youtubeVideoId: ep3?.youtubeVideoId ?? "q6P6i7nkIhU",
                    tip: "Understand why Izakayas serve Otoshi table charge dishes."
                )
            )

            // Grammar Master Pattern
            if let gN3 = grammarService.allGrammar.first(where: { $0.level == "N3" }) {
                items.append(
                    LearningPackageItem(
                        type: focus == .examSprint ? .examTrapQuiz : .grammarFormula,
                        title: "Grammar Master Pattern",
                        subtitle: gN3.level + " Core Formula",
                        japaneseText: gN3.title,
                        furiganaText: gN3.romaji,
                        englishMeaning: gN3.meaningEn,
                        audioKey: gN3.title,
                        tip: gN3.nuanceExplanation,
                        connectionRule: gN3.connectionRule,
                        quizOptions: gN3.quiz?.options,
                        quizCorrectIndex: gN3.quiz?.correctIndex,
                        quizExplanation: gN3.quiz?.explanationZh
                    )
                )
            }


            items.append(
                LearningPackageItem(
                    type: .spacedVocab,
                    title: "Formal Etiquette Vocab",
                    subtitle: "Bill & Official Receipt",
                    japaneseText: "領収書",
                    furiganaText: "りょうしゅうしょ",
                    englishMeaning: "Formal business tax receipt",
                    pitchAccent: "⓪ (Flat)",
                    audioKey: "領収書",
                    tip: "Say 'Ryōshūsho o onegaishimasu' for business reimbursement."
                )
            )

            let newsArticle = newsService.dailyNews.dropFirst().first ?? newsService.dailyNews.first
            let newsArticleTitle = newsArticle?.title ?? "外国人観光客が過去最多 円安の影響で消費拡大"
            items.append(
                LearningPackageItem(
                    type: .newsShadowing,
                    title: "NHK Culture & Society",
                    subtitle: "Tokyo Inbound Tourism Surge",
                    japaneseText: newsArticleTitle,
                    furiganaText: newsArticle?.titleFurigana ?? "がいこくじんかんこうきゃくが かこさいた えんやすのえいきょうで しょうひかくだい",
                    englishMeaning: newsArticle?.summary ?? "Foreign tourists reach record highs with expanding consumption.",
                    audioKey: newsArticleTitle,
                    tip: "Listen to business economics terms: '円安' (weak yen) & '消費' (spending)."
                )
            )

        case .travelSurvival:
            // ✈️ TRAVEL SURVIVAL: Immediate high-frequency survival toolkit
            let ep2 = videoManager.lessons.first(where: { $0.category == "kombini" }) ?? videoManager.lessons.first
            let ep2Title = ep2?.titleJa ?? "コンビニレジ連環問・お弁当温め・袋不要"

            items.append(
                LearningPackageItem(
                    type: .goldenSentence,
                    title: "Universal Courtesy Phrase",
                    subtitle: "Declining Plastic Bag",
                    japaneseText: "袋は大丈夫です。",
                    furiganaText: "ふくろは だいじょうぶです。",
                    englishMeaning: "No bag needed, I am fine.",
                    pitchAccent: "⓪ (Flat)",
                    audioKey: "袋は大丈夫です。",
                    tip: "A gentle hand wave + 'Daijōbu desu' is 100% natural across Japan."
                )
            )

            items.append(
                LearningPackageItem(
                    type: .scenarioVideo,
                    title: "Kombini Register Simulator",
                    subtitle: ep2?.title ?? "Convenience Store Survival",
                    japaneseText: ep2Title,
                    furiganaText: "こんびに れじ",
                    englishMeaning: "Decode the 4 rapid questions asked at kombini registers.",
                    audioKey: ep2Title,
                    youtubeVideoId: ep2?.youtubeVideoId ?? "BTKvaO25MUI",
                    tip: "Learn when to tap your Suica on the terminal screen."
                )
            )

            items.append(
                LearningPackageItem(
                    type: .goldenSentence,
                    title: "Cashless Payment Formula",
                    subtitle: "Suica / IC Card Tap",
                    japaneseText: "Suicaでお願いします。",
                    furiganaText: "すいかで おねがいします。",
                    englishMeaning: "With Suica (IC card), please.",
                    pitchAccent: "① (Head-High)",
                    audioKey: "Suicaでお願いします。",
                    tip: "Works in 99% of convenience stores, vending machines, and taxis."
                )
            )

        case .bedtimeImmersion:
            // 📻 BEDTIME IMMERSION: Gentle radio & ambient audio
            items.append(
                LearningPackageItem(
                    type: .newsShadowing,
                    title: "Tokyo 1-Hour Radio Flow",
                    subtitle: "Relaxing Slow Japanese Stream",
                    japaneseText: "NHK ニュース & 街の音 (Tokyo Ambient Flow)",
                    furiganaText: "えぬえいちけい にゅーす",
                    englishMeaning: "Immerse in gentle native Japanese pacing with synchronized subtitles.",
                    audioKey: "NHK ニュース",
                    tip: "Close your eyes and listen to natural intonation without stress."
                )
            )

            items.append(
                LearningPackageItem(
                    type: .kanaAccent,
                    title: "Mnemonic Soundscape",
                    subtitle: "Subconscious Accent Alignment",
                    japaneseText: "ありがとう (有難う)",
                    furiganaText: "ありがとう",
                    englishMeaning: "Thank you very much",
                    pitchAccent: "② (Mid-High)",
                    audioKey: "ありがとう",
                    tip: "Natural Tokyo pitch drops right after 'ga'."
                )
            )
        }

        let totalEstimated = max(3, items.count * 2)
        return TokyoLearningPackage(
            mode: mode,
            levelTrack: nil,
            focusMode: focus,
            estimatedMinutes: totalEstimated,
            items: items
        )
    }

    // MARK: - JLPT Level-Targeted Packaging (N5 ~ N1)
    public func generateLevelPackage(for level: JLPTLevelTrack, focus: LearningFocusMode = .examSprint) -> TokyoLearningPackage {
        let dict = JLPTDictionaryService.shared
        let grammarService = JLPTGrammarService.shared
        let shortLvl = level.shortLabel

        var items: [LearningPackageItem] = []

        // 1. High-Yield Core Vocabulary with Pitch Accent & Transitive Pair
        let words = dict.allWords.filter { $0.level.uppercased() == shortLvl }
        let targetWord = words.first ?? JLPTWord(
            id: "w_def",
            kanji: "日本語",
            reading: "にほんご",
            romaji: "nihongo",
            pitchAccent: "⓪ (Flat)",
            level: shortLvl,
            partOfSpeech: "名",
            meaning: "Japanese language",
            exampleJa: "毎日日本語を勉強しています。",
            exampleFurigana: "まいにち にほんごを べんきょうしています。",
            exampleZh: "每天都在学习日语。",
            exampleEn: "I study Japanese every day."
        )

        items.append(
            LearningPackageItem(
                type: .spacedVocab,
                title: "\(shortLvl) Essential Vocabulary",
                subtitle: targetWord.partOfSpeech,
                japaneseText: targetWord.kanji.isEmpty ? targetWord.reading : targetWord.kanji,
                furiganaText: targetWord.reading,
                englishMeaning: targetWord.meaning,
                pitchAccent: targetWord.pitchAccent,
                audioKey: targetWord.kanji.isEmpty ? targetWord.reading : targetWord.kanji,
                tip: targetWord.examYearNote ?? targetWord.exampleEn,
                collocation: targetWord.collocation
            )
        )

        // 2. Grammar Blueprint Formula & Connection Rule
        let grammars = grammarService.allGrammar.filter { $0.level.uppercased() == shortLvl }
        let targetGrammar = grammars.first

        if let g = targetGrammar {
            items.append(
                LearningPackageItem(
                    type: .grammarFormula,
                    title: "\(shortLvl) Grammar Blueprint",
                    subtitle: g.meaningZh,
                    japaneseText: g.title,
                    furiganaText: g.romaji,
                    englishMeaning: g.meaningEn,
                    audioKey: g.title,
                    tip: g.nuanceExplanation,
                    connectionRule: g.connectionRule
                )
            )

            // 3. Real Exam Trap Question / Practice Drill
            if let quiz = g.quiz {
                items.append(
                    LearningPackageItem(
                        type: .examTrapQuiz,
                        title: "JLPT \(shortLvl) Exam Trap Drill",
                        subtitle: "Past Question Simulation",
                        japaneseText: quiz.question,
                        furiganaText: quiz.questionFurigana,
                        englishMeaning: "Select the correct syntactic connection.",
                        audioKey: quiz.question,
                        tip: g.examTip,
                        connectionRule: g.connectionRule,
                        quizOptions: quiz.options,
                        quizCorrectIndex: quiz.correctIndex,
                        quizExplanation: quiz.explanationZh
                    )
                )
            }
        }

        // 4. Practical Real-World Tokyo Context Application
        if let g = targetGrammar, let sent = g.sentences.first {
            items.append(
                LearningPackageItem(
                    type: .goldenSentence,
                    title: "Tokyo Living Application",
                    subtitle: "\(g.scenarioTag.capitalized) Situation",
                    japaneseText: sent.japanese,
                    furiganaText: sent.furigana,
                    englishMeaning: sent.english,
                    audioKey: sent.japanese,
                    tip: "Mastered from Grammar Blueprint: \(g.title)"
                )
            )
        }


        let totalEstimated = max(3, items.count * 2)
        return TokyoLearningPackage(
            mode: .commute,
            levelTrack: level,
            focusMode: focus,
            estimatedMinutes: totalEstimated,
            items: items
        )
    }

    public func completeCurrentItem() {
        guard var pkg = currentPackage, pkg.currentItemIndex < pkg.items.count else { return }
        pkg.items[pkg.currentItemIndex].isCompleted = true
        
        // Gamification reward
        GamificationService.shared.addRewards(tp: 15, exp: 25)
        GamificationService.shared.recordMicroLearningTime(minutes: 2)

        if pkg.currentItemIndex + 1 < pkg.items.count {
            pkg.currentItemIndex += 1
        }
        self.currentPackage = pkg
    }
}
