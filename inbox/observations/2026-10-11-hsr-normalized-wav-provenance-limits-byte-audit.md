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
