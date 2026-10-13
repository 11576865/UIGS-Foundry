# Case: ASS HTML prototype v3 converts visual task-shell into safer editable workflow

Date: 2026-10-13
Status: Case / local browser-tested, **prototype-only**
Project: ASS Workbench UI Study 03
Related: inbox/bugs/2026-10-13-ass-offline-ui-v2-draft-loss-and-undo-contract.md
Related: inbox/tests/2026-10-13-ass-prototype-responsive-task-and-longpress-qa.md
Previous correction: inbox/observations/2026-10-13-ass-primary-fixed-vs-spatial-experiment-ui-taxonomy-and-tool-coverage.md

## Trigger
User requested continuation after receiving a critical review of offline ASS UI v2. That review discovered loss of uncommitted Raw text upon changing Event focus and broken Undo/Redo after Apply. User had also objected to uniform layouts, low fidelity to actual ASS catalog and SPATIAL_EXP incorrectly mixed with normal tasks.

## Artifact and scope
A **single-file, dependency-free** HTML/CSS/JS interactive design prototype was changed and shipped as ASS_Workbench_UI_Prototype_v3.html. FIXED has six task-specific layouts, SPATIAL_EXPERIMENTAL remains reachable only through the workspace/global setting selector, and the command tool directory covers all 18 persistent WorkbenchTool IDs. This is not a Kotlin/Compose change or a true ASS renderer.

## Behavioral changes
- Event-scoped Raw ASS draft map + field draft map for start/end/style. Focus changes, task switches, and Host switches preserve dirty fields and associated Event identity.
- Position X/Y transient changes are stored per Event separately from committed geometry, and can be applied or discarded.
- Apply creates history snapshot for formal text/time/geometry edits. Undo/Redo replay snapshots with a distinct document revision. Adding, copying and deleting Events use the same history path.
- Demo batch operation derives targets from actual Selection / filtered events / document instead of inventing 12 affected items. A preview locks the document revision and target IDs; operation executes as one Undo step. Uncommitted drafts in targets block preview and commit.
- Desktop Event and Inspector widths adjusted by draggable handles; mobile current Event context gives direct edit/timing shortcuts; portrait task tab row scrolls horizontally so the last tool is reachable; touching visible subtitle selects editing context.
- Tooltip gesture uses long press and suppresses synthetic click upon release; short tap still operates the tool.

## Local validation
Executed using offline HTML loaded into headless Chromium via Playwright:
- Main test: 46 passing checks for desktop 1440×850 and phone 390×820 including six FIXED layouts, the 18 tool directory, separate canvas Host, navigation, drafts, field commit, Undo/Redo, batch target/undo, touch longpress and mobile list-editor transitions.
- Supplemental test: 13 passing checks, including geometry draft across Focus change, geometry Apply/Undo/Redo, rejecting batch preview if a target Event has a dirty draft, resizing Event pane, reachability of last task tab at 360px, and tap-to-edit subtitle.
- Actual browser screenshots were captured for main/timing/studio/effects/resource/batch/experimental and phone. JS syntax check also passed.
- Preview imagery is **simulated SVG**, waveform is dummy generated visual and no libass, player, font-matching, video decoding, file save, or Matroska writeback were tested.

## Caution
The v2 artifact remains buggy; v3 demonstrates a corrected prototype contract only. Neither browser UI tests nor a successful screenshot prove the production Android app respects the same semantics, or that prototype batch token rewriting is safe for arbitrary ASS. Missing coverage includes native Android IME, TalkBack, OEM gestures, recovery after process death, real media and real ASS round-trip.

## Reusable lesson
A visual editor prototype should be tested against **stateful authoring task sequences**, not solely visual snapshots and discoverability. The minimum transition battery must include: dirty Event A → Event B → Event A; dirty fields → Host/task changes; Apply → Undo → Redo; batch preview → target revision mismatch; transient geometry → commit/revert; touch longpress → release without execution; mobile object selection → editable context; and retained direct access to scoped, safe write commands.

## Dedupe and governance
Queried Foundry for 'ASS offline v3 UI prototype draft undo batch browser test', 'ASS prototype geometry draft commit undo resize', 'ASS v2 draft loss bug'; no matching v3 tested Case existed. Existing v2 Bug remains a historical defect of its artifact; this Case documents the improved v3 independent deliverable rather than falsely closing the v2 defect.

No Canonical promotion; no changes to ASS-Workbench-Android source or production test contracts without user review and independent Kotlin/device acceptance.
