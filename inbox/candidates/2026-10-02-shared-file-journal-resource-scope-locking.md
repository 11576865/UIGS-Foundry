# Candidate: Shared file journals need synchronization at the shared-resource scope

Status: candidate
Date: 2026-10-02
Domains: reliability, architecture

## Summary

Method-level or instance-level synchronization is insufficient when multiple object instances operate on the same fixed filesystem journal or staging paths.

If two instances both use names such as `latest.tmp` / `latest.meta.tmp`, one instance can clear, replace, or overwrite staging files between another instance's stage and read-back verification even when every public method is individually `synchronized`.

Synchronization must be scoped to the shared resource, not merely to the object instance that happens to access it.

## Evidence

ASS-Workbench-Android uses multiple `RecoveryStore` instances that share the app recovery directory. Its staged recovery write uses fixed paths:

- `latest.ass.tmp`
- `latest.meta.tmp`
- `latest.ass`
- `latest.meta`

Android Emulator Regression for Edge Bookmark integration #63 failed independently in the existing destruction regression:

```
java.io.FileNotFoundException:
.../recovery/latest.ass.tmp: ENOENT
at RecoveryStore.write(RecoveryStore.kt:48)
```

The staged ASS file had already been written, but disappeared before read-back verification. The pre-fix methods were `@Synchronized`, which only locked each RecoveryStore instance and therefore did not serialize another instance's `clear()` / `write()` against the same directory.

A product-side fix is under validation in ASS-Workbench-Android PR #64: all journal IO operations use one process-wide monitor, plus a multi-instance write/write/clear instrumentation stress test.

## Candidate rule

For a shared file journal with fixed staging or target paths:

1. Identify the actual shared-resource scope (directory/path/process/database), not just the object scope.
2. Serialize stage, verify, publish, read, and clear operations at that shared scope.
3. Do not treat instance-level `synchronized` as sufficient when independent instances can address the same files.
4. Keep the entire stage → verify → publish transaction inside the shared critical section.
5. Add a multi-instance concurrency test that exercises write/write/clear or equivalent conflicting operations.
6. If cross-process access is possible, a process-local monitor is insufficient; use an OS/file/database coordination mechanism appropriate to that authority boundary.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- source PR exposing failure: `#63`
- failing workflow: `36986759434`
- failure test: `EditorRegressionInstrumentedTest.repeatedActivityRecreationDoesNotMutateDirtyDocument`
- product fix under validation: `#64`
- fix head at capture: `48fb34a7c90046aebce2f502e1046ed641ab49e4`
- evidence level: observed emulator failure + code-level shared-resource analysis; fix CI pending at capture time

This is a Candidate only. It is not Canonical.


## Follow-up: cross-process Model Registry lost-update boundary — CVS PR #20 (2026-10-10)

