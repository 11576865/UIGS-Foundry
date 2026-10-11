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
