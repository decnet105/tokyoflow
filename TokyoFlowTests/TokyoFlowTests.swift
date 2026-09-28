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
        themeManager.currentTheme = .tokyoSubway
        XCTAssertEqual(themeManager.currentTheme, .tokyoSubway)
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_tokyo_subway")

        themeManager.currentTheme = .washiPaper
        XCTAssertEqual(themeManager.currentTheme, .washiPaper)
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_washi_paper")

        themeManager.currentTheme = .readingCat
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_reading_cat")

        themeManager.currentTheme = .liquidGlass
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_liquid_glass")
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
        XCTAssertGreaterThan(primary.durationSec, 3000.0, "Should be approximately 55 minutes")
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

        // N5 is 100% free
        XCTAssertTrue(sub.canAccessJLPTLevel("N5"), "N5 must be free")
        // N4-N1 requires Pro
        XCTAssertFalse(sub.canAccessJLPTLevel("N1"), "N1 must require Pro")

        // Free daily reviews limit
        XCTAssertEqual(sub.maxFreeDailyReviews, 15)

        // Mock upgrade to Pro
        sub.isPro = true
        XCTAssertTrue(sub.canAccessJLPTLevel("N1"), "Pro user can access all levels")
        XCTAssertGreaterThan(sub.remainingFreeReviewsToday, 100)
    }
}
