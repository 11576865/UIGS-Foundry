# Test: QHE VBR-approved codec → real Windows Native full formal v4 HEVC output, independently verified

Date: 2026-10-13 (Asia/Shanghai); CI timestamps 2026-10-12 UTC
Status: **PASS hosted Windows integration**, final exact-head five-workflow rerun pending at initial publication
QHE draft PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104
First passing Windows full-output CI run: `38284134399`, PR head `891620f8027959f7ffdc671b710c0d2c57340211`
Related but separate Tests: `inbox/tests/2026-10-13-qhe-manual-vbr-verified-atomic-task-handoff.md` (formal plan compile/form only); `inbox/tests/2026-10-13-qhe-manual-native-vbr-gate-and-readout-consistency.md` (two short VBR samples); `inbox/tests/2026-10-12-qhe-native-bridge-paired-x264-x265-comparison.md` (actual short CQ).

## Actual path exercised, without mock encoding

1. Windows FFmpeg generates a 5.0-second 320x180/12fps single FFV1 video + single FLAC audio stream Matroska source. `windows/native-bridge.ps1` selects it through `-InitialVideo` and reports source facts via `POST /api/probe`.
2. Same Windows Bridge runs 12 actual source-referenced CQ+SSIM experiments: libx264/libx265 × CRF 18/28/40 × two 1.5s source windows. Then **libx265** runs 2 real VBR bitrate-mode windows at a requested 600000bps. `verifyManualNativeVbrCandidate` admits the 2 real VBR receipts and verifies the identical source/runtime/reference/encoder/preset.
3. `scripts/build-manual-adopted-native-request.mjs` requires the real VBR certificate to pass, uses the existing `commitVerifiedManualCandidate` form transaction and production `compileTask` v4 to produce a complete **HEVC/libx265 bitrate-mode 600000bps + copied FLAC** formal task JSON. This is not an invented FFmpeg CLI replacing QHE task compilation.
4. `POST /api/encode` genuinely launches `windows/native-bridge.ps1::Start-MediaTaskJob` with the formal `task.outputArgs`, and `GET /api/jobs/<id>` reports `completed`.
5. An independent verifier `scripts/verify-manual-adopted-native-output.mjs` runs FFprobe on source AND output and checks one output HEVC video at the exact dimensions, one copied FLAC audio stream, all audio packet payload SHA256 in order identical, source/output frame count, full duration, whole container byte count equal to on-disk size/FFprobe/Native status and a **full-duration separate** FFmpeg source-vs-output decoded SSIM (not the two CQ/VBR windows).

## Empirical results (specific five-second synthetic source only)

- QHE formal output: Matroska + HEVC/libx265 video + copied FLAC audio.
- Exactly 60 source and 60 output decoded video frames, source/output duration 5.000s.
- 235 source FLAC audio packet SHA256 hashes identical to all 235 output payload hashes in order.
- Requested video target bitrate = **600000 bits/s**, nominal requested 5s video bytes = 375000 B, **not a whole-container target**.
- Entire actual output Matroska file = **358516 bytes**, independently matched to FFprobe and native status.
- Independently computed **full-file source-referenced SSIM = 0.999738** for this synthetically generated source.
- At two VBR short windows the same HEVC source-reference measurement minimum was around **0.99936**; this and the full-clip metric are distinct measurements.
- This is an actual Windows-hosted Native production encode and verification, not simulated JS; it is still a generated short-video fixture, not field user media.

## First red / repaired cause

The first end-to-end `POST /api/encode` was rejected **before encoding** when Windows PowerShell sent a string JSON body containing non-ASCII Chinese compatibility warnings; Bridge reads UTF-8 bytes according to Content-Length and `ConvertFrom-Json` failed with `Invalid array passed in, ',' expected`. The exact job after changing the PowerShell client to `[Text.Encoding]::UTF8.GetBytes($requestJson)` and charset `utf-8` passed. Do not report the first red as an HEVC encoder issue. Separate Bug: `inbox/bugs/2026-10-13-qhe-windows-native-json-request-utf8-bytes.md`.

## Evidence preservation

QHE's independent `Windows Manual paired codec acceptance` workflow has been extended to upload only CI-SYNTHETIC source media, the actual produced HEVC output, and a machine-readable independent check JSON (14-day retention). The artifact must be checked against the *final exact HEAD* rather than assumed present from the first green run. These generated files enable replay without uploading any user's private media.

## Remaining scope

The source is only 5s synthetic SDR 8-bit, one FLAC, one video stream, no subtitles/attachments, no external player/physical Windows end-user workstation test; no AV1/NVENC, HDR, VFR, real multi-language audio, realistic scene dynamics or long-duration sampling, no asserted strict whole-container size upper bound, and no Windows save-dialog exported-file acceptance. An observed 358516B whole-file size is **not** a strict video budget guarantee. PR remains Draft/unmerged, Test only; do not promote to Canonical.


## Final exact-head five-gate closure and replayable artifact

QHE draft PR head `cbc8345b3670d8195055fa68776f6b247213070a`: **all 5 workflows success** on that exact commit:
- Test frontend: `38284619884`.
- Windows Manual paired codec acceptance **with actual formal 5-second HEVC output**: `38284620192`.
- Windows local smoke: `38284619879`.
- Windows Stream Plan v4 runtime acceptance: `38284619950`.
- UIGS Evidence Coverage: `38284619839`.

Workflow `38284620192` uploaded artifact `11762832734`, `manual-native-full-output-evidence` (14-day retention): `synthetic-ffv1-flac-source.mkv` 488831B, `verified-hevc-flac-output.mkv` 358516B, `full-output-acceptance.json` with the exact observed independent metrics. Downloaded the actual artifact in this conversation and checked its three member filenames/sizes. **A second local FFprobe verification of the extracted real media files**, independent from Windows-hosted CI, established source streams FFV1+FLAC, output HEVC+FLAC, 235/235 audio packet SHA256 hashes equal and 358516B actual output size. The full-timeline SSIM=0.999738 and frame-count/length gates remain established by the Windows dedicated verifier; the second local check reran the stream and FLAC-hash/byte subset only. Keep the distinction between these evidence layers.

All metrics are for this CI-generated five-second synthetic fixture. No real-world target-size or playback guarantee is implied. Candidate/Test only; no Canonical change and no merge.
