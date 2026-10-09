# TokyoFlow Japanese - Project Rules & Guidelines

## 1. Zero Emoji Policy (Strict Discipline)
- Do NOT use, output, or generate any emojis anywhere in any context.
- This applies universally to:
  - Agent responses and chat messages.
  - Video scripts, slide text, dynamic HUD cards, and subtitles.
  - YouTube video titles, shorts titles, description boxes, and tags.
  - Thumbnails, banner graphics, and covers.
  - Commit messages, pull request descriptions, documentation, and markdown files.
  - Log outputs and script messages.
- Always use clean, professional text, standard brackets (e.g., `[JLPT N5]`, `【JLPT N4】`), bullet points (`-` or `*`), or standard punctuation instead of emoji icons.

## 2. Standardized JLPT Difficulty Badges
- All JLPT difficulty levels must strictly adhere to standard alphanumeric notation:
  - `[JLPT N5]`
  - `[JLPT N4]`
  - `[JLPT N3]`
  - `[JLPT N2]`
  - `[JLPT N1]`
- Use brackets `[JLPT NX]` or full-width brackets `【JLPT NX】` in Chinese contexts without any emoji decorations.

## 3. Multi-Language & YouTube Publishing Architecture
- Single YouTube Channel Architecture:
  - All language versions (English, Chinese, future Korean, etc.) and formats (16:9 Long-form, 9:16 Shorts) must be published to the single official channel to aggregate watch time and subscribers for a unified YouTube Partner Program (YPP) monetization qualification.
  - Column A (Global English): `TokyoFlow Japanese Masterclass [English Edition]` & `TokyoFlow Japanese Shorts [English Edition]`
  - Column B (Chinese Edition): `TokyoFlow 日语实景精讲【中文解说版】` & `TokyoFlow 日语短视频跟读【中文解说版】`
- Audio Synthesis Voice Discipline:
  - Japanese Voice: Pure Tokyo Standard (`ja-JP-NanamiNeural`)
  - Chinese Explainer: `zh-CN-YunxiNeural`
  - English Explainer: `en-US-AndrewNeural`

## 4. Multi-Language Publishing Cadence & Subscriber Notification Rules
- Column A (English Edition):
  - Scheduled Release Time: 08:00 AM EDT.
  - Subscriber Notification: `notifySubscribers = True` (Publish to subscriptions feed and notify subscribers).
- Column B (Chinese Edition):
  - Scheduled Release Time: 08:00 PM EDT (20:00 EDT).
  - Subscriber Notification: `notifySubscribers = False` (Do NOT publish to subscriptions feed and do NOT notify subscribers to avoid confusing the global subscriber base while ensuring full search, playlist, and recommendation discoverability).

## 5. Mandatory Authentic Scene & News Background Photo Rule for Covers
- Every 16:9 Long-Form thumbnail (`thumbnail.jpg`) and 9:16 Vertical Shorts cover (`short_thumbnail.jpg`) MUST have an authentic, realistic base photo (`news_bg.jpg`).
- Priority 1: Authentic original news press/event photo of the topic.
- Priority 2: 4K photorealistic scene photograph matching the authentic Japanese/Tokyo context (e.g. government briefing room, Tokyo skyline, Shibuya yokocho, Akiba street, Ramen counter, Kombini store) or authentic 4K anime aesthetic background.
- Cover Uniqueness Discipline: Every package must use a distinct, dedicated cover image. Reusing the same cover or background hash across different episodes/series is strictly prohibited.
- Strictly PROHIBITED: Plain dark canvas, generic abstract wallpapers (such as liquid glass), or cartoon drawings as cover backgrounds. Always composite with 58% center-right subject crop, contrast boost, and multi-stop cosine/vignette overlays.

## 6. Universal Video First-Frame Master Cover Burn-In Rule (All 16:9 & 9:16 Videos)
- Across ALL video pipelines (both 16:9 Long-Form Masterclasses and 9:16 Vertical Shorts), the serialized master cover (`thumbnail.jpg` for 16:9, `short_thumbnail.jpg` for 9:16) MUST ALWAYS be generated first and burned directly into the video stream as the first 8-10 frames (approx 0.25s ~ 0.33s at 30fps).
- Rationale:
  - For 9:16 Shorts: YouTube Data API does not support custom thumbnail upload for Shorts. First-frame injection ensures YouTube's automatic frame grab displays the full-contrast serialized cover across all mobile feeds, carousels, and search results.
  - For 16:9 Long-Form: Burning the 16:9 master cover into frame 0 ensures that video player previews, hover scrubbers, third-party embeds, social shares, and stream caching always lead with the branded 4K master cover without flickering or empty black frames.

