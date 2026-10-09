# Candidate: Explicit ownership and replacement boundary for browser artifact Object URLs

Status: **Candidate** (not Canonical)  
Date: 2026-10-09  
Domains: browser Blob URL lifecycle, multi-step workbenches, batch artifact retention, long-running client memory

## Observation / source evidence

Project: `11576865/MKV-Fast-Muxer`  
Baseline: `main@76056cb8e3f04f81a71e4781004587f2ee0dc986` (PR #64 merged with green main Pages deployment and Chromium Browser E2E).  
Follow-up branch: `fix/batch-download-url-lifecycle`  
Proposed PR: https://github.com/11576865/MKV-Fast-Muxer/pull/65  
PR head at intake: `319f338bc5d7784622c12c46db7b6f9a34174989`.

In `src/main.js`, completed batch tasks constructed dedicated `URL.createObjectURL(result.blob)` and `URL.createObjectURL(result.reportBlob)` download links, persisted in the visible batch result rows so earlier outputs remained downloadable as later jobs ran. Starting another batch cleared `batchResults.innerHTML` but did **not** invoke `URL.revokeObjectURL` on those batch-owned URLs. Single-task output/preview URLs had their own explicit revoke logic. This is a **source-reviewed possible browser memory retention issue**, not a measured production heap leak or user-reported incident.

## Candidate insight

A browser-created `blob:` URL is a resource handle, not merely presentation text. A batch workbench should assign each result set explicit URL ownership and establish a clear release boundary matching the visible download lifecycle:
- **Do not revoke at individual-job completion** while links to prior jobs remain visible and useful.
- **Do not revoke on a failed attempt to begin a replacement batch** if prior results remain visible.
- **Do revoke URLs belonging to the old result set when a replacement batch actually starts**, before removing the old result rows; retain the new batch's URLs independently.
- Keep single-task, preview and batch-owned handles in separate lifecycles; never bulk-revoke handles from unrelated owner scopes.
- Document that users should save current outputs before replacing the result set.

The proposed change adds `src/batch-result-urls.js` as a batch-only URL registry and calls `releaseAll()` only on the accepted batch-start path; `src/main.js` registers MKV and optional report URLs through that registry. README explains download validity.

## Tests, uncertainty and next evidence

Four source-derived V8 helper regression checks passed (download retention, idempotent release, next-run isolation, absent report). Touched JS parsed. New Chromium Browser E2E uses two consecutive actual mux runs and instruments `URL.revokeObjectURL` to assert that old MKV/report URLs survive until next batch start and new results remain active. **Full repository Node suite, browser E2E and PR review remain Pending CI** at intake; no empirical reduction in peak memory use is asserted.

This addresses lifetime retention across successive batches, **not** the inherent high memory requirements for currently visible large downloads. Current results must remain alive while downloadable. Do not infer that all browser large-file constraints have been solved.

## Deduplication

Searched UIGS-Foundry for Object URL / Blob cleanup and artifact lifetime; no matching URL-lifecycle Candidate was identified. Related record `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md` covers filename identity, filesystem persistence, and ownership of output paths, **not** URL handle lifetime. Keep evidence separate to avoid conflating filesystem entry ownership with in-memory resource ownership. This is a Candidate, with no Canonical modification requested.


## PR #65 integration evidence

Date: 2026-10-09  
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/65  
Validated PR head: `319f338bc5d7784622c12c46db7b6f9a34174989`  
Merged commit: `d5669c6d9bb6ebdd6843ee8c7f651902c80c4d08`  
Integration state: **Merged to main**; epistemic state remains **Candidate**.

The PR-level **Browser E2E mux tests** (`chromium-mux`) and **Deploy to GitHub Pages** (`build`) check suites both completed successfully. The browser job ran the repository Node unit suite, generated real fixture media, built the app, and executed browser end-to-end mux tests. PR review was completed and there were no inline findings or active review threads at merge time. GitHub reported `mergeable_state=clean` and accepted the merge with an expected-head-SHA guard. Confirmed `main` at `d5669c6`.

At this integration checkpoint the new **main-push** Pages deployment and Browser E2E are still asynchronous (`in_progress`), and their ultimate results must not be inferred from PR-level checks. This record documents a code-path lifetime correction and passing CI, **not** a measured heap reduction or a browser-wide memory guarantee. A Blob URL associated with a still-visible large artifact is intentionally retained. No Canonical update requested.
