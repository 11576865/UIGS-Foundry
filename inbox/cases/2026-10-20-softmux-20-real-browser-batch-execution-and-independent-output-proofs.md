# Case: 20 real browser batch jobs are a delivery-evidence gate, not a plan-count assertion

Date: 2026-10-20  
Status: **Case / scoped verified implementation and CI evidence; no Canonical promotion**  
Source: [MKV-Fast-Muxer PR #164](https://github.com/11576865/MKV-Fast-Muxer/pull/164), merged to main `c3118ae308c1d2133969a179a6ec1479c3883d36`  
Exact product test-head: `4410f53ef9f5f415904bd6741f9a1af86baf627d`  
Exact independent native Chromium CI: [run #39401811327](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39401811327) — Node 632/632, S10 20-real-media stage PASS, full pre-existing Chromium E2E PASS.  
Product acceptance record: `docs/softmux-1.0-S10-20-real-batch-acceptance-20261020.md`.

## Concrete problem

Prior batch tests exercised 2 actual outputs, worker failure/retry, preservation of Blob URL and save-only partial publication. The S10 1.0 contract required an additional **20 actual executable jobs**, not a UI matrix with 20 rows or 20 synthetic fake results. A test that checks only `jobs.length===20` could pass while later jobs lose file identity, leak source state, duplicate results, corrupt compressed media, silently shift SRT cue timing, or mark generated-but-unsaved Blobs as persisted.

## Measured corrective test

Added `tests/e2e/batch-20-real.e2e.mjs` as a separate CI stage under the 45-minute Chromium/media workflow:

1. Generate 20 distinct named, browser-authorized MP4 `File` inputs and corresponding alternating ASS/SRT files, by copying **two** already independently generated 2-second MPEG-4/AAC fixtures; share one real font. This is a stress-of-repetition basis, not source-heterogeneity proof.
2. Run production batch UI and real ffmpeg.wasm worker sequentially for 20 actual outcomes; no mock output or success sentinel. Require 20 frozen unique Job IDs/output names, 20 MKV and 20 report downloads, all product artifact audits pass. Verify that the unrelated single-project FileList remains intact.
3. On each downloaded output, compare report SHA-256 with actual MKV bytes; use native `ffprobe` to check actual codecs, subtitle track and font attachment; use `ffmpeg -c copy -f hash -hash SHA256` on video/audio to show **actual compressed bitstream payload hashes** match source; require in-app ASS Dialogue independent audit PASS or native `ffmpeg -copyts` SRT cue-by-cue text/millisecond/time parity.
4. Confirm all 20 statuses are `awaitingSave` (accurate because no destination was selected) rather than falsely claiming disk persistence, with no `auditWarning`, and source video/subtitle input byte hashes unchanged.
5. On success or failure retain machine-readable JSON evidence including names, job IDs, audits, sha, byte sizes, codec and strict coverage notes. CI stores first/middle/last three actual MKVs for independent spot checking.

## Actual results

Initial CI [#39401399455](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39401399455) was red **before running any media**: test script called Playwright `#batchStartBtn.waitFor()` while the actual production batch drawer was intentionally collapsed and button hidden. Fixed the test entry sequencing to wait for the visible main task button then open the drawer. Do not falsely label a hidden expected UI control as a product defect.

Final exact-head CI [#39401811327](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39401811327) passed:
- `S10 BATCH20 verified 1/20` through `20/20`, each native output subtitle audit PASS.
- `S10 BATCH20: 20 real jobs / 20 independent MKVs, strict output audit and retention PASS`.
- `# tests 632`, `# pass 632`, `# fail 0`, plus `All browser E2E scenarios PASS`.
- CI artifact: `s10-twenty-real-matroska-batch-evidence` (original run artifact 12255024668; subject to standard retention), JSON + three real MKV samples.
- Main merge commit `c3118ae308c1d2133969a179a6ec1479c3883d36`.

## Reusable bounded lesson

A batch acceptance denominator must count **independently verified delivered artifacts**, not UI plan rows, mock Worker invocations or FFmpeg process return codes. Each output's identity, actual compressed stream content, subtitle timing, attached resources and publication status need their own evidence. Batching multiple outputs does not make 20 generated-but-not-persisted Blob URLs into 20 saved files. Attach machine-readable evidence at exact validated commit, and distinguish repetition stress with duplicated fixture provenance from varied real-world input diversity.

## Limitations and deduplication

Foundry existing records `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md` handle ambiguous matching and destination collisions; `inbox/candidates/2026-10-14-product-block-delivery-over-pr-fragmentation.md` addresses end-to-end feature units; `inbox/candidates/2026-10-13-multi-artifact-partial-publication-state.md` handles preserving output and report partial save. This Case supplies distinct **20 artifact execution-and-independent-output evidence** and the hidden-drawer testing false start, not a replacement for those rules.

A 20-job short fixture does **not** demonstrate 20 heterogeneous feature films, gigabyte input capacity, actual disk writes, tablet stress, all chapters/tags, or full S10 1.0 acceptance. Single project occurrence; do not modify Canonical.
