# Prevention Registry

`registry.json` links reusable UIGS knowledge to executable prevention controls and generation-specific prevention-effectiveness Claims.

`Captured knowledge != Executable prevention != Proven prevention effectiveness`

## Registry v2

Each entry records `effectiveness_claim_ref`, `enforcement_generation`, generation-tagged controls, attributed `recurrence_events[]`, `legacy_unattributed_recurrence_count`, and total `recurrence_count`.

A recurrence challenges the effectiveness Claim for the generation active when it occurred. Strengthening prevention creates a new generation and a new Claim; old recurrence evidence is preserved against the old Claim.

Future recurrences should be recorded through `tools/record_prevention_recurrence.py`, which atomically appends the recurrence event, creates contradicting Evidence, and attaches it to the current generation Claim.

A historical numeric recurrence count without event provenance is not counter-evidence. It remains `legacy_unattributed_recurrence_count` and generates a provenance-gap Validation Mission.

Enforcement statuses remain `submitted`, `enforced-main`, and `deprecated`.
