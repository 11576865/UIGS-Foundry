# Case: Subtitle authoring acceptance workflow for a spatial tablet workspace

Date: 2026-10-04
Status: Case / acceptance scenario
Scope: tablet-first subtitle authoring UI, spatial workspace validation

## User workflow

A practical first-pass subtitle authoring session from zero should be possible without repeated mode switching or losing simultaneously useful context.

The session includes:

- viewing video while making timing decisions;
- using timeline position plus frame stepping (+1 / -1 frame) to refine subtitle start and end boundaries;
- using waveform and/or spectrogram views as additional timing evidence;
- dragging playback position / playhead;
- undoing failed edits;
- editing subtitle text content;
- merging subtitle events;
- splitting subtitle events;
- assigning / editing multiple subtitle roles or speakers;
- applying a style change to multiple subtitles;
- overriding style on individual subtitles;
- maintaining enough simultaneous context that timing, text, visual preview, and structural edits do not require constant navigation between mutually exclusive screens.

Complex visual effects are intentionally out of scope for this first acceptance scenario.

## Acceptance principle

The spatial workspace is not accepted merely because its camera, windows, zoom, grouping, or infinite extent work.

It must support the above end-to-end task with low interaction overhead and preserved simultaneous context.

A failure includes:

- repeated back-and-forth UI switching for operations that belong to the same continuous authoring loop;
- losing video, timeline, waveform/spectrogram, current subtitle text, or relevant selection state when another adjacent operation is invoked;
- requiring multi-step surface management before ordinary subtitle edits;
- making frame-accurate timing slower than a conventional well-designed subtitle editor;
- forcing the user to reconstruct task context after undo, merge, split, role assignment, or style edits.

## Important distinction

For speech-boundary timing, three audio visualizations are distinct:

- waveform: amplitude over time;
- spectrogram: frequency energy over time;
- instantaneous frequency spectrum: frequency distribution at one time slice.

Waveform and spectrogram are the primary candidates for continuous subtitle timing. A frequency spectrum may be useful for inspection, but should not be conflated with a spectrogram.

## Evidence boundary

This case is based on a real workflow description and is intended as an acceptance test fixture, not a Canonical UI specification. It does not prescribe one fixed layout, exact control placement, or a single mandatory visualization.

Do not promote to Canonical from this case alone.
