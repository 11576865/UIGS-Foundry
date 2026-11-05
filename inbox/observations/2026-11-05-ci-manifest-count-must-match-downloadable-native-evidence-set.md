# Observation: a CI success count does not prove the independently downloadable artifact set is complete

Date: 2026-11-05
Status: **Observation / scoped artifact completeness verified; full PR CI and merge pending**
Scope: external-reviewable evidence for real user-task and native output acceptance
Product: `11576865/MKV-Fast-Muxer`, [PR #250](https://github.com/11576865/MKV-Fast-Muxer/pull/250)

## Evidence and reproducible failure of the previous proof boundary

A prior successful Softmux S10 [Browser E2E #42016372295](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42016372295) generated and independently checked **20 real Chromium/FFmpeg.wasm MKVs** for normal batch plus **20 real MKVs** for fault-recovery batch. Its JSON manifests each reported 20 individually verified files with job IDs, hashes and audit status. However, the uploaded normal artifact `s10-twenty-real-matroska-batch-evidence` (ID `13409202822`) physically contained only **3 of 20 MKVs** and **no per-output reports**; the recovery artifact `s10-combined-fault-recovery-native-evidence` (ID `13409986080`) physically contained only **3 of 20 MKVs** (although 20 reports). This is an **evidence completeness defect**, not evidence that the product failed to generate 20 files.

An external reviewer cannot independently verify 20 output checksums merely because the same manifest *asserts* they were checked within the CI run. A passed producer-side hash assertion is useful but logically distinct from consumer-side availability of every referenced byte sequence.

## Narrow corrective work

[Draft product PR #250](https://github.com/11576865/MKV-Fast-Muxer/pull/250), exact head `89ffa2333074fd2812b8e3b6a2cac7d6e293efb2`, changes only CI upload globs and a **pre-archive standard-library Python verifier**; it does not modify product code or repeat the media generation algorithm. The verifier requires exactly 20 distinct MKVs and corresponding 20 reports in each output directory, validates raw file SHA-256 and size against both the manifest and actual report, checks job and output identity, and refuses unexpected/missing files. The archive step changes `if-no-files-found` to `error`.

The new current-head [Browser run #42025031130](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/42025031130) has independently passed both **20-member prearchive set verifiers and uploads** (main full-browser job still running at intake). New GitHub artifact IDs `13412609360` (normal) and `13413576581` (fault recovery) were downloaded as ZIPs, with **20 actual MKV files + 20 reports each**. A separate local standard-library SHA-256 review plus native `ffprobe` opened **all 40 real files**, confirmed each entry's output hash, expected bytes, report `audit.ok`, unique job ID and filename. Both sets passed: `20/20`, with total MKV bytes `18,913,740` per set. A local second-pass JSON report exists for this exact inspection, but the product CI overall is **not yet** declared SUCCESS at intake.

## Reusable hypothesis and limits

For claims of **N independently auditable produced artifacts**, the evidence contract should enforce a bijection among (1) planned actual output identity, (2) producer manifest entry and report, and (3) **downloadable complete output bytes**. Exact-source or writer-only success does not grant equivalence to a missing archive entry. An archival sample is legitimate only when explicitly labelled *sampled* and cannot support a claim that all N outputs have been independently rehashed outside CI.

Limit: sources are two short real media templates repeated with distinct source File identities/subtitle pairings; in-memory injected directory faults are not physical disk write proofs; nothing implies Android tablet or 1.0 formal acceptance. Preserve all owner-release approval and Canonical boundaries.

## Deduplication

Searched Foundry for `CI zipped selected samples falsely sufficient acceptance manifest`, `all twenty output report pairs archive SHA independent`, `missing artifact list evidence completeness`, `partial artifact upload no original outputs CI evidential limit` and `artifact upload sample manifest cannot rehash`. Related `inbox/candidates/2026-10-13-multi-artifact-partial-publication-state.md` concerns production publication and save-state partial failure, **not completeness of the external CI archive**; existing stream/native comparison observations cover bitstream equivalence, not evidence-set bijection. Treat this as a scoped Observation, **not Canonical**. Final exact-head full E2E result and product merge remain Pending.
