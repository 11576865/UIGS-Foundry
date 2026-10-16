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

## Continuation — Effects preview also needs the shared sealed-audio gate (PR #189)

The user uploaded a further Effects screenshot after rebuilding MKV. Selecting another cue still failed before rendering with the generic missing FLAC / verified MKV warning. The exact on-device artifact/receipt predicate is not exposed by that screenshot, so no device cause can be asserted.

HSR PR #189 unifies `app/effect_voice_preview.py` with `bundle_audio_source_status()` rather than implementing a second, generic receipt check. It now surfaces the exact failed provenance precondition and the selected project's resolved output directory. An existing sealed MKV with matching artifact identity stays reusable for voice preview when a style save makes its subtitle receipts stale.

New real FFmpeg integration: complete MKV with default FLAC → `seal_complete_delivery` discards independent FLAC/ASS/SRT → style receipt marked stale → select a *different* manifest cue → resolve sound from the sealed MKV → produce/decode real WebM video with Opus audio and expected pre/post Fade. This was executed successfully in the `libass-artifact` job of [workflow 38866876020](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38866876020), exact head `05fc559e`, merged to `main@f417e4794e752c4780bb06d7563614315bde4c6a`.

**Boundary:** This demonstrates that the *normal* sealed path is valid. It cannot explain an Android project's **specific** missing, malformed or mismatched receipt, or project/output path identity. If the real device still reports an untrusted source after updating, inspect that exact diagnosis before any repair of user artifacts. Never adopt an arbitrary MKV as trusted by filename alone.

## Continuation — codec-aware preflight before writing ASS/SRT (PR #192)

2026-10-16: A second source-order gap was discovered. `bundle_audio_source_status` is intentionally a **cheap identity/size test**. For `continuous.flac`, it returns available as soon as the non-symlink file is nonempty; it cannot distinguish valid lossless audio from truncated garbage. The previous ASS-internal job then rewrote manifest, SRT, ASS and provenance before FFprobe failed inside the final MKV exporter. This violated the desired preflight-before-mutation boundary even where the source existence test returned success.

[HSR PR #192](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/192) merged into `main@1fd6a4829a631f6af8ad085a42be9c96b009ea8d` from exact tested head `cbb8e5eaa2de7000a02bf7e571072daf03d64cd9`.

- The explicit inner-ASS path runs `verify_internal_ass_audio_source` **before** writing any subtitle or receipt. FFprobe must inspect the selected source, and the first audio stream must be FLAC. Identity matching of sealed MKV remains an independent prerequisite. No setting-save auto-generation is added.
- Regression inserts nonempty unparseable `continuous.flac` and verifies the previous manifest, ASS/SRT and receipt remain byte-identical after the rejected job; it also rejects a wrong primary audio codec and accepts a validated FLAC stream.
- All exact-head workflows passed: [Python/Termux 38885406173](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38885406173), [seven ASS 38885406175](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38885406175), [Chromium/real media 38885406385](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38885406385).

**Limitations:** FFprobe codec discovery is not a full-duration audio decode or verification that every PCM sample matches the manifest. It is a bounded early rejection of clearly invalid sources. The user's physical Android MKV receipt and playback are still not inspected. A nonempty but valid FLAC from a different archive generation can require additional audio-to-manifest identity controls. No Canonical promotion.
