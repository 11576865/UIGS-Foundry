# Bug: Legacy Guided Native output accepted copied-audio size estimates without validating the measured source receipt

Date: 2026-10-13
Status: Fixed in open QHE PR #105, Windows hosted synthetic runtime PASS; field/physical acceptance Pending
Affected interface: Guided ASS size planning -> Windows Native /api/encode legacy request
Source: 11576865/Quick-Automatic-Hardsub-Encoder

## Defect and scope

Guided ASS `assessGuidedWholeFileBudget` had been aligned with Manual's full-container per-stream ledger: copying audio in size mode required measured source packet bytes. But `main.js::runNativeEncode` still constructed the *legacy* `request` without `budgetEvidence`. Unlike `Start-MediaTaskJob`, `windows/native-bridge.ps1::Start-EncodeJob` did not bind those costs to the Windows-selected file at job creation. Thus a measured-size calculation could be used to construct a Native execution request even after its source-cost receipt became stale or absent. This was found by source call-path inspection, not by claiming a malicious exploit was observed in the field.

## Bounded correction

- QHE `aab97eb5c695f65eefa5617717747b72e51c58c6`: include source-scoped `budgetEvidence` for Guided Native budget-rate jobs that copy one or more audio tracks; refuse to create that request without `measurementId`.
- QHE `579d0258983653b3df95b1e389cd4854cab126b9`: `Assert-CurrentCopyBudgetEvidence` checks measurement ID, Windows selected source path, current size and modification ticks, plus **every copied-audio packet byte total against Windows's locally stored measurement**. Called by legacy Guided and pre-existing formal Manual task path. A receipt token alone cannot substitute altered client-entered cost bytes.
- QHE `317b398795d1fad380c49fbe5fbc97a802365c20`: Windows Bridge negative regressions for absent, stale-ID and altered byte totals, while preserving positive copy/two-pass and strict byte ceiling testing.
- QHE `24cbe98288932b320afe6b137fcf3a111c55127d`: frontend source-contract test asserting Guided request/backend receipt path.
- QHE `09ce78c5d06ba5670dfa48008e683c986a620fe9`: Windows real Bridge two-audio output verifies ordered copied packet SHA-256 hashes, measured byte totals and actual container bytes.

## Evidence

Windows local smoke `38427736645` completed with **SUCCESS** for the missing/stale/tampered cost refusal tests and existing real two-pass/strict checks (preceding SHA `24cbe98`).
New exact-code Windows local smoke workflow `38427973572`: the `Exercise real guided Windows Native two-pass and strict byte ceiling` step completed with **SUCCESS** after the real copied-audio SHA-256 comparison was added. At initial intake the overall workflow was still running later unrelated steps; do not promote step PASS to full exact-head workflow success unless separately checked.

## Reusable rule (provisional)

For planning driven by externally measured resource costs, propagate the measured evidence's source identity and immutable payload snapshot into the execution boundary; the owning runtime must revalidate both source and cost receipt at the last trusted task start, not merely at UI plan time. Do not confuse a source-scoped packet budget with final output quality or a universal target-size guarantee.

## Dedup and limits

Existing `inbox/bugs/2026-10-13-qhe-guided-size-frontier-not-refreshed-after-measured-cost.md` addresses stale cross-view projection after updates; this Bug addresses **execution-time native receipt authorization**. Existing `inbox/tests/2026-10-13-qhe-guided-ass-measured-multiaudio-whole-file-budget.md` concerns Linux FFmpeg and browser fixture; this Bug's separate Windows reproduction has its own Test record. Source path/size/ticks are lifecycle checks, not a cryptographic content identity for an adversarial same-size, same-timestamp in-place file replacement. No physical workstation, long movie, rich video, source-referenced ASS SSIM or external player guarantee; no Canonical change or merge.

## Follow-up: client cannot waive receipt by declaring zero audio tracks

Further source inspection showed the legacy request's `expectedAudioTracks` was client-supplied. The initial guard used it to decide if a copied-audio receipt was necessary; a malformed/spoofed zero count could suppress the guard while FFmpeg still maps `0:a?` from a source with audio.

QHE `775bf4b6a50d44f1e4a313d4f96c95da3ada0d8c` now probes Windows's real source stream count before enforcing the receipt, requires the declared count to equal the Native-probed count for Guided size + copy, and requires `Assert-CurrentCopyBudgetEvidence` whenever the *probed* count is positive. The new zero-track negative acceptance case was added at `f0dbe3c918cc4b9183f844e74794695e28f7b80f`; source contract updated at `ad917ef050f88158b67592c7cd05d5a1dde1cb22`. CI exact-head Pending at initial observation.

This is an additional dimension of the same defect, not a separate Canonical rule: the decision to require provenance must be made from trusted runtime source facts rather than a mutable request field.
