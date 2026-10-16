# Observation: Attach per-object output evidence only through an exact source-and-plan identity gate

Date: 2026-10-16
Status: Observation — source changes committed on main, focused logic checks passed; exact-main full CI and browser artifact still pending
Product: https://github.com/11576865/MKV-Fast-Muxer
Product increment: 软封0.1017版本

## Observed integration gap

The production app independently audited a finished MKV with ffprobe and compared preserved original Matroska attachment FileData bytes against the source via SHA-256. However the object-centred workbench showed attachment edit intentions without a clear per-object mapping to these existing result fields. Users could see that *something* passed in a global audit panel but not which original attachment's name/MIME/bytes were confirmed, which requested exclusion was observed in the final inventory, and which cases remained unresolved.

## Bounded implementation

- New pure `source-attachment-delivery-evidence.js`: source-scanned attachment index and original/intended names are execution-time immutable snapshots, not new write owners. For included objects, only unique independent EBML payload audit observations (with real digest and output inventory match) qualify as `filedata-verified`. For exclusions, only a passing complete output ffprobe audit plus absence of the original filename in the actual attachment inventory qualify as `absent-in-probe`. Missing output, mismatches, duplicate source/output names, unknown identity or unverified payload remain `unavailable`.
- Keep UID and TagTargets linkage and user-side disk persistence expressly **not verified**, even after byte or output inventory success.
- Store summary in the actual generated mux report's audit object and present it in the existing output evidence panel.
- Display per-attachment completion badges only when the execution's **exact File reference** is still selected and the actual current mux plan is identical to the output report's planned run. Switching files (even same display metadata) or making a further edit revokes inline assignment of old proof.
- New unit negative cases, existing real-fixture E2E report assertions for rename + exclusion, and an output evidence UI projection test; exact-head full workflow verdict has **not** been independently retrieved.

## Reusable pattern

Proof has at least three separable axes:
1. **Object identity**: source File instance, scanned source index, origin and destination names, and collision safety.
2. **What was proved**: original payload bytes independently recovered, an output name absent in a scoped inventory, structural references, or durable save — these are not synonyms.
3. **Freshness**: an actual output can be valid but no longer correspond to the current editable plan.

A global green status alone cannot authorize per-object green badges. Project per-object evidence only after both the scoped measurement and identity/freshness gates pass. If any constituent evidence is missing, render unavailable rather than inferring success.

## Dedupe and limits

Foundry's `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md` already documents **how** to independently falsify roundtrip preservation using a separate reader. `inbox/tests/2026-10-12-r02-nonplayback-matroska-png-attachment-independent-oracle.md` handles one standalone attachment-only oracle. Neither records the **UI projection from existing finished-output evidence into live user-object identity with strict plan freshness**. This is a narrow Observation, not a Canonical upgrade, and does not claim the new real-browser E2E has completed.
