# Candidate: Treat screen-space masks as incompatible with animated object geometry unless the mask follows the transform

Status: candidate
Date: 2026-10-04
Domains: authoring-tools, animation, masking, coordinate-spaces

## Summary

A visual composition can look correct in a static frame while becoming invalid as soon as the object geometry animates.

When a mask/crop is authored in fixed screen/script coordinates but the visual object later rotates, scales, shears, or otherwise changes geometry, the mask does not automatically follow that transform. Combining the two without an explicit transform relationship can therefore clip the wrong region or make generated layers visually detach.

## Candidate rule

For authoring systems that combine masks/crops with animated geometry:

1. Identify the coordinate space of the mask and the coordinate space of the animated object.
2. Do not assume a fixed screen-space mask follows object-space scale/rotation/shear.
3. If the format/runtime cannot express the required mask transform coherently, fail closed on the unsupported combination.
4. Surface the incompatibility in the authoring UI before commit when practical.
5. Preserve atomicity: an unsupported composition must not partially generate layers or mutate the canonical document.
6. Lift the restriction only after the mask can be represented in a coordinate space or transform chain that remains coherent with the animated geometry.

## Evidence

ASS Workbench Android PR #84 implements a reflected-subtitle spatial fade by splitting the reflection into multiple ordinary ASS Events with non-overlapping rectangular `\clip` bands and different alpha values.

The same composition system can also author a flip/stretch entrance using `\frx` and `\fscy` animation. Those transforms affect the reflected glyph geometry, but the rectangular `\clip` bands remain fixed in script/screen coordinates. Applying both simultaneously would therefore allow the reflection to rotate/scale through static masks and produce geometrically detached clipping.

The branch was corrected to reject `fade + entrance` at the domain composition boundary, mirror that restriction in UI validity, and add regression coverage confirming the failed composition leaves the source document unchanged.

## Provenance

- project: 11576865/ASS-Workbench-Android
- PR: #84
- evidence level: concrete composition incompatibility found during implementation + fail-closed fix + regression test
- deduplication: searched UIGS-Foundry for equivalent screen-space-mask / animated-geometry guidance; no direct duplicate found
- status rationale: reusable coordinate-space/composition rule, but not yet validated across multiple formats/renderers

This is a Candidate only. It is not Canonical.
