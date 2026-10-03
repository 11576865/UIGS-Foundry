# Bug: Generated composition layers can be partially overridden by later span-local effect ownership

Date: 2026-10-04
Status: Bug
Scope: effect composition / timed text / inline override ownership / ASS Karaoke

## Symptom

A generated visual layer can begin with the intended reflection, glow, or entrance geometry and then change incorrectly partway through a line.

The failure appears when a higher-level compositor establishes a layer-level base state (for example alpha, blur, Scale Y, Rotation X or border), while later span-local override blocks in the copied source re-own one of those same properties.

With ASS Karaoke this is especially easy to trigger because each syllable may carry its own override block and time-scoped transforms. The same failure is not Karaoke-specific: ordinary later inline spans, leading time transforms, fades, and style resets can also re-own generated properties.

## Failure mechanism

A compositor that prepends or inserts layer-level overrides is not automatically authoritative for the remainder of the Event. ASS override state is sequential.

Example ownership conflict:

- generated reflection establishes its own `\alpha`, `\blur`, `\fscy` and `\frx`;
- a later Karaoke syllable contains `\1a`, `\blur`, `\fscy`, `\frx` or `\t(...)`;
- that syllable takes ownership back from the generated layer;
- the reflection/glow can therefore diverge from its intended geometry or transparency only after a particular span.

This is not a parsing failure. It is an **ownership-order failure**.

## Mitigation implemented

ASS Workbench Android PR #87 first added a fail-closed compatibility guard for Karaoke-region ownership conflicts. Follow-up review in PR #93 generalized the same boundary after finding that non-Karaoke spans and temporal controls can produce the same failure.

The current mitigation:

- plain Karaoke timing tags remain accepted;
- leading static Event-level base overrides remain accepted;
- any later inline span that re-owns a generated property is rejected, whether or not Karaoke is present;
- leading `\t` transforms are inspected for generated-property ownership;
- `\fad` / `\fade` are rejected when the generated effect owns alpha;
- `\r` Style reset is rejected because it can replace the effective style and re-own alpha/blur/geometry mid-line;
- malformed inline or animation syntax is rejected;
- the guard runs before document mutation.

The guard is intentionally architecture protection. It does not claim to solve full span-aware effect composition.

## Reusable lesson

Before copying a rich inline object into a generated visual layer, define property ownership across the *entire ordered span stream*, not only the initial/base override block.

If later spans can re-own properties required by the generated layer, either:

1. compile those span effects into the generated layer's own base coordinate/state system; or
2. reject the composition explicitly.

Silently relying on the generated layer's initial override is unsafe.

## Evidence

- project: `11576865/ASS-Workbench-Android`
- PRs: #87, #93
- regression coverage: plain Karaoke compatibility; Karaoke and non-Karaoke span conflicts; leading transform/fade ownership; Style reset; reflection/glow/entrance failure before mutation
- deduplication: searched UIGS-Foundry for generated-layer/span ownership, Karaoke reflection, and later-inline-override equivalents; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
