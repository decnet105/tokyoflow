import SwiftUI

public struct JLPTGrammarLabView: View {
    @StateObject private var grammarService = JLPTGrammarService.shared
    @StateObject private var voiceBank = TokyoVoiceBankService.shared
    @State private var selectedGrammarForQuiz: JLPTGrammarPoint?
    @State private var userSelectedQuizOption: Int?
    @State private var hasSubmittedQuiz: Bool = false

    private let scenarioFilterTags: [(id: String?, label: String, icon: String)] = [
        (nil, "All Scenarios", "square.grid.2x2"),
        ("transit", "Transit & Commute", "tram.fill"),
        ("dining", "Dining & Izakaya", "fork.knife"),
        ("shopping", "Shopping & Kombini", "bag.fill"),
        ("business", "Business & Meeting", "briefcase.fill"),
        ("daily", "Daily Living", "house.fill"),
        ("social", "Social & Politeness", "person.2.fill")
    ]

    public init() {}

    @State private var selectedGrammarForDetail: JLPTGrammarPoint? = nil

    public var body: some View {
        NavigationStack {
            TokyoDuoAdaptiveLayout(duoSplitRatio: 0.45) {
                // Left Screen: Search, Filters & Grammar Points Master List
                VStack(spacing: 0) {
                    // Top Level Filter Bar (N5 -> N1)
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(JLPTLevelFilter.allCases) { filter in
                                Button(action: {
                                    withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                                        grammarService.selectedLevel = filter
                                    }
                                }) {
                                    Text(filter.rawValue)
                                        .font(.system(size: 13, weight: .bold, design: .rounded))
                                        .padding(.horizontal, 14)
                                        .padding(.vertical, 8)
                                        .background(
                                            grammarService.selectedLevel == filter
                                                ? Color.blue
                                                : Color(UIColor.secondarySystemBackground)
                                        )
                                        .foregroundColor(
                                            grammarService.selectedLevel == filter
                                                ? .white
                                                : .primary
                                        )
                                        .cornerRadius(20)
                                }
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                    }
                    .background(Color(UIColor.systemBackground))

                    // Scenario Filter Bar
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 6) {
                            ForEach(scenarioFilterTags, id: \.label) { tag in
                                Button(action: {
                                    withAnimation {
                                        grammarService.selectedScenarioTag = tag.id
                                    }
                                }) {
                                    HStack(spacing: 4) {
                                        Image(systemName: tag.icon)
                                            .font(.system(size: 11))
                                        Text(tag.label)
                                            .font(.system(size: 11, weight: .semibold))
                                    }
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 6)
                                    .background(
                                        grammarService.selectedScenarioTag == tag.id
                                            ? Color.purple.opacity(0.2)
                                            : Color(UIColor.tertiarySystemBackground)
                                    )
                                    .foregroundColor(
                                        grammarService.selectedScenarioTag == tag.id
                                            ? .purple
                                            : .secondary
                                    )
                                    .cornerRadius(12)
                                }
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.bottom, 8)
                    }

                    // Grammar List
                    if grammarService.filteredGrammar.isEmpty {
                        VStack(spacing: 16) {
                            Spacer()
                            Image(systemName: "book.closed")
                                .font(.system(size: 48))
                                .foregroundColor(.secondary.opacity(0.6))
                            Text("No grammar formulas found")
                                .font(.headline)
                                .foregroundColor(.secondary)
                            Text("Try selecting a different level or scenario tag.")
                                .font(.subheadline)
                                .foregroundColor(.secondary.opacity(0.8))
                            Spacer()
                        }
                    } else {
                        List {
                            ForEach(grammarService.filteredGrammar) { item in
                                GrammarCardRow(
                                    grammar: item,
                                    isSelected: selectedGrammarForDetail?.id == item.id,
                                    onOpenQuiz: {
                                        selectedGrammarForQuiz = item
                                        userSelectedQuizOption = nil
                                        hasSubmittedQuiz = false
                                    }
                                )
                                .contentShape(Rectangle())
                                .onTapGesture {
                                    withAnimation {
                                        selectedGrammarForDetail = item
                                    }
                                }
                                .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
                                .listRowSeparator(.hidden)
                                .listRowBackground(Color.clear)
                            }
                        }
                        .listStyle(.plain)
                    }
                }
            } secondaryContent: {
                // Right Screen: Grammar Blueprint Detail Lab & Practice
                let activeGrammar = selectedGrammarForDetail ?? grammarService.filteredGrammar.first

                if let grammar = activeGrammar {
                    ScrollView {
                        VStack(alignment: .leading, spacing: 16) {
                            // Header Banner
                            HStack {
                                Text(grammar.level)
                                    .font(.system(size: 13, weight: .black, design: .rounded))
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 4)
                                    .background(levelColor(grammar.level))
                                    .foregroundColor(.white)
                                    .cornerRadius(8)

                                Text(grammar.title)
                                    .font(.system(size: 22, weight: .black, design: .rounded))

                                Spacer()

                                if let firstSent = grammar.sentences.first {
                                    AudioButton(textToSpeak: firstSent.japanese)
                                }
                            }

                            // Connection Formula
                            HStack(spacing: 6) {
                                Image(systemName: "arrow.triangle.merge")
                                    .font(.system(size: 13, weight: .bold))
                                    .foregroundColor(.blue)
                                Text("Rule: \(grammar.connectionRule)")
                                    .font(.system(size: 14, weight: .bold, design: .monospaced))
                                    .foregroundColor(.blue)
                            }
                            .padding(10)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.blue.opacity(0.08))
                            .cornerRadius(10)

                            // Meaning
                            Text(grammar.meaningEn)
                                .font(.system(size: 16, weight: .bold))
                                .foregroundColor(.accentColor)

                            // Nuance & Exam Insights
                            VStack(alignment: .leading, spacing: 6) {
                                HStack(alignment: .top, spacing: 6) {
                                    Image(systemName: "lightbulb.fill")
                                        .foregroundColor(.orange)
                                    Text("Nuance & Exam Pitfall Insights")
                                        .font(.system(size: 13, weight: .bold))
                                }
                                Text(grammar.nuanceExplanation)
                                    .font(.system(size: 13))
                                    .foregroundColor(.primary.opacity(0.9))
                                    .lineSpacing(3)
                            }
                            .padding(14)
                            .background(Color(UIColor.secondarySystemBackground))
                            .cornerRadius(12)

                            // Example Sentences
                            if !grammar.sentences.isEmpty {
                                VStack(alignment: .leading, spacing: 10) {
                                    Text("Example Context Sentences")
                                        .font(.system(size: 13, weight: .heavy))
                                        .foregroundColor(.secondary)
                                        .textCase(.uppercase)

                                    ForEach(grammar.sentences) { sent in
                                        HStack(alignment: .top, spacing: 8) {
                                            VStack(alignment: .leading, spacing: 3) {
                                                Text(sent.furigana)
                                                    .font(.system(size: 11))
                                                    .foregroundColor(.secondary)
                                                Text(sent.japanese)
                                                    .font(.system(size: 15, weight: .bold))
                                                    .foregroundColor(.primary)
                                                Text(sent.english)
                                                    .font(.system(size: 12))
                                                    .foregroundColor(.secondary)
                                            }
                                            Spacer()
                                            AudioButton(textToSpeak: sent.japanese)
                                        }
                                        .padding(12)
                                        .background(Color.primary.opacity(0.04))
                                        .cornerRadius(10)
                                    }
                                }
                            }

                            // Exam Trap Drill Button
                            if grammar.quiz != nil {
                                Button(action: {
                                    selectedGrammarForQuiz = grammar
                                    userSelectedQuizOption = nil
                                    hasSubmittedQuiz = false
                                }) {
                                    HStack {
                                        Image(systemName: "checkmark.circle.badge.questionmark")
                                            .font(.system(size: 14, weight: .bold))
                                        Text("Launch Exam Trap Drill")
                                            .font(.system(size: 14, weight: .bold))
                                        Spacer()
                                        Image(systemName: "arrow.right")
                                            .font(.system(size: 12, weight: .bold))
                                    }
                                    .foregroundColor(.white)
                                    .padding(14)
                                    .background(LinearGradient(colors: [.purple, .blue], startPoint: .leading, endPoint: .trailing))
                                    .cornerRadius(12)
                                }
                            }
                        }
                        .padding(18)
                        .background(.ultraThinMaterial)
                        .cornerRadius(20)
                        .padding(14)
                    }
                } else {
                    VStack(spacing: 12) {
                        Image(systemName: "sparkles")
                            .font(.system(size: 40))
                            .foregroundColor(.accentColor)
                        Text("Select a grammar point to inspect blueprint")
                            .font(.headline)
                            .foregroundColor(.secondary)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
            }
            .navigationTitle("Grammar Blueprint Lab")
            .navigationBarTitleDisplayMode(.inline)
            .searchable(text: $grammarService.searchQuery, prompt: "Search formula, meaning or connection...")
            .sheet(item: $selectedGrammarForQuiz) { item in
                if let quiz = item.quiz {
                    GrammarQuizModalView(
                        grammar: item,
                        quiz: quiz,
                        selectedOption: $userSelectedQuizOption,
                        hasSubmitted: $hasSubmittedQuiz
                    )
                }
            }
        }
    }
}

