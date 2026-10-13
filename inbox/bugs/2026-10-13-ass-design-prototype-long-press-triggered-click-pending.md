# Bug / Pending: Long-press tooltip release can trigger the icon action

Date: 2026-10-13
Status: BUG / PARTIALLY FIXED / PENDING VALIDATION AND SYNC
Scope: editable MagicPath design prototypes of ASS Workbench, NOT current Android production APK
Project: https://www.magicpath.ai/files/460655286273863680
Figma original (unchanged due Starter MCP rate limit): https://www.figma.com/design/RXL2w90u2ClPRg3FH8aKAc

## Evidence
Owner asked to stop permanently displaying interface explanations; present concise semantic icons and reveal explanations through long press. The UI prototypes have six MagicPath components in a shared canvas. They render actual editable, interactive React controls, not generated raster screenshots. The first build images displayed CJK tofu even though build succeeded; subsequent font import corrected Chinese and Japanese in preview images of the main, timing and batch variants.

Review found that the first tooltip implementation used a 500 ms timer to reveal help on touch/pen long press, but attached an independent onClick handler to the same button. A long press ending in pointerup typically leads to click, risking activation of the action it was intended only to describe. This is a source-level risk; no device-touch E2E was executed. A related secondary concern is focus tooltip triggered by pointer-induced focus rather than only keyboard-focus-visible.

## Fix progress
- Screen 01 main editor: React source patched so longPressed ref suppresses subsequent click, touch-specific tooltip behavior is separated from keyboard focus-visible, and the tooltip can persist briefly after release. MagicPath revision `460660225301688320` built successfully. Runtime gesture acceptance is still **Pending**, not verified.
- Screen 02 timing component `460655587177435136`: **Pending** source patch and rebuild.
- Screen 03 visual styles component `460658620363853824`: **Pending**.
- Screen 04 spatial component `460658664257261568`: **Pending**.
- Screen 05 fonts/QC component `460658760193552384`: **Pending**.
- Screen 06 batch component `460658810453921792`: **Pending**.
- Original six Figma boards also **Pending synchronization**: Figma Starter MCP call limit returned explicit rate-limit error, so no changes were made to that file.

MagicPath external-agent API quota reached `limit=50, used=50`, resetPeriod unspecified and API was blocked after screen 01 patch. Do not claim six gesture fixes were performed, and do not invent a quota reset date. Pending until connected tool access is restored.

## Acceptance
1. Touch/pen long-press >500 ms shows name/short help and never triggers the button action on release.
2. Short tap activates action and does not show explanatory tooltip.
3. Mouse hover and keyboard focus-visible may reveal an equivalent accessible description, but pointer-induced focus must not produce a premature tooltip.
4. Gesture movement/cancel/leave cleans up timers, and tooltip overlay is not clipped in phone/tablet states.
5. Same behavior across all six prototypes, with source revision and interactive test/video evidence.
6. Keep visible key data, units, source scope and explicit destructive/primary action verbs; long press hides *explanations*, not domain truth or safety controls.

## Dedupe
Searched Foundry code for 'long press click activation', 'long-press tooltip triggers action', 'Android touch click after long press'; no directly equivalent UI-trigger Bug found. Existing `2026-10-12-single-source-contextual-help-and-settings-scopes.md` supports contextual help and optional compact/icon-only toolbar, and `2026-10-11-browser-ui-screenshot-cjk-font-coverage.md` already addresses the general CJK evidence problem. Do not create a duplicate general CJK candidate.

No Canonical promotion. This Bug is about prototype interaction, not evidence that production ASS Android has the same defect.
