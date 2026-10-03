# Candidate: Separate representability, rendering, structured authoring, and composition workflow

Status: candidate
Date: 2026-10-03
Domains: editor-architecture, authoring-tools, UI, validation

## Summary

A format-capable editor can appear to "support" an advanced effect while still lacking a practical authoring workflow for it.

For complex authored output, distinguish at least four capability levels:

1. **Representability / preservation** — the underlying document model can store the syntax or data without destructive normalization.
2. **Rendering / preview** — the authoritative or reference renderer can display the result.
3. **Structured authoring** — the UI can edit the relevant primitive parameters without requiring raw syntax.
4. **Composition workflow** — the product can efficiently coordinate the multiple objects, layers, timing segments, duplicated variants, and reusable templates needed for the final effect.

A fifth level may exist for effects-heavy domains:

5. **Automation / templating** — repeated per-syllable, per-object, or multi-layer structures can be generated from reusable rules rather than assembled manually.

## Candidate rule

When evaluating or reporting support for an advanced authored effect:

- do not collapse "can parse/render/preserve" into "can author comfortably";
- identify which primitives have structured controls and which still require raw editing;
- identify whether the target effect is a single-object parameter change or a multi-object composition;
- evaluate duplication, layer management, timing coordination, and reusable-template support separately from primitive tag coverage;
- use an end-to-end reference effect as an acceptance fixture before calling the workflow complete.

For UI planning, prioritize the missing composition bottleneck rather than adding more isolated parameter controls when the primitives already exist.

## Evidence

ASS Workbench Android current main can preserve and render advanced ASS, and exposes structured controls for geometry/transform primitives such as scale, X/Y/Z rotation, shear, blur, alpha, fades, and karaoke timing. It also has a numeric keyframe author that compiles multiple keyframes into consecutive `\\t` segments.

However, a karaoke-style reflection/flip effect observed in a real subtitle sample is not merely one parameter. It is plausibly composed from a normal text layer plus one or more transformed copies with separate position, scale/rotation, alpha/blur/clip, timing, and karaoke progression. The current toolset can author many of those primitives, but it does not yet constitute a mature multi-layer FX composition or templating workflow comparable to dedicated karaoke-effect authoring.

## Provenance

- project: 11576865/ASS-Workbench-Android
- current main observed: 2026-10-03, after PR #80
- evidence level: current source inspection + concrete rendered-effect decomposition
- deduplication: searched UIGS-Foundry for equivalent representability/rendering/authoring/composition distinction; no direct duplicate found
- status rationale: reusable editor-capability evaluation heuristic; not yet validated across multiple authoring domains

This is a Candidate only. It is not Canonical.
