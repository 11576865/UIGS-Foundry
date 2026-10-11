# Bug: CVS GPU exclusive group was guarded only within one Runtime Supervisor process

Status: **Bug / source repair submitted / Linux and Windows CI Pending**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Source PR: https://github.com/11576865/Character-Voice-Service/pull/24
Baseline: CVS main after merged PR #23

## Audited defect

`server/runtime_supervisor.py` used one process-local
`threading.RLock` for its startup/stop transitions. The
`exclusive_group` path performed HTTP health probes before the engine
started. Two separate CVS processes could both observe an unused endpoint
before either engine finished booting, then each launch a different
engine assigned to the same physical GPU group. A local RLock cannot
serialize independent service interpreters.

This is a **source-derived concurrency risk**, not a confirmed incident
or user GPU capture.

## Submitted repair

PR #24 introduces a shared-directory OS advisory lock per
`exclusive_group`:

- `fcntl.flock` on POSIX / `msvcrt.locking` on Windows. Locks are
  **create-stable and nonblocking**; a conflict produces a
  `RuntimeConflictError`, rather than spawning a second engine.
- The owning CVS **parent** retains the file descriptor while its managed
  child is alive. Confirmed normal stop, observed exit and spawn failure
  release the lease, while the `.lock` file remains on disk.
- All cooperating CVS processes must use one administratively controlled
  `CVS_DATA_DIR`; separate data directories mean separate lock scopes.
- Tests use independent Python processes, OS lock release after owner kill,
  canonical directory aliases, independent groups and two fake HTTP
  engine supervisors contending for one GPU group. Existing Model Registry
  and crash-loop Windows tests remain in the updated branch.

## Essential limitation

The lock belongs to the CVS parent, **not** the TTS child. If a CVS
parent crashes but leaves a model engine running as an orphan, the OS
releases the parent's lease even though that engine may still occupy
GPU memory. A healthy endpoint can reveal an external owner, but a live
orphan without a responsive health server cannot be ruled out.

External System Supervisor services, unrelated launchers, a second
CVS process with a different data root, and noncooperative processes
do not acquire this lease. The feature does **not** certify universal
physical GPU exclusivity or process orphan cleanup.

## Verification and knowledge placement

PR #24 contains source code, tests and CI wiring, but the new Linux and
Windows jobs are **Pending** at intake, with no real GPU or model-hardware
acceptance. No Canonical adjustment is warranted.

Deduplication: Foundry search for `GPU slot ownership lock`,
`cross-process GPU exclusive`, `runtime slot lease`,
`OS lock process lifetime` and `orphan process GPU` found related
general shared-resource synchronization and CVS IndexTTS crash Bugs,
but no matching CVS-specific independent-interpreter engine-start
race. Record the concrete defect as **Bug**, and link the reusable
principle to the existing shared-resource locking Candidate.


## Follow-up: parent crash releases lock while child may survive — CVS PR #25 (2026-10-11)

PR #24 passed Linux and Windows workflow `38117627282` and merged
into CVS `main` at `4a55200e357649b727195dc37e8231857b2892da`.
That verifies the cooperative cross-process locking implementation in
the automated test environment, **not** the absence of orphaned GPU
workers after a parent crash.

The earlier evidence explicitly noted the unresolved ownership split:
the GPU group lease is held by the CVS **parent**. OS cleanup releases
that lease even if its TTS **child** remains alive or has not exposed an
HTTP health endpoint. A future CVS process could therefore observe a
free lock and mistakenly attempt to start a replacement engine.

