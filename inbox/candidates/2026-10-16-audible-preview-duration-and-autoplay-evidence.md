# Candidate — Audible preview needs stream, duration and playback-gesture evidence

Date: 2026-10-16  
Status: Candidate; validation pending  
Scope: media preview UX, browser playback, FFmpeg provenance, async verification  
Source project: [HSR Voice PR #186](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/186)

## Observation

In HSR's Effects workbench, the user reported that preview animation stayed at 8 seconds and had no sound. Source review found several independently necessary proof layers, not one "video succeeded" flag:

- **Clip selection and timeline:** the actual selected project cue and its PCM start/end clock must be resolved on the server. An 8s browser hint must not override a longer real clip.
- **Mux presence:** FFmpeg output should contain an audio stream when an audible voice preview was requested. Visual-only success is insufficient.
- **Output duration:** existence of an audio stream is also insufficient: FFprobe should assert the encoded media duration still matches the source-resolved preview duration within documented codec/frame tolerance. An 8s output for a requested 9.5s voice-backed preview must fail, not be presented as final.
- **Browser user gesture:** browsers may disallow autoplay *because the preview has sound*. A rejected `video.play()` promise must not be swallowed; native controls and an explicit "click Play for sound" fallback must remain available.

## Code-level implementation

HSR project resolves real PCM voice media and duration in `app/effect_voice_preview.py`, renders real audio in `app/ass_preview.py`, and checks the encoded stream and duration before returning bytes. `app/static/index.html` displays an actionable warning if audible autoplay is rejected without mislabeling the video as silent. Regression fixtures in `tests/test_effect_voice_and_karaoke_source_only.py` inject a stream-count-valid but too-short output and check rejected autoplay message ownership.

## Evidence and limits

- Specialized seven-ASS GitHub workflow for earlier PR head passed; this new bounded head requires its own exact-head CI.
- No HSR real-project device playback was observed in the agent session. The user remains the authority for perceived sound synchronization and output acceptance.
- Avoid claiming physical audio presence, actual audible waveform content, or user-gesture success from metadata tests alone.

## Deduplication

Existing ASS preview cases cover frame/time mapping, raw preview parity, aspect ratio, and video intake. None located in filename scan addresses this specific **three-layer audio–duration–browser gesture** completion contract. Keep this as a separate Candidate; do not automatically edit Canonical.

## Continuation — browser fixture must honor the stronger audio contract (2026-10-16)

On [HSR PR #186](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/186), the dedicated seven-ASS workflow passed at head `e99a616`, while Chromium evidence run `38835128320` timed out waiting for the decoded video preview. Source inspection confirmed the browser-test route returned an older **1.5-second silent WebM**, and its mocked response had only a background-origin header. The application now legitimately requires `X-HSR-Preview-Audio: project`, a positive `X-HSR-Preview-Duration`, and a named project cue before reporting sound-backed video success.

A narrow follow-up changes only `tests/browser_visual_evidence.py` fixture to produce a decodable WebM containing both video and a real synthetic tone, with FFprobe stream-type verification, and supplies the asserted preview identity headers; no production guard was relaxed. The browser fixture is **not** evidence that a genuine HSR PCM sample was selected or correctly synchronized; that remains the independent FastAPI/Termux FFmpeg fixture and user-device acceptance. An adjacent Node preview test's fake `document` lacked `document.body` even though the production callback reads `document.body.dataset.workspaceTask`; its correction restores realistic browser context without bypassing image decode checks. Stale auto-preview assertions were replaced with explicit no-auto-render expectations.

**Status:** follow-up commit present on PR #186; exact-head CI and user-device listening still Pending. This is an additional observation under the existing Candidate, not a Canonical amendment.
