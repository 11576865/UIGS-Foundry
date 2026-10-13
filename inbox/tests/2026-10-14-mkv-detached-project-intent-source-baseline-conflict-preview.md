# Test: detached ContainerProject edit-intent baseline conflict preview

Date: 2026-10-14 (+08:00)
Status: **PASS — exact-head Node/build, full Chromium E2E, named browser artifact, PR #124 merged; post-merge main CI pending**
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


## Verified exact-head evidence and merge

- Exact tested PR head: `9ea98b721cb098b2a53494f0d5ce9e56d1e63581`.
- [Node/build run 38438759648](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38438759648): **PASS 472/472 Node tests plus production build**.
- [Full Chromium E2E 38438759640](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38438759640): **PASS**, explicitly includes five-step source/import workbench, P0/P1 safety and delivered P3 dynamic ASS frame proof.
- Downloaded and independently inspected named CI artifact `five-step-container-recipe-workbench-evidence` ID `11834935339`: **five files** (real browser-exported project and recipe JSON; 1440, 1024 and 390 PNGs). Original downloaded project is still only **one header-level** object with `base.mp4` SHA-256 `a78a0c371584ab404b90c9b7d9b6807550506cedcad8b991013a2cda859f520c`, not a verified typed track or actual edited source. E2E separately fabricated a coherent one-event imported draft to test conflict UI. Both 1440 and 390 images were opened: they show read-only `是 → 否` and explicit baseline conflict `当前真实轨道尚未扫描`, **even after current source SHA equality**. This correctly refuses conflating byte equality with track/object verification.
- PR [#124](https://github.com/11576865/MKV-Fast-Muxer/pull/124) squash-merged into `main@6d3f88a4ae7c0c67c7c058c3422ac4e32213b235`.

Still **only bounded, read-only comparison**. No automatic edit replay, signed actor provenance, write eligibility, completed P1 single authority or Canonical promotion. Post-merge independent CI still a separate closure condition.
