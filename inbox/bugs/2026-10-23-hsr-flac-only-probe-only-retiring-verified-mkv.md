# Bug — FLAC-only delivery could retire a verified MKV after metadata-only FLAC probe

Date: 2026-10-23
Project: `11576865/HSR-Voice-Archive-Builder`
Source baseline: `main@16a81eb9ce68c0a9aa2f6a6113e3da1aedfff548`
Fix PR: [#207](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/207)
Layer: **Bug / source-backed unsafe success path + fault-injection regression, not Canonical**
Initial status: **FIX IN PR / EXACT-HEAD CI PENDING / MERGE PENDING / FIELD PENDING**

## Root cause

`app/delivery_artifacts.py` `publish_flac_only(output)` selects an existing `continuous.flac` or extracts the primary FLAC from the prior sealed MKV, then inspects the file using `ffprobe` to require a nonempty file with exactly one FLAC audio stream. The code then deletes `HSR_Voice_Archive_Bundle.mkv` and its authenticated receipt, plus SRT/ASS/legacy black output.

**A codec/stream-count probe only establishes container metadata.** It does not prove every FLAC frame can be decoded. A pre-existing damaged or partially written working FLAC can be recognizable by FFprobe while containing missing or invalid audio frames. This could result in the *only* previously verified MKV being removed and a damaged FLAC becoming the sole deliverable. The analogous ASS-internal path already enforced `_verify_primary_flac_decodes(source)`, so this is a source-backed inconsistency.

## Repair (PR #207)

- Explicitly reject symlinked primary FLAC sources.
- Reuse the existing `_verify_primary_flac_decodes(audio)`: FFmpeg `-xerror` full-stream decode, source inode/size/mtime/ctime stable before/after and no symlink.
- At the final destructive commit boundary, recheck the same source-file identity, so a non-cooperating edit that replaces the FLAC between full decode and receipt/MKV removal is refused.
- Leave the previous verified MKV, its receipt, and still-present working inputs intact whenever full decode or identity verification fails; preserve normal lossless profile switching.

## Tests / evidence scope

New real-media tests in `tests/test_hsr_single_deliverable.py` create an actual FFmpeg MKV with two subtitles, seal it and preserve receipt bytes:
1. A garbage working FLAC accompanied by deliberately permissive metadata-only FFprobe result must fail **actual FFmpeg full decode** rather than retire the MKV/receipt.
2. An extracted, fully valid FLAC is swapped after decode but before prior MKV/receipt removal; expected identity fence stops the transition and leaves the prior verified MKV intact.

Existing real-media successful sealed-MKV-to-FLAC and FLAC-to-MKV profile-switch regression continues to run. This is not a physical power-loss ACID guarantee or a live Android field case.

## Dedup / acceptance

Search of UIGS-Foundry for `full FLAC decode before deleting MKV`, `publish_flac_only` and `FLAC only stream probe corruption` found related earlier audio publication and track-refresh observations but **no exact project Bug** for a metadata-only verification immediately preceding retirement of the sole verified MKV. Do not conflate this with the older HSR partial-file Hugging Face download Bug or #203 internal MKV sealing marker deadlock.

**Pending:** exact #207 final PR-head CI, merged-main CI, and an end-user physical Termux/Windows long-archive retest. No Canonical promotion.
