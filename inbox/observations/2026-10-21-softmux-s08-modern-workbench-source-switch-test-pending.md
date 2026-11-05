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

## Corrected head verified S08, full-suite still red (2026-10-21)

- Product head `d17d923bfd7f2b785c9dfec22ddd2265761e5585`, exact-head browser [CI #39468296942](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39468296942): **S08 browser scenario PASS**, includes forced-click refusal, safe-source recovery, real MKV and native `ffprobe` assertions; JSON plus real MKV artifact `s08-current-workbench-complex-mkv-safety` ID `12286455794`. Node/S10/build steps were successful, but **overall Chromium job failed** at subsequent existing R2 source-title assertion (`Japanese AAC` rather than `R2 Original Source`).
- Dedup: pre-existing `inbox/bugs/2026-10-20-softmux-r2-source-title-plan-intermittent-integration.md` records two previous exact-head source-title failures and a successful changed-order run, without established root cause. The new red outcome is **further evidence for the existing Pending Bug**, not a new Candidate or proof S08 caused it.
- Re-run of the same failed workflow job requested to distinguish stability. Until entire exact-head required suite passes, PR #166 stays Draft / not merge eligible.

## S08 product integration result

- PR [#166](https://github.com/11576865/MKV-Fast-Muxer/pull/166) was merged (squash) to `main@fdf87a9710247db35adb041640facad5fa5d6380`.
- Source head `d17d923bfd7f2b785c9dfec22ddd2265761e5585`; GitHub Actions [#39468296942](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39468296942) **completed success on second attempt**. On first attempt this same SHA failed a previously known R2 source-title regression **after S08 itself passed**, so S08's targeted acceptance is verified within the reported fixture and run, but no broad nonflaky assurance is asserted.
- This Observation remains an evidence record, not a new canonical safety rule. The separate intermittent R2 problem is tracked in `inbox/bugs/2026-10-20-softmux-r2-source-title-plan-intermittent-integration.md`.


## 2026-11-05 follow-up: independent native source proof in 1.0 convergence

**Deduplication:** This is the existing S08 acceptance Observation, not a new general Matroska preservation rule. Existing [PR #166](https://github.com/11576865/MKV-Fast-Muxer/pull/166) + [successful workflow attempt #39468296942](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39468296942) already established the bounded UI fail-closed and safe-source actual MKV output scenario; do **not** relabel that past S08 pass as a new untested defect or pretend it is 1.0 exact-candidate acceptance.

**Current product work:** [Draft PR #241](https://github.com/11576865/MKV-Fast-Muxer/pull/241), exact commit `73b2d0f6979b2cd313c3657265ce3ad1ecded062`, carries two code/CI changes `4ca102f871a9d1448592dac8811e93befbbd2faf` and `73b2d0f6979b2cd313c3657265ce3ad1ecded062`:
- Upgrade the **existing live Chromium S08 user task** to run native `mkvextract` over the actual dangerous source immediately before selecting it. Require original chapter XML contains parent `ChapterUID=510010` and nested `510011`, and original tags XML references the same nested `510011` with `P0_NESTED_CHAPTER_KEEP`. Preserve independent extracted XML with SHA-256 in test receipt.
- After actual forced-runtime refusal, selected safe source is remuxed/downloaded in Chromium. Compare `ffprobe` video/audio **codec identity** between safe source and finished MKV, in addition to existing stream-count and unchanged source hashes. This verifies a narrower post-rejection stream-copy invariant, not full packet/PTS preservation.
- Upload original `s08-risk-source-chapters.xml` and `s08-risk-source-tags.xml` next to the S08 receipt and finished MKV through the already-existing `s08-current-workbench-complex-mkv-safety` artifact.

**Execution boundary:** GitHub PR commits and registered CI workflow changes are verified. At last query the new head **had no listed completed/active PR-triggered workflow runs**, so the new native-proof enhancement is **Pending CI**, not PASS. Historical S08 first-hand pass remains separately true only at its previous exact SHA. 1.0 `release-evidence.json` S08 stays `UNASSESSED` until frozen candidate/output/approval evidence is collected; no auto-promotion, no product runtime change, no Canonical modification.

**Operational gap:** a test enhancement with no exact-HEAD run cannot close a release gate. Pending status must be explicit; if runner scheduling prevents jobs, repair the execution surface before inferring test success.


## 2026-11-05 second follow-up: exact CI red from malformed regex; scoped fix

**Observed (not inferred) from exact-head CI:** [product PR #241](https://github.com/11576865/MKV-Fast-Muxer/pull/241) commit `73b2d0f6979b2cd313c3657265ce3ad1ecded062` had Browser E2E [run #41880904138](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41880904138) **FAILURE**, job `126752815333`. The run's `Unit tests`, `Build`, `S10 - twenty actual Matroska batch deliveries`, `S10 - combined twenty-job execution and save recovery`, and `S03 - actual font collection faces and CFF subset shaping` steps were independently **SUCCESS**. The `Browser end-to-end mux tests` step exited while Node parsed `tests/e2e/browser-mux.e2e.mjs:5595`, `SyntaxError: Invalid regular expression flags`. The newly inserted literal accidentally contained double-escaped `\\s` and `\\/` in a JavaScript regex. **No full Browser E2E or current S08 behavior ran on that head**; downstream missing artifact upload errors are consequences of the early parse stop, not separate demonstrated feature defects.

**Real product-branch correction submitted:** `1661c4370e64f932abc5372a7cbc0ad09897335f` fixes the escaped regex to valid JavaScript source. `d093d2b9c3184c216ec1910c2408e3985f596162` registers `node --check tests/e2e/browser-mux.e2e.mjs`, moved by `77862f1043bc199a90f29edd184c54ab162f59bb` before expensive `npm test`, S03 and S10 work in the **existing** browser workflow. Corrected exact HEAD: `77862f1043bc199a90f29edd184c54ab162f59bb`. Browser E2E completion is **Pending CI** at last query. No parser, Writer, production UI, acceptance ledger PASS, or Canonical modifications.

**Candidate reusable test-process lesson (not a new Canonical standard):** generated long integration files should be syntax-checked before expensive media/E2E jobs; a CI grammar error is a test-authoring failure and must not be labeled as a runtime safety failure. This supplements the existing S08 acceptance Observation; keep one provenance trail, do not split into redundant cases. Effectiveness to be checked by exact-HEAD run.


## 2026-11-05: New exact-head S08 native-proof CI closed (scoped PASS)

**Dedup:** Continue the existing S08 Observation. The earlier corrected run for PR #166 is preserved; this note reports a *new* exact-head acceptance enhancement in [Draft PR #241](https://github.com/11576865/MKV-Fast-Muxer/pull/241), rather than revising prior observations or adding a redundant general safety rule.

**CI:** Product exact SHA `77862f1043bc199a90f29edd184c54ab162f59bb`; [Browser E2E #41883712596](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41883712596) **SUCCESS** and Pages #41883711835 **SUCCESS**. The Browser workflow's `Check browser E2E syntax before real fixture execution`, Unit tests, Build and actual Browser E2E all completed successfully. The earlier `SyntaxError: Invalid regular expression flags` from #41880904138 is resolved at this exact SHA.

**Direct inspected evidence:** Downloaded actual workflow artifact `s08-current-workbench-complex-mkv-safety` ID `13350732446`, ZIP contents: `softmux-s08-modern-source-safety-evidence.json`, `s08-risk-source-chapters.xml` (986 bytes), `s08-risk-source-tags.xml` (570 bytes), `s08-modern-source-switch-safe.mkv` (946073 bytes).
- Receipt declares browser risk-preflight blocked, forced execution bypass rejected, both original sources unchanged, and safe source real MKV delivered. Those runtime facts are supported by the passing browser scenario and the exact artifact; the source files themselves are not included to independently recompute original hashes.
- Independently inspected ZIP source XML contains chapter UIDs `510010` and `510011`, and the Tag XML targets nested `ChapterUID=510011`. Independently recomputed SHA-256 matches the receipt: chapter XML `2a3428ba3b468fdf2f84e4e3b86adee60c5920623d5aab23f1b8da954e9762c4`, Tag XML `ae760e2a46c7ec054149294f465337a055b91a8d5cbb535a7835273eb2ac5455`.
- Independently recomputed ZIP MKV SHA-256 matches the receipt: `e43433ab843eef764e3756547ae38efab9b4f0a7fd5d217a98b2de659772953c`. Local `ffprobe` directly on extracted MKV exits 0, recognizes `matroska,webm` and reports a `mpeg4` video, `aac` audio, `ass` subtitle and two attachment streams. Receipt's native identity comparison records both safe input and output A/V codecs as `mpeg4` + `aac`.
- This proves a **bounded real Chromium safe-refusal/source-recovery S08 subscenario** in the specified CI. It does *not* independently establish exact video/audio packet equality, all tag preservation for arbitrary MKV, persisted user-local saves, real devices, or full S01–S14 contract-level acceptance.

**Status:** `S08 scoped Chromium/native evidence: PASS at 77862f10`. Softmux `docs/softmux-1.0-release-evidence.json` S08 remains `UNASSESSED` (owner approval of detailed release contract, frozen `1.0.0` release candidate, and cross-scenario evidence are not implied). PR #241 stays Draft; Canonical unchanged. No new release exception or Writer authorization.

## 2026-11-05 V3 PR #239 reconciliation of previously merged S08 native-proof checks

**Product branch evidence:** Main merged Softmux PRs #233 and #241, while the existing V3 Draft PR #239 still diverges. The native S08 mkvextract nested ChapterUID/targeted-Tag assertions, native XML artifact upload, early E2E syntax preflight, and safe-recovery A/V codec comparison previously verified on #241 were absent from the V3 test branch. Commit `b348a967e129317f5d1ab60da571abfa40da3a6c` ports the workflow paths and syntax gate; commit `f6f6d9bd81a92d3e467d199e5d20a25d8cd9a706` ports the original S08 XML and recovery assertions into that same existing V3 branch. The exact regex escapes in the ported JS source were checked textually against the former invalid-regex defect.

**Separate V3 UI red light:** At exact prior code HEAD `8705733b32b52bbec76870839405ad3c66fffdd0`, [V3 pilot CI #41884670851](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41884670851) failed at the `#sfv3Empty` width assertion, although full Browser E2E and S12 scoped workflows succeeded for that head. V3 branch commits `a58491f9ecc20072ef9dbb6d1857c2dfc1fbcb02` and `64b6915bea4e2be1817d5d3b1b7bf790c33bdfdc` enlarge the actual single native empty-canvas dropzone and add off-center pointer/hit geometry checks without introducing a parallel File owner.

**Current acceptance:** Latest V3 branch HEAD `f6f6d9bd81a92d3e467d199e5d20a25d8cd9a706` had no confirmed PR-associated workflow runs in the linked status query. Closing/reopening the Draft PR did not produce a listed workflow for the previous head either. This is a scoped observation of the tool/status surface, not proof of a universal GitHub Actions outage. No latest-head CI PASS is claimed; previously verified #241 native evidence does not equal full V3 acceptance. PR #239 remains Draft; UI visual/physical-device approval and mainline code reconciliation remain pending.

**Dedup:** Extend this existing S08 observation rather than creating another process Candidate; Canonical and 1.0 release ledger unchanged.
