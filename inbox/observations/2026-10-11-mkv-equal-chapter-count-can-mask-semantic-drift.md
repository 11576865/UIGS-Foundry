# Observation: equal chapter count can mask remux semantic drift

Status: **Observation / implementation-backed, CI pending**
Date: 2026-10-11
Source project: `11576865/MKV-Fast-Muxer`
Source branch: `fix/chapter-semantic-mux-audit`
Source commit: `065a1d75d70116bdd8a96f3abdcc52d344250058`

## Direct code observation

At source main `d5669c6d9bb6ebdd6843ee8c7f651902c80c4d08`,
`auditMuxProbe()` checked only the chapter count. Two chapter inventories
with equal counts but different start/end times or titles could therefore
pass the chapter part of the output audit. The tool already had a general
`TEST.CONTAINER_SEMANTIC_AUDIT` registry entry; that entry names chapter
preservation but does not by itself prove that time and title were compared
by the implementation.

## Product-local repair

The branch above adds:
- expectations derived from source ffprobe chapters;
- same-order start/end comparisons with a documented 2 ms allowance for
  muxer time-base quantization;
- source-provided title/language preservation checks with case-insensitive
  metadata-key lookup;
- negative regressions for equal-count drift, missing timestamps, extra
  chapters and edited titles/languages; positive regressions for 1 ms drift
  and renumbered muxer chapter IDs.

## Reusable distinction

**Inventory cardinality** (count preserved) is weaker than **persisted
chapter semantics** (boundaries and metadata preserved). A successful
container output probe should not promote the weaker check into an
unqualified semantic pass. Timestamp comparison needs a format-specific
rounding policy, and volatile muxer-assigned chapter IDs should not be
mistaken for stable identities.

## Evidence boundary and deduplication

This entry supplements rather than replaces
`TEST.CONTAINER_SEMANTIC_AUDIT` and
`CLAIM.TEST.CONTAINER_SEMANTIC_AUDIT`. It does not declare a new Canonical
rule or claim independent cross-project validation. Source-change static
inspection is available; Node and browser CI are **Pending** at intake.
The example is an observed code-coverage defect with a corrective PR,
not a claim that an actual user file suffered chapter loss.
