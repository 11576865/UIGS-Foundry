# Bug: E2E tests asserted a hidden legacy UI surface and a deliberately cleared file picker

Date: 2026-10-20  
Status: **Resolved in scoped branches / integrated UI case and independent CI evidence; not a Canonical rule**  
Product: https://github.com/11576865/MKV-Fast-Muxer  
Current 1 GB feature: [PR #161](https://github.com/11576865/MKV-Fast-Muxer/pull/161), merged to `main@85c0871b027dfb1306ede7cc862db58d5beaad69`  
Metadata tool handoff: original [PR #159](https://github.com/11576865/MKV-Fast-Muxer/pull/159) exact-head success [CI #39295712227](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39295712227); clean-mainline integration [PR #162](https://github.com/11576865/MKV-Fast-Muxer/pull/162), its own exact-head CI pending at time of writing.

## Observed failures

### A. Invisible warning despite populated DOM

New WU-01 showed a source-local, non-blocking warning for input `size > 1_000_000_000` in `#workloadNotice`. New browser test attempted `#workloadNotice [data-source-size-warning] summary`, but in **default modern layout** that legacy stage area was hidden. The DOM node existed and the warning logic returned correct markup, yet the user could not see or click it. The actual Chrome E2E failed with `locator.click: Timeout 30000ms exceeded … element is not visible` at [run #39294865015](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39294865015). Correction: put the same advisory in an always-reachable modern workbench header `#sf14SourceSizeWarning`; retain source-row and batch warning projections; test actual visible clickable UI. Corrected **exact-head** browser CI green [run #39295583406](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39295583406), then merged as PR #161. Unit-only tests or DOM element count would have missed this.

### B. Incorrect FileList source-of-truth assertion

Old PR #159 navigation regression asserted `#unifiedAssetInput.files.length === 1` after browsing Chapter/Tag tool. The public importer deliberately does `void importUnifiedAssets(unifiedAssetInput.files); unifiedAssetInput.value = '';` on change. `FileList.length === 0` is **intentional**, not proof the current selected media File was lost. The failed assertion at Chromium [run #38931803794](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38931803794) therefore cannot establish any product project-state loss. Test correction checks **same exact File reference** between `#videoInput.files[0]` and independent `#p2MetadataSource.files[0]`, authoritative selected source in `#assetInventory`, and the emptied one-shot picker. Previously green behavior preserved.

### C. Old zero-button assertion contradicted the new safe navigation feature

After correcting B, PR #159's exact-head Chromium [run #39295224988](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39295224988) passed the **new** bounded Chapter/Tag tool navigation scenario, then failed an older `scenarioSoftmux1014WholeWorkbench` expectation that flat Chapter/Tag panels contain **zero** buttons. The new feature is precisely one permitted action `data-open-observed-metadata` which only re-inspects exact source and does not inherit write authority; zero buttons is obsolete. Corrected E2E now requires exactly **one** constrained bridge, explicit EBML recheck explanatory scope, and no direct writer controls; PR #159 exact-head [run #39295712227](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39295712227) fully passed. Old Draft PR #159 is stale against main and is being replaced by a semantic delta PR #162, whose own CI must still pass.

## Reusable, bounded lesson

**A UI contract regression test must assert the authoritative state or currently visible user affordance, not an internal input/cache/hidden legacy DOM assumption.** When a legitimate feature intentionally changes affordance count, revise both new and inherited tests **without weakening safety guarantees**: e.g. replacing “zero buttons” with “exactly one safe navigation bridge with no writer consent”; replacing “picker FileList has 1” with “current source-domain File identity persists”; replacing “warning markup exists” with “warning visible, operable, and does not disable mux”.

## Dedupe and evidence scope

Repository search: existing Candidate `2026-10-14-product-block-delivery-over-pr-fragmentation` concerns end-to-end milestones, and Observation `2026-10-17-softmux-flat-observation-to-bounded-writer-tool-identity-gate` concerns independent writer identity/authorization. Existing tests/bugs on file identity address real application stale state, not **false E2E assertions about deliberately cleared one-shot picker** or hidden UI surfaces. This Bug records test-contract mismatch and verified corrections; avoid claiming all future test issues are false alarms. No Canonical edit or generalized probability estimate is justified.
