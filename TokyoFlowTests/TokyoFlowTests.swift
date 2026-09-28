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
        themeManager.currentTheme = .washiPaper
        XCTAssertEqual(themeManager.currentTheme, .washiPaper)
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_washi_paper")

        themeManager.currentTheme = .readingCat
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_reading_cat")

        themeManager.currentTheme = .liquidGlass
        XCTAssertEqual(themeManager.currentTheme.assetName, "wallpaper_liquid_glass")
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
}
