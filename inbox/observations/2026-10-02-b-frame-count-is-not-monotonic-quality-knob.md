# Observation: B-frame count is an efficiency control, not a monotonic quality knob

Date: 2026-10-02
Status: Observation
Scope: OBS / NVENC / offline encoding / hard-sub source recording

## Observation

Increasing the configured maximum number of B-frames does not monotonically increase visual quality.

For OBS/NVENC recording, current OBS guidance uses 2 B-frames as a baseline. With look-ahead enabled, a larger maximum such as 4 can allow the encoder to choose adaptively between fewer and more B-frames depending on content. Without look-ahead, 2 is a safer general-purpose value.

For HEVC/AV1 NVENC, B-frame-as-reference should be enabled when multiple B-frames are used and the encoder/hardware supports it. NVIDIA states that B-frame references improve subjective and objective quality and recommends enabling the feature when multiple B-frames are configured.

At quality-targeted recording settings such as CQP, more B-frames usually improve compression efficiency more than they raise the perceptual-quality ceiling. In fast-motion game content, excessive fixed B-frame use can be neutral or counterproductive; scene-adaptive placement matters more than simply raising the maximum.

## Reusable implication

Treat B-frame count as part of GOP/temporal prediction strategy, not as a generic "quality slider".

For high-quality game-source recording intended for later hard-sub transcoding:
- prioritize source-generation quality, quality-based rate control, bit depth/chroma/color correctness, encoder preset/tuning, and avoiding dropped frames;
- use 2 B-frames as a robust baseline;
- consider 4 only with look-ahead/adaptive placement and after scene-class testing;
- enable B-frame references for HEVC/AV1 when available;
- verify with real fast-motion and low-motion samples rather than assuming larger values are better.

Do not promote to Canonical from this observation alone.
