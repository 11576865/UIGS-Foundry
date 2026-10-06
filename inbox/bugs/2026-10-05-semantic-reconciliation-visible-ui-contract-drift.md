# Bug: Semantic reconciliation can regress visible UI contracts without changing feature capability

Date: 2026-10-05
Status: Candidate Bug
Lifecycle: repair-evidenced
Source project: ASS-Workbench-Android
Evidence: PR #129 current-main reconciliation

## Observation

During current-main reconciliation of the generalized Track Import workflow, the implementation intentionally preserved the current-main container architecture and extended the existing add-track entry point to accept additional source adapters.

The functional capability was broadened from Matroska-only Track import to include standalone ASS/SRT normalization and generic-media compatibility probing / MP3 packet stream-copy.

While doing so, the visible button label was changed from:

`添加轨道`

to:

`导入 / 检测轨道`

The underlying interaction still used the same existing add-track entry point and retained the same test tag, but an existing Android instrumentation acceptance test correctly failed because the expected visible UI contract had changed.

The regression was fixed by restoring the current-main visible label while keeping the generalized picker and new source-adapter behavior.

## Reusable lesson

A semantic re-land / reconciliation must preserve not only data-model and execution invariants, but also externally observable UI contracts unless a deliberate product change explicitly owns that contract migration.

Visible labels, test tags, affordance placement, keyboard bindings, and interaction semantics can all be part of the integration contract.

When broadening an existing action:

- prefer extending the action behind its current affordance;
- do not rename or reshape the affordance as incidental cleanup;
- if a user-visible contract must change, treat that as a separate product/UI change with its own acceptance update;
- existing UI acceptance failures should be treated as regression evidence, not automatically "fixed" by weakening the test.

## Evidence boundary

This is one concrete integration failure from ASS-Workbench-Android PR #129. It supports a reusable bug pattern but does not justify modifying any Canonical rule by itself.