// MARK: - Grammar Card Row
struct GrammarCardRow: View {
    let grammar: JLPTGrammarPoint
    var isSelected: Bool = false
    let onOpenQuiz: () -> Void
    @StateObject private var voiceBank = TokyoVoiceBankService.shared

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // Header: Level Badge + Formula Title + Audio
            HStack(alignment: .center, spacing: 8) {
                Text(grammar.level)
                    .font(.system(size: 11, weight: .black, design: .rounded))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 3)
                    .background(levelColor(grammar.level))
                    .foregroundColor(.white)
                    .cornerRadius(6)

                Text(grammar.title)
                    .font(.system(size: 16, weight: .bold, design: .rounded))
                    .foregroundColor(.primary)

                Spacer()

                if let firstSent = grammar.sentences.first {
                    AudioButton(textToSpeak: firstSent.japanese)
                }
            }

            // Connection Rule
            HStack(spacing: 6) {
                Image(systemName: "arrow.triangle.merge")
                    .font(.system(size: 11, weight: .bold))
                    .foregroundColor(.blue)
                Text(grammar.connectionRule)
                    .font(.system(size: 12, weight: .medium, design: .monospaced))
                    .foregroundColor(.blue)
            }
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(Color.blue.opacity(0.08))
            .cornerRadius(6)

            // Meaning
            Text(grammar.meaningEn)
                .font(.system(size: 13, weight: .semibold))
                .foregroundColor(.accentColor)

            // Nuance & Usage Insight
            VStack(alignment: .leading, spacing: 4) {
                HStack(alignment: .top, spacing: 6) {
                    Image(systemName: "lightbulb.fill")
                        .font(.system(size: 12))
                        .foregroundColor(.orange)
                    Text(grammar.nuanceExplanation)
                        .font(.system(size: 12))
                        .foregroundColor(.primary.opacity(0.9))
                }
            }
            .padding(10)
            .background(Color(UIColor.secondarySystemBackground))
            .cornerRadius(10)

            // Example Sentences
            if !grammar.sentences.isEmpty {
                VStack(alignment: .leading, spacing: 6) {
                    ForEach(grammar.sentences) { sent in
                        HStack(alignment: .top, spacing: 8) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(sent.furigana)
                                    .font(.system(size: 10))
                                    .foregroundColor(.secondary)
                                Text(sent.japanese)
                                    .font(.system(size: 13, weight: .bold))
                                    .foregroundColor(.primary)
                                Text(sent.english)
                                    .font(.system(size: 11))
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                            AudioButton(textToSpeak: sent.japanese)
                        }
                        .padding(8)
                        .background(Color.primary.opacity(0.03))
                        .cornerRadius(8)
                    }
                }
            }

            // Exam Drill Trigger Button
            if grammar.quiz != nil {
                Button(action: onOpenQuiz) {
                    HStack {
                        Image(systemName: "checkmark.circle.badge.questionmark")
                            .font(.system(size: 12, weight: .bold))
                        Text("Exam Trap Drill (Past Question)")
                            .font(.system(size: 12, weight: .bold))
                        Spacer()
                        Image(systemName: "chevron.right")
                            .font(.system(size: 10, weight: .bold))
                    }
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Color.purple.opacity(0.1))
                    .foregroundColor(.purple)
                    .cornerRadius(8)
                }
            }
        }
        .padding(14)
        .background(Color(UIColor.systemBackground))
        .cornerRadius(14)
        .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(Color(UIColor.separator).opacity(0.3), lineWidth: 1)
        )
    }

    private func cardLevelColor(_ lvl: String) -> Color {
        levelColor(lvl)
    }

}

