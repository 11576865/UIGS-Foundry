# Candidate: Touch translation of modifier-key visual manipulators

Status: **Candidate / observed + source-verified desktop interaction**
Date: 2026-10-02

## Trigger

A user-provided Aegisub screen recording demonstrates the visual X/Y scaling tool. The visible guide exposes horizontal and vertical scale simultaneously while the subtitle renderer updates continuously.

Aegisub source verification for `VisualToolScale::UpdateHold()` shows that the desktop interaction is not merely “drag a handle”:
- free pointer delta changes X and Y scale together;
- Shift constrains the delta to one axis;
- Alt preserves the initial X:Y scale ratio;
- Ctrl quantizes scale to 25-unit steps;
- continuous movement writes `\\fscx` and `\\fscy` preview values.

## Reusable finding

A desktop visual manipulator whose interaction grammar depends on pointer hover/precision plus keyboard modifier keys must **not** be ported to touch by replacing mouse drag with finger drag one-for-one.

The mobile design must explicitly reify hidden desktop constraints as touch-reachable state or geometry. Candidate mappings include:
- explicit X / Y / XY manipulation mode;
- persistent or press-and-hold axis lock;
- visible aspect-ratio lock;
- optional snap / quantization toggle;
- remote Interaction Proxy so the finger does not cover the subtitle or guide;
- fine/coarse control-display gain;
- numeric readout and direct numeric fallback;
- transient renderer-authoritative preview during drag, with one formal commit at gesture end.

The semantic operation should remain the same regardless of presentation:
`ScaleX`, `ScaleY`, constraint mode, snap policy, write target, and affected object are domain/interaction state; finger gesture shape is presentation.

## Why this generalizes

The same translation problem appears when porting desktop CAD, vector editors, motion graphics, subtitle authoring, diagram editors, and other precision tools to phones/tablets. Modifier keys often encode essential interaction state that is invisible in screenshots; a mobile port that ignores them silently loses capability.

## Evidence boundary

This candidate is grounded in:
1. one user-provided Aegisub recording;
2. direct inspection of Aegisub's current `visual_tool_scale.cpp` source.

It does not yet establish the optimal Android gesture design. Touch ergonomics, accessibility, stylus behavior, multi-touch alternatives, and one-handed use still require prototypes and device testing.

## Relation to existing UIGS material

Related but not duplicate of:
- orthogonal subtitle rotation direct-manipulation candidate;
- explicit user intent / no ambiguous gesture inference;
- Interaction Proxy;
- transient preview -> single commit;
- semantic parameter -> multiple presentations.

Do not promote to Canonical from this evidence alone.
