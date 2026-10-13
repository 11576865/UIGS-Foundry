# Test: a quality model must retain its exact subtitle-rendered reference identity

Date: 2026-10-14
Status: implementation submitted; Node/browser/Native exact-head acceptance Pending
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact source head: `5361f490c346ff872f5930ec8c64239eea5e162d`
Requirements: B04/B11; B12/B15 related, none fully closed.

## Distinct failure mechanism
A Guided ASS quality calibration indexed by video source plus FFmpeg runtime alone is not sufficient to determine whether its SSIM evidence still describes the *current subtitle rendering*. The decoded ASS text, selected font files, forced substitutions, fallback mappings and renderer can alter the reference. Reusing prior rate–distortion points as though the rendering stayed constant can make the UI recommend a different codec, size or CRF on stale evidence.

This differs from the existing `inbox/tests/2026-10-14-qhe-b15-manual-guided-shared-paired-risk-windows.md`: B15 covers shared *sample positions* versus incompatible Manual/Guided reference **domains**. This Test covers changes *within the same Guided rendered-reference domain*, including async Native samples.

## Contract
- `src/decision-reference-scope.js`: `guidedAssDecisionScope` binds video+runtime key, active rendered ASS text, effective font metadata, forced/fallback mappings and renderer identity. `manualSourceDecisionScope` binds the separate pure SDR source Native reference/filter/paired-window protocol. Cross-domain scope equality must be false.
- `src/main.js` records and checks the Guided scope when admitting RD model branches, rendering current calibration status, evaluating the selected size frontier, compiling a calibrated CRF task, asynchronously selecting risk windows, awaiting Native samples and publishing paired refinements.
- On text/font/source/runtime change, previous measured quality observations become ineligible for the new scope; they are not silently reprojected or relabelled. Existing pure-Manual Native VBR verification and explicit form rollback stay separate.
- A shared comparison kernel is NOT evidence compatibility; an observed CQ curve is still not a full-film quality/size or VBR certificate.
- Scope fingerprint uses noncryptographic FNV-1a-64 plus length. It is only an in-process invalidation key. A source metadata snapshot is not cryptographic media file identity; do not claim tamper resistance.

## Tests and observed bounded evidence
- `src/decision-reference-scope.test.mjs`: same-length ASS text changes, font metadata/substitutions, source/runtime shifts, canonical font mapping order, changed Manual window/reference metric, missing identity, and Guided/Manual non-equivalence. Source-level wiring assertions cover the actual frontier/CRF/Native path.
- Included in Draft-fast and full frontend CI.
- Before remote push, 7 extracted pure module tests passed in a V8 JavaScript evaluator and 9 source-level guard checks passed; 3 modified modules passed JS parse checks. These checks are narrower than actual Node ESM/browser/native execution.
- Exact-head Draft-fast Node, Native ASS/font mutation in flight, full Guided ASS sample, rendered reference SSIM and actual formal delivery acceptance remain Pending.

## Dedup and status
Foundry searches `ASS font mapping invalidates codec quality evidence`, `source-only SSIM rendered subtitle stale scope`, `Guide Manual reference token identity`, `B11 ASS rendered reference`. Related B15 test and general cross-boundary candidate are not duplicate observations of within-domain rendered identity invalidation.
No Canonical modification, no complete B04/B11 initial-version claim. This is a Test + implementation candidate for later trusted acceptance.
