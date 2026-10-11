# Candidate: Green CI requires cross-boundary invariant coverage, not only per-layer tests

Status: candidate
Date: 2026-10-03
Domains: reliability, testing, cross-platform-contracts, operations

## Summary

A repository can have broad green CI while still missing regressions created at the seams between individually tested layers.

The failure mode appears when:
- one layer produces a versioned task or capability;
- another layer advertises support for that version/capability;
- a downstream parser/executor accepts a different set;
- CI exercises each layer separately or with stale fixtures.

Likewise, UI smoke can prove that a control exists and a mocked task compiles while never exercising the real backend path, large-source lifecycle, or alternate workflow presentation that owns the same setting.

## Observed case

Quick-Automatic-Hardsub-Encoder after media task schema v3 / fork-join integration showed three green-CI blind spots:

1. Windows advertised `taskSchemaVersion=3`, while `windows/media-task.ps1` accepted only v1/v2. Existing Windows smoke fixtures used v1/v2 and therefore remained green.
2. Audio strategy existed in the manual task workspace and task compiler, but guided hard-sub still hard-coded `-c:a copy`; UI smoke did not execute the guided audio choice through the real encode backend.
3. Browser probe and execution each staged the same selected large source. Unit/integration tests used small or mocked media and did not exercise the probe -> execute lifecycle with source reuse, so the user-visible “reading source” stall was not detected.

## Candidate rule

For features that cross UI, task compiler, capability advertisement, parser, executor and output verification, maintain an explicit invariant matrix.

Each critical invariant should identify:
- producer;
- advertised capability;
- consumer/parser;
- executor;
- verification/output evidence;
- current-version test fixture;
- at least one end-to-end path crossing the real boundary.

A green test for each component separately is insufficient if no test crosses the boundary where the contract is transferred.

When a schema/capability version changes, CI should fail unless the current producer version is exercised against every claimed consumer.

When a shared setting has multiple presentations (for example guided vs manual), each presentation that claims the capability needs at least one behavioral test that reaches task compilation or execution.

Large-file/runtime lifecycle risks should have dedicated lifecycle tests; tiny synthetic fixtures are not evidence that repeated staging or memory behavior is acceptable.

## Relationship to existing UIGS knowledge

This complements the existing requirement/evidence traceability candidate. That record separates implementation state from evidence coverage per requirement.

The additional rule here concerns **cross-boundary evidence topology**: evidence must cross the same interface boundary that can fail in production, rather than remaining partitioned by layer.

It also aligns with the Canonical governance rule that CI success is not equivalent to device validation.


## Implemented pilot

A first operational pilot is now in place.

Foundry commit `92e5660cf595cfd8a24e9a4c063bff15e50192bd` adds:

- `schemas/invariant-evidence.schema.json`;
- `tools/validate_invariant_evidence.py`;
- validator unit coverage;
- an optional `invariant_evidence` source-project manifest declaration;
- protocol documentation for routing evidence-coverage failures through the existing Pending intake path.

Quick-Automatic-Hardsub-Encoder commit `ca9f2e2fbbbb53fe3ebafd3e84efc81999032d57` pilots the mechanism with five active invariants:

1. current media task schema version alignment across producer, Windows/Android advertisement, parsers and CI fixture;
2. explicit audio-policy wiring across shared output UI, Guided hard-sub and Web/Windows/Android execution paths;
3. stream-copy-only semantics for lossless trim, including real FFmpeg packet-identity evidence;
4. browser source-staging reuse across probe -> execute;
5. explicit output-container resolution.

The new `UIGS Evidence Coverage` workflow passed on the pilot commit. Its workflow is also tracked by the existing UIGS Intake Adapter, so an evidence-coverage failure becomes a Pending packet instead of remaining a silent green-CI coverage gap.

The ordinary frontend workflow also passed the new cross-backend Guided-audio wiring regression test plus existing real-FFmpeg integration tests.

This implementation is evidence for the Candidate; it does not promote the rule to Canonical.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- incident date: 2026-10-03
- related repairs: `8645d596`, `e575a5db`, `b4a6acae`, `5087c061`, `4f763585`
- evidence level: three concrete regression classes + repaired automated tests
- status rationale: reusable testing architecture candidate; not Canonical

This is a Candidate only.


## Guided output verification parity checkpoint — PR #89 (2026-10-11)

