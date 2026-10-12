# Bug — JavaScript replacement string `$&` expands the match inside authored source code

**Observed:** 2026-10-13
**Scope:** source-code editing / engineering automation / CI validation
**Status:** Reproduced, targeted repair committed; complete PR-head regression pending
**Product evidence:** [PR #102](https://github.com/11576865/MKV-Fast-Muxer/pull/102), failing head `ce12714ceac9be5b8c22cedb8f3d868f0bde442a`, [Actions run 38285258058](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38285258058)
**Repair head:** `8e2512bef015e287da6aca78355e0ae217d6bbff`

## Symptom and cause

During an automated GitHub source change, the agent interpolated a JavaScript regular expression containing literal `$&` (MIME token character class) into the **replacement string** argument to `String.prototype.replace(match, replacement)`. In JavaScript replacement strings `$&` is an interpolation sequence meaning *the entire matched substring*. It does **not** mean the two literal characters `$&`. The existing source regex therefore expanded recursively into multiple embedded copies of its source line. Node module loading raised `SyntaxError: Unexpected token '^'`, causing the focused test file to fail import before functional tests could execute. The exact initial CI run showed **328 passing tests, 1 failing test-file load**, with build/E2E skipped.

## Repair / targeted guard

The invalid line was replaced by an **exact full-line rewrite** with the intended escaped regular-expression slash and literal `$&`, avoiding a second unsafe replacement-string interpolation. The next accurate PR-head CI passed Node tests and Vite Build; full Chromium and external research evidence still pending at intake.

For any future automated source-edit workflow where replacement content can contain `$` sequences, supply a callback replacement (e.g., `text.replace(old, () => replacement)`) or a full-line/file rewrite, and validate **actual resulting file bytes** before triggering expensive CI. Avoid using source regex literals as unescaped `String.replace` replacement strings. This is a single observed Bug record, **not** an automatic UIGS Canonical rule promotion.

## Nonclaim

This edit-tooling failure is not a Matroska parsing, EBML, source-identity or writer correctness defect. Keep the source patch failure distinguished from PR #102's independent compatibility matrix results.
