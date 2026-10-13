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
