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
