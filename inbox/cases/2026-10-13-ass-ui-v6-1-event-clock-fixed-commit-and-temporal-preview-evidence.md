# Case: ASS UI v6.1 event-relative temporal editing, persistent action bar and responsive validation

Date: 2026-10-13
Status: Case / standalone browser-prototype evidence; not native Android production acceptance
Product: 11576865/ASS-Workbench-Android (independent UI design prototype)
Related Bug: inbox/bugs/2026-10-13-ass-v5-effects-prototype-semantic-binding-and-commit-gaps.md
Related Case: inbox/cases/2026-10-13-ass-v5-temporal-curves-precision-geometry-and-responsive-tools.md

## Trigger and specific issue
Continuing the user's v6 animation UI design implementation, the first inspected 1280×800 screenshot revealed a critical usability defect: the effects Commit/Discard controls were below the inner scroll viewport rather than visible at the bottom. Subsequent source review found the entire effects time ruler, playback scrub slider, timeline percentages and graph width hardcoded to 3300ms; switching to an Event with a different duration therefore misrepresented the time domain. A first code patch also accidentally set HTML range max as the literal text "fxEventMs()", which pushed the slider thumb to the end while displaying 750ms. Real screenshot and DOM inspection caught it before packaging.

## Changes
- In independent HTML prototype v6.1, move Commit/Discard controls outside the scroll container; flex-shrink-0 footer is always in the bounded effects workspace on tablet and phone. Contextual action remains visible with a dirty/clean state indicator.
- Derive current Event duration from its committed start/end centisecond timestamps. Use this shared duration for timescale ticks, scrubber max/position, Fade/Transform segments, graph cursor, boundary drags, playback wrapping and precise-input constraints. In sample data Event #39=3300ms, Event #40=3100ms, Event #37=2600ms.
- Scale demo Karaoke durations to the active Event duration in centiseconds while distinguishing \\kt onset offsets from \\k, \\kf and \\ko durations. This remains a **demonstration** of a model, not a full ASS token writer.
- Update Scale X slider live: numerical input, \\t preview token, graph path, target handle and range label follow the same state. Playback time samples update CSS preview, readout and curve indicator together.
- Explicitly label fixed approximately 42ms step controls as simulated instead of claiming real VFR PTS. No actual video or libass was loaded.
- Preserve Event effect drafts and explicit Commit -> Undo -> Redo within the prototype. Native Android and canonical ASS engine were not modified.

## Local acceptance evidence
Headless Chromium / Playwright, real browser screenshots at 1280×800, 800×1280, 390×820, and additional task cases.
- 50/50 original v6 effect/browser checks passed.
- 57/57 targeted extended checks passed: pinned footer in five device sizes, correct bounded input ranges, selected-Event duration and Karaoke totals, slider/curve/token synchronization, playback progress/opacity readout, Apply/Undo/Redo, cross-Event dirty draft preservation/discard, 18-tool discovery and experimental Host isolation inherited from core battery.
- Additional touch-pointer >520ms help tooltip on Save did not trigger Save on release/click, and a subsequent ordinary tap performed the demo action.
- Six rendered screenshots stored in local deliverable bundle plus check JSON. A viewport screenshot detected the intermediate invalid range max patch, which was fixed and retested.
- Artifact: /mnt/data/ASS_Workbench_UI_Prototype_v6_1.html
- Bundle: /mnt/data/ASS_Workbench_UI_Prototype_v6_1.zip
- Screenshot index: /mnt/data/ASS_Workbench_UI_v6_1_真实布局预览.png

## Limitations / future action
No native Compose, actual font shaping, real mpv/libass, source parsing of arbitrary nested ASS overrides, exact frame-PTS stepping, file save, recovery, MKV bridge or device OEM stylus/touch tests. Current result is prototype behavior and design evidence only, not a released Android implementation. 107 checks are two bounded script suites, not 107 independent product requirements. UI design aesthetic and task throughput require real user/device evaluation.

## Reusable lesson
An apparently complete professional timeline can still violate control semantics when its displayed value and actual HTML range/domain diverge. Assert both numeric time and real thumb/ruler geometry after changing Event. Keep irreversible or stateful authoring Commit/Discard always directly visible while secondary controls scroll. Do not label a fixed millisecond increment as a verified VFR frame operation.

## Dedupe / governance
Foundry searches: "ASS v6.1 event relative timeline pinned commit", "effect controls document undo browser prototype", and "karaoke per event duration in responsive editor". Related prior v5 Bug and v4/v5 Cases exist; they do not contain this v6.1 real screenshot reproduction, event-duration fix and sticky footer acceptance.
No Canonical promotion. No production ASS source modification.
