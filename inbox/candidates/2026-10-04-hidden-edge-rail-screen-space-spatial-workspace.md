# Candidate: Hidden edge rails should summon transient screen-space tools without moving the spatial world

Status: candidate
Date: 2026-10-04
Domains: interface-grammar, spatial-workspace, edge-navigation, motion
Evidence type: direct user-provided Android recording plus ASS Workbench code review

## Trigger

A user-provided Android recording shows a hidden left-edge affordance that expands into a narrow vertical rail. The underlying home surface remains spatially stable while the rail slides over it. The rail can then replace its own content with a compact widget/card and can launch a destination that expands over the screen. The edge rail is therefore a screen-space summon surface rather than part of the underlying content geometry.

ASS Workbench already has EdgeBookmarkWorkspace semantics (edge bookmarks, open/resident panels, extent fractions and four-edge layers), but current main keeps 50 dp bookmark rails visible and conditionally inserts EdgeLayerPanel without an explicit entrance/exit interpolation. The infinite-canvas PR #107 separately introduces world-space camera/navigation.

## Candidate rule

For a spatial/infinite workspace:

- hidden edge affordances and summon rails belong to Screen Space, not World Space;
- opening a transient edge rail should not change camera x/y/scale or relocate world nodes;
- transient rail/panel motion should overlay the current working set, preserving spatial context behind it;
- a user may explicitly promote a transient edge panel to resident/pinned state, but transient and resident presentation remain distinct;
- the collapsed affordance may be visually minimal, but must retain an accessible touch target and non-gesture alternative;
- edge gesture ownership must be resolved before empty-canvas pan so the same drag is not interpreted by both the rail and the camera;
- opening/closing should preserve tool instance identity, binding, draft and document state;
- programmatic expansion/collapse should use bounded motion continuity rather than one-frame insertion/removal where practical.

## Acceptance direction

Verify that:
- edge summon does not mutate camera state;
- background world remains visually fixed while rail moves;
- outside tap/back/collapse returns to the same camera and working set;
- resident promotion keeps the same tool instance;
- system-back/edge gestures and canvas pan have deterministic precedence;
- document Undo is unaffected by opening, closing, resizing or pinning edge surfaces.

## Evidence boundary

This is a Candidate, not a Canonical rule. It is based on one recorded interaction pattern and current ASS Workbench architecture review. It does not prescribe a single rail width, side, easing curve or mandatory hidden-sidebar design.

No Canonical promotion.
