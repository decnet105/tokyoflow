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
- Priority 2: 4K photorealistic scene photograph matching the authentic Japanese/Tokyo context (e.g. government briefing room, Tokyo skyline, Shibuya yokocho, Akiba street, Ramen counter, Kombini store).
- Strictly PROHIBITED: Plain dark canvas, generic abstract wallpapers (such as liquid glass), or cartoon drawings as cover backgrounds. Always composite with 58% center-right subject crop, contrast boost, and multi-stop cosine/vignette overlays.

## 6. YouTube Shorts First-Frame Master Cover Injection Rule
- The YouTube Data API does NOT support setting custom thumbnails for YouTube Shorts (it only applies to 16:9 long videos).
- For all 9:16 vertical Shorts, the master cover (`short_thumbnail.jpg`) MUST ALWAYS be generated first and burned into the video stream as the first 8-10 frames (approx 0.25s ~ 0.33s at 30fps).
- This ensures YouTube's automatic thumbnail capture on upload displays the full-contrast, serialized 9:16 cover across all mobile feeds, carousels, and search results without requiring manual mobile app intervention.

## 7. Mandatory Authentic Scene Photo & Video Background Retention Rule (Last Mile Standard)
- All long-form masterclass videos (16:9) and vertical shorts (9:16) across both English and Chinese editions MUST retain an authentic background photo (`news_bg.jpg` / 4K Tokyo scene photograph) or authentic video clip as the persistent bottom background canvas, following the Last Mile masterclass production standard.
- Strictly PROHIBITED: Plain solid/flat blank canvas (e.g., solid gray/white `(248, 250, 252)` or flat dark rectangle `(12, 17, 29)`) without authentic photographic/video imagery.
- 16:9 Long-Form: 58% center-right subject crop, dark cosine vignette / multi-stop alpha gradient (dark left side for high-contrast card/subtitle readability, authentic scene visible on right and throughout), translucent frosted-glass HUD cards (`fill=(255, 255, 255, 235)` or dark frosted glass).
- 9:16 Shorts: 9:16 vertical crop, cinematic dark vignette overlay, floating translucent cards with glowing karaoke ruby tokens.
- Dynamic Video Clips: When cinema action clips or scenario video loops are available, composite smooth looped/action video with transparent RGBA HUD pipe overlays via FFmpeg (`overlay=0:0`).

## 8. Selective Target Execution Discipline (No Blanket Batch Re-renders)
- When modifying code, styling, typography, pipelines, or fixing bugs, NEVER re-render, regenerate, or overwrite all historical video packages across the channel unless the user explicitly instructs: "re-render all" / "全量重新生成".
- Always target only the specific active episode (`--ep X`, `--dir <PATH>`, or single package directory) for verification and testing.
- All production scripts MUST require explicit `--all` flags for full batch operations and default to single-target filtering, strictly protecting existing release assets in `docs/youtube_releases/` from accidental blanket overwriting.

## 9. Strict Dual-Language Playlist Isolation Policy (Zero Cross-Contamination)
- English videos and Chinese videos MUST ONLY be categorized into their respective language playlists. Cross-contamination is strictly prohibited.
- English Column A:
  - Long Masterclass: `PLHUEYGzrBe-s` (TokyoFlow Japanese Masterclass [English Edition])
  - Vertical Shorts: `PLVxXRTmSmcAM` (TokyoFlow Japanese Shorts [English Edition])
  - JLPT Levels: `PLY_ZLcqTrnU8` (N5), `PLIiV1gnNj8Ms` (N4), `PLFBaqxuiTcbo` (N3), `PLeb_7jP3fQ2M` (N2-N1)
  - Scenarios: `PLAUUBQzM_liE` (Transit), `PLBhQ4N46ef1k` (Kombini), `PLA-JfaJhOu2E` (Dining), `PLPigp6inTnV8` (Shopping), `PLHPFg4RJy4Po` (News)
  - Dedicated Trailers & Previews: `PLMsazYTqnfLA` (TokyoFlow Official Trailers & Channel Previews [English Edition])
- Chinese Column B:
  - Long Masterclass: `PLVchR4TmK56E` (TokyoFlow 日语实景精讲【中文解说版】)
  - Vertical Shorts: `PLTpb6FPYqYC4` (TokyoFlow 日语短视频跟读【中文解说版】)
  - JLPT Levels: `PLPBpfF_GX60Q` (N5), `PLNFRI1RlIvIU` (N4), `PLHeOP0in6rRg` (N3), `PLRh0i-oZUcq8` (N2-N1)
  - Scenarios: `PLdc0-MFoSiCc` (东京出行), `PLPDcqCSXjUWc` (街头生存), `PLRNRaN1g4Jac` (美食点单), `PLdgqOJf2bv54` (流行文化), `PLMIm06SWP2NE` (时事新闻)
  - Dedicated Trailers & Previews: `PLehSqEkAOYqk` (TokyoFlow 官方宣传片与频道预告【中文版】)
- Strict Isolation Discipline:
  - Trailers/previews (`EFRVKXcv85M`, `_xsDi_X4vo4`, `MkyFXvJrJw4`, `8JYC5wkdx9w`, `XUWDCPU0Tog`) MUST ONLY reside in dedicated trailer playlists and NEVER in educational/masterclass playlists.
  - Educational masterclasses/shorts MUST ONLY reside in their corresponding language educational playlists and NEVER in trailer playlists.

## 10. Scheme D Password-Protected Study Companion & Google Drive Synchronization
- Every episode and weekly compilation must have high-resolution 300 DPI A4 print-friendly study companion PDFs generated in both English and Chinese.
- Security: Encrypt each PDF with standard AES user password using the episode/compilation passcode (e.g. `TOKYOFLOW-EP14`, `TOKYOFLOW-WEEK1`).
- Storage: Upload all companion PDFs to official Google Drive under `TokyoFlow_Academy_Resources/Weekly_Master_Workbooks_PDF` with public read permissions.
- Discovery: Embed verified Google Drive download links and unlock passcodes into the YouTube video description box and pinned comment for every upload.



