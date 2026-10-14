# Observation — ASS Workbench R3 dual-UI design deliverable and review boundary

Date: 2026-10-14
Status: Observation / R3 concept prepared; PENDING user review; not implemented in Android; not validated as a native UI.
Project: 11576865/ASS-Workbench-Android

## Context
User reiterated the sequence of work: evolve the prior pending-review R2 UI to R3 **before** implementing UI changes, with only two separately presented products: FIXED main workbench and SPATIAL independent infinite canvas. Do not substitute tool menu patches for a complete UI design pass.

## Concrete design deliverable
A local editable R3 package was built and verified in the user conversation:
- 01 FIXED: landscape Event navigator, compact video reference without redundant preview title, timeline, per-field provenance, explicit Event-local write scope and Raw.
- 02 SPATIAL: independent spatial Host with world nodes, separate video/ASS renderer surface, audio waveform, tools, bookmark layers, discoverable navigation, constant time dock. The screen is a proposed UI, **not evidence** that every historical spatial feature already has a production consumer.
- 03 Professional tool directory: all 18 stable `WorkbenchTool` IDs from source; CAPABILITIES is the directory role, not another domain editor.
- 04 Source + commit: detail of Event `\\fs48` overriding Style Fontsize 36, Draft `\\fs52`, explicit Event write target, Raw diff and preflight checks.
The package contains 4 SVGs, 4 PNGs, an overview and README. All SVGs were checked with strict XML parsing; user-visible bitmaps were inspected. Images use raster footage as a placeholder; vectors/text remain editable.

## Transferable lesson
**Deliverable-state boundary:** a coherent four-screen editable UI design is stronger evidence of intent than an isolated illustrative hero screenshot, but it does *not* certify implemented workflows, full 18-tool operation, legacy 8-presentation feature parity, Compose geometry, a native screenshot, or device acceptance. Correct next gate is explicit user review, then Compose implementation against the accepted revision. Capability migration is tracked separately under product Issue #146; PR #147 remains Draft and is not the R3 implementation.

The user requested the MagicPath tool; MagicPath refused the design code session with `EXTERNAL_AGENT_API_QUOTA_EXCEEDED` (50/50 used). A tldraw board was created but its editor was not open for drawing. The actual completed artifact is the **locally verified SVG/PNG package**, not a hosted MagicPath, Figma, or tldraw design canvas.

## Dedupe
Queried Foundry for 'R3 ASS Workbench FIXED SPATIAL four design screens', 'R3 UI concept event tool directory provenance commit source', and 'ASS design before implementation two Host complete design deliverable': no exact R3 receipt. Earlier R2 Candidate and ASS capability parity Observations remain in force. Register this *bounded R3 design artifact Observation* only; do not change Canonical.

## Outstanding
1. User design acceptance/changes: main workbench density, video bounds, SPATIAL tool arrangement, inspector semantics.
2. Additional professional workflow screens (raw Event, Style shared edit, Karaoke, Vector Clip, QC, font requirements, batch) may be needed before product-wide design coverage can be certified.
3. Android implementation and CI/device evidence after design approval; no automated Code UI claims from SVGs.
