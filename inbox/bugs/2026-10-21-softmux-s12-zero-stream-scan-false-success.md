# Bug (Pending CI) · Source MKV FFprobe empty stream list reported as successful scan

Date: 2026-10-21
Product: `11576865/MKV-Fast-Muxer`
Reproduction / actual large-source diagnostics: [PR #170](https://github.com/11576865/MKV-Fast-Muxer/pull/170)
Bounded proposed fix: [PR #171](https://github.com/11576865/MKV-Fast-Muxer/pull/171)
Status: **Observed browser product defect; candidate fix Pending exact-head CI; NOT Canonical.**

## Dedup
Existing `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` documents that native parser, Wasm runtime, admission limits and physical memory success envelopes differ. This record is a narrower **actual product failure**, not a new general Candidate. Foundry search found no existing source MKV zero-stream-success Bug.

## Evidence
- Baseline product `0.1025.0`, normal `scanSourceContainer` in `src/main.js`, uses full `fetchFile(video)` / `ffmpeg.writeFile` followed by `probeInput` and blindly assigns `trackState`. A valid ffprobe JSON response with an absent/empty `streams` array is converted to `[]` in `runProbe` and the UI says `轨道扫描完成：0 个流 · 0 个附件 · 0 个章节。` instead of signalling unverified source.
- [S12 CI #39557148027](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39557148027) actually generated distinct real Matroska files (native ffprobe validates original video+audio+16/19 original 64 MiB data attachments), using non-sparse random bytes. Browser 1,000,000,128 B and 1,200,000,000 B both reported 0 streams and misleading `scan complete` status; the stricter test then correctly failed before attempting mux.
- Same CI's 64 MiB **control PASS**: actual browser/Wasm completed, downloaded ~67.15MB MKV, independently validated native video/audio/subtitle/attachment and original attachment data full SHA-256. This does not establish a universal 64MB limit or prove >1GB memory death. At initial intake, 512 MiB job was still in progress.
- `src/probe-policy.js` `decodeStreams` option currently does not change ffprobe flags; a nominal fallback on empty JSON is not a viable new probe mode without further runtime work.

## Submitted bounded code fix
- [Product PR #171](https://github.com/11576865/MKV-Fast-Muxer/pull/171), initial head `ae1b44481d6a9c19798d44da27b39883b4c21320`: `requireObservedSourceStreams` asserts an actual non-empty collection before the main source trackState is set; if FFmpeg/Wasm returns empty streams, mark the scanned generation unverified with a visible error and temporarily suppress automatic same-source endless retries. Explicit user retry clears suppression and a new File starts anew.
- Independent attachment-only read-only inspector remains separate and is not blocked. No hard-coded 1GB admission cap added.
- Node tests cover missing/null/empty streams and pass-through valid video/audio or attachment observed arrays. The proposed development version is `0.1026.0`.
- **Exact-head Node/build/Chromium/S10 status Pending**. No claim that this fix improves large-file success, changes the actual memory path or closes S12 acceptance.

## Follow-up
Classify 512 MiB job and >1GB scan behavior by actual browser stage, JavaScript console, native source structure and sampled RSS. Larger realistic high-bitrate/video-stream source plus target desktop/tablet must still be tested. The S12 pressure-run completion and PR #171 product fix have separate merge/release criteria.
