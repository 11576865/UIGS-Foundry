# Candidate: Use a bounded source-structure hazard gate before lossy container remux

Date: 2026-10-12
Status: Candidate — feature PR under CI / partial domain guard, not Canonical
Related Case: `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`
Related Bug: `inbox/bugs/2026-10-12-mkv-browser-remux-nested-chapter-and-target-tag-loss.md`
Product: `11576865/MKV-Fast-Muxer`
Issue #77: https://github.com/11576865/MKV-Fast-Muxer/issues/77
Implementation Draft PR #78: https://github.com/11576865/MKV-Fast-Muxer/pull/78
Evidence Draft PR #76: https://github.com/11576865/MKV-Fast-Muxer/pull/76

## Reusable engineering knowledge / boundary

When a general-purpose container tool uses an output writer that may silently discard a class of legal source metadata, the correct early remediation is a **pre-write structure and capability risk gate**, not a green status inferred from the writer's successful exit code or one FFprobe stream count.

- The classification MUST distinguish `detected known-risk`, `inconclusive / not inspectable`, and `no known hazard detected` — the latter is not equivalent to 'whole container preservation verified'.
- The inspection should act on the original source before staging large inputs, before creating a new artifact, and before invalidating a user's prior completed output.
- For a media container, the gate should parse structural relationships hidden by flat inspector projections. In Matroska this includes recursively nested ChapterAtoms and UID-targeted Tags.
- Where metadata is small but media payloads are large, use a seek-style scan of EBML element headers through `Blob.slice()` or equivalent bounded random access; skip Clusters without staging their bytes. Malformed, unknown-length, or oversized metadata not covered by the parser is **inconclusive**, and a conservative writer should block rather than silently proceed.
- For multi-job batches, preflight every planned source **before** starting any output or discarding earlier results; otherwise a late blocked job may occur after earlier jobs were already published. Per-job execution must also enforce the same policy to cover mutable plan state.
- Reader/parser confidence and writer capability must not be conflated. A conservative gate may reject benign material (for example many writers emit UID-targeted track statistics), so its actual workload rejection rate should be measured and the policy refined only after independent proof. Unilateral global expansion is not justified.
- A confirmed branch-local fixture demonstrates that FFmpeg/Wasm remux flattened a nested chapter and dropped a target-linked tag; a plain mkvmerge remux also dropped the target-linked tag while preserving nested chapter structure. Thus merely switching to a different ordinary muxer is not proven to fix all structural relationships.

## Specific implementation experiment

Draft PR #78 adds `src/preservation-preflight.js`: bounded EBML header walk and structural Chapters/Tags parsing, `BLOCKED_RISK`, `BLOCKED_UNKNOWN`, `NO_KNOWN_HAZARD` and `NOT_MATROSKA` classifications, direct single and batch source gating, explicit preflight error display, and synthetic unit plus actual browser E2E based on the independently authored source from #76.

The P0 policy only covers known risks and does NOT guarantee other EBML elements, all metadata fields, bytewise packet identity, playback semantics or font rendering. The branch must remain Draft until independent hard-fixture E2E and legacy workflow tests have completed.

Acceptance target: a high-risk source containing a nested chapter and ChapterUID-targeted tag must be refused **before new output**, while existing ordinary single and batch behavior stays functional. Attempting a dangerous new source must not revoke a previously completed download. No universal 'full Matroska preservation' capability claim is permitted.

Do not auto-promote to Canonical from this single project. Source references: RFC 9559 sections 5.1.7, 5.1.8, 24; https://www.rfc-editor.org/rfc/rfc9559
