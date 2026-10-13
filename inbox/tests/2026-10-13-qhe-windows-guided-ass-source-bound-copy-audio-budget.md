# Test: QHE Windows Native source-bound Guided ASS copied-audio budget through actual output

Date: 2026-10-13
Status: PASS Windows hosted Bridge execution step; latest exact-head whole workflow acceptance Pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder draft PR #105
Source head: `09ce78c5d06ba5670dfa48008e683c986a620fe9`
Workflow: Windows local smoke `38427973572`, step `Exercise real guided Windows Native two-pass and strict byte ceiling`

## Actual test path

`scripts/check-guided-budget-native.ps1` uses Windows FFmpeg to generate a short 320×180 video with two PCM audio streams. It starts the actual `windows/native-bridge.ps1` via a local token-protected HTTP API with the file selected, calls `POST /api/source-budget`, and independently remeasures an audio track's packet bytes with FFprobe.

- Negative `POST /api/encode` requests in Guided budget-rate copy-audio mode omit the receipt, replay a stale measurement ID, or change one claimed copied packet total by one byte. The Bridge rejects all before starting a job.
- Positive request includes the exact receipt. Windows Bridge creates a real Guided ASS two-pass software x264 output, with both audio streams copied. Legacy strict-budget failure/pass cases remain separately checked.
- New evidence checks locate the staged actual output, verify Native `completed` response whole-container bytes equal the on-disk file, and for each of two copied audio tracks use independent FFprobe `-show_data_hash sha256` packet hashes to compare source and output **in order**. Total source copied packet bytes must match the two measured ledger entries.
- This is backend-local actual short encode output, not a stubbed JS task. No claim of full decoded PCM or independently measured end-to-end source-reference ASS SSIM is made.

## Observed CI

The earlier source-receipt rejection contract and original Native tests passed in Windows local smoke `38427736645`. At latest code head, `38427973572` recorded the actual Guided Native step **success** (full workflow still running unrelated steps at initial intake). Other platform workflows are independent.

## Limits and separation

Other Test `inbox/tests/2026-10-13-qhe-guided-ass-measured-multiaudio-whole-file-budget.md` covers real Linux FFmpeg synthetic short MKV with two AAC tracks and Browser DOM changes. This Test adds a distinct Windows Native selected-source measurement/receipt authorization check and real two-audio copied output payload identity.
Corresponding Bug: `inbox/bugs/2026-10-13-qhe-guided-native-copied-audio-cost-receipt-not-validated.md`.

Not verified: 10-bit/HDR, VFR, long movie, FLAC re-encode size, precise trim cost, Android/Web source metering, physical Windows client, final exported file in external players, multi-candidate actual ASS quality or guaranteed arbitrary target-size delivery. No Canonical promotion or release claim.

## Follow-up: do not trust request.expectedAudioTracks for receipt enforcement

QHE `775bf4b6a50d44f1e4a313d4f96c95da3ada0d8c` moves the legacy request's copy-audio receipt gate behind `Get-ProbeMedia`. It requires the declared expected track count to equal the actual selected Native source's `audioTracks` and gates cost receipt on that probed number, preventing the previous client-supplied zero-count bypass. Negative case `Assert-GuidedCopyReceiptRejected $null 'forged zero-track count' ... 0` was added at `f0dbe3c918cc4b9183f844e74794695e28f7b80f`; source-contract assertions updated `ad917ef050f88158b67592c7cd05d5a1dde1cb22`.

Earlier exact-code `09ce78c` had all nine principal GitHub workflow gates SUCCESS, including real Windows output and full two-audio packet hashes. The newer zero-count guard exact-head `ad917ef` CI was in progress at this note update, so do not treat its new negative case as already passed.
