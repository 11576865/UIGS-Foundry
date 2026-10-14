# Case: QHE Draft success does not prove full runtime acceptance

Date: 2026-10-15
Status: Case / verified workflow-state boundary; final post-review CI pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder
Integration PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Exact integrated HEAD: `2bafff40e70801f841ae983e385213a2fca26198`

## Observation

Following integration of merged PR #102's mobile clip-queue fix, QHE PR #105 was rebased semantically via a two-parent merge, retargeted to `main`, and remained Draft. GitHub reported it as mergeable. On this exact HEAD, **14 workflow runs succeeded but 7 runs completed as `skipped`**, including Windows local smoke, Windows paired-codec tests, Stream Plan v4 Windows/Android acceptance, Android compilation, device-fixture generation and VVC runtime checks.

The workflow files use `if: github.event_name != 'pull_request' || github.event.pull_request.draft == false` on heavyweight jobs. `Test frontend` uses a `draft-fast` branch and a separate non-Draft full suite. Thus a green Draft-fast run plus independent slice tests does **not** mean exact-head Chromium and cross-platform end-to-end acceptance have completed.

On 2026-10-15 the owner authorized further integration checks. PR #105 was marked Ready for review without changing HEAD, which triggered **20 new full/runtime acceptance runs**, initially queued or running. Their final outcomes and actual mainline merge were still pending at the observation boundary.

## Reusable acceptance distinction

Record the exact SHA, PR review state, **job-level conclusion**, and whether the gate ran in full or fast mode. `success`, `skipped` and `pending` are not interchangeable. Before merging a cumulative PR, verify the required full jobs for that exact HEAD; do not infer coverage from branch mergeability, overall green appearance, previously green ancestor HEADs, or a partial suite. Avoid repeated CI polling: transition once, record pending state, and inspect the asynchronous result when actionable.

## Scope and deduplication

Foundry was searched for draft PR, skipped workflows, exact-head full runtime gates, and adjacent branch-reintegration practices. Related records include Candidate `2026-10-04-reintegrate-stale-branches-as-semantic-deltas`, Case `2026-10-04-ass-mkv-stacked-pr-consolidation`, and Case `2026-10-13-qhe-report-baseline-cannot-be-replaced-by-scoped-ci-delivery`. They address semantic re-integration and product-scope denominators, not this specific Draft-fast versus full runtime CI gate distinction.

This is one project-specific observation. It does not prove a CI defect or universal workflow policy and does **not** justify Canonical promotion.
