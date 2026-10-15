# Case: HSR #159 giant divergent draft retired with verified scope accounting

Date: 2026-10-15
Status: Case / implementation-submitted, CI-pending, remaining feature migration pending
Project: 11576865/HSR-Voice-Archive-Builder
Domains: engineering-process, git, archive-provenance, ass-render-evidence
Deduplicates with: inbox/candidates/2026-10-04-active-work-branch-budget-and-cleanup.md; inbox/observations/2026-10-04-collapse-stacked-pr-chain-by-retargeting-top.md

## Trigger and source evidence

- HSR draft [PR #159](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/159) accumulated 181 unique historical commits and 59 changed files; current-main comparison reported 280 commits missing from the historical head.
- Unlike already-replaced feature heads, its source tree still contains separate, non-current-main modules for archive audit and WAV source-byte verification, exported-ASS bounded raster evidence with resumable window coverage, remote update publication safeguards, and human subtitle recovery.
- Main already owns newer incompatible Studio, true font/FFmpeg preview, subtitle receipts and complete MKV lifecycle. Reapplying stale files wholesale would override product-owned state.
- A stale PR being **unsafe to merge** does not mean its nonmerged capabilities are **fully superseded**.

## Bounded action

1. Re-land one isolated, still-useful slice from the original head as [PR #175](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/175), head `c753f352c9e1521987db7a50201f13c295594305`, based on current main `6a507d57c36beb9a4761453e724faf0798ee12f7`. Paths: `app/archive_audit.py`, original tests and both FastAPI/Termux routing surfaces; include task ledger at `.uigs/tasks/hsr-pr159-controlled-integration-20261015.json`.
2. Create [Issue #176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176) with explicit unfinished feature clusters, test requirements and provenance.
3. Annotate and close original PR #159 **unmerged**. Preserve source branch `feat/hsr-archive-audit-karaoke-v1` unchanged as an evidence input. No blanket delete, force-rebase or false completion claim.

## State boundaries

- **Confirmed:** PR #159 is closed unmerged with migration links. PR #175 is submitted and has a coherent new-main commit. Original branch remains available.
- **Pending external validation:** PR #175 exact-head Python and Chromium CI (observed in_progress at initial status read), actual Termux and original WAV corpus tests.
- **Unfinished product functionality:** ASS sampled/covered raster evidence, remote-update safety, human subtitle recovery, older timing/Karaoke jobs and tests still require semantic migration or explicit no-longer-needed proof. Tracked by Issue #176.
- **Not established:** final successful integration of all #159 capability clusters, user-device acceptance, full interval ASS correctness or canonical UI conformance.

## Reusable distinction, not an automatic rule

A gigantic stale draft may be retired as a **Git merge target** only if its distinctive feature debt is transferred to durable successor owners and its source remains retrievable. Closing the PR is a workflow disposition; it is **not** feature completion. For feature preservation, review the original individual modules, their dependencies and current-main equivalents separately.

This is a project Case providing concrete evidence for the pre-existing branch-cleanup Candidate, not an independent new Canonical policy.

No Canonical promotion.
