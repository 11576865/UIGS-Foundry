# Observation: Transformed WAV hashes cannot be assumed to equal original package bytes

Date: 2026-10-11
Status: Source-level observation; fail-closed handling proposed on unmerged HSR PR #133
Product: HSR-Voice-Archive-Builder
Categories: provenance, source integrity, normalization, evidence scope

## Observation

HSR `app/builder.py` normalizes WAV files in-place within a temporary build work directory when archive PCM formats differ. The entry's `sha256` is computed **after** such conversion. The original ZIP/7z/directory may still contain pre-normalization bytes; therefore an original WAV hash differing from `manifest.json` does not by itself prove corruption.

The builder records a temporary `.pcm_normalized.json` mapping of pre-/post-normalization SHA-256 pairs under its WAV work root, and the build report records an aggregate `count_wav_pcm_normalized`. The temporary mapping is not established as durable per-member original-hash provenance in this review.

## Proposed scoped repair

HSR PR https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133 adds a user-invoked source WAV byte verifier. It performs actual streaming hashes against manifest members and reports ordinary mismatch when no PCM normalization is recorded. If normalization is recorded, a differing source SHA is reported as `normalization_ambiguous`, not asserted to be corrupted or verified. `trusted_complete` remains false. The report clearly separates cheap manifest field coverage from actual WAV byte checking.

This distinction is conservative: an aggregate normalization count cannot identify which original WAV differs, and some such mismatches could still reflect actual corruption. Future work should persist per-member pre-normalization hashes or a verified transform relation, rather than treating aggregate normalization as individual provenance.

## Evidence

- HSR `app/builder.py`: `_normalized_wav_record_path`, `build_entries`, `raw[\"sha256\"]` and entry SHA construction.
- HSR `app/pipeline.py`: work directory extracted source and work-root lifetime.
- HSR PR #133: `app/archive_audit.py`, `tests/test_archive_audit.py`.
- The current exact-head PR CI has not been evaluated after this observation; this is not a claim of release validation or source-project main merge.

## Intake

Observation only. Do not promote to Canonical from one project's source-level evidence.

## 2026-11-10 continuation — resumed metadata versus original extracted PCM

**New user field observation:** Termux build failed at `archive_mar7th_20.wav` with actual `(48000, 1, 16, 277363)` versus cached Entry/manifest `(44100, 1, 16, 254828)`. This is a screenshot-observed failed gate; original PCM content and manifest provenance were not supplied.

**Code-derived explanation:** `build_entries()` transforms minority-format WAVs in the extraction working tree and records post-normalization Entry fields, while `pipeline.build_project_v02()` can reuse that metadata stage and re-extract untransformed members to create FLAC. For 48 kHz / 277363 samples, real local FFmpeg resampling produces exactly 44.1 kHz / 254828 samples; frame durations are within a rounding quantum. This is consistent with the user's report but does not alone prove that their actual source content is unchanged. The pre-/post-normalization relation in the October observation is the relevant provenance boundary.

**Narrow mitigation submitted:** [HSR PR #222](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/222), latest branch commit `c989770abcb9061df3f8ed493b43115365c5bf2a`. When a resumed member differs from the saved Entry PCM tuple, it normalizes **only an isolated temporary streaming copy** to the recorded format and checks both exact PCM tuple and the manifest's **post-normalization SHA-256** before streaming. Already-matching members are also checked against their saved content hash. Discrepancies fail closed without replacing the previously published FLAC. New real-FFmpeg regression reproduces the exact 277363-to-254828 conversion and an equally long altered-audio rejection.

**Status:** Product change submitted on PR, exact-head CI and target Android field success **Pending External Validation**. This fixes the resumed-stream boundary, not the broader original-directory in-place normalization policy or durable per-member pre-transform provenance. Do not promote Canonical from this observation.

**Merge/CI update — 2026-11-10:** HSR PR #222 merged by squash into `main@50a09ac952900c88dde41be3c6823841f83e4838`; all five reported PR-head GitHub Actions workflows completed successfully (tests, seven ASS, Windows, legacy interop, sustained concurrent job journal). Post-merge readback of `app/builder.py` confirms private normalization and SHA-256 identity gate. A later merge #221 leaves both repairs included in `main@9a9c1e74d63f869ec1991f892be6f1482b907ad9`. Physical Termux build on the user's archive remains **Pending Field Validation**, and successful resampling does not prove source-byte identity absent the actual hash check. No Canonical promotion.
