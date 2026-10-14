# Bug · External metadata recovery updated the domain, but its editor still showed stale values

Date: 2026-10-15
Status: **Bug / source-reviewed corrective code submitted; fresh exact-head Chromium pending**. Not Canonical.
Product: [MKV-Fast-Muxer PR #145](https://github.com/11576865/MKV-Fast-Muxer/pull/145)
Fixed parent head: `245f395f52e0938ccc3559bbc358683101737e6c`
Complete R1–R4 regression gate: [PR #146](https://github.com/11576865/MKV-Fast-Muxer/pull/146)

## Observed reproducible failure — actual CI, not hypothesis

GitHub Actions Browser E2E on R1–R4 integration `17a81ee8bc2d057dc633b297a172e986da0f68db`, workflow 38607058882, failed the real `scenarioExternalCheckpointRecoveryRealMux` assertion at line 1427. After the user imported an external metadata checkpoint, completed SHA-256 rebind and expressly applied the prepared external metadata transaction, the actual audio input still displayed `R3 Current Before Restore` instead of the expected `R3 Restored FLAC`.

Review of `src/main.js` found the apply/undo handlers calling `updateUI(); renderMuxPlan();` directly after updating the authoritative `ContainerProject` and legacy external rows. `updateUI()` FIRST calls `captureNewTrackEditorState()`, which can read stale text controls. The checkpoint had correctly changed the domain, but the DOM remained a stale writable projection of the previous value.

## Narrow fix submitted

At both apply and undo success call `renderNewTrackLists()` before `updateUI()`. The renderer compares actual immutable/executor rows with visible fields and reconstructs stale controls from authorized domain data. Only afterward should `updateUI` snapshot visible controls. No SHA, File identity, explicit consent, atomic domain commit or source safety check is weakened. Existing E2E still requires after-apply form value, after-undo old form value, second prepare/commit, and native final MKV audio title.

**The correction is not marked verified until an exact-head complete Chromium workflow passes.** Parent PR #145 head `245f395f52e0938ccc3559bbc358683101737e6c` and stacked R5 PR #147 include the fix.

## Reusable lesson and dedup

For recovery/undo flows with mutable DOM forms and an immutable domain source-of-truth: **after a domain commit, update the controlled form projection before any generic render path captures existing input values**. Otherwise stale DOM can reinject old data or conceal committed changes. Maintain a browser-level assertion covering visible input and independent output, not only internal domain unit tests.

Searched `restore domain stale form re-render`, `external recovery UI projection stale`, `renderNewTrackLists restore`, `output array order identity`. Related prior Cases describe external domain File binding and stale form epoch, but not this **explicit recovery-commit → renderer capture ordering** failure. No Canonical promotion.
