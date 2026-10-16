# Test — HSR sealed MKV voice preview survives deletion of original external WAV package

Date: 2026-10-16
Status: Exact-head CI passed, merged to HSR main; physical-device acceptance pending
Project: `11576865/HSR-Voice-Archive-Builder`
Code: [PR #190](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/190), tested head `0c40ff40bd6c9c3bb6bad91660df424e25307ae6`, merged `728e06c1ab35e51a98329497dd172a40ab6cc0ce`
Location: `tests/test_archive_bundle_exporter.py::BundleRealFFmpegTests.test_sealed_mkv_survives_style_edit_and_real_effect_preview_has_fade_tail`

## Explicit scenario

After a successful complete MKV build, the user may delete the **external original voice WAV package**, while retaining the HSR project output. Voice preview and styled subtitle regeneration should not need to re-open the discarded original package if the completed MKV remains provenance-verified and has its first FLAC audio stream.

## Executed regression

1. Generate a real PCM WAV in an external directory, with an external index CSV.
2. Transcode that WAV once into the project's `continuous.flac`; author manifest clock and subtitle receipts.
3. Export and validate a real MKV, seal the publication and delete the project-local temporary FLAC/ASS/SRT.
4. Delete the entire original external WAV directory and its index CSV. Preserve a real `ProjectConfig.wav_source` pointing to the now-nonexistent package.
5. Mark the existing ASS style stale and select the second manifest cue. The resolver returns the **sealed MKV**, not the missing external package, as audio input.
6. Use actual FFmpeg/libass to produce WebM/Opus from the selected cue, FFprobe its expected total fade/voice envelope duration, and decode nonzero PCM. Verify MKV remains intact.

## Evidence

- Real FFmpeg test executed in [Chromium/libass artifact workflow 38868137967](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38868137967), exact-head success.
- [General Python/Termux workflow 38868138049](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38868138049): success.
- [Seven ASS requirements workflow 38868138146](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38868138146): success.

## Important distinction

The sealed MKV is the lossless **audio bytes** source after temporary `continuous.flac` cleanup; the project-owned `manifest.json` remains the **cue-to-time mapping**. `archive_bundle_receipt.json` attests MKV identity. This is **post-build preview independence from upstream sources**, not the ability to rebuild original WAV inputs or recreate a deleted project manifest/receipt. Absent or mismatched provenance still fails closed; arbitrary MKV files are not automatically adopted.

## Deduplication and promotion

Related Foundry items describe source-verified MKV publication, stale ASS and separate voice preview audio. Search did not find a dedicated regression proving *actual deletion of the original external WAV package followed by decoded audible selected-cue preview*. Record as Test. No Canonical update; Android/Termux physical playback still needs acceptance.
