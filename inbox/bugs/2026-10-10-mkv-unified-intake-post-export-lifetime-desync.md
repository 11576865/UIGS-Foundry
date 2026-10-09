# Bug: Persistent import inventory stranded by legacy post-export state reset

Status: **Bug / reproduced in browser CI; fix under revalidation**  
Date: 2026-10-10  
Project: `11576865/MKV-Fast-Muxer`  
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/69  
Issue: https://github.com/11576865/MKV-Fast-Muxer/issues/68

## Evidence (real browser CI)

Browser E2E `37983860309`, job `114000888354` failed at `scenarioUnifiedContainerTreeEditing` line 1692 with `assert.equal(await tree.isVisible(), true)` after real original-track edit, real MKV mux and downloaded output assertions had passed. The Node suite **168/168 passed** and the Pages build passed; failure was in the actual browser test.

Root-cause source investigation discovered that the pre-inventory mux success path unconditionally performed:

```js
videoInput.value = '';
audioInput.value = '';
subInput.value = '';
externalAudioState = [];
newSubtitleState = [];
renderNewTrackLists();
resetTrackState();
```

But the new unified `importedAssetEntries` remained populated after export. The visible entry and selected source still existed, while the hidden legacy adapter and the live source-container `trackState` no longer existed; `renderImportedAssetInventory` could no longer render the verified source tree. The failure was originally encountered on a 390px viewport transition, but the confirmed cause was the **post-export domain-state reset**, not merely viewport geometry/reflow.

## Correction and reusable boundary

Once a workbench introduces a **persistent imported-asset inventory**, task completion must not silently clear independently owned execution adapters and editable domain state while leaving that inventory in place. Output artifact creation, temporary execution filesystem cleanup, and user-editable task lifecycle are separate ownership scopes.

On PR #69 the unified mode retains selected files, original-source track edits and the post-export ability to re-edit/re-export. The legacy non-inventory path keeps its previous clear-on-success behavior. E2E adds explicit assertions **immediately after export** that the selected source, edited track value and expanded tree survive, plus a 390px condition-based visible/nonzero-layout check to guard responsive reflow races.

## Evidence status / follow-up

Root cause is code-grounded and the pre-fix failure was reproduced in a real GitHub Chromium job. Repaired latest-head CI was **in progress** at initial record creation; do not describe the fix as validated until a subsequent successful run is attached. No Canonical update.

Deduplication: Foundry searches for post-export source inventory reset, task lifetime/input adapter persistence, and content-first workbench clear after mux found no matching record. This is distinct from the previous responsive geometry race observation (PR #60); here the DOM really lost its backing `trackState`, not merely momentarily returned 0×0 during CSS reflow.
