# Test: QHE heterogeneous audio plan and source-owned UI

Date: 2026-10-13
Status: Test / local compiler + actual FFmpeg acceptance; hosted runtime Pending
Source: QHE draft PR #105, code bba86515185d6d204ae653453244a27b5798b9e5

## Dedup
Existing Candidate inbox/candidates/2026-10-12-qhe-per-output-audio-track-intent-and-encoder-capability-layers.md covers the design hypothesis. This records scoped implementation and actual output evidence, not a duplicate design or Canonical promotion. The existing rational-FPS Bug inbox/bugs/2026-10-13-qhe-windows-compression-history-rational-fps-parser.md is referenced; its implementation fix remains pending Windows acceptance.

## Observed implementation / proof
One normalized audioPlan maps source ordinals to contiguous output audio indices; actions copy/AAC/Opus/FLAC/drop, explicit channel/sample-rate/range changes. A legacy global policy applies only when no per-track override exists. Task outputPlan records retained and dropped source tracks. Subtitle and attachment ordinals map separately. Restricted indexed FFmpeg arguments are bounded to 32 output tracks; no shell/path option was added.

Local suite: 196 PASS, 6 conditional skips, 0 failures. Four real FFmpeg integration tests pass: heterogeneous retained codecs are FLAC+AAC or Opus+FLAC; copied FLAC packet SHA256 sequences are unchanged. Output audio codec/channel/sample-rate assertions are independent from task compilation. Build passes. No claim of subjective quality or player support.

Independent review found global-policy leakage in Android count/duration, stale UI defaults/config rows, incorrect known-rate size refusal, false calibration audio costs and missing Android auxiliary counts. These were addressed. Browser fixture covers source reset/default/config ownership; Windows executable tests cover indexed argument rejection and output validation; Kotlin compile/runtime checks are registered but Pending external CI. They are not counted as local runtime passes.

## UI mapping and limits
Intent -> per-output audio intent -> existing authoritative form -> one hidden audioPlan JSON -> expected source-specific transforms -> compiler/actual-output checks. Manual rows use one field; source changes reset it. Guided hard-sub still uses global audio policy and hides this editor. Unknown copy/FLAC budgets remain unknown; complete-file accounting belongs to the next work unit. Old material/report repetition is not independent confirmation. Do not change Canonical.