## 7. Mandatory Authentic Scene Photo & Video Background Retention Rule (Last Mile Standard)
- All long-form masterclass videos (16:9) and vertical shorts (9:16) across both English and Chinese editions MUST retain an authentic background photo (`news_bg.jpg` / 4K Tokyo scene photograph / 4K anime scene) or authentic video clip as the persistent bottom background canvas, following the Last Mile masterclass production standard.
- Cinema/Movie Topics Standard: For movies, anime, or drama masterclasses (e.g. *Last Mile*, Ghibli, Shinkai, live-action films), authentic high-resolution film footage or stills must be used as the persistent bottom canvas. Shot cuts must not repeat or stall across slides.
- Strictly PROHIBITED: Plain solid/flat blank canvas (e.g., solid gray/white `(248, 250, 252)` or flat dark rectangle `(12, 17, 29)`) without authentic photographic/video imagery.
- 16:9 Long-Form: 58% center-right subject crop, dark cosine vignette / multi-stop alpha gradient (dark left side for high-contrast card/subtitle readability, authentic scene visible on right and throughout), translucent frosted-glass HUD cards (`fill=(255, 255, 255, 235)` or dark frosted glass).
- 9:16 Shorts: 9:16 vertical crop, cinematic dark vignette overlay, floating translucent cards with glowing karaoke ruby tokens.

## 8. Selective Target Execution Discipline (No Blanket Batch Re-renders)
- When modifying code, styling, typography, pipelines, or fixing bugs, NEVER re-render, regenerate, or overwrite all historical video packages across the channel unless the user explicitly instructs: "re-render all" / "全量重新生成".
- Always target only the specific active episode (`--ep X`, `--dir <PATH>`, or single package directory) for verification and testing.
- All production scripts MUST require explicit `--all` flags for full batch operations and default to single-target filtering, strictly protecting existing release assets in `docs/youtube_releases/` from accidental blanket overwriting.

## 9. Strict Dual-Language Playlist Isolation Policy (Zero Cross-Contamination)
- English videos and Chinese videos MUST ONLY be categorized into their respective language playlists. Cross-contamination is strictly prohibited.
- English Column A:
  - Long Masterclass: `PLHUEYGzrBe-s` (TokyoFlow Japanese Masterclass [English Edition])
  - Vertical Shorts: `PLVxXRTmSmcAM` (TokyoFlow Japanese Shorts [English Edition])
  - Kana 50 Sounds: `PLIFPD4LvhAZk` (TokyoFlow Japanese Kana Masterclass [Hiragana & Katakana])
  - JLPT Levels: `PLY_ZLcqTrnU8` (N5), `PLIiV1gnNj8Ms` (N4), `PLFBaqxuiTcbo` (N3), `PLeb_7jP3fQ2M` (N2-N1)
  - Scenarios: `PLAUUBQzM_liE` (Transit), `PLBhQ4N46ef1k` (Kombini), `PLA-JfaJhOu2E` (Dining), `PLPigp6inTnV8` (Shopping), `PLHPFg4RJy4Po` (News)
  - Dedicated Trailers & Previews: `PLMsazYTqnfLA` (TokyoFlow Official Trailers & Channel Previews [English Edition])
- Chinese Column B:
  - Long Masterclass: `PLVchR4TmK56E` (TokyoFlow 日语实景精讲【中文解说版】)
  - Vertical Shorts: `PLTpb6FPYqYC4` (TokyoFlow 日语短视频跟读【中文解说版】)
  - 五十音图专栏: `PLNU1sAPLg7Y4` (TokyoFlow 日语五十音图零基础精讲【平假名与片假名】)
  - JLPT Levels: `PLPBpfF_GX60Q` (N5), `PLNFRI1RlIvIU` (N4), `PLHeOP0in6rRg` (N3), `PLRh0i-oZUcq8` (N2-N1)
  - Scenarios: `PLdc0-MFoSiCc` (东京出行), `PLPDcqCSXjUWc` (街头生存), `PLRNRaN1g4Jac` (美食点单), `PLdgqOJf2bv54` (流行文化), `PLMIm06SWP2NE` (时事新闻)
  - Dedicated Trailers & Previews: `PLehSqEkAOYqk` (TokyoFlow 官方宣传片与频道预告【中文版】)

## 10. Free Study Companion, Google Drive Sync & Outro Passcode Display
- Every episode, thematic series, and weekly compilation must have high-resolution 300 DPI A4 print-friendly study companion PDFs generated in both English and Chinese.
- Storage: Upload all companion PDFs to official Google Drive under `Weekly_Master_Workbooks_PDF` with public read permissions (`anyoneWithLink: reader`).
- Discovery: Embed verified Google Drive direct download links into YouTube video description boxes and pinned comments for every upload.
- Video Outro Passcode: Display the official download / unlock passcode on the outro slide of the video (e.g. `Passcode: TOKYOFLOW` / `下载口令：TOKYOFLOW`), while placing the link directly in comments for seamless user access.

