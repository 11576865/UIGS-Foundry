# Reports

Foundry reports combine structured project facts with clearly separated derived analysis.

Pipeline:

project manifests + knowledge records + CI/runtime evidence
-> normalization
-> report generator
-> generated facts
-> optional narrative analysis

Run `python tools/generate_reports.py` for the current local inventory report.

Generated reports must not imply freshness beyond their source revisions.

## Live cross-project state

`reports/generated/project-state.json` and `project-state.md` are generated from live GitHub branch/workflow state plus local Pending/Triage/knowledge counts. Workflow results explicitly record whether the latest run matches current HEAD.


## Knowledge health

`reports/generated/knowledge-health.json` and `knowledge-health.md` separate durable Bug/Candidate inventory from intake backlog and executable prevention coverage.

The report intentionally does **not** treat the number of Bug records as an unresolved-product-bug count. Bug evidence lifecycle comes from `Lifecycle:` metadata, while executable enforcement is registered independently in `prevention/registry.json`.


## Review queue

`reports/generated/review-queue.json` and `review-queue.md` turn raw intake volume into reviewable work.

The queue groups unresolved `needs-review` CI packets by repository, workflow, red-reason category, matched rule set, and related knowledge. This is operational grouping only: it reduces repeated review effort without claiming that every packet in a group has the same root cause.

Open promotion proposals remain explicit per-packet review items and still require accept/reject decisions.
