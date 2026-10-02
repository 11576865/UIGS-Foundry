# Candidate: Verification-oriented media player should reuse the authoritative playback/rendering core

Date: 2026-10-02
Status: Candidate
Scope: subtitle tooling / media-player integration / validation workflows

## Observation

In a toolchain that already depends on FFmpeg/libass semantics for subtitle authoring, hard-sub rendering and output verification, a separate video player is most valuable as a verification surface rather than as an independently implemented decoder/rendering stack.

mpv/libmpv is a strong fit because it already provides:
- FFmpeg-based demux/decode;
- native ASS rendering through libass;
- frame stepping;
- external and secondary subtitles;
- HDR/color-management controls;
- statistics, screenshots and scripting/IPC;
- embeddable libmpv API.

## Candidate principle

When a project needs a media player mainly to inspect subtitle timing, ASS rendering, tracks, HDR and encoded output, prefer reusing the same or closely aligned rendering/decode stack as the production pipeline. Avoid creating a second bespoke playback authority unless the project has requirements that the existing engine cannot satisfy.

Keep the player and editor/encoder semantically distinct:
- player = inspection/playback/verification;
- editor = document authoring;
- encoder = production/transcode.

The shared engine may be reused without merging these products into one application.

## Rationale

This reduces disagreement between preview and final output, avoids reimplementing codec/container/HDR/subtitle behavior, and preserves a single evidence path for visual validation.

Do not promote to Canonical from this single recommendation.
