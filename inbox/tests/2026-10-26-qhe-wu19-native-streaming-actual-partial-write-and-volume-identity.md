# Test: QHE WU19 streaming output, partial-write recovery, and real volume identity

- Date: 2026-10-26 (Asia/Tokyo)
- Project: `11576865/Quick-Automatic-Hardsub-Encoder`
- Product PR: [#146](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/146), initial exact Head `e01a2b5e3474f9fd12a1c695b2dd45618db49584`
- State: **Implementation submitted / exact-head Windows CI PENDING** at initial intake
- Classification: Test, not new Canonical. WU18 existing Test covers real destination-volume free-space preflight and NTFS directory permission refusal, but **not actual partial bytes left by a failed multi-chunk destination write** or actual different-volume transfer. Therefore this is a distinct test, not a duplicate candidate.

## Gap

QHE WU18 production `Export-Job` and `Export-Sample` used PowerShell `Copy-Item` to stage output on the selected destination volume. Verified post-copy SHA, final same-volume atomic publication, capacity preflight and `finally` partial temp cleanup were implemented; however the acceptance had **not injected an I/O failure after real bytes had been written into a partial destination-side file**, nor verified a substantial copy using a fixed-size working buffer. Cross-volume correctness of stage→destination must not be inferred merely from the existence of two drive letters or from the destination preflight.

## WU19 implementation / bounded Windows oracle

- Product `windows/output-safety.ps1` adds `Copy-NativeStageToOutputTemporary`: `FileStream` sequential read/write of **1 MiB memory buffers**, `FileMode.CreateNew` temp output, exact source length / transferred byte count, and flush-to-disk before success. Both production job and sample export use this function while retaining WU13-WU18 SHA checks, strict-size certificate and `Publish-NativeProtectedOutput` protections. No resumable claim: partial temp deleted, encoded stage survives for the user's existing Save-only retry.
- An isolated `GITHUB_ACTIONS=true`-only, authenticated Bridge fault `partial-write` occurs after **262,144+ actual bytes** reach the selected destination's temporary file; no caller supplies a path or failure byte offset. The WU02 shipping Chromium two-source Batch must prove first canceled save, second save physically partial then failed, old output SHA still intact, no leaked temporary file, exact completed Job reused on third save, second distinct source then encoded/saved, two final independent FFprobe/decoded MKVs and SHA receipts.
- Separate `scripts/check-wu19-native-streaming-delivery.ps1` creates actual **96 MiB** deterministic disk bytes (not sparse or arithmetic-only); injects partial failure after at least 5 MiB, checks the partial temp file really contains fewer than 96 MiB, verifies old output and staged source SHA unchanged, removes temp, restages and publishes same 96 MiB bytes with original SHA.
- The same test attempts copying 96 MiB to Windows `LocalApplicationData` from the Runner temp source, but claims cross-volume proof only when `Get-NativeExistingFileIdentity` yields **different real Win32 volume serial numbers** for fixture files. If the environment provides only one volume, output is explicitly `SAME_VOLUME_SERIAL_NO_CROSS_VOLUME_CLAIM` or `SECOND_WINDOWS_VOLUME_NOT_ACCESSIBLE`, not a false cross-volume PASS.
- Important boundary: 96 MiB is **not multi-GB / >4GiB**. Simulated post-byte failure is not actual full disk or physical USB removal. Long-film and user-driven OS SaveFileDialog remain unverified.

## Intake decision

Foundry search for QHE partial-copy recovery / volume identity found earlier WU18 Test and unrelated Softmux large-blob research but **no duplicate WU19 Test**. Write this as a single scoped Test, do not modify Canonical after one bounded experiment. Update its `PENDING` CI status only after verifying exact PR Head and workflow evidence; if cross-volume cannot be proved, preserve the explicit partial evidence state rather than silently claiming it.

## Verified exact-head Windows WU02 evidence

[WU02 Windows run 40221498119](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40221498119) **SUCCESS** at QHE PR #146 exact head `e01a2b5e3474f9fd12a1c695b2dd45618db49584`. Its log independently confirms `WU19 WINDOWS STREAMED DELIVERY PASS`: real `actualBytes=100663296` (96 MiB); actual aborted destination temp size `injectedPartialBytes=5242880` (5 MiB), old target and stage SHA unchanged, the same stage retried and published with SHA `56923CF0E20222F56DE9BC26E5A92C29603A73E65753277F7870BA24DC37BFBE`; **crossVolume=DISTINCT_WINDOWS_VOLUMES_VERIFIED** after comparison of actual Windows volume serials. This is genuine different-volume same-session data transfer, not merely distinct drive letters.

The full shipping Chromium/Native Bridge B21 `partial-write-recovery` ended `WU19 REAL NATIVE PARTIAL-COPY RECOVERY PASS`: after first Save cancellation, a genuine destination temp was partially written and the runner-gated failure occurred; no orphan temporary bytes or damage to the old user output, first completed FFmpeg job reused through Save-only, and a second distinct source exported with independent FFprobe/decoded frames/real disk SHA. Existing WU13–WU18 regressions stayed PASS. **Do not yet claim 4 GiB transfer, USB/SMB/cloud, actual disk-full or user-operated Windows dialog.**

At this evidence checkpoint **9/10** whole-head workflows were SUCCESS, the independent required Windows VVC runtime was still running. PR #146 remains unmerged until exact-head full gate passes; staged Test should not say `main` contains WU19 before that is proven.

## Final exact-head 10/10 merge and mainline verification

PR [#146](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/146) exact Head `e01a2b5e3474f9fd12a1c695b2dd45618db49584` reached **10/10 applicable CI SUCCESS** including the real [Windows WU02 40221498119](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40221498119), Windows Local Smoke, required Windows VVC runtime and the codec/stream plan/ASS and UIGS regression gates. It was **squash merged** as `main@688d7a3a4a36512a47bdce93d4d1ce6bed65ee49`.

Post-merge GitHub reads of the **actual main branch** confirmed exactly one shared `Copy-NativeStageToOutputTemporary` implementation with a fixed 1 MiB buffer, `FileMode.CreateNew`, and `Flush(true)`; there are **two** production Bridge calls (full job and sample). A runner-only partial-write failure mode survives in main solely for bounded CI. The real Windows 96 MiB stage/5 MiB failed write/correct SHA restaging results and **`DISTINCT_WINDOWS_VOLUMES_VERIFIED`** were explicitly confirmed by WU02's logs at this Head. Same-session shipping Chromium real two-source Native batch verified old output intact, no temp leak, same Job Save-only retry and independent second-source FFprobe/decode/SHA.

**Scoped conclusion:** the delivery pipeline is verified for a 96 MiB real data fixture, 5 MiB partial-file failure and actual distinct Windows volumes. It is **NOT** evidence for 4 GiB+ full movies, interruption of physical disk writes during power failure, physical disconnected/removable media, SMB/cloud/NAS, full-volume actual exhaustion or multiple concurrent users replacing a destination. Those remain separate acceptance tasks. No Canonical changes and no Pending write state.
