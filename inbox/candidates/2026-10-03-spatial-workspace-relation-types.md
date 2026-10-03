# Candidate: Spatial workspace relations must separate geometric coupling from semantic navigation

Status: **Candidate / design-review observation**
Date: 2026-10-03

## Observation

Discussion of an unbounded professional workspace introduced several useful ways to keep related tool surfaces together or recover them in a large world: rigid groups, magnetic/docked assemblies, chain/tether relations, visual links, and jump/portal navigation.

These mechanisms look similar on screen because they can all be drawn as lines, adjacency, or shared selection, but they impose very different behavior. Treating them as one generic "connected windows" feature would create ambiguous movement, persistence, undo, and domain semantics.

## Reusable rule

In a spatial workspace, relation type must be explicit. At minimum distinguish:

- **geometric group**: surfaces share a transform or move as a rigid/relative cluster;
- **dock/tile relation**: surfaces share edges and participate in local layout/resizing;
- **tether/constraint relation**: surfaces keep a relative distance/offset or follow constraint but remain individually placed;
- **semantic relation**: surfaces or tools are related by domain meaning, binding, observation, or data flow without requiring co-movement;
- **navigation link / portal**: activation changes camera focus or jumps to a remote surface/region without changing either surface's world geometry.

## Interaction contract

- A visible connector must not silently imply both semantic binding and geometric coupling.
- Grouping and ungrouping must not retarget domain bindings.
- Camera jumps and portals must not rewrite world-space surface geometry.
- Docking may change local layout constraints but should remain workspace state rather than document/domain state.
- Relation visuals should identify their behavior through type, affordance, or mode instead of relying on one generic line style.

## Why this generalizes

The distinction applies to node editors, diagramming tools, CAD workspaces, whiteboards, DAWs, visual programming systems, spatial IDEs, and multi-tool professional canvases.

## Evidence boundary

This candidate comes from design reasoning around an infinite-canvas prototype and has not yet been validated as a production interaction system. Exact relation vocabulary, visual style, and persistence rules remain product-specific.

Do not promote to Canonical from this observation alone.
