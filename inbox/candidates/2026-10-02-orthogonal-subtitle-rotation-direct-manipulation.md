# Candidate: Orthogonal subtitle rotation as direct-manipulation geometry

Status: **Candidate / single-observation**
Date: 2026-10-02

## Observation

A user-provided Aegisub screen recording shows a visual typesetting interaction in which subtitle text is rotated around the screen-space X and Y axes. During manipulation, the rendered subtitle visibly compresses toward an edge-on state and re-expands after passing it, making the change legible as a spatial transformation rather than as a numeric-only parameter edit.

## Source verification added during implementation

Direct inspection of Aegisub `visual_tool_rotatexy.cpp` confirmed that its X/Y rotation gesture maps screen deltas asymmetrically:

- vertical pointer delta drives X-axis rotation with inverted sign;
- horizontal pointer delta drives Y-axis rotation;
- Shift constrains the gesture to one pointer axis;
- Ctrl quantizes both angles to 30-degree increments;
- the visual grid is rendered with the current X/Y/Z rotation, scale, shear, and origin.

This strengthens the touch-porting implication: an Android implementation should preserve the semantic distinction between “tilt around X” and “turn around Y”, while replacing hidden modifier-key state with explicit touch-accessible controls.

## Reusable hypothesis

For authoring tools whose output format already contains orthogonal rotation parameters, X/Y rotation should be treated as a first-class spatial manipulation capability rather than hidden as raw numeric fields.

A robust UI contract should separate:

- domain parameters (for ASS, likely the semantics corresponding to orthogonal rotation and rotation origin);
- manipulation presentation (gizmo / drag proxy / gesture);
- renderer-authoritative preview;
- explicit write target and affected object;
- transient preview during continuous manipulation and one formal commit at gesture end.

The UI should make axis identity explicit and must not infer the user's intended axis from an ambiguous freeform gesture.

## Why this may generalize

The same interaction pattern can apply to 2.5D text/object editors, motion-graphics controls, subtitle authoring, and other parameterized visual editors where rotation exists in the domain model but is difficult to understand through numbers alone.

## Evidence boundary

This began from one observed Aegisub interaction supplied by the user on 2026-10-02 and now also includes direct source verification of Aegisub's X/Y rotation drag mapping. It does **not** establish:
- Aegisub's complete internal implementation;
- exact ASS/libass mathematical behavior;
- the best mobile gesture mapping;
- accessibility behavior;
- whether perspective/origin manipulation is coupled to the same tool.

Before promotion, verify Aegisub behavior, ASS tag semantics, renderer differences, and mobile direct-manipulation ergonomics.

## Related UIGS principles

Consistent with:
- renderer-authoritative feedback;
- explicit user intent;
- transient preview -> single commit;
- semantic parameter / multiple presentations;
- no ambiguous gesture inference.

Do not promote to Canonical from this observation alone.
