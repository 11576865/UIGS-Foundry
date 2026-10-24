# Bug: Incremental voice merge can overwrite same-basename source audio or mix stale downloads

Date: 2026-10-11
Status: Repair proposed on HSR PR #133, latest exact-head CI pending
Lifecycle: recurring
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


## Follow-up repair: verify current download session bytes, not just selected names (2026-10-12)

Further review of the existing HSR provider downloader found a distinct stale-data path: it searches its destination for `<stem>.*` and may return a cached `status=exists` result without re-fetching or hashing the selected audio. The old fixed directory `.generated/incremental_audio` could therefore allow a same-name leftover file to masquerade as the just-resolved provider voice; prior successful-record filtering and full index/member matching do not alone prove current download provenance. This is a source-code finding and regression scenario, not a reported corruption of a user's real HSR package.

HSR PR [#133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133) now gives every FastAPI and Termux Lite Apply a fresh UUID-scoped download session. The shared `verified_completed_new_wavs` gate verifies exact chosen basenames, `status=ok` (rejects cache `exists`), current-session path, disk SHA-256 vs provider completion digest, absence of symlinks, and RIFF/WAVE chunk structure (format and nonempty data, chunk bounds). Invalid or unexpected records fail **before** config/index publication; the immutable versioned WAV and index publication remains separately guarded. Success can clear its now-redundant staging files; failed sessions are not reused. Tests use a real tiny PCM WAV, simulate full mocked provider-to-config Apply preserving same-basename chapter members, and reject unsolicited/cached result, hash/path mismatch, invalid and truncated containers.

**Exact code/docs HEAD** `741ea4daa56a0944f8926de364a58223cb8af704` passed [Python 3.11/3.12/3.13 + Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38164326333) (4/4 jobs) and [Chromium UI + libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38164326345) (2/2 jobs). This is fixture evidence, not real Hugging Face content verification, decoded speech-quality acceptance, real HSR archive migration, cross-process crash safety or physical Android operation. Keep as Bug evidence, no Canonical change.

## Recurrence — 2026-10-24: Termux flattened members again after earlier merged fix

**Lifecycle: recurring.** Historical HSR [PR #133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133) **was merged** as `8796f417a0106f7b266cbefa8179319ec941fabb`, with regression tests and explicit relative-path preservation. Later HSR `main@a0ee60a58a05793701377c4a26095c5e4f10fa3d` was directly inspected: `app/lite_server.py` again used `target = temporary_root / wav.name`, copied source WAVs into a flat directory, published that directory, and omitted `source_member_id` when creating incremental index rows. `app/server.py` retained relative paths, but both adapters were separate implementations. This recreates the earlier merge collision for two different chapter members sharing a basename, even if all audio is Japanese. It is source-confirmed regression; no user original archive has been inspected.

HSR proposed [PR #211](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/211) adds one `prepare_incremental_audio_stage` implementation shared by desktop and Termux. It requires verified completed download SHA-256/file paths, preserves each old WAV's relative source member ID, refuses symlink members and new basenames already present anywhere in the original package, and publishes a new immutable generation before switching the project index. Termux index writing is brought into parity with the desktop version and persists `source_member_id` on additions. Regression tests include a directory and ZIP each with two `chapter*/same.wav` members, old-byte retention, unsafe symlink, new-old basename collision, and invalid digest. This closes the previously missing test seam at a shared helper rather than relying on separate route text-only checks.

**Exact-head evidence status:** PR #211 head `857ebb2fccdc539250b29b0367531c4ae3b5a2bc` CI was in progress at time of intake; do not claim tests passed until actual workflow results confirm. The old artifact/user-device repair and real-Japanese listening remain FIELD-PENDING. This is recurrence of the existing Bug, so this entry is updated, not duplicated. No Canonical change.

### Related non-English LAB side effect

Source inspection of `app/builder.py::build_entries` shows `source_text_language != en` reads sibling member-relative LAB files to resolve the source language's actual text and falls back to the original index only if LAB is absent. Original incremental merger in both runtimes copied WAV only, so cumulative Japanese source generations silently discarded original chapter-specific `.lab` provenance; this can change transcript binding on rebuild even when WAV identity is preserved. HSR PR #211 therefore stages **both WAV and LAB** with their original relative member paths. Directory and ZIP fixtures now carry distinct `chapter1/same.lab` and `chapter2/same.lab` Japanese source texts. Updated exact head `572ed202f6d718096e6f6e90484db0c28491d7f6` CI is pending. No user archive data altered.

## Exact-head merge confirmation — 2026-10-24

HSR PR #211 proposed head `572ed202f6d718096e6f6e90484db0c28491d7f6` passed all six workflow gates: Python 3.11/3.12/3.13 + Termux Lite + real-libass tests, Chromium browser/libass evidence, Seven ASS, Windows writer/journal, long-running concurrent journal stress, and pinned legacy interop/recovery. Squash merge to `main` succeeded as `8d86c83d2b047c74d4f26b67d5f7090bb163ab8a`. The merged implementation stages chapter-relative original WAV and LAB members in a single shared helper and blocks incoming basename collisions with source members.

**Authority / remaining boundary:** Lifecycle remains `recurring` to preserve the important fact that a previously merged fix (PR #133) regressed in later code. CI verifies synthetic directory/ZIP same-basename and distinct Japanese LAB members, not a byte-by-byte reproduction on the user's actual project. An existing already-contaminated/flattened source is not automatically restored; field inspection, rebuild and listening still pending. No Canonical promotion.
