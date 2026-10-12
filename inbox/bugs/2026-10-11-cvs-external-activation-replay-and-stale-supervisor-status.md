# Bug: CVS external runtime file activation could replay commands and mislabel health

Status: **Source-audited Bug; repair PR submitted, CI and live integration Pending**
Lifecycle: validation-pending
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Source: https://github.com/11576865/Character-Voice-Service/pull/26
Base: CVS `main` after merged runtime orphan-owner PR #25

## Source-derived failure modes (not confirmed incidents)

The external-only engine activation bridge in
`server/runtime_supervisor.py::_request_external_activation` previously
created a fresh UUID and `<uuid>.json` activation command whenever
`ensure_ready()` found an unhealthy engine and `start_on_demand=true`.
Its polling loop waited for HTTP health, then timed out without
retaining the request's pending identity. Independent CVS server
processes could issue multiple commands simultaneously for the **same**
external `service_key` and retry additional commands after timeout,
even while the external owner might still be starting.

A second source-level issue was that an older external Supervisor
`status_file` `state` could overwrite live HTTP `ready` or `busy`,
or mask a failed HTTP health probe with a stale `ready` state.
An empty configured external `request_dir` was also accepted through
a truthy `Path(".")` conversion.

## Submitted bounded repair

[CVS PR #26](https://github.com/11576865/Character-Voice-Service/pull/26):

- Uses a **nonblocking OS file lease** keyed to the canonical request
  directory and exact `service_key`. A second cooperating CVS process
  gets a classified conflict rather than publishing another command.
- Atomically stages and fsyncs a durable pending request identity before
  publishing the existing `activate-engine` command. Internal records
  are kept in `request_dir/.cvs-activation-state/`, not at the command
  inbox's top-level `*.json`, to avoid accidental consumption.
- Leaves pending evidence on timeout or partial publication; a later
  caller must not blindly replay. A genuinely healthy endpoint can
  reconcile the **matching** request ID without issuing another command,
  including after CVS restart. Mismatched engine identities or
  corrupted/unreadable records fail closed.
- Exposes `external_activation` and unresolved/pending states in admin
  diagnostics. Live HTTP health controls actual readiness while external
  `status_file` remains supplementary evidence.
- Rejects empty external request directory configuration.
- Adds 15 tests, including a disposable second Python interpreter
  competing for the activation lease, delayed recovery, replay refusal,
  internal inbox separation, live/stale status conflict, and malformed
  state. Linux full pytest and Windows targeted tests are configured.

## Evidence boundary

CI is **Pending at intake**; the source PR may be updated after actual
Linux/Windows workflow evidence. No real external System Supervisor
consumer, speech model or GPU process was activated or measured.

The repair controls commands published by **cooperating CVS processes**,
not external launcher ownership. A successful HTTP health response
does not cryptographically or transactionally prove that a particular
`request_id` caused the engine to start. End-to-end correlated
acknowledgment, lifecycle authority and actual GPU ownership remain
open integration tasks.

No automatic pending timeout/TTL cleanup or forced external process
termination was introduced. An ambiguous request may require manual
inspection before clearing the receipt.

## Dedup / knowledge placement

Foundry searches for `external activation duplicate command`,
`system supervisor activation request idempotency`,
`external runtime status stale health`,
`external activation receipt` and `file request inbox duplicate`
did not reveal an existing project-specific record with this precise
failure mechanism. Related shared-resource locking Candidate covers
the general multi-process coordination boundary. This record belongs
under **Bug** and may extend the existing Candidate without changing
Canonical from a single project observation.


## Verification update — PR #26 merged

Final PR #26 head `7e31f88a31e7d0ffbf6264ee939b648603ed536b`
passed GitHub Actions run `38120009311`: Linux `test` and Windows
`windows-script-audit` both **success**. It was merged into CVS
`main` at `568f2cc6643dbae9b35e9632488d4575b5423227`.

The previously Pending CI assertion above is now superseded by this
observed result. Source CI covered simulated external health, file
activation and two Python interpreters contending for the same lock.
Live System Supervisor consumer interoperability, correlated
request acknowledgments and real GPU process management remain
FIELD-PENDING. No Canonical change.


## Producer-consumer contract acceptance follow-up — CVS PR #29 (2026-10-11)

Previous CVS PR #26 verified file command publication, concurrency locks and
health-state handling using mostly stubbed/mocked health responses, but
**no independent OS process actually consumed the command file**.
This means a mock health success alone did not prove that a separate
consumer could use the existing bridge fields to activate an HTTP endpoint.

[CVS PR #29](https://github.com/11576865/Character-Voice-Service/pull/29)
adds a dedicated **test-only external consumer process** that reads the
existing top-level `<request_id>.json` file, validates
`schema_version`, `action`, `engine_id`, `service_key` and file
identity, and starts a local HTTP health server. Three multiprocess tests
now cover: (1) producer -> file -> independent consumer -> live health ->
receipt reconciliation, (2) activation timeout and later recovery
without a second command, and (3) abrupt death of a different CVS
controller after the command is published, while a replacement CVS
must refuse replay until the original consumer goes healthy.

The repository does **not** include the actual deployed System
Supervisor implementation. The consumer is a fixture and its mock
`last_request_id` field is **not a protocol-level acknowledgement
consumed by CVS**; a health endpoint alone cannot attribute startup
to a particular request ID. Documentation explicitly keeps actual
System Supervisor integration, TTS weights and GPU behavior FIELD-PENDING.

PR #29 head `05b04b0e7e0b2d55a7a87f183f674d2ea5d6d615`:
GitHub Actions `38132656247` Linux `test` **success** and Windows
`windows-script-audit` **still in progress** at first intake.
Source PR not yet merged at this observation.

De-dup: adds direct producer-consumer acceptance evidence to this
existing external activation Bug, not a new unrelated issue or
Canonical rule.


## PR #29 independently executing consumer test: verified and merged

Final [CVS PR #29](https://github.com/11576865/Character-Voice-Service/pull/29)
head `05b04b0e7e0b2d55a7a87f183f674d2ea5d6d615` passed both
Linux `test` and Windows `windows-script-audit` in GitHub
Actions run `38132656247` and merged to CVS `main` at
`62e438dcc1d7588d4f08c03aaa2f001c52f37027`.

The independent *test-only* consumer read the real top-level activation
file, started a loopback health endpoint and wrote an observational
status file. The suite passed delayed consumer health, refused replay
after timeout and real producer-process kill with recovery by a
replacement CVS. This proves the simulated producer/consumer file
protocol under CI; it does **not** prove deployed System Supervisor
consumer interoperability or request-correlated acknowledgement.

The earlier Pending CI snapshot is now historical; live System
Supervisor and GPU acceptance remain FIELD-PENDING. No Canonical change.
