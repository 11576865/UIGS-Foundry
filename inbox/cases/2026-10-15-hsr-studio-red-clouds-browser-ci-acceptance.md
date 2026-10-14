# Case: HSR Layout/Effects red-clouds preview CI cleared through three browser acceptance failures

Date: 2026-10-15
Project: `11576865/HSR-Voice-Archive-Builder`
PR: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/166
Accepted head: `815ac9d703fdd28c4884d73df840bd68da757449`
Case status: **exact-head CI green; real physical Android/Termux field validation pending**
Level: Case (specific failure-and-repair chain), not Canonical

## User report and evidence

User reported that PR #166 had turned red after the user-supplied red-clouds picture was committed and the responsive Layout/Effects workbench was revised. Inspection found Python and real FFmpeg/libass tests green, but Chromium visual/integration workflows progressively exposed three different issues. Subsequent reruns were used to separate the failures, not to weaken acceptance.

### Red stage 1: asset did not decode in Chromium fixture

[Browser workflow 38632650029](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38632650029) failed in `tests/browser_visual_evidence.py`, waiting for `previewBackgroundImage.complete && naturalWidth===640 && naturalHeight===360`. The packaged user-provided image was a genuine 640×360 WebP (5,858 bytes; Git blob SHA `2c6332e1d1f7661cb8181708a358e8e7e2aac885`), and production FastAPI/Termux static handlers both served `/static`. **The test-only HTTP server had special-cased a CSS file, without routing `/static/assets/...` to `app/static/assets/...`**. This produced a 404 and an opaque image-decode timeout.

Repair `2786ec5a64eabae6cac4a90a6a877e7796dcc856`: fixture serves all static assets safely from the same root as production, with MIME, bounded directory resolution and an explicit HTTP/content-type/image-dimension diagnostic on failure. This preserves a browser pixel/decode assertion rather than deleting it.

### Red stage 2: stage overlay intercepted timeline pointer input

[Browser workflow 38634139721](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38634139721) passed reference-image decoding, then failed a **real mouse pointerdown** drag-handle test: `layoutTimelineDrag` remained null. The new high-layer sticky preview stage overlapped the timeline area after scrolling the internal canvas pane, blocking hit targeting. This was a genuine layout/interaction regression, not only stale test semantics.

Repair `cc8ca7019e8ed71b3adbba1fb10d728f218af165`: scene remains positioned relative to the independently scrolling preview pane; the Inspector continues to scroll separately. Update the source contract test (`e1f40a248e15c589a260bd32166d579c58aafc0e`) so a sticky overlay is not asserted as a feature. Chromium's real drag test is preserved.

### Red stage 3: E2E did not open newly collapsed optional media controls

[Browser workflow 38634399731](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38634399731) passed responsive drag and media backend tests, but `tests/browser_live_preview_e2e.py` timed out filling `#effectFootageStart` because the new optional media controls intentionally lived in a collapsed `<details>` disclosure. The production UI correctly hides these lower-frequency inputs until user action.

Repair `815ac9d703fdd28c4884d73df840bd68da757449`: the real Chromium–FastAPI–FFmpeg test now clicks the media disclosure, asserts the offset is visible, then uploads footage and continues to assert real video/audio decode. The product disclosure stays intact.

## Exact-head accepted CI

- [HSR subtitle browser evidence 38634750995](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38634750995): **success**, including Chromium visual/interactions, real browser–FastAPI preview and actual FFmpeg/libass artifact checks.
- [tests 38634751018](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38634751018): **success**, including Python 3.11/3.12/3.13 and Termux Lite surface checks.
- Android physical device, real user's foreground/background browser reload, and subjective Layout/Effects usability acceptance are **not established** by these CI runs. PR #166 was still open when this record was authored.

## Reusable case boundaries

1. A browser UI fixture must faithfully serve **the actual production static asset URL namespace**; a single stylesheet special case can hide missing asset paths until a new image is required. Failure diagnostics should distinguish 404/incorrect MIME from decoder failure.
2. Responsive design must be accepted by real hit-testing and dragging, not only screenshots and element rectangles. Sticky high-z preview surfaces can occlude timeline controls when `scrollIntoView` brings them into the same pane.
3. After replacing permanently visible controls with progressive disclosure, E2E automation should follow the real user affordance (open the disclosure), **not** force a hidden input or reverse the desired UI design simply to satisfy old tests.
4. Exact-head green CI is a concrete verification layer; it is still not physical-device acceptance.

## UIGS Intake

Foundry searched for `fixture static assets`, `browser visual evidence static resource 404`, `test server /static production mount`, `visual test image route`, and reviewed the related HSR Observation `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md`. This is a distinct concrete CI-failure Case with three confirmed causal chains and their verified fixes, not a new Canonical pattern. No automatic Canonical update.
