# Bug: Logarithmic endpoint rounding drops complete candidate context curves

Date: 2026-10-15
Status: **FIX-SUBMITTED; exact-head Chromium verification PENDING**
Project: [QHE PR #103](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/103)
Related: QHE [Mainline Convergence #106](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/issues/106)
First failed full Frontend CI: [run 38641241345](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38641241345)
Candidate fix SHA: `31b31654eaad0dafa00146fc23b759214cadd855`

## Reproduction
PR #103 was semantically reapplied on top of merged main PR #105, retaining the single decision envelope and bounded dashed fitted alternatives. Existing Node model tests passed, but the Playwright synthetic x264/HEVC scenario found **zero** `.curve-branch-ghost` paths where two were expected. The envelope itself remained valid and one main curve was visible.

## Causal mechanism / proposed correction
`createMultiBranchFrontier().sampleBranchCurves(n)` built logarithmically spaced budgets using exact min and max endpoints, called each branch `evaluateTargetBytes`, discarded any non-`within-evidence` point, then discarded the **entire** branch unless all `n` points remained. Small floating-point round-off or branch endpoint differences could make a boundary probe fall just outside the branch's admitted evidence domain. This converted one marginal probe rejection into a missing whole curve.

The candidate patch samples the **interior of the shared measured-domain bins** using `(i+0.5)/n` in log space, without extrapolation or changing the authoritative envelope/evidence bounds; it retains all-point completeness and adds the same asymmetric synthetic fixture to `compression-decision.test.mjs`. Exact-head full Chromium and Windows CI must confirm the fix.

## Reusable lessons (Observation/Bug only)
Numeric graph sampling should not rely on logarithmically reconstructed boundary values being bit-exact when downstream range membership uses strict comparisons. All-or-nothing group filters can hide the whole visualization when one numerical boundary point is rejected. Test asymmetric measurement domains and compare visible plotted-path count, not merely model `ok` or valid primary curve.

## Deduplication
Foundry search located related Candidate `2026-10-03-continuous-decision-sliders-need-branch-aware-frontier-transitions`, which records the feature and evidence intersection, but not this exact observed rounding/strict-completeness failure. This Bug adds the failing example and regression boundary without promoting any Canonical rule.
