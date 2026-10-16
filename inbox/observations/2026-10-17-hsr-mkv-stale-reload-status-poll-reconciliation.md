# HSR — reload-visible stale MKV and status-poll reconciliation side effects

Date: 2026-10-17
Status: **Observation / code-verified mechanism; actual device trigger unverified**
Product: `11576865/HSR-Voice-Archive-Builder`

## User symptom and evidence boundary

User reports that every page reload displays “MKV 已过期” despite no conscious media or settings edit. We have not inspected the affected project's receipt, subtitles, fonts, MKV bytes, or exact `bundle_export.message`. It is **not proven** whether reloading causes a fresh invalidation or merely redisplays an already-persisted `stale` status.

## Verified source behavior

- `bundle_export_status(output)` is a derived status, not a test of whether the file opens: its `stale` branches include subtitle export-receipt/input changes, style-stale marker, supplemental ASS/SRT mismatch, font metadata and optional chapter audio changes, and MKV byte-identity mismatch.
- `update_project` saves project settings and calls `mark_ass_style_stale` **only when an effective `subtitle_*` field actually differs**. A no-op settings save should not invalidate; `tests/test_layout_autosave_export_boundary.py` explicitly checks this.
- `fillProject` calls `loadSubtitleLayoutSettings`, which sets `savedSubtitleSettings` from current controls without an immediate save operation. Consequently direct page load is **not shown** to rewrite MKV or subtitle receipt.
- More subtly, both the FastAPI and Termux Lite `GET /api/status` paths call `maybe_queue_complete_mkv(config)` before assembling the project summary. This is a **read-triggered reconciliation path**: when `state` is stale and `can_generate` and other gates are true, a background `archive-bundle-export` job may be queued even though the user did not press Generate. It is guarded by source-generation identity and retry backoff; it does not prove that this happened in the user's run.
- A persisted stale receipt can remain stale on every load when the user has not explicitly regenerated ASS and re-sealed the MKV; repeated display alone does not imply repeated mutations.

## Proposed diagnostic test boundary (not yet implemented)

1. Capture `bundle_export.message`, `blockers`, subtitle export `state/artifact_error`, and integrity `code` **before** navigating/reloading; capture them again afterwards.
2. Assert that a pure project read with unchanged sources never modifies receipt bytes or effective subtitle config.
3. Independently assert whether a status GET queues a writer job, including the exact source snapshot and authorization policy; separate this side effect from pure status reporting, or make it clearly visible.
4. Keep `stale`, `unverified`, `missing`, `build in progress`, and `artifact content mismatch` distinct. Never overwrite or re-sign legacy MKV without independent proof.

## Deduplication

Extends rather than duplicates `inbox/bugs/2026-10-10-hsr-durable-subtitle-edit-versus-export-refresh-failure.md` (persistent subtitle export status and autosave boundary) and `inbox/observations/2026-10-13-hsr-mkv-track-refresh-vs-full-rebuild.md` (source-backed rebuild). This observation records the *read-triggered reconciliation* ambiguity and the need to differentiate persisted warnings from a new reload mutation. Do not promote to Canonical based on one user report.