fileprivate func levelColor(_ lvl: String) -> Color {
    switch lvl.uppercased() {
    case "N5": return .green
    case "N4": return .cyan
    case "N3": return .blue
    case "N2": return .purple
    case "N1": return .pink
    default: return .blue
    }
}

// MARK: - Grammar Quiz Modal
struct GrammarQuizModalView: View {
    let grammar: JLPTGrammarPoint
    let quiz: GrammarQuiz
    @Binding var selectedOption: Int?
    @Binding var hasSubmitted: Bool
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            VStack(alignment: .leading, spacing: 16) {
                // Header
                HStack {
                    Text(grammar.level + " Exam Trap Drill")
                        .font(.headline)
                        .foregroundColor(.primary)
                    Spacer()
                    Button("Close") {
                        dismiss()
                    }
                    .font(.subheadline.bold())
                }
                .padding(.top, 8)

                // Question Box
                VStack(alignment: .leading, spacing: 8) {
                    Text("Question:")
                        .font(.caption.bold())
                        .foregroundColor(.secondary)

                    Text(quiz.question)
                        .font(.system(size: 18, weight: .bold, design: .rounded))
                        .foregroundColor(.primary)

                    Text(quiz.questionFurigana)
                        .font(.system(size: 13))
                        .foregroundColor(.secondary)
                }
                .padding(14)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(UIColor.secondarySystemBackground))
                .cornerRadius(12)

