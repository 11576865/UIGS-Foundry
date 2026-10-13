# Test: detached MKV ContainerProject edit-intent internal coherence (not replay)

Date: 2026-10-14
Status: **PASS — exact-head and separate post-merge main Node/build/deploy/complete Chromium, inspected artifact**
Product: `11576865/MKV-Fast-Muxer`
Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/123
Base main: `7e1274a70748810463129051e99529dbb1b62fa3`
Initial tested head: `1df4e11cfb62f768f886d9eed85bd353e95bec0b`

## Purpose

After independently passing PR #120 versioned detached ContainerProject export, PR #121 strict read-only re-import and source/object drift comparison, and PR #122 bounded SHA-256 source-byte comparison, a domain-specific integrity gap remained: imported edit-intent records could have individually plausible typed `from/to` fields, yet disagree with the serialized final object state or with the previous edit of the same field.

This P1 Test verifies **internal consistency of untrusted JSON**, not author provenance or authorization. A new deterministic pure function reverse-walks the saved final objects: for each intent, require final `to` to equal the current semantic state, undo to `from`; this also checks intermediate chains. Refuse duplicate/out-of-order revisions, unsupported kind-specific metadata fields, impossible numeric/boolean types and no-op records. Preserve legitimate Undo revision gaps.

The existing strict parser calls this audit before accepting imported drafts. Actual browser UI shows at most 12 validated semantic changes as a keyboard-accessible **read-only** disclosure with explicit warning that the history may be fabricated. Actual Chromium E2E must import both an internally coherent user-visible Include change and a deliberately contradictory saved-final-state draft: one displays an inert preview, the other is rejected, without changing source File, output, backend or job queue.

## Dedup and source references

- `inbox/tests/2026-10-13-mkv-container-project-import-source-drift-review.md`: prior import drift/source-byte evidence and scope. This P1 Test adds **intent-chain semantic consistency**, not duplicate file-identity verification.
- `inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md`: existing general persistence proposal; current entry is product-specific Test.
- `inbox/candidates/2026-10-03-batch-intent-vs-local-draft-ui-contract.md`: source-of-truth distinction; current detached read-only history must not be mistaken for committed local editor intents.
- PR #120/#121/#122 are independently merged and previously accepted.

## Fail-closed and scope limits

- An attacker or user can fabricate a **fully coherent** edit history and checksum. This test never claims the editing truly occurred or that the author is trusted.
- A document source `sha256` is a commitment supplied by that editable JSON, **not a signature**; previous byte match does not validate imported object's old track identity, order or edit semantics.
- Import/audit is always non-executable: `authorshipProven=false`, `changesApplied=false`, `executionAuthorized=false`, `writerEligible=false`.
- The production editor remains legacy write authority; full P1 editable domain migration, safe arbitrary EBML writer, device/large-file and P5/P6 exit criteria remain incomplete. Do not promote Canonical from this single case.

**Pending proof**: exact PR head all Node/build and full browser E2E PASS, inspected artifact screenshot(s); after merge confirm separate main-push checks.

## Verified exact-head acceptance and merge

- Exact PR head: `1df4e11cfb62f768f886d9eed85bd353e95bec0b`.
- [Node and build 38435603584](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38435603584): **PASS 464/464**, production build.
- [Complete Chromium E2E 38435603563](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38435603563): **PASS**, explicitly logs five-step source/import/recipe workbench and existing P0/P1 source preservation, P3 four-frame actual-MKV ASS/libass evidence; browser test asserts coherent detached inclusion edit preview plus rejecting contradictory final snapshot.
- Inspected actual CI artifact `five-step-container-recipe-workbench-evidence` **ID 11832582920**: five items (source `container-project-v1` JSON, `batch-recipe-v1` JSON, screenshots at 1440x900, 1024x768, 390x844). Exported draft JSON contains **one header-only source object and zero intents**; browser *separately creates a valid single-intent imported copy* for read-only visual audit. Source hash field exists. Screenshots at 1440 and 390 were opened, showed the imported one-line `是 → 否` change and explicit non-authorizing notice. Not an actual editing operation.
- [Merged PR #123](https://github.com/11576865/MKV-Fast-Muxer/pull/123) squash main commit `334596a86c6dd9091d5a5446c9db01132e16235e`.

**This evidence demonstrates internal semantic self-consistency only, never history/authorship authenticity or safe replay.** No Canonical change.

## Post-merge main independently green

Squash merge commit `334596a86c6dd9091d5a5446c9db01132e16235e` was independently verified as current `main` exact SHA.

- [Main Node/build and GitHub Pages 38436633075](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38436633075): **PASS**.
- [Main complete Chromium E2E 38436632889](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38436632889): **PASS**; actual logs explicitly include `Five-step recipe export/import and capability truthful UI PASS`, `P0/P1 pre-mux safety, unknown-header refusal and source-switch freshness PASS`, `P3 dynamic final-MKV 4 subsecond snapshots and 3 effect negative controls PASS`, and `All browser E2E scenarios PASS`.

No Canonical promotion. Distinguish schema coherence from author provenance, source attestation and any writer eligibility; full P1–P6 theoretical release criteria remain open.
