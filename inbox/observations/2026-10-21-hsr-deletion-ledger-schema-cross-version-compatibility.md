# Observation — Persistent sidecar schema must remain readable by still-running older peers

Date: 2026-10-21
Source: `11576865/HSR-Voice-Archive-Builder` PR [#199](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/199) / correction PR [#200](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/200)
Level: **Observation + test evidence; no Canonical change**

## Concrete code-contract mismatch

- HSR PR #198's still-running reader required `jobs.json.deleted.json` to have `schema_version == 1`, a list-valued `job_ids`, and ignored additional fields.
- PR #199 introduced a `schema_version: 2` sidecar to carry original producer `owner_sessions`, which new code could read but old #198 code would reject as an unreadable deletion ledger. Even though the new release's parser was backward compatible, the **stored shared resource was not forward-readable by an old live peer**.
- This was caught by source-level post-merge review, not by an observed user incident. It demonstrates why checking only that the new reader understands old files is insufficient when different program versions can run concurrently.

## Product correction

- [PR #200](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/200) writes the old `schema_version: 1` and unchanged `job_ids` contract, with an optional additional `owner_sessions` mapping. The previous reader ignores the mapping, while the new reader applies it for compaction.
- The new reader also accepts PR #199's short-lived v2 files. The startup maintenance sweep atomically converts v2 to v1 **even if the original owner is alive**, without deleting the associated job ID or owner mapping.
- Compatibility tests assert that newly written metadata still satisfies the old v1 parser contract and that v2-to-v1 migration retains deleted IDs and producer provenance.
- PR #200 exact tested head `9b118afc5325537252535595de5d33d73c23e4b6` passed [Python / Termux tests #39466229547](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229547), [native Windows process tests #39466229267](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229267), and [seven ASS #39466229292](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229292). Merged `main@90a5d6ef77e3323e9d3a6f49d21c6cf0dcc5683c`. Merged-main independent workflow results were pending when first recorded.

## Reusable engineering consideration

For a persistent artifact shared by independently running processes, migration direction has two dimensions: **new reader <- old file** and **old reader <- new file**. Before changing a top-level format version, determine whether concurrently running old processes can still access that artifact. If old readers already tolerate additive optional fields, additive changes to the existing contract can be safer than a major schema bump; preserve unknown-owner fail-closed behavior rather than manufacturing ownership evidence.

## Boundaries

Source plus CI tests prove parser-contract compatibility and on-start migration. They do not exercise a real deployed #198 binary running side by side with #200 across process restart, power loss, or partial rollout. These field cases stay Pending, and no single observation modifies Canonical.

## Exact merged-main CI closure

At HSR `main@90a5d6ef77e3323e9d3a6f49d21c6cf0dcc5683c`, all four independent workflows succeeded:
- [Python 3.11/3.12/3.13, Termux Lite surface, real libass `tests` #39466462336](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462336)
- [Native Windows writer/journal compatibility #39466462356](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462356)
- [Seven ASS requirements #39466462284](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462284)
- [Pages build/deploy #39466461767](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466461767)

The prior Pending merged-main CI item is now closed; physical simultaneous old/new HSR and power-loss tests remain FIELD-PENDING. No Canonical promotion.
