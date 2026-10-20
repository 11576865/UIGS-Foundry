# Bug — Windows atomic jobs.json replacement can fail despite cooperative journal lock

Date: 2026-10-21
Project: `11576865/HSR-Voice-Archive-Builder`
Fix: [PR #202](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/202)
Merged main: `2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`
Evidence: CI-observed failure + committed correction + passing exact PR-head tests
Layer: **Bug; not Canonical**

## Observed failure

During a new sustained test, two independent Python worker interpreters repeatedly persisted `archive-verify` job progress while two other interpreters polled `get_job` and checked monotonicity. All cooperating HSR writes/reads used the existing shared OS journal mutex. Native Windows runner nevertheless produced a concrete failure:

```
PermissionError: [WinError 5] Access is denied:
  '...\.jobs.json.<random>.tmp' -> '...\jobs.json'
at app/project.py atomic_write_json -> os.replace(temp, path)
via app/job_journal.py persist_rows -> app/jobs.py report_progress
```

This failed a legitimate in-flight job and recorded it as `failed`. Both the first [Windows sustained run #39471600002](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39471600002) and the instrumented rerun [#39471860940](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39471860940) failed, while the same tests passed on Ubuntu. Logs show the exact `os.replace` denied rename; which external file handle held the target was **not identified**. Antivirus or indexing activity is a possible explanation, not proven causation.

## Correction

- `app/job_journal.py` now funnels only jobs journal / deletion-ledger atomic writes through `_atomic_journal_write`.
- Bounded retry (3 seconds, short sleeps) is restricted to WinError 5 or WinError 32; unrelated I/O errors immediately propagate and a persistent Windows denial still fails closed.
- Keep the writer mutex read/merge/write transaction intact, keep `app/project.py` generic atomic writes unchanged, and do not change fail-fast FLAC/ASS/MKV output writer exclusion.
- Test injects 3 denied replacements before success; separate tests ensure permanent denial is bounded and errors without these Win32 codes are not retried. Sustained real subprocess test then passed on Ubuntu and Windows in [PR #202 final #39472204422](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204422).

## Related job-start failure

The same source audit found a second error boundary: `jobs.runner` moved from `queued` to `running` and persisted the transition **before** entering its `try/except`. If initial running-state publication failed, the daemon thread crashed, leaving a phantom in-memory `running` job and potentially blocking future builds. PR #202 now records terminal failure before executing the task body and attempts durable failure publication, with a regression that injects this exact failure and permits a subsequent build. If the filesystem remains unavailable, even the failure status cannot be guaranteed durable; physical storage recovery is out of scope.

## Verification and limits

The exact PR head `451ea47824abfa3f5516e0bbf35fcf75cf8dc708` passed Python 3.11/3.12/3.13 and Termux Lite surface [#39472204781](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204781), Windows writer safety [#39472204234](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204234), pinned legacy matrix [#39472204693](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204693), sustained Ubuntu/Windows stress [#39472204422](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204422) and seven ASS [#39472204166](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472204166).

Pending: exact merged-main workflow verification at initial intake, a real Windows end-user machine, Android/Termux hardware, long-duration full media encoding, and physical power interruption. Sustained CI tests involve hundreds of repeated job-journal writes over seconds, **not** a multi-hour production benchmark.

Dedup: journal shared-resource synchronization is already documented in `inbox/candidates/2026-10-02-shared-file-journal-resource-scope-locking.md` and the HSR cross-process Test. This Bug records the distinct **OS-target-replacement denial** and **unhandled job-start journal failure**; do not modify Canonical from one observed CI issue.

## Exact merged-main confirmation

The corrected HSR `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c` passed all six application workflows, including [Ubuntu/Windows sustained journal #39472471082](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471082), [Windows writer safety #39472471080](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471080), and [Python/Termux/libass #39472471101](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39472471101). The earlier Pending exact-main automated validation item is closed. Physical Windows/Android and extended-hours production workload still FIELD-PENDING. Canonical unchanged.
