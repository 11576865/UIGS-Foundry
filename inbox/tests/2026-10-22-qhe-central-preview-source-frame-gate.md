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
