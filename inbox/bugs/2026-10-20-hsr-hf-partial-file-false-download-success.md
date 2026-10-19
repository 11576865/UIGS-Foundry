# Bug candidate — HSR Hugging Face partial audio may be counted as successfully obtained

Date: 2026-10-20
Level: **Bug / source-confirmed logic; end-to-end provider regression pending**
Project: `11576865/HSR-Voice-Archive-Builder`
Reviewed exact main: `dea5411312ed3e819864f1915f4f2008f938cba3`

## Concrete path
At [`app/huggingface_audio.py#L255-L286`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/huggingface_audio.py#L255-L286), `download_resolved_audio` checks `list(destination.glob(stem + ".*"))` and treats any match as `{"status":"exists"}`. The same routine writes downloads to `<stem>.<ext>.part`, without guaranteed removal on write failure. Python's `Path.glob("voice_001.*")` matches `voice_001.wav.part` even when no playable `voice_001.wav` exists. The standard library matching behavior was independently reproduced, but the full HSR download routine was not executed locally.

At [`app/server.py#L1665-L1790`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/server.py#L1665-L1790) and the corresponding Termux Lite route, all `downloaded["completed"]` filenames feed the `successful` set used for incremental index rows. Copy-to-staging separately ignores names ending in `.part`. `confirmed_reference_metadata` also counts any completed row without checking the download status or audio integrity.

## Consequence
A failed download can leave a partial file that is accepted on retry, reported as successful, yet excluded from the rebuilt source directory; the resulting index may refer to nonexistent voice audio. An unrelated `<stem>.txt` or malformed audio can similarly pass the wildcard existence check.

## Repair/verification gate
- Exclude `.part` and non-audio extensions from existing-file discovery; verify the actual media structure, expected source identity/hash and language/member ownership.
- Stream downloads to bounded temporary files, safely clean up failures, and publish only validated final files.
- Add a regression with a preexisting `voice_001.wav.part`, then run provider apply and prove that no success/index commit occurs until a verified audio file is present.
- No user-device bug claim; no Canonical promotion.

## Dedup
This is different from prior HSR source-revision publication observations: it is an **audio-acquisition completeness predicate** before an otherwise-successful incremental Apply.
