# Test: Source import menus retain stable visible focus through file selection

Date: 2026-10-17 Asia/Shanghai
Status: Test / local evidence passed / hosted pending
Product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/123
Head: c0957e7b195f71fd5eae628d152615f1f6e035cc

## Dedup
Searched `picker focus`. Related existing Case: inbox/cases/2026-10-11-qhe-functional-ui-rebuild-low-copy-workbench.md (PR96 invisible file-input focus). Related observation: inbox/observations/2026-10-14-ass-unified-container-attach-replace-intent-review.md (cancel picker preserves source/focus). This is narrow regression evidence for a menu-triggered picker, not a new Canonical rule.

## Counterexample and repair
The new source menu hid its currently focused menu button and programmatically clicked the original Native/Web picker. Main logic still selected the correct asset, but an activeElement assertion deterministically failed: focus fell to the body rather than a visible control. Restoring focus to the Native picker button alone would be unstable because it is temporarily disabled while its asynchronous picker request is pending.

The menu now focuses its visible, stable toolbar trigger before invoking the unchanged original picker. Native picker completed/cancelled and real Web filechooser completed paths all preserve this visible focus. Cancelled Native selection keeps the previous ASS. Escape also closes the menu and returns trigger focus. No duplicate source-state owner or automatic import.

## Tests and limits
Actual QHE main + Windows client exercised with mocked Bridge HTTP: explicit external ASS/fonts, ordinal1 embedded ASS import/retry, pending-source and unsupported/workflow/running gates, and unchanged subtitle/attachment preservation. Native cancellation and completion focus pass; Web Playwright filechooser confirms user-activation chain and post-selection focus. Full browser suite, 11 widths x3 workflows, 427 Node passes/12 skips and build passed. Independent review closed the focus finding.

Native mock fonts are transport fixtures, not real font validation or OS dialog/device evidence. Hosted current-head CI is pending. Do not infer real Windows extraction/libass, Android SAF, universal accessibility or Canonical promotion.
