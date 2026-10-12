# Bug: Resolving a source ambiguity collapses the focused file chooser during redraw

Date: 2026-10-12
Status: **Bug / Chromium-reproduced / source repair submitted / re-verification Pending**
Lifecycle: validation-pending
Project: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/74
Failing workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38163292219
Failure case: `scenarioContentFirstSourceAmbiguity` in `tests/e2e/browser-mux.e2e.mjs`

## Reproduction and evidence

Import two valid container candidates, e.g. an MP4 and a Matroska source. The program correctly expands the secondary `#sourceFilesDetails` disclosure, because choosing a primary source is necessary. Focus the radio for the desired MKV and activate via keyboard Space.

In the E2E run at head `804d95fe9f2dda047f548f5563e7494f41a4a0df`, all **216/216 Node tests passed**. Chromium then failed before mux in the source-ambiguity scenario:

- expected `document.activeElement.dataset.assetSource` to equal the selected MKV source key;
- actual active element attribute was `null`.
- The user interaction itself resolves the ambiguity and re-renders the inventory. Source details had `open = roles.needsSourceChoice || roles.unknown.length`, so it collapsed immediately when the source became unambiguous, hiding the still-focused radio. The inventory's DOM was also replaced.

This is a **real keyboard continuity regression**, not a test-oracle wording problem or evidence of failed FFmpeg mux execution.

## Submitted bounded repair

In the same `renderImportedAssetInventory` call:

1. Capture whether the currently focused element is a source radio contained in the disclosure.
2. While it owns focus, preserve its open state instead of automatically collapsing the disclosure mid-interaction.
3. After replacing the list DOM, find the radio with the same source key and restore focus with `preventScroll` only when it remains enabled and visible.
4. Retain user-initiated native details open/close behavior. Do not duplicate the asset selector, change source role policy, or rewrite the existing execution engine.

Repair commit: `1d0363624ab1b5386eff66e6cf419b89a3cf42d1`.

## Generalizable lesson / evidence boundary

**Automatic progressive disclosure must not revoke keyboard focus as a side effect of a successful choice.** When conditionally expanded panels contain currently focused controls, evaluate whether the state transition can safely close the panel; rerendered keyed controls require identity-based focus restoration. This is separate from whether a UI copy reduction succeeds visually.

The fix is source-submitted; a new exact-head Chromium E2E run must pass, including source choice, source-only mux and populated screenshots, before this case is marked resolved. No Canonical specification change is justified from one product observation.
