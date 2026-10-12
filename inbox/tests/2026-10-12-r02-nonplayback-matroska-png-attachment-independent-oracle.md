# Test: R-02 non-playback Matroska — single PNG attachment, zero Tracks/Cluster, independent reader+byte oracle

Date: 2026-10-12
Status: Test / **one passing independent-tool research fixture**, not Canonical or production writer certification
Project: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/88
Product merged commit: `fee72462c687181348f7f1f2e181816c1dc8d30d`
Exact PR head: `c267e639ef6058ceb1c1ca0f7401ba8a24af794f`
Verified workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38237809185
R-02 experiment artifact: `r02-png-only-matroska-experiment` (artifact ID `11741029185`, attached to run; time-limited retention)
Reference specification: RFC 9559 §§4.5, 6.1 and 21.

## Hypothesis and scope

The container domain is permitted to **model** a target with exactly one PNG AttachedFile, zero Tracks, zero Cluster, and no video surrogate. Current video-rooted FFmpeg mux execution is a **different** capability from the format's top-level structure. RFC 9559 §6.1 says Info is the sole REQUIRED Segment top-level element while a *playable* Matroska requires Tracks and Cluster; this is a normative starting condition, not a guarantee that a particular fixture satisfies every EBML constraint.

## Reproducible independent oracle

1. `scripts/r02-attachment-only-experiment.mjs` writes a deterministic **test-only** EBML Header + Segment(Info, Attachments) document containing a valid one-pixel PNG `pixel.png` as AttachedFile FileData, FileMediaType `image/png`, FileUID 42. It deliberately adds **no** video, audio, subtitle, Tracks or Cluster elements.
2. Independently run `mkvmerge -J` (different software from the fixture writer). Require exactly 0 tracks and 1 attachment with the requested file name and media type.
3. Extract attachment using `mkvextract attachments` and compare extracted bytes with the original PNG via SHA-256/content equality. Do not treat a copied MIME string as a byte integrity check.
4. Run `ffprobe` separately. A reader returning EOF for a non-playing/no-track container is recorded as a compatibility observation; it is **not** automatically classified as a broken EBML structure.
5. Save machine-readable `r02-attachment-only-report.json` even if MKVToolNix fails. CI runs this experiment `continue-on-error: true`; **green workflow status alone does not certify R-02**. The JSON verdict is the scoped oracle.

## Observed exact-head result

- GitHub workflow `38237809185`: **254/254** Node unit tests pass, Vite Build pass, full Chromium Browser E2E passes.
- Experiment step completed successfully, logging:
  `result=INDEPENDENT_READER_AND_BYTES_MATCH`;
  `reader.mkvmerge=parsed`;
  `reader.mkvextract=extracted`;
  `reader.ffprobe=rejected-or-no-media`.
- Independent audit artifact was uploaded. These observations establish **one validly extracted test-only sample** and demonstrate why reader/playability and format-domain representation must not be conflated.

## Non-claims / future falsification

- No production browser attachment-only writer, GUI operation or generalized attachment extractor is proven.
- Not a formal standards conformance suite, not multiple-independent-reader certification, not portable player support.
- No proof that arbitrary Chapters, Tags, unknown EBML elements, UID target relationships, or changing an existing MKV are preserved.
- Follow-up: inspect additional independent parser/validator, document full schema constraints, test a production-compatible writer with arbitrary attachment bytes/size/name/MIME and no invented media, then validate roundtrip and filename conventions. Keep the writer capability explicitly unsupported until those gates pass.

## Existing-knowledge dedup

Extends the scope/standards distinction already recorded in:
`inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`
and
`inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md`.

It is a **Test-level evidence record**, not a promotion or rewrite of either Observation and not a change to any UIGS Canonical rule.
