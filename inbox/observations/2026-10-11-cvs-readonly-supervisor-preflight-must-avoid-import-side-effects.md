# Observation: read-only deployment preflight must avoid importing service initialization code

Status: **Observation / code+tests submitted / Windows CI Pending**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Source PR: https://github.com/11576865/Character-Voice-Service/pull/30
Related Bug: [CVS external activation replay/stale status](../bugs/2026-10-11-cvs-external-activation-replay-and-stale-supervisor-status.md)

## Concrete source observation

CVS runtime Registry parsing currently imports `server.config`,
whose `ADMIN_TOKEN = _admin_token()` initialization can create the
machine's `data/admin-token.txt` if no explicit admin token exists.
A command advertised as **read-only external System Supervisor preflight**
would violate that contract if it imported the normal service
configuration chain on an uninitialized machine.

The external activation state also contains distinct evidence types:
a persisted pending receipt means a request may have been published,
a top-level `<request_id>.json` file means the command artifact exists,
an external asynchronous `status_file` reports a Supervisor
observation, and loopback HTTP health reports current endpoint
responsiveness. None by itself proves the external System Supervisor
**accepted and executed that exact request ID**. In particular, a
missing command file might mean it was consumed OR never published.

## Submitted implementation and tests

[CVS PR #30](https://github.com/11576865/Character-Voice-Service/pull/30)
adds `scripts/external_supervisor_preflight.py` using Python
**standard library only** and no imports from server code.
It compares CVS Registry external control fields against an explicitly
provided actual Supervisor config, observes status files, validates
pending receipt IDs and any matching top-level command, and returns
structured JSON with `pass/warning/error` and exit codes `0/1/2`.
Default behavior is offline, with **no writes, no process launch and
no activation publication**.

Optional health probe requires an explicit flag and allows only a
loopback HTTP URL; environment HTTP proxies and redirects are disabled
to prevent accidental requests beyond the intended host. The output
does not include admin tokens, model prompts or full command/status
payloads. It explicitly declares
`correlated_acknowledgment="not-established"`.

Regressions check the CLI doesn't create an `admin-token.txt` or
mutate its fixture directory, mismatched service/engine paths,
corrupt/unresolved receipts, lack of request correlation and
loopback/redirect refusal. Linux full GitHub CI passed at first
intake for PR #30 head
`8d2b9ca977b078900f5a20b652fa5a2ce21978ad`;
Windows targeted CI was still Pending.

## Reuse boundary and status

This is a project-specific engineering observation with a plausible
cross-project lesson: **a validation tool cannot be called read-only
merely because its own function bodies omit writes; imported module
initializers and optional network dependencies are part of its
side-effect boundary**. Another lesson is to distinguish artifact
existence, asynchronous state and correlatable consumer
acknowledgement.

The deployed System Supervisor consumer is not in the CVS repository,
so real consumer interoperability, GPU behavior and request-level
external acknowledgments are FIELD-PENDING. The new CLI narrows
uncertainty but does not prove deployment success.

Deduplicated against existing CVS external activation Bug and the
shared-resource synchronization Candidate; store as **Observation**,
not a new Canonical rule or premature general requirement.


## CI acceptance and main integration — PR #30 (2026-10-11)

Final PR #30 head `8d2b9ca977b078900f5a20b652fa5a2ce21978ad`
passed GitHub Actions run `38133437202` with both Linux `test`
and Windows `windows-script-audit` concluding **success**. Main-relative
diff comprised 5 intended files with `behind_by=0`, GitHub reported
`mergeable=true`, and the PR merged into CVS `main` as
`2d842f8e64ef199532cea61685da0179ffa6ccfd`.

This supersedes the earlier Windows Pending snapshot. Tests verified
the no-write/no-import-side-effect CLI contract, cross-platform path
checks, receipt/command mismatches, local HTTP probe and redirect
refusal; they did **not** exercise an installed System Supervisor
consumer or GPU hardware. Thus the field acceptance gap stays
FIELD-PENDING. Retain as Observation; do not promote to Canonical.
