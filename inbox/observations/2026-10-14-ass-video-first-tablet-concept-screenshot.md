# Observation — ASS tablet concept screenshot: video-first, self-identifying authoring surface

Date: 2026-10-14
Status: Observation / explicitly USER-CONFIRMED PENDING REVIEW (2026-10-14); visual interpretation only, not approved target UI, verified Compose screenshot, or measured usability.
Product: 11576865/ASS-Workbench-Android

## Input and observed facts
A 1534×960 screenshot was provided in conversation with top caption “ASS Workbench · 新 UI 概念方案” and bottom watermark “概念图 · 待确认 · 非运行截图”. The screenshot depicts a dark wide tablet/workbench layout: top document name/dirty/save controls, task strip “正文 / 排版 / 时间 / 效果”, a left selectable subtitle list and search, a large center video with image-overlay action chip “位置 · 当前字幕 #39”, optional safe-area/grid options on the video, direct subtitle bounding box with handles, separate compact playback transport beneath the image, an aligned waveform/timeline with timed Event blocks, and a right Event #39 inspector with scope, position, typography, appearance, Raw ASS, cancel and apply.

No large separate visible title “预览” is placed above the video in this concept. Video has some small insets and must NOT be described as mathematically edge-to-edge without measurement. It is an example of prioritizing the media image over ornamental panel headers; preserving aspect ratio and avoiding unwanted crop remain requirements to test independently.

## Transferable interface pattern (candidate for further validation; not promoted)

For media-centered creation tools, the viewport can self-identify through its actual content plus unobtrusive **context-bound overlay commands** (e.g. active subtitle/geometry mode). Semantic accessible names and status are still mandatory even when a redundant visible panel header is removed. Locate player transport and time ruler adjacent to the content, and keep directly manipulable objects in the same coordinate space as their real rendering. Treat source list, media preview, and Event editor as stable spatial anchors across task changes rather than assuming task switching should reorder the main columns.

The overlay must not obscure important video content or corrupt hit-target arbitration. Transparent title-bar removal alone does not establish compactness: acceptance should measure actual video image rectangle vs enclosing space, unused area, touch-handle reachability, and retained editor room across aspect ratios, viewport sizes and soft keyboard states.

## Evidence limits
Screenshot supplied without running APK identity or frame metric proof. It is a concept, not code evidence, an actual application capture, user signoff of every pixel, or proof that currently implemented Compose has this structure. No claim that user explicitly approved this entire arrangement. Code/field alignment requires an exact commit and a native screenshot or test.

## Deduplication
Related existing Foundry observations: `2026-10-13-ass-real-android-ui-video-comparison-and-spatial-anchors.md` (stable semantic anchors from VLC/LosslessCut recordings) and `2026-10-14-ass-preview-aspect-panel-chrome-attribution.md` (reconstruction vs pane chrome and media aspect occupancy). This entry is specifically a new user-supplied *ASS concept image* and its visually instantiated overlay/direct-object/timeline alignment pattern. No Canonical update.

## Explicit user disposition (2026-10-14)
In response to whether this image was an approved UI target or a design needing critique, the user chose **“待审查”**. This is a pending review subject, **not** consent to treat the shown screenshot as the target implementation or acceptance baseline. Previous assistant praise must not be mistaken for acceptance.

## New source-image review hypotheses (not reproduced bugs)
- The depicted media has only a narrow but still visible inset from the central column. Source picture is not an exact container-fit measurement and its source-media aspect ratio is unknown; test real display bounds without stretching/cropping.
- The screen has stable list/media/inspector semantic anchors, but the selected “排版” task still devotes a relatively tall permanent area to waveform/event blocks; validate task-dependent time dock height and affordance to expand on timing.
- The inspector's “局部覆盖” scope, “写入：当前字幕 · 1 条”, and “来自 Style: Opening” annotation near Raw ASS may not sufficiently distinguish Focus, Selection, Write Target, per-field inheritance and Event-local override. The source-visible Raw includes `\\pos(960,720)\\fs48`, so provenance must be presented at field/tag scope, not as a generic single provenance for all values.
- Tiny video object handles, numeric spin controls and dense inspector elements may fail touch-target accessibility on real tablet DP scaling; provide measured hit targets and precise alternative input.
- Context overlay, safe-area controls, and selected subtitle bounds are appropriate to layout mode but require checks for video-content occlusion and gesture arbitration.

No runtime defects, exact DPI usability scores, or user approval are inferred. Remain Observation, not Canonical.
