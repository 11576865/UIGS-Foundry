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

### PR #198 exact merged-main CI closure (2026-10-21)

At HSR `main@f366f3fc6da47b8c06bb961945d4658da21d6a98`, all four independently triggered workflows passed:
- [Python 3.11/3.12/3.13, Termux Lite, real libass `tests` #39462745051](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462745051)
- [Native Windows job-journal/process tests #39462745100](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462745100)
- [Seven ASS requirements #39462745133](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462745133)
- [Pages build/deployment #39462704444](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39462704444)

**Disposition:** HSR code integrated, exact-main CI verified. Ongoing Pending: actual Android/Termux and Windows end-user devices, power-loss timing between two atomic JSON files, test-driven safe tombstone compaction, and very long job retention/supervision. No Canonical promotion.

## 2026-10-21 — PR #199 conservative tombstone compaction under original owner liveness

Deduplicated extension of this HSR Test and the 2026-10-02 shared-resource synchronization Candidate, not a new Canonical rule.

- HSR [PR #199](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/199), final tested head `49ae30ea6e1b722ad5de6d915686f092f8e4f32d`, merged `main@69c6ce92f7356dbd18a32be695e3c8369b266494`.
- PR #198's v1 deletion ledger contained only job IDs, so a supposedly safe old tombstone could not be proven free of a running stale writer. PR #199 introduces a backward-compatible v2 ledger containing the original `owner_sessions` identity for **new deletions only**; legacy v1 and any tombstone without a valid owner remain uncompactable. A deletion mark can be removed only when its producer session lease is verifiably no longer held.
- `compact_tombstones` acquires the shared journal mutex, commits the deletion-filtered `jobs.json` **before** publishing a reduced sidecar. Crash injection after the first commit (or before it) proves the old tombstone remains authoritative until safe retry; this is not a general two-file ACID transaction.
- `jobs._persist_locked` clears local pending IDs only on successful durable publication; otherwise even a safely compacted tombstone could be recreated by the deleting process's own stale `_DELETED_JOB_IDS` set.
- Controlled `jobs.compact_job_history_tombstones()` plus a single post-recovery startup sweep trigger safe cleanup without polling-time lease scans. Maintenance failure logs a warning and retains the journal view.
- Independent two-Python-process regression: a producer completes and retains its job in memory; another instance deletes it; compaction declines while producer is alive, accepts once producer exits, and subsequent persistence does not recreate the deleted record. Windows workflow also executes these tests.
- Exact PR-head [Python matrix / Termux surface / real libass #39465417901](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39465417901), [Windows writer and journal #39465417926](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39465417926), [seven ASS #39465417930](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39465417930) all **success**. Merged-main CI is separate and was in progress at the time of this intake.

**Pending:** v1 unknown-owner entries can grow indefinitely by design, long-lived producer sessions prevent pruning, physical Android/Termux and Windows customer device, deliberate power removal, long-running archival stress, and general cross-user/distributed ownership are unverified. Source-integrated Test with PR-head CI; do not promote Canonical.

### PR #200 correction — keep sidecar readable by older running HSR peers

After PR #199 merged, code review found its `schema_version: 2` deletion ledger was incompatible with an older still-running HSR #198 process, whose reader required version 1. The corrected [HSR PR #200](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/200) writes `schema_version: 1` with optional additive `owner_sessions`, accepts the temporary v2 records, and migrates them on startup while preserving all tombstones and owner mappings. Exact PR head `9b118afc5325537252535595de5d33d73c23e4b6` passed Python/Termux [#39466229547](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229547), native Windows [#39466229267](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229267), and seven ASS [#39466229292](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466229292), merged as `90a5d6ef77e3323e9d3a6f49d21c6cf0dcc5683c`.

The generic compatibility lesson is separately recorded in [cross-version sidecar Observation](../observations/2026-10-21-hsr-deletion-ledger-schema-cross-version-compatibility.md) after dedup. Actual heterogeneous-version side-by-side deployment remains FIELD-PENDING. Canonical unchanged.

### Final mainline state after PR #200

The compatible compaction implementation is now `HSR main@90a5d6ef77e3323e9d3a6f49d21c6cf0dcc5683c`. All four exact-main workflows succeeded: [Python/Termux/libass #39466462336](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462336), [Windows #39466462356](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462356), [seven ASS #39466462284](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466462284), and [Pages #39466461767](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39466461767).

**Disposition:** safe v1-compatible compaction integrated and mainline automated regression verified; unchanged FIELD-PENDING items include heterogeneous live versions, physical power loss, physical Android and long-duration archival stress. No Canonical promotion.

## 2026-10-21 — Real historical source checkout vs current HSR, PR #201

This is an incremental verification of the same job-journal Test, not a new Canonical rule. Following PR #200, schema compatibility was previously checked with source-derived expectations, **not** a second independently executed old codebase. [PR #201](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/201) now checks out the authentic pinned HSR main `f366f3fc6da47b8c06bb961945d4658da21d6a98` (PR #198 era) into a second directory, checks the historical Git SHA and launches old `app.jobs` and `app.job_journal` in a separate Python interpreter. The current HSR instance uses the same disposable jobs.json and OS-user session lock namespace.

- Integration verifies an *actual* old producer's completed job, deletion by current version, v1 sidecar with optional new owner metadata read by the old parser, protection against stale old-process writes, and safe compaction once the old producer exits.
- Reverse operation checks an actual old-version deleter: because its v1 tombstone has no durable original-producer identity, the current compactor **must leave it uncompactable**. This is correct for safety, but means disk usage is not provably bounded while arbitrary older deleters coexist.
- Two independently launched current-code Python subprocesses execute `os._exit(71/72)` exactly between tombstone/journal two-file publication boundaries. Tests prove the remaining sidecar and journal data support safe recovery and idempotent compaction. This is an **abrupt process exit**, not physical power cut or filesystem-cache loss.
- The exact PR head `7e0f4f4522477d03cd81dcd9a55f597132f73804` passed [legacy cross-version matrix run #39468760286](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468760286) on Ubuntu and Windows, [Python / Termux / libass #39468760113](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468760113), [Windows journal writer #39468760084](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468760084), and [seven ASS #39468760213](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468760213). PR #201 merged to HSR `main@987dfbe4d17aba8a1e81c01849e22b7ce5d90a49`. Exact merged-main CI was pending at intake.

**Evidence upgrade:** an independently executed historical source version is tested alongside the latest code on Linux and Windows CI. **Not yet covered:** a real installed old/new service deployment, every historical HSR revision, Android physical Termux, hardware power failure / storage durability, long-running media workloads, other users or uncooperative processes. Canonical unchanged.

### PR #201 exact-main acceptance (2026-10-21)

The merged source at HSR `main@987dfbe4d17aba8a1e81c01849e22b7ce5d90a49` passed the independently triggered:
- [actual pinned old/current HSR dual-runner Ubuntu + Windows matrix #39468979396](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468979396)
- [Python 3.11/3.12/3.13, Termux Lite surface, libass #39468979801](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468979801)
- [Windows writer/journal #39468979280](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468979280)
- [seven ASS #39468979425](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468979425)
- [Pages build/deploy #39468978519](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39468978519)

**Disposition:** exact-main automated cross-version and abruptly exiting process tests verified. Prior Pending for an *independently executed historical code revision under CI* is now closed. Deployed old+new servers, physical Android/Windows environments, physical power removal, and multi-hour workload remain FIELD-PENDING. No Canonical promotion.

## 2026-10-21 — Sustained shared journal progress, kill recovery, and Windows replace failure, PR #202

Deduplicated addition to this HSR job-journal Test. Product [PR #202](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/202), exact PR-head `451ea47824abfa3f5516e0bbf35fcf75cf8dc708`, merged `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`.

- Two independently launched Python producer processes each issue **180 actual persisted job progress updates** against the same journal. Two independent observer processes concurrently fetch status, assert no progress regression, preserve both task IDs and require eventual `succeeded`.
- A separate run forcibly kills one producer mid-update and checks its task becomes `interrupted` on live polling; the surviving producer finishes `succeeded`. A fresh Python interpreter reopens the journal and verifies both histories.
- Fault injection forces the `queued -> running` persistence to fail immediately after successful initial enqueue; a source fix avoids the previous ghost `running` job and prevents executing user callbacks without a recorded running state. Error remains terminal and future builds can be admitted.
- The first real Windows sustained workflow red, while Ubuntu was green: multiple in-flight jobs encountered `PermissionError WinError 5` from `os.replace(tmp, jobs.json)` despite a cooperating journal mutex. Source of the conflicting OS handle remains unproven. A distinct Bug is recorded at [Windows atomic journal replacement](../bugs/2026-10-21-hsr-windows-atomic-job-journal-replace-winerror5.md).
- The repair retries only WinError 5/32 at job journal / tombstone atomic-publication boundaries for <=3 seconds. Tests inject temporary, permanent and unrelated errors, covering eventual publication and fail-closed limits.
- Final PR exact-head runs all succeeded: [sustained Ubuntu/Windows #39472204422](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204422), [Python / Termux / libass #39472204781](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204781), [Windows writer #39472204234](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204234), [pinned old/current matrix #39472204693](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204693), [seven ASS #39472204166](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204166).
- Mainline post-merge CI pending when first recorded. This is a seconds-long repeated-persistence stress test, not an hours-long real FFmpeg/media pipeline soak. Physical Android/Termux, physical power cut, and deployed Windows machines remain FIELD-PENDING.

No Canonical promotion.

### PR #202 merged-main closure — all HSR workflows green

At exact HSR `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`, the independent push-triggered workflows all passed: [sustained progress Ubuntu+Windows #39472471082](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471082), [Python 3.11–3.13 / Termux Lite surface / libass #39472471101](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471101), [native Windows project writers #39472471080](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471080), [actual pinned PR #198 legacy interoperability #39472471149](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471149), [seven ASS #39472471218](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471218), and [Pages build/deploy #39472470120](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472470120).

**Acceptance disposition:** new bounded high-frequency journal stress and crash-owner recovery pass on CI-native Linux/Windows, integrated in main. Unmet field acceptance remains actual physical Android/Termux, installed Windows systems, real media multi-hour soak, and disk power removal. No Canonical promotion.
