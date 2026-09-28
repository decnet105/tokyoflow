import SwiftUI

public struct TokyoContextHubCardView: View {
    @ObservedObject var engine = TokyoLearningPackageEngine.shared
    @State private var showPackageRunner: Bool = false
    @State private var selectedTrackTab: Int = 0 // 0: By Scenario, 1: By JLPT Level

    public init() {}

    public var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            // Header
            HStack {
                Label("DUAL-TRACK ADAPTIVE BUNDLE", systemImage: "sparkles")
                    .font(.system(size: 10, weight: .black))
                    .foregroundColor(.accentColor)
                    .tracking(1.0)
                Spacer()
                Text("Ebbinghaus • Native VoiceBank")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundColor(.secondary)
            }

            // Track Switcher: Scenario vs JLPT Level
            Picker("Track", selection: $selectedTrackTab) {
                Text("Real-World Scenes").tag(0)
                Text("JLPT Level Track (N5-N1)").tag(1)
            }
            .pickerStyle(.segmented)
            .onChange(of: selectedTrackTab) { newTab in
                if newTab == 0 {
                    engine.selectedTrack = .scenario(.commute)
                } else {
                    engine.selectedTrack = .jlpt(.n5)
                }
            }

            // Subtitle & Focus Pill
            HStack(alignment: .center) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(selectedTrackTab == 0 ? "Where are you learning now?" : "Target JLPT Proficiency")
                        .font(.system(size: 17, weight: .black, design: .rounded))
                    Text(selectedTrackTab == 0 ? "Curated 5-minute practical immersion bundle." : "Synthesized high-yield JLPT exam mastery package.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }


                Spacer()

                // Focus Toggle (Fluency vs Exam Sprint)
                Button(action: {
                    withAnimation {
                        if engine.selectedFocusMode == .practicalFluency {
                            engine.setFocusMode(.examSprint)
                        } else {
                            engine.setFocusMode(.practicalFluency)
                        }
                    }
                }) {
                    HStack(spacing: 4) {
                        Image(systemName: engine.selectedFocusMode.icon)
                            .font(.system(size: 10))
                        Text(engine.selectedFocusMode == .practicalFluency ? "Fluency" : "Exam")
                            .font(.system(size: 10, weight: .bold))
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 5)
                    .background(engine.selectedFocusMode == .examSprint ? Color.purple.opacity(0.18) : Color.blue.opacity(0.12))
                    .foregroundColor(engine.selectedFocusMode == .examSprint ? .purple : .blue)
                    .cornerRadius(8)
                }
            }

