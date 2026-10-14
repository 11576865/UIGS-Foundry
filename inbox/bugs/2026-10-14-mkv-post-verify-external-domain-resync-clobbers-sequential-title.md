# Bug: Re-syncing a verified domain before mux can erase authored metadata in a later task

Date: 2026-10-14  
Status: **bounded production repair submitted; latest exact-head Chromium Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#133](https://github.com/11576865/MKV-Fast-Muxer/pull/133), repaired head `9fe7625993817c0193c8cde1e77e7b2a9e6964eb`.

## Independent exact evidence

After a prior cancel/restart inventory bug was addressed by explicit task-boundary rebinding, GitHub Chromium E2E workflow [38510905199](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38510905199) reported **scenario 10 PASS**. The next existing test, **scenario 11**, executes two sequential successful mux operations. In the second, the user edits subtitle title to `Second Task`; the independently `ffprobe`-inspected delivered MKV had default inferred title `English · ASS`, and Node assert failed at `tests/e2e/browser-mux.e2e.mjs:916`.

This is a real **final-output metadata regression**, not a test fixture typo, unrelated to Matroska Chapter/UID safeguards. Existing `executeCurrentMuxTask` first checked or rebound an immutable external-domain owner, then **unconditionally invoked `syncNewTrackState()` again** just before dispatching legacy mux. That extra re-inference could replace the current executor subtitle row (and edited title) even after the approved domain was coherent.

## Bounded repair

Commit `9fe7625993817c0193c8cde1e77e7b2a9e6964eb`:
1. If there is no current domain owner, build it from the active input once.
2. If a real new primary task has been explicitly selected, first **verify** the existing domain projection. If already coherent, preserve it and its edits; if and only if the inventory is stale (`EXTERNAL_DOMAIN_INVENTORY_CHANGED`), permit one bounded selection rebind.
3. Finally verify actual external audio/subtitle/sidecar/selected-font state and go straight to existing FFmpeg preparation; **do not unconditionally `syncNewTrackState()` after successful verification**.
4. Ordinary same-task source replacement/metadata bypass still fails closed, no persistent File grant or new writer is created.

The same exact source fix was included in dependent batch-v2 branch, commit `e3193aee38aa724e58edbc01e27599c7781c7cab`. Latest repaired head full Node/build/Chromium **PENDING**: do not report the bug closed until both scenario 10 and scenario 11 and the complete E2E suite pass.

## Deduplication and transfer hypothesis

Foundry Bug `inbox/bugs/2026-10-14-mkv-external-domain-cancel-restart-stale-file-inventory.md` covers stale FileList inventory after cancellation; this record covers **the opposite regression, over-eager resynchronization after a successful domain validation**. Older `inbox/bugs/2026-10-04-async-rerender-can-clobber-live-editor-values.md` covers general async rendering; this finding is specifically at a real mux authorization boundary and its evidence is the final file's lost user-authored title.

Potential transferable safety rule: when a bounded immutable editor is the write owner, a successful commit/validation is an execution-ready projection. Do not overwrite it with inferred defaults at the handoff boundary. Any exceptional rebind must be triggered by an explicit new-task identity transition and separately constrained. Bug level only; no automatic Canonical change.
