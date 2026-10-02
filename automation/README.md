# Foundry Automation Topology

GitHub Actions automation must not assume that a commit pushed by a workflow with the repository `GITHUB_TOKEN` will trigger another push-based workflow.

Therefore, dependent transformations are executed in the **same workflow run** when correctness depends on them:

- Collect Outboxes -> Triage -> Red Reason -> Promotion Proposal -> reports.
- Triage Pending -> Promotion Proposal -> reports.
- Review Promotion -> promotion status report.
- Capture Reference Baselines -> rebuild UI search/showcase coverage.

Separate workflows remain useful for direct human/repository pushes, scheduled entry points, and manual repair runs, but they are not used as an implicit bot-commit event bus.

If a future design intentionally requires cross-workflow triggering, it must use an explicit supported trigger/token design and document the privilege boundary.

## Writer concurrency

Foundry has several workflows that may write to `main`. They do not rely on a single pre-push `pull --rebase`. All writers use `tools/push_with_rebase_retry.sh`: fetch current main, rebase, attempt push, and retry boundedly if a disjoint writer wins the race. A true rebase conflict remains an explicit failure.

## Derived-output rule

When a writer produces both source evidence and deterministic derived files, source evidence is persisted first. The workflow then reconciles with current `main`, regenerates derived files from that latest state, and commits them separately. Generated indexes should not be conflict-merged as authored truth.
