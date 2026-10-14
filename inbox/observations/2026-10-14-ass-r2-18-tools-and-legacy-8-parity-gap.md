# Observation — ASS Workbench R2 concept lacks documented capability parity with legacy UI

Date: 2026-10-14
Status: Observation / review of conceptual UI only; NOT a reproduced product defect, NOT an approved Canonical change.
Project: 11576865/ASS-Workbench-Android
Subject: User-supplied/assistant-generated R2 concept drawing with three UI states: primary video-first workbench, per-field provenance view and write-review view.

## Review question
User asked whether the NEW UI fully integrates ALL OLD UI features. Answer: not demonstrated. The image supports some mainline flows, does not contain a traceable 18-tool route inventory and cannot prove interactive operation or preserved state. Visual absence alone does not prove that source code lacks a feature.

## Legacy capability directory from 2026-10-14 engineering report p.6
- SUBTITLES, TEXT, EVENT
- TIMELINE, FRAMES
- STYLE, POSITION, VECTOR_CLIP
- EFFECTS, KARAOKE
- FONTS, FONT_REQUIREMENTS, QC, COMPATIBILITY, DIAGNOSTICS
- BATCH, PROJECT, CAPABILITIES

R2 drawing: event list, selected Event, video, geometry handles, timeline and source/write inspector explicit; shared Style editing, specialized frames, vector clipping, karaoke, font evidence, QC, compatibility, diagnostics, batch audit, project resources and capability directory not individually specified. An unlabeled '工具' dropdown is an affordance, not evidence of those workflows. UI concept has only top-level task links 正文 / 排版 / 时间 / 效果; no exact full capability mapping.

## Legacy historical presentations
2026-10-13 41-page synthesis p.18 documents non-equivalence for CANVAS, PAGER, TOOL_INSTANCES, PRECISION_LENS, GLASS_LAYERED, SUBTITLE_OBJECT, EDGE_BOOKMARK, TIMELINE_DOCK even under contemporary FIXED/SPATIAL. Therefore a fresh R2 drawing must not assert inheritance by renaming UI modes or putting a generic layout button in the top bar. Examples: four-edge bookmark, surface docking/tab grouping, multi-instance bindings, semantic zoom/recall, precision lens, transparent audio and other spatial affordances require independent routed scenes and evidence.

## Reusable scoped lesson
A *new screen* may be a visually improved task projection without full **capability parity**. For each stable capability ID require user task -> UI Host/task/tool invocation -> focused target/binding/write scope -> actual behavior -> persistence/undo -> automated evidence -> device evidence. Add explicit unsupported / not drawn / planned / implemented / verified distinctions; never assign coverage scores from static screenshots. A capability need not be always visible, but must be discoverably reachable without identity or draft loss.

## Limit
No R2 Android code, exact-head Native screenshot, validated runtime test or 240 item-by-item audit is produced by this conversation. The old 240 ledger's 51/108/79/2 snapshot (2026-10-03) is not a current R2 coverage percentage. The user has not approved this concept as a functional-completeness baseline.

## Dedupe
Foundry searches for 'ASS UI R2 mockup 18 WorkbenchTool coverage missing advanced panels', 'capability parity cannot be inferred from tool navigation or schematic UI', and 'ASS legacy 8 presentation modes 18 tools R2 layout review' found no exact record. The general principle (capability parity across Hosts) already exists in the 2026-10-13 engineering report and the 2026-10-14 R2 layout candidate. This Observation records the **particular R2-to-18/legacy-8 audit gap**, not a new Canonical requirement.

## User-confirmed direction and execution tracker (2026-10-14)

User clarified the prior open-ended design audit into an explicit product requirement: **only two production-selectable UIs** (default main/FIXED and independent complete infinite canvas/SPATIAL), while **every actually implemented capability from earlier interfaces must have a visible, executable entry in at least one**. The eight retired layouts are not to return as independent UI choices. The source reality of former behavior must be audited, not inferred from 240 experimental status labels.

Current checked product `main` already has:
- `UiVariantRegistry.entries = [FIXED, SPATIAL_EXPERIMENTAL]`; archive names decode to the canvas (compatibility route, not proof of behavior).
- `WorkbenchToolCatalog` enumerates all 18 persisted tool IDs.
- `WorkbenchTaskBar` has grouped tasks, contextual tools and a tool directory button.

Outstanding capability-consumer gaps are documented in `docs/MULTI-UI-CAPABILITY-MIGRATION-2026-10-11.md` and include unconsumed historical docking/minimized/tabGroup state, full four-edge panels, and GlassToolWindow material behaviors. These are source-grounded migration questions, NOT all proven functioning in current Native main.

Concrete product execution issue: [ASS-Workbench-Android #146](https://github.com/11576865/ASS-Workbench-Android/issues/146), containing 18-tool inventory, eight historical interface capability families, Host routing, explicit entries and validation gates. The issue is an **implementation tracker only**: no new product code, tests or verified Native screenshots were delivered by this turn. `FIXED / SPATIAL` shared canonical domain does not make them one visible UI; the second remains its own complete spatial presentation.

Intake treatment: update this existing Observation rather than duplicating its capability-parity lesson or promoting Canonical. User confirmation upgrades the *product requirement authority*, not its implementation evidence.
