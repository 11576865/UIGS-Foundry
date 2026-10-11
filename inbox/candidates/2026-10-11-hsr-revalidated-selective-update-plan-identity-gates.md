# Candidate: Selective updates require an exact revision and identity gate at Apply

Date: 2026-10-11
Status: Proposed implementation in HSR PR #133, new-head CI pending
Project: HSR-Voice-Archive-Builder
Categories: UI selection, plan invalidation, mutation safety, source identity

## Evidence

HSR's existing remote index comparison differentiates newly indexed voices, existing source changes, variants and identity ambiguity. The first implementation offered one Apply action for all new voices while other classes remained review-only. The added filtered selection UI can narrow this operation by visible chapter/category/search results.

The source comparison and eventual download happen at different times. If an archive is rebuilt in between, a previously displayed update list may no longer represent the actual current archive. Filename-only provider mapping also cannot distinguish package-relative paths with the same basename.

## Proposed implementation

- `remote_update_plan` stores the SHA-256 digest of the Manifest it compared. The Apply request verifies this digest against the current Manifest before creating a background job; plans lacking binding or changed by a rebuild must be rechecked.
- Selected filenames must be an explicit validated subset of `new_logical`, not `changed_existing` or `ambiguous`, with collision rejection against existing index/member basenames. `None` retains old all-new API behavior, but an explicitly empty selection never means all.
- The UI's existing update review supports per-file checkboxes and current-visible select/deselect, with the existing grouping and filtering surfaces, avoiding a new workbench.
- Only a current-run selection can enter the combined package; old human subtitle override sidecars are not reauthored by Apply.

The supplier presently exposes filename-keyed source records, so not every local member path can be imported through this incremental route. Reject rather than guess.

## Evidence / limits

- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
- `app/remote_update_guard.py`, `app/remote_index.py`, `app/server.py`, `app/lite_server.py`, `app/static/index.html`, `tests/test_remote_update_guard.py`
- Synthetic fixture/unit and CI evidence only; no real game package acceptance or main merge at intake.
- Existing Foundry search found adjacent stale-batch candidates, but none covering this provider-source identity and Manifest revision gate specifically.

Intake: Candidate. No promotion to Canonical from one observation.
