# Case: Legacy source-text and UI-copy assertions block a QHE cumulative integration

Date: 2026-10-15
Status: Case / reproduced CI failures; exact-head full CI pending
Source: [QHE PR #105](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105)
Related tracking: [QHE issue #106](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/106)

## Actual observations
- Full frontend run `38636604553` failed in `src/transcode-calibration-panel.test.mjs` because source-string assertions still expected an old `if(-not [bool]$o.sampleExact)` branch and `manual-ui-paired-windows-2x2-v1`. Production had moved to strict `$exactManualEvidence` and `manual-ui-paired-risk-v2` scoped windows. At commit `1903f53`, those assertions were replaced with stronger path/protocol checks; no production code changed.
- Run `38637363036` then passed the earlier stage but failed in `src/ui-shell.test.mjs` because three assertions still required direct Guided codec/size assignment and an obsolete `sourceEvidenceKey(state.media)` token. Current product uses `createGuidedBranchProposal` → VBR verification → `commitVerifiedGuidedBranch` transaction and `currentGuidedDecisionScope`/samplePlan evidence. Assertions updated at `02114ec`; production code unchanged.
- Run `38637660759` then passed Node/source checks but failed Chromium `scripts/check-whole-budget-ui.cjs`: an expectation `/CPU 参数方案.*重新验证/` was inconsistent with an already stronger UI text `CPU 交接已通过共同任务编译与实际表单复核…需要重新验证编码结果，ASS / VBR 短样证据不转移`. Assertion strengthened to the current verification semantics in `41f360c`; no runtime change.
- Heavy Windows/Android suites were triggered on each ready-for-review synchronize; repeat CI incurred overhead despite the three issues being detectable as outdated assertions. This does **not** justify bypassing full runtime gates at merge.

## Reusable candidate learning, not Canonical
After refactoring a high-authority task/verification path, source grep and exact UI copy checks can become stale even when the new execution contract is strictly safer. Prefer behavior assertions of allowed/forbidden transitions and evidence receipts; when source-level invariants remain necessary, tie them to semantic markers (verified adoption, stable evidence scope, correct rollback) rather than exact implementation spelling. Preflight an inexpensive complete Node/static/Chromium contract suite before dispatching all expensive native matrices, while still requiring the mandated exact-head full acceptance before merge.

## Boundary
These failures establish **test drift** for the cited assertions only. They do not prove no application bug elsewhere; the actual Chromium + Windows + Android result on the final head remains open. No Canonical promotion and no replacement of approved initial-version scope.

## Dedupe
Queried Foundry for stale source-regex assertions, source-text drift after refactor, branch-inventory/squash divergence and exact-head acceptance. Related `2026-10-15-qhe-draft-green-not-full-runtime-acceptance` Case concerns Draft job gating, not source-contract drift. Existing stale-branch and product-block Candidates concern integration granularity, not these actual failing test assertions.
