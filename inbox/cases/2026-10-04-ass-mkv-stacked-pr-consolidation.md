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


## 2026-10-04 consolidation update

The earlier `#89 -> #92 -> #96` stack subsequently grew through attachment CRUD and attachment read/update work. The latest complete attachment workflow was present in stale stacked PR #102, while current `main` had advanced independently.

A current-main replay was first created as PR #101 for the CRUD-level stack. When #102 appeared with the newer extraction + metadata-edit layer, the intermediate replay was intentionally superseded rather than maintaining two authorities.

Current consolidation authority:

- PR #103: `feat: re-land complete Matroska attachment workflow on current main`;
- branch: `feat/mkv-attachment-metadata-current-main`;
- replay revision: `8221bb71f1b6e911b42bed95a8a5c44dc274650f`;
- submission delta: one commit ahead / zero behind current main;
- stale/intermediate PRs #101 and #102 closed as superseded;
- validation state at submission: asynchronous CI pending.

The replay uses the latest #102-owned blobs only across the identified MKV/container ownership surface; unrelated current-main semantic-search work remains authoritative.

This update records integration state only and does not promote any Canonical rule.
