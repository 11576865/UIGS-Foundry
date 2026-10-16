# Bug candidate — HSR single-cue effect preview can declare Fade beyond encoded video tail

Date: 2026-10-16
Status: Source-confirmed envelope inconsistency; runtime reproduction pending
Project: [HSR-Voice-Archive-Builder](https://github.com/11576865/HSR-Voice-Archive-Builder)
Scope: ASS timeline, selected voice preview, FFmpeg/libass, duration and temporal evidence

## Observed source path

The user asked whether the Effects workbench's generated video includes the requested Fade envelopes or only spoken voice duration. Investigation on HSR main after PR #187 shows:

- `app/effect_voice_preview.py::resolve_effect_voice` computes `before` and `after` from actual manifest PCM voice boundaries and neighboring gaps. It returns `duration_seconds = before + voice_duration + after` and `preview_after_fade_ms = after * 1000`. A final cue, having no following start time, gets `after=0`.
- `app/ass_preview.py::render_ass_preview_video` passes the actual audio voice start, end and `preview_end_margin_ms` to an individual `PreviewEntry`, produces a video of exactly the resolved `duration_seconds`, and ffprobes the encoded duration.
- `subtitle_layout/ass_writer.py::_voice_fade_windows` initially limits the last cue's fade-out to `min(outgoing, preview_end_margin_ms)` if the margin is present. However, the unconditional last assignment `windows[-1] = (windows[-1][0], outgoing)` subsequently overwrites the cap regardless of whether the margin exists. For a selected last/single cue, ASS event end can therefore be later than the FFmpeg output end, even when format-duration and presence checks pass.
- Example: requested 600 ms Fade, 4 s voice and a final-cue `after=0` produce a 4 s preview, while the ASS last-event outgoing envelope is still 600 ms. The full declared Fade is not present within the encoded video.

## Classification

**Source-grounded code defect**, with player-visible clipping still needing deterministic FFmpeg/libass regression proof. No claim that every preview loses Fade: positive, sufficient margins preserve the intended duration. This specifically concerns ending cues and insufficient preview tail margins.

## Required bounded regression

Construct real temporary FLAC + manifest with selected cue as the final entry, and separately with a following cue providing < requested Fade tail. Render the actual dynamic preview and probe duration and frame alpha progression. Establish that the ASS fade-out envelope does not extend beyond the encoded preview video duration, or deliberately extend video using a documented, provenance-safe silent still-image tail. Do not shift PCM speech times, invent audio samples, or report success merely from an ASS `\\fad` tag or successful ffprobe.

## Deduplication

Reviewed `inbox/candidates/2026-10-16-voice-anchored-ass-transition-gap-budget.md`, which already tracks general speech/effect/video-tail clocks and the final archive MKV video-tail extension. This Bug candidate isolates the additional *single-cue preview* inconsistency between its capped `preview_end_margin_ms` and the ASS writer's unconditional outgoing envelope. No Canonical modifications.
