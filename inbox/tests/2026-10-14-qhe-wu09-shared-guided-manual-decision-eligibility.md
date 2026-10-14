# Test: QHE WU09 shared Guided/Manual evidence-to-recommendation eligibility gate

Date: 2026-10-14
Status: PASS — bounded pure model + production Chromium JS/visible UI control; independent Windows Native final media not tested in this slice
Source PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact tested source SHA: 6ea0bea2b5d2e0ae467ccd9cf5310e3982f0388c
CI: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38592703806
Related CI: Test frontend 38592703737 SUCCESS; UIGS Evidence Coverage 38592703764 SUCCESS
Owner report: R19 §16 P3, Supplement B and R24 §13–18; B04/B11/B12/B13/B14

## Dedup and distinctive new evidence

Foundry Candidate `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md` already defines the generic boundary between curve diagnosis, local recommendation and globally optimized decisions; Foundry Test `inbox/tests/2026-10-14-qhe-b11-guided-ass-rendered-quality-evidence-invalidation.md` covers ASS content/source/runtime/font reference invalidation; prior Manual VBR Tests own the actual Native provenance and atomic application. WU09 adds a **single common UI-facing executable eligibility gate** reused by BOTH workflows, distinguishing whole-file vs video-only budgets and preventing conditional recommendation when copied audio cost is unknown. It is a Test, not a new normative Candidate or Canonical rule.

## Product contract

`src/shared-evidence-decision.js` accepts a workflow discriminator, separately established decision-reference scope, current scope, already-built frontier, currently selected target bytes, budget coordinate and optional independent VBR receipt. It returns a frozen diagnosis/recommendation/VBR-only eligibility object, never writes a task or codec. Guided reference must have `guided-ass-rendered` domain, Manual must have `manual-source-sdr` domain; they are not comparable SSIM evidence. Scope drift, outside-sampled-domain target, missing finite bitrate/quality or invalid frontier fail closed.

Guided `src/main.js` and Manual `src/manual-transcode-compare-ui.js` now use this common classifier. A video-payload-only view remains diagnostic, not a full-mux recommendation; Guided copied-audio-cost-estimated budget also cannot spawn a codec-branch proposal. Formal Native VBR verification and user-confirmed atomic codec adoption remain under their existing independent workflow-specific validators; `canCommit` on this new view alone cannot bypass those.

## Falsifiable tests and exact-head results

- Shared Node suite tests both workflow scopes, cross-domain mismatch, stale reference, missing/invalid sample, outside tested target interval, video-only and estimated-copy diagnostic-only modes, VBR receipt matching its scope, selected branch, budget and bitrate, plus explicit approval prerequisite.
- Integration passes actual `fitRateDistortionModel`, `createMultiBranchFrontier`, `projectWholeFileFrontier`; two codec candidates rank only inside common sampled budget and measured whole-file cost coordinates.
- Production Vite/Chromium imports the same shipped JS module, exercises two real fitted frontiers under both reference identities and verifies that without Native sampling the Manual adoption control remains disabled. It checks the actual Manual UI defaults to whole-file and that an explicit video-payload diagnostic option exists; the hidden Native-only comparison controls are not artificially forced open.
- First Chromium attempt failed only because acceptance code tried to `selectOption` on an intentionally hidden Manual comparison selector before Native evidence existed; script changed to assert the negative preflight and module semantics. Exact head `6ea0bea2...` WU09 run `38592703806` SUCCESS, frontend run `38592703737` SUCCESS.

## Non-claims

These are generated fitted unit samples and controlled Chromium execution, not a new live Windows Native paired x264/x265/ASS reference run, not whole-file size/quality evidence and not hardware/device playback proof. One gate layer is completed; P3 and B04/B11/B12/B13/B14 remain partially implemented. No Canonical promotion.
