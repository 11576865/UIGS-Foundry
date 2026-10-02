# Candidate: Shared subtitle renderer does not imply identical player output

Status: candidate
Date: 2026-10-02
Domains: media-playback, subtitle-rendering, validation

## Summary

Two media players that both use libass can still produce visibly different ASS output because the renderer is only one layer of the playback pipeline.

Player integration controls at least:
- libass version/build options;
- font attachment discovery and fallback;
- frame/storage size supplied to libass;
- pixel/display aspect information;
- ASS style overrides and compatibility switches;
- subtitle color handling relative to video metadata;
- compositor/blending behavior after libass returns subtitle images.

Therefore "uses libass" is evidence of semantic compatibility, not proof of pixel-identical output.

## Candidate rule

When selecting a reference player for ASS validation:

- identify the actual subtitle renderer and its version;
- disable user/player style overrides where possible;
- preserve embedded-font loading;
- ensure video geometry/aspect metadata reaches the renderer;
- distinguish libass rendering output from the player's later compositing/output path;
- use the same player/build/configuration for regression baselines;
- use a second player only as a cross-check, not as an assumed equivalent oracle.

A player with more explicit controls over ASS integration may be preferable as a reproducible reference even when another player also uses libass and is perfectly suitable for normal playback.

## Evidence

Current mpv documentation exposes explicit ASS controls such as sub-ass-override, embeddedfonts, sub-ass-use-video-data, VSFilter color compatibility, shaping and hinting.

Current VLC source initializes libass directly, loads embedded TTF/OTF/TTC attachments, supplies frame/storage size and pixel aspect to libass, and renders via ass_render_frame. VLC then converts libass images into VLC subpicture regions; the source comments note limitations around subpixel blending that can make text look unaligned in some cases.

## Provenance

- public sources: mpv manual; VLC current libass integration source
- evidence level: source-code/documentation comparison
- status rationale: reusable engineering guidance, but not yet validated across a broad player/version matrix

This is a Candidate only. It is not Canonical.
