import XCTest
@testable import TokyoFlow

final class TokyoFlowTests: XCTestCase {

    func testScenariosLoadSuccessfully() {
        let manager = DataManager.shared
        manager.loadAllData()

        XCTAssertFalse(manager.scenarios.isEmpty, "Scenarios should be loaded from JSON")
        XCTAssertGreaterThanOrEqual(manager.scenarios.count, 6, "Should contain at least 6 core scenarios")

        for scenario in manager.scenarios {
            XCTAssertFalse(scenario.id.isEmpty)
            XCTAssertFalse(scenario.title.isEmpty)
            XCTAssertFalse(scenario.dialogue.isEmpty)
            XCTAssertFalse(scenario.keyVocabulary.isEmpty)
        }
    }

    func testMangaLessonsLoadSuccessfully() {
        let manager = DataManager.shared
        manager.loadAllData()

        XCTAssertFalse(manager.mangaLessons.isEmpty, "Manga lessons should be loaded from JSON")
        for lesson in manager.mangaLessons {
            XCTAssertFalse(lesson.id.isEmpty)
            XCTAssertFalse(lesson.panels.isEmpty)
            XCTAssertFalse(lesson.grammarBreakdowns.isEmpty)
        }
    }

    func testAnnouncementsAndListeningQuiz() {
        let manager = DataManager.shared
        manager.loadAllData()

        XCTAssertFalse(manager.announcements.isEmpty, "Announcements should be loaded from JSON")
        for ann in manager.announcements {
            XCTAssertFalse(ann.id.isEmpty)
            if let quiz = ann.listeningQuiz {
                XCTAssertGreaterThan(quiz.options.count, 1)
                XCTAssertTrue(quiz.correctIndex >= 0 && quiz.correctIndex < quiz.options.count)
            }
        }
    }

    func testDojoBattlesLoadSuccessfully() {
        let manager = DataManager.shared
        manager.loadAllData()

        XCTAssertFalse(manager.dojoBattles.isEmpty, "Dojo battles should be loaded from JSON")
        for battle in manager.dojoBattles {
            XCTAssertFalse(battle.id.isEmpty)
            XCTAssertFalse(battle.rounds.isEmpty)
            XCTAssertFalse(battle.ninjaComboPhrase.isEmpty)
            for round in battle.rounds {
                XCTAssertFalse(round.clerkPrompt.isEmpty)
                XCTAssertGreaterThanOrEqual(round.options.count, 2)
                XCTAssertTrue(round.options.contains(where: { $0.isCorrect }))
            }
        }
    }

    func testSM2SpacedRepetitionAlgorithm() {
        var item = SRSItem(
            japanese: "領収書をお願いします",
            reading: "りょうしゅうしょをおねがいします",
            english: "Receipt please",
            context: "Shopping"
        )

        XCTAssertEqual(item.repetition, 0)
        XCTAssertEqual(item.intervalDays, 1)

        // First successful review (Good)
        SRSService.processReview(item: &item, grade: .good)
        XCTAssertEqual(item.repetition, 1)
        XCTAssertEqual(item.intervalDays, 1)

        // Second successful review (Perfect)
        SRSService.processReview(item: &item, grade: .perfect)
        XCTAssertEqual(item.repetition, 2)
        XCTAssertEqual(item.intervalDays, 6)

        // Third review (Good)
        SRSService.processReview(item: &item, grade: .good)
        XCTAssertEqual(item.repetition, 3)
        XCTAssertGreaterThanOrEqual(item.intervalDays, 14)

        // Failure review (Blackout)
        SRSService.processReview(item: &item, grade: .blackout)
        XCTAssertEqual(item.repetition, 0)
        XCTAssertEqual(item.intervalDays, 1)
    }

    func testUserProfileBookmarkAndProgress() {
        let profile = UserProfile()
        let initialCount = profile.bookmarkedPhrases.count

        profile.toggleBookmark(japanese: "テストフレーズ", reading: "てすと", english: "Test Phrase", context: "Testing")
        XCTAssertEqual(profile.bookmarkedPhrases.count, initialCount + 1)
        XCTAssertTrue(profile.isBookmarked("テストフレーズ"))

        profile.toggleBookmark(japanese: "テストフレーズ", reading: "てすと", english: "Test Phrase", context: "Testing")
        XCTAssertEqual(profile.bookmarkedPhrases.count, initialCount)
        XCTAssertFalse(profile.isBookmarked("テストフレーズ"))
    }

