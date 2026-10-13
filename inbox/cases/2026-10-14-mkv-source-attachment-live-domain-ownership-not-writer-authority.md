# Case: Live domain ownership of source attachments must not impersonate Matroska writer authority

Date: 2026-10-14  
Status: **Case / implementation submitted; exact-head integration CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#130](https://github.com/11576865/MKV-Fast-Muxer/pull/130), direct-to-main consolidated P1 advanced order plus source attachments  
Base: `main@e993c66f5c2ede9e76d97773bd5e0b40d796a0c2`, merged #128.

## Gap

Audio/subtitle track state had moved to a live immutable `ContainerProject`, and advanced source flags/order were implemented on the preceding branch. Yet actual source attachment controls still had distinct direct mutable writes: central object inspector, original attachment table, preserve checkbox, bulk keep/drop and metadata reset. A read-only `ContainerDocument` could display these changes but was not the write owner. At the same time, Matroska AttachmentUID / targeted Tag relations and unsupported EBML mean that making a semantic attachment edit **does not** authorize a remux or certify byte-preserving output.

## Concrete bounded migration

PR #130 adds source attachment `include`, `filename` and `mimetype` to the same live source-bound immutable `ContainerProject` editor session used by audio/subtitle tracks. It maps **actual scanned** attachment objects by stream index, type and exact original ffprobe stream object reference, and binds the session to the identical browser File that completed the scan. Per-action commands validate all proposed edits, MIME/name lengths, disallowed path/control characters, duplicate identity and stale executor state before constructing the next immutable project. The already-validated legacy `trackState.attachments` is synchronously updated only *after* all validations succeed. No source or output File is written by the command, and no second mux writer appears.

All actual user-facing entry points now go through this command: source-tree inspector, original list text fields and checkboxes, preserve-attachments switch, keep/drop all and reset metadata. The existing FFmpeg selective output and P0 safety/preflight continue to decide whether media write is supported. The command receipt explicitly says `sourceUidRelationsPreserved: 'not-proven-by-domain-command'`.

**Portable state distinction:** detached project `objects` can show modified attachment names/MIME and exclusion, but the current `editIntents` construction/verified replay does not yet support a safe UID-aware source attachment baseline. The app must warn on export rather than imply that those changes will automatically restore. The analogous live-only track-order boundary is recorded separately.

## Evidence

- Focused Node regressions added for immutable attachment field updates, status, batch multi-field atomicity, invalid field/MIME and traversal-like filename refusal, source File/ffprobe object drift, legacy owner bypass, preserve-all gating, exclusions and 150 metadata keystrokes under bounded domain history.
- Browser E2E added: actual two-attachment MKV → rename first, change MIME, exclude second → project export confirms current state and visible non-portability warning → existing FFmpeg mux → independent native ffprobe confirms retained attachment count/name/MIME, and original source bytes remain unchanged.
- Isolated real-module execution passed attachment name/MIME edit, rejection of control-character MIME and >100 edits with bounded immutable history; changed JavaScript source/test syntax checks passed. **Full exact-head Node/Vite/Chromium for PR #130 is Pending**, so there is no claim of green integration or device acceptance yet.

## Scope, dedup, and status

- Extends earlier source-track ownership Case `inbox/cases/2026-10-14-mkv-live-domain-track-authority-with-legacy-mux-projection.md`; unlike it, this Case is specifically about attachment name/MIME/include state and AttachmentUID safety.
- Complements P0 `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md`, which concerns writer authorization and independent structure preservation, **not** editable domain state.
- No change to Canonical. Next corroboration: complete exact-head CI, verified attachment UID/target Tag relation preservation, and a separate conflict-checked attachment edit-intent replay contract. Chapter/Tag issue #77 remains unresolved.
