# Candidate — ASS 18-tool active/passive/hybrid authoring taxonomy (presentation-only)

Date: 2026-10-16
Status: Candidate / conceptual UI classification; Pending owner acceptance
Product: 11576865/ASS-Workbench-Android
Basis: app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt, and existing AdvancedQcPane.kt/AssLinter.kt and RuleBatchPane.kt examined during the related Figma phase 2.
Context: Owner asked "哪些是主动型，哪些是被动" after BATCH/QC candidate UI design.

## Terminology / important distinction

The repo’s real `WorkbenchToolGroup`, `ToolContextKind`, `WorkbenchTask`, `ToolDescriptor` are persisted/business-oriented taxonomy. The following is **not** an existing code field or an official repo classification. It is a proposed **dominant UI-behavior** taxonomy to assist information density and write safety.

Distinguish independently:
- **Initiation**: triggered by user vs automatically refreshed/contextual
- **Mutation**: reads/observes vs writes document/resources
- **Dominant job**: active editor (primarily produces edits), passive observatory (primarily inspects/explains), mixed (observes, navigates and/or conditionally writes).

A button press to run analysis is user-initiated but read-only. Passive/active must not be inferred from clickability.

## Proposed per-ID classification (all 18)
- **Active authoring (8)**: TEXT, EVENT, BATCH, STYLE, POSITION, VECTOR_CLIP, EFFECTS, KARAOKE.
- **Passive-first (4)**: FONT_REQUIREMENTS, COMPATIBILITY, DIAGNOSTICS, CAPABILITIES.
- **Mixed (6)**: SUBTITLES (browse/filter vs focus/selection/structure operations), TIMELINE (playhead/observe vs trim/drag), FRAMES (PTS inspection vs frame-align edits), FONTS (glyph/fallback observation vs import/bind/package), QC (lint is read-only; Quick Fix is explicit edit action), PROJECT (inspect resources/tracks vs save/export/writeback).

These classes describe dominant UI affordance, not limits on the subsystem. For QC, a conditional Quick Fix may mutate, so its report surface stays passive and its fix action should be clearly separated and guarded. For BATCH, preview is read-only, but the tool's *purpose* remains an editing transaction with scope, immutable review, explicit apply, and Undo.

## Reusable candidate (not Canonical)
1. **Passive surfaces**: compact contextual status/warnings with drill-down, rich provenance and actionable explanations on demand, not permanent heavy panels or fabricated edit controls; no automatic writes.
2. **Active surfaces**: explicit source target/binding, edit state, preview vs saved value, consequence and commit, Undo.
3. **Mixed surfaces**: explicit `Inspect → Proposed change → Review/Confirm → Apply → Re-check`; badge state and permission to write must never be conflated.
4. Preserve all 18 stable Tool IDs, original WorkbenchToolGroup and task identity; a presentation-only taxonomy must not force a registry migration or Host redesign.
5. Passive services can be computationally proactive/background while staying strictly non-mutating; 'passive' means side-effect semantics in this context, not CPU scheduling.

## Evidence and limitations
Source confirms each tool's description but **does not assign an official active/passive enum**. Actual implementation behavior differs by tool, and a later UI/interaction audit would be needed before imposing strict constraints. Some user actions in otherwise passive tools can change UI state (focus, filter, playback) without committing data.

## Dedupe
Queried UIGS-Foundry on 2026-10-16 for 'active passive tools interaction read only', '主动 被动 QC 批量 UI', and 'passive tool active affordance status inspection'; no exact prior finding. Existing T1.1 BATCH/QC design Candidates concern two screens and safe commit, not complete 18-tool classification. Do not modify Canonical based on this classification alone.
