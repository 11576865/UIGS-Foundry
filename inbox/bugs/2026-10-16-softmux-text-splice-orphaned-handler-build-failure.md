# Bug: String-slice UI patch matched a nested `for` and stranded old handler body

Date: 2026-10-16
Status: Bug — reproduced in exact-head GitHub build and source-corrected; final browser E2E independently pending
Affected project: 11576865/MKV-Fast-Muxer
Implementation PR: https://github.com/11576865/MKV-Fast-Muxer/pull/156

## Observed failure

When converting the 0.1014 object's attachments/chapters/tags workbench tabs from explanatory placeholders to real *read-only source observations*, an assistant-authored file replacement selected its end anchor using the first textual occurrence of `  for (const button of root.querySelectorAll('[data-sf-section]'))`. Two spaces were also a substring of an inner four-space-indented `for` in `setSection`. The replacement therefore stopped inside the old function instead of at the intended top-level loop, leaving a duplicate old handler fragment and one stray closing brace. Vite production build failed: `src/softmux-10.14-workbench.js (481:2): Return statement is not allowed here`. Initial head `b7d36681e43c16105e65e3ec31eeb27e118f4c1e`, Actions run `38783764896`.

The repair removed only the duplicated orphaned fragment, preserving the new real source-observation rows, `setSection` logic, and existing navigation listener. Fixed head `c97928f5af4c94729e652d3aa720acb66bec5477`; the build workflow `38783922937` completed successfully. Browser E2E for that head was still in progress when first documented.

## Reusable prevention

For automated modifications to nested JavaScript source, textual occurrence counts and `indexOf` alone are not sufficient if delimiters occur at multiple indentation depths. Match an explicit full marker or use AST-aware transforms, inspect the exact diff range, and run `node --check` / build immediately. Do not silently accept a null branch or orphaned code just because unit tests for unrelated modules pass. Structure-sensitive source rewrites require parse validation before broad Chromium E2E.

## Dedupe / authority

Foundry searches for nested-block string-slice replacement bugs and orphaned returns found no matching record. Related 2026-10-16 softmux output-dock `querySelector` case concerned DOM self-selection rather than source-code splice boundaries. This is a Bug observation, not a Canonical amendment; do not generalize one occurrence into mandatory project policy.
