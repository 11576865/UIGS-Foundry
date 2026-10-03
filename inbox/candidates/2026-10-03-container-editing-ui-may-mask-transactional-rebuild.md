# Candidate: Container editing UI may mask transactional rebuild

Status: candidate
Date: 2026-10-03
Domains: workflow, reliability, file-formats, interaction-model
Evidence type: cross-domain design observation

## Summary

For many container and archive formats, a user-facing "edit inside the file" operation does not imply true in-place mutation of the binary container.

The UI may present:
- open container;
- replace/add/delete an internal item;
- save;

while the implementation safely performs:
- read/extract required entries;
- build a new temporary container;
- verify it;
- atomically replace/publish the result.

This interaction model appears in both media containers (for example remuxing an MKV after attachment changes) and compressed archives.

## Candidate rule

- distinguish **interaction-level direct editing** from **physical in-place binary modification**;
- prefer transactional rebuild when format structure, compression, checksums, indexes, encryption or recovery semantics make in-place mutation unsafe or impractical;
- the product may expose a direct-edit workflow if the implementation preserves source safety and result integrity;
- replacement should normally be staged and verified before overwriting the original;
- formats with solid compression, encryption, signatures, recovery records or complex central indexes may require rewriting much more data than the changed entry alone;
- do not promise constant-time or local mutation merely because the UI resembles filesystem editing;
- preserve metadata and unsupported format features explicitly or warn when reconstruction may change them.

## Scope

Applies to archive managers, media-container editors, package editors, document bundles, game-resource packs and similar compound-file formats.

## Provenance

- design discussion comparing MKV attachment remuxing with RAR/ZIP-style archive content modification
- evidence level: general engineering pattern; no Canonical change

This is a Candidate only. It is not Canonical.
