# Test Pending: Softmux vs MKVToolNix on identical attachment replacements

Date: 2026-11-04
Status: **Test / execution pending — not a passed preservation claim**
Product: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/236
Implementation head: `35fbbabc85df6ac1b73bf741b6c4a3f79c530658`
Workflow: `.github/workflows/browser-e2e.yml`
Test script: `scripts/p2-mkvtoolnix-same-input-replace-comparison.mjs`
Evidence output: `.e2e/output/p2-mkvtoolnix-same-input-replace-comparison.json`

## Test question

Does the existing bounded Softmux attachment FileData writer produce an independently valid output, or refuse honestly, when native `mkvpropedit` can perform the **same attachment replacement on a copy of the exact same MKV source**? The source is independently authored by MKVToolNix with nested ChapterAtom and ChapterUID-targeted Tag.

Two planned payload changes: exact same byte length and 61-byte growth. Both target the exact string FileUID, not merely a file name or floating-point UID.

## Script boundaries

- Native `mkvpropedit` edits a copied MKV, never the source.
- The product backend gets the original Blob and the same replacement bytes, and its result is a new Blob.
- A completed native operation must independently preserve attachment filename/MIME/UID, exact replacement SHA-256, complete chapter/tag XML strings, and ffprobe packet fields/hashes.
- The product receives the same independent checks if it produces an artifact.
- An explicit product refusal is **a measured capability gap**, not a false positive and not a corruption result; an accepted product output that fails checks is a regression.
- Native reference itself can fail; such a result is FAILED/INCONCLUSIVE, not a reason to call the product equivalent.
- Exact-head tests, browser execution, upstream license/code migration, arbitrary EBML support and diverse player behavior are distinct unproven dimensions.

## Deduplication

Existing Foundry cases describe *individual* native Matroska attachment replacement writers and validation fixtures; Candidate `2026-10-15-mkv-multiple-bounded-writers-one-router-with-output-oracle.md` describes aggregation and a broad common readback. This Test specifically makes a **same-source/same-intent dual-executor comparison** against mature `mkvpropedit` on a nested-chapter/UID-tag source, with explicit PASS/BLOCKED/FAIL statuses.

New Canonical changes: none. Wait for workflow run and audit artifact before reporting test outcome or deciding whether to replace the underlying writer.
