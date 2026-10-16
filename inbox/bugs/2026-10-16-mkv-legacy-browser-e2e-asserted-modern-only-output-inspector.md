# Bug: Legacy E2E execution tried to assert a modern-only finished-MKV inspector

Status: **Bug / reproducible exact-head Chromium CI; repair submitted, new CI pending**  
Date: 2026-10-16  
Domain: interface-grammar / reliability / acceptance  
Product: https://github.com/11576865/MKV-Fast-Muxer  
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/157  
Initial observed failing workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38885305543

## Direct evidence

At PR #157, the 618 Node tests passed and the Vite / Pages workflow succeeded. The Browser E2E workflow reached `scenarioSelectiveAttachments`, completed the real selective source-MKV mux and report assertions, then timed out after 30 seconds:

```text
locator.click: Timeout 30000ms exceeded
waiting for locator('[data-sf-section="attachments"]')
tests/e2e/browser-mux.e2e.mjs:616
```

`openApp(browser)` deliberately navigated to `?ui=legacy` and asserted `#sf14Root` was absent. But the end of that scenario clicked `[data-sf-section="attachments"]` and checked `#sf14SectionItems` / `#sf14SectionSelection`, which only exist inside `mountSoftmux1014Workbench` on the current public/default UI.

This is a **test-runtime and assertion-surface contradiction**, not evidence that the actual muxed MKV contained the wrong attachments; the real mux and independent report assertions occurred before the unsupported selector call. Nor is it proof the modern inspector works: that requires separate execution against the actual modern UI.

## Bounded repair submitted

In `tests/e2e/browser-mux.e2e.mjs`:

1. `openApp(browser, {modern=false})` retains the legacy fallback by default; `modern=true` loads the normal current workbench and requires `#sf14Root`.
2. The selective MKV+ASS+font+source-attachment scenario now runs once in legacy and once in modern mode, with distinct artifact filenames.
3. Both routes must complete real mux, saved-download report, native `ffprobe` structure and original attachment FileData SHA-256 verification.
4. The modern route opens the real progressive-disclosure source editor, changes the original attachments, and asserts the genuine same-session finished-MKV per-object statuses and audit reason codes.
5. The legacy route checks only legacy surfaces, no fake `sf14Root` / `sf14SectionItems`; no `force` clicks, no removed verified-output assertions and no production writer modifications.

Repair commit: `a729442242851fdd4d61448663f2078e816a86f4` on PR #157. Syntactic parse of updated E2E module body passed; exact-head Node/build/Chromium remain **Pending External Validation**, and product functionality must not be pronounced green based on this record.

## Reusable hypothesis

During gradual UI migration, each integration scenario must bind its expected UI objects and assertions to its explicitly launched runtime/presentation mode. A legacy fallback can validate shared execution and artifact properties but cannot verify production/current-only UI behavior. If both require validation, execute separate scoped real flows with runtime identity checks and independent outputs; do not silently skip current-surface proof or assert selectors absent from the chosen mode.

## Dedupe / authority

Searched Foundry for `ui=legacy`, modern-only selector, softmux legacy E2E and dual-mode migration. Related but non-duplicate record: `inbox/bugs/2026-10-11-mkv-e2e-version-assertion-drift.md` concerns stale **version expectations**, not contradictory **presentation mode**. Other legacy-capability migration Candidates concern functional inheritance. This record is a scoped **Bug**, not a new Canonical grammar or universal release gate. Retain Pending CI until the new exact SHA is externally accepted.


## Follow-up: reverse hidden-adapter mismatch in current UI (2026-10-16 21:14 +08:00)

PR #157 exact head `7594ad41ef330b26134d24becfec9ae15c486cb1` passed 618/618 Node tests and Pages build (run `38892742782`), but Chromium run `38892742989` failed after the legacy selective-MKV case passed. The current/default UI scenario correctly used `#unifiedAssetInput` and observed 2 real original attachments, then timed out on `page.locator('#appendPreserveAll').uncheck()`: Playwright found the checkbox but established that it was **not visible**.

This is the inverse of the original Bug: launching the modern workbench then driving the hidden legacy editor as if it were the visible production UI. `#sf14OptionsDrawer` can disclose some edit options but does not make `#appendPreserveAll` a supported public action. The actual `src/main.js` current-source inventory renders `.asset-container-tree [data-tree-preserve-all]`, with delegated `change` routed to the same underlying domain adapter. Attachment rows are selected in the source tree and edited through `#assetInspectorHost .asset-tree-inspector`, rather than filling hidden `.attachment-item` controls.

Bounded correction in test-only commit `0ee5d5bf16658cdd0d78adfa9ab0242e88d2ae7d`: current-mode scenario now uses the visible source tree, chooses original font and notes by actual scanned names, excludes one attachment, renames the other and edits MIME via context Inspector; it asserts projection parity with original execution adapter values. Legacy mode retains its old input/control path. Real output, ffprobe and finished-file FileData assertions are untouched.

**Pending External Validation:** corrected head browser E2E not yet checked. This is additive evidence to the same mode/selector-contract Bug, not a new Canonical rule or proof of full Matroska preservation.
