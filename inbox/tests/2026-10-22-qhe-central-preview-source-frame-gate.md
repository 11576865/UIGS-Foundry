# Test: QHE central preview rejects a previous File's source frame

Date: 2026-10-22
Status: Test / code committed / automated execution PENDING
Product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/124
Source branch: feat/workbench-real-frame-preview-20261022

## Dedup and scope

Foundry searched `preview source identity`, `stale frame`, `source object identity preview` and `asynchronous UI artifact stale`. Relevant existing Candidates:
- `inbox/candidates/2026-10-03-interactive-preview-backpressure-stale-results.md` — backend request-generation/source identity and stale-completion rejection;
- `inbox/candidates/2026-10-03-latest-request-identity-for-async-probes.md` — Native probe and preview waiter cancellation;
- `inbox/candidates/2026-10-03-post-operation-visual-verification-must-map-by-timeline-time.md` — visual evidence tied to timestamp.

The present item is a **narrow product Test**, not a duplicate Candidate or newly approved general Canonical policy. The difference is presentation-layer stale image reuse in a central composed view even when the original decoder owner is elsewhere in the DOM.

## Proposed counterexample and implementation

The Figma v3 central source-frame preview used an existing `img.src` projection from a collapsed timeline owner. Changing a File source can leave an earlier decoded image URL momentarily in the old element. Displaying that URL in the *new* source context would mislabel previous-media visual data as current.

Product PR #124 adds explicit matching by **File object reference**, not equal name/size/mtime. On source change, the old source frame URL (and the hard-sub preview image separately) becomes ineligible for the composed view. A newly populated frame URL may be shown. A user command in transcode/Stream Copy routes to existing `#taskWaveformLoad`, which starts the established decode path rather than creating a second decoder. No-source and decode-error text is explicit.

## Submitted tests and evidence limit

- Unit assertions: old URL rejected, new URL accepted, absent/hidden URL rejected.
- Browser regression assertions: no-source central generation does not silently succeed; replacing a source with a distinct `File` sharing the same metadata does not leave its previous frame visible.
- GitHub connector created product commits and Draft PR #124. **No Node, Playwright, FFmpeg, GPU or physical-device suite executed in this session.** Branch code committed does not imply Test PASS, defect conclusively reproduced, backend verified, or user acceptance.
- Test state remains **Pending External Validation** until the exact-head CI/real-browser observation is attached. The source/decode ownership and independently verified product output semantics remain distinct.

No Canonical promotion.

## 2026-10-22 follow-up: full browser coverage, not yet execution proof

The first PR #124 check reported whole-workflow success while GitHub jobs revealed `draft-fast: success`, `frontend: skipped` due to its Draft state. The project has now submitted additional `scripts/check-source-import-entry.cjs` browser assertions for the existing real `main.js` + Windows Native client, mocked `/api/frame` response, empty-audio timeline path, decode error disclosure and successful retry; both Transcode and Stream Copy must route through the same original frame owner. This stronger assertion is **committed but remains unexecuted** until a non-Draft/full frontend workflow runs. It does not upgrade the existing general Candidate or prove physical FFmpeg decoding, device performance or arbitrary-video compatibility.

## 2026-10-23 observed CI counterexample and bounded test-synchronization repair

QHE PR #124 full Frontend run [39754507684](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39754507684) failed at `check-source-import-entry.cjs:81` with the Copy step expecting a fourth frame request but observing only three at assertion time. A previously successful Transcode frame leaves a populated `data-v3-frame.src`, so waiting on that predicate does **not establish that a new Copy request completed**. This is a precise browser-test synchronization counterexample, not yet independently proven missing product frame generation.

In the one permitted bounded repair generation, the test now registers a Playwright `waitForResponse` for the next `POST /api/frame` **before** the Copy click and awaits it before retaining the exact four-request assertion. No sleeps, relaxed assertion or product decode change. The repaired generation remains **Pending External Validation** until a new exact-head full frontend result; do not upgrade Test to PASS or alter existing Candidates/Canonical.

## 2026-10-23: asynchronous projection completion is a distinct oracle

The next full frontend run [39877054900](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/39877054900) again failed, but later in the same test: a new Copy `POST /api/frame` response was observed and the exact transport-request assertion passed, yet the immediate composed `img.src` read returned `null` (line 88). This does not prove absent decoding: HTTP response, Native callback, decoder-owner DOM update, and central workbench `requestAnimationFrame` composition are separate asynchronous completion boundaries.

QHE repair commit `75c78e5c0ecdf27f1af5c9092717dc4dc0044daf` keeps the transport assertion but also awaits the original image owner and the central composed image to become ready with the same URL. This is a source-specific Test extension of the already-identified asynchronous-preview Candidate; **the next exact-head CI remains pending**. No claim of real FFmpeg success or Canonical promotion.
