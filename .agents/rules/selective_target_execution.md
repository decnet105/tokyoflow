# Selective Target Execution Discipline

## Core Directive
Never re-render, regenerate, or overwrite all historical video packages across the channel when modifying code, styles, typography, or fixing bugs, unless the user explicitly requests a full channel rebuild (e.g., "re-render all" / "全量重新生成").

## 1. Single-Target Default
- When developing, testing, or verifying fixes, always target only the single active episode or newly added episode (e.g. `--ep 11`, `--dir docs/youtube_releases/E11...`).
- Never run batch generation loops across all release folders without explicit user instruction.

## 2. CLI Script Safety Standard
- All generator and packager scripts MUST implement argument parsers (`argparse`):
  - `--ep` / `--episode <NUM>`: Run on a single specific episode.
  - `--dir <PATH>`: Run on a specific target directory.
  - `--all`: Explicit flag required to perform batch loops over all configured items.
  - Default behavior when no target is passed: Display usage instructions or target the single latest release, never silently looping over the entire repository.

## 3. Preservation of Historical Assets
- Existing packages in `docs/youtube_releases/` are final release artifacts.
- Protect them from unintended clobbering, ensuring that existing uploaded videos, audio tracks, and thumbnails are preserved in their validated state.
