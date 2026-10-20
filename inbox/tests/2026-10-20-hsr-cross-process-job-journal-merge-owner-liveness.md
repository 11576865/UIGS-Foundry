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
