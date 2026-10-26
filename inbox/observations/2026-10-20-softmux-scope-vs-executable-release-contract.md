# Observation: Strategy + scope + stage gates are not an executable product release contract

Date: 2026-10-20  
Status: **Observation / single-project owner feedback + documented proposal, not Canonical and not runtime-validated**  
Source product: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)  
Product proposal: [PR #160](https://github.com/11576865/MKV-Fast-Muxer/pull/160) and `docs/softmux-1.0-product-acceptance-contract-20261020.md`  
Reference: `main@dc481b9c784e9be69e50544ac0fecafd157c6288` (before PR #160).

## Trigger

The user challenged softmux 1.0 as still "not concrete, ambiguous" after approving a **bounded professional Matroska workbench (scope B)** and an approximately **1 GB** first-release file target. Existing product documentation separately captured:

- D-01—D-10: approved strategy / product identity;
- R0—R6: engineering/process and release quality gates;
- scope B: permitted capability boundaries and excluded universal EBML editing;
- 44 legacy features and 57 historical acceptance items.

None alone provided a bounded, easily falsifiable **customer-visible action → input → output → refusal → independent verification** catalogue. A loose schedule estimate (5–8 weeks, later withdrawn) also substituted duration for an acceptance denominator.

## Reusable observation / proposed test

1. Before declaring a major version well-defined, require three separate source-of-truth layers: **product purpose**, **first-release capability envelope** (including size, platform, operation and negative claims), and **frozen externally observable acceptance tasks**.
2. Each release task should explicitly enumerate source fixtures, user-visible entry/action, actual writer/backend, expected artifact and independent readback, failure mode, operating environment, and supporting exact-commit evidence.
3. A capability envelope is **operation-dependent**. A 1 GB ordinary mux target does not promote a 60 MiB research EBML editor or a 64 MiB structure-inspection writer to 1 GB. Distinguish read-only import/inspect, ordinary remux, bounded byte edit, save and native validation.
4. Negative promises belong in the contract: unsupported object mutation, unknown structured metadata, missing source identity or no File permission must fail with a specific diagnostic rather than silent loss or fake success.
5. Existing green CI, branch/PR counts, design docs and scope decisions are not a substitute for a frozen testable release denominator. Conversely, historical `unassessed` ledger entries are not proof that functionality is absent.
6. Do not silently convert an assistant-authored acceptance proposal into a user-approved Canonical product target. Track user-approved scope separately from suggested thresholds, and hold unsettled choices (source-only vs both source+output 1 GB) for owner review.

## Specific action

Product PR #160 added proposed S01—S14 user scenarios and N01—N06 explicit exclusions, then cross-linked the acceptance proposal from the pre-existing 1.0 release contract. This is a **documentation commit on an open PR**, not 1.0 functionality, automated acceptance, user approval of each scenario, or a passed 1 GB media benchmark.

## Dedupe / relationship

Foundry search and file review found:
- `inbox/candidates/2026-10-14-product-block-delivery-over-pr-fragmentation.md` — feature-block delivery vs micro-PR metrics, does **not** define first-release scope+acceptance separation;
- `inbox/candidates/2026-10-14-agent-generated-next-units-goal-drift-guard.md` — root-goal traceability and generated work queue control;
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` — the composed MKV as primary interface object;
- `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` — runtime capability classification by operation/file size/browser/output.

This entry connects their concerns at **major product-version specification clarity**, rather than promoting or replacing any of them.

## Evidence limitation

This is based on one user evaluation and a proposed product-contract change. It has not been tested whether writing S01—S14 improves actual delivery speed or reduces acceptance disputes, and no runtime 1 GB pass was observed. Retain as Observation; do not promote Canonical from a single occurrence.

## 2026-10-27 implementation-backed continuation: executable release-evidence gate (pending exact CI)

Product [PR #205](https://github.com/11576865/MKV-Fast-Muxer/pull/205), baseline `main@36f71dc9ae80a4e0b463de51d2f3aa2edae64c02`, candidate head `5dba60e3ad0f2c57730d3a0be806bd514ad5c5be`, turns the previously **proposed** S01–S14 release-contract distinction into a real fail-closed pre-release CLI and GitHub manual workflow:

- [`docs/softmux-1.0-release-evidence.json`](https://github.com/11576865/MKV-Fast-Muxer/blob/feat/softmux-s14-evidence-gated-release-20261027/docs/softmux-1.0-release-evidence.json) retains 14 MUST IDs and 57 exact historical R/T/B/S/U acceptance IDs, including the original `partial/unassessed` states. Historical Node/Chromium green does NOT automatically change a release result to PASS.
- [`docs/softmux-1.0-legacy-capability-ledger.json`](https://github.com/11576865/MKV-Fast-Muxer/blob/feat/softmux-s14-evidence-gated-release-20261027/docs/softmux-1.0-legacy-capability-ledger.json) records all original L-001–L-044 items from the 2026-10-12 owner decision, with migration disposition proposals and initially UNASSESSED independent results. It is a migration proof denominator, not an assertion of 44 missing functions.
- `npm run release:audit` validates full denominator shape and reports release blockers without preventing development builds. `npm run release:gate` separately checks a frozen exact 1.0.0 SHA, row-level independent receipts, actual target device evidence for S12/S13, deployed site and tested rollback evidence, and live GitHub Actions successful runs with the same commit. The manually dispatched workflow checks out the user-specified exact commit.
- New Node negative tests check deletion or duplication of legacy IDs, forged receipts or SHA, wrong CI commit, fake tablet evidence, unapproved retirement and improper history promotion. Passing static gate checks is **not** equivalent to authenticating manually entered URLs or actually running an OS-level device/roll-back test.

**Epistemic state at this intake:** product PR #205 exact-head Node/Pages CI has completed successfully; full real Chromium E2E and S12 specialized large-media workflows were **running**, so do not claim release-gate merge or acceptance yet. Even if all three pass, product 1.0 remains **BLOCKED** while contract S01–S14 and physical-device evidence are unresolved. This updates this existing Observation rather than creating a duplicate Candidate and does NOT modify Canonical.

**Foundry validation and lifecycle:** This Foundry PR is Pending unless its own current validator passes and merge is actually observed. Previous Foundry global validation had failed on pre-existing Bug intake files' missing `Lifecycle` fields; do not silently assign another project's defect to this Observation.
