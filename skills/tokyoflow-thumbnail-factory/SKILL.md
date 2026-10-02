---
name: tokyoflow-thumbnail-factory
description: >
  Mandatory standardized high-CTR YouTube thumbnail & cover design skill for TokyoFlow Japanese.
  Covers both 16:9 Long-Form / Micro-Lesson 4K Covers (thumbnail.jpg) and 9:16 Vertical Viral Shorts Covers (short_thumbnail.jpg).
  Standardizes the authentic 5-Element visual architecture, color grading palettes, typography hierarchies,
  master prompt engineering, and automated Python PIL rendering pipelines for every released video.
---

# TokyoFlow Japanese: Master Thumbnail and Cover Factory (16:9 and 9:16)
## 0. Golden Master Cover Standard (黄金样本标准: EP.10)

> [!IMPORTANT]
> **Approved Master Landscape Thumbnail**: `docs/youtube_releases/E10-ayase_haruka_tennen-v1.0/thumbnail.jpg`
> **Approved Master Vertical Shorts Cover**: `docs/youtube_releases/E10-ayase_haruka_tennen-v1.0/short_thumbnail.jpg`
> **Reference Format Templates**: `output/日语长片标准格式.jpg` (16:9) and `output/日语短片标准格式.jpg` (9:16)
> All future thumbnails must strictly replicate the color warmth, 3D typography, photorealistic scene base, and precise element placement demonstrated in this reference set.

## The 4 Core Pillars: Production Bible & Director Contract (制作圣经与导演合同)

Thumbnails must directly drive the **4 Core Pillars of Competitive Moat**:
1. ⚡ **Rapid Trend Velocity & High-CTR Clickability**: Dynamic visual translation of same-day trending events with bold uppercase 3D hooks.
2. 🎭 **Viral Entertainment & Warm Relatability**: Authentic lived-in Tokyo scenes with warm lighting, real smiling people, and emotional depth (never cold/flat corporate NHK graphics).
3. 🎯 **Strict JLPT Level Alignment**: Prominent, unmissable `[JLPT N5]` badge on both landscape and vertical covers.
4. 🧠 **Frictionless Reading & Zero Overflow**: Autoscale typography, crisp contrast, pure white Kanji with magenta aura, and 3-pill top header on Shorts.

---

## 1. 16:9 Long-Form Master Thumbnail Standard (`thumbnail.jpg`)

### The Locked-in 6-Element Landscape Architecture (1920x1080 / 4K UHD)

Every 16:9 long-form thumbnail must strictly adhere to the approved master format (warm, relatable, grounded, informative):

```
+----------------------------------------------------------------------------------------+
| [1. Brand Capsule]                                                                     |
|  TokyoFlow Japanese                                                                    |
|                                                                                        |
| [2. 3-Tier Giant 3D Hook Stack]            [3. Warm Grounded Tokyo Living Scene]       |
|  ANIME                                     (Warm ambient cedar/neon lighting, steam,   |
|  SAUNA                                      real smiling people enjoying the scene,    |
|  HACK                                       friendly, relatable, daily-life warmth)    |
|                                                                                        |
| [4. Giant Glowing Japanese Soul Phrase]     [5. 3D Metallic Episode Badge]             |
|  サウナを作った！                             EP.09 (or EP.XX)                           |
|                                                                                        |
|                                            [6. Bottom Scenario Value Tag Pill]         |
|                                             [JLPT N5] Native Audio - Pop Culture Trend |
+----------------------------------------------------------------------------------------+
```

### Layer-by-Layer Specifications (16:9)

| Layer # | Element | Dimensions / Typography | Color & Effect |
| :--- | :--- | :--- | :--- |
| **1. Atmosphere & Scene** | Warm, Grounded Tokyo Living Scene | 1920x1080 (4K UHD) | Real people in authentic daily scenarios (sauna, cafe, train, izakaya, shop, press conference), warm amber/neon lighting, high friendliness and cultural relatability; natural dark left vignette for text contrast. **STRICT MANDATE**: Never use cartoon illustrations like `akiba_neon.jpg`. If no local photo exists, fetch authentic news photo from YT/web or synthesize 4K photorealistic scene. |
| **2. Brand Capsule** | `TokyoFlow Japanese` | `x=50, y=40, h=72`, Bold 38pt | Crimson red pill with white text, crisp white outer stroke |
| **3. 3-Tier 3D Hook Stack** | 3-Line High-CTR Uppercase Hook (e.g. `ANIME`, `SAUNA`, `HACK`) | Left-aligned `x=50, y=140..580`, **120pt Ultra Heavy** | Lines 1 & 2: Solar Yellow (`#FACC15` / `#FEF08A`) with 3D black extrusion; Line 3: Metallic White (`#FFFFFF`) with 3D drop stroke |
| **4. Japanese Soul Phrase** | Core Scene Phrase (e.g. `サウナを作った！`, `まもなく参ります`) | Bottom-left `y=height-220`, **110pt Bold Japanese** | Pure White `#FFFFFF` + Neon Pink/Magenta glowing outer aura (`#EC4899`) + deep black drop stroke |
| **5. 3D Episode Badge** | `EP.XX` (e.g. `EP.09`) | Bottom-right / Inline with phrase, **110pt 3D Heavy** | `EP.` in Metallic White + Number `XX` in 3D Solar Yellow with deep 360-degree black stroke |
| **6. Scenario Value Pill** | `[JLPT N5] Native Audio - Topic` | Bottom-right `y=height-80, h=60`, 28pt Rounded | Dark slate `#18202F` pill, Crisp white border, White & Yellow `#FACC15` text (Instant difficulty & topic recognition) |

