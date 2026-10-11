# Bug: Incremental voice merge can overwrite same-basename source audio or mix stale downloads

Date: 2026-10-11
Status: Repair proposed on HSR PR #133, latest exact-head CI pending
Project: HSR-Voice-Archive-Builder
Categories: audio identity, archive data loss, cumulative output, platform divergence

## Source-level findings

HSR previously assembled a combined voice source by iterating every WAV from the existing package, then copying every file in persistent `.generated/incremental_audio`. Different source members can have the same WAV basename. The new download directory can retain older WAVs from previous runs. Consequently the naïve copy-through can replace a current root WAV or import an unselected stale WAV into a new batch, despite the API labelling the current apply as new-only.

The Termux Lite implementation additionally copied original members to the flat temporary root by `wav.name`, so distinct chapters' same-basename voices could overwrite each other before the index was updated. FastAPI had previously been fixed to preserve original relative paths, but it still copied every persistent incoming file.

These are evidenced code risks, not a demonstrated lost user archive.

## Proposed repair

HSR PR https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133 adds a shared pre-merge gate `verify_combined_source_no_collisions` that compares case-insensitive basenames against all current package members and rejects unsafe, missing or colliding current-run downloads. Both servers copy **only the current job's successful set**, not all older cached files. Termux Lite now preserves relative source paths through staging and replacement.

Tests in `tests/test_remote_update_guard.py` cover ambiguous members, existing-name collisions, unselected stale cache carryover and missing selected audio. Additional real archive data and Android device acceptance are not claimed.

## Generalizable lesson / intake

A persistent download staging directory is not an execution transaction. The set of committed input files must derive from the actual current successful outputs and pass independent identity preflight, not from a directory sweep. Reusable for any append/merge archive pipeline; keep as Bug candidate pending exact-head evidence, do not alter Canonical automatically.

## Exact-head CI verification (2026-10-11)

HSR PR #133 head `bd272bc957130a0773fcaeedd8290bf548d86e08` passed [tests run 38118776948](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38118776948) — Python 3.11/3.12/3.13 and Termux Lite dependency-surface checks — and [browser evidence run 38118776884](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38118776884) — Chromium UI fixture and FFmpeg/libass artifact checks. These are code/fixture/CI results, not proof of a production archive migration, Android physical-device use, or a merged release. Canonical remains unchanged.
