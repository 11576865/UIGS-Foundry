# Candidate: Separate imported asset identity from its task role in content-first media workbenches

Status: **Candidate / implementation under Draft PR CI**  
Date: 2026-10-10  
Domains: information architecture, media ingest, UX-dataflow contracts, source selection, container/track navigation

## Observation

Product: `11576865/MKV-Fast-Muxer`  
User direction: The initial UI refresh only changed icon labels but retained four separate **Video / Subtitle / Font / Audio** upload gates. The user rejected that architecture: a workbench capable of recognizing multiple actual input content types must not require users to choose a type before importing. The earlier UI-only Draft PR #67 was closed without merge.

The existing code uses distinct DOM File inputs (`videoInput`, `subInput`, `fontInput`, `audioInput`) with real change handlers for mux execution, subtitle/family inspection and source MKV track scanning. These represent **execution roles**, but the visible UI was using them as **ingress categories**. A new content-first intake can unify import without assuming that content identity alone defines source/append roles.

## Proposed principle

**Asset identity is discovered; role is assigned.** Keep them distinct:
- One import surface for files, folder selection or file drag/drop; preserve an auditable inventory of *every* input, including unrecognized bytes.
- First classify by inspected content/signature, not filename extension or MIME claim. Distinguish recognized headers from internal stream evidence; a recognized MP4 `ftyp` or Matroska EBML header does not establish a video stream.
- Choose the primary video-bearing container explicitly if more than one is present. A single candidate can be tentatively selected, but `ffprobe` still validates actual streams before the video mux path accepts it.
- Standalone recognized subtitle/font/audio assets may be mapped to existing role adapters; classify undecidable inputs as `UNSUPPORTED` or `UNVERIFIED`, not silently dropped.
- Source-container tracks, attachments, chapters and metadata belong conceptually *under the container object*, not as four separate files to upload.
- Keep user-edited metadata and audit paths owned by stable domain objects, not input-widget lifetimes.
- The UI affordance change alone is insufficient: replace the implicit source+added-subtitle precondition so a source-only MKV remux can be represented, while maintaining actual video-stream verification.

## Engineering proposal and current evidence

Issue: https://github.com/11576865/MKV-Fast-Muxer/issues/68  
Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/69  
Initial head: `896019e97fca2b8a87d7fc52cde749ed69156850`

PR #69 adds `src/asset-intake.js` (bounded content-signature classifier and explicit source-role resolution), a unified resource inventory in `index.html`, and `src/main.js` wiring through the existing input-event adapters. It preserves the existing source-MKV scan and post-mux audit. The classifier's role claims are explicitly weaker than mux/codec support claims. A single-source-only MKV remux path is enabled without mandatory new subtitles.

Local source-derived V8 results: **8/8** classification/role checks and **6/6** UI source checks passed; full Node CI, Chromium E2E, actual viewport screenshots and manual UX acceptance **not yet proven**. New browser scenarios exercise mixed-content import with real mux, unsupported asset gating/removal, multiple-container ambiguity and source-only MKV remux. PR is Draft; do not claim production deployment or tested visual appearance.

## Deduplication and evidence boundaries

Foundry search for `content-first intake`, `unified asset inventory`, `role after classification`, `import slot category` found no identical intake/role UX case. Existing `2026-10-05-media-import-capability-stages-must-not-collapse.md` already distinguishes parseability, decoding, stream-copy and execution readiness. The new candidate specifically addresses **user-facing import categories vs post-recognition task roles**, a separate information-architecture boundary. `2026-10-02-media-format-support-is-a-compatibility-relation.md` covers compatibility evidence, not the import-gate UX constraint.

The new importer is deliberately incomplete: signatures are bounded, file identity is not equivalent to complete byte hashing, and the internal legacy role input adapters remain. Do not infer arbitrary format support or guarantee that all media containers can serve every role. Keep Candidate-only; no Canonical update based on one draft implementation.
