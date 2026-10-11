# Candidate: Fractional renderer snapshots must preserve output timebase independently of source frame cadence

Date: 2026-10-12  
Status: Candidate / HSR implementation committed / CI pending  
Source: [HSR-Voice-Archive-Builder PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), head `440c1bab4b7704ac3c5ba41b36c88bc875977a73`  
Domain: media rendering, FFmpeg timestamps, UI evidence, Karaoke/kinetic effects

## Trigger and observed failure mechanism

HSR's actual ASS-preview pipeline generated a synthetic 1920×1080 black input with `r=1` and used `-ss` to choose the frame. This one-second source cadence cannot by itself guarantee the fractional PTS requested by the UI time scrubber. Rendering a screenshot of a particular animation instant is **not the same operation** as seeking within a low-frame-rate input stream.

A small local FFmpeg/libass motion probe compared `\\move` frames at fractional times. Offsetting PTS directly at a 1 fps timebase collapsed distinct subsecond requests; `settb=AVTB,setpts=PTS+requestedSeconds/TB` yielded different render positions for 0.1, 0.45, 0.8 and 1.2 seconds. This is a specific source-code and controlled probe observation, not arbitrary-codec or device-wide proof.

## Proposed reusable engineering rule

When a renderer consumes presentation timestamps to compute animated content, a single-frame synthetic input may use low frame cadence **only if the timestamp for that frame is represented at the precision required by the animation**. Explicitly establish the filtergraph timebase *before* offsetting PTS. Treat preview-time evidence and input sampling rate as separate contracts.

A preview test should vary an effect with subsecond behavior (such as ASS `\\move`, `\\t` or `\\kf`) and assert two requested instants produce the expected distinct renderer outputs. Do not accept HTTP 200 or successful PNG decoding as proof of correct temporal position.

## Implementation / scope

HSR PR #134 changes the screenshot filter to `settb=AVTB,setpts=PTS+time/TB,subtitles=...`. The same precision is used for on-demand dual-background rendered-ink inspection. Real FFmpeg/libass motion fixture added in `tests/test_rendered_ink_boundary.py`.

- Source implementation: submitted in Draft stacked PR, not yet merged.
- Independent local FFmpeg probe: successful.
- Exact-head CI and target Android/Termux field acceptance: **Pending**.
- Frame safety inspection: one chosen instant only, not full temporal coverage.
- No new universal FFmpeg command template is mandated; downstream renderers with other timing semantics need their own tests.

## Deduplication and promotion boundary

Searched Foundry for `timebase`, `settb AVTB`, `subsecond`, and fractional-timestamp rendering. The existing `human-friendly-media-time-input-normalization` Candidate concerns parsing user-entered timestamps; this Candidate concerns the **downstream renderer's timebase and evidence**, so it is not a duplicate. Related prior HSR asynchronous preview Case addresses stale results and decoding provenance but not one-second filtergraph time quantization.

Remain Candidate. A single code review and one controlled probe are insufficient to modify Canonical standards.
