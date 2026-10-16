# Case — ASS Workbench Tablet V1: integrated initial product UI after design-review drift

Date: 2026-10-16
Status: Design Case; **V1 initial interface drawn; Pending owner aesthetic/task acceptance and native implementation**
Product: 11576865/ASS-Workbench-Android
Figma: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
New first-version page ID: `43:2`, name `ASS Workbench · Tablet UI 初版 V1`

## Owner correction
Owner stated: "偏了，我们要设计一个初版UI". Recent work had accumulated many isolated Candidate/Observation/Figma audit and interaction screens without a coherent *initial product interface*. This turn immediately moved to product-facing, integrated tablet UI authoring rather than more matrices or candidate audits. Prior instruction "改动要谨慎" remains in force, so old T1.1 frames were retained.

## Grounded constraints
- Tablet only; 1440×900 baseline and 1024×768 compact landscape.
- One document/task core with FIXED and independently entered SPATIAL Host.
- Current `WorkbenchToolCatalog.kt` contains 18 stable Tool IDs, `TEXT` as first-class WorkbenchTask, `STYLE/POSITION` support Pinned Event and duplicate whereas `TEXT/EFFECTS` do not.
- Maintain clear source/target, Event draft vs saved Raw/Style, approval prior to write, QC as lightweight status with optional detail.
- Media visual is editable placeholder, NOT actual libass rendering or live playback.

## Actual Figma-native product views (not isolated analysis)
- `43:3` — FIXED main editor (1440×900): global project actions; persistent six-task rail incl TEXT; Event list with #39 selection; centralized media preview/playback/actual Event Text draft/shared PTS audio waveform+timeline; compact Event metadata inspector and QC small status.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=43-3
- `45:2` — integrated searchable 18-tool directory overlay (1440×900), three groups; only grounded implementation exemplars routed, other tools visibly present without fabricated interactions.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=45-2
- `46:2` — SPATIAL (1440×900), same project chrome, bookmark rail, independent Event list and media instances, POSITION instance pinned #38 distinct from current Focus #39, persistent timeline Dock and recall.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=46-2
- `47:2` — actual 1024×768 compact tablet adaptation, Event list moved to drawer; video/text/timeline and concise source-aware inspector visible without clipping.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=47-2
- `48:2` — BATCH full-workspace task view (1440×900), scope → filter → transform → reviewed before/after timecodes (+200ms for #39/#40) → guarded commit.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=48-2
- `49:2` — compact Event list drawer state (1024×768), #39 selected and route to same compact main screen; other rows display-only to avoid fake changes.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=49-2
- `50:2` — Event #39 write-review overlay (1440×900), literal saved Before `{\pos(960,720)\fs48}世界依然值得凝视` vs candidate with punctuation, target Event Text only, shared Style unchanged, revision guard. Confirm is clearly demo/nonfunctional.
  https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=50-2

The new page has exactly **seven** editable Figma frames: five 1440×900 and two 1024×768; user-visible screenshot inspection performed on all seven (main before and after timeline repair, 18-tool overlay, SPATIAL, compact, BATCH, compact drawer, write-review). One visual clipping defect was caught in the first FIXED screenshot: timeline clips were hidden under the footer. Fixed timeline to begin at y=638 in the central region, height 154, with event tracks and waveform moved up; follow-up screenshot verifies full clips visible.

Created **17 view-only ON_CLICK prototype routes** for grounded scenes (FIXED↔SPATIAL, FIXED↔directory, TEXT→write review, directory→BATCH, compact↔drawer); no actual save, ASS mutation, Quick Fix or animation data writes are simulated as successes. The tool directory includes exactly **18 of 18 unique Tool IDs**. Existing Page 1 original nine T1.1 Frame IDs remain exactly `2:21,2:612,4:2,5:2,6:2,7:2,8:2,16:2,18:2`, verified by independent Figma page readback. The prior isolated candidate review page remains separate.

## Important boundaries
- This is the first coherent UI product baseline **for evaluation**, not a complete 18-task operational design, and not user-approved design freeze.
- In directory, some controls are presentation/discovery only. Selected individual Event #39 in compact drawer can navigate; other row click behavior is not simulated. Missing task details remain future design work.
- The Figma media background is a vector-drawn placeholder. Real Android video/ASS rendering, media PTS, IME, Save, content binding, exact state lifetime, gestures, app compatibility and device acceptance are NOT tested.
- No Android source, project data, Stable IDs, existing T1.1 prototype reactions or UIGS Canonical changes made.

## Reusable bounded observation
A series of well-audited standalone tool screens can fail the user's actual goal if the primary product layout still does not exist. When the owner asks for a "first UI", privilege an **integrated default workflow**, a coherent navigation/overlay system, a concrete compact viewport, and one expanded task example before making more audit/heritage matrices. Preserve source-backed boundaries and review real screenshots, then iterate the actual screen.

## Intake and dedup
Searched UIGS-Foundry for the precise V1 integrated seven-frame design, FIXED/SPATIAL/BATCH compact combo and T1.1 diversion correction; no exact duplicate. Related previous records (T1.1 source semantics, footprint matrices) remain distinct and have not been promoted to Canonical. This new record documents actual user-directed course correction and delivered integrated UI, not just a Candidate list.
