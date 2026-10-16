# HSR — sealed MKV identity versus visual-only Fade preview

Date: 2026-10-17
Level: **Case / merged code + PR CI verified; physical-device acceptance Pending**
Product: `11576865/HSR-Voice-Archive-Builder`
Patch branch: `fix/effects-preview-provenance-fade-20261017` — merged PR #194
Source: Android browser screenshot supplied by project user, coupled with direct GitHub `main` inspection.

## Observed failure, not a generalized diagnosis

On the real HSR Effects screen, `render-preview-video` returned an error from `bundle_audio_source_status(prefer_sealed=True)`: existing MKV identity differs from its sealed publication receipt. The screenshot does not show the actual MKV bytes, receipt fields or whether the user's media were modified. Therefore the discrepancy cannot honestly be classified as only an mtime change or only a replaced stream.

The `archive_bundle_lifecycle._signature` used only `size` and `mtime_ns`; the original receipt had no MKV content digest. A media timestamp touch can therefore cause a false rejection, while identical metadata alone cannot cryptographically certify media. Independent FLAC working files are routinely retired after sealing, so a failed sealed-MKV check can prevent voiced preview.

The user's second request concerned absent Fade animation in preview. `render_ass_preview_png` is necessarily one still frame; `render_ass_preview_video` and `ass_writer._voice_fade_windows` already implement actual ASS `\\fad` animation. Blocking the whole dynamic video when audio provenance fails prevents a user from inspecting even the genuine rendered Fade envelope.

## Submitted bounded repair

1. New publications store `artifact_sha256` in addition to legacy stat data. `_bundle_artifact_matches` checks the content digest for new receipts (using a narrow inode/size/mtime/ctime cache), while old receipts without a digest retain the exact legacy stat fence. Metadata-only changes to new receipts need not block authentic MKV reuse. Changed media bytes still block. No silent resigner for legacy receipts.
2. A sealed MKV mismatch does not authorize an arbitrary leftover `continuous.flac`; only a file with the exact recorded source stat can act as a recovery input.
3. Explicit render-preview route allows `resolve_effect_voice(..., allow_visual_only=True)`. If the source cannot be trusted but the manifest clock binding still holds, render a **silent video** through the real ASS writer using the selected cue's bounded lead-in/out. Do not open the unverifiable MKV, do not include footage audio instead, and report `X-HSR-Preview-Audio: visual-only`.
4. The browser accepts this explicitly labeled mode and displays a warning that real voice synchronization is unverified. Normal verified voiced previews still report `project`. `require_bound_voice_timeline` continues to reject differing sealed and manifest PCM clocks.
5. Added Python tests for modified bytes at equal size/restored mtime, legacy timestamps, video-only Fade envelope, absent audio stream, and API audio status.

## Follow-up: repeated failure is not a regression against deployed patch

Second Android screenshot again shows `v0.9-N+01ad440`, the base commit. On 2026-10-17 PR #194 remains **Open/unmerged**, so the user's repeated error is from the original running binary, not evidence that the PR code was tested on-device.

The user additionally reports `生成 ASS` failure after changing selected subtitle cues. Actual code shows `queue_ass_regeneration` calls `verify_internal_ass_audio_source` before mutation in complete-delivery mode. This shares the sealed audio gate with `resolve_effect_voice`; both may fail when complete-mode sealing has retired loose FLAC and MKV identity cannot be verified. Changing cue ID has no authority to repair a broken publication receipt.

New PR #194 follow-up includes:
- Shared `diagnose_bundle_audio_source` read-only classification: `legacy_stat_mismatch`, `artifact_content_mismatch`, `voice_timeline_mismatch`, `missing_receipt`, verified, etc.; active-project authenticated endpoints for FastAPI and Termux Lite.
- An explicit user recovery path: independent external ASS remains available without granting false MKV trust, while full archive recreation from original voice data requires an additional manual action.
- Browser preflight for `生成 ASS（内）`; no repeated job creation when sealed audio is unprovable, and no implicit FFmpeg rebuild / receipt overwrite.
- An integrated regression contract requiring internal ASS failure to leave the old MKV unchanged while allowing `生成 ASS（外）`.

The old stat-only sealed archive **cannot** be authenticated after a stat mismatch without independent trusted evidence. A rebuild using original sources (or verified recovery evidence) remains required to restore *voiced* playback; silent Fade animation is not a source-repair substitute.

Earlier exact PR head `5325c392` had three PR CI workflows marked successful, but the expanded diagnostic changes are at a newer head with CI pending. Neither result is Android/Termux field evidence.

## Final PR integration evidence (2026-10-17)

- HSR PR [#194](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/194) **merged** into `main`, squash SHA `dea5411312ed3e819864f1915f4f2008f938cba3`.
- Exact PR head `b60f1be5b116772862d60c5b534ab87091fd6999` passed `tests` run `38935511796`, `HSR seven ASS requirements` run `38935511697`, and `HSR subtitle browser evidence` run `38935511721`. These are repository CI results, not user device/media validation.
- Main file re-read confirmed `diagnose_bundle_audio_source` and `artifact_sha256` are now present.
- The user's browser screenshot remains `01ad440` and pre-dates integration. Real Termux deployment requires `git pull --ff-only`, termination of the former server, `bash run_termux.sh`, browser refresh, and actual project reproduction.
- **FIELD-PENDING:** do not declare the original legacy MKV restored, authenticated, or repaired on-device. If legacy metadata differs and no previously recorded content digest exists, the voiced preview and inner ASS cannot be automatically trusted. Explicit rebuild from original sources or independently proved source restoration is still necessary.

## Evidence boundaries

At writing, this is submitted source and static review, not a demonstrated Android fix. Corresponding CI and real-device FFmpeg/libass, browser decode, imported fonts, and authentic large project artifacts have not yet been verified. Existing legacy MKV whose metadata no longer matches its receipt cannot be automatically authenticated: rebuild from trusted sources or independent verification is still required for voiced preview.

## Deduplication

This Case extends, not replaces:
- `inbox/bugs/2026-10-16-hsr-inner-ass-export-audio-source-preflight-and-retained-mkv-status.md` — input provenance and inner ASS gating.
- `inbox/bugs/2026-10-16-hsr-effect-preview-tail-fade-envelope-exceeds-video.md` — terminal Fade video envelope.
- `inbox/candidates/2026-10-16-audible-preview-duration-and-autoplay-evidence.md` — audible preview/actual playback proof.
- `inbox/observations/2026-10-16-softmux-output-evidence-stale-same-metadata-source-file.md` — metadata-versus-byte-identity distinction in another project.

Do not promote a single screenshot or this unvalidated patch to Canonical.
