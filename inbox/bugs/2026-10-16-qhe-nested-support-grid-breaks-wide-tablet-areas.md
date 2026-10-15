# Bug / Observation: support wrapper changed named-grid participation on wide tablets

Status: Bug / observed and locally repaired; hosted repair validation pending. No Canonical change.

Product: 11576865/Quick-Automatic-Hardsub-Encoder. Owner authorized expected-model UI integration and desktop/tablet Figma handoff, 2026-10-16.

## Evidence

PR #113 merged as 6bd0ac6dd38323620a812262b60dcb1fce6c680c. Frontend run 38787479870, job 116603120896, failed at check-media-ui.cjs:132: a 920px overview had left=53 while main.right=609. Unlike the earlier review-must-fit-phone baseline failure, this failure is newly observed at the integrated expected-workbench stylesheet.

Cause: changing .support-rail from display:contents to display:grid nested runtime/overview inside a new layout context. Their grid-area values no longer place them in the outer workspace named areas. Mere no-horizontal-overflow checks did not detect the semantic placement loss; the earlier targeted browser test omitted 920/1024/1180 widths.

## Bounded correction and local evidence

Restore display:contents for expected-workbench tablets at 821–1180px. At 920–1180px use explicit outer rows runtime/runtime, main/intent, main/overview, and assign expected-inspector to intent. Existing execution forms remain untouched.

Extended check-expected-workbench.cjs with 1180/1024/920 widths and DOM geometry assertions: overview.left >= main.right - 5 and runtime.top <= main.top + 1. Observed red first (overviewLeft=254.47, mainRight=869 at 1180), then green after CSS correction. All eight widths × three task modes passed, including draft isolation/keyboard/reset.

## Reusable observation / limits

When an override changes a wrapper from display:contents to a formatting context, audit direct participation in ancestor named-grid areas. Test critical arrangement breakpoints and pane relationships, in addition to scrollWidth.

Related dedup: 2026-10-15-version-vector-and-atomic-ui-cutover-gate covers product/spec/code/evidence distinctions; 2026-10-15-hsr-studio-v3-rebuild-after-accepted-v2-rejection covers nested preview clipping. Neither records this particular grid-participation mechanism. This narrow case does not establish a universal layout rule or physical tablet acceptance. Product evidence and repair commit remain authoritative; hosted repair CI pending.
