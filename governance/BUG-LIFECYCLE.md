# Bug record lifecycle

Status: **Experimental governance**
Date: 2026-10-04

Bug records in `inbox/bugs/` are durable evidence. Their presence does **not** mean the underlying product defect is still open.

Each Bug record should carry a machine-readable `Lifecycle:` line immediately after `Status:`.

Allowed lifecycle values:

- `recorded` — the defect and reusable lesson are captured, but the record does not contain concrete repair evidence.
- `repair-evidenced` — the record names a concrete mitigation, repair PR/commit, or implemented correction. This does not imply that the repair is merged or fully validated.
- `validation-pending` — a concrete repair is submitted and the record explicitly says validation/CI/device evidence is still pending.
- `regression-verified` — the record contains repeatable regression evidence for the repaired behavior.
- `recurring` — the same failure family has reappeared after prior knowledge existed and should be counted as prevention/enforcement debt.
- `superseded` — this record remains historical evidence but a newer record is the authoritative description of the failure family.

These values describe the **evidence state of the Bug record**, not an issue-tracker state. They must not be used to claim that a source repository is bug-free, deployed, or validated beyond the evidence cited in the record.

## Prevention distinction

Knowledge capture and prevention are separate dimensions:

`Observed -> Captured -> Validated -> Enforced -> Recurrence monitored`

A Candidate or Bug document is not an enforcement mechanism. Prevention may be implemented through typed APIs, schemas, linters, invariant checks, regression tests, preflight gates, CI assertions, or other executable controls.

`prevention/registry.json` records these controls separately from the knowledge documents they implement.

Do not promote this governance model to Canonical solely because it has been introduced operationally.
