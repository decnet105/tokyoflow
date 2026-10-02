---
name: tokyoflow-video-factory
description: >
  End-to-end automated production pipeline for 'TokyoFlow Japanese' YouTube micro-lesson videos,
  serialized thumbnails, and launch metadata. Standardizes 3-Tier Ruby typography, millisecond-level
  karaoke follow-along highlighting, bilingual teamwork breakdown micro-lessons (Nanami JA + Andrew EN),
  unclipped natural outro CTA, automatic high-CTR thumbnail generation via tokyoflow-thumbnail-factory,
  strict YouTube title formatting (EP.XX prefix), emoji-free and URL-free description boxes, and unified release directory packaging (En-标题-版本).
---

# TokyoFlow Japanese: Video Production Factory Pipeline Standard

This document defines the mandatory end-to-end production workflow, visual contracts, typography rules, audio architecture, thumbnail standard, YouTube Studio title/description rules, and packaging specifications for every video produced under the TokyoFlow Japanese brand. Every future episode must strictly follow this skill pipeline.

---

## 1. Target Audience and Pedagogical Formula

1. Target Audience: Global English speakers learning practical Japanese (N5 Beginner to N1 Advanced, travelers, anime fans, and Tokyo expats/commuters).
2. Audience Difficulty Distribution (70% N5 Mandatory):
   - 70% JLPT N5 (Beginner / Zero-barrier / Primary Focus): Core everyday words, basic polite verb forms, zero prerequisite.
   - 20% JLPT N4-N3 (Intermediate): Practical news, workplace/social nuance, netizen slang.
   - 10% JLPT N2-N1 (Advanced): Official public relations, legal/editorial nuances.
3. Mandatory JLPT Level Badge and Prefix:
   - Long-form video titles MUST strictly start with: `[JLPT N5] EP.XX <High-CTR English Title> | Real Japanese Breakdown`.
   - Shorts video titles MUST strictly start with: `[JLPT N5] SH.XX <High-Impact English Hook>! #Shorts #LearnJapanese`.
   - Video slides MUST render a prominent JLPT difficulty badge (e.g. `[ JLPT N5 ] Essential Foundation`).
4. Language and Speaker Contract:
   - Japanese Voice: `ja-JP-NanamiNeural` (`rate="-6%"`, `pitch="+3Hz"`), pristine Tokyo native cadence for dialogues, vocabulary cards, and grammar spotlight examples.
   - English Voice: `en-US-AndrewNeural` (`rate="+2%"`), natural American male voice for grammatical breakdowns, parts of speech, and cultural nuances. English speaker speaks only English, never mispronounces Japanese words.
