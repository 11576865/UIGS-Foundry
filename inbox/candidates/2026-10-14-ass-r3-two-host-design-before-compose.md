# Candidate — ASS Workbench R3 two-host reviewable layout before Compose implementation

Date: 2026-10-14
Status: Candidate / DRAFT VISUAL DESIGN — user review pending; **not** a native Android implementation or accepted specification.
Project: 11576865/ASS-Workbench-Android

## Context and binding sequence
User explicitly corrected a repeated planning/implementation-order mistake: **make R3 designs first, then implement**. R2 was a review-only basis; do not call R2 implementation complete or treat #147's localized "空间功能" menu as the requested main UI redesign. Product scope stays ONLY two independent UIs: FIXED professional editor and SPATIAL independent infinite canvas. Previously implemented interactions from retired UI presentations must remain callable in at least one Host; no restoration of eight separate UI products.

## Actual R3 deliverable this turn
Four locally created editable Inkscape SVG screens with matching 1600×960 PNG previews, plus overview and README in a verified ZIP in the current conversation's sandbox (file links are session-local; not permanent repository evidence):
1. R3 FIXED main: Event list, aspect-constrained media, time dock, context inspector, field provenance, explicit write target, uncommitted preview/commit and a discoverable professional tools entry.
2. R3 independent SPATIAL: world-grid board, camera/overview/recall, media node, subtitles, Style, transparent waveform, node chrome, optional bookmark rails and live time dock. It is an independent UI, not a subsection of FIXED.
3. R3 professional tool catalog: all 18 stable `WorkbenchTool` identities organized into understandable tasks. Appearance of an entry in a design image does not prove actual Kotlin execution.
4. R3 provenance/write review: `Event \\fs48` overrides Style baseline; a draft proposes `\\fs52` for Event #39 only, shared Style untouched, explicit source revision preflight and Raw diff. Complex `\\r/\\t` need time/range dependent provenance handling in production.

SVGs verified parseable by lxml and rendered using installed Inkscape, output PNGs visually inspected. Media derived from prior R2 concept and cropped to exclude old burned-in subtitle; it is a static placeholder, not a live libass or device screenshot.

## Implementation gate
User review/acceptance of R3 design must precede any new Android UI implementation derived from it. Keep #147 as separate Draft off-main work until its relation to R3 implementation is decided. No new production Kotlin code was changed in this R3 design turn.

## Remaining design scope
R3 four screens are a high-fidelity initial architecture, **not a claim that every specialist tool panel/flow has been drawn**. Need detailed flows for editing text, time, effects/Karaoke, frame tools, clip node editing, fonts, QC/compat/diagnostics, batch review, project resources and spatial Surface behavior, as product requirements and implementation evidence warrant. Do not infer every historical 240 ledger item already implemented. Native acceptance separate.

## Dedup
Foundry searches for 'ASS Workbench R3 dual host layout design before Android implementation', 'ASS R3 design review four screen fixed spatial 18 tools provenance receipt', and 'R2 to R3 UI concept artifact branch before compose' showed no exact R3 record. Existing 2026-10-14 R2 layout candidate and per-field provenance candidate cover the predecessor patterns, but not this user-corrected R3 sequence and paired independent-host visual deliverable. Canonical unchanged.
