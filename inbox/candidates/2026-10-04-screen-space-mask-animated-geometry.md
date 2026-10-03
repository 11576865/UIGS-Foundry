# Candidate: Prevent screen-space masks from overlapping incompatible animated geometry

Status: candidate
Date: 2026-10-04
Domains: authoring-tools, animation, masking, coordinate-spaces

## Summary

A visual composition can look correct in a static frame while becoming invalid as soon as the object geometry animates.

When a mask/crop is authored in fixed screen/script coordinates but the visual object later rotates, scales, shears, or otherwise changes geometry, the mask does not automatically follow that transform. Combining the two while both are visible can therefore clip the wrong region or make generated layers visually detach.

There are at least two safe resolution strategies: make the mask follow the same transform, or remove the temporal overlap so the mask is only visible after the animated geometry has reached the state for which the mask was authored.

## Candidate rule

For authoring systems that combine masks/crops with animated geometry:

1. Identify the coordinate space of the mask and the coordinate space of the animated object.
2. Do not assume a fixed screen-space mask follows object-space scale/rotation/shear.
3. If the format/runtime cannot express the required mask transform coherently, either fail closed or explicitly sequence visibility so the fixed mask is hidden while incompatible geometry is moving.
4. A temporal workaround must preserve the source timing model; for timed text, prefer alpha-gating over shifting Event start time when shifting would desynchronize span-local timing.
5. Surface the composition strategy or incompatibility in the authoring UI before commit when practical.
6. Preserve atomicity: an unsupported composition must not partially generate layers or mutate the canonical document.
7. Treat temporal sequencing as a different visual behavior from true transform-following masks; do not claim geometric equivalence.

## Evidence

ASS Workbench Android PR #84 implements a reflected-subtitle spatial fade by splitting the reflection into multiple ordinary ASS Events with non-overlapping rectangular `\clip` bands and different alpha values.

The same composition system can also author a flip/stretch entrance using `\frx` and `\fscy` animation. Those transforms affect the reflected glyph geometry, but the rectangular `\clip` bands remain fixed in script/screen coordinates. Applying both simultaneously would therefore allow the reflection to rotate/scale through static masks and produce geometrically detached clipping.

The branch first corrected this by rejecting `fade + entrance` at the domain composition boundary. A subsequent implementation found a safe canonical-ASS fallback that does not require a transformed mask: source/glow perform the entrance, while the clipped reflection bands remain fully transparent until the entrance settles and then reveal over a short window. The reflected Events retain their original start time, so Karaoke timing is not shifted. If the Event is too short to leave a post-entrance visible interval, composition still fails atomically.

Regression coverage verifies that the authored entrance is handled by temporal sequencing, reflection bands are not given incompatible geometry transforms, their Event start times are preserved, and short Events fail without mutating the input document.

A later PR #93 review found the same coordinate-space hazard in **pre-existing source animation** rather than compositor-authored entrance animation. A source Event with a leading `\t(...,\frz...\fscx...)` or later span-local geometry changes could previously pass spatial-fade validation even though the generated rectangular clips stay fixed in screen/script coordinates. The branch now rejects geometry-affecting source transforms/spans for spatial fade while still allowing non-geometric transforms such as color-only animation.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PRs: #84, #93
- evidence level: repeated coordinate-space incompatibility found in both compositor-authored and pre-existing source animation + fail-closed/temporal-sequencing corrections + regression tests
- deduplication: searched UIGS-Foundry for equivalent screen-space-mask / animated-geometry guidance; no direct duplicate found
- status rationale: reusable coordinate-space/composition rule, but not yet validated across multiple formats/renderers

This is a Candidate only. It is not Canonical.
