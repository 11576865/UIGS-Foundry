# Test / Pending: QHE orphan preview modal and retired mobile tutorial CSS

Date: 2026-10-11
Product: `11576865/Quick-Automatic-Hardsub-Encoder`
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/92
Head: `8c9bd5b5de7e6c54bd9c4d59e7677a46135c12fe`
Status: **Pending external Frontend, Windows smoke and UIGS CI** (runs `38118986854`, `38118986726`, `38118986825` initially in_progress). Not merged.

## Evidence: stale UI styling retained after a component's DOM was removed

QHE `src/main.js` no longer instantiates an element with `id="previewLightbox" class="preview-lightbox"` or the older `.preview-lightbox*` class family. The current image-preview CSS and modern media workspace fullscreen functionality are separate. Nevertheless, `src/style.css` still contained 11 inert desktop/mobile selectors for that deleted preview modal, including backdrop, viewport sizing, safe-area offsets and `display:none!important`. The previous `src/ui-shell.test.mjs` positively asserted that an obsolete `.preview-lightbox` CSS block still existed while also asserting the matching modal DOM had been removed: the test contract itself perpetuated the residue.

The older mobile runtime-help DOM was once a wrapper `<details>` with a direct `<summary>` and `.mobile-runtime-help-body`. The current production UI in `src/main.js` is a `<section class="mobile-runtime-help">` containing two independent `<details class="mobile-runtime-option">`. Ten prior selectors targeted only the old direct summary/help-body shape.

## Bounded correction

QHE PR #92 removes those exact 21 orphan CSS selector blocks (2826 source characters), leaves actual `.preview-image`, `.mobile-runtime-help-grid`, `.mobile-runtime-option` and Android/Windows instructions intact, and replaces the old positive test for the retired modal CSS with **negative assertions** preventing its return plus a positive assertion for the active phone help grid.

This is a **static DOM/selector and source evidence** report. Frontend/Playwright and Windows CI are still pending; no successful screenshots or live physical device claims have been made. The legacy Windows WinForms launcher `windows/start_windows_legacy_ui.bat` remains a specifically documented diagnostics route, not an orphaned production UI.

## Reusable lesson / further scope

A removed UI component can leave more than DOM: dead CSS across responsive layers, stale test assertions, and contradictory fallback policies. Cleanup should compare active markup, CSS selectors and tests, retire only proven mismatches, and guard against resurrection. Other candidate orphan selectors (e.g. `.hero-main`, `.hero-tools`) were noted but **not** removed in this bounded work unit; they require a separate full source/reference check. No promotion to Canonical based on one repository observation.
