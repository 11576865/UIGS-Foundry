# HSR: cancellable ASS evidence job history grows without in-memory bound
Lifecycle: validation-pending

- **Type:** Bug
- **Status:** Mitigation committed in Draft PR; exact-head CI initially pending
- **Repository:** [11576865/HSR-Voice-Archive-Builder](https://github.com/11576865/HSR-Voice-Archive-Builder)
- **Affected code:** `app/jobs.py`, `app/ass_coverage_batches.py`
- **Fix HEAD:** `017b7f640f489e7ec041603e23dd0ebab8f6d593`, [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134)
- **Authority:** observed in current repository source; controlled unit tests, not real device field evidence

## Observed defect

The existing persistent job journal wrote only the last `MAX_PERSISTED_JOBS=100` entries. The live `_JOBS` dictionary, however, kept *every* completed task indefinitely. The new exported-ASS window-pass UI can legitimately start thousands of successive user-approved background evidence jobs for a long archive. This accumulates in-process Job records and makes project-scoped duplicate task scans increasingly expensive. Moreover, when more than 100 jobs are active concurrently, the previous journal's last-100 slice can silently omit older queued/running jobs; process recovery would not be able to mark these omitted jobs interrupted.

## Fix and boundaries

- Prune oldest normal completed entries when writing the journal; retain queued/running unconditionally, and prioritize interrupted/awaiting-input over ordinary history.
- Persist all live jobs even when their number temporarily exceeds the normal history limit, and reload older queued/running records on restart.
- A bounded history entry is not itself evidence: actual exported ASS batch receipts remain separate and durable.
- New `tests/test_jobs_history_pruning.py` covers pruning behavior, 109 sequential completed jobs, preservation of 103 concurrent running records, and recovery of an older in-flight job despite more recent completed history.
- The separate late-cancel-after-commit job status issue is documented in the preexisting HSR Case.

## Verification

Exact-head [Python 3.11/3.12/3.13 + Termux CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245248441) and [Chromium/real FFmpeg-libass CI](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245248555). At initial intake, one run was successful and the second was still running. Final outcome must be updated after completion.

Limits: No measured memory residency of thousands of actual FFmpeg jobs in a real game archive, nor Android physical-device validation. This source-level fix is not automatic evidence to change UIGS Canonical.


## Final exact-head verification (2026-10-12)

The regression fix is on HSR PR #134 exact SHA `7e3577d5f4ef170ff01b6f1b680e6f324383a1be`. [Python 3.11/3.12/3.13 + Termux Lite run 38245706504](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245706504) **success** and [Chromium + actual FFmpeg/libass run 38245706585](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38245706585) **success**. The libass runner explicitly exercised four job-history and crash-recovery cases, all `ok`. Mark code-level issue **FIXED IN DRAFT**, not merged or physically device-accepted. Real thousands-of-FFmpeg-jobs residency unmeasured; Canonical unchanged.
