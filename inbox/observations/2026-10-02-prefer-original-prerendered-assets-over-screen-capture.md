# Observation: Prefer original pre-rendered video assets over screen-recorded playback when available

Date: 2026-10-02
Status: Observation
Scope: game capture / pre-rendered cutscenes / Bink BK2 / archival workflows

## Observation

When a game cutscene is stored as a pre-rendered video asset such as a Bink 2 .bk2 file, directly decoding that asset and screen-recording its in-game playback are not equivalent.

Direct asset path:
.bk2 asset
→ decoder
→ frames/audio

Screen-recording path:
.bk2 asset
→ game decoder
→ game presentation/render/compositor
→ OS/GPU presentation path
→ capture
→ recording encoder

The screen-recorded path can introduce:
- an additional lossy encode generation;
- scaling or aspect-ratio transforms;
- color-range, matrix, transfer or HDR/SDR conversions;
- frame pacing and dropped/duplicated capture frames;
- overlays, subtitles, post-processing or UI added by the game;
- audio remixing, spatialization or track loss depending on the capture path.

Conversely, the original asset may not contain elements added during playback, such as separately rendered subtitles, overlays, localized audio, or game-side post-processing.

## Reusable implication

For archival extraction or codec-quality comparison, prefer the original pre-rendered asset when it is available and decodable.

For reproducing exactly what the user sees/hears in-game, use the game presentation path, but treat the resulting capture as a derived representation rather than the source asset.

Do not promote to Canonical from this single observation.
