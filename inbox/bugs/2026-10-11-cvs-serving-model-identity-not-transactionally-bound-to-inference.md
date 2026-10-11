# Bug: CVS serving model identity is not transactionally bound to synthesis

Status: **Source-confirmed invariant gap / not yet reproduced on real GPU**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Audited main: `184d481c8cae911643a3a059211bbd71cbece20e`
Severity: **P0 potential wrong-voice / model-identity correctness risk**

## Invariant that must hold

For each user speech request, the selected `model_id`, reference,
configured runtime/engine identity, *actual loaded weights during
inference* and emitted `X-CVS-Generation-Revision` should refer to
the same serving transaction. A process-start lock, a health probe,
or a process-local model-switch lock alone does not establish that
invariant when several CVS processes can address one TTS backend.

## Source evidence

1. `server/backends/gpt_sovits.py` tracks the backend state with the
   module global `_active_managed_model: tuple[str, str] | None` and
   serializes `_ensure_selected_model() + /tts` with a **local**
   `threading.Lock`. Independent CVS Python workers do not share
   this state or mutex. Both can send `/set_sovits_weights`,
   `/set_gpt_weights` and `/tts` to the same registered endpoint,
   interleaving a model change with another request's synthesis.
2. That global cache contains **weight paths only**, with no backend
   process incarnation/epoch. `runtime_supervisor.py` can restart a
   managed engine independently, while `gpt_sovits.py` does not
   subscribe to engine death/restart or invalidate the cached weight
   signature. A newly started backend can have different loaded
   weights even when the client-side signature still matches, causing
   a switch to be skipped incorrectly.
3. `server/runtime_supervisor.py::_enforce_exclusive_group()` calls
   `_stop_owned(engine_id, other)` on a healthy *owned* sibling
   sharing the GPU group before starting a replacement. It does not
   establish whether another HTTP synthesis request is currently
   executing against the old backend, or wait for in-flight inference
   to drain. Even if this auto-stop is a documented policy, it is
   not safe as a request-level handoff guarantee.
4. `RuntimeSupervisor.start()` and `ensure_ready()` accept a live
   HTTP health response as sufficient to proceed without acquiring
   the current process's launch lease or confirming the backend's
   active model. `app.py` computes response provenance based on
   selected/registered config, not a correlated backend-side loaded
   model attestation.
5. `server/app.py::speech()` calls `runtime_supervisor.ensure_ready()`;
   `server/engines/__init__.py::synthesize()` repeats
   `ensure_ready()`, but neither admission protects model residency
   **through the entire inference**.
6. Unit test `tests/test_gpt_sovits.py` verifies one process's
   switch cache and request ordering, not backend restart identity,
   simultaneous independent CVS workers, or an in-flight inference
   surviving sibling group switch. The Windows targeted CI command
   does not include `tests/test_gpt_sovits.py`.

## Failure mechanism and impact

Example conditional trace, **inferred rather than observed**:

- CVS A loads model A and caches A.
- A shared GPT-SoVITS process restarts, potentially loading a default
  model B. CVS A's process-local cache still says A.
- New request asks for A. CVS A skips the weight switch and sends
  `/tts`. The response may contain audio from B but CVS publishes
  selected-model A metadata.

A second conditional trace is A and B cross-process switching the
single shared backend between each other's `/set_weights` and `/tts`.

This is a **source-confirmed missing synchronization/identity proof**,
not evidence of an actual wrong-voice recording or of a security
breach on a user machine.

## Required regression gates before resolution

- A deterministic fake-backend *restart epoch* test that forces the
  backend to drop loaded weights while CVS retains its local cache;
  new synthesis must reload/verify the exact expected model.
- Two independent CVS OS processes with model A/B sharing one fake
  weight-switch backend, interleaved with barriers; no request can
  synthesize under another request's model identity.
- In-flight A inference while same exclusive GPU group is requested
  for B: do not kill A until an explicit admission/drain decision.
- Correlate the backend model identity and runtime epoch with the
  request's emitted provenance, or fail the request when it cannot
  be established.
- Windows CI and Linux CI actually run these invariants, followed by
  real GPT-SoVITS model/GPU field acceptance.

## Deduplication

Foundry searches for `GPT-SoVITS wrong voice cross process switch`,
`model cache restart voice drift`,
`shared backend weight switching lock` and
`runtime same GPU group in flight request` found a related general
shared-resource-locking Candidate and a validated
`ARCH.RUNTIME.EXCLUSIVE_RESOURCE_OWNERSHIP` pattern, but no matching
CVS serving-model transaction Bug. That pattern's lifecycle-ownership
rule does not assert per-synthesis model consistency. This belongs in
**Bug**, not a change to Canonical.

Status remains **OPEN / reproduction and repair Pending**.
