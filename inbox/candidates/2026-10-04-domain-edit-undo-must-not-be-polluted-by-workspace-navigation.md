# Candidate: Domain edit history must not be polluted by workspace navigation

Date: 2026-10-04
Status: Candidate
Scope: spatial professional editors, undo/redo, workspace interaction

## Observation

In a spatial workspace, users may pan or zoom the camera, focus a tool, rearrange surfaces, then immediately undo a subtitle edit. If presentation/navigation operations share the same undo stream as domain edits, Undo becomes unpredictable and destroys editing flow.

## Candidate rule

Keep domain edit history distinct from presentation/navigation state.

- Camera pan/zoom, focus projection, viewport navigation, and ordinary tool activation must not consume document Undo steps.
- Moving/resizing workspace surfaces should not silently enter the subtitle/document history.
- User-level domain operations such as merge, split, timing edits, text edits, and style changes should have explicit transaction boundaries.
- Undo/Redo of domain operations should preserve or deliberately restore useful session context such as selected cue and playhead when feasible.
- If layout editing itself needs Undo, provide a separate workspace-layout history or a clearly scoped layout-edit mode rather than mixing it into document history.

## Why this generalizes

The same issue appears in CAD, DAWs, NLEs, IDEs, node editors, diagramming tools, and other interfaces where viewport manipulation coexists with semantic editing.

## Evidence boundary

This is an architectural inference from workflow acceptance design, supported by the existing requirement that surface geometry not contain domain undo state. Exact restoration semantics for selection, playhead, and layout history require implementation and usability testing.

Do not promote to Canonical from this observation alone.
