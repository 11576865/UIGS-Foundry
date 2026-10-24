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

## 2026-10-25 first exact-head real Windows evidence

[QHE PR #141](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/141) commit `4b598e12defe196a9b6c309ee7813a190a95e9ee`, Windows WU02 [CI run 40135682895](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40135682895) **SUCCESS**:

- Shipping V3 + actual Windows Native Bridge, private source picker, real FFmpeg and original save flow tested **two prohibited output targets**: first the currently selected video, then the other already-authorized but not-yet-executed batch video. Both were rejected by the Native publishing guard before any replacement. The two input file SHA-256 hashes remained unchanged after the two attempts.
- The same source's already completed encode was saved successfully without re-encoding, then the second source was encoded/saved. Two actual jobs, four export attempts, two final independently FFprobed/FFmpeg-decoded and SHA-checked MKVs:
  - job `9ab71b0e8493448eabd13212a2980eb7`, 551,130 bytes, SHA-256 `440f37642c45c60881313320c5e8eca3c9833ae5662b74048aec31bf7466735f`;
  - job `63d73dced0804f3f8b7f79862886334a`, 364,793 bytes, SHA-256 `be8f957ecfe0e3316e0599d15741ddfbbf7dc1b5d4d30bb13c166345aad99f49`.
- Earlier WU13 complete Native save, B21 divergent-source Stream Copy + H.264/AAC and WU14 cancel/publish denial/retry paths also passed in the same Windows test. Windows Local Smoke, including Windows PowerShell entrypoint parser, passed.
- **Evidence status:** WU15 two-source protection is `HOSTED_BOUNDED_VERIFIED`; whole exact-head PR merge remains **PENDING** until the last VVC runtime check (9/10 workflows SUCCESS when verified). Genuine user SaveFileDialog, NTFS hard-link/path-junction aliases, external drives, Windows ACL and disk-full need field or new independent tests.
- Dedup: this is the already created WU15 Bug; no additional Candidate and no Canonical change.
