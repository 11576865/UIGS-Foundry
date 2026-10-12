# Bug: Source-revision handling loses Chinese correction history and accepts a stale editor session

Date: 2026-10-11
Status: Open / confirmed source-code paths, targeted regressions pending
Lifecycle: validation-pending
Project: HSR-Voice-Archive-Builder
PR reviewed: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
Head reviewed: a0d4b95712bf2fa320584224c49099afd0c2c80f

## Findings

1. `app/subtitles.py::_update_project_subtitles_locked` lines 945–970: when `new_chs == raw_target`, the code removes both current-ID and same-member old overrides. When `new_chs != raw_target`, `overrides[key]` is overwritten with the newly reviewed revision. The implementation therefore does **not** guarantee previous human Chinese corrections are retained for review after a reset or new save. Earlier assistant acceptance text overstated this. The test `test_new_human_edit_binds_source_then_rebuild_requires_recheck` checks old bytes only before the re-review, not after.

2. Optimistic save preconditions check `expected_final_chs` and `expected_source_member_id` (lines 890–920) but do **not** bind the editor draft to the original transcript revision. A project may rebuild source text while keeping the same WAV member and Chinese baseline. An editor with a stale draft can then satisfy both preconditions and save a previous-revision translation into the new archive. Client and API revision tokens need to include immutable official source text identity or a versioned entry fingerprint.

3. `_official_source_sha256` lines 75–78 hashes `"".join(source.split())`, so English `"now here"` and `"nowhere"` share the same source fingerprint. The hash algorithm is not cryptographically broken; the input normalization collapses semantically different texts before hashing. Version detection must preserve linguistically meaningful word boundaries while normalizing only safe formatting differences, with multilingual fixtures.


4. Review confirmation has a separate identity-reuse bug: `subtitle_review_state.json` is a simple ID→boolean mapping, and `get_project_subtitles` uses `bool(review_state.get(str_id, False)) and not translation_override_stale`. After an archive reindex, the same ID can refer to a different WAV member/source line with **no stale override to trigger the mask**, so that entirely different entry is shown as reviewed/confirmed. Confirmation must bind to immutable source-member and transcript identity, not the display row index. Add regression for two reordered members with a saved old confirmation but no human text override.

## Remediation tests and outcome requirements

- Simulate original-text revision with same source member and same Chinese base text; submit a stale editor draft and assert rejection without sidecar or export mutations.
- Save a new Chinese correction and later reset to base after source revision; ensure earlier human text and provenance remain recoverable in a dedicated immutable/history record, not just in a transient warning.
- Duplicate file basenames and entry reindexing must never bypass these checks.
- Test `now here` vs `nowhere`, plus harmless line-ending variations separately.

Tests/CI passing on the reviewed PR only demonstrate the current checked fixtures. No report of actual user data loss is claimed. This is a Bug intake; Canonical unchanged.


## Repair checkpoint and remaining limitations (2026-10-11)

HSR PR [#133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133) now stores old human Chinese corrections into the append-first `subtitles_override_history.jsonl` journal before replacing/resetting them or reassigning a numeric key. Both existing subtitle editor save surfaces submit original transcript revision preconditions; the backend validates them with source-member and final-text baseline before writing. Source fingerprints retain whitespace *boundaries* (`now here` ≠ `nowhere`). Review receipts now bind confirmed state to source member plus transcript fingerprint; legacy unbound boolean confirmation cannot automatically attest a reindexed record. Stale fingerprinted human overrides now block newly certified ASS/SRT publication until manual review; no Chinese Karaoke or source transcript editor was added. Human history is included in verified recovery packages, including manual-only projects without an AI translation checkpoint, and a human-only import preserves the full package without automatically reapplying stale edits.

Targeted tests cover source version drift, changed and unchanged Chinese baseline, history after replace/reset, numeric-ID reassignment, review status reuse, English fingerprint collision, and export fail-closed. Exact code/test SHA `731b65a65a3c57595a05cb2a45ab34634a6dfeb4` passed [Python+Termux CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714940) and [Chromium+libass CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714983).

**Residual:** pre-fingerprint legacy Chinese overrides have no historic transcript identity and remain a compatibility path, not a proven source revision. Full crash/multiprocess and real HSR package acceptance are unverified. Manual-only backup import is evidence-preserving, not an automatic human correction restoration to the active project. Bug repair proposed on PR, not Canonical promotion.
