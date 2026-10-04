# Bug: Code written against an assumed dependency model can fail only after CI injects the pinned dependency revision

Date: 2026-10-04
Status: Bug
Lifecycle: repair-evidenced
Scope: pinned dependencies / source injection / CI compile boundary / external API contracts

## Symptom

ASS Workbench Android PR #97 extended the injected mkvgo helper with attachment replacement logic and attempted to read/write `mkv.Attachment.Description`.

The repository does not compile that helper against an arbitrary/latest mkvgo model. CI checks out the pinned upstream revision:

`gravity-zero/mkvgo@085894ba0df6d14fb4dc4d41bab9aeb3283b3743`

and injects the project helper into that tree.

At that pinned revision, `mkv.Attachment` has no `Description` field. All three PR workflows therefore failed during the injected Go bridge build before Android validation began.

## Root cause

The feature implementation assumed a Matroska concept/API surface that the pinned external model does not expose.

The repository-side helper file can look internally coherent because its target package is materialized only in CI. Static review of the host repository alone is therefore insufficient to prove the injected code compiles against the actual dependency contract.

## Fix

PR #97 revision `78c7b5ca92a318b78807557b6db19dd126be3024`:

- removes use of the nonexistent `Attachment.Description` field;
- updates regression fixtures to assert the identity/content guarantees the pinned model can actually represent;
- narrows the PR claim: FileDescription preservation is not claimed while the pinned writer model does not expose it.

## Reusable rule

For source-injection or patch-overlay integrations:

1. treat the exact pinned dependency revision as the compile-time API authority;
2. inspect the pinned model before adding fields/method assumptions;
3. make tests construct only values representable by that pinned model;
4. do not claim preservation of metadata the dependency cannot read/write;
5. where feasible, add a local or CI preflight that compiles the injected overlay against the pinned tree before broader platform jobs.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #97
- failing revision: `51b8d2e26ad8b14401b8a5d0bb458bbc5c76ff6b`
- repair revision: `78c7b5ca92a318b78807557b6db19dd126be3024`
- pinned dependency: `gravity-zero/mkvgo@085894ba0df6d14fb4dc4d41bab9aeb3283b3743`
- observed compile errors: nonexistent `mkv.Attachment.Description` field in implementation and tests
- deduplication: searched UIGS-Foundry for pinned-dependency/API-model/source-injection mismatch guidance; no direct duplicate found

This Bug record is evidence. It is not Canonical.
