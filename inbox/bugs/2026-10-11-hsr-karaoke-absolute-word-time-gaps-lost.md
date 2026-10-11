# Bug: HSR Karaoke \k / \kf compilation drops word onset offsets and silent gaps

Date: 2026-10-11
Status: Static source-level defect identified; corrective code and runtime regression pending
Product: HSR-Voice-Archive-Builder main 5dde8e3d8a1bc32f3553be7f4f17ae6873930d75
Categories: subtitle timing, forced alignment, ASS Karaoke, provenance

## Observation

In `subtitle_layout/ass_writer.py`, `_validated_word_alignment_details` correctly retains each aligned word's `start`, `end`, and `duration`. But `_validated_word_alignments` drops `start/end` and reduces each item to `(word, duration)`. `format_karaoke_text` then emits consecutive `{\\kN}` / `{\\kfN}` tags computed only from word durations.

This is not generally equivalent to forced alignment: an initial silent interval and gaps between spoken words are missing. For example, alignment `A: 0.40–0.80 s, B: 1.00–1.30 s` generates 40 cs + 30 cs with an implied first onset at event time zero, not at 0.40 s; the 0.20 s inter-word silence also disappears. The existing `test_format_karaoke_explicit_word_alignments` exercises contiguous alignments starting at zero, so it does not cover this discrepancy.

The `clip` implementation instead reads the absolute `start/end` timestamps, exposing an internal divergence between the three existing Karaoke modes.

## Suggested repair and acceptance

- Compile ASS Karaoke timing from relative absolute onsets, not merely summed vocal durations; preserve initial offset and all inter-word silent gaps without introducing visible extra text.
- Cover `\\k` and `\\kf` with fixture cases for initial silence, pauses, punctuation/spacing and an output that is longer than the final word.
- Validate the actual output in FFmpeg/libass at representative timestamps, not only tag presence or totals.
- Keep Chinese translated target text unaligned to the foreign source track unless independent verified cross-language mapping exists.
- Reuse the existing Word Sync / Karaoke controls; no new workbench section or UI surface is implied.

## Evidence / boundary

- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/subtitle_layout/ass_writer.py
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/tests/test_ass_advanced_typography.py
- Evidence level: static code inspection and logically constructed counterexample. No executable reproduction, patch or user-device result is claimed in this record.
- Existing Foundry search for Karaoke timing gaps and cumulative durations yielded no directly equivalent HSR record.

## Intake disposition

Bug candidate for HSR-specific repair. Do not promote a one-off finding into UIGS Canonical. 
