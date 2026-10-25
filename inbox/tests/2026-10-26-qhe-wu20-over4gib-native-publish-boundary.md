# WU20: actual Windows Native >4 GiB transport and UInt32 boundary oracle

Date: 2026-10-26  
Project: `11576865/Quick-Automatic-Hardsub-Encoder`  
State: **PENDING exact-head Windows test until hosted evidence is observed**  
PR: [#147](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/147); initial head `ee938329a3d65dec5efc7b8cbba8220a3360c21b`

## Distinct unresolved gap

[WU19 Test](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/tests/2026-10-26-qhe-wu19-native-streaming-actual-partial-write-and-volume-identity.md) proves actual 96 MiB source→output copy, a 5 MiB on-disk partial write failure/retry, and a distinct-volume output with Win32 volume serial comparison. It does NOT prove the product's `Int64`-based `FileStream` copy succeeds past the **UInt32.MaxValue 4 GiB** boundary. That is a new Test, not a duplicate general staging Candidate nor a reason to change Canonical.

## Submitted evidence plan

QHE [PR #147](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/147) introduces `scripts/check-wu20-native-over4gib-publish.ps1` and a distinct Windows 25-minute CI workflow, not an alternative product save implementation. The test will only PASS upon the following actual file-system evidence:

- A source with exact length **4,295,032,832 bytes (4 GiB + 64 KiB)**, using NTFS sparse *only on input fixture* for bounded hosted-runner disk consumption. Actual nonzero markers are physically written around signed 2 GiB and unsigned 4 GiB boundaries.
- Initial Win32 `GetDiskFreeSpaceEx` on selected output volume must report enough capacity for **the full 4 GiB+ output plus 1 GiB safety margin**; lack of space should FAIL the test, not silently skip or claim pass. The actual temporary output is a regular file, never flagged sparse, and every byte must traverse the production **1 MiB buffer**.
- Actual failure after at least 2,147,484,672 bytes written into that temporary file; destination's old SHA unchanged, verified source unchanged, temporary file removed; rerun the same source stage and re-copy all 4 GiB+ before publishing.
- Independently compare full `SHA-256` of initial source, complete temporary and final published file; read actual marker bytes at absolute 64-bit offsets around 2 GiB, 4 GiB and file tail. The destination must not be changed before `Publish-NativeProtectedOutput`. Process peak working set must stay under 768 MiB, preventing accidental load of whole 4 GiB source into RAM.

This test uses genuine filesystem bytes, but its source is **synthetic sparse binary, not a 4 GiB encoded movie or MKV**. It cannot support full-film playback/decode claims. WU19 already proves genuinely distinct volumes for 96 MiB, not for this 4 GiB run. It also does not establish actual full-disk exhaustion, loss of network/USB connectivity, SMB/NAS, power failure, consumer hardware tests or concurrent process identity races.

## Intake

Foundry dedup queries for QHE WU20, Windows file lengths and 4 GiB boundary returned earlier WU19 and shared-staging candidates but no WU20 boundary Test. Keep one scoped Test record, update it only with **real exact-head CI and merge checks**, never silently promote Canonical.