                // Options
                VStack(spacing: 8) {
                    ForEach(0..<quiz.options.count, id: \.self) { idx in
                        Button(action: {
                            if !hasSubmitted {
                                selectedOption = idx
                            }
                        }) {
                            HStack {
                                Text("\(idx + 1). \(quiz.options[idx])")
                                    .font(.system(size: 15, weight: .semibold))
                                Spacer()
                                if hasSubmitted {
                                    if idx == quiz.correctIndex {
                                        Image(systemName: "checkmark.circle.fill")
                                            .foregroundColor(.green)
                                    } else if selectedOption == idx {
                                        Image(systemName: "xmark.circle.fill")
                                            .foregroundColor(.red)
                                    }
                                } else if selectedOption == idx {
                                    Image(systemName: "circle.fill")
                                        .foregroundColor(.blue)
                                }
                            }
                            .padding(12)
                            .background(optionBackground(idx))
                            .foregroundColor(.primary)
                            .cornerRadius(10)
                        }
                    }
                }

                // Submit / Reveal Answer Button
                if !hasSubmitted {
                    Button(action: {
                        if selectedOption != nil {
                            withAnimation {
                                hasSubmitted = true
                            }
                        }
                    }) {
                        Text("Check Answer")
                            .font(.headline)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                            .background(selectedOption != nil ? Color.blue : Color.gray.opacity(0.3))
                            .foregroundColor(.white)
                            .cornerRadius(12)
                    }
                    .disabled(selectedOption == nil)
                } else {
                    // Explanation Box
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Image(systemName: selectedOption == quiz.correctIndex ? "checkmark.seal.fill" : "exclamationmark.triangle.fill")
                                .foregroundColor(selectedOption == quiz.correctIndex ? .green : .red)
                            Text(selectedOption == quiz.correctIndex ? "Correct! 正解です" : "Incorrect 惜しい！")
                                .font(.headline)
                        }

                        Text(quiz.explanationEn)
                            .font(.system(size: 13, weight: .medium))
                            .foregroundColor(.primary)
                    }
                    .padding(14)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(selectedOption == quiz.correctIndex ? Color.green.opacity(0.1) : Color.red.opacity(0.1))
                    .cornerRadius(12)
                }

                Spacer()
            }
            .padding(16)
        }
    }

    private func optionBackground(_ idx: Int) -> Color {
        if hasSubmitted {
            if idx == quiz.correctIndex {
                return Color.green.opacity(0.15)
            } else if selectedOption == idx {
                return Color.red.opacity(0.15)
            }
        } else if selectedOption == idx {
            return Color.blue.opacity(0.12)
        }
        return Color(UIColor.secondarySystemBackground)
    }
}
