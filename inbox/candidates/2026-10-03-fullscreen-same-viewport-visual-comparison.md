# Candidate: Thumbnail comparison should provide a full-screen same-viewport inspection path

Date: 2026-10-03
Status: Candidate
Scope: visual comparison / media inspection / frame-accurate editing UI

## Observation

Side-by-side thumbnails are sufficient for coarse differences but are weak for subtle frame-to-frame changes. The user must perform repeated eye jumps and mentally register the same spatial detail across two small views.

In a lossless-cut inspection workflow, the requested IN frame and the actual keyframe-aligned IN frame may differ only by a small amount of motion, subtitle timing, particle state, camera movement, or object position. Small thumbnails make these differences unnecessarily hard to judge.

## Candidate principle

When a compact UI presents two images whose differences may be subtle:

- clicking either comparison image should open a full-viewport inspection surface;
- when both images represent the same scene/alignment, prefer a same-viewport wipe comparison with a draggable divider over separate full-screen images;
- preserve labels and timestamps in the full-screen surface so visual evidence remains bound to its semantic source;
- provide keyboard escape and a deterministic reset position;
- keep the compact thumbnails as navigation/summary rather than the only evidence surface.

## Rationale

The full-screen surface solves scale; the wipe comparison solves registration. These are distinct problems and both matter for high-precision visual inspection.

## Limits

- Full-screen presentation does not improve source-frame accuracy; the underlying frame extraction path remains authoritative.
- Wipe comparison assumes the two frames share the same geometry/aspect mapping.
- This candidate does not imply all image pairs need a full-screen viewer; it is most useful where subtle visual differences affect a user decision.

Do not promote to Canonical from this single implementation.
