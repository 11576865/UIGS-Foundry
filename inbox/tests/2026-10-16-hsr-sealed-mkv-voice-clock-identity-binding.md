# Test — Sealed MKV voice clock binding independent of editable subtitles

Date: 2026-10-16
Status: Test / exact-head CI passed / HSR main merged / Android device acceptance pending
Project: [HSR-Voice-Archive-Builder](https://github.com/11576865/HSR-Voice-Archive-Builder)
Implementation: [PR #193](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/193), tested head `7c2a01f6b8784a9d1c85a1a6667f560248f7a2c2`, merged `main@01ad440bf77ea6cfec4ba24c494bd38cd8205053`

## Risk

Existing artifact provenance of the sealed MKV checked the container signature and optional source working-file signatures but did not bind the saved `manifest.json` PCM voice clock. After a manual edit or unintended replacement of voice start/end times, the MKV could be intact but a cue-specific preview would extract the wrong audio interval. Generating new ASS-internal subtitles could then rely on that wrong timeline.

## Bounded test contract and fix

- For new MKV publication, compute a SHA-256 over **ordered cue identifiers, `start_seconds` and `audio_end_seconds`**, stored as optional `voice_timeline_sha256` in the MKV publication receipt. Translation, original text, corrected subtitle text, styling, fonts, position, karaoke and Fade are deliberately excluded.
- On selected-voice preview, internal ASS export preflight and recovery of a FLAC from a sealed MKV, require the current voice-clock identity to match that receipt if present.
- A normal bilingual text edit after sealing does **not** trip this check.
- A post-sealing timing modification trips the check before ASS writes (manifest, subtitle receipt, old MKV unchanged by the refused operation), and before audio preview extraction.
- A legacy receipt **without** the optional field remains readable for compatibility. It must not be reported as possessing the new voice-clock evidence.
- This does not attempt to guarantee cryptographic identity of a valid independently regenerated FLAC's decoded samples. It is a **manifest-clock to known MKV publication** binding, not a substitute for full audio-content provenance.

## Evidence

Exact-head CI:
- [Python unit and Termux Lite](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38888894751): success
- [Seven ASS requirements](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38888894516): success
- [Chromium and libass artifact](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38888894590): success

Pending physical Android/Termux verification on a real user project. Existing output receipt mismatches and missing or corrupted files are not silently repaired.

## Deduplication and promotion

Foundry was searched for sealed MKV voice timeline binding / manifest clock identity. Existing tests include deletion of upstream WAV packages and reuse of MKV audio; those do not cover deliberate **clock modification while the sealed MKV stays byte-identical**. Store this as a separate Test. No Canonical rule change on a single project observation.
