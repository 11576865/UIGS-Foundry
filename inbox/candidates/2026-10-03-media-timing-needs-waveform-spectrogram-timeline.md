# Candidate: Media inspection workflows need timeline waveform/spectrogram, not merely playback controls

Date: 2026-10-03
Status: Candidate
Scope: subtitle timing / media trimming / verification UI

## Observation

For subtitle timing, dialogue boundary finding, and practical video trimming, a conventional media player timeline is insufficient. Users benefit from:
- audio waveform over time;
- optional spectrogram;
- synchronized playhead;
- zoom/pan;
- frame stepping;
- cue/segment overlays.

Existing tools already provide this effectively:
- Subtitle Edit combines video playback with waveform/spectrogram and subtitle cue overlays;
- LosslessCut combines video playback, thumbnails and audio waveform for cutting.

## Candidate principle

When a media workflow requires timing decisions from audio, prefer integrating or reusing a waveform/spectrogram timeline rather than expanding a generic player into a full editor.

Do not promote to Canonical from this single observation.