            // Option Pills: Either Scenarios or JLPT Levels
            if selectedTrackTab == 0 {
                // Scenario Pills
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(LearningContextMode.allCases) { mode in
                            let isSelected = engine.selectedContextMode == mode && selectedTrackTab == 0
                            Button(action: {
                                withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
                                    engine.selectedTrack = .scenario(mode)
                                }
                            }) {
                                HStack(spacing: 6) {
                                    Image(systemName: mode.icon)
                                        .font(.caption)
                                    Text(mode.rawValue)
                                        .font(.system(size: 12, weight: .bold))
                                    Text(mode.targetDuration)
                                        .font(.system(size: 10, weight: .semibold, design: .monospaced))
                                        .opacity(0.8)
                                }
                                .foregroundColor(isSelected ? .white : .primary)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(
                                    isSelected
                                        ? Color(hex: mode.badgeColorHex)
                                        : Color.primary.opacity(0.06)
                                )
                                .cornerRadius(12)
                                .shadow(color: isSelected ? Color(hex: mode.badgeColorHex).opacity(0.3) : .clear, radius: 4, y: 2)
                            }
                        }
                    }
                    .padding(.horizontal, 2)
                }
            } else {
                // JLPT Level Pills
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(JLPTLevelTrack.allCases) { lvl in
                            let isSelected: Bool = {
                                if case .jlpt(let currentLvl) = engine.selectedTrack {
                                    return currentLvl == lvl
                                }
                                return false
                            }()

                            Button(action: {
                                withAnimation(.spring(response: 0.35, dampingFraction: 0.75)) {
                                    engine.selectedTrack = .jlpt(lvl)
                                }
                            }) {
                                HStack(spacing: 6) {
                                    Text(lvl.shortLabel)
                                        .font(.system(size: 12, weight: .black))
                                    Text(lvl.rawValue.replacingOccurrences(of: "JLPT ", with: ""))
                                        .font(.system(size: 11, weight: .semibold))
                                }
                                .foregroundColor(isSelected ? .white : .primary)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(
                                    isSelected
                                        ? Color(hex: lvl.badgeColorHex)
                                        : Color.primary.opacity(0.06)
                                )
                                .cornerRadius(12)
                                .shadow(color: isSelected ? Color(hex: lvl.badgeColorHex).opacity(0.3) : .clear, radius: 4, y: 2)
                            }
                        }
                    }
                    .padding(.horizontal, 2)
                }
            }

            // Current Package Summary Card
            if let pkg = engine.currentPackage {
                VStack(spacing: 12) {
                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(packageTitle(for: pkg))
                                .font(.system(size: 12, weight: .semibold))
                                .foregroundColor(.primary)

                            Text("\(pkg.items.count) Multi-Grain Steps • Vocab + Grammar + VoiceBank")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }

                        Spacer()

                        Text("+\(pkg.items.count * 15 + 50) TP")
                            .font(.system(size: 11, weight: .black))
                            .padding(.horizontal, 8)
                            .padding(.vertical, 3)
                            .background(Color.orange.opacity(0.2))
                            .foregroundColor(.orange)
                            .cornerRadius(6)
                    }

                    // Steps Preview Chips
                    HStack(spacing: 6) {
                        ForEach(pkg.items.indices, id: \.self) { idx in
                            let item = pkg.items[idx]
                            HStack(spacing: 4) {
                                Circle()
                                    .fill(item.isCompleted ? Color.green : Color.accentColor.opacity(0.5))
                                    .frame(width: 6, height: 6)
                                Text(item.type.rawValue)
                                    .font(.system(size: 9, weight: .bold))
                                    .lineLimit(1)
                            }
                            .padding(.horizontal, 6)
                            .padding(.vertical, 3)
                            .background(Color.primary.opacity(0.05))
                            .cornerRadius(6)
                        }
                    }

                    // Launch Button
                    Button(action: {
                        showPackageRunner = true
                    }) {
                        HStack(spacing: 8) {
                            Image(systemName: "play.fill")
                                .font(.caption)
                            Text("Launch \(packageButtonLabel(for: pkg)) (~5 min)")
                                .font(.system(size: 13, weight: .black))
                        }
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 11)
                        .background(
                            LinearGradient(
                                colors: [Color(hex: packageColorHex(for: pkg)), Color.accentColor],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .cornerRadius(12)
                        .shadow(color: Color(hex: packageColorHex(for: pkg)).opacity(0.35), radius: 6, y: 2)
                    }
                }
                .padding(12)
                .background(Color.primary.opacity(0.04))
                .cornerRadius(14)
            }
        }
        .padding(16)
        .background(.ultraThinMaterial)
        .cornerRadius(20)
        .overlay(
            RoundedRectangle(cornerRadius: 20)
                .stroke(Color.primary.opacity(0.08), lineWidth: 1)
        )
        .sheet(isPresented: $showPackageRunner) {
            TokyoPackageRunnerView()
        }
    }

    private func packageTitle(for pkg: TokyoLearningPackage) -> String {
        if let lvl = pkg.levelTrack {
            return "\(lvl.shortLabel) Comprehensive Exam & Scenario Sprint"
        }
        return pkg.mode.tagline
    }

    private func packageButtonLabel(for pkg: TokyoLearningPackage) -> String {
        if let lvl = pkg.levelTrack {
            return "\(lvl.shortLabel) Sprint"
        }
        return "\(pkg.mode.rawValue) Bundle"
    }

    private func packageColorHex(for pkg: TokyoLearningPackage) -> String {
        if let lvl = pkg.levelTrack {
            return lvl.badgeColorHex
        }
        return pkg.mode.badgeColorHex
    }
}
