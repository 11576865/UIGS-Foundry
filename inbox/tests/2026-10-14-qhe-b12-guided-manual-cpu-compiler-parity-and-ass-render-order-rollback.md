# Test: Guided → Manual CPU transfer requires authoritative executable-task parity

Date: 2026-10-14
Source product: `11576865/Quick-Automatic-Hardsub-Encoder`
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Product commit: `281b41254b9f1b2e86adfdd5a494000b14d13130`
Status: code implemented; Draft-fast Node and actual browser/Windows FFmpeg field acceptance Pending.
Requirements: B04/B11/B12; full B01–B25 / A01–A10 theoretical initial version not closed.

## De-dup and new scope
Existing `inbox/candidates/2026-10-12-intended-reference-and-subtitle-render-order-for-media-qa.md` proposes a general media-quality **intent reference** with crop/scale/ASS order and color provenance. This is NOT a duplicate Candidate. This Test specifies and checks a particular **executable task compiler transaction** crossing two QHE UI strategies, and independently uses the existing `src/media-verification.js::hardsubReferenceFilter` reference-frame oracle.

## Defect boundary
Before the work, `guidedTaskSettings` could copy the Guided codec/target size to Manual UI without preview-compiling the authoritative `compileTask` or proving the resulting byte budget/bitrate/ASS filters. It implicitly used the Manual form's prior `sizeReserve` and other advanced settings, emitted Lanczos scaling where Guided Native used bicubic, and used the Manual filter order **scale → ASS** where Guided Native used **ASS → scale**. This can change rendered glyphs and the compression reference even when the codec and target bytes match.

## Test contract and implementation
1. An executable source-scoped CPU handoff must compile a versioned `compileTask` **before** any UI mutation using the real source metadata and full-source measured copy-audio packet evidence. A stale or missing copied stream measurement rejects the plan; no guessed audio payload.
2. Strict byte limits and two-pass policy must survive, with the authoritative fixed 4% reserve, exactly the intended target file bytes and target video bitrate, software encoder/preset and output container/geometry.
3. An explicit `subtitleRenderOrder` field distinguishes the legacy Manual default `after-scale` from Guided's `before-scale` pipeline; the latter compiles the exact `ass=__ASS__:fontsdir=__FONTS__,scale=...:flags=bicubic,pad=...` chain, rejecting silent inherited crop, alternative fps, extra filters or encoder flags. The existing `hardsubReferenceFilter` reconstructs the same order.
4. The Guided→Manual UI first validates the compiler plan, then applies the form once, re-reads and recompiles actual accepted settings against every executable FFmpeg argument and stream-cost projection. If any difference is found, roll back the old form and report rejection; a failed rollback is an explicit error. Only after success may the workbench switch into Manual strategy.
5. The handoff creates a **new software CPU** task; Guided Native NVENC, ASS SSIM/CQ evidence, source/runtime-specific VBR certificates and final movie verification are explicitly **not transferred**. GPU/Web/Android equality is not asserted.

## Bounded evidence and pending
- `src/guided-cpu-compiler-contract.js` + `src/guided-cpu-compiler-contract.test.mjs`; real `src/media-task.js`, `src/media-workspace.js` and `src/guided-task-handoff.js`.
- Eleven source-equivalent isolated V8 tests passed with the repo's actual `compileTask`, stream, budget, media-time and output-container modules. Includes copy-audio cost, strict policy, ASS filter order, stale source, oversized/incorrect costs, preset failures and form rollback.
- The independent existing reference filter was evaluated at timestamp 2.5 s and preserved the ASS-before-bicubic-scale ordering. This is not an FFmpeg pixel comparison.
- Test suite added to Draft-fast and full `Test frontend`; source push's immediate one-time workflow read found `Test frontend` queued, `Windows local smoke` in progress and heavy paths skipped; no external PASS claimed.
- Browser DOM application, real FFmpeg ASS shaping/fonts, NVENC strategy and Android/Web output remains Pending. Neither a common compiler nor short sample evidence guarantees final file size, visual similarity or physical-player delivery.

## Promotion policy
This is a Test-level implementation and evidence observation, not Canonical. Do not automatically generalize Native Guided render order to every Manual/crop/compositing use case; Manual default intentionally remains unchanged. Full theoretical initial-version requirements are not closed.
