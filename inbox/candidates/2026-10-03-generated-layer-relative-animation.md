# Candidate: Animate generated composition layers relative to each layer's own base state

Status: candidate
Date: 2026-10-03
Domains: authoring-tools, animation, composition

## Summary

When a higher-level effect compiles one source object into several visual layers, applying animation only to the source can break the composition: generated reflections, glows, shadows, masks, or echoes can appear detached while the source moves or transforms.

A safer model is to apply the same **relative animation intent** to every generated layer while resolving each layer's final/base values independently.

For example, if a source ends at scale Y 80 and rotation X 10, while a reflected companion ends at scale Y 40 and rotation X 190, a shared entrance such as "start at 10% height, overshoot to 125%, rotate +90° into place" should compile to:
- source: 8 -> 100 -> 80, 100° -> 10°;
- reflection: 4 -> 50 -> 40, 280° -> 190°.

Copying the source's absolute target values into the reflection would destroy the reflection's own geometry.

## Candidate rule

For generated visual stacks:

1. Express reusable animation as relative intent (percentage, offset, delta, duration, easing), not source-specific absolute target values.
2. Resolve each generated layer's current/base geometry first.
3. Compile the relative animation separately against each layer's base.
4. Keep timing synchronized across the stack.
5. Add regression coverage that verifies generated layers return to their own base state, not the source object's base state.
6. If a generated layer cannot safely participate in the animation, make that limitation explicit instead of leaving it visually detached without warning.

## Evidence

ASS Workbench Android PR #83 initially applied the flip/stretch entrance only to the source Event after creating glow and reflection companions. That left generated layers static during the source entrance.

The implementation was corrected so the same relative entrance specification is compiled for the source and every generated Event. Because the reflection already owns its own `\fscy` and `\frx+180` base values, its generated keyframes resolve against those reflected values rather than the source targets. Regression coverage checks source, glow, and reflection final states separately.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #83
- evidence level: concrete composition bug found during implementation + repaired domain logic + regression test
- deduplication: searched UIGS-Foundry for equivalent generated-layer/base-relative animation guidance; no direct duplicate found
- status rationale: reusable animation/composition architecture candidate; not Canonical

This is a Candidate only. It is not Canonical.
