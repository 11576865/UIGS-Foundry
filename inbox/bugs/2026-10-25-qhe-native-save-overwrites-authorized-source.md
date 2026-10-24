# Bug: QHE verified Native publish could overwrite an authorized input or queued source

- Date: 2026-10-25
- Project: `11576865/Quick-Automatic-Hardsub-Encoder`
- State: **Implementation proposed; exact-head hosted acceptance pending**
- Scope: Windows Native SaveFileDialog export, including B21 multi-source selection and Native samples
- Related accepted reusable concept: `inbox/candidates/2026-10-04-private-staged-mutation-publish-only-final-verified-output.md` (private staging/verified atomic publish). This is a separate **destination ownership** defect, not a duplicate atomicity proof.
- PR: [QHE #141](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/141), initial head `4b598e12defe196a9b6c309ee7813a190a95e9ee`

## Reproducible source observation

QHE `main@dc203fb5e22754adcdaad4735882d7d3a1e2939c` `windows/native-bridge.ps1` `Export-Job` delegates to a genuine user-selected Windows `SaveFileDialog`, then copies the staged MKV into an on-destination-volume temporary file and uses `Publish-VerifiedOutput`. The latter reliably publishes after SHA and FFmpeg output checks, with `[IO.File]::Replace` for an existing target. **It did not compare the chosen destination path to the currently selected input video, other source grants in B21 batch, selected ASS/fonts, or any staged result.** Thus a valid finished MKV could *successfully overwrite* an unprocessed original video, irreversibly losing user data. Atomic replace is not sufficient for destination safety. The `Export-Sample` path used direct `Copy-Item -Force` without any source/destination collision exclusion.

This is a source-code-derived risk; do not claim an actual user's file was destroyed.

## Proposed fix and bounded oracle

QHE PR #141 adds an explicit private `Get-BridgeProtectedPublishPaths` inventory retaining current source and **all other queued native source grants**, ASS/fonts, Bink staging, completed Job outputs and samples; `Assert-NativePublishDestinationSafe` verifies an absolute output path is not any protected path under Windows case-insensitive canonical comparison, blocks destination directory and file-level reparse points. Both job and sample export use the guard **before copy and directly before publish**. Samples additionally copy into same-volume temporary output and compare origin/staged SHA before existing atomic publisher. The ordinary user's Windows SaveFileDialog and explicit user overwrite of unrelated files are preserved.

An isolated `GITHUB_ACTIONS`/preauthorized `RUNNER_TEMP` CI-only fault adapter can target (1) selected current source and (2) a different **already authorized batch source** by registered ID; no client-selected paths are ever accepted. The real production Chromium V3 → Native Bridge scenario is required to prove two attempted source-colliding exports are rejected, both input SHA digests unchanged, exact first Job remains completed for save-only retry, then two actual source outputs save normally and pass independent FFprobe/FFmpeg/hashes. CI fixture-generated sources are synthetic; actual human SaveFileDialog mistakes, junction/hard-link path aliases, network/cloud targets and OS ACL/disk-full remain out of scope.

## Intake / dedup decision

- Distinct domain-level Bug: **atomic verified delivery may be semantically destructive when the destination is also an authorized input**.
- Reuses the existing private-staging Candidate and QHE Case; do not auto-promote Canonical based on this single implementation.
- Do not mark fixed or pass until PR #141 exact-head Windows WU02 and all applicable CI succeed, and merge is verified.
