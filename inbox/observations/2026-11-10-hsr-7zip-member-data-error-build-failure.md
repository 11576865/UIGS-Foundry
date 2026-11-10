# HSR field observation: 7-Zip member Data Error halts project build

- **Date:** 2026-11-10
- **Level:** Observation / reported user-device failure, not independently reproduced
- **Project:** `11576865/HSR-Voice-Archive-Builder`
- **Scope:** Source archive integrity and task-center failure communication
- **Status:** Open for source-package verification; do not promote to Canonical from one observation

## Direct evidence

A user-provided Android browser screenshot of the local Voice Archive Builder task center shows a failed last project build and the runtime error:

```
7-Zip extraction failed (2): ERROR: Data Error :
chapter3_24_mar7th_131.wav
```

The same cause is repeated in the task report and diagnostic panel. The screenshot does not identify the archive's path, checksum, full 7-Zip output, original download, or disk health. It does not prove which input byte was damaged or that all other members are bad.

## Current implementation anchor

[HSR app/builder.py](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/app/builder.py) `_extract_7z_cli`:
1. performs `7z l -slt` and validates member paths, links, declared size and limits;
2. invokes `7z x -y -o<dest> <archive>`;
3. when return code is nonzero, raises `RuntimeError("7-Zip extraction failed (...): ...")`, matching the screenshot's exact prefix.

This means the displayed failure occurred during extraction after the archive listing stage, not necessarily during audio decoding, subtitle rendering, or FLAC encoding. Listing metadata is not content integrity verification.

7-Zip exit code 2 is a fatal error; `Data Error` commonly occurs when content cannot be faithfully decompressed. Causes still require testing: damaged/truncated source, missing volume, storage/read fault, or encrypted-archive key mismatch where relevant. See official FAQ: https://www.7-zip.org/faq.html and recovery notes https://www.7-zip.org/recover.html.

## Suggested one-time investigation, not observed repair

- Identify the precise configured 7z source path and whether split volumes exist; capture source size, hash, modification time and source binding.
- Run `7z t <archive>` / `7zz t <archive>` directly against that source; retain complete output and exit code. Do not interpret an `l` listing or Quick Scan count as a successful test.
- If test fails, compare against a trusted re-download or authoritative checksum. Preserve existing project state, manifest, validated work products and any progress that can be reused.
- If test passes but build extraction fails, investigate destination/storage conditions and exact CLI invocation, permissions and available space.
- Add a regression fixture with a well-formed 7z directory but a damaged member payload; assert failure before downstream processing, clear source identity + actionable cause, no partial output presented as verified, safe retry after replacing source and preservation of verified checkpoints.

## Reuse hypothesis

**Archive directory enumeration is not a content-integrity gate.** A build that relies on member listing without a content test may discover invalid source data only at extraction; the UI should retain source/progress identity and present a repair route without encouraging indiscriminate cache deletion. This is an observation and test candidate, not a proven widespread bug or a new Canonical requirement.

## Follow-up reported by user (same day)

The user explicitly clarified that the source voice archive **had successfully completed a build before**. This materially narrows interpretation: it rules out assuming the archive was always unusable, but it does not prove the bytes or configured source path remain identical today. Priority differential is now (a) source replaced, truncated, changed or differently selected since last success, (b) transient filesystem or read issue, versus (c) a changed build path requiring re-extraction despite previous validated stages.

An inspected HSR `app/pipeline.py` build route calls `ensure_dir_or_extract(wav_source, work, "wavs")` when its metadata stage cannot be reused, while documented `docs/reliability.md` recovery records stage identity and validated artifact hashes. A repeated extraction may be legitimate due to changed source identity/configuration/stage version. Do not equate a formerly completed build with byte identity now; do not recommend deleting `.state`, `.generated`, manifest, existing FLAC or validated outputs.

**Discriminating field test:** Run `7z t "<exact configured source .7z>"` (or `7zz t`) and retain full result. If test fails, compare source SHA-256/size with prior recorded fingerprint or trusted original and review split volumes. If test succeeds, check whether the path matches what the build used, storage free space, and reason for stage invalidation/re-extraction. Previous success is owner testimony only; no previous source hash or actual current file verification has been provided.
