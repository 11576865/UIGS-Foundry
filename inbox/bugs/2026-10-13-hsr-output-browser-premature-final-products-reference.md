# Bug: HSR output browser used an uninitialized lexical product collection

Date: 2026-10-13
Status: Fix submitted to product main; matching CI and real browser acceptance not yet confirmed
Product: `11576865/HSR-Voice-Archive-Builder`
Affected surface: project overview and Export finished-products browser

## Observed code path

A mainline product-grouping change made `renderProjectOverview(p)` compute whether any existing final artifact should be displayed before a later `const finalProducts=groups.final_products||{}` declaration. The earlier expression accessed `finalProducts` before its `const` initialization, a JavaScript temporal dead zone error. Loading a project with results could throw `ReferenceError` before rendering the artifacts and stop the rest of the overview update. This is a source-level deterministic defect, not a field report.

## Repair and regression

Product main fix: [`2973aa8f`](https://github.com/11576865/HSR-Voice-Archive-Builder/commit/2973aa8fd00c069fdbfe12abb2b23f05516b79d0). The availability check uses a separately initialized `availableProducts=p.output_groups?.final_products||p.outputs||{}` value before toggling the finished-output section. This preserves the last-known-good MKV when a fresh build is interrupted and avoids prematurely reading the subsequent local `finalProducts` binding.

Follow-up regression in `tests/test_archive_bundle_delivery_contract.py` checks the contract; Chromium test `tests/browser_visual_evidence.py` checks stale/current MKV badges, standalone FLAC/SRT/ASS, and legacy black-video distinction on both desktop and narrow phone viewport. During review another test-specific issue was caught: the first button on an existing file is “复制路径,” so browser assertions must inspect the *action list* to find the actual regeneration control; corrected on main.

## Reusable finding

A source-product regrouping can break an adjacent UI even when the data model is correct. In JavaScript render code, all collections used in visibility evaluation must be initialized before their first use; tests should exercise the *production page* against a project with existing but stale outputs, not just search for expected strings.

Evidence tier: source review + corrective commits and submitted regression contracts; not yet confirmed by a matching passing CI run. No Canonical change.
