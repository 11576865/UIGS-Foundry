# Case: ASS UI v6 uses one temporal model for edit, scrub, playback and reversible prototype commit

Date: 2026-10-13
Status: Case / Browser-verified prototype, **not Android production evidence**
Product context: 11576865/ASS-Workbench-Android
Source artifacts (conversation-local):
- /mnt/data/ASS_Workbench_UI_Prototype_v6.html
- /mnt/data/ASS_Workbench_UI_Prototype_v6.zip
- /mnt/data/ASS_Workbench_UI_v6_真实界面预览.png
Earlier observations / bugs:
- inbox/bugs/2026-10-13-ass-v5-effects-prototype-semantic-binding-and-commit-gaps.md
- inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md
- inbox/cases/2026-10-13-ass-v5-temporal-curves-precision-geometry-and-responsive-tools.md

## User task / decisions
The user requested continued modifications after a v5 UI review found semantic and control-grammar errors: unsupported confidence in curves, \\kt confused with \\k-duration mode, repeated fixed CSS animation unrelated to edited parameters, effects not written to formal Undo history, cramped touch handles, excessive explanatory text and category confusion. The owner principally uses an Android tablet, with phone as a secondary responsive case. This work retained the two-Host distinction (FIXED main / SPATIAL_EXPERIMENTAL separate).

## Applied prototype implementation
1. Rebuilt the Effects pane around one preview, shared 0–3300ms ruler, alpha/fade and scale/transform tracks, visible and wider drag handles, two parameter curves, explicit numeric fields, bounded coarse sliders, and an editable target point on the scale curve.
2. Removed the unrelated looping CSS animation. Scrub and requestAnimationFrame playback now sample the same `motionValue(t)` function for graph readout, preview subtitle alpha/Scale X and the shared playhead. A separate simplified Karaoke syllable highlighter uses the same scrub time; it is explicitly a demonstration, not libass.
3. Removed \\kt from the mode dropdown. Modes \\k/\\kf/\\ko supply durations; a separate optional \\kt onset control demonstrates event-relative centisecond start offsets, with syntactic preview showing both time origins. This is not a general ASS parser/writer.
4. Added per-Event `fxDrafts`, source-preserving structured `fxCommitted` data in the demo Event object, deep document history snapshots for effect commit, Undo/Redo, discard, Event switching, and refusal of conflicting batch preview/commit. The prototype deliberately does **not** insert effect tokens into arbitrary unknown Raw ASS (would require safe span ownership and real renderer acceptance).
5. Increased motion and Karaoke pointer-hit zones to 36×44 CSS px; touch size in native Android dp is not inferred. Compact view uses task switching and scrollable controls; portrait tablet gains preview/curve height. Action footer stays visible while internal area scrolls.
6. Brought primary task names closer to their layer: main tab “检查” (opens QC; Fonts/etc in subtools), “批量” (PROJECT remains available from global engineering entry), whereas experimental Host is global.
7. Retained icon long-press descriptions instead of permanently large labels, and added minimal state-local transitions with reduced-motion media-rule support.

## QA (executed)
Headless Chromium/Playwright using HTML set_content, not Android:
- Main suite: 50/50 passed at 1440×850, 1280×800, 800×1280, 390×820, 360×780, checking no JS exceptions, coherent layout / no horizontal overflow, edit controls, 18 searchable tool entries, graph manipulation, Undo/Redo, kt onset, separate spatial Host.
- Extended suite: 23/23 passed, including alpha CSS 0 at t=0, alpha=1 at t=700ms, requestAnimationFrame advances sample time, slider input updates numeric and label before blur, effects draft survives task and Event changes, batch preview refuses dirty effect target, discard restores committed baseline, Karaoke duration redistribution preserves 330cs, 36×44 hit targets and commit reachability across sizes.
- Five authentic Chromium screenshots and composite review generated; zip integrity checked. Demo-state semantics are not equivalent to native libass or a deployed APK.

## Remaining limitations
No actual mpv/libass or VSFilter render, arbitrary ASS override parsing or \\t nested-span mutation, real typed Gradle/Compose integration, real Android IME/gestures/OEM behavior, MKV Bridge saving, output roundtrip, physical stylus ergonomics, TalkBack or timed task usability acceptance. CSS preview could still depart from true ASS animation interpolators. Five screens in composite are actual browser renders rather than image-generated concept mockups.

## Reusable lessons / non-Canonical
A curve that visually looks editable must either support direct manipulation with visible readouts or be clearly labeled analysis-only. An editor's sample value, playhead, displayed curve and playback need to consume a common temporal model. Input-type correctness (duration vs onset, scalar vs interval, coarse slider vs exact numeric) is a domain matter, not decoration. Scrub/play temporal agreement and formal reversible commit must be tested as stateful traces. In portrait tablet, reallocate surplus space to primary preview and graph instead of leaving unused viewport height. Keep editability claims scoped to the verified artifact.

## Dedupe
Foundry queries: 'ASS v6 temporal semantic kt onset vs duration draft undo preview'; 'ASS prototype v6 same time model slider graph playback'; 'effect compiler demo mode current scope'. No equivalent case found; v5 Bug and control-grammar Observation are related prior evidence.

No Canonical update; Android production repository unchanged.