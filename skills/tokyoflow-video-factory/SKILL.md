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
## 0. Golden Master Sample Standard (黄金样本标准: EP.10)

> [!IMPORTANT]
> **Approved Master Reference Package**: `docs/youtube_releases/E10-ayase_haruka_tennen-v1.0/`
> This episode represents the locked-in, approved Golden Master Standard for all subsequent episodes produced across TokyoFlow Japanese. Every automated and manual video run must strictly replicate the craft, audiovisual timing, dual-voice role separation, and thumbnail layout embodied in this package.

## The 4 Core Pillars: Production Bible & Director Contract (制作圣经与导演合同)

Every single video and release package produced by TokyoFlow Japanese must strictly satisfy the **4 Core Pillars of Competitive Moat**:

```
+----------------------------------------------------------------------------------------------------+
|                               TOKYOFLOW 4 CORE PILLARS PRODUCTION BIBLE                           |
+------------------------------------+---------------------------------------------------------------+
| 1. ⚡ Rapid Trend Velocity & GEO   | 24h Japanese Trend Radar indexing (Yahoo/NHK/X/Google Trends) |
|    (热点反应速度快 + 本地GEO定位)    | Dynamic Tokyo GEO tags (Shinjuku, Shibuya, Akiba, Ginza, etc.)|
+------------------------------------+---------------------------------------------------------------+
| 2. 🎭 Viral Entertainment & News   | Intriguing, humorous, culturally authentic pop culture topics |
|    (话题好玩 + 真实新闻原声镜头)     | Live News Broadcast TV HUD + authentic Japanese anchor voice  |
+------------------------------------+---------------------------------------------------------------+
| 3. 🎯 Strict JLPT Level Alignment  | 70% JLPT N5 (zero prerequisite) / 20% N4-N3 / 10% N2-N1       |
|    (能学到对应级别JLPT内容)          | Downscale complex news jargon into accessible SOV patterns    |
+------------------------------------+---------------------------------------------------------------+
| 4. 🧠 Frictionless Learning Ease   | Slowed-down native Tokyo speech (-10% ~ -12%) for beginners   |
|    (容易学 + 毫秒发光卡拉OK)         | 30fps true frame-by-frame word-by-word glowing yellow karaoke  |
+------------------------------------+---------------------------------------------------------------+
```

---

## 1. Target Audience, Pedagogical Formula & SEO/GEO Contract

1. Target Audience: Global English speakers learning practical Japanese (N5 Beginner to N1 Advanced, travelers, anime fans, and Tokyo expats/commuters).
2. Audience Difficulty Distribution (70% N5 Mandatory):
   - 70% JLPT N5 (Beginner / Zero-barrier / Primary Focus): Core everyday words, basic polite verb forms, zero prerequisite.
   - 20% JLPT N4-N3 (Intermediate): Practical news, workplace/social nuance, netizen slang.
   - 10% JLPT N2-N1 (Advanced): Official public relations, legal/editorial nuances.
3. Mandatory JLPT Level Badge and Prefix:
   - Long-form video titles MUST strictly start with: `[JLPT N5] EP.XX <High-CTR English Title> | Real Japanese Breakdown`.
   - Shorts video titles MUST strictly start with: `[JLPT N5] SH.XX <High-Impact English Hook>! #Shorts #LearnJapanese`.
   - Video slides MUST render a prominent JLPT difficulty badge (e.g. `[ JLPT N5 ] Essential Foundation`).
4. High-Efficiency SEO & GEO Design (SEO/GEO 战略设计):
   - GEO Precision: Target specific Tokyo districts and landmarks (e.g., `SHINJUKU STATION`, `SHIBUYA 7-ELEVEN`, `AKIHABARA ANIME TOWN`, `GINZA SHOPPING`, `ROPPONGI`).
   - Trending Entity Harvesting: Exploit real-time Japanese trending keywords, celebrity names, anime titles, and JLPT search volume.
   - Zero-URL Clean SEO Description: High-density keyword placement in timestamps, key phrase lists, and pinned interactive poll comments.
5. Strict Zero-Crossover Dual-Voice Contract (纯净双语角色分离铁律):
   - Female Voice (`ja-JP-NanamiNeural`, `rate="-12%"`, `pitch="+2Hz"`): 100% Native Tokyo Japanese ONLY (dialogues, vocabulary readings, example sentences). Strictly NEVER reads English translations or definitions.
   - Male Voice (`en-US-AndrewNeural`, `rate="+2%"`): 100% Natural American English ONLY (immediate English translations after each Japanese phrase/word, grammatical breakdowns, and cultural explanations). Strictly NEVER reads Japanese characters.
   - Priority 1 (Authentic Native Event Audio / 原音原声优先): When real press/news event soundbite is available (`source_audio.mp3`), use it for the opening 3-5s immersion!
   - Priority 2 (Studio Broadcast Delivery): When synthesized, use `ja-JP-KeitaNeural` at standard un-rushed broadcast cadence (`rate="+0%"`, `pitch="+1Hz"` with TV broadcast chime).
6. Mandatory Deep Japanese Cultural Insight by Andrew (男声必带日本本土文化深度解说):
   - In every episode's breakdown section, Andrew MUST deliver a dedicated 1-2 sentence English cultural insight explaining the unique Japanese social/cultural context of the topic (e.g. why '天然/tennen' is beloved as cute airhead charm in Japanese pop culture, omotenashi hospitality, seasonal kombini culture).
   - Strict Authenticity: Grounded strictly in authentic Japanese society, zero hallucination.