QHE Windows Native previously used a stronger output contract for manual tasks (stream counts, duration, packet scan) than Guided hard-sub (video stream header plus strict-mode byte ceiling). This is a cross-workflow verification gap even when both share the same Bridge. [PR #89](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/89) submits a guided final-output validation step requiring one video stream, expected audio count where supplied, nonzero/near-expected duration, and FFmpeg stream-copy packet scan **before** completed/exportable state. The Native test fixture now carries two real audio tracks to exercise copy preservation under software two-pass and strict under-limit policies.

**Status: implementation submitted, Pending CI; no full decoding, physical Windows hardware or long-form acceptance inferred.** This extends the existing cross-boundary Candidate rather than creating a duplicate or promoting Canonical.


## Long-form Guided verification claim correction — QHE PR #90 (2026-10-11)

Source check after #89: the Windows Guided finalization path verified stream count, duration and a full **packet remux-to-null** scan, but the production UI text claimed "packet scan + full decode passed". A stream-copy scan is not frame-by-frame decoder acceptance; treating one as proof of the other is an evidence-to-presentation contract mismatch. The reconciled [PR #90](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/90) (`56535f5cf5b78fab207c41885fbe813984ac015f`) changes the UI completion claim to the exact verification scope, and caches the verified Guided duration so later long-movie completed-status requests do not repeatedly start FFprobe.

Status: source-verified defect and submitted correction / **Pending integrated-branch CI**. This does not claim all long movies can be decoded or that packet checks replace full decode. Existing Candidate only; no Canonical promotion.


## Re-audit: CVS green lifecycle CI did not prove voice/model/audio identity (2026-10-11)

The October 11 CVS foundation re-audit found a **stronger
cross-boundary invariant gap** than the earlier token-bootstrap risks:

- `server/backends/gpt_sovits.py` uses a Python-process-local
  `threading.Lock` and a cached pair of weight paths. Two CVS
  processes sharing one GPT-SoVITS endpoint do not share the mutex;
  a restarted backend can have a new model state while an old CVS
  process's weight cache remains unchanged. The runtime OS GPU lease
  protects model process **launch**, not model switching plus in-flight
  inference.
- `RuntimeSupervisor::_enforce_exclusive_group` may stop another
  owned engine in the group without checking whether it is serving
  an active synthesis request. A healthy URL also does not attest
  serving model identity.
- The public speech API emits requested-model provenance and
  `audio/wav` success metadata even though the GPT-SoVITS adapter
  reads upstream HTTP bytes without verifying WAV decodeability;
  existing tests explicitly treat `b"wav-data"` as successful
  audio and use `b"RIFF....WAVE"` in contract mocks.

These are source-confirmed missing guarantees, not real wrong-voice
GPU field incidents. Concrete records:

- [Serving model identity transaction Bug](../bugs/2026-10-11-cvs-serving-model-identity-not-transactionally-bound-to-inference.md)
- [Speech WAV success contract Bug](../bugs/2026-10-11-cvs-audio-wav-success-lacks-payload-validation.md)

**Reusable test boundary**: A green process-lifecycle/HTTP/status
suite does not prove semantic integrity of a response. Require
`selected model/reference -> backend serving epoch -> inference
admission -> decodeable output -> provenance` to be verified across
independent clients and backend restarts. Existing source CI did not
establish this chain; regression design and hardware tests are still
Pending. This is a deduplicated Candidate extension, **not
Canonical promotion**.


## Submitted CVS repair: make model serving an indivisible inference transaction (2026-10-11)

[CVS PR #32](https://github.com/11576865/Character-Voice-Service/pull/32)
extends the previous source audit with a cooperating multi-process
endpoint-scoped model-switch/inference OS lock. A durable pending
transaction survives an abrupt CVS controller death, because that
process's OS lock can release while the actual backend keeps
generating. With no backend model/epoch attestation, the repair
explicitly reasserts both managed weights on every request rather
than treating a client-side path cache as model residency evidence.

New acceptance fixtures use an independent HTTP mock backend and
two independent CVS interpreters to force model-switch races and
controller death during inference; Windows CI now runs the
previously omitted GPT-SoVITS and public API contract tests.

**PR #32 is Pending CI at intake.** These are not real audio content,
GPU, noncooperating backend clients or coordinated sibling-runtime
teardown tests; source-correctness and test selection are distinct
from field acceptance. Added here after deduplication, not to
Canonical.


### PR #32 verified multi-process serving transaction

CVS [PR #32](https://github.com/11576865/Character-Voice-Service/pull/32)
head `7cf2ecacaac8d5927addf50fd31cf7cbfe47747b`
passed independent Linux and Windows jobs in GitHub Actions
`38139136194` and merged as
`7d2ecd1d4e91b1aac77384c1729c2619475e3c8c`.

New tests use separate CVS interpreters against a disposable HTTP
fake backend to exercise cross-process model-switch refusal,
backend restart stale-cache avoidance and fail-closed durable
unknown-inference-state after CVS death. Physical voice/GPU correctness,
noncooperating clients, and active-request-aware GPU sibling
handoff remain unproved. Candidate only; no Canonical promotion.


## GPU group handoff must share inference admission (CVS PR #33, 2026-10-11)

[CVS PR #33](https://github.com/11576865/Character-Voice-Service/pull/33)
extends the serving transaction correctness work after PR #32:
per-backend model-weight locks cannot prevent a **different**
managed GPU engine from auto-stopping the entire process that
currently serves an inference. A one-shot health/busy check is
also subject to a check-then-act race.

The proposed implementation uses a single cross-process
**group activity lease** for beginning inference and all
managed lifecycle operations, with a durable inference-pending
receipt when the controller dies mid-request. It explicitly
distinguishes this from both the persistent process lifetime
lease and the endpoint weight-switch transaction lock.
A locally rejected request does not permanently poison the group.

Nine tests with a disposable live managed HTTP runtime, real
interpreter-held group lease and controlled controller death
were submitted. **Linux/Windows CI pending at intake**;
actual IndexTTS/GPT-SoVITS inference and GPU drivers not
tested. This is a deduplicated Candidate extension to
cross-boundary invariants, **not Canonical**.


### PR #33 validated group activity + lifecycle admission

Final CVS PR #33 head
`9171399a2037831ad289cad7ed5ce32114a9c7c6`
passed Linux and Windows jobs in Actions run
`38140671243` and merged into `main` as
`1aa568047b2564e5f1e5eebacfa3fb2fc7ea66f8`.

The evidence exercises cooperating CVS activity leases, durable
inference receipts and mock cross-process group stop/switch refusal;
it does not prove physical GPU process quiescence, external
Supervisor cooperation, accurate real-model voice identity
or valid WAV output. Keep this as Candidate evidence without
Canonical promotion.
