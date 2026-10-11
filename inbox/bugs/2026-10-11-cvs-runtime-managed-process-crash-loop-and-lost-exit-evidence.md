# Bug: CVS managed runtime crash loop loses process exit evidence and has no automatic restart backoff

Status: **Bug / code repair submitted, CI Pending**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Source fix PR: https://github.com/11576865/Character-Voice-Service/pull/23
Dependency baseline: main after merged PR #21 and #22

## Audited code-path defect

Before this repair, `server/runtime_supervisor.py::_clean_exited`
removed an owned Python/engine process as soon as `poll()` returned its
exit code, closing its log handle and deleting the only process record.
`status()` subsequently returned a generic `stopped` state when the
health URL was unavailable; the exit code and crash timing disappeared
from administrative diagnostics.

For an engine with `start_on_demand=true`, the next
`ensure_ready()` invocation launched the engine immediately again.
A runtime failing every model load could therefore cause repeated
expensive process starts on request traffic, with no per-engine restart
cooldown. Process-spawn OS errors could surface as unclassified exceptions.

These are **source-derived failure paths**, not a reported real-user
GPU crash or measured system outage.

## Submitted repair

[CVS PR #23](https://github.com/11576865/Character-Voice-Service/pull/23) adds:

- A last-unexpected-exit observation (`pid`, `returncode`, uptime,
  timestamp and log path), retained for admin diagnostics even after the
  process handle has been cleaned up.
- A per-engine, in-memory **bounded automatic restart backoff** for
  unexpected exits, startup health deadline and spawn failures. Starts
  at 5 seconds, doubles on consecutive failure and caps at 60 seconds.
  A 300-second stable uptime or failure-free history gap resets the
  sequence. A cooldown is reported as `restart-backoff`, with count,
  remaining delay and last reason. Automatic attempts fail promptly,
  rather than sleeping inside a long request or launching a replacement
  on every new request.
- An explicit administrator `restart()` clears the cooldown before
  one new attempt while preserving exit diagnostics. Intentional stop,
  GPU-group stop and service shutdown do not create an unexpected-exit
  record.
- Classified `RuntimeSupervisorError` for process-spawn `OSError`;
  log file cleanup continues on all launch exceptions.
- Seven targeted Python tests (including actual disposable child
  processes that exit with distinct codes), plus inclusion in the
  Windows targeted CI and a bounded-retry operator runbook.

## Verification / limits

New test implementation and source changes are submitted to PR #23.
Linux and Windows CI remain **Pending** at intake. Real GPU, actual
IndexTTS/GPT-SoVITS, user-machine processes and external system
supervisor recovery have not been exercised in this turn.

The protection and last-exit record are **not durable across CVS server
restart**. It is neither a new scheduler nor evidence that GPU-driver
or kernel stalls recover when the supervisor process exits. The admin
must inspect real engine logs and process ownership before overriding
backoff.

## Reuse / de-duplication

Foundry searches for `crash loop restart cooldown`,
`supervisor restart backoff`, `unexpected exit process`,
`process exit code diagnostic` and bounded startup retry found related
CVS IndexTTS hang and native helper observability records, but no
prior record for **managed process crash-loop suppression with retained
exit provenance**. It is therefore recorded as a project-specific Bug,
not a duplicate of the inference-slot watchdog defect.

Reusable candidate insight: cleanup of a finished native process
must not erase failure evidence, and a per-request on-demand startup
policy needs a bounded failure circuit breaker. Do not promote to
Canonical based on this one project/source observation.


## Follow-up: Windows CI exposed expired-cooldown test assumption (2026-10-11)

PR #23 initial GitHub Actions run `38116430882`: Linux `test`
**success**; Windows `windows-script-audit` **failure** with 88 passed
and 1 failed test.

The one failing test expected each request immediately after an intentional
child crash to see `restart backoff active`. Windows' slower health probes
allowed the real **5-second** cooldown to expire before that assertion.
The next attempt was then correctly permitted to launch, failed with the
same code 17, and caused a mismatched-regex assertion. This is **not**
evidence that the runtime exited with the wrong code, nor proof that the
real crash-loop limiter had been bypassed.

Source-level secondary performance gap: during cooldown,
`ensure_ready()` probed the failing health URL with its normal timeout
(1.5s) *before* dispatching to `start()`, which probed again. This
both amplified request latency and consumed the short intended cooldown.

The fix now short-circuits cooldown requests into the managed `start()`
admission path, whose health probe has a **0.2s bounded timeout** during
active backoff; it still lets an actually healthy endpoint take
precedence. Tests use a **test-only widened cooldown** in the slow-system
concurrent refusal scenario; the independent policy test retains
production 5/10/20/40/60-second timing. Two more regression tests verify
short probe and healthy-endpoint preservation.

Latest PR head after the fix:
`5c0d31f8ae78748b663f066ed11aa07adec090f9`.
It is main-based, GitHub says mergeable, and its main-relative
files are limited to five expected paths. **Fresh Windows CI is Pending**;
no successful rerun result or production GPU acceptance is claimed.

Dedup: this is further evidence for the existing **CVS runtime crash-loop
Bug**, not a new Candidate or Canonical standard.


## Verification update: PR #23 merged after early-watchdog repair (2026-10-11)

The final [CVS PR #23](https://github.com/11576865/Character-Voice-Service/pull/23) head `210a1605b66b4553f4336b4c7fdb92eff07167f6` passed GitHub Actions run `38117245421`: Linux `test` **success**, Windows `windows-script-audit` **success**. It merged to `main` as `a8fb0fea30739d2238fbd7ffbf51c631f31699a1`.

The final patch also repaired the previously recurring Windows IndexTTS
watchdog case. A `threading.Timer` callback was permitted to run a little
*before* the deadline according to `time.monotonic()` and would simply
return without scheduling another callback. That could permanently disarm
the sole watchdog. The repair waits out the residual duration, rechecks
active request identity and then exits only if that original inference
is still active. A deterministic **early-trigger timer** subprocess
regression was added.

Evidence status: Linux and Windows CI of the final commit **passed**;
actual GPU hang recovery and independent external System Supervisor remain
FIELD-PENDING. Previously Pending notes above are historical and should
not be confused with this later, observed merge result. No Canonical change.
