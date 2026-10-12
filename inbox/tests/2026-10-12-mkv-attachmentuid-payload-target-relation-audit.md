# Test: Matroska AttachmentUID-targeted tag must resolve to identical attachment payload after remux

Date: 2026-10-12
Status: **Verified, scoped green** — checked AttachmentUID target relation matched in actual browser remux
Product: `11576865/MKV-Fast-Muxer`
Merged PR: https://github.com/11576865/MKV-Fast-Muxer/pull/84 (main squash commit `0b2d2a502e015374043f0bf664fbacd2cc14b82c`)
Verified CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38220651710 (229/229 Node tests; full Chromium E2E PASS; `P0 attachment tag semantic relation: CHECKED_RELATIONS_MATCH`). Initial CI https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38212101317 was cancelled during slow apt downloads, before the experiment ran; it is not failure evidence.
Related P0 cases: `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`; `inbox/bugs/2026-10-12-mkv-browser-remux-nested-chapter-and-target-tag-loss.md`.

## New test dimension

A Matroska mux writer may legitimately **renumber `AttachmentUID`** while preserving the semantic tag target. Raw UID equality is therefore an invalid all-or-nothing preservation oracle. Conversely, merely retaining an attachment file and a custom Tag does not prove the Tag still points to that attachment: the target might be dangling or redirect to a different file.

The P0 browser experiment deliberately creates a flat Matroska with two content-distinct attachments, attaches a custom `P0_ATTACHMENT_RELATION` Tag to the actual `properties.uid` of one of them (not `mkvmerge -J attachments[*].id`), and self-checks the source XML.

The independent oracle `scripts/p0-audit-attachment-tag-relations.py` uses MKVToolNix to independently enumerate and extract all source/output attachments, reconstructing each item's **filename + MIME + byte length + SHA-256** and resolving Tags' `AttachmentUID` to this identity. It compares the fixture marker and its **logical target**, allowing raw UID reassignment while detecting dropped/changed Tags, payload changes, a dangling target and a retarget to the distinct decoy attachment. A Python `--selftest` exercised from Node contains negative and positive controls.

CI writes `p0-attachmenttag-relation-audit.json` even on `DIFFERENCE_DETECTED` or `CHECK_UNAVAILABLE` and uploads it unconditionally. A red is preserved as evidence, not downgraded merely to make CI green.

## Decision boundary

- Green `CHECKED_RELATIONS_MATCH` supports only this fixture's single AttachmentUID tag/payload relation, *not* general Matroska preservation.
- Red `DIFFERENCE_DETECTED` means a semantic mismatch in the tested warning-and-allow class. Investigate and revise protection only after independently verifying the failure.
- `CHECK_UNAVAILABLE` is test infrastructure/fixture absence, not proven data loss.

Test evidence now confirms this particular attachment-targeted marker remains bound to the same extracted content for the tested source/output, allowing UID renumbering. This does **not** authorize a universal product guarantee or removal of preflight warnings, and Issue #77 remains open. Main post-merge CI requires independent checking. This Test is not Canonical.

**Post-merge exact-head confirmation:** main `0b2d2a502e015374043f0bf664fbacd2cc14b82c` completed [Browser E2E run 38221153051](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38221153051): 229/229 Node tests, all browser scenarios PASS, `P0 track-tag semantic relation: CHECKED_RELATIONS_MATCH` and `P0 attachment tag semantic relation: CHECKED_RELATIONS_MATCH`. [Pages build/deploy run 38221153070](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38221153070) succeeded. These positive controls remain fixture-scoped; known ChapterUID/nested-chapter issue #77 stays open.
