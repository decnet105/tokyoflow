---
name: tokyoflow-video-factory
description: >
  End-to-end automated production pipeline for 'TokyoFlow Japanese' YouTube scenario videos
  and companion iOS App lessons. Standardizes serialized episode numbering (EP. 01, EP. 02...),
  bilingual slide typography (Kanji + Furigana + English Translation + Pro-Tip + Shadowing Drill),
  high-click 16:9 YouTube thumbnails, EdgeTTS voice synthesis, and iOS App Video Academy synchronization.
---

# 🎌 TokyoFlow Japanese • Video Production Factory & Pipeline Standard

This skill defines the mandatory standards, asset guidelines, and automation pipeline for every episode produced under the **TokyoFlow Japanese** brand.

---

## 🎯 Target Audience & Core Principles

1. **Target Audience**: Global English speakers learning Japanese (Beginner N5 to Advanced N1, travel enthusiasts, anime fans, and Tokyo residents).
2. **Language Rule**:
   - Japanese content remains authentic (Kanji, Furigana, pitch accent nuances, native pacing).
   - All explanations, UI labels, subtitles, cultural notes, and YouTube metadata are **100% English**.
3. **Core Formula (The 3-Step Flow)**:
   - **Step 1: Real Audio Immersion** (Authentic Tokyo environment sound / announcement / clerk question).
   - **Step 2: 1-Second Core Response** (Rapid survival phrase with pitch accent & Keigo breakdown).
   - **Step 3: Native Shadowing Drill** (Repetition drill + iOS App companion practice).

---

## 📐 Episode Architecture & Structure (Per-Video Standard)

Every episode MUST contain 4 distinct chapters/slides:

```
[Slide 1: Real-Life Audio Immersion]
   ↓ (9-12s, native train/clerk sound, Japanese kanji + furigana + English meaning)
[Slide 2: Core Safety / Grammar / Etiquette Nuance]
   ↓ (7-10s, deep dive into the underlying cultural or grammar rule)
[Slide 3: High-Frequency Survival Action Phrase]
   ↓ (6-8s, the 1-second golden response learners can immediately use)
[Slide 4: Standardized Outro & Call to Action]
   ↓ (8-10s, Subscribe on YouTube • Download free iOS app on App Store)
[Final Video Total Length: 25s - 45s (Shorts/Long-form Hybrid)]
```

---

## 🎨 Serialized Visual & Slide Design Rules

### 1. Video Slide Canvas (1920x1080 Full HD)
- **Top Brand Ribbon**: Dark navy `#161C2D` with `TokyoFlow Japanese | Real-Life Tokyo Japanese Academy` + `Chapter: XX`.
- **Category Badge**: Soft lavender pill `#EEF2FF` with category name (e.g., `Tokyo Transit • Yamanote Line`).
- **Main Japanese Box**: Pure white card with `#E2E8F0` border:
  - Furigana (Top, `#64748B`, 30pt).
  - Kanji Japanese Main Text (`#0F172A`, 50pt bold).
  - English Meaning (`#1E293B`, 34pt, prefix: `Meaning: `).
  - Pro-Tip (`#10B981` Green, 26pt, prefix: `💡 Pro-Tip: `).
- **Bottom Drill Box**: `#F1F5F9` bar with `🗣️ Shadowing Drill: Repeat aloud with native timing and pitch accent`.
- **Outro Card**:
  - Red Hero Header: `Subscribe to TokyoFlow Japanese on YouTube`.
  - Blue App CTA Box: `📱 Download 'TokyoFlow' Free on the iOS App Store`.

### 2. High-Click YouTube Thumbnail Standard (16:9, 1920x1080)
- **Top-Left**: White pill with crimson border `TokyoFlow 🇯🇵`.
- **Top-Center Hook**: 2-3 high-impact uppercase English words in Bright Yellow `#FEF08A` with heavy black stroke (e.g. `TOKYO METRO HACK`, `KOMBINI SURVIVAL`, `IZAKAYA SURVIVAL`).
- **Top-Right Badge**: Serialized Episode Number in bold white (e.g., `EP. 01`, `EP. 02`, `EP. 03`).
- **Center-Bottom**: 4-6 character soul Japanese phrase in huge white font (e.g., `まもなく参ります`, `温めますか？`, `とりあえず生！`).
- **Bottom-Center Pill**: Dark slate pill `#1E293B` with amber border `🇯🇵 Native Audio • [Skill Tag]`.

---

## 🎙️ Audio Narration & TTS Standards

- **Engine**: Microsoft EdgeTTS (`edge_tts`).
- **Voice Actor**: `ja-JP-NanamiNeural` (Tokyo Standard Pitch & Accent).
- **Default Narration Pace**: `rate="-6%"` (Slightly relaxed for crisp learner comprehension).
- **Default Pitch**: `pitch="+3Hz"` (Friendly, cheerful educational tone).
- **Sync Rule**: Audio duration is dynamically probed via `ffprobe`, and slide video segments are rendered to `duration + 0.5s` for natural breathing room between slides.

---

## 📱 iOS App & YouTube Long-Term Synchronization

Every YouTube video must have a 1:1 corresponding entry in the iOS App's [`TokyoScenarioVideoLesson.swift`](file:///Users/kilvonwu/Documents/UseCaseDrivenJapanese/TokyoFlow/Models/TokyoScenarioVideoLesson.swift):
1. `episodeNumber`: Sequential integer matching `EP. XX`.
2. `title`: `EP. XX • [English Scenario Title]`.
3. `scenarioId`: Link to corresponding interactive simulation scenario in `TokyoFlow`.
4. `chapters`: Matching timestamps (`00:00`, `02:30`, etc.).
5. `keyTakeaways`: Interactive audio flashcard phrases.

---

## 🚀 Execution Pipeline

To produce a new episode, execute:
```bash
# 1. Run the video generation engine
python3 scripts/videogen/pipeline.py --episode 4

# 2. Verify generated assets
# Video: output/videos/tokyoflow_v04_xxx.mp4
# Cover: docs/youtube_assets/thumbnails/ep04_xxx_thumb.jpg

# 3. Test & deploy iOS App updates
xcodebuild test -project TokyoFlow.xcodeproj -scheme TokyoFlow -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```
