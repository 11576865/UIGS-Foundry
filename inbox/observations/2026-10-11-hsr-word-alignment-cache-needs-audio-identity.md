# Observation: Word-alignment cache validity does not bind to source audio bytes

Date: 2026-10-11
Status: Source-level observation; real data reproduction and repair pending
Product: HSR-Voice-Archive-Builder main 5dde8e3d8a1bc32f3553be7f4f17ae6873930d75
Categories: derived data, provenance, invalidation, speech alignment

## Observation

`app/word_alignment.py` stores a normalized source-text SHA-256 and a source-audio duration in `word_alignments.json`. `_record_matches_entry` invalidates a record when text changes or when the source duration changes beyond tolerance. It does not compare the original source WAV content hash.

A same-text, similar-duration audio replacement could therefore reuse old forced-alignment timestamps even if the actual speaking rate, silences, or phrase timing changed. The broader archive already models source membership and source-audio identity, but this particular cache predicate does not bind timing to the original bytes.

This is a stale-cache risk inferred from code, not a demonstrated production failure.

## Suggested repair / evidence

- Incorporate available source-audio SHA-256 (and source-member identity) into the derived word-alignment cache identity, or use an equivalent proven audio revision identity.
- If audio identity cannot be established, report unverified/stale rather than infer valid alignment from equal text and near-equal duration.
- Introduce a fixture with two different WAVs of equal duration and same official transcript; stale word timing must not carry across the replacement.
- Keep `word_alignments.json` an independent derived sidecar; do not mutate canonical official dialogue/translations.
- Extend the existing Word Sync diagnostic instead of adding a second Karaoke UI.

## Evidence / boundary

- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/app/word_alignment.py
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/app/local_word_alignment.py
- Search across existing Foundry for HSR alignment/audio fingerprints did not find a directly matching record.
- No new code, runtime reproduction or CI is claimed.

## Intake disposition

Observation, not yet a confirmed runtime Bug or a Canonical UIGS requirement.


## Implementation update — HSR PR #133 (2026-10-11)

The proposed improvement is now committed on HSR PR https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133 (submitted head `cd695d76eac48b13827aa7ddb7c51d0982c4c6cf`).

`app/word_alignment.py` stores `source_audio_sha256` with new imported word-alignment records, and requires it to match the current manifest SHA-256 when the manifest carries a valid hash. Records without this new evidence become stale rather than silently reusing timings after unchanged text/duration. A new regression changes the audio identity without changing the text/duration. The initial migration intentionally treats legacy entries lacking this hash as stale under new manifests; fallback for legacy manifests without WAV hash retains limited text/duration validation.

The separate HSR archive audit (same PR) reports provenance coverage by group but is explicitly structural only: it does not recompute WAV hashes. Status: **submitted, Pending CI**, not mainline-merged or physically verified. Canonical unchanged.


## Follow-up: import identity consensus and asynchronous source revision (2026-10-11)

Further HSR inspection uncovered an adjacent distinct failure mode: the word-alignment import resolver previously returned the first matching identity from `source_member_id`, `logical_id`, entry ID/index or basename. When a record contained two contradictory identities, one could silently be ignored, and duplicate manifest keys were resolved by dictionary last-wins. A long-running local WhisperX job also imported results into whichever Manifest existed at completion, rather than necessarily the revision it aligned.

HSR PR [#133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133) now requires all supplied identity keys to resolve to one unambiguous row, enforces any supplied text/audio hash and duration evidence, and binds local generated batches to the SHA-256 of the initial Manifest. Source/canonical transcripts remain read-only. English/Japanese/Korean tests use synthetic WhisperX responses to verify exact script preservation and cache ownership, not actual model accuracy.

Code+tests checkpoint `8503148d54907200b6223318075b5634e938b233` passed [Python 3.11/3.12/3.13 and Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38128432169), plus [Chromium/libass evidence](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38128432178). Documentation update followed. Remaining evidence limit: import uses pre-save Manifest hash revalidation, not an atomic multi-process transaction with the build pipeline. The user has not supplied true JA/KO game audio acceptance evidence. Record stays Observation, no Canonical promotion.


## All-rejected imports preserve existing evidence bytes (2026-10-11)

An additional source-level finding in the same HSR Word Sync domain: the importer rewrote its sidecar `updated_at` even when it accepted zero new records and rejected the entire incoming batch. That made a failed attempt appear as a newer evidence revision. HSR PR #133 now writes a cache only when at least one record is accepted; a regression imports a valid record, then rejects a fingerprint-conflicting record, and verifies that the existing sidecar bytes remain exactly unchanged and usable. Test checkpoint `2c4292dea39ea3639e584af49ee728c52c814914`; asynchronous exact-head CI outcome must be checked independently. Observation remains project-specific; no Canonical promotion.