5. Authentic Japanese Cultural Insight Mandate:
   - In every long-form video (and metadata), when the topic relates to a genuine Japanese cultural phenomenon (e.g. sauna boom / 'Totono'u' ととのう, anime production collaboration, izakaya otoshi customs, train melody history, kombini seasonal shifts, etiquette), Andrew must provide a concise, engaging cultural insight in English during the breakdown section.
   - Strict Authenticity Rule: Only share genuine, verifiable Japanese cultural facts. Never fabricate or hallucinate cultural trivia. If there is no specific cultural lore, gracefully focus on practical daily conversational nuances.
6. Strict Typography Safety:
   - Dynamic multi-line wrapping with minimum 80px side margins. NEVER truncate or clip text horizontally. All glyphs must render with clean typography without placeholder boxes.

---

## 2. Standard 6-Step Episode Architecture

Every TokyoFlow YouTube episode follows a structured 6-step chapter sequence:

```
[Chapter 1: Real-Life Dialogue Immersion & Follow-Along]
   -> (4-6s, 3-Tier Ruby typography with 80ms Anticipatory Millisecond Karaoke Highlighting)
[Chapter 2: Sentence 1 Bilingual Teamwork Breakdown Micro-Lesson]
   -> (30-38s, Nanami reads JA tokens & examples + Andrew explains grammar & nuances in English)
[Chapter 3: Situational Response / Platform Drill Follow-Along]
   -> (4-6s, 3-Tier Ruby typography with 80ms Anticipatory Millisecond Karaoke Highlighting)
[Chapter 4: Sentence 2 Bilingual Teamwork Breakdown Micro-Lesson]
   -> (30-38s, Nanami reads JA tokens & examples + Andrew explains grammar & nuances in English)
[Chapter 5: High-Frequency Practical Drill Follow-Along]
   -> (4-6s, Rapid situational phrase + karaoke follow-along prompt)
[Chapter 6: Rapid Action Outro & Call to Action]
   -> (Strict 3.4-3.5s, Unclipped audio, TokyoFlow - Japanese Speaking, Real Scenarios, 10,000+ JLPT Vocab)
[Final Total Video Length: ~75s - 95s (High Retention & High Educational Value)]
```

---

## 3. Visual Design and Typography Specifications

Canvas resolution: `1920x1080 Full HD`, `30.0 fps`, `yuv420p`.

### 1. 3-Tier Ruby Typography (Follow-Along Slides)
- Tier 1 (Top Row): Kana / Furigana (`#64748B`, 26pt Hiragana, precisely centered over Kanji).
- Tier 2 (Middle Row): Japanese Main Text (`#0F172A`, 52pt Bold Hiragino Sans).
- Tier 3 (Lower Row): Romaji (`#475569`, 28pt Spaced Hepburn Romanization directly below Japanese).
- Tier 4 (Bottom Row): English Meaning (`#1E293B`, 32pt, prefix: `Meaning: `).
- Pro-Tip Banner: (`#10B981` Emerald, 25pt, prefix: `[ PRO-TIP ] `).
- Bottom Drill Bar: (`#F1F5F9` background, `Shadowing Drill: Repeat aloud with native timing and pitch accent`).

### 2. Millisecond Karaoke Highlighting
- Whisper-based word-level alignment with an 80ms anticipatory lead offset:
  - Active Capsule: Golden-yellow pill background (`#FEF08A` with `#F59E0B` border, radius: `16px`).
  - Follower Dot: Vibrant red indicator dot (`#DC2626`) positioned above the active Kana.
  - Active Text Weight: Ruby Kana, Kanji, and Romaji for active token switch to bold amber (`#B45309`).
  - Non-active tokens remain crisp slate gray for seamless eye-tracking.

### 3. Bilingual Teamwork Breakdown Slide Standard
- Top Header: Pixel-locked category pill (`[ BREAKDOWN ]`), Title (`EP. XX - <Title>`), and Japanese sentence banner.
- Top Half (Vocabulary Grid):
  - 4 to 5 cards displaying: Part of Speech tag (`[Adjective]`, `[Noun]`, `[Verb Stem]`), Kanji, Kana / Romaji, and English definition.
  - Dynamically highlights in warm gold with a red indicator dot when Nanami and Andrew discuss that word.
- Bottom Half (Grammar and Nuance Spotlight Box):
  - Dedicated card detailing grammatical formula, rule breakdown, and cultural etiquette.
  - Highlights with blue outline (`#4F46E5`) when the team reaches the grammar explanation and example sentence.
- Footer: `[ TOKYOFLOW ACADEMY ] Practice interactive word drills and pitch accent scoring in the TokyoFlow iOS App!`.

### 4. Outro Card Standard
- App Name: `TokyoFlow - Japanese Speaking`
- Feature Bullets:
  - `Real Tokyo Life Scenarios (Transit, Kombini, Izakaya, Akiba...)`
  - `14,000+ Native VoiceBank Audio & Pitch Accent Intonation Guides`
  - `10,000+ JLPT N5-N1 Vocabulary & Interactive Drills`
- Duration: 3.4 to 3.5s (Audio plays completely to the end with a 0.35s natural visual padding, zero audio clipping).

---

## 4. Automated Thumbnail Generation (Dedicated Skill Standard)

Every video build strictly adheres to the `tokyoflow-thumbnail-factory` master visual standard, saving the 16:9 master cover directly as `thumbnail.jpg`:
1. Resolution and Canvas: `1920x1080 Full HD / 4K UHD`.
2. Atmosphere and Scene: Lived-in Tokyo backdrop with authentic ambiance.
3. Top-Left Brand Capsule: Crimson-red pill with crisp white text: `TokyoFlow Japanese`.
4. Left 3-Tier 3D Hook Stack: Uppercase typography (Lines 1 & 2 in Solar Yellow `#FACC15`, Line 3 in Metallic White `#FFFFFF`) with heavy black 3D extrusion (`ANIME` / `SAUNA` / `HACK`).
5. Bottom-Left Japanese Key Phrase: Bold pure white Japanese calligraphy kanji/kana with pink/magenta glowing aura (`#EC4899`) and deep black drop stroke.
6. Bottom-Right 3D Episode Badge: Metallic badge `EP.XX` with yellow/gold number.
7. Bottom-Right Value Tag Pill: Rounded dark slate pill with white outline: `[JLPT N5] Native Audio - Pop Culture Trend`.

---

## 5. YouTube Studio Metadata Guidelines (Mandatory Format Rules)

Every generated `metadata.md` must strictly follow these platform standards:

### 1. Title Standard: Mandatory `[JLPT Level]` and `EP.XX` Prefix
- Format: `[JLPT N5] EP.XX <High-CTR English Title> | Real Japanese Breakdown`
- Example: `[JLPT N5] EP.09 Anime Company Made a Real Sauna in Tokyo! | Real Japanese Breakdown`
- Rule: JLPT level and Episode number MUST be at the very start (`[JLPT N5] EP.XX`) for immediate recognition across playlists, search feeds, and mobile cards.

### 2. Description Box: NO URLs & NO Emojis (Clean Text Contract)
- Zero URLs Policy: Do NOT include any HTTP/HTTPS web links or App Store URLs in the description text.
- Zero Emojis Policy: Do NOT use graphical emojis in headers or body text (use clean uppercase bracketed or plain text labels).
- Required Sections:
  - Episode Overview and Location
  - `TIMESTAMPS AND CHAPTERS:` with clickable `00:00` format calculated from rendered video segments
  - `KEY PHRASES COVERED:` with Romaji and English translations
  - `GRAMMAR AND NUANCE SPOTLIGHTS:` with core formula breakdowns
  - `RECOMMENDED PRACTICE:` referencing the companion iOS app by exact name (`TokyoFlow - Japanese Speaking`)
  - Standard hashtags (`#TokyoFlow #LearnJapanese #JapaneseSpeaking #TokyoTravel #JLPT #JapaneseShadowing`)

### 3. Dual-Playlist Architecture (Mandatory on Upload)
Every video upload is mapped to two distinct playlists on YouTube:
1. Scenario/Topic Playlist (Transit, Kombini, Dining, Pop Culture/Anime, News).
2. JLPT Level Playlist (`JLPT N5`, `JLPT N4`, `JLPT N3`, `JLPT N2-N1`).

---

## 6. Unified Release Directory Architecture (`En-标题-版本`)

All release assets for every episode are packaged into a single standardized folder under `docs/youtube_releases/` following the strict naming rule `E{XX}-{Title_Slug}-v{Version}`:

```
docs/youtube_releases/E09-anime_sauna_trend-v1.0/
├── video.mp4            # 1080p Full HD Video (30fps, 44.1kHz AAC Stereo, ~80-95s)
├── thumbnail.jpg        # 1920x1080 High-CTR Serialized YouTube Cover ([JLPT N5] EP.XX)
├── metadata.md          # YouTube Studio Launch Kit (Title, Clean Description, Chapters, Tags, Pinned Comment)
├── short.mp4            # 9:16 Vertical Short (30fps, 4-Stage Interactive Shadowing)
├── short_thumbnail.jpg  # 9:16 Minimalist Vertical Cover
├── short_metadata.md    # YouTube Shorts Launch Kit ([JLPT N5] SH.XX)
└── youtube_schedule_kit.json # Automated YouTube publishing & scheduling payload
```

---

## 7. Execution Commands

```bash
# 1. Generate autonomous daily hot-topic release package (Long + Short + Covers + Schedule)
python3 scripts/trend_radar/daily_trend_producer.py --date YYYY-MM-DD

# 2. Upload and schedule YouTube publishing into Dual Playlists (Scenario + JLPT)
python3 scripts/videogen/youtube_publisher.py

# 3. Batch generate 16:9 and 9:16 thumbnails across all episodes
python3 scripts/videogen/generate_thumbnails.py
```
