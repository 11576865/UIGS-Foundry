# Bug: Corrected bilingual CSV fallback can migrate human edits to a different WAV member

Date: 2026-10-11
Status: Source-level repair proposed on HSR PR #133, code/test CI passed
Product: HSR-Voice-Archive-Builder
Categories: archive provenance, subtitle edits, member identity, lossless migration

## Defect

HSR `app/subtitles.py::_sync_corrected_csv` previously created maps from
source member, basename and index using dictionary last-wins. When a CSV row
specified a source member no longer in the rebuilt Manifest, it nevertheless
fell back to the filename or entry index, which could now identify an
entirely different voice line. A chapter-level duplicate WAV basename made
the problem especially likely.

A nearby `_override_for_entry` logical-ID fallback could similarly apply
a historical human Chinese translation to a new source member when their
logical IDs were equal, despite different source-member identities.

These are code-review findings with synthetic regression reproduction, not
claims that any customer's original project was corrupted.

## Implementation and acceptance

HSR PR [#133](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133)
now resolves corrected CSV rows only by an unambiguous source member.
Member IDs that are specified but no longer found **never** fall back to a
different basename or index. Memberless legacy rows can use a globally unique
filename; only when the current Manifest itself has no filename may a unique
index recover the record. Duplicate indices, member IDs or basenames refuse
last-wins selection. Old human overrides may still follow their exact original
WAV member after reindexing, but not a different member sharing a logical ID.

`tests/test_duplicate_members.py` covers chapter same-name WAVs, deleted
source members, memberless old CSV, duplicate member identity, and valid
legacy index-based migration. Existing `test_subtitle_editor.py` also caught
the legitimate legacy no-filename case, which was corrected without relaxing
the duplicated-member guard.

Exact code/test checkpoint `eb411b592650743c1e8a01b7dd9b0fed9ad43f9a`
passed [Python + Termux](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38132602948)
and [Chromium + libass](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38132602955).
Later PR commits also extend human translation provenance; check their
exact-head status separately.

## Reusable lesson

In reindexable archives, a filename or display index is not an acceptable
backup for a **contradicted explicit source identity**. Conservative migration
permits fallback only when the stronger identifier was never present and
its uniqueness is established; do not substitute a different voice file.

UIGS Intake: Bug. No promotion to Canonical.


## Audit re-open: direct same-ID legacy override bypasses basename ambiguity (2026-10-11)

Review of HSR PR #133 exact head `a0d4b95712bf2fa320584224c49099afd0c2c80f` shows an adjacent unresolved entry path in `app/subtitles.py::_override_for_entry` (lines 133–144). When an old override has the same numeric item ID and filename but no `source_member_id`, the direct-ID clause accepts it even if the current manifest has multiple same-basename WAVs. The later fallback correctly uses `ambiguous_filenames`, but the direct clause runs first and does not check it. Therefore the previous fix is partial. Code-path evidence, not a runtime user-data corruption report. Recommended regression: two members `female/dup.wav` and `male/dup.wav`, legacy ID=1/filename=dup.wav with missing member identity, ensure no override is applied merely because an ID is reused. Do not update Canonical; triage before PR merge.


## Repair checkpoint — direct identity fallback re-audited (2026-10-11)

The same PR now disallows the direct same-ID bypass when a legacy record's filename or logical ID is ambiguous, and refuses completely identity-less old row-ID overrides on modern source-member-aware entries. Existing member identity must match when provided. Reset/replace also carries full manifest duplicate awareness; a reused numeric key is journaled as historical evidence before assignment to a different source. Tests cover same-basename chapter siblings and legitimate stable-member rebuild migration. Exact SHA `731b65a65a3c57595a05cb2a45ab34634a6dfeb4` passed [Python CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714940) and [browser evidence](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38135714983).

Legacy overrides without identity cannot be proven against an old source revision; they are a separate migration risk, not proof that all historical data is validated. No Canonical promotion.
