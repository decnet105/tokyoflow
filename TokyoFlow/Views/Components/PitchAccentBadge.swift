import SwiftUI

public enum PitchAccentType: String, Codable, CaseIterable {
    case heiban = "0 (Flat / Heiban)"
    case atamadaka = "1 (Head-High / Atamadaka)"
    case nakadaka = "2 (Mid-High / Nakadaka)"
    case odaka = "3 (Tail-High / Odaka)"

    public var code: String {
        switch self {
        case .heiban: return "⓪"
        case .atamadaka: return "①"
        case .nakadaka: return "②"
        case .odaka: return "③"
        }
    }

    public var label: String {
        switch self {
        case .heiban: return "Flat"
        case .atamadaka: return "Head-High"
        case .nakadaka: return "Mid-Peak"
        case .odaka: return "Tail-High"
        }
    }

    public var pitchShapeDescription: String {
        switch self {
        case .heiban: return "Low -> High (Flat across particles)"
        case .atamadaka: return "HIGH on 1st mora -> Drops on 2nd"
        case .nakadaka: return "Low -> HIGH in middle -> Drops"
        case .odaka: return "Low -> High -> Drops on following particle"
        }
    }

    public var badgeColor: Color {
        switch self {
        case .heiban: return .blue
        case .atamadaka: return .red
        case .nakadaka: return .orange
        case .odaka: return .purple
        }
    }
}

public struct PitchAccentBadge: View {
    public let type: PitchAccentType

    public init(type: PitchAccentType) {
        self.type = type
    }

    public var body: some View {
        HStack(spacing: 3) {
            Text(type.code)
                .font(.system(size: 11, weight: .heavy, design: .rounded))
            Text(type.label)
                .font(.system(size: 10, weight: .semibold))
        }
        .padding(.horizontal, 6)
        .padding(.vertical, 2)
        .background(type.badgeColor.opacity(0.12))
        .foregroundColor(type.badgeColor)
        .cornerRadius(6)
    }
}