7. High-Definition Artist/Scene Photo as Master Thumbnail Base (艺人高清大图作为封面底图法则):
   - Whenever an authentic high-definition photo/scene of the artist, celebrity, or news subject is obtained (from YT/news media/4K scene synthesis), it MUST serve directly as the base background image (`bg_image_path`) for both 16:9 Master Thumbnail (`thumbnail.jpg`) and 9:16 Shorts Cover (`short_thumbnail.jpg`), overlaying the 3D yellow hook stack and pure white glowing Japanese soul phrase.
8. Strict Typography Safety:
   - Dynamic multi-line wrapping with minimum 80px side margins. NEVER truncate or clip text horizontally. All glyphs must render with clean typography without placeholder boxes.

---

## 2. Standard 7-Step Episode Architecture (with Live News Immersion)

Every TokyoFlow YouTube episode follows a structured 7-step sequence:

```
[Chapter 0: Live Breaking News Broadcast Immersion & Authentic Event Voice]
   -> (3-6s, Live TV News HUD, Flashing 【LIVE ニュース速報】, Authentic Event Soundbite / Natural News Anchor Audio + Chime)
   -> Background Mandate: Strictly use authentic, photorealistic topic press conference / Tokyo event scenes (e.g. news_bg.jpg).
   -> Audio Mandate: Prioritize real event soundbites (原音); if using studio anchor, keep natural un-rushed speed (rate=+0%).
   -> Strict Zero Cartoon Fallback Rule: NEVER use cartoon manga illustrations (e.g. akiba_neon.jpg) or generic placeholder drawings. If no topic image is available locally, the pipeline must search YT/web or dynamically synthesize a 16:9 4K photorealistic press event/street scene matching the topic.
[Chapter 1: Real-Life Dialogue Immersion & Follow-Along]
   -> (4-6s, 3-Tier Ruby typography with 80ms Anticipatory Millisecond Karaoke Highlighting at -12% Speed)
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

### 4. Outro Card & Scheme D Passcode Standard (片尾完播密码与讲义分发规范)
- **Visual Scheme D Passcode Card**:
  - Outro frame MUST render a high-contrast amber/gold Passcode Card (`[ STUDY PASSCODE: TOKYOFLOW-EPXX ]`).
  - Subtitle / Instruction Box: `[SUBSCRIBER REWARD] Download the full JLPT N5-N3 Study Workbook PDF from the Google Drive link in description using this passcode.`
- **Mandatory Spoken Vocal Announcement**:
  - Explainer voice (Andrew EN / Yunxi ZH) MUST speak the passcode announcement aloud:
    - English: `"Great job today! Download this episode's complete JLPT study workbook in the description below using unlock passcode TOKYOFLOW-EPXX. Remember to subscribe for daily Tokyo immersion!"`
    - Chinese: `"今天的实景跟读训练完成！欢迎在视频简介栏和置顶评论区获取本期 JLPT 配套研习讲义，输入解锁密码 TOKYOFLOW-EPXX 即可免费下载。记得点击订阅开启每日跟读！"`
- **App & Channel Features**:
  - `TokyoFlow - Japanese Speaking | Real Tokyo Scenarios | 10,000+ JLPT Vocab`
- **Audio Padding**:
  - Duration: 4.5s to 6.0s (Full natural speech without clipping + 0.5s visual tail).

---

## 4. Automated Thumbnail Generation (Golden Master Standard)

Every video build strictly adheres to the `tokyoflow-thumbnail-factory` Golden Master visual standard, saving the 16:9 master cover directly as `thumbnail.jpg`:
1. **Resolution and Canvas**: `1920x1080 Full HD / 4K UHD`.
2. **Authentic HD Photo Base**: Real-life authentic Tokyo photograph on right 55%-60% (`x > 800`), contrast `1.15x`, saturation `1.18x`. Zero cartoon drawings/stickers.
3. **Smooth Non-Linear Dark Gradient Fade**: Cosine gradient `alpha = 245 * 0.5 * (1 + cos(pi * x / 1180))` for `x < 1180`, ensuring pristine text contrast without dimming the hero subject.
4. **Top-Left Solid White Brand Pill**: `TokyoFlow Japanese` in bold crimson `(225, 29, 72)`.
5. **Top-Right Solid Crimson Badge**: `[JLPT Level] • EP.XX` in bold pure white `(255, 255, 255)`.
6. **Left Giant 3D Solar Yellow Hook**: 96pt Heavy Hiragino Sans font (`#FEF08A`) with 5px solid black 3D extrusion + Pink Sub-hook (`#F472B6`, 34-36pt).
7. **Glassmorphic Japanese Learning Card**: Rounded dark navy card (`#0A0F1C`, 235 alpha) with Sky Cyan border (`#38BDF8`, 3px), displaying Target Japanese line, JLPT Grammar tag, English translation, context note, and Tokyo setting.
8. **Bottom Full-Width Crimson Conversion Ribbon**: Solid crimson `#E11D48` ribbon highlighting `100% NATIVE TOKYO AUDIO • SHADOWING PRACTICE • FULL VOCAB & GRAMMAR BREAKDOWN`.

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
