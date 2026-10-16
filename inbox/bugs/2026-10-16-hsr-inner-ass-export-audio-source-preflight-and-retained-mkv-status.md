# Bug — HSR inner ASS export checks sealed-MKV audio only after mutating subtitle artifacts

Date: 2026-10-16
Status: Source fix merged, exact-head CI green; physical Android artifact provenance unresolved
Project: `11576865/HSR-Voice-Archive-Builder`
Merged repair: [PR #188](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/188), main merge `3450626828c3eeb7a3c594384e9d3b41835d6e7b` from `9caa6b49874dbfc1579b070196d9b84d3aba453f`

## User-observed symptom

The user states that a complete MKV was built successfully, then immediately after saving layout changes the app treats the result as unavailable. A following explicit ASS-internal generation job fails with `新字幕尚不能安全封装进 MKV：既没有独立 FLAC，也没有已验证 MKV 音轨` even while an old MKV may still exist on device. The displayed screenshot proves the job error, but **does not provide the on-disk MKV, its `archive_bundle_receipt.json`, or the project output directory**; the precise cause of that particular device's missing audio-provenance evidence remains undetermined.

## Source diagnosis

- A settings save marks the ASS subtitle export receipt style-stale; this legitimately makes the **current subtitle version** outdated but should not delete or invalidate the underlying sealed MKV's lossless audio identity. In the present code `bundle_export_status` recognizes audio from either an independent `continuous.flac` or a sealed MKV with matching publication artifact signature.
- `app/auto_delivery.py::queue_ass_regeneration` previously called `refresh_subtitle_artifacts_from_settings` before checking `bundle_export_status(...).can_generate` in `publish_generated_ass_complete_mkv`. When no certifiable audio was available, an explicit internal export first rewrote ASS/SRT/manifest and export receipts, then failed. This ordering is source-confirmed independently of the device's missing provenance cause.
- A file's presence is not the same as a provenance-verified, current MKV; an older, unsealed, modified or incorrectly associated MKV must be preserved, reported precisely and not automatically promoted to a trusted audio source.

## Repair and checked invariants

- Add `bundle_audio_source_status` to distinguish independent FLAC, sealed same-identity MKV, missing MKV, symlink, unsealed publication, missing/bad receipt, and modified MKV identity. Report the precise gate that prevents reuse.
- Explicit internal ASS export preflights certifiable lossless audio before modifying subtitle files, manifest or receipt. Failures preserve prior ASS/SRT/MKV; independent external ASS export remains separate.
- Bundle status states that a stale but sealed and intact old MKV remains present and that its FLAC audio remains reusable for regeneration. Only current subtitle provenance is stale.
- New unit regressions check immutability on missing audio, unverified legacy MKV, unsealed receipt, altered old MKV, and sealed but style-stale MKV with reusable audio. Existing Python 3.11/3.12/3.13, Termux Lite, real libass and seven-ASS CI workflows passed for `9caa6b49`.

## Important remaining boundary

There is no on-device evidence showing whether the user's earlier MKV was sealed, the receipt was lost/invalid, its signature disagreed or the selected project/output path changed. The exact original symptom **cannot be claimed fully repaired** without inspecting the next error detail against the device's project files. Do not delete or silently adopt an unverifiable old MKV; do not claim an old MKV is current after a new layout save.

## Deduplication

Existing `inbox/bugs/2026-10-13-hsr-mkv-stale-ass-and-output-writer-race.md` documents accepting stale ASS and overlapping writers. Existing `inbox/observations/2026-10-13-hsr-mkv-track-refresh-vs-full-rebuild.md` records product preference for full regeneration and retaining the previous artifact. This Bug record isolates the **preflight-before-subtitle-mutation ordering**, the separate audio-source gate and the user-facing distinction between a retained stale MKV and an unverified one. No Canonical change.
