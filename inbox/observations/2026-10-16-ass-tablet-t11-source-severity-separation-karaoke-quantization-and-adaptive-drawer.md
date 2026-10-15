# Observation / Design QA — ASS tablet T1.1 provenance semantics, Karaoke quantization, compact drawer

Date: 2026-10-16
Status: Observation; user review pending; not Canonical
Project: 11576865/ASS-Workbench-Android
Figma: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Previous T1 Case: `inbox/cases/2026-10-16-ass-tablet-t1-figma-task-semantic-seven-screen-prototype.md`

## Source symptom and repair (verified in editable Figma)
The initial 7-frame tablet T1 concept was rejected as not yet polished enough ('差一点，优化'). On inspection three concrete, repeatable design problems were found:
1. Normal ASS Event parameter *provenance* used the exact amber background as unsaved warnings. A valid Event override looked like a hazard. The source/effective value model also conflated an edited draft with saved raw text. Introduced two scoped COLOR variables `color/sourceEventBg = #292D49`, `color/sourceEventText = #B9B5F3`; used those for `Event \pos`, `Event \fs`, `Event \t`, `Event-local`, and source receipts, preserving amber for warning/draft status, blue for Style provenance. Inspector now labels draft values separately from stored Raw ASS.
2. The Karaoke design fixture used segment durations `[180,210,150,225,180,165,250,240]` ms. These summed to 1600ms, but independently rounding `225ms→\k23` and `165ms→\k17` yielded **161 centiseconds**, not 160. The edit inspector also showed selected syllable `值` beginning at 765ms, while actual cumulative offset had been 765ms from imprecise segments. Fixed the design fixture to `[180,210,150,220,180,170,250,240]`ms (exact `\k[18,21,15,22,18,17,25,24]`, sum=160cs=1600ms); selected `值` now starts at `760ms`. Updated both literal labels and visible segment geometry. **This is a Figma design fixture inconsistency, not evidence of a production Android parser bug.**
3. A 1440×900 three-region composition does not preserve comfortable touch geometry at narrower tablet width. Added true editable 1024×768 compact screen `16:2` and separate event drawer `18:2`. Primary editing frame retains video/transport/shared timeline and source inspector; event list becomes explicit 354px drawer instead of a permanent third column. The compact inspector was recomposed to X/Y dual inputs, alignment row, and size/font pair with 44px editable fields; source chips are **not** treated as action targets. Standard action buttons are 45–50px tall. Real screenshot review caught an overlapping bottom timeline/footer and missing lower inspector buttons in the first draft; repositioned media/transport/timeline, constrained the footer to center work area, and rechecked screenshot.

## Interaction truth / model boundaries
- Compact view and drawer have ON_CLICK prototype links for open/close, current #39 selection, navigation to existing task screens and write-review. Other event rows are intentionally **display only**, explicitly annotated to avoid falsely suggesting that selecting #36, #37, #38, #40, or #41 updates the selected document.
- Compact prototype linking to another 1440×900 task demonstrates navigation, NOT verified responsive implementation of all nine screens.
- Video and waveform remain *illustrated reference geometry*, not real media or libass visual evidence.
- Confirm/save actions remain nonfunctional prototype artifacts; no Android production branch or behavior was changed.
- Neither T1 nor T1.1 has been accepted by user as final. **Do not declare design freeze or native parity.**

## Verified checks
Figma `use_figma` read-back reported **nine** top-level editable tablet frames: seven 1440×900 + two 1024×768; 20 local color variables; 66 reaction-bearing prototype sources; all five compact edit fields measured 44px in height; Karaoke subtitle `\k` values checked to sum 160cs with displayed selected offset 760ms. Captured Figma screenshots for main, Karaoke, compact main, compact drawer; fixed clipping and source-state visibility after inspection.

## Reusable guardrails to test (not normative yet)
- A design review should cross-check the independent dimensions: *value provenance* (Event, Style, Raw), *state severity* (warning/blocker), and *transaction state* (draft/saved); avoid one color meaning all three.
- An ASS Karaoke UI fixture must use integer centiseconds as the canonical source if showing `\k` values, with displayed milliseconds and cumulative offsets derived from those integers. An individually rounded textual `\k` tag can violate the declared full-phrase duration.
- Compact tablets should test touch target sizes, navigation discoverability and nonoverlapping content at the **actual device-size frame**, not rely on scaling a desktop-oriented layout. A background scrim must not hide the real input/confirmation area unintentionally.
- Do not add prototype reactions for actions which would falsely claim document mutation; note representational boundaries.

## Deduplication
Queried UIGS-Foundry (same turn) for `ASS Workbench karaoke centisecond inconsistent syllable 225ms`, `ASS tablet compact adaptive object drawer Event source color warning`, `ASS Tablet T1 Figma task semantic seven screen`. The prior T1 case was found; no exact record of quantization/source-color correction or 1024×768 interactive compact drawer. This Observation extends, not supersedes, that Case. No Canonical files changed.
