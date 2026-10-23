# Bug — HSR final publication marker commit not covered by rollback; legacy cleanup preflight happens after deletion

Date: 2026-10-23
Repository: `11576865/HSR-Voice-Archive-Builder`
Base HSR: `main@6a6410b0181b82e60528fe52f4e807911b430f4d` (PR #203)
Level: **Bug / deterministic source-path + fault-injection tests**
Status: **PR #204 under review; mainline not yet merged/accepted**
PR: [#204](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/204)

## Context and distinct faults

Following the full-MKV build marker fix in #203, a source-level audit found two later-stage commit boundaries not covered by that fix.

### 1. Marker commit failure after the rollback handler

`app/publishing.py` `preserve_published_archive(output,state)` backed up generated media, stages and receipt, then performed the build in a `try: yield ... except BaseException:` rollback section. However the final `.build_in_progress` marker removal was executed in the **`else:` section after the rollback-catching try body**, so a permission/I/O error at that final commit step would escape without restoring the previous coherent archive, leaving a new receipt/files behind with an apparently incomplete marker.

Correction in PR #204: move `marker.unlink(missing_ok=True)` inside the protected `try` immediately after `yield`. On failure, the existing rollback restores the last coherent published media, receipts and stage files. If marker deletion later succeeds, return to the old verified state; if deletion remains impossible, the old coherent file set is restored but the marker is kept for fail-closed public freshness.

### 2. Legacy output symlink rejection after destructive cleanup

`app/delivery_artifacts.py` `seal_complete_delivery` checked working FLAC, ASS and SRT safety but wrote `sealed=true` and unlinked the working sources **before** checking that `HSR_Voice_Archive_Black.mkv` was not a symlink. Standalone `seal_complete_delivery` calls without an outer rollback manager could return a late safety error after having already altered the receipt and removed working inputs.

Correction in PR #204: preflight this final legacy cleanup path before changing any receipt or deleting a working source. Retain the symlink safety refusal; do not bypass it.

## Reproduction and tests

`tests/test_owned_build_mkv_seal.py` adds three portable fault-injection cases to the prior #203 owned-marker suite:

1. Simulated unsafe legacy path on an otherwise verifiable standalone MKV: refusal leaves previous unsealed receipt bytes, FLAC/ASS/SRT bytes, legacy file and actual MKV untouched.
2. Fail the exact final marker `Path.unlink` once: verify the transaction raises, rolls back to previous sealed MKV and receipt, resets transaction ownership and returns to public `current` after second marker deletion succeeds.
3. Fail marker unlink persistently: old sealed MKV and receipt restored, context ownership reset, busy marker remains, public `stale` rather than false verified `current`.

The tests use fixture bytes for journal/receipt path behavior, not audio decoding. Existing FFmpeg+FFprobe real-media suites and full Python/Windows/ASS CI are required to accept the fix; physical Termux and power-loss tests remain FIELD-PENDING. This does not claim multi-file hardware ACID durability.

## Dedup / normative guard

This is different from `inbox/bugs/2026-10-23-hsr-build-marker-vs-mkv-seal-verification-deadlock.md`: the previous Bug concerns **the build's own marker blocking internal validation**; this one concerns a **failed final marker removal outside rollback** and **late preflight after data deletion**. Foundry searches for “HSR final build marker unlink rollback failure”, “seal complete legacy black mkv symlink discarded source”, and “HSR file cleanup preflight mark sealed” returned no duplicate.

No Canonical edit or automatic promotion. Update this Bug with exact-PR-head and exact merged-main CI only when actually verified.
