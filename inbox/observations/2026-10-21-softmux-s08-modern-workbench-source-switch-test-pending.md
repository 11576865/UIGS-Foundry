# Observation / Pending CI: S08 current-workbench hazardous-source refusal and source-rebind recovery

Date: 2026-10-21
Status: **Pending CI / test implementation committed; no observed pass result**
Product: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/166
Exact submitted product head: `379d22cc9984907e35405a7600f41bd9ca0064cd`
Scope: Softmux 1.0 Plan B, WU-03 / F-B / S08, current production object workbench (`?ui` unset).

## Intake deduplication

Related existing Foundry knowledge:
- `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md` — known source structural preservation gate.
- `inbox/bugs/2026-10-13-mkv-unknown-header-skips-preservation-preflight.md` — final executor source/header authorization and adversarial first-read failure.
- `inbox/candidates/2026-10-02-batch-execution-async-preflight-readiness-race.md` — disabled controls do not serialize asynchronous readiness.

**No new Canonical rule or duplicate safety Candidate is proposed.** This observation is narrowly about acceptance coverage added for the actual modern user-facing composition entry, which the existing legacy `scenarioP0PreservationBlocksSingle` alone did not cover.

## Submitted acceptance path (not yet executed at this head)

1. Import two genuinely different media `File` objects plus external ASS via `#unifiedAssetInput`. Resolve the deliberate multiple-main-source ambiguity with the visible inventory source radio.
2. Select the independently MKVToolNix-authored nested `ChapterUID` / ChapterUID-targeted `Tag` fixture. Assert blocked structural readiness, disabled mux, explanatory risk reason and no generated artifact/report links.
3. Tamper only with the test DOM disabled state and dispatch an actual mux click. Assert the **execution-time** authorization refuses the source, still with no final artifacts; source SHA-256 unchanged.
4. Without resetting the entire app, reselect a separate safe MKV via visible inventory radio. Assert old source risk is not inherited, perform real FFmpeg/Wasm remux and download actual MKV.
5. Independently `ffprobe` the new result for real video/audio/subtitle streams and compare both original source SHA-256 hashes before/after. Save a machine-readable, source- and output-identified JSON receipt.

Code: `tests/e2e/browser-mux.e2e.mjs` (new `scenarioS08ModernUnsafeSourceSwitch`)
CI evidence: `.github/workflows/browser-e2e.yml`, artifact `s08-current-workbench-complex-mkv-safety`

## Evidence boundary / follow-up

- GitHub PR/commit proves **submitted test code and CI registration only**. **Pending CI** means no assertion of green test, verified product fix, saved user-local file, general EBML safety or physical-device acceptance.
- If CI fails, determine whether it is a real UI source-identity/rebinding bug, selector/test issue, asynchronous timing problem or media error; record the exact observed failure before proposing a correction.
- On exact-head CI completion, add the run ID, raw acceptance report and observed status. Do not promote this observation to Canonical on one tested fixture.

## First exact-head CI red / scoped test repair

- Product head `379d22cc9984907e35405a7600f41bd9ca0064cd`, Browser E2E workflow [39465515066](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39465515066): **failure**. Build/Pages workflow [39465515079](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39465515079): **success**.
- Failure occurs immediately at the first `locator.check()`, *before* risky-source classification assertions. Playwright resolved the right radio but it was hidden in the production 1280px tablet layout; after 30 s it timed out. This does **not** establish a product safety regression or an S08 preservation result.
- Root UI contract: `src/softmux-figma-tablet.css` hides `.sf14-source` between 681–1365px until `#sf14SourceToggle` sets `#sf14Single[data-show-source="true"]`. Production `sourceFilesDetails` is already open on initial mount, but the containing overlay is not visible.
- Follow-up product test-only commit `d17d923bfd7f2b785c9dfec22ddd2265761e5585` explicitly clicks the actual header 来源 control and verifies the overlay/underlying details and source radio are visible before `.check()`; no production code or permissive safety bypass was changed.
- **Current status: Pending CI for new head.** Need exact-head execution evidence before marking this test PASS. Do not infer that the downstream runtime-block, source recovery, actual output or native oracle assertions pass.
- Reusable distinction: test automation must first traverse documented progressive-disclosure/navigation before asserting an interaction, rather than force-clicking a hidden DOM control. This is a scoped observation and duplicates no existing Canonical requirement.
