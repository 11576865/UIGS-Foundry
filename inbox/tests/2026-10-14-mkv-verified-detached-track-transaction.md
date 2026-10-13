# Test — MKV verified detached-track transaction (P1)
Date: 2026-10-14
Status: Pending CI (not yet accepted)
Product: https://github.com/11576865/MKV-Fast-Muxer/pull/125
Submitted head: ad07908fd8e84aa4f00c71ce836ddb488218fef6

## Concrete addition and provenance
The predecessor [read-only comparison test](2026-10-14-mkv-detached-project-intent-source-baseline-conflict-preview.md) ended with changesApplied=false. New PR #125 adds the distinct, explicitly consented mutation boundary in the **existing live trackState**, without attaching file permissions or invoking a writer.

- Export real source-scan-to-current-editor audio/subtitle deltas, including true empty titles and disposition flags; normalize unknown source size (size:null) when constructing the derived project.
- Validate imported edit chain; require exact bound File, bounded full SHA-256 equality, scanned source/track identity, current old-field agreement, selective-edit mode, supported field and separate consent.
- Prepare every touched track, precommit-compare every track, then atomically apply the whole edit set; reject any conflict without partial state mutation. Supported: source audio/subtitle inclusion, title, language, default, forced; no arbitrary chapters/tags/attachments/order.
- A source-scoped inverse only succeeds when all touched rows still match their postimage. Subsequent user changes block undo.
- Added Node tests and real Chromium export -> import -> hash proof -> apply -> undo/reapply -> actual MKV output audit scenario.

## Evidence and gates
Implementation source + tests and product draft PR exist. **Exact-head unit/build/Chromium CI, real output results, merge and postmerge main validation: Pending.** No published PASS is claimed. Full EBML preservation, general writer eligibility, actor authenticity, cross-browser and field compatibility remain unproven.

## Knowledge dedup
The #124 Test and preceding import/SHA/intent-chain Tests covered read-only prerequisites. This record adds the compare-and-swap/atomic replay and scoped inverse contract, not a duplicate of the read-only case. Do not promote to Canonical on one implementation.