### High-Definition Artist / News Photo as Cover Base Rule (艺人高清大图作为封面底图法则)
Whenever a real event, celebrity, or pop culture entity is the subject of the episode and an authentic high-definition 4K photo is acquired (e.g. Ayase Haruka press conference, Tokyo anime event, Shibuya landmark), this photo MUST serve directly as `bg_image_path`.
The rendering pipeline automatically:
1. Positions the photorealistic subject on the right 60% of the canvas with clear emotional expression.
2. Applies a subtle cinematic dark vignette on the left 40% for ultra-high text readability.
3. Overlays the 3-line 3D Solar Yellow hook stack, glowing pure white Japanese phrase, metallic `EP.XX` badge, and `[JLPT N5]` value pill.

---

## 2. 9:16 Shorts Vertical Cover Standard (`short_thumbnail.jpg`)

### The Locked-in 5-Element Vertical Architecture (1080x1920)

Every vertical Short thumbnail must strictly feature these 5 elements optimized for mobile feeds:

```
+--------------------------------------------------------+
| [1. Brand Pill]      [2. JLPT Badge]    [3. SH Code]   |
|  TokyoFlow             JLPT N5             SH.01       |
|                                                        |
|  SHINJUKU STATION - YAMANOTE (Location Tag)            |
|                                                        |
| [4. Giant 3D Uppercase Action Hook Title (110pt)]      |
|  TRAIN HACK                                            |
|  STATION ANNOUNCEMENTS                                 |
|  --------------------------------                      |
|                                                        |
| +----------------------------------------------------+ |
| | [5. Central Glassmorphic Hero Card (Theme Border)] | |
| |  TOKYO SURVIVAL PHRASE                             | |
| |  点字ブロックの内側へ                              | |
| |  Tenji burokku no uchigawa e                       | |
| |  ------------------------------------------------  | |
| |  ENGLISH MEANING:                                  | |
| |  "Behind The Yellow Line"                          | |
| |  +----------------------------------------------+ | |
| |  | 3-STEP INTERACTIVE SHADOWING                 | | |
| |  | Listen - Break Down - Speak With AI Pitch    | | |
| |  +----------------------------------------------+ | |
| +----------------------------------------------------+ |
|                                                        |
| +----------------------------------------------------+ |
| | [6. Bottom Conversion & App Store Strip]           | |
| |  TOKYOFLOW - JAPANESE SPEAKING                     | |
| |  Real Scenarios - 10,000+ Native Words & Audio     | |
| |  Available on the App Store                        | |
| +----------------------------------------------------+ |
+--------------------------------------------------------+
```

### Layer-by-Layer Specifications (9:16)

| Layer # | Element | Dimensions / Typography | Color & Effect |
| :--- | :--- | :--- | :--- |
| **1. Brand Pill** | Top-Left Brand Capsule | `x=70, y=90, h=64`, Auto-sized (`text_w + 52`) | Solid Pure White `#FFFFFF` pill, Bold Crimson `#DC2626` text (Ultra-high contrast, zero overflow) |
| **2. JLPT Level Badge** | Top-Center Level Capsule | `x=pill_bx+18, y=90, h=64`, Auto-sized | Dark Glassmorphic `#18202F`, Sky Cyan `#38BDF8` border, Solar Yellow `#FACC15` text |
| **3. Episode Code Badge** | Top-Right SH Pill | `x=W-70-pill_w, y=90, h=64`, Auto-sized | Scenario Primary Accent Color (e.g. Emerald, Orange, Pink), Dark Navy `#0A0E18` text |
| **4. Location Tag** | Scenario District Line | `x=75, y=185`, 30pt Heavy | Slate Gray `#94A3B8` uppercase location pill |
| **5. 3D Action Hook** | 1-2 Words Giant Hook | `y=270, 110pt Heavy Uppercase` | Scenario Secondary Accent (e.g. Sky Cyan, Warm Yellow, Solar Yellow) + 3D drop shadow |
| **6. Hero Dialogue Card** | Central 3-Tier Japanese Card | `x=70, y=530, w=940, h=920`, Dark Slate `#0F172A` | 4px Scenario Accent border, Pure White Kanji (**86pt auto-scaled down to 44pt to strictly prevent overflow**) + Bright Yellow Romaji + **Dynamic Multi-line English Meaning (strictly zero truncation)** |
| **7. 3-Step Shadowing Pill** | Interactive Status Box | `x=110, y=1210, w=860, h=160`, `#1E293B` | Scenario Accent header `3-STEP INTERACTIVE SHADOWING` + White guide text |
| **8. Bottom App Strip** | Conversion Banner | `x=70, y=1540, w=940, h=260`, Dark Navy `#020617` | Pure White App Title + Slate bullets + Secondary Accent `Available on the App Store` |

