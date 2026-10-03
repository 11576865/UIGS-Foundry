# Candidate: Spatial canvas camera, semantic zoom, and gesture ownership

Status: **Candidate / design-review observation**
Date: 2026-10-03

## Observation

Reviewing an ASS Workbench infinite-canvas prototype showed a meaningful architectural shift from viewport-clamped floating surfaces to a true workspace camera: the whole workspace can be panned through large signed X/Y offsets and zoomed independently of individual tool surfaces.

That solves a different problem from moving a single panel. It also creates new interaction and rendering constraints that should be modeled explicitly rather than treated as a larger version of a draggable-window host.

## Reusable rule

For an infinite or very large 2D professional workspace:

1. **Workspace camera is a first-class presentation state.**
   - Keep world-space surface geometry separate from the camera transform.
   - Camera pan/zoom must not rewrite committed tool geometry or domain state.
   - Persist or restore camera state only as workspace/presentation state.

2. **Zoom should preserve an interaction anchor.**
   - Cursor-, touch-centroid-, or explicitly selected-object-centered zoom should keep the anchored world point stable when feasible.
   - This is the spatial counterpart of the existing touch-centered temporal zoom invariant.

3. **Low zoom requires semantic zoom / LOD, not only geometric shrinkage.**
   - At overview scales, fully interactive controls can become unreadable and untouchable while still consuming composition/rendering cost.
   - Switch surfaces to compact representations, snapshots, labels, or placeholders below product-specific thresholds.
   - Restore full live controls only when the surface is sufficiently large on screen.

4. **Gesture ownership must be explicit.**
   - Empty-canvas drag may pan the camera.
   - Surface chrome drag may move a surface in world space.
   - Tool-content scroll/drag belongs to the tool.
   - Preview/media pan-zoom belongs to the preview unless the user explicitly invokes workspace navigation.
   - Do not infer ownership from motion shape after the gesture has already started.

5. **Offscreen and overview rendering should be virtualized.**
   - Cull or suspend expensive surfaces outside the viewport plus a bounded prefetch margin.
   - Avoid keeping heavyweight renderers, lists, or editors fully live solely because their world-space node still exists.

## Why this generalizes

The same constraints apply to node editors, diagramming tools, DAWs with spatial workspaces, CAD-like canvases, whiteboards, visual programming systems, and professional multi-tool workbenches.

## Evidence boundary

This candidate comes from design review of a prototype interaction recording, not a completed implementation or measured performance test.

It does not prescribe:
- exact zoom thresholds;
- whether a minimap is required;
- persistence defaults for camera position;
- specific Android gesture APIs;
- a particular coordinate precision strategy.

Do not promote to Canonical from this observation alone.
