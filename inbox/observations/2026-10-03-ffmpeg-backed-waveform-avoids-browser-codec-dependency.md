# Observation: Render media waveforms in the authoritative FFmpeg backend to avoid browser codec dependency

Date: 2026-10-03
Status: Observation
Scope: media timing UI / waveform visualization / heterogeneous container support

## Observation

A waveform timeline does not require the browser to decode or play the source media.

In Quick-Automatic-Hardsub-Encoder, the waveform was implemented through the same FFmpeg authority used by the media pipeline:
- select an audio stream explicitly;
- down-negotiate it to mono for visualization;
- render a bounded waveform image with FFmpeg `showwavespic`;
- return only the lightweight image plus authoritative media duration to the UI;
- keep interactive cursor and trim-boundary overlays in the frontend.

This avoids making waveform availability depend on browser-native support for combinations such as MKV, AV1, ALAC, FLAC, or unusual multitrack inputs. The same UI contract can be backed by Web FFmpegKit, a Windows localhost bridge, or Android FFmpegKit.

## Reusable implication

For inspection-only waveform UI, prefer backend-derived visualization over a second browser-native media decode path when the application already has a trusted FFmpeg pipeline.

Benefits:
- codec/container coverage follows the backend rather than the browser;
- no full decoded-audio buffer needs to cross into UI memory;
- waveform rendering remains independent from final encode settings;
- start/end markers can remain semantic UI overlays instead of being baked into waveform data.

## Limits

- `showwavespic` availability still depends on the concrete FFmpeg build and should fail explicitly when unavailable.
- A rendered waveform image is suitable for timing/navigation, not sample-level audio analysis.
- Spectrograms, loudness analysis, or per-channel diagnostics require separate data products.

Do not promote to Canonical from this single implementation.
