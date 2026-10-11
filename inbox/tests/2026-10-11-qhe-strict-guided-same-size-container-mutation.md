# Test: strict QHE guided output rejects equal-length content changes

Status: **Pending CI / submitted regression**  
Date: 2026-10-11  
Project: `11576865/Quick-Automatic-Hardsub-Encoder`  
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/90  
Submitted commit: `bfbc6b502d5fe6fe6c297ff55096095cda4bb17d`

## Risk

An output can preserve its exact byte length while the contents change after a successful decode/stream/packet check. A strict ceiling alone rejects oversize files, **not** a different same-size file. The previous #87 guard compares stage/copied lengths and previously successful state; a same-size corruption is a separate integrity acceptance boundary.

## Regression

Windows localhost Bridge + real FFmpeg synthetic two-pass H.264 execution:

1. Produce and verify a strict under-limit staged MKV with two copied source audio streams.
2. Locate its private completed output; flip one byte in-place without changing file length.
3. Advance its write timestamp to trigger the conditional status fingerprint recheck.
4. Require the completed status to become failed, removal of the corrupted stage, and export API refusal.
5. Retain the original oversize-tamper regression and the successful strict/two-pass checks.

## Implementation

`windows/native-bridge.ps1` takes a SHA-256 fingerprint of the stream/packet-validated staged container at terminal strict completion. Terminal status avoids repeated hashing when byte count and modification timestamp are unchanged, but invalidates a changed-time file on digest mismatch. Strict export must hash the copied private temp file and match the original approved digest before publishing.

## Evidence boundary

**This test is not yet reported passed**; it was newly submitted with PR #90. Stage-time stamp checks are a performance optimization, not a cryptographic integrity guarantee. Hashing the copy protects its match to the verified staged content at that check, but does not impose a permanent OS-level file lock across publication. Full decode, GPU/HDR/VFR/long-form performance and real user save-dialog acceptance remain separate.

Related Candidate: `inbox/candidates/2026-10-04-private-staged-mutation-publish-only-final-verified-output.md`. No Canonical promotion.
