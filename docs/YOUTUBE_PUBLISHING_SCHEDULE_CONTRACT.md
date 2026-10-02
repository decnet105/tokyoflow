#  TokyoFlow Japanese • YouTube Production & Publishing Contract
# Standard Operating Procedure (SOP) & Accelerated YPP Sprint (Target: Pre-Feb 1)

This contract defines the **mandatory production cadence, release schedule, video formats, packaging requirements, and platform rules** for the **TokyoFlow Japanese** channel to surpass the YouTube Partner Program (YPP) requirements (**1,000 Subscribers + 4,000 Public Watch Hours**) prior to February 1st.

---

##  The 7-Day Master Publishing Schedule (EST Timezone)

All publishing times are strictly locked to **Eastern Standard Time (EST)**, achieving dual-peak algorithmic saturation across North America, Europe, and Asia-Pacific.

```

                        TokyoFlow Weekly Publishing Grid (EST)                          

 Day of Week   Time (EST)    Format & Video Type                       Core Mission  

 Mon – Fri     08:00 AM EST  1x 16:9 Micro-Lesson (75s - 95s / 2.5m)   High APV/APX  
 (Workdays)                  1x 9:16 Vertical Short (30s - 50s)        Subscriber Hub
              
               05:00 PM EST  1x 16:9 Micro-Lesson (75s - 95s / 2.5m)   High APV/APX  
                             1x 9:16 Vertical Short (30s - 50s)        Subscriber Hub

 Saturday      05:00 PM EST  1x 16:9 Mega-Compilation (15 - 25 Min)    Watch Hours   
                             1x 9:16 Vertical Short (30s - 50s)        Subscriber Hub

 Sunday        05:00 PM EST  1x 16:9 Mega-Compilation (15 - 25 Min)    Watch Hours   
                             1x 9:16 Vertical Short (30s - 50s)        Subscriber Hub

```

### Weekly Total Output
- **10x 16:9 Single-Scenario Micro-Lessons** (1080p Full HD, 3-tier Ruby, bilingual breakdown, 3.5s CTA)
- **2x 16:9 Mega-Compilations** (15 ~ 25 Minutes, 10-episode seamless immersion loops)
- **14x 9:16 Vertical Shorts** (Rapid single-phrase shadowing & call-outs)
- **Total: 26 Packaged Video Assets per Week**

---

## ⏱ Mathematical Velocity Model (120-Day YPP Sprint)

| Metric | Weekly Output | 17-Week Total (Pre-Feb 1) | Target Required | Safety Margin |
| :--- | :--- | :--- | :--- | :--- |
| **16:9 Micro-Lessons** | 10 videos | **170 Episodes** | ~100 Episodes | **+70% Buffer** |
| **15-25m Compilations** | 2 compilations | **34 Mega-Videos** | ~15 Videos | **+126% Buffer** |
| **9:16 Shorts** | 14 shorts | **238 Shorts** | ~100 Shorts | **+138% Buffer** |
| **Projected Watch Hours** | ~350 hrs/wk | **~5,900 Hours** | **4,000 Hours** | **147.5% Target Achieved** |
| **Projected Subscribers** | ~90 subs/wk | **~1,530 Subs** | **1,000 Subs** | **153.0% Target Achieved** |

---

##  Mandatory Skill Pipeline Standards

Every produced video must strictly adhere to the standardized skills:

### 1. Video Production Contract (`tokyoflow-video-factory`)
- **Visuals**: 1920x1080 Full HD, 30.0 fps, `yuv420p`.
- **Typography**: 3-Tier Ruby (Kana top, Japanese mid, Romaji bottom, English meaning bottom).
- **Karaoke Timing**: Millisecond Whisper word alignment with **80ms anticipatory offset**.
- **Bilingual Teamwork**:
  - `ja-JP-NanamiNeural` (`rate="-6%"`, `pitch="+3Hz"`): Japanese dialogue, tokens & spotlight examples.
  - `en-US-AndrewNeural` (`rate="+2%"`): English explanations of POS, meanings & nuances (speaks 100% pure English, never mispronounces Japanese).
- **Outro CTA**: Strictly **3.4 ~ 3.5s** unclipped audio (`TokyoFlow - Japanese Speaking`, Real Scenarios, 10,000+ JLPT Vocab).

### 2. Master Thumbnail Factory Contract (`tokyoflow-thumbnail-factory`)
Every released episode must generate both high-CTR covers:
- **16:9 Landscape Cover (`thumbnail.jpg`, 1920x1080 / 4K UHD)**:
  - Top-left `TokyoFlow 🇯🇵` brand capsule (white pill, crimson text).
  - 3D Electric-yellow / white heavy uppercase hook title (96pt).
  - Upper `[JLPT Level] EP.XX` serialized badge.
  - Giant 116pt center-bottom Japanese survival phrase with 10px black drop stroke.
  - Bottom `🇯🇵 Native Audio • [Tag]` scenario value pill.
- **9:16 Vertical Short Cover (`short_thumbnail.jpg`, 1080x1920)**:
  - Top header brand & serialized `[JLPT] SH.XX` category theme ribbon.
  - 108pt 3D electric-yellow hook banner.
  - Central 3-tier Ruby Japanese dialogue card.
  - Active Live Mic & dynamic waveform shadowing HUD (`🔴 REC | LIVE MIC`).
  - Bottom AI verification & TokyoFlow App conversion pill (`🎯 98.6% MATCH`).

### 3. YouTube Studio Metadata Rules
- **Long-Form Title**: MUST start with **`[JLPT Level] EP.XX [Title]`** (e.g. `[JLPT N5] EP.01 Tokyo Train Station Announcements Decoded!`).
- **Shorts Title**: MUST start with **`[JLPT Level] SH.XX [Title] #Shorts #LearnJapanese`**.
- **Description Box**:
  - **ZERO URLs** (no web links, no app store URLs in body).
  - **ZERO Emojis** (clean professional plain-text uppercase headers).
  - Accurate `00:00` dynamic chapter timestamps.
  - Key phrases list with Romaji and English translations.
  - Grammar spotlight summaries.
  - Mention exact App name: `TokyoFlow - Japanese Speaking`.
  - Clean hashtags: `#TokyoFlow #LearnJapanese #JapaneseSpeaking #TokyoTravel #JLPT #JapaneseShadowing`.

### 4. Release Directory Format (`En-标题-版本`)
Every episode is packaged as a 7-in-1 self-contained release under:
`docs/youtube_releases/E{XX}-{Title_Slug}-v{Version}/`
- `video.mp4` (16:9 Full HD Micro-lesson)
- `thumbnail.jpg` (16:9 4K High-CTR Landscape Cover)
- `metadata.md` (16:9 YouTube Launch Kit)
- `short.mp4` (9:16 Vertical Interactive Shadowing Short)
- `short_thumbnail.jpg` (9:16 Minimalist High-CTR Vertical Cover)
- `short_metadata.md` (9:16 YouTube Shorts Launch Kit)
- `script.json` (Structured machine-readable episode manifest)
