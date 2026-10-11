# Bug: CVS speech success can label unverified bytes as audio/wav

Status: **Source-confirmed contract gap / real backend failure not reproduced**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Audited main: `184d481c8cae911643a3a059211bbd71cbece20e`
Severity: P1 output contract / reliability

## Verified source path

- `server/backends/gpt_sovits.py::_synthesize_locked()` issues an
  HTTP `/tts` request and, after a successful HTTP response, returns
  `response.read()` without checking Content-Type, RIFF/WAVE magic,
  WAV chunk consistency, frame count, or minimum payload size.
- `server/app.py::speech()` takes the bytes returned by the adapter
  and always wraps them as `fastapi.responses.Response(...,
  media_type="audio/wav")`, with success/provenance headers. It does
  not validate that the bytes are an actual WAV file.
- `server/engines/index_tts.py` and `sidecar.py` check
  `audio/` Content-Type and nonzero length, but not a canonical,
  decodeable WAV header. Thus the contract check is inconsistent
  across adapters.
- `tests/test_gpt_sovits.py` actively asserts that fake bytes
  `b"wav-data"` constitute a successful synthesis result. The
  contract tests return `b"RIFF....WAVE"` as successful audio, which
  is also not a valid complete WAV file.
- `docs/character-voice-contract-v1.md` promises `audio/wav`, and
  the user-facing Android TTS integration requires real PCM frames.

## Impact and interpretation

A backend returning HTTP 200 with an error page, JSON body, empty
or truncated content (or other incorrect bytes) can be surfaced by
CVS as a successful `audio/wav` response. That is a **source-derived
possible failure**, not proof it has occurred in a production
synthesis run.

This undermines the meaning of a green contract test: the test
proves response metadata/routing but not decodeable audio validity,
duration, sample rate, or request-identity correctness.

## Minimum repair/verification contract

1. Validate the response at the centralized audio boundary:
   actual PCM WAV RIFF/WAVE structure, bounded size and reasonable
   audio frames/duration; reject non-WAV/truncated payloads with
   classified upstream failure before returning 200 success.
2. Independently test each adapter's bad-200 responses: HTML, JSON,
   zero bytes, truncated WAV, declared type mismatch, too-large
   payload and valid minimal PCM WAV.
3. Replace synthetic strings in API contract tests with actual
   generated small WAV fixtures; require WAV decoding and frame count.
4. Add end-to-end WAV decode plus requested model/reference provenance
   validation to hardware acceptance, while preserving
   `response_format="wav"` compatibility.

## Dedup

Foundry searches for `audio wav payload acceptance`,
`HTTP 200 non WAV bytes response` and similar uncovered related HSR
media-cache observations, but no matching CVS speech-output acceptance
Bug. The existing cross-boundary-invariant Candidate is relevant; do
not duplicate a general Candidate or update Canonical.

Status **OPEN / targeted regression and fix Pending**.