    func testDailyNewsAndShadowing() {
        let newsService = NHKNewsService.shared
        newsService.loadBundledNews()

        XCTAssertFalse(newsService.dailyNews.isEmpty, "Daily news should contain articles")
        for news in newsService.dailyNews {
            XCTAssertFalse(news.id.isEmpty)
            XCTAssertFalse(news.title.isEmpty)
            XCTAssertFalse(news.contentSentences.isEmpty)
            XCTAssertFalse(news.vocabulary.isEmpty)
            XCTAssertFalse(news.comprehensionQuiz.isEmpty)
        }
    }

    func testGamificationAndQuests() {
        let gamification = GamificationService.shared
        gamification.setupDailyQuests()

        XCTAssertFalse(gamification.dailyQuests.isEmpty, "Daily quests should be populated")
        XCTAssertGreaterThanOrEqual(gamification.leaderboardUsers.count, 3, "Leaderboard should have users")

        let initialTP = gamification.tokyoPoints
        let initialEXP = gamification.totalEXP

        gamification.addRewards(tp: 50, exp: 100)
        XCTAssertEqual(gamification.tokyoPoints, initialTP + 50)
        XCTAssertEqual(gamification.totalEXP, initialEXP + 100)
    }

    func testThemeManagerSelection() {
        let themeManager = ThemeManager.shared
        themeManager.currentTheme = .none
        XCTAssertEqual(themeManager.currentTheme, .none)
        XCTAssertNil(themeManager.currentTheme.assetName)

        themeManager.currentTheme = .washiPaper
        XCTAssertEqual(themeManager.currentTheme, .washiPaper)
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_washi_paper")

        themeManager.currentTheme = .morningMist
        XCTAssertEqual(themeManager.currentTheme, .morningMist)

        themeManager.currentTheme = .warmSepia
        XCTAssertEqual(themeManager.currentTheme, .warmSepia)
    }

    func testJapaneseWordSegmenter() {
        let text = "JR東日本は東京やその近くを走る電車の終電の時間を早めると発表しました。"
        let tokens = JapaneseWordSegmenter.shared.segment(text: text)
        XCTAssertFalse(tokens.isEmpty, "Sentence should be split into word tokens")
        XCTAssertGreaterThanOrEqual(tokens.count, 5, "Should have multiple words")

        let tokenTexts = tokens.map { $0.text }
        XCTAssertTrue(tokenTexts.contains("JR東日本") || tokenTexts.contains("東京") || tokenTexts.contains("電車"))
    }

    func testTokyoProsodyEngine() {
        let raw = "JR東日本は東京やその近くを走る電車の終電の時間を早めると発表しました。"
        let formatted = TokyoProsodyEngine.formatProsodyText(raw, style: .newsBroadcast)
        XCTAssertFalse(formatted.isEmpty)

        let settings = TokyoProsodyEngine.prosodySettings(for: .newsBroadcast)
        XCTAssertGreaterThan(settings.rate, 0.4)
        XCTAssertLessThan(settings.rate, 0.6)
        XCTAssertGreaterThan(settings.pitch, 0.9)
    }

    func testKanaDataManager() {
        let kana = KanaDataManager.shared
        XCTAssertEqual(kana.seionList.count, 46, "Should contain 46 Seion kana")
        XCTAssertGreaterThanOrEqual(kana.dakuonList.count, 20, "Should contain Dakuon kana")
        XCTAssertFalse(kana.yoonList.isEmpty, "Should contain Yoon kana")

        for item in kana.seionList + kana.dakuonList + kana.yoonList {
            XCTAssertFalse(item.hiragana.isEmpty)
            XCTAssertFalse(item.katakana.isEmpty)
            XCTAssertFalse(item.romaji.isEmpty)
            XCTAssertFalse(item.exampleWordJa.isEmpty)
            XCTAssertFalse(item.exampleWordRomaji.isEmpty, "Every kana must have an example word romaji")
            XCTAssertFalse(item.exampleWordEn.isEmpty)
        }
    }

