# Candidate: Generated span effects must restore the effective base state, not a hard-coded default

Status: candidate
Date: 2026-10-04
Domains: authoring-tools, animation, text-effects, state-resolution

## Summary

A generated timed effect often needs a temporary start state (hidden, blurred, rotated, scaled) and a final state. The final state must be resolved from the source object's **effective state**, not from format defaults.

For text/span effects this includes more than geometry:

- inherited style scale/rotation versus Event overrides;
- per-channel alpha carried by style colors;
- explicit Event-level overrides;
- resets or independent fade/transform mechanisms that may change the effective state mid-object.

Hard-coding a generated effect to end at Scale Y 100, Rotation X 0 or Alpha 0 can silently change the authored appearance even if the animation itself looks correct.

## Candidate rule

When compiling temporary animation into existing spans/objects:

1. Resolve the source object's effective base value for every property the compiler owns.
2. Express the generated animation relative to, and return to, those resolved base values.
3. Preserve independently meaningful channels separately when the format distinguishes them (for ASS, primary/secondary/outline/shadow alpha).
4. If a reset or another animation mechanism changes the owned base state and the compiler cannot resolve it safely, reject generation rather than falling back to defaults.
5. Keep a text-only/default API only when its default-state assumption is explicit; document-aware authoring should use document/style context.

## Evidence

ASS Workbench Android PR #86 extends the Karaoke FX compiler with per-syllable flip/stretch motion and fixes two base-state hazards:

- Scale Y resolves from Event override first, then Style; Rotation X resolves from Event override.
- Generated syllables return to each Event's resolved scale/rotation instead of 100/0.
- Reveal alpha no longer returns every channel to fully opaque. It hides all four ASS alpha channels temporarily, then restores the alpha embedded in the Style primary/secondary/outline/back colors.
- Existing alpha/blur/transform/fade syntax is rejected because the compiler does not yet define safe composition semantics for those mechanisms.
- `\r` Style resets are rejected because they can change both geometry and alpha after the initially resolved base state.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #86
- evidence level: implemented domain logic + regression coverage; CI pending at intake time
- deduplication: searched UIGS-Foundry for effective-base restoration, style-alpha preservation, and reset/fade conflict guidance; no direct duplicate found
- status rationale: reusable authoring/compiler rule; not Canonical

This is a Candidate only. It is not Canonical.
