# Bug: CVS IndexTTS inference stall could block following synthesis and lifecycle diagnostics

Status: **Bug / code repair submitted, CI and real GPU acceptance Pending**
Date: 2026-10-11
Source project: `11576865/Character-Voice-Service`
Source fix: https://github.com/11576865/Character-Voice-Service/pull/22
Scope: IndexTTS 2.5 Sidecar and CVS Runtime Supervisor

## Source-level failure paths

This is a code-audited risk, **not a confirmed user incident or measured
GPU deadlock**.

1. `sidecars/index_tts_api.py` runs synthesis under a blocking process-wide
   `with _INFER_LOCK:`. Its advertised concurrency is one and cancellation
   unsupported. A native/GPU inference that never returns can hold that lock
   forever; every later `ThreadingHTTPServer` synthesis handler then also
   waits without an admission limit. The original `GET /health` always
   returned HTTP 200 `status=ready`, so clients had no observable distinction
   between idle and occupied inference.
2. The CVS IndexTTS HTTP adapter formerly translated a sidecar `503` to
   `502`, preventing clients from reliably identifying retryable congestion.
3. Independently, `RuntimeSupervisor.start()` holds an `RLock` while
   waiting for the engine's configured startup deadline (up to minutes).
   `status()` and `diagnostics()` acquired the same lock, allowing
   status requests to appear frozen during an otherwise bounded startup.

## Submitted repair

CVS PR #22:
- adopts a **non-blocking single-slot admission gate**, returning `503`
  with `Retry-After: 2` and `retryable=true` for concurrent inference,
  instead of making another worker wait indefinitely;
- exposes `busy`, an opaque request identity and `active_seconds` through
  sidecar health and CVS Runtime Supervisor, without exposing speech text;
- adds a configurable default **240-second inference watchdog** (allowed
  range 1–280, explicit `0` disables) below the adapter's existing
  300-second network timeout. If native inference still owns the process
  after that deadline, it logs the request identity and calls
  `os._exit(124)` to abort **the dedicated IndexTTS sidecar process**.
  The current HTTP call fails; the configured lifecycle owner may reactivate
  the engine on a later call. No automatic duplicate synthesis retry;
- makes `RuntimeSupervisor.status()` return an immediate
  `supervisor-transition` snapshot when another thread owns the lifecycle
  lock. Start/stop actions remain serialized; status queries no longer
  wait behind the entire engine startup timeout;
- carries targeted Linux and Windows CI regression tests, including real
  localhost HTTP contention against a **fake** TTS engine, watchdog
  termination of a disposable subprocess, successful-completion timer
  cancellation, and locked startup diagnostics.

## Boundaries / epistemic status

- An inference watchdog is **process-level fault containment**, not safe
  per-request GPU cancellation. Killing the process drops its loaded model,
  may cause a delayed reload, and does not prove recovery from a GPU driver
  or operating-system deadlock. A configurable long legitimate inference
  may exceed 240 seconds; operators may tune the deadline.
- HTTP `200` health with `status=busy` means the process is reachable,
  **not** able to accept another inference.
- `Retry-After` is advisory; client retries must be bounded and avoid
  blindly duplicating non-idempotent speech generation.
- Submitted automated tests are **not reported as passing** until the PR's
  actual CI evidence is observed. Real GPU/IndexTTS2 inference and Windows
  lifecycle recovery remain pending.

## Dedup / knowledge boundary

Foundry search on 2026-10-11 for inference watchdog, sidecar stuck, GPU
hang, unbounded queue, busy health and supervisor transition found related
`interactive-preview-backpressure-stale-results`, long-job ownership and
helper observability records but no CVS-specific bounded inference
admission + process watchdog + startup diagnostic-lock defect.

The reusable principle extends the existing shared native-work backpressure
Candidate: single-owner expensive backends require explicit admission
refusal and a recovery policy, not merely a mutex; diagnostics must stay
responsive when lifecycle operations are slow.

This record is classified **Bug**, not Canonical.


## Windows CI failure and follow-up — 2026-10-11

The initial [PR #22](https://github.com/11576865/Character-Voice-Service/pull/22) workflow `CVS tests`, run `38115596012`, completed with:

- Linux `test`: **success**.
- Windows `windows-script-audit`: **failure** — 22 passing targeted tests and one failing `test_inference_watchdog_terminates_stalled_child_process`, raising `subprocess.TimeoutExpired` after four seconds while `subprocess.run(..., capture_output=True)` was awaiting process/pipe completion.

The traceback showed a process object with `returncode=1` while Python was still waiting for a redirected pipe reader thread to finish. This is evidence of a Windows-specific **test/process-output wait defect or abnormal exit**, but **does not itself prove** the underlying cause is an inherited pipe handle or that the engine watchdog succeeded. Avoid converting this test failure into a runtime cancellation claim.

The repair commit on #22 changes both subprocess-based watchdog tests to redirect stdout/stderr into an ordinary temporary file, asserting the exact process return code and reading the recorded log *after* `wait` has returned. This distinguishes actual watchdog failure from waiting indefinitely for a captured PIPE EOF and yields diagnostics if the exit code is wrong.

Because CVS [PR #21](https://github.com/11576865/Character-Voice-Service/pull/21) merged the separate Model Registry infrastructure into `main`, #22 also received a reviewed two-parent reconciliation commit `21439209b3704fee8410bef07eb9d61137a17641`, preserving both the model-registry Windows test suite and new IndexTTS targeted Windows test suite. The PR's main-relative delta is now only 10 expected files, `behind_by=0`, mergeable according to GitHub at inspection.

**Verification of this follow-up commit remains Pending CI** and real IndexTTS/GPU recovery remains FIELD-PENDING. No canonical promotion; this is added evidence within the existing Bug, not an independent generalization.


## Watchdog root-cause evidence and merged follow-up — 2026-10-11

After the earlier pipe-capture change, PR #23 still failed Windows
`test_inference_watchdog_terminates_stalled_child_process` (run
`38116628298`, Linux success, Windows one failure). The newer traceback
waited directly on the child **process handle** with a regular temporary
log file, ruling out the previously suspected PIPE EOF issue as an
adequate explanation.

The implementation's actual bug was a one-shot timer deadline race:
a timer thread could wake slightly *before* monotonic elapsed time reached
the deadline, return from `_terminate_stalled_inference`, and never check
again. The repair waits out any remaining fractional deadline before
re-checking that the original request still owns inference. A dedicated
subprocess regression forces an eager callback before the deadline.

Final PR #23 head `210a1605b66b4553f4336b4c7fdb92eff07167f6`,
GitHub Actions `38117245421`: both Linux and Windows **success**;
merged at `a8fb0fea30739d2238fbd7ffbf51c631f31699a1`.

This strengthens the existing Bug's evidence; it does not establish
real GPU hang recovery. Do not promote to Canonical.
