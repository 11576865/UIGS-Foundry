# Decision / Case — Freeze only FIXED Tablet UI V1.1, defer SPATIAL UI

Date: 2026-10-16
Status: **Approved design-scope freeze for FIXED**; Android implementation/device verification Pending; SPATIAL visual design Deferred, preserved as historical reference
Figma file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Implementation baseline page: `85:2` — `ASS Workbench · FIXED 主UI V1.1 · 冻结实施基线 2026-10-16`
Baseline screen: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=85-3
Earlier integrated V1.1 including SPATIAL remains in page `56:2`.

## User decision
"算了，暂时不做无限画布，先把主UI固定下来，后面再做无限画布UI"

This updates the *previous* project-specific V1.1 decision to include SPATIAL in the implementation target. It authorizes a narrowed FIXED-only UI design freeze now. Do **not** infer approval to delete existing canvas code/models, old Figma content, project document state, saved SPATIAL settings or architectural commitments.

## Actual design change and verification
Created an independent Figma PAGE `85:2`, non-destructively cloned exactly four editable FIXED screens from prior V1.1. Frame identities on this new page:
- `85:3` 1440×900 default professional subtitle editor
- `85:390` 1440×900 specialist timing workspace
- `85:942` 1024×768 compact editor
- `85:1237` 1024×768 compact subtitle grid drawer

Across all four frames, set the SPATIAL tab `visible=false`, removed inherited prototype reactions pointing into the old page or the deferred SPATIAL branch, then connected only five safe local view-navigation actions: default↔timing, compact↔grid drawer and active #39 row back to compact. Current saved-media, waveform and subtitle placeholders are design fixtures; no Android code changed.

Figma structural readback confirmed exactly four FIXED frames, all with hidden SPATIAL tabs and only the five intended prototype links. Actual screenshot of the cloned 1440×900 default screen was captured and visually inspected; subtitle grid, media, waveform/cue track, bilingual draft and source-aware inspector remain consistent.

The prior eight-screen integrated V1.1 page `56:2` (with SPATIAL overview/focus/compact prototypes) and older V1/T1.1 pages remain **unmodified and accessible**. The new page is the sole current FIXED implementation design baseline to hand off; do not use older SPATIAL diagrams as a substitute for their historical functional contract.

## Scope of "freeze"
Freeze visual composition, FIXED task navigation and responsive screen hierarchy for starting Android delivery. Do not claim native implementation is already accepted, Figma link clicks perform actual mutations, or every professional tool has a fully designed flow. Usability findings from real tablet operation can justify scoped revisions against this recorded baseline.

SPATIAL UI and incomplete canvas interaction presentation are **deferred**, not removed or silently discarded. No canonical UIGS specification should be changed from this single project decision.

## Engineering handoff gates
1. Implement/compare the current FIXED main editor and specialist timing view at 1440×900/1024×768, with actual IME and touch target evidence.
2. Prove Focus, Selection, Event/Text draft, saved Raw and explicit write-review semantics while switching task panels and opening drawers.
3. Verify actual video, libass subtitle overlay, waveform/PTSes, frame alignment, media controls, session restart and Undo; static Figma visuals cannot validate these.
4. Maintain existing persisted UI mode and spatial domain artifacts without deletion; restoring the SPATIAL UI workstream later will require separate design acceptance based on prior project documents and actual host capabilities.

## UIGS Intake / dedupe
Searched Foundry for the exact FIXED-only decision, deferred SPATIAL and four-screen V1.1 baseline; no precise earlier case. Related earlier `inbox/cases/2026-10-16-ass-tablet-v11-approved-design-baseline-spatial-integration.md` is historically true for its time but **superseded in current implementation scope** by this more recent explicit user decision. This case does not erase prior history, change Canonical or assert SPATIAL functionality was removed.
