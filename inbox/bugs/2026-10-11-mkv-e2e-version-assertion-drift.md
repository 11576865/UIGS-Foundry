# Bug: hardcoded E2E report-version expectation became stale after provenance fix

Status: **Bug / CI-reproduced; repair submitted, CI pending**
Lifecycle: validation-pending
Date: 2026-10-11
Source repository: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/70
First failed workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38116582111
Repeated failed workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38116832733

## Direct evidence

The production mux report had an outdated application version `1.2.0`
while `package.json` was already `1.2.2`. PR #70 repaired the
report value and added a Node source-to-manifest check, but
`tests/e2e/browser-mux.e2e.mjs:128` still asserted the old literal.

The real Chromium/FFmpeg/browser E2E successfully executed several
content-first UI and MKV container-tree scenarios, then failed on the
first multi-track scenario's report assertion:

```text
AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
'1.2.2' !== '1.2.0'
at scenarioMultiTrack (.../tests/e2e/browser-mux.e2e.mjs:128:12)
```

This was a **stale test oracle**, not evidence of corrupt mux output
or an FFmpeg failure.

## Repair and verification contract

The production E2E assertion was changed to load the version from the
package manifest and compare the report's `application.version` to that
authoritative value. This preserves actual downloaded-report
verification without duplicating a version constant in the test.

Source commit: `f0a5233b1f11f72c7507505509e1d522d6f76c77`.
The replacement CI run is Pending at time of intake; do not claim green
until the exact new head passes.

## Reusable finding

When fixing provenance/identity metadata, audit and update all
independent test oracles that embed the old value. Prefer an
authoritative manifest-derived expected value rather than another
hardcoded copy, while still checking the real serialized artifact.
Do not weaken or remove the output assertion to force CI green.

This is an observed bug and repair in one repository. No Canonical
promotion is warranted. It is separate from the existing general
`TEST.CONTAINER_SEMANTIC_AUDIT` entry and from the earlier chapter
cardinality observation.
