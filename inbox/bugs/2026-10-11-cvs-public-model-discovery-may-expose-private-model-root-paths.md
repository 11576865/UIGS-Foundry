# Bug: public CVS model discovery can disclose private Model Root paths in error strings

Status: **Source-derived path exposure / no deployed incident reproduced**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Audited main: `184d481c8cae911643a3a059211bbd71cbece20e`
Severity: P1/P2 depending on deployment network reach

## Source path

`server/app.py` exposes `GET /v1/models` without the
`require_admin` dependency. That endpoint returns `list_models()`
from `server/model_registry.py`.

For registry entries marked `present`, `list_models()` calls
`resolve_model()` and catches
`(OSError, ValueError, json.JSONDecodeError)`, adding
`item["error"] = str(exc)` directly to the public model object.

`resolve_model()` constructs an absolute
`model_root/manifest_rel` path and calls
`validate_manifest(manifest_path)`; that function uses
`manifest_path.read_text(...)`. If a previously registered manifest
is missing, a `FileNotFoundError` includes its absolute local path
inside `str(exc)`, which is then returned to the unauthenticated
client. The public contract in
`docs/character-voice-contract-v1.md` states:
“Public discovery must not expose local model paths, local reference
paths, or reference transcripts.”

Therefore this is a source-derived **public error sanitization gap**,
not proof an actual host secret was disclosed.

## Proposed hardening and regression

- Keep detailed errors in administrator-only diagnostics/logging,
  using a stable error code and sanitized description on public
  discovery.
- Inject a missing manifest in a temporary Model Registry and assert
  that unauthenticated `GET /v1/models` never emits the temporary
  model root path. Include invalid checksums and corrupt manifest
  cases, not just the happy path.
- Apply the same public-info review to `GET /health`, which
  currently includes engine adapter exception strings in the
  public `engines[].error` object.
- Preserve the public discovery contract rather than placing every
  discovery route behind the admin token.

## Dedup / evidence

Foundry search for `public model registry error path disclosure`
and `public model discovery leaks file paths` found no matching
CVS Bug. Store as concrete **Bug**; source path confirmed, external
network exploit or data exposure not field-tested.
No Canonical change. Status **OPEN / tests and remediation Pending**.


## Proposed repair and expanded public diagnostics audit — PR #35 (2026-10-12)

[CVS PR #35](https://github.com/11576865/Character-Voice-Service/pull/35)
head `c896744d9fe5e50b40a1d594069f2df5c362f36e` adds a
bounded public-diagnostics response contract:

- `list_models()` no longer copies raw FileNotFoundError/manifest
  errors into anonymous discovery JSON. It reports a fixed
  `model metadata unavailable` message with a stable
  `model-metadata-unavailable` error code.
- The public Registry 500 response omits the raw path-bearing
  exception detail.
- The public `/health` output uses an allowlist for engine ID,
  normalized short status, boolean busy, finite active time and
  short precision instead of forwarding arbitrary third-party
  Sidecar health keys, host/model paths, internal request IDs or
  raw exception texts.
- Public profile/selection error strings no longer echo internal
  validation or lookup exceptions.

New tests create a real temporary Model Root, register a manifest,
then delete/corrupt/mutate it to confirm that unauthenticated
discovery never leaks its absolute path; they also inject malformed
health payloads and host path errors. Linux full and Windows
targeted CI were **in progress** in run `38160208039` at intake.

This extends the previously filed concrete Bug rather than creating
a duplicate; actual external exploitation is not claimed.
No Canonical change or real GPU/Supervisor acceptance is implied.


## PR #35 verified and integrated (2026-10-12)

Final [CVS PR #35](https://github.com/11576865/Character-Voice-Service/pull/35)
head `c896744d9fe5e50b40a1d594069f2df5c362f36e` passed
GitHub Actions `38160208039` with Linux `test` **success**
and Windows `windows-script-audit` **success**, including
PowerShell parse and discovery/doctor smoke tests. The branch
had `behind_by=0`, six intended files and `mergeable=true`.
The PR merged into CVS `main` at
`06244f71f5d962ace3922b94f9e8f12456858cf5`.

The source-level public filesystem-path disclosure for
`GET /v1/models`, top-level Registry errors, and reflected
voice validation/selection exceptions is repaired. Health output
now uses an allowlist that excludes arbitrary backend diagnostics
and internal request IDs while retaining basic public status.
Actual temporary Model Root deletion/corruption/mutation regressions
and path injection tests passed CI.

The prior Windows Pending snapshot is superseded. This is a
verified, merged source/test remediation for these public
diagnostic paths, **not a full API security audit or evidence of
a real information leak on a deployed host**. Other public routes,
network policies, real GPU/speaker identity and external Supervisor
field verification remain separate work. No Canonical promotion.
