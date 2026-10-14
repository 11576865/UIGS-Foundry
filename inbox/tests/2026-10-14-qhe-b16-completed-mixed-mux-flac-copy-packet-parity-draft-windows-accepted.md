# Test — source-bound auxiliary preflight versus completed mixed-media mux packet parity (Windows accepted)

Date: 2026-10-14
Product: 11576865/Quick-Automatic-Hardsub-Encoder
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact product head: `0bd2381c3f0a85195410e610a3cde89ca033daac`
Focused Windows run: `38513613921` — PASS
Status: **bounded short synthetic Windows acceptance PASS**, full B16 and theoretical initial version remain Partial/Pending.

## De-dup
Prior B16 Foundry Tests covered independent FLAC/trim copy *pre-encode observations* and separate *post-output* packet audits. This Test specifically checks **source/ledger and executed task-matched comparisons** between those two evidence sources on one *completed mixed-media job*, and the real Windows negative fixture that prevents fraudulent promotion. It is not a replacement for prior packet-counting contracts.

## Contract
- Source identity, full-source packet `measurementId`, native source stat FILETIME string, exact clip bounds, *actual* keyframe-adjusted trim start, Matroska container, per-source ordinal and per-output ordinal, FLAC encoder/channel/sample rate and softsubtitle map must match.
- The output must be verified completed and independently FFprobe-audited under `scope:'completed-artifact'`. No missing/negative/non-integer/overflowed packet value may enter a comparison.
- `status:'exact-observed-payload-match'` means measured auxiliary payload bytes were equal *in that already completed one-job observation*; `status:'observed-packet-delta'` records measured per-track differences. Changed source or runtime plan returns `unavailable`, not an interpolated cost.
- A comparison **never grants** `canReplaceFormalBudget` or `canCertifyFutureMux`. File-container overhead and subsequent job predictions remain outside evidence.

## Real exact-head acceptance
- Windows focused run `38513613921` on `0bd2381c3f0a85195410e610a3cde89ca033daac`: PowerShell 5.1 syntax, JS receipt/plan/parity tests, actual dual FLAC full/trim encode and FFprobe independent oracle, actual video+two-FLAC+softsubtitle Matroska mux, and actual two-audio+softsubtitle isolated copy oracle ALL **PASS**. `Test frontend` and `UIGS Evidence Coverage` also PASS.
- The Windows 3-second synthetic fixture observed two FLAC tracks with exact preflight-vs-mixed audio packet *payload* deltas of 0 bytes. This is one observed case, not a prediction guarantee or byte-identical media-file claim.
- Root-cause history: earlier run `38510258959` failed due PowerShell `$args` automatic argument shadowing; run `38513290671` proved real FLAC/mixed encoding succeeds but negative expected-stderr fixture terminated harness under `$ErrorActionPreference='Stop'`. The accepted head uses named `$Arguments`/`$muxOptions` and a bounded, independently redirected negative child with explicit nonzero exit/no receipt assertion.
- Output: `src/auxiliary-mux-reconciliation.js` plus tests and report-only workbench integration; code maintains conservative sizeBudget behavior.

## Pending acceptance
Real Native Bridge HTTP/UI with source switching; long/VFR/complex subtitles/attachments; actual mixed seek and timestamp equivalence across codecs/containers; resource bounds and restart recovery; Android/Web evidence; strict FLAC formal budget adoption after independent repeated proofs. B16 is **not closed**; no Canonical promotion from a single Windows fixture.
