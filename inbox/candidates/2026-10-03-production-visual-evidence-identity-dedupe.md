# Candidate: Prefer stronger existing evidence over parallel duplicate UI capture states

Status: candidate
Date: 2026-10-03
Domains: operations, interface-grammar, reliability

## Summary

When closing Production Visual Evidence gaps, first resolve the target Surface against existing source-owned capture states. If a current capture already proves the same claim at an equal or stronger evidence level, extend or reuse that evidence instead of adding a parallel lower-fidelity capture with a second identity.

The goal is not to minimize screenshot count mechanically. It is to avoid multiple competing evidence authorities for the same product claim.

## Evidence

ASS-Workbench-Android PR #76 originally added four capture states:

- Canvas workspace;
- renderer-backed preview;
- Tool Instances workspace;
- synthetic Interaction Overlay.

While the branch was open, current main gained stronger dedicated evidence:

- `ASS.TOOL_INSTANCE_WORKSPACE.FIXTURE_LANDSCAPE` via `UigsToolInstanceVisualCaptureInstrumentedTest`, covering real ToolInstance binding plus floating-surface geometry;
- `ASS.RENDERER_POSITION.RUNTIME_LANDSCAPE` via `UigsRendererVisualCaptureInstrumentedTest`, covering the real mpv/libass preview and production Interaction Overlay from the shared runtime registry.

Keeping the older PR #76 ToolInstance/renderer/synthetic-overlay captures would therefore create overlapping evidence identities, including a weaker synthetic proxy fixture for a claim already covered by runtime-backed evidence.

PR #76 was reduced to the remaining unique gap: `ASS.CANVAS.WORKSPACE.FIXTURE_LANDSCAPE`.

## Candidate rule

Before adding a new production visual capture state:

1. resolve the Surface ID against current source-owned capture declarations;
2. compare the exact claim and evidence level of existing states;
3. reuse or strengthen an existing state when it already owns the claim;
4. add a new capture identity only for a distinct presentation, state, claim, or evidence tier;
5. do not preserve a lower-tier duplicate merely because it was implemented earlier on a feature branch;
6. keep genuinely complementary evidence separate when it proves different layers (for example production-rendered presentation vs runtime-backed renderer behavior).

## Relationship to existing Foundry knowledge

This complements:

- `OPS.UIGS.SOURCE_OWNED_UI_INVENTORY`, which makes the product repository authoritative for concrete Surfaces;
- `OPS.UIGS.CROSS_LAYER_EVIDENCE_RESOLVER`, which keeps evidence gaps and evidence layers explicit;
- `Automated Production Visual Evidence Capture`, which defines distinct production-rendered/runtime-backed/field tiers.

The additional observation is the **evidence-identity deduplication step** during gap closure.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#76`
- dedupe commits: `d36e79962934c63fde83e4b0f97c54d75c62e86d`, `b0b21c6c2d8a62449af6191434e5d5b008327bca`
- evidence level: source-owned capture-contract audit + implementation cleanup under CI validation

This is a Candidate only. It does not modify Canonical guidance.
