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

## 2026-10-14 continuation — User-approved code-first R3 under strict visual matching requirement

User explicitly approved beginning Android code against the existing R3 design before further refinements and added a strong acceptance condition that the result must match the supplied reference. Treat this as **visual test gate**, not permission to claim a still-unrendered native screen matches the image.

Product **Draft PR #148**: https://github.com/11576865/ASS-Workbench-Android/pull/148 (branch `feat/r3-fixed-visual-layout-20261014`; latest observed SHA `22e8431703dffcaa0c6502e7cd8266a60229a0d3`). Distinct from partial entry-only PR #147; neither automatically merged.

Source changes introduced R3 only in FIXED expanded Host: navigator left; VideoPreview + real Timeline middle; movable FloatingToolContent right; video aspect first; external 48dp playback bar not obscuring subtitle glyphs; native 56dp app bar, 50dp task bar, dark navy/cyan palette; Event/Binding/Write Scope context header based on real Domain state. SPATIAL remains a separate selectable UI using shared Domain. Preexisting user-selected appearance overrides are preserved; new-install fallback switched to DARK. Narrow/IME policy uses preexisting fallback.

Technical correctness checkpoints: JVM screenshot-based geometry assertions for ratios 267/1600 and 427/1600, aspect 16:9 and alternate video ratios, available timeline minimums; Android instrumented compositor capture only when actual layout has expanded dimensions and semantic pane bounds. Those are newly added tests, **not executed local results**. GitHub Actions Android CI, Emulator Regression, Fontconfig were in progress for exact head when recorded; pending is not pass.

**Known remaining parity and visual deltas**: native screenshot comparison at a grounded 1600x960-equivalent viewport, all R3 interior tool and tab styling, right inspector per-field labels/dirty semantics, professional tool dialogs, Write Review page, SPATIAL appearance/legacy capability parity, embedded video's media frame source and player metrics. Don't count Stage-1 layout code as a completed R3 pixel match. Do not alter Canonical based on this observation.

Intake: append this bounded engineering continuation to the existing R3 evidence observation rather than creating a duplicate general UI redesign principle. Status remains **Pending Native Visual Acceptance and CI**.

## R3 follow-on source/acceptance update (2026-10-14)

Later PR #148 commits also (1) aligned 56dp app header and 50dp task strip to R3 drawing; (2) showed a wide ASS Workbench header and explicitly labeled host switch; (3) restored transport bar visibility when editing Position; (4) added real Event binding / write scope at top of wide inspector, not a speculative write target; and (5) committed `docs/R3-NATIVE-VISUAL-FIDELITY-CONTRACT-2026-10-14.md` with reference 1600x960 region bounds, navy/cyan sampled color tokens and exact staging gates. Latest known head `29a668087ca1ff705756f7f23cab273368c27594`. Android CI/Emulator/Fontconfig for this exact SHA were in progress at time of record; no green build, Native screenshot or device comparison claimed. R3 still Draft Pending visual fidelity acceptance and remaining specialized R3 pages. Single observation continuation; Canonical unchanged.
