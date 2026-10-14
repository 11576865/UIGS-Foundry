# Test: QHE P1 read-only Source / Intent / OutputPlan projection of authoritative schema-v4 task

Date: 2026-10-14
Status: PASS — bounded real Chromium + model, whole P1 and B02 not complete
Project: 11576865/Quick-Automatic-Hardsub-Encoder PR #105
Tested exact source SHA: 0124946d6939f73a285dcf609a6a973924d44219
CI: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38575999722
Requirement basis: owner R19 §03/P1, R24 §05; B02/B20/B24

## Source-derived requirement

The owner report requires the migration sequence `SourceAsset/SourceStream -> UserIntent -> OutputPlan -> ImmutableJobPlan -> ArtifactRecord`, with the first-stage P1 explicitly a **read-only projection** from existing v4 task structure, checking command equivalence and preserving single execution authority. Current `task.outputPlan` already exposes partial stream decisions, but inspection lacked combined source facts, explicit compiled-intent provenance, output maps and unknown artifact evidence.

## Code under test

`src/delivery-contract-projection.js` consumes the authoritative v4 compiled task and source probe facts. It creates a deeply frozen projection including all observed video/audio/ASS subtitle/font attachment stream rows and copy/encode/drop actions, compiler-inferred intent, the existing OutputPlan, actual outputArgs map/codec/filter hints, and explicit unverified artifact state. Mapping mismatches produce advisory warnings, not modified task arguments. The production existing task review disclosure displays exact stable source identity and invalidates the prior model when the input source changes.

## Tests and results

- Real schema-v4 `compileTask` is used for mixed-MKV Transcode, ASS hardsub and Stream Copy; project source audio codec, drop of original subtitles and fonts, encoding intent and exact FFmpeg maps.
- Check compiled task deep-equal before/after projection, and that frozen derived arguments do **not** freeze or modify the original authoritative task.
- Contradictory map test must surface `review-required` but must not rewrite FFmpeg outputArgs or claim artifact verification.
- Production Playwright/Chromium clicks '验证当前方案', expands the actual source/stream/intent/output/command inspector, verifies the selected input identity and all five mixed-media stream rows, switches workflow to Stream Copy and confirms `-c:v copy`, then changes source and requires old projection hidden without initiating encode.
- Initial browser run 38575759908 exposed that the UI showed only 'source identity bound' instead of the actual identifier; fixed UI to display that provenance in tested SHA 0124946, and rerun 38575999722 SUCCESS. Test frontend 38575999605 SUCCESS; UIGS Coverage 38575999820 SUCCESS.

## Evidence boundary

This proves a passive projection layer, not a separately owned, signed UserIntent, a new immutable backend job plan, an independently verified ArtifactRecord, source-stream stable IDs across all backends, live mixed MKV physical validation or full B02 acceptance. No Canonical promotion.

Dedup: existing Foundry candidate `2026-10-12-qhe-verified-media-transformation-delivery-domain-proposal.md` owns the cross-project conceptual domain model, and `2026-10-13-qhe-shared-task-presentation-and-execution.md` owns single executor/UI state. This entry is only the new falsifiable P1 read-only projection test evidence, not a competing theory or new Candidate.