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


## 2026-10-09 implementation follow-up — validation pending

Source: \`11576865/ASS-Workbench-Android\`, branch
\`redesign/infinite-canvas-workbench-v2\` (reviewable implementation; **not** evidence of passed CI or device acceptance).

A previous scaled-live-surface UI made tool typography and touch targets
dependent on camera zoom. The replacement separates three representations
while retaining one ToolInstance/Binding/Domain authority:

- Spatial overview uses lightweight identity and binding-summary cards.
- Close-up board restores multiple live Composables at native control density.
  Camera position and surface footprint change, but individual slider/text
  touch targets are not geometrically scaled by the camera.
- A focused native-density edit stage gives a narrow-screen tool a stable
  touch area; video and transparent audio retain explicit layered composition
  and passthrough behavior.

This extends the earlier semantic-zoom candidate with a **two-plane working
surface** hypothesis: composition and spatial organization need not require
permanent downscaling of production controls. It also preserves explicit
gesture ownership and separation of camera history from ASS Undo.

Evidence level: source implementation and proposed JVM/Android regressions,
**Pending CI**. No measured device ergonomics, renderer performance,
large-scene virtualization or universal draft-lifecycle correctness is
claimed. This note does not change Canonical policy or prescribe fixed
zoom thresholds for other products.

## 2026-10-09 PR #138 repair follow-up — Pending CI

An Android Emulator run of the spatial-workbench redesign exposed a presentation-native tool access regression: the old entry-point action was removed, while the replacement tool-directory action was placed after an unbounded horizontal list of tool instances. In a narrow viewport, primary creation/navigation actions must remain visible outside an independently scrollable overflow region; merely retaining them in the composition or accessibility tree does not guarantee practical touch reachability. The branch now fixes `spatial-add-tool` before the scrolling instance tabs and adds an explicit visibility assertion.

The same redesign introduces a deferred tool-picker selection transaction. Explicit birdseye/recall navigation must cancel that pending transaction, or a later unrelated active ToolInstance update may unexpectedly steal focus. A new connected regression checks that manual navigation remains authoritative over a stale picker selection.

These are implementation-level hypotheses and regressions in `11576865/ASS-Workbench-Android` PR #138, not confirmed post-fix Android acceptance. Status: **Pending CI**. This follow-up supplements the existing camera/gesture/semantic-zoom candidate and does not modify Canonical requirements.

## 2026-10-09 offscreen composition and draft ownership — Candidate / Pending CI

The ASS Workbench infinite-canvas redesign initially applied offscreen culling to every live tool. A code review identified an important boundary: removing an Android Compose editor from composition can destroy local non-saveable draft state, even when a `SaveableStateHolder` is present. That holder does not by itself establish draft-lifecycle durability for arbitrary tools.

The implementation therefore limits viewport-driven composition suspension to media evidence/preview (`preview` and `audio`), while leaving potentially draft-bearing subtitle, parameter, and general ToolInstance editors mounted pending explicit restoration/ownership tests. The camera/world intersection predicate uses Double intermediates with a bounded prefetch band. The scene's persisted nodes remain independent of whether production content is currently composed.

This is a **risk containment decision**, not measured performance evidence or proof that every media-side transient state is safe to suspend. Product branch PR #138 includes pure JVM coverage and an Android instrumentation regression, both awaiting this head's CI. A future generalized virtualization pattern would require proof of draft restoration (including transient previews and foreign-owner conflicts) before broader unmounting. Do not promote to Canonical from this observation.

## 2026-10-10 v2 usability and interaction recovery — Pending CI

ASS Workbench PR #138 exposed a design/regression risk when replacing a viewport-constrained live-surface workspace with a semantic-zoom board plus native focused editor. Although camera and touch-target models improved, the replacement dropped previously usable actions (layout lock, domain-instance close/duplicate, binding controls and immediate tool entry from the default focused stage). Restoring those actions requires forwarding commands through existing ToolInstance/Binding capability declarations, not cloning domain state inside the host.

A second design risk: switching from a live editor to a lightweight semantic card can **unmount the editor even when the node remains visually represented**. `rememberSaveable` does not generally preserve ordinary `remember` drafts. The follow-up keeps draft-bearing editor composition present but visually masked by a compact card, while allowing explicitly scoped offscreen media virtualization. Instrumentation introduces a non-saveable draft preservation test across zoom out/in.

Additional recovery: explicit one/two-column arrangement honors layout locks and hidden nodes; `infinite-v2` carries layoutLocked while decoding v1; initial project-scene nodes are not pruned before WorkspaceState hydration; the focused title provides direct navigation instead of requiring birdseye/return cycles.

**Evidence boundary:** code/tests submitted to PR #138 on 2026-10-10; current Android CI, emulator and visual/device acceptance are Pending. This is a Candidate observation with compatibility-test implications, not a new Canonical policy or a claim that the complete 240 UI ledger is closed.

## 2026-10-10 focused-stage reference/editor split — Pending CI

Follow-up engineering observation from ASS Workbench Android PR #138: a semantic-zoom canvas with a single full-screen focused editor is still ergonomically fragmented when users must continuously compare live ASS/video output with text, Style or Position changes. The workbench must preserve **simultaneous observation and authoring**: a real synchronized media preview can coexist with the actual production editor at native control density. Narrow devices stack panels; wide devices use columns; the preview can be collapsed or resized without changing canonical ASS, node geometry or document Undo.

Crucial implementation distinction: toggling between split and unsplit layout can unmount ordinary `remember` editor drafts. The patch uses `movableContentOf` keyed to the editor identity and `rememberUpdatedState` for live callbacks to preserve the editor composition during those pane moves; an Android regression exercises non-saveable draft continuity. The design also temporarily gives keyboard/IME height back to the editor and insets the focused stage beside a resident tool rail instead of allowing its overlay to obscure controls.

**Evidence:** source and new connected test in PR #138, latest-head Android CI/Emulator and device acceptance pending. This does not establish arbitrary dual-writer ToolInstance safety or universal draft survival across sessions; no Canonical change from this single project observation.
