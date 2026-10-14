# Case: Mainline-converged QHE still advertises Draft PR authority in durable task state

Date: 2026-10-15
Status: **OBSERVED / correction in Draft PR #108, not merged at this record's creation**
Project: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder
Observed main: `c66b0658fe2e62259322b4b2e0b6fbd1e797fde1`
Source recovery file: `.uigs/tasks/qhe-initial-version-full-report.json`
Root requirement tracing: `docs/initial-version-report-traceability-2026-10-13.md`
Correction: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/108
Authoritative new acceptance review: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/107

## Verified mismatch
At exact integrated main, PR #102/#103/#104/#105 were all merged, no PR was open and all 4 main push CI workflows passed (Frontend, Windows smoke, Android build/deploy, UIGS Coverage). Yet the durable task JSON still had `branch=feat/qhe-five-round-delivery-20261013`, `pr=105`, and a blocker claiming #104/#105 Draft and unmerged. The traceability document's intro also presented the former branch baseline without a dated supersession banner.

This is more than an out-of-date prose paragraph: the repository's AGENTS.md explicitly instructs resumed workers to read the durable task file before taking further steps. A resumed worker treating this outdated status as current could waste budget attempting to remerge or rebuild already integrated features. Meanwhile legitimate product acceptance gaps remain: original R19/R24 B01–B25 and A01–A10 are still open in part; green mainline CI is not V1 certification.

## Bounded correction, not implementation rewrite
Draft PR #108 updates only the root JSON and the traceability preface. It snapshots current main, 4/4 push CI, merged PR graph, the explicit WU11 design-only scope and actual Web vendor missing-core blocker. It archives previous task fields and keeps all 25 requirements, prior work units, and historical SHA-specific test claims unchanged. No product code or Canonical policy is changed. PR head `7aac123f6718cff741c39473a4765114211e0e61`; exact-head CI was in progress at observation time.

## Reusable nuance
Completion of code integration, PR closure, CI, and durable recovery-authority refresh are **distinct transactions**. Reconciliation on every resumed engineering turn should compare external truth (main SHA, PR state and exact-head CI) against task fields and annotate stale records before starting new work. A historical design checkpoint must remain as such, not be silently rewritten as if its recorded CI ran on new main.

## Deduplication
Foundry already includes `2026-10-04-interrupted-session-reconcile-before-reimplementation` Candidate and `2026-10-04-ass-mkv-stacked-pr-consolidation` Case, both covering resumption and duplicate implementation. This case adds a **post-merge durable task-authority drift** instance with exact conflicting fields and a distinct bounded correction mechanism. Single case only; no Canonical promotion.
