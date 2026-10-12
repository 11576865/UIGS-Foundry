# Bug: HSR Karaoke \k / \kf compilation drops word onset offsets and silent gaps

Date: 2026-10-11
Status: Static source-level defect identified; corrective code and runtime regression pending
Lifecycle: validation-pending
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


## Implementation update — HSR PR #133 (2026-10-11)

The proposed repair is now committed on HSR branch `feat/hsr-archive-audit-karaoke-v1`, PR https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133, exact submitted HEAD `cd695d76eac48b13827aa7ddb7c51d0982c4c6cf`.

`subtitle_layout/ass_writer.py` emits ASS `\\kt` word onset anchors when word start differs from the preceding word end; it retains `\\k` / `\\kf` per-word active durations. Multiple rendered lines can retain karaoke where each source word maps wholly to a displayed line; splitting a word falls back to plain text. Tests cover onset gaps and multi-line mapping.

An independent local FFmpeg/libass synthetic probe confirmed `\\kt` timing behavior, but PR #133 exact-head GitHub Actions is **Pending CI** at submission, and no physical device/full real archive acceptance is claimed. The implementation is **proposed repair**, not yet merged/main nor an audited production release. Canonical unchanged.


## Further boundary: audio-aware ASS pre-roll shifts every source word's event-relative time (2026-10-11)

Static audit of HSR PR #133 showed a second offset issue beyond word gaps: with audio-aware kinetic entrance, the ASS event's Start can precede the source WAV Start. Per-source word alignments remain WAV-relative. If the writer emits \k, \kf or clip times without applying the actual render event pre-roll, highlights trigger early. The project writer now shifts each word's render-only start/end by the computed pre-roll and does not mutate cached alignments. Added synthetic regression for two adjacent cues with a 200 ms entrance pre-roll, all three Karaoke modes, and unchanged input word timing.

This is **related to the same relative/absolute timing family** as the existing bug, not a new Canonical rule. Source-level repair is submitted in HSR PR #133; exact-head CI was still in progress at intake and must be followed separately.



## CI evidence for original-language Karaoke role/pre-roll correction (2026-10-11)

HSR PR #133 exact HEAD `83248e831b2440f1b8581d1f82f5dcebfc4a6547` passed [tests run 38119628856](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38119628856): Python 3.11/3.12/3.13 and Termux Lite dependency-surface; and [subtitle evidence run 38119628853](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38119628853): Chromium UI and FFmpeg/libass fixture tests. CI does not establish real official Japanese/Korean forced-alignment accuracy or physical-device acceptance. This PR remains unmerged and dependent on #132. No Canonical promotion.
