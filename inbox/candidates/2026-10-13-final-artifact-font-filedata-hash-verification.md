# Candidate: Audit final container FileData against the exact staged attachment bytes

Date: 2026-10-13
Status: Candidate — exact-head Node/build and real Chromium output verified (not Canonical)
Product: [MKV-Fast-Muxer PR #109](https://github.com/11576865/MKV-Fast-Muxer/pull/109)
Scope: new subtitle/font attachment deliverables; not a generalized writer or preservation standard

## Reusable observation and engineering hypothesis

A post-mux ffprobe stream/attachment count and filename match does not prove the **newly written attachment's bytes** equal those passed to the muxer. Likewise, the hash of a *source* font prior to HarfBuzz subsetting does not establish what was actually staged.

Use a stricter witness hierarchy:
1. At the final FFmpeg virtual filesystem write, hash the exact staged byte array (post-transformation/subsetting).
2. After FFmpeg emits the MKV Blob, traverse its actual EBML attachment inventory with an independent seek-only parser.
3. Uniquely match the new attachment by filename; separately check declared MIME and byte count; SHA-256 hash the extracted FileData and compare with the staged digest.
4. Report pass, warning, unavailable or not-requested, keeping generated output available even when this bounded audit is inconclusive.
5. Propagate warning/unavailable to task and UI audit status without misrepresenting FFprobe stream-level evidence as full EBML or runtime playback certification.

A bounded, independent reader can enforce a per-file and aggregate byte budget. Ambiguous duplicate filenames, missing attachment, unexpected MIME or bytes, parser failure, or budget exhaustion must never turn into false pass.

## Product implementation under verification

- `src/output-font-payload-audit.js` is a new isolated, no-DOM verifier.
- `src/main.js` records staged font bytes, invokes the verifier on the real output and binds `report.audit.fontPayloadAudit`. The shared single/batch operation retains downloadable artifacts and treats discrepancies as audit warnings.
- The existing output evidence inspector displays the actual new-font verification count.
- Unit fixtures include real EBML output and mismatch/unknown tests; browser E2E is extended for deduplicated full font and HarfBuzz subset font real output.

**Pending:** final exact-head Node/build and full Chromium E2E results. No conclusions of completed verification may be drawn from the candidate before these pass. No Canonical promotion from this single implementation.

## Evidence limits

This checks **new font attachment FileData** only. It does not prove original attachment preservation, Chapters/Tags UID relation safety, unknown EBML, font license or executable safety, actual glyph shaping/rendering or playback in other media players.

## Exact-head production verification (2026-10-13)

PR [#109](https://github.com/11576865/MKV-Fast-Muxer/pull/109) exact tested head `007d9d0e26ba00d172805512f7b3240adef7b484`, merged into main at `39f73c59ff015cf4aa56c89d3771e3ccef11e52b`.

- [Node tests and Pages build 38345684396](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38345684396) **success**.
- [Full real Chromium E2E 38345684462](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38345684462) **success**. Scenario 1 validates a deduplicated normal TTF output against actual `audit.fontPayloadAudit.status === pass` and the UI's 1/1 byte-verified text; Scenario 27 verifies the output's actual post-HarfBuzz subset TTF payload; existing P0/batch/attachment and browser fixture tests remain mandatory and green.
- Bounded negative Node tests: changed staged SHA, missing/duplicate filename, MIME difference, unparseable output and resource budget do not produce a false pass.
- Newly generated MKV remains downloadable on audit warning; the shared batch result ledger inherits `auditWarning` rather than representing it as fully verified.

Evidence remains bounded to **new font attachment FileData**, and the re-reader is still internal to the product (the external Chromium mux suite verifies actual output and FFprobe semantics, not full external independent EBML relationship equivalence). No promotion to Canonical.


## Extension: original source FileData versus output FileData (2026-10-13; pending exact-head browser oracle)

Product [PR #113](https://github.com/11576865/MKV-Fast-Muxer/pull/113), head `e76093406d89245bfc3c8470c07f85d424c417a6`, adds a second, **separate** preservation claim: source MKV attachment FileData SHA-256 compared with actual output MKV FileData, including explicitly renamed selected source attachments. Existing FFmpeg ffprobe count/MIME checks cannot establish byte equivalence.

The implementation uses two independent seek-bounded EBML attachment inventories (source and final output), requires unique source/output filename correspondence, expected MIME and equal byte length, and checks both actual SHA-256 digests within per-file and total bounded read budgets. It returns pass/warning/unavailable/not-requested, with evidence observations for each verified file. A warning or unavailable result must downgrade otherwise-passing final audit and batch task to review-required **without losing the artifact**. The output inspector shows original payload verification separately from new-font staged/output verification.

**Non-claim:** byte equality does not prove original FileUID or TagAttachmentUID references, Chapters, unknown EBML relations, or generic Matroska fidelity; these continue to require separate evidence. UID retained is only an observed pair, not an asserted relationship graph.

Node tests with real EBML outputs include two matching files, same-length modified bytes, authorized rename, missing name, altered MIME, malformed EBML and bounded budget. The existing Chromium selective-original-attachment scenario now requires pass and SHA evidence in actual downloaded report and UI.

Status: Node/build [38359416355](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38359416355) **success**; full browser [38359416323](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38359416323) **still pending** at intake. No Canonical promotion.
