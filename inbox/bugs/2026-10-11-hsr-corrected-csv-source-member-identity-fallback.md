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
