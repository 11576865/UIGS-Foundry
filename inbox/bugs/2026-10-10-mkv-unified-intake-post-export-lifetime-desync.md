# Bug: Persistent import inventory stranded by legacy post-export state reset

Status: **Bug / reproduced in browser CI; fix under revalidation**  
Lifecycle: repair-evidenced  
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


## Fix verification — latest PR #69 head

Corrected head: `0e16632d422dd2ea6550f6bce558cbe7df766910` (still **Draft**, not merged).  
Browser E2E: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/37984257203 — **completed success**, with **168/168 Node tests passed, zero failed**. Log contains `MKV container-tree source track editing and post-export retention PASS` as well as `MKV container-tree attachment editing PASS`. The test asserts the selected source still exists after mux, the edited title remains in the tree, the 390px view renders nonzero geometry without document horizontal overflow, and the mux action remains available for a revised run. Latest PR Pages build also passed.

Conclusion: **verified fixed on the PR branch by real Chromium E2E**. No merged-main deployment or broad user visual acceptance has yet been claimed. This Bug remains an engineering observation rather than a Canonical policy change.


## PR #157 regression test adapter-bypass (2026-10-16, pending repair validation)

A later CI event reproduced the **same lifetime boundary from the test side**, not as a newly discovered production regression:

- Exact-head Chromium run: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38888945140; Node **618/618 pass**, Pages/build success, browser failed after real scenario-2 mux and report; `scenarioSelectiveAttachments` modern route observed 0 `.sf14-source-observation` entries instead of two.
- The new dual-mode test launched the modern UI but set `#videoInput`, `#subInput` and `#fontInput` **directly**. These are legacy role adapters; the current public entry `#unifiedAssetInput` was bypassed, leaving `importedAssetEntries.length === 0`.
- Production `src/main.js` intentionally preserves a current task after export **only** when the user-facing inventory exists. The legacy adapter-only branch still clears the hidden input and calls `resetTrackState()`; the source-observation projection then truthfully has no current scanned source. The detached mux report can remain valid without implying source-edit context continuity.
- PR #157 repair commit `22c2bff52410c2810585c551d8ac90d36b2b639b` changes the **modern test route** to import the MKV, ASS and font through `#unifiedAssetInput`, confirms both source observations before output, then requires the exact selected source and object evidence to survive actual output. The legacy route and production cleanup rule are deliberately unchanged.

**Evidence status:** updated test source parsed and core assertions were inspected, but exact-head Node/Chromium after this commit are **Pending External Validation**. This addendum does not claim the current PR is green or that the original MKV's full EBML/UID graph is preserved.

Reusable distinction: integration tests must enter through the user-facing source-identity owner of the presentation mode under test. A hidden execution adapter is not a drop-in substitute for a registered resource inventory when asserting post-export project persistence. This strengthens the existing lifetime Bug rather than generating a new Candidate or modifying Canonical.