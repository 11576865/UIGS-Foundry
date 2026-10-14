# Test: QHE WU08 real browser File multi-source queue with independently compiled frozen source jobs

Date: 2026-10-14
Status: PASS — bounded production Chromium controlled backend + Node File identity tests; real WebAssembly FFmpeg multi-source artifacts and disk persistence unverified
Product: 11576865/Quick-Automatic-Hardsub-Encoder PR #105
Tested exact SHA: `2b42a49e94ab3fbec991451807791a5b113a4892`
CI: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38588049167
Related: Test frontend `38588049084` PASS, UIGS Evidence Coverage `38588049025` PASS
Original authority: owner R19 §16 P5 batch matrix, R24 §22 multiple independent transformation/cut jobs; B21/B02/B24. Whole B21 remains incomplete.

## Distinction from prior WU03

WU03 `src/output-recipe-matrix.js` froze different output plans for exactly ONE media source and intentionally denied source switching. QHE WU08 adds a genuinely different product use: the user picks distinct Web `File` objects and queues one independent frozen Copy/Transcode configuration for each. Execution activates the individual original `File` object, invokes source-specific media preflight/probing, then calls the authoritative existing schema-v4 `compileTask`, validate, run, output-report and save hooks. It does not simply loop commands against the same source or use source metadata from the previous queued item.

## Test contract

- Node `File` model checks object identity versus a source descriptor (name, file bytes and lastModified), duplicate-identity rejection, 1 GiB Web size guard, 8-item cap, frozen raw settings and error gates for borrowed ASS, audio plans, must-copy locks and strict size evidence.
- Production Playwright/Chromium uses the actual multi-source UI to enqueue two different user-selected File instances, then changes the editable quality field. The two distinct source activations and official v4 tasks preserve the settings snapshot for EACH source rather than reading current form values.
- Controlled backend returns independently verified result stubs; first output is handed off, second deliberately fails during save. The UI retains already handed-off output and verified second result, allows only retry-save (no second encode), and distinguishes `browser-download` handoff from independently verified disk persistence.
- After both outputs complete, user may clear completed queue records and enqueue another distinct pair without losing previous browser download handoffs or exhausting output names.
- First WU08 Chromium attempt `38586688977` failed because the test did not expand the `<details>` disclosure before trying to click hidden controls; corrected interaction. Exact-head `38588049167` SUCCESS.

## Evidence boundary and dedup

**No actual WebAssembly FFmpeg two-file encoding or filesystem verification was performed by this suite**; controlled run hooks are explicitly a browser integration test of product orchestration and compiler, not physical media correctness. Native Windows multi-file and Android SAF handling, hard-sub with per-file ASS/fonts, real-user diverse media and player/disk acceptance remain open.

Existing Foundry Candidate `2026-10-02-batch-execution-async-preflight-readiness-race.md` already captures the generalized danger of triggering batch work before asynchronous input readiness. Existing Candidate `2026-10-09-browser-batch-artifact-object-url-ownership.md` covers per-batch Blob URL lifetime. This Test adds specific QHE source-identity and download-handoff proof without inventing another Canonical rule. A browser download handoff is not an independently verified on-disk `ArtifactRecord`.
