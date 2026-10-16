# Test: QHE mode change completes before deferred range-panel projection

Date: 2026-10-17 (Asia/Shanghai)
Status: Test / local regression passed / hosted repair pending
Product: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/122
Repair head: fdd3945c7242946a257b35af7c810077b374449f
Failure: frontend run 38929527049, job 117069627655, check-workbench-basic.cjs line182, `Copy opens its primary range controls`, false!==true.

## Dedup
Searched `animation frame` and `condition wait`. Related existing Candidate: inbox/candidates/2026-10-02-presentation-regression-isolation-semantic-sync.md, read before intake. This adds a narrow Web scheduling counterexample and Test evidence; no new general rule or Canonical change.

## Reproduction and cause
A Copy mode click synchronously updates body.dataset.mediaOperation. A MutationObserver schedules requestAnimationFrame(refresh); only the later basic projection refresh sets details.open and boundary visibility. Playwright click completion therefore does not guarantee rendered projection readiness. Calling the actual DOM button click and immediately reading details.open within one page.evaluate event turn deterministically reproduced the original false while mode already equalled copy.

## Regression
Keep same-turn click to avoid accidentally passing because browser-driver timing allowed a frame. Wait for the semantic contract: mode copy, range details open, range controls unhidden, and copy boundary unhidden. Retain original open=true and actual isVisible assertions, plus downstream real task-compiler and per-stream timing checks. A permanently closed panel still times out. No sleep, assertion deletion, generic retry, or product code change.

## Evidence and limits
Repaired entire check-workbench-basic.cjs passed; Node 427 passed/12 skipped/0 failed. Independent static review found no required issue. Original failing CI had already passed Node, real FFmpeg integrations, build and both other browser suites. Repair hosted CI is Pending and intentionally not polled after one bounded repair. Browser media transport is simulated; this proves test synchronization, not field media timing, exact cut accuracy, or physical device acceptance.
