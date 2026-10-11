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
