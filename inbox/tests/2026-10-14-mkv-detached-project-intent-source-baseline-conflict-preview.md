# Test: detached ContainerProject edit-intent baseline conflict preview

Date: 2026-10-14 (+08:00)
Status: **PENDING exact-head browser CI and merge**
Project: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/124
Baseline main: `334596a86c6dd9091d5a5446c9db01132e16235e`
Initial head: `9ea98b721cb098b2a53494f0d5ce9e56d1e63581`

## Concrete engineering proof

The previously merged PRs #121–#123 established detached project import, bounded actual-file SHA-256 versus editable JSON, and **internal** edit-intent chain consistency. These do not prove that a recorded pre-edit field still matches the user's CURRENT, freshly inspected source object. A naïve replay could silently overwrite a different value.

PR #124 adds a read-only source/old-value comparison:
- Audit the untrusted edit-intent chain before checking it; reverse-walk the consistent final object data to reconstruct the earliest `from` value for each touched object field; coalesce repeated field edits into one `before -> after` proposal.
- Only report an inspected field as `baseline-matches` after original source identity matches, full source digest was independently verified for the **same actual File reference** by the existing UI flow, and current source tracks are scanned. Distinguish missing objects, changed object identity/type, external unbound objects, changed current field value, no hash, source drift and unscanned container.
- A green read-only comparison **still sets** `changesApplied=false`, `executionAuthorized=false` and never changes the legacy editor, output composition or container writer.
- Chromium checks imported coherent one-change draft remains blocked both before SHA verification and after a SHA match **without** verified track inspection. Node tests cover repeated field edits, old-value conflict, forged final values, unbound external objects, source identity drift and no-edits.
- Product control is a disclosure with explanatory text, not an executable “restore” action.

## Knowledge dedup and boundaries

- `inbox/tests/2026-10-14-mkv-detached-project-intent-chain-semantic-review.md`: **earlier PR #123** proves only edit-chain internal consistency. This distinct Test adds comparison to actual inspected CURRENT object baselines and hash gates; not a duplicated Candidate.
- `inbox/tests/2026-10-13-mkv-container-project-import-source-drift-review.md`: earlier PR #122 proves source digest equality, explicitly not previous/edit ownership.
- `inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md`: saved semantic roundtrip for another product, not this detached Matroska source/field conflict.
- No Canonical change or inferred general authorization.

**Unverified:** project actor/authorship, user consent, arbitrary MKV preservation, writer eligibility, actual replay/undo in live editor, cross-device behavior and full P0–P6 release. PR must pass exact-head full browser CI and post-merge main CI before Test is marked PASS.
