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

## New exact Chromium evidence and bounded repair (2026-10-14)

- [Chromium run 38512726435](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38512726435), head `8054d02159b030a850dc7c323ecb4a153c91810c`: **Node/unit success, build success, E2E failure** at previously known sequential-task #11. Cancel/restart #10 now passed. Independent native `ffprobe` again found the second task's subtitle title `English · ASS` instead of `Second Task`.
- [Chromium run 38513161769](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38513161769), head `400ee90966e1ccc16a6a6dfc881bce17fb4c9184`: Node/build success; scenario #10 passed and #11 still failed with the same final-MKV title mismatch. Clearing stale subtitle form during pending inspection was **not sufficient**.
- A closer inspection of the actual pre-mux authorizer found that `externalAssetPendingTaskRebind` catches `EXTERNAL_DOMAIN_INVENTORY_CHANGED` and calls `syncNewTrackState()`, which can re-infer subtitle title from the filename **after the user authored the new task metadata**.
- Bounded source-only repair head `35411ad3a9976ecd9e0881610cc2231efdde7bee`: on inventory-only rebinding, verify all currently chosen audio File refs and subtitle File/sidecar refs exactly match the existing edited executor rows, and then call `refreshExternalAssetAuthority()` instead of `syncNewTrackState()`. If the sources differ, refuse the rebind rather than carrying old fields into a new File. No FFmpeg writer, Chapter/Tag/UID or batch implementation changed. New head [Chromium workflow 38514430477](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38514430477) was **in_progress** at last observation, so the bug remains Pending.
- The following Batch Recipe v2 branch [#135](https://github.com/11576865/MKV-Fast-Muxer/pull/135) separately carries the same bounded correction to avoid reintroducing the old title clobbering during stacked integration. Neither branch may be reported merged/green from these provisional results alone.

This strengthens the original separation: an inventory-only mutation (new font/picker reference) may require rebinding a domain owner, but **must not recreate track rows and re-infer editable metadata** if the current exact File and sidecar references already agree. An unapproved different File must still fail closed. Record Bug only; no Canonical promotion from repeated failures.
