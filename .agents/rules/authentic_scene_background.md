# Authentic Scene Photo & Video Background Retention Rule

## Core Directive
All long-form masterclass videos (16:9) and vertical shorts (9:16) across both English and Chinese editions MUST retain an authentic background photo (`news_bg.jpg` / 4K Tokyo scene photograph) or authentic video clip as the persistent bottom background canvas, following the Last Mile masterclass production standard.

## 1. Strict Prohibition of Flat/Solid Canvases
- Never use a plain solid or flat canvas (e.g. solid white/gray `(248, 250, 252)`, solid flat dark rectangle `(12, 17, 29)`) without authentic photographic or video imagery.
- All slide frames, karaoke follow-along drills, vocabulary breakdown HUDs, intro slides, and outro cards must be composited over the authentic scene.

## 2. 16:9 Long-Form Masterclass Standard
- Base Layer: High-resolution authentic news photo (`news_bg.jpg`), scene photograph (e.g. `docs/youtube_assets/scene_backgrounds/`), or continuous movie action footage.
- Visual Hierarchy & Compositing:
  - 58% center-right subject crop to preserve key visual focal points.
  - Multi-stop cosine vignette / alpha gradient on the left half to ensure 100% text and HUD readability.
  - Contrast boost (1.15x) and saturation calibration (1.18x) on base photography.
  - Translucent frosted-glass HUD cards (e.g., `(255, 255, 255, 235)` or dark frosted `(15, 23, 42, 230)`) with crisp borders.

## 3. 9:16 Vertical Shorts Standard
- Base Layer: 9:16 vertical crop of the authentic scene photo or motion video footage.
- Dark Vignette & Readability: Multi-stop gradient overlay on top and bottom regions to guarantee clear contrast for header capsules, hook titles, and dynamic karaoke cards.
- Floating HUD: Semi-transparent dialogue cards floating directly over the authentic Tokyo street / news backdrop.

## 4. Video-on-Video Compositing Standard (Cinema Masterclass)
- When video footage is available, FFmpeg compositing must pipe the smooth background MP4 stream (`[0:v]`) under the transparent RGBA HUD pipe (`[1:v]`) using `overlay=0:0`.
