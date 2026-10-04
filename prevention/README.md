# Prevention Registry

`registry.json` links reusable UIGS knowledge to **executable prevention controls** in source projects.

A knowledge document and an enforcement control are intentionally separate:

`Captured knowledge != Executable prevention`

Each entry records:

- `id`: stable prevention identity;
- `knowledge_refs`: Bug/Candidate/Observation evidence that motivated the rule;
- `enforcement`: concrete source-project controls;
- `recurrence_count`: known recurrences after related knowledge already existed.

Enforcement statuses:

- `submitted` — a concrete control exists on a submitted branch/PR but is not claimed as current-main authority;
- `enforced-main` — the source project's current main contains the control;
- `deprecated` — retained for provenance but no longer an active guard.

Kinds may include regression tests, typed APIs, schemas, linters, parser boundaries, preflight checks, CI assertions, or production-structure constraints.

The registry does not promote the linked knowledge to Canonical. Its purpose is to measure whether reusable knowledge has crossed the gap from prose memory to executable prevention.
