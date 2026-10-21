# Test candidate: S09 wrong-source rejection and mixed source-track/attachment inverse CAS

Date: 2026-10-21
Status: **Scoped S09 Test PASS and merged to main; aggregate S09 still PARTIAL; NOT Canonical**
Product: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/169
First submitted head: `8b2ffb1023ea4043fe3992d39295fa8a95ecd9ff`
Reference: `docs/softmux-1.0-product-acceptance-contract-20261020.md` S09.

## Deduplication
- `inbox/cases/2026-10-14-mkv-verified-source-attachment-intent-atomic-cross-object-replay.md` already establishes source-track and attachment domain atomic replay at module scope; this is **not a new design rule**.
- `inbox/tests/2026-10-14-mkv-verified-detached-track-transaction.md` already treats byte digest/old-value CAS and explicit consent.
- `inbox/tests/2026-10-21-softmux-s09-two-draft-cross-reload-real-output-pending.md` already records the completed positive Chromium multi-draft reload and native output acceptance.
- Distinct need: one **actual modern object workbench** exercise combining a deliberately wrong **real** MKV, a user-edit old-value conflict, a deliberately conflicting mixed **inverse** and a genuine independent native final-output audit. These must be attempted in the same UI product path. No new Candidate, no Canonical mutation.

## Submitted adversarial acceptance path
1. Current object workbench public source intake, real `source-with-attachments.mkv`; change original audio title + original source attachment filename via same public Inspector; export one derived ContainerProject JSON with complete source SHA-256 and two explicit edit intents.
2. Reload, select `source-multitrack.mkv` instead. Verify digest `digest-mismatch`, restore button disabled, no title contamination of that user's current executable plan, original bytes unchanged.
3. Reload, re-import same detached draft, reselect correct File; verify title/attachment scan baseline unchanged and complete SHA-256 `digest-matches-draft`. Digest match alone cannot enable applying.
4. Edit source audio to a third local value; old-value collision in conflict preview must disable import replay, leaving attachment unchanged.
5. Restore local baseline and explicitly confirm, apply combined source-track/attachment edit once. Change attachment again and invoke inverse. Expect **entire inverse refused**, so the audio remains in the applied state and user-updated attachment remains intact.
6. Reset attachment to just-restored value, explicitly run inverse, verify original audio/attachment states. This does not auto-authorize a redo; separately confirm and re-apply the plan.
7. Actually execute FFmpeg/Wasm and download MKV. Independent native `ffprobe` checks BOTH final original-audio title and attachment filename; original wrong/correct sources remain SHA-256 unchanged. Save machine-readable receipt and real MKV via CI artifact `s09-conflict-source-attachment-atomic-undo`.

## Evidence boundary
- Product PR committed, but **no exact-head green evidence yet**. Branch and created test do not prove existing safety logic passes.
- Scope: one fixture/current Chromium with real binary output; not a general project-wide atomic undo/redo stack, not automatic File access resurrection, not arbitrary EBML metadata write.
- If red, classify exact failing action against UI progressive disclosure/selection, scan authority, source proof or domain CAS before changing product/assurance code. Never delete strict security assertions just to turn CI green.

## First exact-head Chromium result (functional test head PASS)

- Product PR #169 head `8b2ffb1023ea4043fe3992d39295fa8a95ecd9ff`: [Browser E2E CI 39547270407](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39547270407) **completed success**. Chromium console prints `S09 source/attachment conflicts and atomic inverse + real MKV PASS` and `All browser E2E scenarios PASS`; S10 20 independently inspected real MKV batch also passed.
- Exact S09 adversarial artifact: `s09-conflict-source-attachment-atomic-undo`, artifact ID `12322730990`, contains exported JSON, actual remuxed MKV and bound hash/negative-assertion receipt.
- A separate candidate version increment to **0.1025.0** and README release note follows; product head `0fe780eeff528997281d0d3160a1387dfe0eef8a` is **Pending exact-head CI**. Do not treat the prior green run as final release-head evidence; no merge claim yet.
- S09 contract remains **partial**, because universal undo/redo coverage and device/UX testing have not been established. No Canonical changes.

## Final 0.1025 integration and precise evidence

- [PR #169](https://github.com/11576865/MKV-Fast-Muxer/pull/169) merged to product `main@b7d4a4fca5c3329e8654f90277f531a69f10f90f` using squash.
- **Accepted exact PR head:** `a2955febf6fe454b24ed7c9dd773dcbdecde1c73`. Full Browser E2E [run 39548135801](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39548135801) completed success; Pages build [run 39548135870](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39548135870) also completed success.
- Exact log: `S09 source/attachment conflicts and atomic inverse + real MKV PASS`; `S10 BATCH20: 20 real jobs / 20 independent MKVs, strict output audit and retention PASS`; `All browser E2E scenarios PASS`.
- Archived `s09-conflict-source-attachment-atomic-undo` artifact ID `12321869565` with real output MKV, original source project draft and SHA-256-bound negative/positive receipt.
- Deliverable product-version authority now `0.1025.0`; UI/mux report derive from the same package. This passes the narrow current-Chromium fixture case for wrong-source digest, old-value conflict and mixed inverse atomic refusal. It does **not** prove all possible old-value combinations, arbitrary device behavior, user-local save, or a general infinite-history undo/redo system.
- No Canonical modification. Follow-on 1.0 release gate remains separate S12 ≥1 GB physical run, S13 tablet device and S14 44 historical capabilities / 57 source scenarios review; S09 overall remains partial pending its unsupported-type and UX matrix.