## 11. Mandatory Native Japanese Audio Playback in Shorts Follow-Along Drill (Zero Silence Discipline)
- In all 9:16 Shorts (both English Column A and Chinese Column B), Stage 3 (Follow-Along / Shadowing Drill) MUST directly play the native Tokyo standard Japanese audio (`ja-JP-NanamiNeural`) rather than empty silence or blank recording gaps.
- Rationale: Since pre-recorded video viewers cannot receive interactive microphone feedback, silence creates dead air. Playing the native pronunciation again enables the user to listen to authentic Japanese pronunciation a second time while reading along, significantly enhancing immersion and learning effectiveness.
- Cue Narration:
  - English: `"Now your turn! Read along with native audio in 3, 2, 1, go!"`
  - Chinese: `"轮到你跟读啦！跟着东京原声一起大声读，3、2、1，开口！"`
- Visual Synchronization: Stage 3 glowing karaoke tokens must be synchronized with the drill audio (`05_jp_drill.mp3`) via Whisper millisecond word alignment.

## 12. Strict TTS Voice Separation Discipline (Zero Cross-Language Pronunciation)
- Rule: Chinese explainer TTS (`zh-CN-YunxiNeural`) and English explainer TTS (`en-US-AndrewNeural`) must NEVER pronounce Japanese words, romaji, or kana.
- Rule: Japanese native TTS (`ja-JP-NanamiNeural`) is EXCLUSIVELY responsible for all Japanese kana, kanji, words, phrases, and sentence pronunciation.
- Explainer Voice Duties:
  - Chinese Explainer (`Yunxi`): Pronounces ONLY Chinese text explaining parts of speech, grammar nuances, cultural context, and translation.
  - English Explainer (`Andrew`): Pronounces ONLY English text explaining parts of speech, grammar nuances, and translation.
- Decoupled Cues: In all breakdown cues, teamwork cues, slide scripts, and prompts, ensure explainer speech strings contain zero Japanese words or romaji tokens.

## 13. Zero Unreleased App Promotion Policy
- Under no circumstances should unreleased TokyoFlow iOS/Android App promotions, download prompts, or App Store references be included in video outros, bottom banners, slides, audio synthesis, descriptions, metadata, or pinned comments.
- Video outros and bottom banners must focus exclusively on subscribing to the channel, daily shadowing practice, and downloading the free study companion PDF from Google Drive.

## 14. Typography, Universal Font Fallbacks & Bounding Box Layout Discipline
- All PIL/Pillow canvas drawing, subtitle rendering, and slide generation scripts must configure robust font fallbacks (`/System/Library/Fonts/Supplemental/Arial Unicode.ttf`, `/Library/Fonts/Arial Unicode.ttf`, or `/System/Library/Fonts/Hiragino Sans GB.ttc`).
- Zero Missing Glyphs: Ensure wave dashes `〜`, Japanese punctuation, quotation marks, and full-width brackets never render as `⌧` or empty box characters.
- Dynamic Text Wrapping & Bounding Box Safety: Long sentences must dynamically wrap to prevent any text clipping or overflowing outside cards. Layouts must compute actual text bounding boxes (`draw.textbbox`) with adequate margins.

## 15. Mandatory Pre-Upload QC / UMS Gate (Enso Shide 99-Point Standard)
- Every video release package MUST pass the automated Quality Control engine (`scripts/videogen/tokyoflow_qc_engine.py`) with a score of >= 99.0 / 100.0 before uploading to YouTube.
- The 10 Mandatory Checkpoints:
  1. Cover uniqueness & HD authentic topic photo.
  2. Authentic film stills/clips for cinema topics (Last Mile standard, non-repeating cuts).
  3. Valid H.264 video encoding & exact aspect ratios (1920x1080 for 16:9, 1080x1920 for 9:16).
  4. Typography, dynamic text wrapping & bounding box margins (zero overflow/clipping).
  5. Strict TTS voice separation (zero Japanese words in EN/ZH explainer speech).
  6. Free 300 DPI A4 study companion PDF generated & verified on Google Drive (HTTP 200).
  7. Video outro passcode display & comment link placement.
  8. Millisecond karaoke glowing highlight synchronization.
  9. Shorts Stage 3 follow-along drill plays native Japanese audio (zero dead air).
  10. Strict Zero Emoji Discipline & Zero Unreleased App Promo.
