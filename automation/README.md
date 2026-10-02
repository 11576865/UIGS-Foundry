# Foundry Automation Topology

GitHub Actions automation must not assume that a commit pushed by a workflow with the repository `GITHUB_TOKEN` will trigger another push-based workflow.

Therefore, dependent transformations are executed in the **same workflow run** when correctness depends on them:

- Collect Outboxes -> Triage -> Red Reason -> Promotion Proposal -> reports.
- Triage Pending -> Promotion Proposal -> reports.
- Review Promotion -> promotion status report.
- Capture Reference Baselines -> rebuild UI search/showcase coverage.

Separate workflows remain useful for direct human/repository pushes, scheduled entry points, and manual repair runs, but they are not used as an implicit bot-commit event bus.

If a future design intentionally requires cross-workflow triggering, it must use an explicit supported trigger/token design and document the privilege boundary.
