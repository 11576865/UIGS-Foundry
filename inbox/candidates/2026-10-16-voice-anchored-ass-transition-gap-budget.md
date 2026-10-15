# Candidate: Voice-anchored ASS transition envelopes with a shortest-gap budget

Status: Candidate
Date: 2026-10-16
Product evidence: HSR-Voice-Archive-Builder PR #185 (still unmerged, CI and device acceptance pending)
Domains: subtitle timing, interaction safety, animation, user-configurable constraints

## Observation and user intent

A user reported that retaining subtitles fully visible throughout inter-voice silence is undesirable, but restricting the entire subtitle ASS event to the PCM speech boundaries makes fade-in and fade-out consume the *spoken* display interval. Their intended split has three clocks:

1. **Speech interval**: authoritative PCM voice start -> PCM voice end, which remains the full-opacity, full-legibility interval and the source for generated karaoke timing.
2. **ASS effect envelope**: can begin before speech for fade-in and end after speech for fade-out, using adjacent silence.
3. **True clear gap** between entries: the remaining interval after previous fade-out and next fade-in.

For adjacent clips separated by gap `G`, requested `F_out + F_in` leaves `G - F_out - F_in` without text. A specific user-requested decision rule for this product is to warn strictly above **60%** of the *shortest* adjacent real PCM gap, and prevent further increase above **100%**. Large chapter breaks must not be used to raise the safe bound for shorter between-voice pauses. At exactly 100%, no clear gap remains, but the fade envelopes need not overlap.

The user also requested removal of unrelated arbitrary Fade caps or preset overrides that would silently change manually selected duration. A safety constraint should be derived from source data, not from an opaque global `5000 ms` input limit or auto-derived `80/150/300 ms` replacement.

## Engineering design proposed in HSR

- Store/read PCM `start_seconds` and `audio_end_seconds` as immutable source timing. Keep SRT strictly speech-aligned; enlarge only ASS event envelopes around a cue, and never shift karaoke onset relative to speech.
- Compute fade envelope per neighboring clip pair. When a gap is insufficient, protect against overlap; the settings UI and server should normally block **newly increased** invalid requests, while allowing historic over-limit settings to be reduced.
- Expose a source-linked gap budget and live remaining-clear-silence diagnostic. Warning `> 60%`, reject new increases `> 100%`, admit exactly 100%. Distinguish unknown pre-build configured gaps from actual post-build manifest PCM gaps.
- Apply the same timing to all generated subtitle layers (text, cards, overlay, HUD) and validate transition behavior in actual playback, including very short gaps and first/last entry boundaries.
- Avoid hidden clamping and replace arbitrary Fade input maxima with contextual constraints. Changes in the gap profile must invalidate previously computed safety diagnostics.
- Keep product-specific numerical thresholds in Candidate/Case, **not Canonical**, until separately justified.

## Evidence links and verification

- HSR branch `fix/ass-export-progress-20261016`, PR https://github.com/11576865/HSR-Voice-Archive-Builder/pull/185
- Implemented in source: `app/subtitle_fade_budget.py`, `subtitle_layout/ass_writer.py`, `subtitle_layout/kinetic_motion.py`, FastAPI/Lite settings routes and inspector controls
- Regression fixtures: `tests/test_subtitle_voice_only_display.py`, `tests/test_subtitle_fade_budget.py`
- **Pending**: exact-head CI; physical Android/Termux export, FFmpeg/libass temporal playback and user acceptance

## Deduplication

- `inbox/candidates/2026-10-02-co-registered-temporal-layers-subtitle-timing.md` covers visual alignment of temporal layers in an editor, but does not define the distinct speech, ASS effect and clear-gap interval budgets.
- `inbox/bugs/2026-10-11-hsr-karaoke-absolute-word-time-gaps-lost.md` covers source-aligned word onset preservation and pre-roll shifting; this Candidate extends the temporal contract to user-adjustable effect envelope constraints.
- `inbox/cases/2026-10-14-ass-native-fade-blur-draft-commit-guards.md` covers transactional draft safety for native ASS fade editing, but not source-audio-derived fade budgets.

**Status remains Candidate. No Canonical changes from this one HSR design discussion.**
