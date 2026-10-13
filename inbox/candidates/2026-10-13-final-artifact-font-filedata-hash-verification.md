# Candidate: Audit final container FileData against the exact staged attachment bytes

Date: 2026-10-13
Status: Candidate — implementation and exact-head CI pending
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
