# Candidate · Split media remux from original Matroska attachment byte preservation

Date: 2026-10-22
Status: **Candidate / bounded positive native+Chromium empirical proof; NOT Canonical; product integration NOT authorized**
Owner project: `11576865/MKV-Fast-Muxer` S12
Research PR: https://github.com/11576865/MKV-Fast-Muxer/pull/176
Exact code head: `876c026734c4f4fcc6be4c003bbdf0910e6b8198`
Scoped independent CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39653258553

## Deduplication
- Existing `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md` already requires structure-preservation fail-closed before a lossy remux; unchanged. This Candidate addresses a **different new bounded execution geometry**: separate the engine's A/V writer from large source original AttachedFile/FileData bytes.
- Existing `inbox/candidates/2026-10-03-reuse-large-browser-media-staging.md` addresses source input staging and identity; the current 0.1027 WORKERFS path is reused, not re-specified.
- Existing `inbox/cases/2026-10-14-ebml-crc32-nested-attachedfile-attachments-writer.md`, `inbox/cases/2026-10-14-mkv-variable-filedata-adjacent-void-without-offset-movement.md`, and S12 `inbox/tests/2026-10-21-softmux-s12-original-attachments-blob-seekhead-native-browser-pending.md` supply raw EBML CRC, positional and native oracle precedents. This Candidate is **not** a general EBML writer or a duplicate of those Cases.
- Search for exact combined `FFmpeg.wasm excludes attachment output AVStreams + reattach original Blob.slice master` did not reveal another registered Candidate; do not promote merely because one CI environment passed.

## Observed problem
- Before this design, WORKERFS already allowed >1GB real PCM media-packet MKV mux in 0.1027, while **128MiB original attachments pass / 256MiB originals fail** when ffmpeg.wasm directly maps original attachment AVStreams. Controlled five-case [#39610097982](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39610097982): with total 256MiB original attachments, 2×128, 4×64, and 8×32MiB all OOM during formal output; 128MiB 2×64 and 4×32 passed. This links failure more strongly with total original FileData payload allocation, not raw object count alone. Does not establish a universal 256MiB ceiling.
- Merely using `WORKERFS` for source input cannot prevent the FFmpeg output muxer from buffering/copying original attachments while constructing the Matroska header.

## Bounded two-lane candidate
1. Bind the **same actual immutable source browser File** and reject source graph shapes outside the verified class **before** loading/running FFmpeg.wasm: one complete `Attachments` master, finite exact Segment, no unsupported Segment CRC, no original `Tags` or `Chapters` (especially UID-targeted relationships), no arbitrary unknown layout grant.
2. Mount source read-only with already-delivered `WORKERFS` / exact File reference. Execute real Chromium FFmpeg.wasm with explicit `-map 0:v:0 -map 0:a:0 -map 1:s:0 -c copy -c:s srt` and **never** map original attachment streams into the output. FFmpeg.wasm owns the A/V+new-subtitle packet streams only. It returns a bounded, small no-attachments MKV Blob; failure is terminal, never silently fall back to full input MEMFS.
3. The independent browser `Blob.slice` path references the original Matroska `Attachments` master bytes without reading large FileData as a single JS array; reindexes appended master with the output's fixed-width Segment VINT, the first valid CRC-protected `SeekHead`, an adjacent `Void` slot sized to keep offsets invariant, and recomputed `SeekHead` CRC32 using the existing `src/ebml-crc32-bounded.js`. If the reserved index layout cannot fit, reject; do not silently relocate Cluster/Cues or claim graph preservation.
4. Deliver a new Blob via browser download, **not** mutate original. Independently inspect final MKV's video/audio/new subtitle, exact attachment inventory, `mkvextract` every original attachment + full SHA-256, untouched source SHA, and byte-level SHA-256 of **every ordered original/output encoded audio and video packet**. No success state if any native audit fails.

## Exact bounded evidence
- [PR #176 S12 CI #39652209683](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39652209683), exact head `456e2dcd73b78bc8856155bfd2dc0306485e1208`, completed two real-Wasm jobs with 128MiB/2×64 and 256MiB/4×64 original attachments: no-original-attachment WASM media mux -> browser original Blob reattachment -> actual download -> native full audit. The first 256MiB download was 268,479,375 B; 128MiB 134,261,510 B. One interim harness mistakenly interpreted the word `attachments` in **output filename** as a mapped attachment stream. Final command checker compares exactly the three `-map` values; no production mapping was relaxed.
- [Exact later CI #39652594549](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39652594549), head `54fbb3d8f2eaee6e333ee0b41437ae9defb5ac61`: both workloads PASS with independent per-packet video+audio SHA sequence parity, original attachment SHA and native final output audit.
- [Latest S12 scoped CI #39653258553](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39653258553), exact head `876c026734c4f4fcc6be4c003bbdf0910e6b8198`: all eight research jobs **SUCCESS**, including true original `Tags` negative branch in Chromium 128MiB: rejects at bounded source preflight **before FFmpeg.wasm exec**, emits no new output authority and cannot carry stale output evidence to a changed File. A tagged input is intentionally NOT supported. Full ordinary Browser E2E at this head was pending at Candidate intake.
- These are real non-sparse 2-second video/audio MKV source files with large incompressible original binary attachments, not typical long-duration compressed films, and only run on the CI Chromium/Linux setup. The research API carries `authorization:'NONE_RESEARCH_ONLY'` and lives outside the product UI and dispatch. Main remains softmux 0.1027.0.

## Remaining safety/performance gates before any bounded product promotion
- Formal source and remux metadata parity or explicit no-edit impossibility for `Tags`, `Chapters`, `TagAttachmentUID`, `ChapterUID`, attachments with per-master/nested CRC, atypical `SeekHead`/nonterminal `Attachments`, `Cues`, unknown-size/fragmented Segment and multiple original master ordering. Source-attached FileUID/name/mimetype uniqueness and graph targeting require independent verification; don't assume binary bytes imply complete document semantics.
- Failed, interrupted, changed-source or canceled operations must not leave stale writer authority or a green downloadable artifact. Validate source File object identity and execution-bound revision, including batch/project recovery.
- Real desktop/tablet memory envelope (including browser output data copies), 512MiB/≥1GB original attachments with realistic long media, output persistent-save reliability, and diverse browser engines.
- Explicit authorized limited route and human-readable scoped capability disclosure; never automatically default a general MKV to this research writer. No Canonical update until repeated independent source and real-device evidence supports it.

## Disposition
**Reusable technical candidate established; no general Matroska preservation rule or release capability adopted.** Integrate only if the full acceptance and unsupported-input refusal matrix becomes green on the exact product branch. Keep research PR Draft.
