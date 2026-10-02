# Candidate: Co-registered temporal layers for subtitle timing

Status: **Candidate / single visual observation**
Date: 2026-10-02

## Observation

A user-provided subtitle-editor screenshot shows audio waveform, subtitle event spans, event text, boundary markers, and time ruler occupying the same horizontal time coordinate. Subtitle regions are not presented as a separate list requiring mental mapping back to the waveform; event duration is directly co-registered with the underlying audio structure.

## Reusable hypothesis

For timing-oriented editors, waveform, event spans, playhead/keyframes, timing diagnostics, and event labels should be treated as **co-registered temporal layers** over one canonical time mapping rather than as independent widgets which merely happen to scroll together.

The core contract is:

`time -> shared x-coordinate mapping`

All temporal layers derive geometry from the same mapping and the same time-base policy. Pan, zoom, CFR/VFR conversion, snap, and focus changes must therefore not maintain separate local time scales.

Semantic zoom should control which information is visible and how dense it is, but should not force mutually exclusive “waveform mode” and “event-block mode” when the combined view is useful. At intermediate scales it may be beneficial to show both waveform shape and event identity/text simultaneously.

## Interaction implications for touch

A touch implementation should distinguish:
- tapping an event span -> focus/select event;
- dragging an explicit start/end handle -> trim that boundary;
- dragging a selected event body -> move the event only if that operation is explicitly enabled;
- dragging empty timeline space -> pan time viewport;
- pinch on timeline -> zoom time viewport;
- long press / contextual action -> open detailed timing or event controls.

Touch hit targets may be larger than the rendered boundary line, but visual geometry and write target must remain explicit. Gesture capture freezes target and operation until finish/cancel.

## Why this generalizes

The pattern applies to subtitle editors, DAWs, captioning systems, annotation tools, video editors, transcription tools, and any domain where multiple objects share a common temporal coordinate system.

## Evidence boundary

This candidate is based on one user-provided screenshot and the current ASS Workbench design context. The screenshot alone does not establish the source application's complete interaction model, exact meaning of its colors, or overlap-lane behavior.

Before promotion, validate on real touch prototypes:
- event overlap presentation;
- dense-event readability;
- boundary-hit precision;
- pan vs trim gesture arbitration;
- text truncation at multiple zoom levels;
- VFR/frame-boundary behavior.

## Relation to ASS Workbench

This refines, but does not replace, the existing Timeline semantic-zoom direction. It suggests that event bars and waveform should be understood as layers sharing one temporal projection, with zoom changing information density rather than necessarily switching between isolated representations.

Do not promote to Canonical from this observation alone.
