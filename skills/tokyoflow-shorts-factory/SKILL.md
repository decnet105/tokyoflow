---
name: tokyoflow-shorts-factory
description: >
  End-to-end automated production pipeline for 'TokyoFlow Japanese' YouTube Shorts (9:16 vertical 1080x1920).
  Standardizes 4-stage psychological retention framework, millisecond token glow highlighting,
  bilingual role separation (Andrew EN + Nanami JA), minimalist serialized 9:16 covers (short_thumbnail.jpg),
  mandatory [JLPT Level] SH.XX title format, and unified release directory packaging.
---

# TokyoFlow YouTube Shorts Factory (9:16 Vertical Video Skill)

This skill defines the standardized architecture, visual design, audio composition, and metadata rules for creating high-converting YouTube Shorts (9:16 vertical 1080x1920) for the TokyoFlow Japanese channel.

---

## 1. Video Specifications and Audio Architecture

| Parameter | Specification | Purpose |
| :--- | :--- | :--- |
| **Aspect Ratio** | **9:16 Vertical** (`1080x1920`) | Native mobile feed & algorithm optimization |
| **Frame Rate & Codec** | `30.0 fps`, `H.264 (yuv420p)`, `AAC 44.1kHz Stereo` | Universal mobile playback compatibility |
| **Duration Target** | **30s ~ 45s** (Strictly under 50s) | High Average Percentage Viewed (APV > 85%) & retention |
| **Dual-Voice Engine** | **Male Voice (`en-US-AndrewNeural`)** for English hook/pro-tip/poll<br>**Female Voice (`ja-JP-NanamiNeural`)** for native Japanese pronunciation & shadowing | Clear pedagogical role division & cognitive ease |
| **Karaoke Follow-Along** | Millisecond/token-level glowing yellow capsule (`#fef08a`) + amber border (`#f59e0b`) | Multi-sensory word recognition & shadow timing |
| **JLPT Difficulty Badge** | Mandatory On-Screen Pill (e.g., `[ JLPT N5 ] Essential Foundation`) + Title Prefix `[JLPT N5]` | Instant target learner alignment (Strict Quota: 70% JLPT N5, 20% N4-N3, 10% N2-N1) |
| **Typography & Layout Safety** | Strict Multi-Line Wrapping (max width <= 880px, padding >= 60px), ZERO text truncation, ZERO unrenderable placeholder glyphs | Pixel-perfect mobile readability |

---

## 2. 4-Stage Storyboard and Retention Engine

Every vertical Short must execute a tight 4-phase psychological retention loop:

```
+------------------------------------------------------------------------+
|                      TokyoFlow 9:16 Short Architecture                 |
+------------------+--------------+--------------------------------------+
| Time Window      | Audio Cue    | Visual Screen State                  |
+------------------+--------------+--------------------------------------+
| 0.0s - 5.0s      | Andrew (EN)  | Phase 1: High-Contrast Hook Question |
| (The 3s Hook)    | Male Hook    | Top 3D Hook + JLPT Badge [N5-N4]     |
+------------------+--------------+--------------------------------------+
| 5.0s - 20.0s     | Nanami (JP)  | Phase 2: Native Dialogue & Karaoke   |
| (Core Delivery)  | Tokyo Native | 3-Tier Card + Auto-Wrap + Word Glow  |
+------------------+--------------+--------------------------------------+
| 20.0s - 32.0s    | Nanami (JP)  | Phase 3: Slow Repeat Shadowing Drill |
| (Shadowing)      | 0.85x Speed  | SHADOW NOW + Glowing Syllables       |
+------------------+--------------+--------------------------------------+
| 32.0s - 40.0s    | Andrew (EN)  | Phase 4: A/B Poll + Long-Form Funnel |
| (Conversion CTA) | "Comment A/B"| "Watch Full Deep Dive" + Poll CTA    |
+------------------+--------------+--------------------------------------+
```

---

## 3. Vertical Visual Layout Geometry (1080 x 1920)

- Header Safe Zone (`y=60..300`):
  - `y=70`: Brand & Episode Pill `TokyoFlow - [JLPT N5] SH.XX`
  - `y=140..250`: 3D Heavy Hook Title (Yellow `#facc15` & White `#ffffff`, 48pt~54pt)
  - `y=265`: Scenario District Pill `Shinjuku Station` (Indigo `#e0e7ff` bg, `#4338ca` text)
- Central Focus Zone (`y=330..990`):
  - Glassmorphic Main Card (`x=60, w=960, h=640`, Dark slate `#1e293b` with `#334155` border)
  - Kana / Furigana (`y=410`): 28pt Neon Cyan (`#38bdf8`)
  - Japanese Kanji Text (`y=460`): 60pt Bold White (`#ffffff`), with glowing electric yellow highlight for active spoken words
  - Romaji Subtitle (`y=670`): 28pt Bright Yellow (`#fef08a`)
  - English Translation (`y=760`): 34pt Crisp White (`#f8fafc`)
- Pro-Tip and Value Box (`y=1020..1440`):
  - Emerald Formula Card: `[ LOCAL PRO-TIP ]`
  - Nuance explanation / Cultural rule in bold text
