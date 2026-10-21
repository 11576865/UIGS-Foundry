# Test (Pending CI) · S09 two distinct source/external drafts across browser reload

Date: 2026-10-21
Status: **Test candidate submitted; exact-head CI Pending. NOT accepted; NOT Canonical**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/168
First exact product head: `cf47c3e7edfd0bd046c642f0c2a63fed44d8048c`
Reference: `docs/softmux-1.0-product-acceptance-contract-20261020.md` S09.

## Deduplication
- `inbox/tests/2026-10-15-mkv-external-checkpoint-sha-sidecar-rebind-cas-undo.md` already covers external track checkpoint SHA/sidecar rebind and consent/undo at its own boundary.
- Historical source-track detached-draft replay / original attachment case tests are already in product `scenarioVerifiedDetachedTrackRestore` and source/attachment recovery. No new general Candidate is proposed.
- This newly proposed **integration acceptance** binds *both existing portable draft types* to the same real user workbench across a literal page reload. It does not introduce a new merged project schema or general permission authority.

## Submitted test path
1. Real Chromium, current object workbench; public intake of `source-with-attachments.mkv` and `external.flac`. Edit a real scanned original audio-track title via Inspector, and external FLAC title via its existing owned editor.
2. Export the separately scoped original-source ContainerProject draft and external metadata checkpoint; verify source SHA-256 and actual edit intent.
3. Reload the actual page. Verify no File permission/selected source and no automatic consent. Import both JSON files; neither is permitted to restore File handles or authorize execution.
4. Re-import both original resources from current public UI; verify no silent metadata application. Independently SHA-256 verify/authorize source draft, then SHA-256 verify/authorize external checkpoint. Require separate confirmation checkboxes.
5. Verify frozen executable plan contains both actual titles; generate a real output Matroska, run independent native `ffprobe` on both audio-stream titles, and verify source bytes not modified.
6. Upload two JSON drafts + actual MKV + source-bound output receipt as one exact-run CI artifact.

## Explicit limitations
- No single atomic all-objects project export/import is claimed; existing implementation has **two** independent user-confirmed portable drafts.
- No browser File grants, arbitrary Chapters/Tags/UID edits, running job, persistent undo history or future device support is reconstructed by JSON import.
- UI change in `src/softmux-10.14-workbench.js` displays these restrictions inside the real recovery disclosure.
- S09 full contract additionally requires negative conflict tests, supported undo/redo scope and further device/UX acceptance. This PR **alone** cannot make S09 fully PASS.
- On CI failure capture exact assertion/error before any correction. No Canonical mutation from one fixture.

## First Chromium CI result and correction (2026-10-21)
- First PR head `cf47c3e7edfd0bd046c642f0c2a63fed44d8048c`, Browser E2E [run 39543164963](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39543164963): **failure inside newly added S09 test before exporting drafts**. Playwright found `#newAudioList [data-new-audio-field="title"]` but the actual shared Inspector had not been switched to the external-audio filter, so the element was hidden for 30 s. This is a **test entry/navigation bug**, not evidence of a broken restore transaction.
- Exact corrective commit `3e416596c3a83feffe03382a6588ff243868b2cc`: navigate using actual asset resource's `[data-asset-focus-key]` Edit action; verify correct options drawer and visible external title field. No production recovery/authorization change and no weakened assertions.
- **Next exact-head CI Pending**. Capture and classify any later failures independently; never call S09 accepted before the reload/mux oracle actually completes.

## Second Chromium CI / desktop disclosure correction

- Product head `3e416596c3a83feffe03382a6588ff243868b2cc`, [CI 39543624691](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39543624691): **failure** at `assert(#sf14OptionsDrawer.open === true)` immediately after the external-audio Edit action. That action changes object focus, but the desktop (>680px) shared options drawer intentionally stays collapsed; only phone layout automatically opens it. This is a UI navigation expectation error, not a verified domain recovery failure.
- Corrected test first chooses the actual external asset, then explicitly clicks the visible options drawer summary when closed. Follow-up `6924b66b0008f5ff3d9b6b3b3d827bd5041ac2e8`.
- To reduce expensive delayed feedback, move the independent S09 case near the beginning of full Chromium suite before the historical 90+ scenarios (`c67e45ac47ae57f69c3c5963f18441460c7a290d`). Full suite remains mandatory. **Exact head Pending CI**, no S09 pass claim.

## Third CI: exact-head S09 real browser PASS

- Product test head `c67e45ac47ae57f69c3c5963f18441460c7a290d`, [CI 39544078401](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39544078401): **success, full Browser E2E**. Log explicitly reports `S09 real reload + two explicit consent paths + ffprobe PASS` and `All browser E2E scenarios PASS`.
- The same run includes real S10 batch execution, native Matroska fixtures and the full historical suite. Exact S09 uploaded artifact `s09-cross-reload-two-draft-real-mkv` contains the two JSON drafts, finished MKV and SHA-bound receipt; the actual code asserts independently probed original and FLAC title metadata and unchanged source files.
- PR #168 then advanced the product version authority from `0.1023.0` to `0.1024.0`, plus README scoped release note. **Current PR head `c8b04a5fd1166ee6fea92c6ef4fdeba569cd25eb` is Pending final exact-head full CI.** Do not treat old version-head success as proof that new exact commit passed.
- This single case proves the two distinct supported recovery paths work together in the tested browser/fixtures. Full S09 across source/attachment/external conflicts and comprehensive undo/redo is still partial. No Canonical changes.
