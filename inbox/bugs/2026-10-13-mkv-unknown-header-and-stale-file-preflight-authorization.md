# Bug: unknown media headers must not bypass a preservation gate

Date: 2026-10-13
Status: **Bug / P1 code-review finding with corrective PR; exact-head Chromium regression Pending**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/108
Related Candidate: `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md`

## Observed code-level defect (not a confirmed media-loss reproduction)

Codex review at https://github.com/11576865/MKV-Fast-Muxer/pull/108#discussion_r4254474086 identified that a source header with `container='unknown'` had been classified as positively *not Matroska* in the new UI readiness preview. The old runtime path gated preservation checks only when the cached header identity was `matroska`/`matroska-webm`, so a transient unreadable header for a real hazardous MKV could skip both gates. This is a **credible possible authorization bypass** from source-shape analysis; no independent physical MKV loss through this precise read-error path has been demonstrated.

## Independent regression during Round 5

A full real-Chromium E2E on [run 38342696206](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38342696206) timed out after replacing previously invalid fonts with a valid font. It showed an integration problem with readiness and input recovery. The exact causal mechanism was not established from the initial timeout alone. Instrumented browser diagnostics were committed and later source-scoped readiness refreshing/resniffing logic was added. Do not claim this issue resolved until the exact-head full E2E passes.

## Correction submitted; Pending verification

In product PR #108:
- Only **positively identified non-Matroska** types (`iso-bmff`, `mov`, `webm`) avoid the Matroska-specific preview; `unknown` remains on the fail-closed path.
- At actual mux authorization, `sniffFileContainer(video)` reads the **exact current source** again. Unknown or cached-versus-actual container mismatch refuses to start the writer. A File object replacement during preflight is refused even when name/size/lastModified are identical.
- The earlier direct `inspectMatroskaPreservation` and source-structure hard refusal remain mandatory.
- Chromium regression submitted: invalid EBML bytes under a plausible .mkv name must disable Mux in the UI and be refused even when an event is dispatched programmatically. Existing valid-font recovery E2E also remains.

Reusable failure mode: **unknown ≠ negative evidence**, and a cached filename/size/timestamp identity must not be a separate authority for a destructive operation. UI safety and executor authorization require independently checked source identities. Preserve the full test oracle; do not treat a green build as a media oracle.

No Canonical promotion. Pending final exact-head Node/Chromium outcomes and source/branch hashes.


## Final resolution evidence and test-harness lessons (2026-10-13)

**Correction accepted in scoped product code; closed by verified merge**, PR #108 exact head `c0ebc77bdbb1db23c6519b0e1d1dd970044b4dad`, main merge `5b98af3af17269add441c7571d39009848b2e604`.
Full Chromium [run 38344211420](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38344211420): **success**. Node/build [run 38344211490](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38344211490): **success**, 369/369 Node tests. The browser log expressly confirms recovery from invalid fonts (`Scenario 13 PASS`), from invalid external audio (`Scenario 9 PASS`), and both high-risk/unknown-header source refusals.

Two additional testing/process observations arose during the fix:
1. An actual **disabled native button** can suppress a synthetic `click` even if a test dispatches the event. That does *not* exercise runtime authorization. The hard-fixture browser test now deliberately enables the DOM button **only inside the test environment**, synchronously clicks it, and verifies the independent executor still refuses the dangerous source. The source inventory scan must finish first, or `isBusy()` may correctly short-circuit before the intended authorization path.
2. Introducing an awaited new-source security check after a previous failed task caused a stale error string to remain visible long enough for the existing invalid-audio recovery oracle to report a false continuation failure. The executor now publishes a synchronous **new-task preflight** status *before* the await. Tests remain unchanged as behavioral oracles.

The earlier potential unknown-header bypass was a verified **code-level P1 risk**, not a demonstrated loss through injected failed header reads. The independent Chromium fixture proves rejection at the repaired boundary. This Bug is **resolved for the tested flows**; avoid expanding that claim to all EBML forms or devices. No Canonical promotion.
