# Bug: Generated composition layers can be partially overridden by later span-local effect ownership

Date: 2026-10-04
Status: Bug
Scope: effect composition / timed text / inline override ownership / ASS Karaoke

## Symptom

A generated visual layer can begin with the intended reflection, glow, or entrance geometry and then change incorrectly partway through a line.

The failure appears when a higher-level compositor establishes a layer-level base state (for example alpha, blur, Scale Y, Rotation X or border), while later span-local override blocks in the copied source re-own one of those same properties.

With ASS Karaoke this is especially easy to trigger because each syllable may carry its own override block and time-scoped transforms.

## Failure mechanism

A compositor that prepends or inserts layer-level overrides is not automatically authoritative for the remainder of the Event. ASS override state is sequential.

Example ownership conflict:

- generated reflection establishes its own `\alpha`, `\blur`, `\fscy` and `\frx`;
- a later Karaoke syllable contains `\1a`, `\blur`, `\fscy`, `\frx` or `\t(...)`;
- that syllable takes ownership back from the generated layer;
- the reflection/glow can therefore diverge from its intended geometry or transparency only after a particular span.

This is not a parsing failure. It is an **ownership-order failure**.

## Mitigation implemented

ASS Workbench Android PR #87 adds a fail-closed compatibility guard:

- plain Karaoke timing tags remain accepted;
- leading Event-level base overrides remain accepted;
- generated reflection rejects Karaoke-region alpha/blur/Scale Y/Rotation X ownership;
- generated glow rejects Karaoke-region alpha/blur/border ownership;
- generated flip entrance rejects Karaoke-region Scale Y/Rotation X/transform ownership;
- malformed inline syntax is rejected;
- the guard runs before document mutation.

The guard is intentionally temporary architecture protection. It does not claim to solve Layer-aware Karaoke composition.

## Reusable lesson

Before copying a rich inline object into a generated visual layer, define property ownership across the *entire ordered span stream*, not only the initial/base override block.

If later spans can re-own properties required by the generated layer, either:

1. compile those span effects into the generated layer's own base coordinate/state system; or
2. reject the composition explicitly.

Silently relying on the generated layer's initial override is unsafe.

## Evidence

- project: `11576865/ASS-Workbench-Android`
- PR: #87
- regression coverage: plain Karaoke compatibility; reflection/glow/entrance ownership conflicts; failure before mutation
- deduplication: searched UIGS-Foundry for generated-layer/span ownership, Karaoke reflection, and later-inline-override equivalents; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
