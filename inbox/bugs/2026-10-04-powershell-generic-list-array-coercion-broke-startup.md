# Bug: PowerShell generic List array coercion broke optional-adapter discovery at startup

Date: 2026-10-04
Status: Bug
Scope: PowerShell / helper discovery / startup reliability

## Symptom

Windows Native Bridge never became healthy after an optional Bink adapter was added. CI only observed repeated health-check failure until Bridge stdout/stderr were exposed.

The process had exited during startup with:

`Argument types do not match`

at a converter-discovery return expression using:

`return @($candidates)[0]`

where `$candidates` was a generic `System.Collections.Generic.List[object]`.

## Fix pattern

Avoid array-subexpression coercion when all that is required is the first element of a generic list:

`if ($candidates.Count -gt 0) { return $candidates[0] }`
`return $null`

Also cast `.Add(...)` to `[void]` so the list insertion index cannot leak into the function's pipeline output and accidentally turn a scalar discovery result into a heterogeneous array.

## Diagnostic implication

Long-lived helper startup smoke tests should surface captured stdout/stderr when readiness fails. "Service never became ready" is only a secondary symptom; preserving process diagnostics reduced this fault to a single source line.

Do not promote to Canonical from this single bug record.
