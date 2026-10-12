# Bug: Windows Native completed HEVC job cannot record compression history when source FPS is rational text

Date: 2026-10-13 Asia/Shanghai
Status: **OPEN / observed reproducibly; NOT yet fixed**
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
Draft PR #104: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
Evidence: hosted Windows Native full real job logs in `38286010896`, `38286271487`, and subsequent complex rich Matroska acceptance after AAC fix.

## Observation

Real `Start-MediaTaskJob` completed and emitted a verified HEVC Matroska artifact, yet Windows Bridge logged:

`[WARN] Compression history write failed: Cannot convert value "12/1" to type "System.Double". Error: "Input string was not in a correct format."`

The generated source has video FPS 12/1, a perfectly legitimate FFprobe rational rate. In `windows/native-bridge.ps1::Ensure-CompletedJobHistory`, fallback FPS is computed from the probe by a direct PowerShell cast:

`$fps=if($request -and $request.sourceFps){[double]$request.sourceFps}elseif($source){[double]$source.fps}else{0.0}`

`[double]'12/1'` throws. The function catches/logs failure, so the media job and independent output acceptance remain **successful**, but the expected full-encode compression history record may be missing and therefore cannot be used as future rate/quality evidence. This is distinct from the AAC priming packet corruption and should not be confused with a failed video encode.

## Candidate repair (not yet implemented)

Use a bounded, culture-invariant parser for FFprobe rational frame rates (e.g. `30000/1001` and `12/1`), reject zero denominator, nonfinite/negative values, bound rates to a supported range, and keep the exact rate expression separately if needed for precise timebase modeling. Do not change the final full artifact acceptance status in response to a *history* write failure without a new explicit product policy. Add dedicated Windows parser and `Ensure-CompletedJobHistory` acceptance tests for `12/1`, `30000/1001`, invalid and missing FPS values.

## Evidence boundary

Not yet proven that every history write in this job is missing without inspecting persisted storage; the logged catch guarantees the particular write attempt failed. Treat as Bug/Open in Draft PR, not Canonical. Can be fixed in a follow-up once the core AAC preservation regression and Stream Plan v4 cross-platform tests are accepted.
