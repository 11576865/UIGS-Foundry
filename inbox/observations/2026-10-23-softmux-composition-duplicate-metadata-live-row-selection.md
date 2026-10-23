# Observation: Composition display keys can collide even when live resource grants are distinct

Date: 2026-10-23
Status: **Observation / code-level defect and submitted bounded repair; exact-head CI Pending**
Product: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Product baseline: 软封 0.1027 / main `585f4e8e8473e09d0a4c7fa63d66368d9a9f9870`
Product repair: [PR #182](https://github.com/11576865/MKV-Fast-Muxer/pull/182), branch `fix/softmux-s13-composition-collision-20261023`, head `17cd2754d7345bfddaae38d6ae25398ce15e1e91`

## Source-grounded defect

The existing `buildOutputComposition` produced row IDs such as `external:subtitle:${file.name}|${file.size}|${file.lastModified}` and `font:${file.name}|${file.size}|${file.lastModified}`. Multiple intentionally selected media resources with identical filename/size/mtime, including intentionally repeated *same* File, could have identical visual row IDs, active selection keys, and downstream document projection identifiers.

The workbench's `activateCompositionTrack` then used `.findIndex(row => outputCompositionFileKey(row.file) === target.fileKey)` to route to an external editor. When two rows shared metadata, the second row could select the first editor field. The intake inventory focus similarly took the first metadata match. This is a UI object-routing defect, not evidence of byte-level mux corruption; no Chromium reproduction has yet been claimed.

## Bounded change submitted

- `src/output-composition.js`: retain the first legacy row ID, append a duplicate-occurrence suffix to subsequent same-key external audio, external subtitle and font rows; attach the **current live row index** to each target. The index is a presentation occurrence, not a persisted or cryptographic resource identity.
- `src/main.js`: validate the selected index against the current live row before navigating. When stale, clear selection rather than sending the click to an arbitrary first metadata match. Inventory focus uses exact `entry.file === targetRows[matched].file` reference identity.
- `tests/output-composition.test.mjs`: test distinct same-metadata Files and intentionally repeated same File, unique IDs, deterministic re-projection and indices.
- `tests/composition-workspace.test.mjs`: enforce index-bound routing and explicitly exclude metadata-first `findIndex` selection.
- Execution and persistence contracts, writer admission, source digest/permission checks and product version are unchanged.

## Evidence and pending gates

Code inspection demonstrates the preexisting duplicate-key possibility and first-match selection path. The submitted diff is four files. **Node/build/Chromium exact-head results and real-device acceptance have not been observed in this intake**. PR #182 is not a verified merged fix; preserve `Pending CI` until a specific run and SHA confirm it. The collision scenario is an additional coverage target, not an S13/1.0 completion claim.

## Dedupe with existing Foundry records

- [2026-10-14 external asset live-domain exact File and form epoch Case](../cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md) already addresses **authoring metadata propagation** under file re-selection and asynchronous DOM mounting.
- [2026-10-16 stale same-metadata output evidence Observation](2026-10-16-softmux-output-evidence-stale-same-metadata-source-file.md) already addresses **historical artifact applicability**.
- This Observation adds the distinct **same-session output composition multiplicity and editor-target routing** failure mode. Neither existing item is duplicated or superseded.

## Transferable hypothesis, not Canonical

A display reconciliation key derived from `name|size|mtime` should not be presumed unique within a multi-object UI. Distinguish repeated occurrences, validate that an interaction still addresses its current live row, and keep exact browser File object authority separate from both row position and file metadata. Stronger permanent identity, async list-reordering semantics and end-to-end browser behavior require separate evidence. One implementation does not justify automatic Canonical rule changes.

## 2026-10-23 follow-up: real browser routing regression submitted and a distinct intake caveat

Product PR #182 head moved to `91a6682c246e6341c723fbe6ea25a5a3f3e76fd4` with a direct modern Chromium scenario in `tests/e2e/browser-mux.e2e.mjs`: two distinct browser File instances with **exactly equal** name, byte count and lastModified are selected into the existing subtitle picker alongside a real MP4; after the editor builds two composition rows, clicking the second must focus subtitle title field `data-index="1"`, then clicking the first must focus `data-index="0"`. It asserts the two UI row IDs differ, and does not claim a completed media mux. **Exact-head Chromium verdict Pending** at this record update.

A separate source audit found `src/main.js::importUnifiedAssets` and `importBatchUnifiedAssets` explicitly deduplicate incoming Files using `assetIntakeKey = path|size|lastModified`, before classification. Therefore the **unified intake flow can omit a distinct same-metadata File from its inventory**, regardless of the composition projection repair. The direct-picker test does **not** certify the unified intake collision path. That intake behavior needs its own bounded UX/collision handling and tests; do not misrepresent this PR as solving both. This is an open, unverified-in-browser gap, not silently promoted to a release acceptance PASS.

Dedupe: exact File vs metadata ambiguity is covered by the prior live-domain Case; this addition distinguishes **insertion-time duplicate elimination** from the already documented **display occurrence routing** failure. The Foundry record stays at Observation; no Canonical change.

## 2026-10-23 real Chromium negative result at S13 exact head

[PR #182](https://github.com/11576865/MKV-Fast-Muxer/pull/182) exact head `91a6682c246e6341c723fbe6ea25a5a3f3e76fd4`: Node and build + S10 real 20-job step passed, but [full Chromium CI #39896671612](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39896671612) **failed** in the new `scenarioS13SameMetadataCompositionSelection`. Two distinct equal-metadata browser File objects produced two output rows and two title form controls, but after clicking the second row the intended `[data-index="1"][data-new-sub-field="title"]` input was not `document.activeElement`. This is now **actual browser-observed UI routing/focus negative evidence**, not merely a source-code hypothesis. Do not merge or mark S13 accepted. A diagnostic-only follow-up head `8b28a8d21feeba57105ae1d7d3a288f01446eab2` records active element, editor category, field visibility and selected row for root-cause localization; verdict Pending. Separate unified-intake filter Issue #184 remains open.

## 2026-10-23 diagnostic proof and focused repair attempt

[CI #39897150104](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39897150104), head `8b28a8d21feeba57105ae1d7d3a288f01446eab2`, recorded the precise Chromium negative state: the second output row had `aria-pressed=true`, editor category was `subtitle`, both index 0 and index 1 title fields were visible/enabled, but `document.activeElement` was `<body>` after the click. This falsifies a simplistic “wrong first metadata row index” explanation; a repaint/focus-lifetime interaction is implicated. The code still called `first.focus()` before `renderOutputComposition()`.

[PR #182 follow-up commit](https://github.com/11576865/MKV-Fast-Muxer/commit/426b3c863e31fbbd32dd2e321e31fbdee15e1aff) now repaints the composition before querying and focusing the live editor field. This is a **hypothesis-driven repair, Pending exact-head Chromium**; no verified pass or main merge has been asserted. No unrelated writer, File permission, or browser-download behavior is changed.

## 2026-10-23 S13 admission correction and post-click focus guard (separate pending PRs)

[Issue #184](https://github.com/11576865/MKV-Fast-Muxer/issues/184) tracked a separate insertion-time loss: unified single and batch intake computed `assetIntakeKey(path|size|lastModified)` and silently omitted the second distinct File reference **before classification or user-visible diagnostics**. [PR #185](https://github.com/11576865/MKV-Fast-Muxer/pull/185) adds a shared pure `planIncomingAssetIntake`: identical exact File object is idempotent, different File with identical display metadata is a *visible, non-executable, removable conflict entry*, both single and batch. Existing unidentified-file blockers inhibit single mux and batch job admission. This is conservative **rejection with explanation**, not concurrent support for ambiguous names, byte equality proof or a new File permission model.

The initial Node failure at 642/643 was a newly authored fixture with escaped literal newline characters instead of actual ASS line separators. Corrected test subsequently reached Node/build green. First new Chromium regression arrived at the explicit collision status but test code mistakenly called nonexistent Playwright Locator `.text()`; changed to `.textContent()`. Latest candidate PR #185 head `3a038bed5218bcaef077e073eed3022e067ef9a4` is **Pending exact-head full Chromium E2E**, not integrated. Two **different byte payloads** with equal metadata are authored by the browser test and separately exercised through public single and batch upload inputs; downstream refusal/removal still requires verified E2E.

PR #182's repaint-before-focus candidate head `426b3c8` failed a rerun of [Chromium CI #39897349011](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39897349011): second object stayed selected and visible, but focus remained `<body>`. The follow-up `f6617093aef4bc283123a2cb851c2717c6c6c499` retains synchronous focus and attempts a guarded next-frame focus: only if selected composition ID and currently bound File reference still match. The full Chromium E2E on that head is **Pending**; do not infer passing interaction from the code change.

**Dedupe and authority:** Existing live external asset Case covers metadata drift and immutable form epoch; this Observation distinguishes (1) duplicate output row key, (2) browser event default-focus lifecycle, and (3) pre-classification ingestion elimination. Keep these as candidate/observed scopes, do not change Canonical from a single defect or unvalidated CI.

## 2026-10-23 S13 real Chromium green subscenario, whole-suite pending

[PR #182](https://github.com/11576865/MKV-Fast-Muxer/pull/182) head `f6617093aef4bc283123a2cb851c2717c6c6c499`, [Chromium run #39908268202](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39908268202): **S13 equal-metadata external subtitle composition routing PASS** with actual two subtitle controls and target focus restored after browser click finalization; S09 wrong-source/source-attachment recovery and S08 nested ChapterUID/targeted Tag refusal also passed, and the 20 real S10 batch job step passed. **The overall E2E run failed later** in existing Scenario 9 invalid-audio recovery (`#muxBtn` still disabled directly after failure status). Code review located that status is published in `catch` before asynchronous FFmpeg/WORKERFS cleanup and `finally{running=false;updateUI()}`, creating a plausible test timing race. New PR head `942838cc69e6e06b3e2acc400a982fb65fc67692` waits for actual executor/Cancel readiness after error before asserting recovery. This is a *test-oracle timing repair*, and only exact-head subsequent native/Chromium output can establish full regression green. Do not assert merge or universal S13 acceptance from the one passing subscenario.
