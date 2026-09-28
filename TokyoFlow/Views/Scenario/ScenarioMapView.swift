import SwiftUI

public struct ScenarioMapView: View {
    @ObservedObject var dataManager = DataManager.shared
    @EnvironmentObject var userProfile: UserProfile
    @State private var selectedCategory: String = "all"
    @State private var selectedQuarter: Int = 1
    @State private var showSearchSheet = false
    @State private var showAmbiencePicker = false
    @ObservedObject private var audioService = AudioService.shared

    private let categories = [
        ("all", "All Places", "map.fill"),
        ("transit", "Transit", "tram.fill"),
        ("kombini", "Kombini", "cart.fill"),
        ("dining", "Dining", "fork.knife"),
        ("services", "Services", "bicycle"),
        ("shopping", "Shopping", "bag.fill"),
        ("living_services", "Living Log", "shippingbox.fill")
    ]

    private var filteredScenarios: [Scenario] {
        dataManager.scenarios.filter { scenario in
            let matchesCategory = selectedCategory == "all" || scenario.category == selectedCategory
            let matchesQuarter = scenario.quarter == selectedQuarter
            return matchesCategory && matchesQuarter
        }
    }

    public var body: some View {
        NavigationStack {
            ZStack {
                MangaThemeBackgroundView()

                ScrollView {
                VStack(spacing: 20) {
                    // Header Banner: Tokyo Use-Case Journey
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                Text("TOKYO LIVING TIMELINE")
                                    .font(.system(size: 11, weight: .bold))
                                    .foregroundColor(.accentColor)
                                    .tracking(1.5)
                                Text("A Day in Tokyo")
                                    .font(.system(size: 26, weight: .bold, design: .rounded))
                            }
                            Spacer()
                            HStack(spacing: 4) {
                                Image(systemName: "flame.fill")
                                    .foregroundColor(.orange)
                                Text("\(userProfile.streakCount) Days")
                                    .font(.system(size: 14, weight: .bold))
                            }
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Color.orange.opacity(0.12))
                            .cornerRadius(20)
                        }

                        Text("Master practical Japanese by living real Tokyo scenarios: train commuting, combini checkouts, noodle bar ticket machines, and apartment logistics.")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    .padding(.horizontal)
                    .padding(.top, 8)

                    // Quarter Switcher
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 10) {
                            ForEach(1...4, id: \.self) { q in
                                Button(action: { selectedQuarter = q }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: q == 1 ? "tram.fill" : (q == 2 ? "bag.fill" : (q == 3 ? "building.2.fill" : "sparkles")))
                                        Text("Q\(q): \(quarterTitle(q))")
                                            .font(.system(size: 13, weight: .semibold))
                                    }
                                    .padding(.horizontal, 14)
                                    .padding(.vertical, 8)
                                    .background(selectedQuarter == q ? Color.primary : Color(.systemGray6))
                                    .foregroundColor(selectedQuarter == q ? Color(.systemBackground) : .primary)
                                    .cornerRadius(20)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Category Pill Filter
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(categories, id: \.0) { cat in
                                Button(action: { selectedCategory = cat.0 }) {
                                    HStack(spacing: 6) {
                                        Image(systemName: cat.2)
                                            .font(.system(size: 12))
                                        Text(cat.1)
                                            .font(.system(size: 13, weight: .medium))
                                    }
                                    .padding(.horizontal, 12)
                                    .padding(.vertical, 6)
                                    .background(selectedCategory == cat.0 ? Color.accentColor.opacity(0.15) : Color(.systemGray6))
                                    .foregroundColor(selectedCategory == cat.0 ? .accentColor : .secondary)
                                    .cornerRadius(16)
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Scenario Cards List
                    LazyVStack(spacing: 14) {
                        if filteredScenarios.isEmpty {
                            VStack(spacing: 12) {
                                Image(systemName: "mappin.and.ellipse")
                                    .font(.system(size: 40))
                                    .foregroundColor(.secondary)
                                Text("No scenarios found in this quarter filter.")
                                    .foregroundColor(.secondary)
                            }
                            .padding(.vertical, 40)
                        } else {
                            ForEach(filteredScenarios) { scenario in
                                NavigationLink(destination: ScenarioDetailView(scenario: scenario)) {
                                    ScenarioCard(scenario: scenario, isCompleted: userProfile.completedScenarioIds.contains(scenario.id))
                                }
                                .buttonStyle(.plain)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
        .navigationTitle("Tokyo Scenarios")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button(action: { showAmbiencePicker = true }) {
                        HStack(spacing: 4) {
                            Image(systemName: audioService.currentAmbience.icon)
                            if audioService.currentAmbience != .none {
                                Text("Ambience ON")
                                    .font(.system(size: 11, weight: .bold))
                            }
                        }
                        .foregroundColor(audioService.currentAmbience != .none ? .green : .secondary)
                    }
                }

                ToolbarItem(placement: .topBarTrailing) {
                    Button(action: { showSearchSheet = true }) {
                        Image(systemName: "magnifyingglass.circle.fill")
                            .font(.system(size: 20))
                            .foregroundColor(.accentColor)
                    }
                }
            }
            .sheet(isPresented: $showSearchSheet) {
                TokyoSearchSheet()
            }
            .confirmationDialog("Tokyo Ambient Soundscape", isPresented: $showAmbiencePicker, titleVisibility: .visible) {
                ForEach(TokyoAmbienceType.allCases) { amb in
                    Button(amb.rawValue) {
                        audioService.setAmbience(amb)
                    }
                }
                Button("Cancel", role: .cancel) {}
            } message: {
                Text("Select a background ambient soundscape to practice listening in real-world Tokyo audio environments.")
            }
        }
    }

    private func quarterTitle(_ q: Int) -> String {
        switch q {
        case 1: return "Survival"
        case 2: return "Neighborhoods"
        case 3: return "City Logistics"
        case 4: return "Fluency"
        default: return ""
        }
    }
}

public struct ScenarioCard: View {
    public let scenario: Scenario
    public let isCompleted: Bool

    public var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top) {
                ZStack {
                    RoundedRectangle(cornerRadius: 12)
                        .fill(Color.accentColor.opacity(0.12))
                        .frame(width: 44, height: 44)
                    Image(systemName: scenario.categoryIcon)
                        .font(.system(size: 20))
                        .foregroundColor(.accentColor)
                }

                VStack(alignment: .leading, spacing: 4) {
                    HStack {
                        Text(scenario.district)
                            .font(.caption)
                            .fontWeight(.bold)
                            .foregroundColor(.accentColor)
                        Text("• \(scenario.timeOfDay)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Spacer()
                        Text(scenario.jfCanDoLevel)
                            .font(.system(size: 10, weight: .bold))
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.green.opacity(0.15))
                            .foregroundColor(.green)
                            .cornerRadius(6)
                    }

                    Text(scenario.title)
                        .font(.headline)
                        .foregroundColor(.primary)

                    Text(scenario.titleJa)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }

            Text(scenario.context)
                .font(.footnote)
                .foregroundColor(.secondary)
                .lineLimit(2)

            HStack {
                HStack(spacing: 4) {
                    Image(systemName: "bubble.left.and.bubble.right.fill")
                        .font(.caption2)
                    Text("\(scenario.dialogue.count) dialogue lines")
                        .font(.caption)
                }
                .foregroundColor(.secondary)

                Spacer()

                if isCompleted {
                    HStack(spacing: 4) {
                        Image(systemName: "checkmark.seal.fill")
                            .foregroundColor(.green)
                        Text("Completed")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(.green)
                    }
                } else {
                    HStack(spacing: 4) {
                        Text("Start Scenario")
                            .font(.caption)
                            .fontWeight(.semibold)
                        Image(systemName: "chevron.right")
                            .font(.caption2)
                    }
                    .foregroundColor(.accentColor)
                }
            }
        }
        .padding(16)
        .background(Color(.secondarySystemGroupedBackground))
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.04), radius: 8, x: 0, y: 2)
    }
}
