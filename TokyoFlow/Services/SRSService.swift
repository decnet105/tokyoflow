import Foundation

public enum SRSGrade: Int {
    case blackout = 0 // Complete blackout
    case incorrect = 1 // Incorrect response; remembered the right answer when revealed
    case hard = 2 // Incorrect; correct answer seemed easy to recall
    case good = 3 // Correct response after hesitation
    case perfect = 4 // Perfect response without hesitation
}

public class SRSService {
    public static func processReview(item: inout SRSItem, grade: SRSGrade) {
        let q = grade.rawValue

        if q >= 3 {
            // Correct response
            if item.repetition == 0 {
                item.intervalDays = 1
            } else if item.repetition == 1 {
                item.intervalDays = 6
            } else {
                item.intervalDays = Int(round(Double(item.intervalDays) * item.easeFactor))
            }
            item.repetition += 1
        } else {
            // Failed response
            item.repetition = 0
            item.intervalDays = 1
        }

        // Calculate new Ease Factor (EF)
        // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        let delta = 0.1 - Double(5 - q) * (0.08 + Double(5 - q) * 0.02)
        item.easeFactor = max(1.3, item.easeFactor + delta)

        // Set next review date
        item.lastReviewedDate = Date()
        item.nextReviewDate = Calendar.current.date(byAdding: .day, value: item.intervalDays, to: Date()) ?? Date()
    }
}
