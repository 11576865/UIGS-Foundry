# Bug candidate — HSR single-cue effect preview can declare Fade beyond encoded video tail

Date: 2026-10-16
Status: Source repaired and CI regression-verified in PR #189; Android device playback pending
Project: [HSR-Voice-Archive-Builder](https://github.com/11576865/HSR-Voice-Archive-Builder)
Scope: ASS timeline, selected voice preview, FFmpeg/libass, duration and temporal evidence

## Observed source path

The user asked whether the Effects workbench's generated video includes the requested Fade envelopes or only spoken voice duration. Investigation on HSR main after PR #187 shows:

- `app/effect_voice_preview.py::resolve_effect_voice` computes `before` and `after` from actual manifest PCM voice boundaries and neighboring gaps. It returns `duration_seconds = before + voice_duration + after` and `preview_after_fade_ms = after * 1000`. A final cue, having no following start time, gets `after=0`.
- `app/ass_preview.py::render_ass_preview_video` passes the actual audio voice start, end and `preview_end_margin_ms` to an individual `PreviewEntry`, produces a video of exactly the resolved `duration_seconds`, and ffprobes the encoded duration.
- `subtitle_layout/ass_writer.py::_voice_fade_windows` initially limits the last cue's fade-out to `min(outgoing, preview_end_margin_ms)` if the margin is present. However, the unconditional last assignment `windows[-1] = (windows[-1][0], outgoing)` subsequently overwrites the cap regardless of whether the margin exists. For a selected last/single cue, ASS event end can therefore be later than the FFmpeg output end, even when format-duration and presence checks pass.
- Example: a 4 s final voice, a 600 ms configured Fade and 600 ms available *before* the voice produce a 4.6 s video (`before=0.6`, `after=0`), but the ASS last-event outgoing envelope still declares 600 ms after the voice. This clips the outgoing portion even though the ordinary inter-cue Fade budget is valid.

## Clarification after user correction

The project's “blank time” means **deliberately inserted silence between independent archived PCM clips**, not unpredictable silence inside source recordings. Default same-group gap is 2.5 s and chapter gap is 5 s; when Fade is configured at 600 ms, the existing UI/server budget admits it and leaves at least 1.3 s clear between same-group voices (for those defaults). An over-budget adjacent-cue situation is actively prevented and is **not** the normal preview failure explanation.

The reported discrepancy is narrower: the **end-of-archive / end-of-selected-preview boundary** does not have a following manifest voice with which to measure a gap. The full archive can extend still-image video to accommodate a final Fade, but the isolated preview resolver currently sets `after=0` for a final manifest cue. The correct repair is to provide a deliberate bounded *preview video tail* with the configured Fade while keeping PCM speech times immutable, not to warn the user about invented missing inter-cue silence. The source-level code problem remains unverified by an actual end-cue rendered-frame regression.

## Classification

**Source-grounded code defect**, with player-visible clipping still needing deterministic FFmpeg/libass regression proof. No claim that every preview loses Fade: positive, sufficient margins preserve the intended duration. This specifically concerns ending cues and insufficient preview tail margins.

## Required bounded regression

Construct real temporary FLAC + manifest with selected cue as the final entry, and separately with a following cue providing < requested Fade tail. Render the actual dynamic preview and probe duration and frame alpha progression. Establish that the ASS fade-out envelope does not extend beyond the encoded preview video duration, or deliberately extend video using a documented, provenance-safe silent still-image tail. Do not shift PCM speech times, invent audio samples, or report success merely from an ASS `\\fad` tag or successful ffprobe.

## Deduplication

Reviewed `inbox/candidates/2026-10-16-voice-anchored-ass-transition-gap-budget.md`, which already tracks general speech/effect/video-tail clocks and the final archive MKV video-tail extension. This Bug candidate isolates the additional *single-cue preview* inconsistency between its capped `preview_end_margin_ms` and the ASS writer's unconditional outgoing envelope. No Canonical modifications.

## Repair verification — PR #189 (2026-10-16)

HSR [PR #189](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/189), exact tested head `05fc559e5a14ddeb8fdc21c15d99e711b0d50f02`, merged to `main@f417e4794e752c4780bb06d7563614315bde4c6a`.

- `resolve_effect_voice()` now reserves the author-chosen after-voice Fade for the last archive cue as a bounded **video-only tail**, even with no following voice. PCM timing and the source audio samples are not extended.
- `_voice_fade_windows()` no longer overwrites the bounded preview outgoing margin with the archive-only terminal Fade. A non-preview archive retains its full configured Fade and extends its video as before.
- Regression tests verify both language ASS Dialogue intervals and native `\\fad(600,600)` for a 4s voice + 600ms/600ms margins (5.2s preview), and a separately constrained tail of 200ms without impossible ASS events.
- The real-MKV-selected-other-cue FFmpeg/libass preview integration decoded a genuine FLAC track copied from the sealed Matroska and validated the generated WebM/Opus duration and audible PCM.
- Exact-head GitHub workflows all passed: [unit + Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38866875998), [seven ASS requirements](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38866876011), [Chromium + libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38866876020).

**Remaining evidence:** User's physical Android/Termux media, receipt and visual Fade frame progression are not yet inspected. CI proves generated timing/audio properties, not perceptual playback on that device. Do not treat the bug as physical-device accepted or promote to Canonical based on this project.
