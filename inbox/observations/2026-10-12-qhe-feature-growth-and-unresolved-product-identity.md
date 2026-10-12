# Observation: Feature growth does not settle product identity

Date: 2026-10-12
Status: Observation / user feedback and interpretive review; **not a product decision**
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
Related prior: `inbox/observations/2026-10-12-qhe-competitive-scope-and-evidence-boundary.md`; `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`

## New user feedback
After evaluating QHE's implemented functions, direction and competitors, the project owner expressed growing uncertainty about what their creation now is, where it should go, and what it should become. **No new scope reduction, feature deletion, split, or Canonical identity was authorized.**

## Tentative interpretation
The current project has accrued at least three distinguishable user-job families:
1. Render ASS + fonts into a video via libass and deliver a verified artifact.
2. Measure quality/size/time, select a supported encode plan and explain uncertainty.
3. Generic transcode and lossless stream-copy/multi-clip jobs.

Each family has plausible individual value, but a shared runtime/FFmpeg implementation does not itself show that all three must be equal first-class missions. Conversely, retaining adjacent capabilities need not mean abandoning a primary flagship workflow. A sufficiently broad slogan like 'intelligent media workbench' can describe all accumulated features without actually resolving relative purpose or future feature-selection rules.

## Reusable review practice (hypothesis)
Before another large feature program or redesign when the owner reports identity ambiguity:
- distinguish **already implemented capability**, **primary user job**, **supporting subsystem**, and **competing mission**;
- trace the intended reason for each major expansion to user-authorized use cases, rather than inferring product purpose from a feature inventory;
- seek explicit owner decision on what must remain central, what may remain adjacent without priority, and what should stop expanding;
- do not silently remove working capabilities or rewrite product/Canonical requirements during this reflective stage;
- subsequently test any identity proposal against concrete examples and alternative products.

This is an Observation of one project and a design hypothesis, **not** evidence that one particular identity is optimal or that the user approves restructuring. No source-code edits or normative changes.

Evidence: user feedback dated 2026-10-12 in product-direction discussion; current QHE main `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`; README, `docs/manual-media-workspace.md`; recent multi-clip PRs #99–#101.
