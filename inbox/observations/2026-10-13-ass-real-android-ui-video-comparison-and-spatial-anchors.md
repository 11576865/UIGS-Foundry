# Observation: ASS UI review against recorded Android player/editor surfaces and desktop workbench patterns

Date: 2026-10-13
Status: Observation / video inspection + official documentation + project design constitution; recommendations remain hypotheses
Product: 11576865/ASS-Workbench-Android
Related prior Observation: inbox/observations/2026-10-13-ass-design-reference-to-android-ui-fidelity-gap.md

## Source evidence
Two user-uploaded Android screen recordings, examined as real state sequences (not conceptual renders):
- Screenrecorder-2026-10-13-14-48-46-587.mp4, 41.4 s, 1282×1920: **VLC Android** shown in portrait browsing, SAF selection, then rotated playback. This footage demonstrates browsing/playback transitions, *not* professional subtitle creation. At about 3–18 s, left library rail, top media tabs, permission/SAF flows; from about 24–38 s, video and transient playback controls dominate.
- Screenrecorder-2026-10-13-14-49-58-466.mp4, 56.6 s, 1920×1282: **LosslessCut** landscape video editing. At about 7–10 s: stable left and right tool rails, video-centered space and full-width bottom timeline with pinch-zoom affordance; about 13–20 s: settings overlay leaves editor visible; about 27–48 s: time navigation remains spatially stable; about 51–54 s: Smart Cut panel shows parameter sliders and explicit Apply/Cancel. Footage does not prove its entire feature set, native quality, or superiority. Note material content includes black video frames; black space alone cannot establish inefficient viewer allocation.

Authoritative additional inputs:
- ASS UI Constitution replacement 2026-10-01: bounded adaptive workspace; five distinct coordinate spaces; shared canonical domain; tools in Hosts without dropping identity, bindings or drafts; no demand that all content be in the infinite canvas or fixed panels removed.
- Designing Interfaces 3rd ed Chinese edition: Canvas Plus Palette and Many Workspaces; task/content structure and spatial continuity.
- Aegisub overview (https://aegisub.org/docs/latest/overview/), Subtitle Edit main-window documentation (https://github.com/SubtitleEdit/subtitleedit/blob/main/docs/features/main-window.md), Blender workspace documentation (https://docs.blender.org/manual/en/latest/interface/window_system/workspaces.html).

## Distinct transferable pattern
For a complex mobile ASS editor, preserve stable recognizable **semantic anchors** (video+ASS result, media clock/timeline, focused/selected subtitle identity, document save status), while allowing context-sensitive editing tools to change presentation (inspector, side/bottom sheet, docked node, focused surface). Persistent access to functions need not equal permanently expanded panels. Task switching should not reinitialize the editor or silently alter Focus/Selection/Binding/Write Target, draft, history, media time or the user's layout.

Do not copy VLC's minimal player UI as an editor, nor LosslessCut's cutter-only timeline/rails as a complete subtitle production system. ASS requires event/grid/text semantics in addition to video and timing. Desktop Aegisub and Subtitle Edit validate that lists/edit boxes, waveform/timeline and video are complementary, not independent replacement products.

Possible product experiment, not Canonical:
- large landscape: content-first video anchor, expandable/persistent timeline at bottom, event navigator on an edge, on-demand target-aware inspector on available side or local overlay;
- narrow portrait: reorder as bounded responsive flow with preserved tool identity; video may pin, collapse to compact, or expand; timeline remains reachable from a discoverable handle; no permanent unreadably small preview or duplicated editors;
- spatial Host: preserve the same semantic anchor/accessibility even when tools live in world geometry; screen-fixed navigation/return survives.
- use raw/rendered previews as two semantic views of one editable ASS document; show inherited Style, event override, write target, draft status and renderer limits at the point of editing.

## Acceptance evidence boundary
No current real ASS APK was recorded in these two samples. Specific assertions that the existing ASS interface fails these proposed quality goals require a current-exact-SHA capture and user-task inspection. Suggested screenshot states: browsing/import; selected event+video; timeline timing drag; style/geometry gesture; raw ASS with IME; batch preview/apply; save/reopen/recovery; device rotations. Observe both render quality and task preservation. Captured reference videos support comparative design reasoning only.

## Dedupe
Foundry GitHub searches for mobile anchor, real video recording review, contextual workspace and ASS comparison found no directly equivalent ASS-specific Observation; existing design-to-implementation fidelity Observation remains distinct. This is not Canonical promotion or authorization for app code changes.
