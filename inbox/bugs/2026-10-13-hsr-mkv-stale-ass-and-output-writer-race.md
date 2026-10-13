# Bug: HSR MKV exporter accepted stale ASS and concurrent output writers

Date: 2026-10-13
Status: **Fixed in source main; exact-head automated verification green; physical device and arbitrary real-world media pending**
Lifecycle: regression-verified
Project: `11576865/HSR-Voice-Archive-Builder`
Repair: [PR #154](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/154)
Tested head: `62d4ddaab64e6d2e262da3304e4632748dd99e8d`
Merged main: `f78c2794c309b01ff01d5ed7aab4bf036a9333af`

## Observed defect and risk boundary

The project's existing `app/subtitle_export_status.py` already records checksum-bound `subtitle_export_receipt.json`: source manifest, human text/timing overrides, and ASS/SRT outputs. However, both the full FastAPI MKV route and Termux lite route accepted merely existing `continuous.flac` + `HSR_Voice_Archive.ass`. That let a stale or externally modified ASS be bundled into a newly created "verified" MKV. There was a classic check-versus-publication race: authoritative subtitles could change after a job was queued or while FFmpeg muxed.

`ArchiveBundleExporter.validate()` checked one video/audio/subtitle stream and FLAC/ASS codecs but did not check video was the specified H.264 or matched expected resolution, and counted font attachments without confirming each filename/MIME. A symlinked project font directory could result in no attachments rather than an explicit error.

The job scheduler serialized build jobs only. Same-project MKV exports, ASS, black-video, build and remote-apply operations could run concurrently, competing for authoritative output files. This is a source-verified race condition; no user report of actual overwritten files is asserted.

## Implemented mitigation

- `require_current_bundle_subtitles()` reuses the project's *existing* receipt validation rather than a new parallel provenance layer. Both API adapters reject missing/stale/unverified/non-ASS receipts before queuing a job; the MKV writer also rechecks at execution start and immediately before atomic publication.
- Output integrity validation now verifies H.264 video codec and dimensions, each font filename and MIME type, duplicated attachments and exact project font name membership. Symlinked font asset directories fail closed.
- `app/jobs.py` now serializes output-writing jobs **per project**, retaining unrelated-project concurrency; build-global single-flight semantics remain.
- FFmpeg remains FLAC stream-copy + selectable ASS soft subtitles + existing video background; old successfully validated MKV is preserved when any new check fails.
- Legacy projects without a valid subtitle export receipt must regenerate ASS/SRT before the next complete MKV export. A file existing alone is not sufficient to certify current content.

## Regression evidence

- [Python/Termux workflow 38388064657](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38388064657): success
- [Chromium plus real FFmpeg/libass/MKV workflow 38388064667](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38388064667): success
- New real FFmpeg tests construct a known-good MKV, then assert stale receipt, modified override between validation and replace, and mismatched video codec are rejected. Tests assert the original output bytes remain unchanged. Font symlinks/attachment identity and full/lite API gates have coverage. Held background job tests prove same-project output-writer rejection, other-project independence, and retry after completion.
- GitHub main comparison after squash merge returned `identical` at the cited merge commit.

## Reusable knowledge and boundaries

A container's successful mux and superficially correct stream inventory cannot prove it corresponds to **current authoritative project state**. Verify provenance at task admission *and publication*, and serialize writers sharing an output identity. Keep separate evidence for stream structure, decoded/raster quality, physical player compatibility and real source packages. No AAC or multi-subtitle enhancement was delivered by this bug fix.

Related historical sources: `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`, `inbox/bugs/2026-10-11-hsr-source-revision-loses-human-override-and-accepts-stale-editor.md`, `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md`. This record is a concrete new MKV publication-boundary defect, not a duplicate of editor-draft conflict handling. No automatic Canonical change.
