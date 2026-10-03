# Candidate: Optional timeline visualizations must not gate the core timeline interaction

Date: 2026-10-03
Status: Candidate
Scope: media timelines / source trimming / progressive enhancement

## Observation

A media timeline can serve several independent functions:
- authoritative source duration and ruler;
- IN / OUT range selection;
- playhead positioning;
- source-frame preview;
- optional audio waveform;
- optional keyframe visualization.

If the implementation treats the audio waveform as the prerequisite for constructing the whole timeline, silent/video-only media can make the timeline appear broken even though range selection and source-frame inspection remain valid.

## Candidate principle

Treat optional analytical overlays as progressive enhancement rather than as the authority for the timeline itself.

For example:
- no audio -> keep ruler, IN/OUT markers, playhead and frame preview;
- waveform extraction failure -> report the missing layer but preserve the timeline;
- keyframe data -> add only where the operation semantically needs it, such as lossless copy.

The UI should state what the timeline means in the current workflow. A source-range timeline in a transcode workflow should not be visually or verbally confused with a source-vs-output quality comparator.

## Reusable implication

Separate:
1. timeline authority and navigation;
2. optional visualization layers;
3. post-operation verification/comparison.

Do not make a nonessential visualization failure collapse the core interaction.

Do not promote to Canonical from this single implementation.
