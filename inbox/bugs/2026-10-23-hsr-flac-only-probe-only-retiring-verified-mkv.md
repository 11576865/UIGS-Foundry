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

## Exact PR-head red-to-green distinction (2026-10-23)

Original PR head `a2321a8fd750a83850a4dcc962fc8b382d9d6881` passed Python, Windows, seven actual ASS, historical interop, and sustained multiprocess tests, but [browser/media workflow #39911699243](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911699243) failed on the two **new regression test assertions**, NOT from full FLAC decoding or audio loss. The tests created deliberately corrupt/new loose FLAC files and incorrectly expected `bundle_export_status` to report `current` even though the user-visible working sources had changed. Product status correctly returned `stale`. Original sealed MKV bytes and receipt bytes were identical.

Final PR head `db81280c8d29a1e2da85cff09931c9d1dafb96c7` corrected the test oracle: while an untrusted loose FLAC exists, public status must be `stale`; `_bundle_artifact_matches(MKV, authenticated_receipt)` and sealed receipt must still validate; removing just the test's bad loose FLAC returns public state to `current`. **No production-state waiver was introduced.**

At final head, success:
- [Python 3.11–3.13, Termux Lite, real libass #39911973869](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973869)
- [Native Windows locks and journal #39911973909](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973909)
- [Seven real ASS + MKV contracts #39911973892](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973892)
- [Long-running multiprocess journal #39911973902](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973902)
- [Pinned historical-code interoperability #39911973864](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973864)
- Within [browser/media workflow #39911973888](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39911973888), the **libass-artifact job**, which executes the new real-FFmpeg FLAC-only regression, succeeded; Chromium UI subjob was still installing browser dependencies at time of this snapshot. Entire workflow therefore Pending, PR not yet merged.

Distinguish working-source freshness from preserved last sealed-artifact provenance. Tests must not call an archive 'current' in the presence of untrusted loose inputs just to make rollback assertions pass. No Canonical change.
