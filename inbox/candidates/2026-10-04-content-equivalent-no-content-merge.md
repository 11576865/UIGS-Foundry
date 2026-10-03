# Candidate: When a feature branch already contains main's file changes, use a no-content merge to restore ancestry only after path-level equivalence is verified

Date: 2026-10-04
Status: Candidate
Domains: git, branch-integration, CI, parallel-development

## Summary

Parallel branches can independently absorb the same corrective patch before that patch is merged to `main`. After `main` advances, Git then reports the feature branch as behind even though the relevant file contents are already equivalent or the feature branch contains a strict superset.

Blindly recreating the merge by overwriting files from `main` can erase branch-specific work. Conversely, leaving ancestry stale causes repeated mergeability churn and redundant CI.

A safer integration pattern is:

1. identify every path changed on `main` since the feature branch's merge base;
2. verify each such path on the feature branch is either content-identical to `main` or a reviewed semantic superset;
3. if all main-side changes are already represented, create a merge commit whose tree is the current feature-branch tree and whose parents are the feature head and current main;
4. if any main-side path is missing, construct the combined tree explicitly before recording the merge;
5. rerun CI from the resulting head.

## Evidence

ASS Workbench Android advanced `main` with PR #94, which changed only:

- `.uigs/ui-visual-capture.json`
- `UigsRendererVisualCaptureInstrumentedTest.kt`

PR #93's branch already contained the corrected PNG-backed renderer fixture plus additional spatial-fade capture logic, so its current tree was a reviewed superset of `main` for those paths. The branch therefore used a no-content merge commit solely to restore ancestry.

PR #95 did not contain those main-side fixture updates, so its integration used an explicit combined tree: current #95 tree plus the two files from current `main`, followed by a two-parent merge commit.

This distinction prevents both accidental reversion and unnecessary manual conflict edits.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- main: `31db5c79679fa8e14aa59fa1421362d14ea4370a`
- PR #93 merge-main commit: `db01c0ff489bc3132bb6f9d80a239064a32eb13f`
- PR #95 merge-main commit: `1e19e0d0f4bf2d52da27c95f624582017b9596d1`
- deduplication: searched UIGS-Foundry for equivalent content-equivalent/no-content ancestry merge guidance; no direct duplicate found

This is a Candidate only. It is not Canonical.
