# Observation: HSR gradient backgrounds must follow the first theorem's prior-art gate

Date: 2026-10-13
Status: Observation / early source review; no feature implementation or runtime test
Project: `11576865/HSR-Voice-Archive-Builder`
Domains: background generation, UI reuse, FFmpeg integration, quality acceptance, engineering method

## Trigger: violated product process

The user pointed out that gradient and soft backgrounds are established capabilities, and challenged a proposal to design HSR-specific presets, controls and parameter taxonomy from scratch without first surveying successful and failed existing implementations. The authoritative `项目原则报告_2026-09-30.txt` explicitly calls its first principle `第一定理：既有经验与失败研究定理`: first survey comparable Internet projects, why implementations succeeded, public failures/maintenance costs, reusable/avoided choices, and the differentiator. A speculative UI design without that survey violates the first theorem.

## Preliminary authoritative examples (not a comprehensive competitive audit)

- Shotcut's preexisting Gradient Video Filter documents `linear/radial`, offset, colors, position and blend mode; a reply from a user briefly thought options missing, then retracted that report. Distinguish this from Shotcut's *Gradient Map* (maps image intensities to a color ramp; not the same function): https://forum.shotcut.org/t/gradient-video-filter/14508
- Kdenlive's maintained `Cairogradient` lists pattern, start/end colors and opacity, normalized start/end coordinates and blend mode as a video effect: https://docs.kdenlive.org/en/effects_and_filters/video_effects/generate/cairogradient.html
- Kdenlive's title shape editor provides solid color or gradient, selectable presets and gradient editor without making users use a standalone paint product: https://docs.kdenlive.org/en/titles_and_graphics/titles/title_shapes.html
- GIMP's gradient tool exposes linear/radial and many additional shapes, and separates perceptual RGB, linear RGB and CIE Lab interpolation. Their existence is *prior art*, not evidence HSR requires an eleven-mode paint UI: https://docs.gimp.org/3.2/en/gimp-tool-gradient.html
- **FFmpeg itself already implements the `gradients` video source** with linear/radial/circular/spiral/square modes and multiple colors in newer source; available options vary across version; feature must be checked at runtime. This makes coding an entirely separate gradient renderer premature. https://www.ffmpeg.org/doxygen/8.1/vsrc__gradients_8c_source.html and https://ffmpeg.org/doxygen/5.1/vsrc__gradients_8c_source.html

## Initial failure/risk research

- FFmpeg's `gradfun` documentation explicitly states that 8-bit truncation causes **banding** in near-flat gradients, and it says the `gradfun` filter is designed for playback, not as pre-lossy-compression mitigation; encoding may erase the dithering. A linear/radial gradient is easy to render yet can still look poor in the final H.264 output. Source: https://ffmpeg.org/ffmpeg-filters.html (gradfun section).
- Cross-platform FFmpeg versions and static builds may differ in `gradients` availability or parameters, so a planned integration must discover the installed capability, test generated pixels with real FFmpeg and verify the final MKV on representative targets. This is a validation hypothesis, not a reported HSR field failure.
- Gradient Map versus Gradient generator are different operations; the names must not be conflated in the design or testing.

## Bounded consequence for HSR

Stop inventing novel soft-background option lists before evidence. First compare existing workflow controls and real source filter support. HSR likely needs only a *small reuse/adaptation* of proven linear/radial gradient input and preview behavior, integrated into the current Export/background scope, while keeping source FLAC, ASS and atomic MKV publication unchanged. Advanced gradient editing or broad creative presets are not established user requirements.

Acceptance must include actual FFmpeg output and final H.264/MKV frames (especially banding, clipping, black borders, text contrast and cross-build filter support), plus project-setting persistence; raw preview CSS is not a substitute. At this intake point there is **no code implementation, no validated gradient feature or production failure reproduction**.

Related: `inbox/observations/2026-10-13-hsr-mkv-track-refresh-vs-full-rebuild.md` tracks *export lifecycle* rather than prior-art background controls. Dedup search for gradient/background prior-art returned no matching Foundry records. No Canonical change.