---

## 3. Scenario Accent Color Themes (Episode-by-Episode Palette)

Every episode uses a distinct scenario-tailored color palette:

| Episode / Theme | Primary Accent (Border & Badges) | Secondary Accent (Hook & Glow) | Scenario Location Tag |
| :--- | :--- | :--- | :--- |
| **SH.01 Yamanote Transit** | Emerald Green (`#10B981`) | Sky Cyan (`#38BDF8`) | `SHINJUKU STATION • YAMANOTE` |
| **SH.02 7-Eleven Kombini** | Kombini Orange (`#F97316`) | Warm Yellow (`#FACC15`) | `SHIBUYA 7-ELEVEN • TOKYO` |
| **SH.03 Izakaya Night** | Amber Beer Gold (`#EAB308`) | Warm Glow (`#F97316`) | `SHINBASHI IZAKAYA ALLEY` |
| **SH.04 Akiba Anime Shop** | Cyberpunk Purple (`#A855F7`) | Neon Pink (`#EC4899`) | `AKIHABARA ELECTRIC TOWN` |
| **SH.05 Tokyo Metro Subway** | Metro Cyan (`#06B6D4`) | Blue Line (`#3B82F6`) | `TOKYO METRO • MARUNOUCHI` |
| **SH.06 Kombini Coffee & ATM** | Roasted Amber (`#D97706`) | Crema Gold (`#FBBF24`) | `ROPPONGI LAWSON • TOKYO` |
| **SH.07 Ramen Ticket Machine** | Fiery Ramen Red (`#EF4444`) | Tonkotsu Gold (`#F59E0B`) | `IKEBUKURO RAMEN ALLEY` |
| **SH.08 Ginza Tax-Free Shopping**| Luxury Rose Gold (`#EC4899`) | Fashion Lavender (`#A855F7`)| `GINZA SHOPPING BOULEVARD` |
| **SH.09 Anime Studio Sauna Trend**| Neon Anime Pink (`#EC4899`) | Solar Sauna Yellow (`#FACC15`)| `TOKYO ANIME STUDIO • SAUNA` |
| **SH.10 Ayase Haruka Charm (Master)**| Neon Pink (`#EC4899`) | Solar Yellow (`#FACC15`)| `TOKYO POP CULTURE • JLPT` (4K Photo Base) |

---

## 4. Incremental Execution and Numbering Rules

1. Incremental Generation by Default:
   - The thumbnail factory script MUST run in single-target mode by default (`--episode <EP_NUM>` or `--dir <DIR_PATH>`).
   - DO NOT regenerate all historical episodes every time unless explicitly requested with the `--all` flag.
2. Sequential Shorts Numbering (`SH.XX`):
   - New Shorts follow strict sequential release numbering (e.g. following SH.01-SH.08, the next short is `SH.09`).
   - The top header ribbon and metadata files must match the sequential short number.

---

## 5. Python Automated Rendering Pipeline

All thumbnails are automatically generated via Python scripts utilizing Apple Silicon TrueType font rasterization (`/System/Library/Fonts/Hiragino Sans GB.ttc`) and PIL:

### Running the Thumbnail Generator

```bash
# Generate standalone thumbnails for any episode
python3 scripts/videogen/generate_thumbnails.py

# Integrated build (automatically produces 16:9 thumbnail.jpg and 9:16 short_thumbnail.jpg)
python3 scripts/videogen/build_all_releases.py
python3 scripts/videogen/build_all_shorts.py
```

---

## 6. Packaging and Storage Rule

Every episode release directory must strictly contain both standardized cover files:

```
docs/youtube_releases/E{XX}-{Title_Slug}-v{Version}/
├── thumbnail.jpg          # 16:9 4K High-CTR Landscape Cover (1920x1080)
├── short_thumbnail.jpg    # 9:16 High-CTR Vertical Cover (1080x1920)
├── video.mp4              # 16:9 Full HD Micro-lesson Video
├── short.mp4              # 9:16 Vertical Interactive Shadowing Short
├── metadata.md            # 16:9 Launch Package Metadata
├── short_metadata.md      # 9:16 Shorts Launch Package Metadata
└── script.json            # Machine-readable episode manifest
```
