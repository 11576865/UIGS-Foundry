# Test / Observation — HSR shared jobs journal lost-update and live-owner recovery

Date: 2026-10-20
Project: `11576865/HSR-Voice-Archive-Builder`
Repair: [PR #197](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/197)
Merged main: `7aec0361206c211512aced0e1ef233fe03732a81`
PR tested head: `fcb195df1a51e9eee548f78dea27d8355c2d4fc5`
Level: **Test/Observation, source integrated + exact-PR-head Linux/Windows CI passed; post-merge and field acceptance separately pending**

## Issue isolated from PR #196
The existing HSR `app/jobs.py` guarded project output files using an OS writer lease, but persisted the *entire* process-local `_JOBS` into one shared `jobs.json` with no journal-scoped OS lock. Two servers could overwrite each other's independent jobs. The startup `_load_previous` also marked all `queued`/`running` entries `interrupted` without checking whether another HSR process was still alive. Atomic JSON file replacement prevented torn reads but did **not** prevent lost updates or false interruption.

## Repair and evidence
- `app/job_journal.py` keeps the legacy JSON-list format while acquiring a durable OS lock at the shared journal-resource scope across read/merge/write; locally owned job records are merged with latest disk entries rather than overwriting foreign live jobs.
- A unique per-interpreter UUID with retained OS file lease distinguishes a live producer from a provably exited one; incomplete legacy owner information is marked interrupted on recovery. OS lock sessions release explicitly at Python `atexit`.
- Foreign job records are refreshed for status endpoints and admission checks; failed durable queue admission rolls back its own memory-only queued entry.
- Real subprocess tests start two independent Python service actors writing overlapping jobs and a third inspector. They assert both job IDs persist; a live other-owner job stays `running` after a third instance's startup; killing only owner A marks only job A interrupted while B remains running.
- Corrupt or malformed JSON is not silently replaced upon new job admission. Native Windows workflow also exercises earlier cross-process output-writer tests.

## Exact-head CI
- [`tests` #39441959682](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39441959682): Python 3.11/3.12/3.13, Termux Lite surface, real libass — success.
- [`seven ASS` #39441959669](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39441959669): success.
- [`HSR Windows writer and journal safety` #39441959667](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39441959667): success on Windows runner.

## Windows red-to-green caveat
The first Windows CI run #39441611983 found an output encoding problem in the earlier `tests/test_project_writer_lock.py` child: it printed a Chinese lock failure into a default cp1252 console and raised `UnicodeEncodeError`, leaving an unexpected process exit code. The **lock was actually rejecting contention**. The test was corrected to print an ASCII sentinel independent of console locale. New process-session lease explicitly closes at interpreter teardown, avoiding a shutdown-time import warning. Do not confuse this fixture output error with an OS lock failure.

## Limits / Pending
- OS-user-scope and cooperative-process locks only; not cross-user or distributed access. Physical Windows workstation, Android Termux and abrupt power-loss tests remain FIELD-PENDING.
- A process-independent legacy media/archive corruption proof is not established by jobs journal tests.
- The background jobs journal preserves concurrent admitted state, but automated cancellation, global process supervision, and cross-process deletion tombstones are not asserted complete.
- Exact merged-main post-merge CI must be checked separately from PR-head runs.

## Dedup and epistemic boundary
General lost-update law is already in `inbox/candidates/2026-10-02-shared-file-journal-resource-scope-locking.md` (ASS recovery store and CVS model registry). This HSR-specific test records *live owner vs dead owner classification* and two-service journal state continuity, not a new Canonical rule. No Canonical promotion.

## Exact merged-main CI closure (2026-10-20)

HSR `main@7aec0361206c211512aced0e1ef233fe03732a81` passed all four triggered workflows:
- [Python tests / Termux Lite / real libass #39442235231](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39442235231)
- [Seven ASS #39442235336](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39442235336)
- [Native Windows process and journal safety #39442235498](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39442235498)
- [Pages build/deploy #39442240490](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39442240490)

Status: **source integrated, exact-main automated regression verified**. Further Pending: physical Android/Termux and actual Windows customer machine, abrupt power removal, very long-running jobs, cross-process deletion tombstones and stale historical records. One-time CI does not prove these boundaries. Canonical unchanged.

## 2026-10-21 extension — durable deletion tombstones and waitable journal lock, HSR PR #198

Deduplicated against this existing job journal Test and the shared-resource journal Candidate: this adds failure-specific evidence, **not** a new Canonical rule.

- Repair [HSR PR #198](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/198), tested PR head `dcfeee12d6755abf3bad41f05624299a019457ec`, merged to `main@f366f3fc6da47b8c06bb961945d4658da21d6a98`.
- A completed historical job deleted by one process could be resurrected by another still-live process's stale owned `_JOBS` snapshot. A persistent `jobs.json.deleted.json` sidecar, published before the updated JSON list under the same journal mutex, now vetoes later resurrection. A two-file power failure may temporarily leave a tombstoned row in the raw legacy `jobs.json`; coordinated recovery filters it. Tombstones are retained; compaction remains Pending.
- Existing services now reconcile dead-owner session leases when serving job status, not only on fresh server startup. Unknown owner state is not equated with proof of death.
- CI failures on the first PR revisions exposed a distinct generic concurrency issue: the shared journal reused the **nonblocking, fail-fast output-writer lock**. This caused short-lived journal contention to kill a valid child job, later misdiagnosed as `interrupted`. The repair adds a 15-second bounded retry for the journal's short read/merge/write critical section. Media writer admission remains fail-fast. A dedicated independent-process test verifies waiting and eventual success.
- Fault injection covers a crash-like failure after the deletion ledger is atomically published but before `jobs.json` is rewritten, plus stale-owner replay and malformed-ledger fail-closed semantics.
- The earlier red workflow runs are real CI evidence for an unsafe assumption and should **not** be counted as passing. Final exact PR head passed [Python/Termux `tests` #39462464890](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462464890), [seven ASS #39462464379](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462464379), and [native Windows process safety #39462464420](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462464420).
- Post-merge exact-main CI, physical Android/Termux and Windows user device, power cut and tombstone garbage collection still require separate evidence. This repair does not claim a multi-file ACID transaction or cross-user/distributed durability.

**Status:** Test/Observation integrated with automated PR-head evidence; keep field and safe-compaction tasks Pending. Canonical unchanged.
