import SwiftUI

public struct FlashcardDeckView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var userProfile: UserProfile
    @State private var currentIndex = 0
    @State private var isFlipped = false

    private var deck: [SRSItem] {
        userProfile.bookmarkedPhrases
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 24) {
                    if deck.isEmpty {
                        VStack(spacing: 12) {
                            Image(systemName: "bookmark.slash.fill")
                                .font(.system(size: 44))
                                .foregroundColor(.secondary)
                            Text("No Bookmarked Phrases")
                                .font(.headline)
                            Text("Bookmark phrases in scenarios or survival cheat sheets to review them here with Spaced Repetition.")
                                .font(.footnote)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                                .padding(.horizontal, 32)
                        }
                        .padding(24)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(.horizontal)
                        .padding(.top, 60)
                        Spacer()
                    } else {
                        let currentItem = deck[min(currentIndex, deck.count - 1)]

                        // Progress Header
                        HStack {
                            Text("Card \(currentIndex + 1) of \(deck.count)")
                                .font(.caption)
                                .fontWeight(.bold)
                                .foregroundColor(.secondary)
                            Spacer()
                            Text("Ease Factor: \(String(format: "%.1f", currentItem.easeFactor))")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                        .padding(.horizontal)
                        .padding(.top, 8)

                        // Flashcard Flip View
                        ZStack {
                            RoundedRectangle(cornerRadius: 20)
                                .fill(.ultraThinMaterial)
                                .shadow(color: Color.black.opacity(0.06), radius: 12, x: 0, y: 4)

                            VStack(spacing: 16) {
                                Text(currentItem.context)
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .foregroundColor(.orange)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 4)
                                    .background(Color.orange.opacity(0.12))
                                    .cornerRadius(8)

                                Text(currentItem.japanese)
                                    .font(.system(size: 28, weight: .bold, design: .rounded))
                                    .multilineTextAlignment(.center)
                                    .padding(.horizontal)

                                if isFlipped {
                                    Divider().padding(.horizontal, 40)

                                    Text(currentItem.reading)
                                        .font(.headline)
                                        .foregroundColor(.secondary)

                                    Text(currentItem.english)
                                        .font(.title3)
                                        .fontWeight(.medium)
                                        .multilineTextAlignment(.center)
                                        .foregroundColor(.primary)
                                        .padding(.horizontal)
                                } else {
                                    Text("Tap to reveal reading & meaning")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                        .padding(.top, 20)
                                }

                                AudioButton(textToSpeak: currentItem.japanese)
                            }
                            .padding(24)
                        }
                        .frame(height: 320)
                        .padding(.horizontal)
                        .onTapGesture {
                            withAnimation(.spring(response: 0.4, dampingFraction: 0.7)) {
                                isFlipped.toggle()
                            }
                        }

                        // SRS Grade Buttons
                        if isFlipped {
                            VStack(spacing: 8) {
                                Text("How well did you recall this?")
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                HStack(spacing: 12) {
                                    Button("Again (Hard)") {
                                        handleGrade(.incorrect)
                                    }
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .padding()
                                    .frame(maxWidth: .infinity)
                                    .background(Color.red.opacity(0.15))
                                    .foregroundColor(.red)
                                    .cornerRadius(12)

                                    Button("Good") {
                                        handleGrade(.good)
                                    }
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .padding()
                                    .frame(maxWidth: .infinity)
                                    .background(Color.blue.opacity(0.15))
                                    .foregroundColor(.blue)
                                    .cornerRadius(12)

                                    Button("Easy (Mastered)") {
                                        handleGrade(.perfect)
                                    }
                                    .font(.caption)
                                    .fontWeight(.bold)
                                    .padding()
                                    .frame(maxWidth: .infinity)
                                    .background(Color.green.opacity(0.15))
                                    .foregroundColor(.green)
                                    .cornerRadius(12)
                                }
                                .padding(.horizontal)
                            }
                        }

                        Spacer()
                    }
                }
            }
            .navigationTitle("SRS Review Deck")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }

    private func handleGrade(_ grade: SRSGrade) {
        if currentIndex < userProfile.bookmarkedPhrases.count {
            var item = userProfile.bookmarkedPhrases[currentIndex]
            SRSService.processReview(item: &item, grade: grade)
            userProfile.bookmarkedPhrases[currentIndex] = item
        }

        #if os(iOS)
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
        #endif

        isFlipped = false
        if currentIndex < deck.count - 1 {
            currentIndex += 1
        } else {
            currentIndex = 0
        }
    }
}
