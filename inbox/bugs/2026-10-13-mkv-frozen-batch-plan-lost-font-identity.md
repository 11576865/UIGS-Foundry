# Bug: Frozen batch plans must carry derived resource identities needed by execution

Date: 2026-10-13
Status: **Bug / confirmed Chromium regression; correction pending exact-head CI**
Product: `11576865/MKV-Fast-Muxer` PR [#105](https://github.com/11576865/MKV-Fast-Muxer/pull/105)
Failed exact head: `b7ad5f65755004f743fb6c9ad6736156a42c2fa8`
Failed browser run: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38326334935

## Actual failure

Chromium E2E `scenarioBatchGroupSubset` exercised a two-episode batch with a renamed-but-content-recognized TrueType font and Group subsetting enabled. The first output MKV's real attachment name was `BatchSharedFont.ttf`, not the independently expected `*.subset.ttf`. The test rightfully failed; do not remove this assertion or call Node/build success a release acceptance.

## Causal source review (inference, correction submitted)

The legacy `buildGroupedSubsetFonts(fonts, pairing)` consumes **both** selected File objects and the per-file `pairing.fontRecognition.recognized[]` identities to construct `fontIdentity` input for `subsetFontItems`. Round 2 froze `fonts` and `jobs` but originally omitted `fontRecognition`; the real caller now passed this incomplete frozen plan instead of the full pairing. That loses type/provenance evidence even though each input File reference survived. Without identity the Group subset route may fall back to attaching the unsubsetted font. This diagnosis is based on the exact changed source and failed browser output; correction still requires E2E rerun.

Correction submitted to PR #105: freeze the content-derived recognized-font inventory alongside the font File references and add a regression asserting that the identities are present and unaffected by later recognized-array mutation.

## Reusable test boundary

A migration from mutable runtime state into an immutable `JobPlan` must inventory **execution dependencies**, not just the visible files and UI options. Derived recognition, permissions, relationships and contextual evidence can be operational inputs. Use a real behavioral oracle (here the produced Matroska attachment) to detect missing evidence, because isolated plan immutability tests can pass while behavior silently changes.

Related Candidate (not duplicated): `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md`. Do not promote to Canonical from a single case. Exact-head corrected CI/real output remains **Pending**.
