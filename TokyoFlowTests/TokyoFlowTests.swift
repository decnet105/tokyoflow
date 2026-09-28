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
}