- Interactive Shadowing Indicator (`y=1470..1580`):
  - Status Pill: `LISTEN` -> `SHADOW WITH NATIVE PITCH!`
- Bottom Call to Action (`y=1610..1860`):
  - App Showcase Card: `TokyoFlow - Japanese Speaking (iOS)`
  - `Subscribe for Daily Tokyo Japanese!`
  - Bottom Millisecond Progress Line (`y=1900..1910`)

---

## 4. YouTube Shorts Metadata and Cover Contract

1. Title Formula (Mandatory Serialized Prefix `[JLPT Level] SH.XX`):
   - Must strictly start with `[JLPT N5] SH.XX ` (matching long-form `[JLPT N5] EP.XX`)
   - Followed by punchy hook + `#Shorts #LearnJapanese`
   - ZERO Emojis
   - Example: `[JLPT N5] SH.09 Anime Studio Opened a SAUNA in Tokyo?! #Shorts #LearnJapanese`
2. Minimalist High-CTR Cover Architecture (`short_thumbnail.jpg`):
   - Dimensions: 9:16 Vertical (`1080x1920`)
   - Top 3-Pill Header:
     - Left: `TokyoFlow` (Solid White Pill, Bold Crimson `#DC2626` text)
     - Center: `JLPT N5` (Dark Glassmorphic Capsule `#18202F`, Sky Cyan `#38BDF8` border, Solar Yellow `#FACC15` text)
     - Right: `SH.XX` (Scenario Accent Pill, Dark Navy `#0A0E18` text)
   - Location Tag: Upper district indicator (`SHINJUKU STATION - YAMANOTE`, `SHIBUYA 7-ELEVEN - TOKYO`, `TOKYO ANIME STUDIO - SAUNA`)
   - Minimalist 1-2 Words Punchy English Hook: Large 110pt heavy uppercase hook in secondary accent color with 3D drop shadow (`TRAIN HACK`, `7-ELEVEN`, `IZAKAYA`, `ANIME SHOP`, `SUBWAY HACK`, `ICED COFFEE`, `RAMEN CHANT`, `FITTING ROOM`, `ANIME SAUNA`)
   - Central Glassmorphic Hero Card: 4px Scenario Primary Accent border, Authentic Japanese survival phrase + Romaji + English translation + 3-step shadowing pill
   - Bottom Conversion Strip: App Store branding + feature bullets
   - Scenario Color Palettes:
     - SH.01 Yamanote: Emerald `#10B981` & Sky Cyan `#38BDF8`
     - SH.02 7-Eleven: Kombini Orange `#F97316` & Warm Yellow `#FACC15`
     - SH.03 Izakaya: Amber Beer Gold `#EAB308` & Warm Glow `#F97316`
     - SH.04 Akiba Anime: Cyberpunk Purple `#A855F7` & Neon Pink `#EC4899`
     - SH.05 Subway: Metro Cyan `#06B6D4` & Blue Line `#3B82F6`
     - SH.06 Kombini Coffee: Roasted Amber `#D97706` & Crema Gold `#FBBF24`
     - SH.07 Ramen: Fiery Red `#EF4444` & Tonkotsu Gold `#F59E0B`
     - SH.08 Ginza Shopping: Luxury Rose Gold `#EC4899` & Fashion Lavender `#A855F7`
     - SH.09 Anime Sauna Trend: Neon Anime Pink `#EC4899` & Solar Sauna Yellow `#FACC15`
3. Shorts Title Standard: Mandatory `[JLPT Level]` and `SH.XX` Prefix:
   - Format: `[JLPT N5] SH.XX <High-Impact English Hook>! #Shorts #LearnJapanese`
   - Example: `[JLPT N5] SH.09 Anime Studio Made a SAUNA in Tokyo?! #Shorts #LearnJapanese`
   - Rule: JLPT level and Short number MUST be at the very start (`[JLPT N5] SH.XX`) for instant recognition on mobile feeds and search.
4. Description Formula (Zero URLs, Zero Emojis in Body):
   - Clean uppercase structure
   - Japanese sentence transcription + Romaji + English meaning
   - Quick grammar pro-tip note
   - Mention `TokyoFlow - Japanese Speaking`
   - Hashtag stack: `#Shorts #LearnJapanese #JapaneseSpeaking #TokyoFlow #Tokyo #JLPT #JapaneseShadowing`
5. Release Asset Packaging (Single Unified Path: `docs/youtube_releases/`):
   - Saved inside `docs/youtube_releases/E{XX}-{Slug}-v1.0/`:
     - `short.mp4`
     - `short_thumbnail.jpg` (Custom minimalist cover)
     - `short_metadata.md`

---

## 5. Execution Commands

```bash
# 1. Generate autonomous daily hot-topic release package (Linked 9:16 Short + 16:9 Long)
python3 scripts/trend_radar/daily_trend_producer.py --date YYYY-MM-DD

# 2. Upload and schedule YouTube publishing into Dual Playlists (Scenario + JLPT)
python3 scripts/videogen/youtube_publisher.py

# 3. Generate batch scenario shorts catalog (SH. 01 to SH. 08)
python3 scripts/videogen/build_all_shorts.py
```