[CVS PR #25](https://github.com/11576865/Character-Voice-Service/pull/25)
adds a durable `<exclusive_group>.owner.json` launch receipt to the same
shared slot scope, under the OS lock. It publishes `starting` before
`Popen` and `running` with PID and OS process-creation identity after
the child is created. A later process may clear a previous receipt
automatically only after proving the exact child has exited or the PID
identity has changed. Incomplete intents, live matching PIDs, inaccessible
identities, malformed receipts and unreadable files **fail closed** rather
than advertising the slot as safe.

The implementation uses Linux `/proc` start ticks or Windows
`GetProcessTimes` creation FILETIME for PID reuse protection, with
atomic staged/fsynced JSON publication. Administrative diagnostics
show `ownership-unresolved`. Nine fake-engine/subprocess tests are
committed and Windows CI coverage is wired in. **PR #25 CI Pending**;
no live GPU parent-crash drill has been performed.

Boundaries remain: only the immediate child PID is tracked, not all
possible descendants; separate System Supervisor or launchers without
the same data root/protocol are not participants; an ambiguous receipt
may require deliberate manual reconciliation. This is a follow-up under
the existing concrete Bug, not a new Canonical requirement.


## Verified integration: PR #25 (2026-10-11)

The source PR #25 head
`8136fce26f38179145997e97a99db2f2e6e623d5` passed GitHub
Actions `38118913441`: both Linux `test` and Windows
`windows-script-audit` concluded **success**. PR #25 was then merged
into CVS `main` at `1d333d90ca36e0349f983a4b9278a8fcaae0da60`.

This updates the previous `CI Pending` snapshot above. Cross-platform
tests verified the durable receipt behaviors with disposable child
processes, not with a real GPU, multi-generation TTS process tree, or
independent external System Supervisor. The orphaned-child and
manual-reconciliation limitations remain **FIELD-PENDING**. No
Canonical promotion.


## Further containment boundary — managed engine descendants (2026-10-11)

[CVS PR #27](https://github.com/11576865/Character-Voice-Service/pull/27)
audits a remaining source-level hole after PRs #24–#26: the managed
engine's **direct PID** can exit while independently spawned worker
processes continue consuming GPU resources. Prior `_clean_exited`
and normal stop operated only on `Popen`, potentially discarding a
durable owner receipt and OS lease too early.

The proposed repair places managed GPU-exclusive runtimes in dedicated
POSIX sessions/process groups and checks surviving members before
clearing the receipt; explicit stop sends group-wide TERM and then KILL
with bounded verification. On Windows a Python launcher assigns
**itself** to a kill-on-close Job Object *before* spawning the real
engine, so the normal child and descendants inherit OS job ownership.
The durable receipt carries the kind of process-tree containment;
old records lacking verifiable tree scope fail closed after the direct
PID exits. The admin runtime status exposes surviving group evidence
as `process-tree-unresolved`, preventing automatic replacement.

A cross-platform mock HTTP engine that spawns a separate long-lived
Python child is included as test evidence. The first Linux PR #27 run
`38128784706` failed four new tests because the **test fixture**
omitted the fake engine's `TEST_PORT` environment variable (observed
traceback `KeyError: 'TEST_PORT'`); a follow-up commit
`f2454aa9964df85a16773c173e0c371e60a54515`
supplied this setting. New Linux/Windows CI remains **Pending**.

The scope excludes deliberately escaping descendants, outside process
owners, driver/kernel issues and real GPU/IndexTTS workloads. Do not
assert the process group or Windows job guarantee total GPU cleanup,
and do not promote this single-project observation to Canonical.


## PR #27 verified integration — 2026-10-11

The final source PR #27 head
`f2454aa9964df85a16773c173e0c371e60a54515` passed independent
Linux `test` and Windows `windows-script-audit` jobs in GitHub Actions
run `38128862977`, after correcting a first-run fake engine fixture
(`TEST_PORT` was missing). The PR merged into CVS `main` as
`0bc7fa8a15ecc30ef8962c6611d4eae30179c9b5`.

Cross-platform tests exercise a disposable HTTP engine spawning a
long-lived child. The POSIX test also covers the direct leader exiting
while the descendant survives, the retained GPU lease and durable owner
receipt, refused auto restart and explicit tree-wide cleanup. The
Windows job tests cover the actual kill-on-close wrapper lifecycle.

Evidence is **verified CI for simulated processes**, not a physical GPU
allocation/driver guarantee, external Supervisor adoption, or a proof
against deliberate process group/job escape. The earlier Pending note
above is a historical capture only. No Canonical promotion.


## Actual CVS parent-kill fault injection — PR #28 (2026-10-11)

Earlier cross-process tests modeled a dead CVS parent by manually
releasing its OS lease. [CVS PR #28](https://github.com/11576865/Character-Voice-Service/pull/28)
adds a **real second Python interpreter** running RuntimeSupervisor,
launching a disposable HTTP engine and a long-lived child worker.
The test forcibly kills the CVS controller process without shutdown,
checks the OS GPU slot lease becomes acquirable while the engine and
worker survive, and verifies a new independent controller with the
same `exclusive_group` and shared receipt refuses replacement launch.

Another real-controller fault injection stops the first controller
after `starting` intent publication but **before engine Popen**;
a replacement controller must preserve ambiguous evidence and refuse
automatic restart. This distinguishes a known-empty test fixture from
real production ambiguity (no automated stale-intent removal).

During audit, Linux `_live_posix_group_members` was also found to
silently skip all `OSError` conditions when reading procfs entries.
An unreadable process entry due to permissions could have belonged to
the target session; treating it as absent could falsely authorize GPU
lease release. The proposed fix distinguishes transient disappearance
(`FileNotFoundError`) from unreadable entries (`PermissionError`
and other I/O errors), returning unknown and failing closed when
process-tree emptiness cannot be established. Two Linux regression
tests inject both cases.

PR #28 head `1e53dcd56ecc93fcc20d1cdfd1da12704e5f87b6`:
Linux full tests **success** in workflow `38130752048`;
Windows targeted CI was still in progress at this intake.
No merge or physical GPU-field acceptance is claimed here.

Deduplication: further process-lifetime fault-injection evidence for
this existing concrete Bug and the shared-resource scope Candidate,
not a new Canonical rule.


## PR #28 cross-platform verification and merge

The final PR #28 head `1e53dcd56ecc93fcc20d1cdfd1da12704e5f87b6`
passed both Linux `test` and Windows `windows-script-audit` jobs in
GitHub Actions run `38130752048`. GitHub reported a clean, mergeable
five-file delta and merged it into CVS `main` as
`d0c3d3871713400bdb657dda9e786145052ffa00`.

The tests really killed an independent CVS mock controller while its
mock engine and worker survived; they demonstrated that a freed parent
lease does not permit a second controller to override a live durable
owner receipt. Windows executed the Job Object path and Linux the
POSIX session path. The Linux-only procfs tests confirmed unknown
visibility fails closed, unlike a vanished PID.

This supersedes the earlier PR #28 Windows CI Pending snapshot.
**Real TTS GPU memory reclamation and actual System Supervisor
interoperability remain FIELD-PENDING**; no canonical promotion.
