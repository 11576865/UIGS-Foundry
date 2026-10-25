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

## Verified Windows evidence and merged main

At product PR [#147](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/147) exact head `ee938329a3d65dec5efc7b8cbba8220a3360c21b`, **2/2 applicable checks completed SUCCESS**: the newly added independent [Windows WU20 40225139690](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40225139690) and UIGS Evidence Coverage. This is **not** a claim of 10 older checks being rerun, since those workflows were not applicable to this tests-only PR.

The real Windows job [log](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40225139690) recorded:
```
WU20 REAL OVER-4GIB WINDOWS NATIVE PUBLISH PASS:
 sourceBytes=4295032832
 realPartialBytes=2148532224
 fullCopyBytes=4295032832
 finalSha256=79060B6A9A5300215CDA491F8BBA698C68343C661C031E5500A51116E656123C
 processPeakBytes=109547520
 sourceFixture=NTFS_SPARSE_BOUNDARY_MARKERS
 output=FULL_REAL_NONSPARSE_FILESTREAM_WRITES
 encodedMovie=false
```

The file is 4 GiB + 64 KiB, passing the 32-bit unsigned threshold. A first copy actually wrote **2,148,532,224** bytes before injected failure. It was cleaned and the same original stage was re-copied to full length, independently SHA-256 verified including checked bytes around both signed 2 GiB and unsigned 4 GiB offsets, then published with the same SHA. Peak PowerShell resident working set **109,547,520 bytes** (~104.5 MiB), demonstrating bounded process memory in this run. Input source was NTFS sparse with real non-zero boundary writes, output was an ordinary newly created streamed file, not sparse-flagged by test. **This is NOT a media codec/decoding test** and not proof of 4 GiB cross-volume transfer.

PR #147 was squash-merged as `main@9ec29e657ff06b941d51bfa65f2153126a8ffcb9`. Post-merge main read independently confirmed the checked-in 4 GiB+ test, its 2 GiB failure threshold, full disk SHA assertions, and the standalone Windows workflow. It did not change the already merged WU19 production copying routine.

**Acceptance classification:** `EXACT_HEAD_WINDOWS_LARGE_BINARY_DELIVERY_VERIFIED_AND_MAIN_MERGED`. Remains explicitly open for 4 GiB actual playable MKV, external USB/NAS, power interruption, physical full-disk IO failure, and hostile concurrent file access. No Canonical change, no Pending connector operation.
