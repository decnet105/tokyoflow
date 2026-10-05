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
