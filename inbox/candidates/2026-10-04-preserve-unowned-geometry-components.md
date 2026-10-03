# Candidate: Preserve unowned geometry components during semantic transforms

Status: candidate
Date: 2026-10-04
Domains: semantic-editing, geometry, authoring, non-destructive-transforms

## Summary

A semantic transform should change only the geometry components it explicitly owns. Normalizing or clamping unrelated coordinates while applying an orthogonal transform silently changes author intent and can move valid off-screen geometry.

For example, a reflection operation that owns only a Y offset should not clamp X coordinates merely because they fall outside the current PlayRes bounds.

## Candidate rule

1. Identify the exact geometry components owned by the operation.
2. Preserve all unowned components byte-semantically or value-semantically unless the user explicitly requested normalization.
3. Do not clamp unrelated axes to viewport bounds as a side effect of applying an orthogonal transform.
4. If the owned component itself would exceed an operational constraint, either preserve it when the target format allows it or fail explicitly; do not silently rewrite another component to keep the result visible.
5. Add regression coverage with off-screen / oversized coordinates so viewport assumptions cannot re-enter through helper functions.

## Evidence

ASS Workbench Android PR #93 generates reflected ASS Events by shifting vertical geometry. The implementation was clamping X values of `\pos`, `\move`, and `\org` to `PlayResX` even though reflection authoring did not own horizontal position.

That meant a valid source such as `\pos(-120,1100)`, `\org(2040,1200)`, or an off-screen `\move` path could be silently snapped back toward the current PlayRes while only a reflection offset was requested.

The correction now preserves explicit `\pos`, `\move`, `\org`, and rectangular `\clip` geometry exactly apart from the requested Y offset. It also stops clamping inherited-margin anchors during explicitization. Spatial fade is different because its mask is intentionally screen-space: if the resulting reflection anchor is outside the picture, the compiler fails explicitly instead of moving the anchor into view.

Regression coverage includes negative and beyond-PlayRes coordinates, translated clips, moving Events, and fail-closed spatial fade for an off-screen anchor.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #93
- evidence level: concrete semantic mutation bug + implementation correction + regression tests across explicit and screen-space geometry
- deduplication: searched UIGS-Foundry for unrelated-axis clamping / preserving unowned geometry / semantic patch ownership; no direct duplicate found
- status rationale: reusable semantic-editing principle; not promoted to Canonical from a single project observation

This is a Candidate only. It is not Canonical.
