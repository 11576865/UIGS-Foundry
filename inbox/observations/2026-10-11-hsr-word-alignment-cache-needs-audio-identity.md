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
