# Case: Secondary CueTime proof must not erase already-valid CueTrack/Block evidence

Date: 2026-10-24
Status: **Case / implementation and regression submitted; exact-head CI pending, not Canonical**
Product: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/198
Product branch: `feat/softmux-s12-cue-timing-proof-20261024`
Base product main at review: `dbd35c3c471bc3bb20af5fe195041462c3a46154`
Related Foundry Case: `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`

## Actual code review observation

A read-only S12 scanner already proved a Cues reference's TrackNumber and real SimpleBlock/BlockGroup header under a fixed visit budget. Adding a **more demanding** CueTime-to-Block timestamp proof changed the shared loop condition to continue while pending timing remained, using the same `ctx.visits` budget and the same full-candidate comparison list.

Automated [Codex review on PR #198](https://github.com/11576865/MKV-Fast-Muxer/pull/198) identified two separate risks at head `7ed3955bfacb1ecc9cb4d873092a7b084aede577`:
1. On nondefault TrackTimestampScale or nonzero CodecDelay, no timing proof is eligible, but pending time references keep scanning thousands of Cluster child headers. Hitting the shared global budget can reset an otherwise established `CUE_TRACK_BLOCK_HEADERS_VERIFIED` to `CUE_BLOCK_EVIDENCE_UNVERIFIED`.
2. For large numbers of references and block candidates in one Cluster, each newly seen candidate causes every pending reference to re-search the entire accumulated array; this is O(R × B²) comparison work without a comparable CPU budget.

One additional test-helper finding was already fixed on the product branch before this intervention. Exact earlier PR #198 head `ba3284df00745754e43e52693482d8e82d1558a6` had passed Node/Pages/Chromium/S12 real-media CI, but those green workflows did not invalidate the algorithmic review findings.

## Submitted correction

Product PR #198 now separates the **header proof** scan and **time proof** scan:
- The header pass stops once the required actual Track/Block and CueRelativePosition boundary facts are established; it does not traverse the rest of a large Cluster solely to pursue timing.
- The timing pass has a separate `ctx.visits` budget and per-Cluster child cap. Unsupported per-track scale/delay is reported immediately without any timing-only scan.
- In each Cluster, actual parsed Block headers are indexed by `TrackNumber : signedBlockTicks` with sets of their genuine direct child offsets. Cue matching consults the index once per reference, O(B+R) instead of repeated candidate-array scans.
- A failed or exhausted secondary timing scan reports `CUE_BLOCK_TIMESTAMP_UNVERIFIED` and reasons, **not** a regression of a previously proven `CUE_TRACK_BLOCK_HEADERS_VERIFIED`.
- Newly added Node fixtures cover a tight timing-only budget after a successful header proof, unsupported scale/delay plus extra real Block headers, and hundreds of unmatched CueTimes with bounded Blob.slice reads. Files remain read-only and no media payload/writer authority is introduced.

Product code commits submitted on PR #198: `38e861009ef705476e4b3eea705004340dc7d15c`, `0253054ade0fca300641797eeb1f47cfae3895a2`, `61eb266c8be498f9cd9ff52db428733a0ba9615c`, documentation `9ca50b87ac32ed8b30a8e4fddbd9bd1b6e6c44a5`.

## Transferable engineering observation

A stronger **supplemental evidence check** must not consume the budget needed for an independent weaker proof or downgrade its established result due solely to the additional check's refusal. Treat them as separate evidence contracts with separate resource budgets and failure paths. A per-element hard limit is not a CPU-complexity guarantee: test reference-to-candidate join complexity as well as byte access size.

This observation is implementation-backed and currently **Pending exact-head CI**. It does not establish general Matroska packet identity, decodability, authorisation to write, actual target-device performance, or long-duration stability. It is a Case, not a proposed revision to any UIGS Canonical standard.

## Deduplication

The 2026-10-12 Matroska preservation Case already requires **scoped independent output oracles** and explicit `notChecked` claims; this new Case adds a different observed failure mechanism — *independent proof resource consumption causing regression in already-established evidence* — plus its concrete complexity and budget regression. The 2026-10-04 interface-as-evidence Candidate concerns visible vs inferred hidden state, not the bounded parser's independent proof budgets. Do not duplicate or promote either source automatically.
