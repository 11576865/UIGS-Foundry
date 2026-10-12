# Bug: optional MIME warning erased attachment rows after non-returning DOM helper

Date: 2026-10-12
Status: Bug / failure reproduced in real Chromium; **fix submitted, exact-head re-verification pending**
Product: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/92
Failing exact head: `4c74d74253c1ae3812ecb4463bd30f6ff682c13d`
Failing CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38246524759

## Failure observation

During the new real-browser PNG-only Matroska acceptance scenario, an attachment named `pixel.png` with actual PNG bytes was deliberately declared as `application/pdf`. The browser successfully displayed a `warning` status after requesting prefix inspection, **but the attachment row had disappeared**. Playwright timed out at `locator('.attachment-extraction-row').first().textContent()` in `scenarioP2R02NoTrackAndMimeEvidence` (line 2909). Node **281/281** and Vite Build were green, but full Chromium E2E failed. Independent R-02 research step did not run because it was after the failing browser job.

Root cause in `src/attachment-extraction-ui.js`: DOM factory `field(parent, label, value)` appended its constructed row but returned `undefined`. The newly added mismatched MIME warning path called `const warning = field(...); warning.classList.add(...)`, throwing after `render()` had already called `list.replaceChildren()` and before any new rows were appended. A broad catch converted the exception to the same `warning` state, making a check of status alone insufficient to prove the warning UI rendered.

## Repair and regression boundary

Product fix commit `76ec55ea79fdcd2916c89ac65e650fab47bef229` returns the newly constructed row element from `field(...)`. The failing Playwright scenario remains intact and asserts the content-warning row is present with both declared `application/pdf` and observed `image/png`, after inspecting actual PNG FileData. **Exact-head full E2E at that commit was pending at Bug intake.** Do not claim resolved until that passes.

Reusable bounded learning (candidate, not Canonical): when re-rendering lists by clearing children before constructing replacement rows, exercise *uncommon warning/error data branches* in a real UI test. An outer catch can mask a rendering exception as a business-domain warning; assert the actual row and warning text, not only the status indicator.

No EBML writer issue, file-byte corruption or MIME sniffing parser defect was identified in this failure. The broader untrusted attachment security Case remains distinct.

## Exact-head verified resolution — 2026-10-12

Fix head `76ec55ea79fdcd2916c89ac65e650fab47bef229` passed **281/281 Node**, Vite Build and all real Chromium Browser E2E scenarios in [workflow 38247044454](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38247044454). The previously failing scenario now logs `P2 R-02 no-track browser extract + MIME mismatch warning PASS` and the combined suite logs `All browser E2E scenarios PASS`. Research steps independently logged `INDEPENDENT_READER_AND_BYTES_MATCH` and `MODEL_AND_INDEPENDENT_ATTACHMENT_BYTES_MATCH` after the shared deterministic fixture refactor.

Product PR [#92](https://github.com/11576865/MKV-Fast-Muxer/pull/92) squash merged as `main@f8ccc15c5d304d2d63034fe1f4f2f53360274c9d`. This **specific DOM-helper return-value bug is verified resolved** in the scoped regression. No claim that all future warning render branches or malformed Matroska cases are safe; no Canonical promotion.