In `11576865/Character-Voice-Service`, [PR #20](https://github.com/11576865/Character-Voice-Service/pull/20) advances the same shared-resource synchronization principle from in-process recovery journals to a Model Registry that can be written by independent service/CLI processes.

- A uniquely staged, fsynced and atomically replaced `model-registry.json` prevented partial JSON reads, **but did not prevent Lost Update**: two processes could load the same old snapshot and then overwrite each other's independent lifecycle mutations.
- The repair holds an advisory OS exclusive file lock over the **entire read-modify-write transaction** for `scan_model_root`, `set_status`, `promote_model` and `retire_model`; the scan includes directory discovery and weight verification, not merely its final save.
- The lock identity is the canonical registry path, and its `.lock` file persists on disk rather than being deleted/recreated. Linux uses `flock`; Windows uses a byte-range lock. Cross-process regression tests use separate Python interpreters and force overlapping model status updates.
- Lock ownership is cooperative. A direct low-level whole-snapshot overwrite with stale data, an external writer ignoring the lock, or uncoordinated edits to physical model artifacts remain outside this protection.
- Evidence is **source+test implementation submitted, Pending CI**, not a verified production incident or a passing Linux/Windows workflow. Source PR is stacked on CVS #19; merge reconciliation remains outstanding.

Dedup assessment: this is implementation evidence for the existing shared-resource-scoped synchronization Candidate, not a new generic lock rule. It also relates to the [CVS Model Registry Bug](../bugs/2026-10-10-cvs-model-registry-promotion-identity-integrity-gaps.md) as a concrete project repair. **No Canonical promotion.**


## Follow-up: cross-process GPU engine slot ownership — CVS PR #24 (2026-10-11)

Related project Bug: [CVS GPU slot process-local lock](../bugs/2026-10-11-cvs-runtime-gpu-slot-process-local-lock-allows-overlap.md).

The same resource-scoped mutex principle applies beyond mutable files.
CVS Runtime Supervisor can start a single-concurrency model engine assigned
to a GPU `exclusive_group`. An `RLock` guarded only one Python server;
two independently launched CVS interpreters could both see unhealthy
engine endpoints during boot and start competing GPU workloads.

[CVS PR #24](https://github.com/11576865/Character-Voice-Service/pull/24)
adds a **persistent OS lease** per GPU group, kept open from before child
creation until the owned child exits. Cooperative contenders fail
immediately instead of starting another engine. Tests exercise two real
Python interpreters, aborted lock owner, distinct groups and mock HTTP
engine lifecycles. The relevant resource scope is the **shared GPU group**,
not the individual HTTP endpoint, Python interpreter or model ID.

**Important counterexample to overgeneralization:** the lease is held
by the CVS **parent**. When that parent dies and a child remains alive,
the OS releases the lease while the GPU is potentially still in use.
External supervisors and unrelated processes that do not share the
protocol also remain outside the lock. Therefore this is cooperative
process-lifetime serialization, not proof of physical GPU ownership.

At intake, code and tests are submitted but PR #24 CI and real
hardware acceptance are Pending. Record as a cross-project evidence
extension of this existing Candidate, **not a new Candidate or
Canonical rule**.


## Follow-up: parent-owned lease must not imply child-owned resource absence (2026-10-11)

The CVS GPU group [PR #24](https://github.com/11576865/Character-Voice-Service/pull/24) cross-process OS lease passed Linux and Windows CI and merged. Its ownership boundary nevertheless ends at the CVS **parent process**. If the parent dies while its managed TTS child survives, the lock can be acquired by another CVS process even though the GPU is still occupied.

[CVS PR #25](https://github.com/11576865/Character-Voice-Service/pull/25) proposes a complementary **durable launch intent / process-identity receipt** under the same resource-scoped lock: write `starting` before spawn, change to `running` after obtaining PID plus creation identity, and require affirmative proof of process disappearance or PID reuse before auto-clearing. Unknown, inaccessible and partially published states block admission and are shown in admin diagnostics.

This illustrates a distinct boundary in shared-resource coordination:
**the lifetime of a synchronization holder is not necessarily the
lifetime of the resource it launched**. Lock release can be correct
without meaning the GPU or its descendants are free.

Evidence remains implementation-plus-regression tests under PR #25,
**CI Pending** at intake, no real orphan GPU acceptance. Append as
incremental evidence to this existing Candidate; do not generalize to
Canonical based on this one incident-free source audit.


### Validation update — CVS PR #25

The durable launch receipt follow-up above passed Linux and Windows
GitHub Actions run `38118913441` and merged to CVS `main` as
`1d333d90ca36e0349f983a4b9278a8fcaae0da60`.
This verifies mocked Linux/Windows process-identity and receipt
regressions, **not** physical GPU-orphan recovery. The original Pending
note is historical; the hardware/independent-supervisor gap remains.
Candidate only, no Canonical promotion.


## Follow-up: file-command idempotency for external runtime activation (2026-10-11)

[CVS PR #26](https://github.com/11576865/Character-Voice-Service/pull/26)
applies the shared-resource-scoped synchronization principle to a
**file-based command inbox** owned by an external System Supervisor.

Before this repair, CVS could concurrently publish several
`activate-engine` messages for the same service from independent
processes, and a timed-out activation left no durable identity blocking
later duplicate submission. The submitted change scopes the OS lock to
the canonical request directory plus exact `service_key`, and persists
a pending request identity **before** publishing the command. Concurrent
or subsequent callers do not replay while outcome is unconfirmed.
Internal pending state is kept outside the top-level `*.json` command
inbox, so a consumer cannot mistake it for a command. Live health
observations, rather than an asynchronous stale status file, decide
whether the external endpoint is actually ready.

This is an example of **single-flight admission plus durable uncertain
outcome**, not an exactly-once guarantee from the external consumer:
only a correlated System Supervisor acknowledgment could establish
that a particular `request_id` was acted on. A failed or interrupted
publication can conservatively require operator reconciliation.

At intake PR #26 has implementation and 15 fake-engine / OS-lock
regression tests submitted, with **Linux/Windows CI Pending** and real
System Supervisor interoperability FIELD-PENDING. Append to the
existing Candidate after deduplication, **not Canonical**.


### Validation update — CVS external activation single-flight

Final [CVS PR #26](https://github.com/11576865/Character-Voice-Service/pull/26)
head `7e31f88a31e7d0ffbf6264ee939b648603ed536b` passed both Linux
and Windows jobs in GitHub Actions `38120009311` and merged into
`main` at `568f2cc6643dbae9b35e9632488d4575b5423227`.

This verifies the implemented file-based control and OS-lock test
contracts, not real external System Supervisor request/response
interoperability, GPU lifecycle authority or exact request-correlated
acknowledgment. Candidate evidence only; no Canonical promotion.


## Follow-up: process-tree lifetime exceeds direct PID lifetime (2026-10-11)

[CVS PR #27](https://github.com/11576865/Character-Voice-Service/pull/27)
extends the process-ownership boundary again. A managed GPU engine
may spawn descendants that outlive its direct `Popen` PID. Releasing
the resource-scoped GPU OS lease when only that PID dies is therefore
insufficient. The submitted implementation uses an independent POSIX
session/group or a Windows kill-on-close Job Object wrapper and ties
durable receipt clearing to that containment boundary.

This reinforces the Candidate's distinction between **scope of a
synchronization primitive** and **lifetime of a physical resource
across descendants**. It is supported by source audit and a fake
engine that creates a long-lived child. The first Linux CI failed due
to missing `TEST_PORT` test fixture setup; subsequent CI is Pending.
Actual GPU, intentional process escape and external System Supervisor
cases remain FIELD-PENDING. This is a deduplicated Candidate extension,
not Canonical.


### CI evidence update — CVS managed process-tree containment

Final [CVS PR #27](https://github.com/11576865/Character-Voice-Service/pull/27)
head `f2454aa9964df85a16773c173e0c371e60a54515`
passed GitHub Actions `38128862977` on Linux and Windows and merged
to main at `0bc7fa8a15ecc30ef8962c6611d4eae30179c9b5`.

The first CI failure was a missing fake-engine `TEST_PORT` fixture,
not a verified process tree design failure. This second CI run exercises
mock TTS-descendant teardown, Linux orphan session checks and Windows
Job Object execution. Real GPU, external lifecycle owners and process
escape scenarios remain FIELD-PENDING; no Canonical change.


## Follow-up: real controller-death injection and incomplete procfs observability (2026-10-11)

[CVS PR #28](https://github.com/11576865/Character-Voice-Service/pull/28)
extends prior simulated parent-lock release with an actual independent
CVS Python controller process that is abruptly killed while its
managed mock engine and worker child survive. The OS lease is correctly
released by controller death, but a new owner must still reject the
durable PID/process-identity receipt before spawning competing work.
A second injected crash occurs between the durable `starting`
publication and the engine's `Popen`; the intent remains unresolved
and blocks replacement.

A related Linux audit found that merely skipping an unreadable
`/proc/<pid>/stat` entry can cause a group scan to claim no remaining
resource owners. The proposed change treats permission-denied
observations as **unknown** and distinguishes them from confirmed
transient process disappearance. This reinforces the Candidate's
core distinction: **not observing an owner** is not equivalent to
**proving the resource is unowned**.

At intake the PR #28 Linux full suite had succeeded, but Windows
CI was Pending. Tests use disposable mock processes, not GPU hardware
or external System Supervisor. Append to the existing Candidate
without promoting Canonical.


### Confirmed CI and integration — PR #28

CVS [PR #28](https://github.com/11576865/Character-Voice-Service/pull/28)
head `1e53dcd56ecc93fcc20d1cdfd1da12704e5f87b6` passed independent
Linux and Windows jobs in GitHub Actions `38130752048` and merged as
`d0c3d3871713400bdb657dda9e786145052ffa00`.
Both OSes exercised a genuinely killed mock CVS parent. This confirms
the cooperative durable receipt and process-scope acceptance tests,
not physical GPU process/driver cleanup or an external Supervisor
consumer. The earlier Pending CI status above is historical.
No Canonical promotion.