    func testTokyoRadioDataManagerAndService() {
        let radioData = TokyoRadioDataManager.shared
        XCTAssertFalse(radioData.stations.isEmpty, "Radio stations should be loaded")

        let primary = radioData.stations[0]
        XCTAssertEqual(primary.id, "nhk_journal_55")
        XCTAssertGreaterThan(primary.durationSec, 60.0, "Should contain authentic broadcast duration")
        XCTAssertFalse(primary.chapters.isEmpty, "Should contain chapter bookmarks")
        XCTAssertFalse(primary.chapters[0].transcriptSentences.isEmpty, "Chapters should contain transcript sentences for live shadowing")

        let radioService = TokyoRadioService.shared
        radioService.setSleepTimer(minutes: 30)
        XCTAssertEqual(radioService.remainingSleepSeconds, 1800)

        radioService.setSleepTimer(minutes: nil)
        XCTAssertNil(radioService.remainingSleepSeconds)
    }

    func testTokyoVoiceBankService() {
        let voiceBank = TokyoVoiceBankService.shared

        // Test Kana Pronunciation mapping
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "あ"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "か"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "サ"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "きゃ"))

        // Test Kana Example Word matching
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "ありがとう"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "いぬ (犬)"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "さくら (桜)"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "すいか (Suica)"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "とうきょう (東京)"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "ラーメン"))

        // Test High-frequency survival phrases
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "温めてください"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "大丈夫です"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "とりあえず生で！"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "お会計お願いします"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "袋は大丈夫です"))

        // Test Grammar Formulas & Sentences
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "〜てください / 〜ないでください"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "白線の内側までお下がりください。"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "〜たら / 〜なら / 〜ば / 〜と (四大条件假定)"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "〜を踏まえて / 〜に基づいて"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "〜ざるを得ない"))

        // Test Essential Core Vocabulary & Pairs
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "開ける"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "閉める"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "相応しい"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "相席"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "相容れない"))


        // Test Tokyo Vocabulary & SFX
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "Suica"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "居酒屋"))
        XCTAssertTrue(voiceBank.hasNativeAudio(for: "ドキドキ"))

        // Test audio file URL resolution
        let filename = voiceBank.findAudioFilename(for: "温めてください")
        XCTAssertNotNil(filename)
        if let fn = filename {
            XCTAssertNotNil(voiceBank.audioURL(for: fn))
        }
    }


    func testGamificationDailyCheckInAndMicroLearning() {
        let gamification = GamificationService.shared
        gamification.setupDailyQuests()
        gamification.setupLeaderboard()

        // Test Weekly check-in calendar generation
        let weeklyStatus = gamification.getWeeklyCheckInStatus()
        XCTAssertEqual(weeklyStatus.count, 7, "Weekly check-in status must contain all 7 days (Mon-Sun)")
        XCTAssertTrue(weeklyStatus.contains(where: { $0.isToday }), "Weekly status must highlight today")

        // Test Micro-learning progress tracking
        let initialMinutes = gamification.dailyMinutesLearned
        gamification.recordMicroLearningTime(minutes: 5)
        XCTAssertEqual(gamification.dailyMinutesLearned, initialMinutes + 5)
        XCTAssertGreaterThan(gamification.microLearningProgress, 0.0)

        // Test Daily Quests configuration
        XCTAssertGreaterThanOrEqual(gamification.dailyQuests.count, 5)
        XCTAssertTrue(gamification.dailyQuests.contains(where: { $0.id == "q_checkin" }))
        XCTAssertTrue(gamification.dailyQuests.contains(where: { $0.id == "q_micro_time" }))
    }

    func testTokyoLeaderboardMultiTier() {
        let gamification = GamificationService.shared
        gamification.setupLeaderboard()

        // Test Weekly League
        XCTAssertFalse(gamification.leaderboardUsers.isEmpty)
        XCTAssertTrue(gamification.leaderboardUsers.contains(where: { $0.isCurrentUser }))

        // Test All-Time Hall of Fame
        XCTAssertFalse(gamification.allTimeLeaderboardUsers.isEmpty)
        XCTAssertEqual(gamification.allTimeLeaderboardUsers[0].rank, 1)

        // Test Friends League
        XCTAssertFalse(gamification.friendsLeaderboardUsers.isEmpty)
        XCTAssertTrue(gamification.friendsLeaderboardUsers.contains(where: { $0.isCurrentUser }))
    }

    func testKana7DayNonRepeatingVocabulary() {
        let kanaData = KanaDataManager.shared
        XCTAssertFalse(kanaData.seionList.isEmpty)

        for item in kanaData.seionList {
            XCTAssertEqual(item.exampleWords.count, 7, "Each kana item must have 7 distinct daily example words")
            
            // Check uniqueness across the 7 days of the week
            var distinctWords = Set<String>()
            for day in 0..<7 {
                let word = item.exampleWordForDay(dayOffset: day)
                distinctWords.insert(word.japanese)
            }
            XCTAssertEqual(distinctWords.count, 7, "Kana \(item.hiragana) must have 7 unique non-repeating words for the 7 days of the week")
            
            // Check today's rotation word
            XCTAssertFalse(item.dailyExampleWord.japanese.isEmpty)
            XCTAssertFalse(item.dailyExampleWord.romaji.isEmpty)
            XCTAssertFalse(item.dailyExampleWord.english.isEmpty)
        }
    }

    func testNotificationServiceConfiguration() {
        let notificationService = NotificationService.shared
        XCTAssertEqual(notificationService.dailyReminderHour, 21, "Daily reminder must be set to 9:00 PM (21:00)")
        XCTAssertEqual(notificationService.dailyReminderMinute, 0)
    }

    func testJLPTDictionaryServiceAndSearch() {
        let dict = JLPTDictionaryService.shared
        dict.loadDictionary()
        XCTAssertFalse(dict.allWords.isEmpty, "JLPT Dictionary should have words loaded")

        // Test Level Filter
        dict.selectedLevel = .n5
        let n5Words = dict.filteredWords
        XCTAssertFalse(n5Words.isEmpty)
        for w in n5Words {
            XCTAssertEqual(w.level, "N5")
        }

        // Test Search query
        dict.searchQuery = "食べる"
        let searchResults = dict.filteredWords
        XCTAssertFalse(searchResults.isEmpty)
        XCTAssertEqual(searchResults[0].reading, "たべる")

        // Reset
        dict.searchQuery = ""
        dict.selectedLevel = .all
    }

    func testWeakWordTrackerImplicitCollection() {
        let tracker = WeakWordTrackerService.shared
        
        // Test repeated listening trigger (>= 2 times)
        tracker.recordListen(word: "相応しい", reading: "ふさわしい", meaning: "合适")
        tracker.recordListen(word: "相応しい", reading: "ふさわしい", meaning: "合适")

        XCTAssertTrue(tracker.activeWeakWords.contains(where: { $0.word == "相応しい" }), "Word listened to twice must be tracked as weak word")
        
        // Test Mastering weak word
        let initialMastered = tracker.masteredCount
        tracker.markMastered(word: "相応しい")
        XCTAssertEqual(tracker.masteredCount, initialMastered + 1)
        XCTAssertFalse(tracker.activeWeakWords.contains(where: { $0.word == "相応しい" }))
    }

    func testSubscriptionFreemiumAccessControl() {
        let sub = SubscriptionService.shared
        sub.isPro = false

        // During YouTube + Free App Growth Phase, all levels N5-N1 are 100% free
        XCTAssertTrue(sub.canAccessJLPTLevel("N5"), "N5 must be free")
        XCTAssertTrue(sub.canAccessJLPTLevel("N1"), "N1 must be free during community growth phase")

        // Free daily reviews unlimited
        XCTAssertEqual(sub.maxFreeDailyReviews, 9999)
        XCTAssertEqual(sub.remainingFreeReviewsToday, 9999)

        // Mock upgrade to Pro
        sub.isPro = true
        XCTAssertTrue(sub.canAccessJLPTLevel("N1"), "Pro user can access all levels")
        XCTAssertGreaterThan(sub.remainingFreeReviewsToday, 100)
    }

    func testTokyoGenerativeLearningEngine() {
        let engine = TokyoGenerativeLearningEngine.shared
        XCTAssertFalse(engine.presetDestinations.isEmpty, "Presets must not be empty")

        // Test preset plan generation
        engine.generatePlan(for: "shibuya")
        XCTAssertEqual(engine.selectedPresetId, "shibuya")

        // Test custom plan generation
        engine.generateCustomPlan(userPrompt: "台场高达与海滨公园")
        XCTAssertEqual(engine.selectedPresetId, "custom")
    }

    func testTokyoLearningPackageEngineAllModes() {
        let engine = TokyoLearningPackageEngine.shared

        // Test Scenario Context Track
        for mode in LearningContextMode.allCases {
            let package = engine.generatePackage(for: mode, focus: .practicalFluency)
            XCTAssertEqual(package.mode, mode)
            XCTAssertGreaterThan(package.estimatedMinutes, 0)
            XCTAssertFalse(package.items.isEmpty, "Package for \(mode.rawValue) must have items")
            XCTAssertGreaterThanOrEqual(package.items.count, 2, "Context package should have at least 2 grain items")

            for item in package.items {
                XCTAssertFalse(item.id.isEmpty)
                XCTAssertFalse(item.title.isEmpty)
                XCTAssertFalse(item.japaneseText.isEmpty)
                XCTAssertFalse(item.englishMeaning.isEmpty)
            }
        }

        // Test JLPT Level Track (N5 ~ N1) with Exam Focus
        for lvl in JLPTLevelTrack.allCases {
            let pkg = engine.generateLevelPackage(for: lvl, focus: .examSprint)
            XCTAssertEqual(pkg.levelTrack, lvl)
            XCTAssertEqual(pkg.focusMode, .examSprint)
            XCTAssertFalse(pkg.items.isEmpty, "Level package for \(lvl.shortLabel) must have items")
            XCTAssertGreaterThanOrEqual(pkg.items.count, 3)

            for item in pkg.items {
                XCTAssertFalse(item.id.isEmpty)
                XCTAssertFalse(item.japaneseText.isEmpty)
            }
        }
    }

    func testJLPTGrammarServiceAndFormulas() {
        let grammarService = JLPTGrammarService.shared
        grammarService.loadGrammarData()

        XCTAssertFalse(grammarService.allGrammar.isEmpty, "Grammar data should be loaded")

        // Test Level Filter
        grammarService.selectedLevel = .n5
        let n5Grammar = grammarService.filteredGrammar
        XCTAssertFalse(n5Grammar.isEmpty)
        for g in n5Grammar {
            XCTAssertEqual(g.level.uppercased(), "N5")
            XCTAssertFalse(g.connectionRule.isEmpty)
            XCTAssertFalse(g.nuanceExplanation.isEmpty)
        }

        // Test Quiz Present
        let sample = grammarService.allGrammar.first(where: { $0.quiz != nil })
        XCTAssertNotNil(sample)
        if let quiz = sample?.quiz {
            XCTAssertFalse(quiz.question.isEmpty)
            XCTAssertGreaterThanOrEqual(quiz.options.count, 2)
            XCTAssertTrue(quiz.correctIndex >= 0 && quiz.correctIndex < quiz.options.count)
        }

        // Reset
        grammarService.selectedLevel = .all
    }

    func testTokyoLearningPackageAudioKeySynchronization() {
        let engine = TokyoLearningPackageEngine.shared
        let voiceBank = TokyoVoiceBankService.shared

        // Verify Coffee Break drill specifically (Screenshot regression test)
        let coffeePackage = engine.generatePackage(for: .coffeeBreak, focus: .practicalFluency)
        let microwaveDrill = coffeePackage.items.first(where: { $0.japaneseText.contains("温めますか") })
        XCTAssertNotNil(microwaveDrill, "Microwave prompt item must exist in coffee break")
        XCTAssertEqual(microwaveDrill?.japaneseText, "お弁当温めますか？")
        XCTAssertEqual(microwaveDrill?.audioKey, "お弁当温めますか？", "AudioKey must match displayed Japanese text exactly")
        XCTAssertTrue(voiceBank.hasNativeAudio(for: microwaveDrill!.audioKey), "VoiceBank must contain native voice for microwave drill")

        // Verify All Scenario Tracks have native voice bank entries
        for mode in LearningContextMode.allCases {
            let pkg = engine.generatePackage(for: mode, focus: .practicalFluency)
            for item in pkg.items {
                XCTAssertFalse(item.audioKey.isEmpty, "Item audioKey cannot be empty")
                XCTAssertTrue(voiceBank.hasNativeAudio(for: item.audioKey), "VoiceBank must have native audio for \(item.audioKey)")
            }
        }

        // Verify All JLPT Level Tracks have native voice bank entries
        for lvl in JLPTLevelTrack.allCases {
            let pkg = engine.generateLevelPackage(for: lvl, focus: .examSprint)
            for item in pkg.items {
                XCTAssertFalse(item.audioKey.isEmpty, "Item audioKey cannot be empty")
                XCTAssertTrue(voiceBank.hasNativeAudio(for: item.audioKey), "VoiceBank must have native audio for \(item.audioKey)")
            }
        }
    }

    func testInboxAndNightlySummaryAudioVerification() {
        let notificationService = NotificationService.shared
        let voiceBank = TokyoVoiceBankService.shared

        // 1. Verify all stored / seeded Inbox messages with golden sentences have 100% native audio
        for msg in notificationService.messages {
            if let golden = msg.goldenSentence, !golden.isEmpty {
                XCTAssertTrue(
                    voiceBank.hasNativeAudio(for: golden),
                    "Inbox golden sentence '\(golden)' must have 100% native studio voice bank audio (no TTS fallback)"
                )
            }
        }

        // 2. Verify dynamically generated today's nightly summary
        let todaySummary = notificationService.generateTodayNightlySummary()
        if let golden = todaySummary.goldenSentence, !golden.isEmpty {
            XCTAssertTrue(
                voiceBank.hasNativeAudio(for: golden),
                "Today's generated summary golden sentence '\(golden)' must have native studio voice"
            )
        }
    }

    func testKaraokeMoraAlignmentPrecision() {
        let segmenter = JapaneseWordSegmenter.shared

        // Test Japanese word segmentation with spaced furigana reference
        let text = "すみません、注文をお願いします。"
        let furi = "すみません、 ちゅうもんを おねがいします。"
        let tokens = segmenter.segment(text: text, furiganaReference: furi)

        XCTAssertFalse(tokens.isEmpty)
        XCTAssertGreaterThanOrEqual(tokens.count, 2)

        // Test pure text segmentation
        let pureTokens = segmenter.segment(text: "東京駅に行きます")
        XCTAssertFalse(pureTokens.isEmpty)
        XCTAssertTrue(pureTokens.contains(where: { $0.text.contains("東京") || $0.text.contains("東京駅") }))
    }

    func testDailyClassroomScenarioAndJLPTPackageEngines() {
        let engine = TokyoLearningPackageEngine.shared
        let voiceBank = TokyoVoiceBankService.shared

        // 1. Verify Track 1: 5-Minute Practical Scenario Package
        let scenarioPkg = engine.generateTodayScenarioPackage()
        XCTAssertFalse(scenarioPkg.title.isEmpty)
        XCTAssertEqual(scenarioPkg.durationSeconds, 300, "Daily scenario must be strictly timeboxed to 300 seconds (5 minutes)")
        XCTAssertFalse(scenarioPkg.sceneDialogue.isEmpty, "Scenario must contain dialogue")
        XCTAssertFalse(scenarioPkg.vocabGrammarAnalyses.isEmpty, "Scenario must contain vocab & grammar analyses")
        XCTAssertFalse(scenarioPkg.youtubeVideoId.isEmpty, "Scenario must have linked YouTube lesson")
        XCTAssertFalse(scenarioPkg.goldenSentence.isEmpty, "Scenario must have 30s shadowing golden sentence")
        XCTAssertTrue(voiceBank.hasNativeAudio(for: scenarioPkg.goldenSentence), "Golden sentence must have native voice bank audio")

        // 2. Verify Track 2: JLPT 2 New + 3 Review Ebbinghaus Package
        for level in ["N5", "N4", "N3"] {
            let jlptPkg = engine.generateTodayJLPTPackage(level: level)
            XCTAssertEqual(jlptPkg.newItems.count, 2, "JLPT package must contain strictly 2 NEW items per day")
            XCTAssertEqual(jlptPkg.reviewItems.count, 3, "JLPT package must contain strictly 3 REVIEW items (Ebbinghaus Spaced Repetition)")
            XCTAssertEqual(jlptPkg.allItems.count, 5, "Total daily drill count must be exactly 5 items")

            for item in jlptPkg.allItems {
                XCTAssertFalse(item.kanji.isEmpty)
                XCTAssertFalse(item.reading.isEmpty)
                XCTAssertFalse(item.romaji.isEmpty)
                XCTAssertFalse(item.englishMeaning.isEmpty)
                XCTAssertTrue(voiceBank.hasNativeAudio(for: item.kanji), "VoiceBank must contain native studio audio for \(item.kanji)")
            }
        }
    }
}





