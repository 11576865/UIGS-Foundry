# Test: QHE Native encode progress survives webpage refresh

Status: **Pending CI / FIELD-PENDING real long-film refresh**  
Date: 2026-10-11  
Project: `11576865/Quick-Automatic-Hardsub-Encoder`  
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/91  
Revised head: `402a095ebded23261e617931e8910cb293ea4892`

## Observed defect

The browser's `recoverNativeJob()` already queried the authoritative Native Bridge status but discarded that status snapshot on the running-job branch, then launched an additional monitor GET before rendering current progress. After refreshing a long running encode, the progress bar could start from empty/initial rather than immediately show the running backend percentage. A stale or missing subsequent sample could also roll back the rendered progress; preflight status text could overwrite progress guidance.

This is a source-code-confirmed UI state-rehydration defect, **not evidence that FFmpeg itself restarted**.

## Correction submitted

- Pass the fetched recovery status directly to `monitorNativeJob(jobId, initialStatus)` as its first render state.
- Keep displayed progress monotonically nondecreasing for a single active task; allow terminal failure/cancel to reset. Don't claim 100% before `completed`.
- Suppress preflight guidance from overwriting active/completed Native job text.
- Retain bounded bridge polling-error behavior and persistent job ID ownership.

## Regression evidence

`src/native-job-monitor.test.mjs` exercises (1) running second pass at 61.8% refreshed with only one first Bridge GET; (2) subsequent stale 0%/missing validating progress followed by terminal cancellation; (3) preflight guidance suppression; (4) preexisting bounded bridge-error retry.

First CI on commit `6e0d86109075bda7b35369adf719cbe3e09ea7fe` **failed in the VM test fixture**, which still matched the old monitor function signature and omitted `localPredictionForPlan` in the mock. No evidence was obtained of an encoder regression. A dedicated test fixture correction was committed as `402a095ebded23261e617931e8910cb293ea4892`. The revised CI outcome is **Pending**.

## Acceptance still required

- Frontend CI passes with revision, plus the existing frontend build and Playwright UI smoke.
- Real Windows long-film test: start two-pass encode, refresh browser while running, verify same job ID, pass number and consistent progress/ETA; verify cancel and completed/export states.
- Android Native behavior remains distinct; no claim of its persistence without Android-backed evidence.

Links to existing Candidates: `inbox/candidates/2026-10-03-cross-boundary-invariant-coverage.md`, `inbox/candidates/2026-10-04-private-staged-mutation-publish-only-final-verified-output.md`. This is a Test/Pending intake only, not Canonical.


## 2026-10-11 verification checkpoint after conflict reconciliation

Frontend, Windows smoke, and UIGS Evidence Coverage all passed on the pre-integration #91 head `402a095ebded23261e617931e8910cb293ea4892`. Subsequently, #90 merged into QHE main as `c1c7872016dbee4d0c199522a5ab7bfcf77d4665`. Since both changed `src/main.js`, #91 was semantically reconciled with a two-parent commit `7d3121958c1f693ce3c43227743bcf6b6b6be60f`, preserving both the strict-output verification wording and the refresh progress-state tests. **The reconciled head has its own CI pending**; earlier #91 green results do not certify the new combined tree.

Real long-film refresh and GPU evidence remains FIELD-PENDING. No Canonical promotion.
