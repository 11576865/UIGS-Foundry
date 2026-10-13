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
