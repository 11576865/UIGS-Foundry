# Observation: Composition display keys can collide even when live resource grants are distinct

Date: 2026-10-23
Status: **Observation / code-level defect and submitted bounded repair; exact-head CI Pending**
Product: [MKV-Fast-Muxer](https://github.com/11576865/MKV-Fast-Muxer)
Product baseline: 软封 0.1027 / main `585f4e8e8473e09d0a4c7fa63d66368d9a9f9870`
Product repair: [PR #182](https://github.com/11576865/MKV-Fast-Muxer/pull/182), branch `fix/softmux-s13-composition-collision-20261023`, head `17cd2754d7345bfddaae38d6ae25398ce15e1e91`

## Source-grounded defect

The existing `buildOutputComposition` produced row IDs such as `external:subtitle:${file.name}|${file.size}|${file.lastModified}` and `font:${file.name}|${file.size}|${file.lastModified}`. Multiple intentionally selected media resources with identical filename/size/mtime, including intentionally repeated *same* File, could have identical visual row IDs, active selection keys, and downstream document projection identifiers.

The workbench's `activateCompositionTrack` then used `.findIndex(row => outputCompositionFileKey(row.file) === target.fileKey)` to route to an external editor. When two rows shared metadata, the second row could select the first editor field. The intake inventory focus similarly took the first metadata match. This is a UI object-routing defect, not evidence of byte-level mux corruption; no Chromium reproduction has yet been claimed.

## Bounded change submitted

- `src/output-composition.js`: retain the first legacy row ID, append a duplicate-occurrence suffix to subsequent same-key external audio, external subtitle and font rows; attach the **current live row index** to each target. The index is a presentation occurrence, not a persisted or cryptographic resource identity.
- `src/main.js`: validate the selected index against the current live row before navigating. When stale, clear selection rather than sending the click to an arbitrary first metadata match. Inventory focus uses exact `entry.file === targetRows[matched].file` reference identity.
- `tests/output-composition.test.mjs`: test distinct same-metadata Files and intentionally repeated same File, unique IDs, deterministic re-projection and indices.
- `tests/composition-workspace.test.mjs`: enforce index-bound routing and explicitly exclude metadata-first `findIndex` selection.
- Execution and persistence contracts, writer admission, source digest/permission checks and product version are unchanged.

## Evidence and pending gates

Code inspection demonstrates the preexisting duplicate-key possibility and first-match selection path. The submitted diff is four files. **Node/build/Chromium exact-head results and real-device acceptance have not been observed in this intake**. PR #182 is not a verified merged fix; preserve `Pending CI` until a specific run and SHA confirm it. The collision scenario is an additional coverage target, not an S13/1.0 completion claim.

## Dedupe with existing Foundry records

- [2026-10-14 external asset live-domain exact File and form epoch Case](../cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md) already addresses **authoring metadata propagation** under file re-selection and asynchronous DOM mounting.
- [2026-10-16 stale same-metadata output evidence Observation](2026-10-16-softmux-output-evidence-stale-same-metadata-source-file.md) already addresses **historical artifact applicability**.
- This Observation adds the distinct **same-session output composition multiplicity and editor-target routing** failure mode. Neither existing item is duplicated or superseded.

## Transferable hypothesis, not Canonical

A display reconciliation key derived from `name|size|mtime` should not be presumed unique within a multi-object UI. Distinguish repeated occurrences, validate that an interaction still addresses its current live row, and keep exact browser File object authority separate from both row position and file metadata. Stronger permanent identity, async list-reordering semantics and end-to-end browser behavior require separate evidence. One implementation does not justify automatic Canonical rule changes.
