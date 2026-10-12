# Candidate: QHE as an evidence-led media transformation and delivery workbench

Date: 2026-10-12
Status: **Candidate / strategic design proposal only**. The owner requested an optimal possible future design integrating the 2026-10-12 soft-mux resolution and the current multi-turn first-principles QHE discussion. **Owner has not yet ratified this proposal, and no QHE code/UI/Canonical modification is authorized by this note.**

Project: `11576865/Quick-Automatic-Hardsub-Encoder`
Reference product: `11576865/MKV-Fast-Muxer`
QHE reviewed main: `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`
Dedup search: Foundry searched `qhe product identity`, `QHE trusted media delivery plan`, `QHE media transformation task model`, `QHE project direction` and reviewed the existing observations, per-output-track audio Candidate and rate-distortion frontier Candidate. No prior cross-domain strategic contract found. This Candidate **extends rather than replaces**:
- `inbox/observations/2026-10-12-qhe-feature-growth-and-unresolved-product-identity.md` (owner's epistemic root-cause correction)
- `inbox/observations/2026-10-12-qhe-competitive-scope-and-evidence-boundary.md`
- `inbox/candidates/2026-10-12-qhe-per-output-audio-track-intent-and-encoder-capability-layers.md`
- `inbox/candidates/2026-10-12-media-transform-temporal-mapping-must-be-explicit.md`
- `inbox/candidates/2026-10-12-intended-reference-and-subtitle-render-order-for-media-qa.md`
- `inbox/candidates/2026-10-10-diagnostic-curves-are-not-yet-an-optimized-decision-frontier.md`
- `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md`

## Proposed core identity and design test

**QHE is a local, verifiable media transformation and delivery workbench, led by specialized high-assurance ASS burn-in.** The core object is the **Output Media Transformation / Delivery Plan**, not the input file, ASS alone, MP4/MKV container alone, FFmpeg CLI args or codec/preset list. The user states desired preserved properties, required transformations, admissible quality/time/size/compatibility bounds and desired deliverables; an implementation-specific compiler derives a transparent plan; a platform backend executes; independent evidence distinguishes what was actually proven.

The pitch is a product hypothesis, not a claim of existing global optimality or superiority over HandBrake, StaxRip, Shutter Encoder, ab-av1 or Av1an. Their established codec, passthrough, VMAF/target-quality, queue and general convert capabilities remain competitive baselines.

Hierarchy (analogous in method, NOT identical in object to approved MKV-Fast-Muxer direction):
- **A Flagship workflow:** reliable ASS/SSA + fonts hard-sub delivery, including embedded MKV subtitle/font extraction, actual renderer/geometry/clock/color correctness, output audit.
- **B Domain authority:** source media inventory -> user conversion/preservation intent -> versioned per-deliverable stream plans -> resulting output composition. Stable IDs/provenance, single mutable authority.
- **C Cross-cutting decision engine:** bounded sampling, codec/performance/quality/size evidence, branch comparisons with uncertainty and costs; no untested global optimum or arbitrary fixed-byte success guarantee.
- **D Cross-cutting inspection/assurance:** capability probe, timestamps, colorspace, per-track decode/copy/encode semantics, subtitle/font render, output independent structural and content audit, playback-specific compatibility only when tested.
- **E Execution and delivery:** backend adaptors (Windows FFmpeg/native, Android FFmpegKitNext/Service, Web/WASM), staged output, immutable job snapshot, owned job/queue, safe publish/recovery, optional handoff to advanced soft-mux composition.

The five are different responsibilities over *one coherent task model*, not five separate apps/tabs, and the letter classification is descriptive only.

## Domain sketch (proposal, no API commitment)

`SourceAsset/SourceStream/ResourceDependency` -> `UserIntent (must-preserve, may-transform, target profile, budgets)` -> `OutputPlan[TrackAction, TimeMapping, ColorTransform, RenderReference, ArtifactComposition]` -> `Capability/EvidenceResolver` -> `ImmutableJobPlan (actual encoder/plugin/runtime args)` -> `JobRuntime/Artifact` -> `IndependentAudit/ArtifactRecord`.

Important invariants:
- Explicit mapping and separate per-output video/audio/subtitle stream actions; preserve selected streams packet-wise when requested.
- No silent audio transcoding, subtitle removal, downmix, HDR conversion, clip boundaries, or encoder fallback; unsupported policy is a meaningful outcome.
- Source truth, observed probe facts, task intent, inferred estimates, actual output and playback evidence distinct.
- Performance/quality exploration data, actual final encode and measured output are different evidence modalities; a decision curve is a bounded candidate frontier, not global optimality.
- Source timing (PTS/DTS/clock offsets) and transform-time coordinates modeled explicitly; filter/reference geometry and color are testable.
- The single output task is a normal success path: never require the separate mux application for a plain MKV/MP4 output.

## Boundary vs MKV-Fast-Muxer

Soft-mux approved domain center: `ContainerDocument`, full Matroska track/attachment/chapter/tag/unknown-EBML composition and structural preservation; flagship soft subtitle/font self-contained delivery.
QHE domain center: change encoded and rendered *media content* when necessary; make ordinary muxing/output a first-class supporting capability without duplicating advanced Matroska editors.
Possible **interchange** is a versioned, independently verifiable `ArtifactManifest` (source provenance/stream identity, actions, codecs, timestamps, subtitled render properties, output format, audit hash/status), not two apps sharing one mutable DB. This is future integration, NOT an existing cross-app handoff.

## Competitor/reality checks

- HandBrake already offers track-by-language audio selection, passthrough with fallback; QHE can only claim value by making user-intended irreversible differences explicit and testable.
- StaxRip already orchestrates external tools, encoders and multiple muxers: adapter architecture is established, not itself a unique innovation.
- Shutter Encoder already exposes FFmpeg as a rich operation-focused workbench; generic conversion does not define unique QHE identity.
- ab-av1 and Av1an already implement sampled target-quality/metric search, so QHE decision differentiation depends on the **complete ASS/font + media-preservation + measurable constraints + verified delivery chain**, measured in an identical controlled corpus.
- FFmpeg direct stream `-map` and per-output-stream `-c:a:N` support exists; QHE `src/media-task.js` task-wide `-c:a` is a product model boundary, not a platform impossibility.
- Strict size-ceiling currently only verifies the final file is under a ceiling (in narrow Windows libx264 path) or refuses publication. No guarantee any arbitrary target can be achieved at specified quality.
- H.266/VVC/10-bit/HDR and more platform encoders are optional, verified plugin/adaptor research rather than shortcuts to the product's core value.

Sources: user conversation 2026-10-12; attached `软封工程_未来规划总决议_2026-10-12(1).txt` sections 05/06/07/08/11/13/14/16, `项目原则报告_2026-09-30.txt`, QHE compression reports Oct 10/11; QHE README, `docs/manual-media-workspace.md`, `src/media-task.js`, `src/media-container.js`, and `docs/stream-plan-v4-device-acceptance.md`.

## Proposed staged falsification gates

0. **Baseline** current user workflows including guided ASS hard-sub, manual transcode, stream-copy, clip queue, all 3 executors; inventory media first principles and source/expected/output evidence before UI rebuild.
1. **Read-only output-plan projection** over existing v4 task compiler; compare compiled FFmpeg args and actual output against frozen fixtures, with single editable authority and zero regression; do not replace v4 wholesale.
2. **Per-track audio actions, stream preservation and embedded-ASS/font source binding** with mixed-codec and independent final output oracles, keyframe/timebase/geometry constraints.
3. **Bounded decision-frontier** over controlled codec/resolution/time/quality candidates and fixed copied audio/attachments budgeting; report incomplete search and cost; compare matched workflows against competing tools.
4. **Color/HDR and VVC/other runtime adapters** only after actual probes, firmware/device compatibility, independent re-decode, rendering and legal packaging.
5. **Batch deliverable matrix and optional soft-mux handoff**, separate output/result lifecycle; UI re-projection only after representative task tests.

User-centered acceptance corpus: multi-video/multi-audio MKV, internal ASS + font attachments, VFR/offset, SDR/HDR, sharp subtitles, detailed texture/grain, keyframe trims, corrupted/unknown metadata, audio passthrough with explicit partial conversion, output storage failure, Windows/NVENC real machine, Android real phone/SAF, browser memory limits. State per environment, media case and evidence level; no imaginary cross-platform parity.

Failure conditions: the suggested model significantly increases time-to-first-success; loses existing one-click hard-sub/fast copy/batch/quality controls; cannot explain its recommendation; silently changes untouched streams; collapses warning/pending states into green badges; or generates duplicate mutable states per workspace. In these cases, stop and revise rather than justify by architectural elegance.

This Candidate proposes a coherent strategic direction for owner review and can inform comparative prototypes. It is **not Canonical, not an implementation mandate, and not a claim that QHE has already achieved this vision**.
