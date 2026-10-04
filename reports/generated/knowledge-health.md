# UIGS Knowledge Health

Generated: 2026-10-04T18:52:27+00:00

## Intake and knowledge inventory

| Metric | Count |
| --- | ---: |
| Bug records | 22 |
| Candidates | 140 |
| Observations | 20 |
| Cases | 8 |
| Durable Pending packets | 234 |
| Pending packets without review decision | 233 |
| Pending packets with triage record | 234 |
| Pending packets not yet triaged | 0 |
| Triage records total | 234 |
| Promotion proposals (total / open) | 4 / 3 |
| Typed intake records | 2 |
| Catalog entries | 71 |

## Bug evidence lifecycle

Bug records are historical/reusable evidence. Their count is **not** the count of unresolved product defects.

- recorded: 8
- regression-verified: 3
- repair-evidenced: 9
- validation-pending: 2

## Prevention coverage

- Registered prevention rules: 5
- Enforced on source main: 4
- Submitted but not yet main-enforced: 1
- No executable guard registered: 0
- Rules with recorded recurrence: 2
- Total recorded recurrences: 2

Prevention coverage tracks executable controls separately from prose knowledge. A Bug or Candidate document alone is not counted as enforcement.

## Catalog maturity

- candidate: 4
- experimental: 51
- validated: 16

## Interpretation boundary

- A high Bug/Candidate count can reflect stronger observation and capture rather than lower product quality.
- The Pending directory is durable intake storage: a packet may already be triaged while remaining under Pending.
- Untriaged Pending and open review proposals are stronger backlog signals than the raw Pending count.
- Review/proposal backlog measures governance debt, not source-product defect count.
- `submitted` prevention controls are not counted as enforced until the source main contains the control.
- Recurrence is tracked separately because repeated failure after prior knowledge is evidence of prevention/enforcement debt.
