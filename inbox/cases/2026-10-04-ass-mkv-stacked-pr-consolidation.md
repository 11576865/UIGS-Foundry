# Case: ASS Workbench MKV container work forms an explicit stacked-PR consolidation chain

Date: 2026-10-04
Status: Case / repository continuation
Project: 11576865/ASS-Workbench-Android

## Observed repository state

Three open pull requests form an explicit implementation stack:

- PR #89: container inventory, identity, preservation verification, and verified-output evidence;
- PR #92: generic Matroska attachments and cover-image workflow, explicitly built on #89;
- PR #96: typed container mutation plan and capability/preflight evidence, explicitly built on #92.

The PR descriptions themselves document the intended dependency order:

`#89 -> #92 -> #96`.

## Continuation implication

When selecting the next engineering task, this state should not be interpreted as three missing features or as a reason to reimplement cover-image / attachment support from scratch.

The productive continuation is dependency-aware consolidation:

1. preserve #89 as the inventory/identity foundation;
2. integrate #92 after that foundation;
3. integrate #96 after the generic mutation path;
4. rebase/retarget downstream PRs as earlier layers land;
5. keep asynchronous CI outside the active polling loop unless an immediately actionable failure is already available.

## Why this case matters

The repository demonstrates a common resumed-agent failure mode: a later session can see an unmerged feature request and incorrectly infer that no implementation exists. In reality, the implementation may already exist in a stacked branch whose remaining work is integration, validation, or merge-order cleanup.

This case therefore provides concrete evidence for the Candidate **Interrupted engineering sessions must reconcile existing work before reimplementation**.

## Evidence boundary

This is one project-specific case. It records current branch/PR relationships and should not be promoted directly to Canonical guidance.
