# Observation: HSR regenerated FLAC/ASS requires a new MKV; no incremental track update exists

Date: 2026-10-13
Status: Observation / source-verified workflow distinction; design improvement not implemented
Project: `11576865/HSR-Voice-Archive-Builder`
Source: current `main`, after merged PR #154 (`f78c2794c309b01ff01d5ed7aab4bf036a9333af`)
Domains: container outputs, derived artifact lifecycle, media provenance, UI export workflow

## User question and verified code behavior

The user asked how an already-packaged MKV should change after rebuilding the continuous FLAC and subtitle track.

1. In `app/pipeline.py`, rebuilding the audio stage invalidates and `unlink(missing_ok=True)`s both `HSR_Voice_Archive_Black.mkv` and `HSR_Voice_Archive_Bundle.mkv` **after the new continuous FLAC has been successfully encoded and verified**. This is invalidation, not incremental patching of existing video.
2. In `app/archive_bundle_exporter.py::export`, every invocation creates a new synthetic color or user-image video input; uses `libx264` to encode a new video track, stream-copies FLAC (`-c:a copy`), and muxes the current ASS soft subtitle. After stream and subtitle-freshness checks, a temporary MKV atomically replaces the output. It does not ingest an existing MKV and therefore does **not** stream-copy the previous video track.
3. The Export UI `#archiveBundlePanel` explicitly says uploaded background image bytes are **not persisted** in the project. A re-export without reselecting an earlier custom image can silently change the background to the selected default solid color, even if user intended only audio/subtitle changes. This is a concrete source-level workflow risk, not an observed user loss incident.
4. Regenerating ASS does not automatically remux an already-exported MKV. Newly merged PR #154 rejects stale ASS from being *used* in a new export, but does not make the old MKV self-updating or display a complete provenance/refresh path for existing bundles.

## Bounded recommendation (not delivered)

Offer a distinct `Update MKV tracks` task that picks authoritative current FLAC/ASS/font assets and performs a verified temporary Matroska **remux** (`-c copy`) of eligible unchanged video/attachments, then atomically publishes the result. If the old bundle was deleted, the new continuous audio exceeds its video duration, or its source video/provenance is unknown, transparently fall back to full background regeneration rather than silently shortening the output. Persist/recover user-selected background asset identity or require explicit user reconfirmation before destructive replacement. Keep unchanged archive bytes until verification; represent stale output distinctly from fresh output.

## Dedup and evidence boundaries

Related: `inbox/bugs/2026-10-13-hsr-mkv-stale-ass-and-output-writer-race.md` (freshness + writer isolation, already fixed), `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md` (destination identity) and `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md` (requirement vs actual main delivery). This Observation is specifically about **replace-only track updates versus full video regeneration and transient background selection**; it does not duplicate their prior remedies.

No automatic Canonical promotion; neither the incremental remux nor background-state preservation is implemented or CI-validated.


## Subsequent scope recommendation — prefer full regeneration for HSR (2026-10-13)

The user explicitly noted that the separate **MKV-Fast-Muxer** (软封) project already owns the generalized task of replacing media container tracks, and questioned whether HSR should simply regenerate the entire bundle and replace the result. The subsequent engineering recommendation is **yes for HSR's current product scope**, subject to user approval; this is *not* a new implemented feature or an approved Canonical rule.

- HSR is a voice/subtitle archive generator with a trivial synthetic still/color video background (currently 1280×720, 1 fps, ultrafast H.264), whereas MKV-Fast-Muxer is the dedicated general-purpose track-remux/preservation product. Adding arbitrary old-container track update, stream identity reconciliation, duration handling and attachment preservation to HSR would duplicate that ownership and add failure states beyond the primary workflow.
- Retain the existing deterministic full-build path: latest current FLAC + verified ASS/SRT receipt + project-owned fonts + chosen background → fresh temporary MKV → ffprobe validation → atomic publication. Existing PR #154 freshness and writer isolation remain necessary.
- **Residual gap distinct from PR #154:** HSR audio rebuild currently deletes the previous bundle once new FLAC is validated, rather than marking it stale and atomically replacing it only after the next bundle export. A safer product workflow should explicitly indicate `MKV needs regeneration`, require/recover the original optional background image, and avoid showing stale output as current. Preserving an old file until replacement requires a clear obsolete/non-authoritative state, not silent use.
- For unusually long-duration archives, actual performance benchmarks should decide whether video regeneration warrants a specialized optimization. Generalized container remux remains out of HSR's immediate scope.

This updates the **preferred recommendation** of the prior 'Bounded recommendation (not delivered)' section without erasing its recorded technical alternative. No code change or user acceptance is claimed; Canonical unchanged.


## Verified delivery — bounded full regeneration with source-aware receipts (2026-10-13)

The user approved HSR's **full MKV regeneration rather than generalized Remux** scope. Product [PR #156](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/156), tested head `3937184c4afb77ab6236b948d0318d2ee32e4437`, was squash-merged directly to `main@eabb5ffd6bf78f326d18ad5b6089d120932b0bea`. GitHub postmerge compare returned `identical`. The divergent initial draft #155 was closed without merge. The reusable choice is product-specific, not a promotion of a universal media packaging standard.

Implementation:
- `app/pipeline.py` no longer unlinks `HSR_Voice_Archive_Bundle.mkv` after verified FLAC rebuild. The old file remains physically present but the Export interface reports `stale` rather than showing it as a current artifact.
- `app/archive_bundle_lifecycle.py` defines an explicit project-local receipt `archive_bundle_receipt.json` with source FLAC/ASS/subtitle receipt/font file signatures, MKV artifact signature, saved color, font-attachment preference and optional bounded content-addressed background picture. Saved picture bytes are checked by SHA-256 before reuse; explicit new upload wins, otherwise user can reuse or turn off reuse for pure color. Legacy pre-receipt MKVs are `unverified`.
- FastAPI and Termux Lite use the same image replay contract. Project summary exposes `bundle_export` states `current`, `stale`, `missing`, `unverified`, and UI shows `重新生成并替换旧 MKV` when needed without erasing current unsubmitted choices during refresh.
- The actual new video is still encoded from saved or selected still/color background, not copied from the previous MKV. `ArchiveBundleExporter` validates its temporary MKV with FFprobe, then prepares the new image + provenance receipt **before** atomic replacement. A simulated final rename failure restores the previous receipt, with the old media file still intact. This closes the publish-error window discovered after first-pass source review.

Evidence:
- [Python 3.11/3.12/3.13 and Termux checks 38393291476](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38393291476): success.
- [Chromium UI and real FFmpeg/libass media checks 38393291438](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38393291438): success.
- Unit tests exercise missing/corrupt legacy receipt, changed audio/subtitle, tampered image cache, interrupted build, last-known-good background, and old file retention. Actual FFmpeg tests render two complete MKVs across a changed FLAC, verify that old bytes remain until safe replacement, verify color pixels of the image-backed video, and inject failed final rename to verify old MKV/receipt restoration.

Evidence boundary: the routine `size + mtime_ns` source identity is a conservative **operational change signal**, not a cryptographic tamper-proof source seal; subtitle exports independently use checksum-bound provenance. Real player/device and end-user archive-length performance remain unverified. A process crash in the narrow receipt-prepared/pre-replace window conservatively reports a stale old output; this is not full multi-file transactional crash recovery. No AAC/multiple-track features added, no new Remux engine, no Canonical change.

This section **supersedes the earlier 'not delivered' status for persistent background and stale-output management**, while retaining prior exploratory alternatives as historical context.
