import SwiftUI

public struct InteractiveRoleplayView: View {
    public let scenario: Scenario
    public let challenge: InteractiveChallenge
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedOptionIndex: Int? = nil
    @State private var showFeedback: Bool = false
    @State private var isSuccess: Bool = false

    @ObservedObject private var languageManager = LanguageManager.shared

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                VStack(spacing: 24) {
                    // Header Prompt
                    VStack(spacing: 8) {
                        Image(systemName: "theatermasks.fill")
                            .font(.system(size: 36))
                            .foregroundColor(.accentColor)

                        Text(languageManager.isEnglish ? "Roleplay Scenario Challenge" : "实战场景角色扮演挑战")
                            .font(.title3)
                            .fontWeight(.bold)

                        Text(challenge.localizedPrompt)
                            .font(.subheadline)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                            .padding(.horizontal)
                    }
                    .padding(.top)

                    // Multiple Choice Options
                    VStack(spacing: 12) {
                        ForEach(Array(challenge.options.enumerated()), id: \.offset) { index, option in
                            Button(action: {
                                selectedOptionIndex = index
                                showFeedback = true
                                isSuccess = option.isCorrect
                                if isSuccess {
                                    userProfile.markScenarioCompleted(scenario.id)
                                }
                                #if os(iOS)
                                let generator = UINotificationFeedbackGenerator()
                                generator.notificationOccurred(option.isCorrect ? .success : .error)
                                #endif
                            }) {
                                HStack(alignment: .top, spacing: 12) {
                                    ZStack {
                                        Circle()
                                            .stroke(Color.secondary.opacity(0.3), lineWidth: 1.5)
                                            .frame(width: 24, height: 24)
                                        if selectedOptionIndex == index {
                                            Circle()
                                                .fill(option.isCorrect ? Color.green : Color.red)
                                                .frame(width: 14, height: 14)
                                        }
                                    }

                                    VStack(alignment: .leading, spacing: 4) {
                                        Text(option.text)
                                            .font(.headline)
                                            .foregroundColor(.primary)
                                        Text(option.romaji)
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                    Spacer()
                                    AudioButton(textToSpeak: option.text)
                                }
                                .padding()
                                .background(
                                    selectedOptionIndex == index
                                        ? (option.isCorrect ? Color.green.opacity(0.18) : Color.red.opacity(0.18))
                                        : Color.primary.opacity(0.04)
                                )
                                .background(.ultraThinMaterial)
                                .cornerRadius(14)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 14)
                                        .stroke(
                                            selectedOptionIndex == index
                                                ? (option.isCorrect ? Color.green : Color.red)
                                                : Color.primary.opacity(0.08),
                                            lineWidth: 1.5
                                        )
                                )
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal)

                    // Feedback Explanation
                    if showFeedback, let idx = selectedOptionIndex {
                        let option = challenge.options[idx]
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Image(systemName: option.isCorrect ? "checkmark.circle.fill" : "xmark.circle.fill")
                                    .foregroundColor(option.isCorrect ? .green : .red)
                                Text(languageManager.isEnglish ? (option.isCorrect ? "Excellent! Natural Tokyo Japanese" : "Not Quite Right") : (option.isCorrect ? "答对了！地道东京实战表达" : "还不够地道，再试一次吧"))
                                    .font(.headline)
                                    .foregroundColor(option.isCorrect ? .green : .red)
                            }
                            Text(option.localizedExplanation)
                                .font(.footnote)
                                .foregroundColor(.primary.opacity(0.9))
                        }
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(option.isCorrect ? Color.green.opacity(0.15) : Color.red.opacity(0.15))
                        .background(.ultraThinMaterial)
                        .cornerRadius(12)
                        .padding(.horizontal)
                    }

                    Spacer()

                    Button(action: { dismiss() }) {
                        Text(languageManager.isEnglish ? (showFeedback ? "Continue" : "Cancel") : (showFeedback ? "完成并继续" : "取消"))
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.accentColor)
                            .foregroundColor(.white)
                            .cornerRadius(14)
                    }
                    .padding(.horizontal)
                    .padding(.bottom)
                }
            }
            .navigationTitle(languageManager.isEnglish ? "Live Simulation" : "实境演练")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}
