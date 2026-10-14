# Reclassified investigation: #103 Chromium failure was Manual test isolation, not proven candidate-curve endpoint loss

Date: 2026-10-15
Status: **MISDIAGNOSIS CORRECTED; numerical robustness patch remains provisional / exact-head CI pending**
Project: [QHE PR #103](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/103)
Run [38641241345](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38641241345)

## Evidence correction (supersedes the initial finding in this entry)

An earlier reading of the bare CI failure `0 !== 2` at `scripts/check-curve-design.cjs:159` wrongly attributed it to `.curve-branch-ghost` SVG paths. The *actual assertion* at line 159 was `#taskCompareCandidates li` from the **existing Manual codec comparison**. The newly inserted synthetic candidate-reference SVG test was located earlier and had already passed. This was confirmed by fetching the exact script and its line numbers and by a later run `38641640221` in which the new same-data Node model test also passed but the Manual UI candidate-list assertion still failed.

**There is NO verified evidence from these runs that floating-point endpoint rounding removed candidate context paths.** The prior content overstated cause and must not be used as product Bug confirmation or promoted to Canonical.

## Engineering changes under investigation

- Candidate defensive change `31b31654eaad0dafa00146fc23b759214cadd855`: bin-center log sampling of fitted alternatives within the common measured evidence interval. This is a reasonable precaution against boundary rounding but is **not shown to have fixed the observed Chromium failure**.
- Candidate UI-test isolation change `64e048ba40b8978adfe72cd44b678475ddf6e588`: the synthetic candidate reference-curve DOM fixture now runs **after** the complete existing Manual task lifecycle, following fresh page navigation, rather than mutating that fixture's original DOM before Manual tests. Original Manual candidate assertions remain enforced and wait for actual rendered list.
- Latest exact-head full CI status: PENDING at this entry; no release acceptance inferred.

## Reusable investigative caution

Always resolve the exact failing assertion by checking the current test file at the reported line number. Error numbers without line context cannot establish whether a regression was in a model, visualization, browser lifecycle or test fixture. Source assertions and programmatic mocks may mask lifecycle coupling; isolate independent synthetic visual tests from shared production UI interaction fixtures.

## Deduplication

Foundry Candidate `2026-10-03-continuous-decision-sliders-need-branch-aware-frontier-transitions` describes candidate curve construction; this corrected record is a misdiagnosis/case of CI evidence attribution, not a confirmation of endpoint failure. Keep historical audit trail without changing Canonical.
