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

## Repair checkpoint — PR #195 (2026-10-20)

`download_resolved_audio` now ignores `.part`/unrelated files, validates audio headers and indexed member suffixes, streams bounded 128 MiB downloads to fsynced temporary files and atomically publishes only after checks. Added regressions for interrupted `.wav.part`, malformed existing media, format mismatch, private URL and download budget. URL checks are defense in depth, not a full DNS-validated outbound networking sandbox.

Patch: [HSR PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) branch `fix/hsr-archive-publish-safety-20261020`. Exact tested head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2`: Python 3.11/3.12/3.13, Termux Lite surface, real libass and seven ASS workflow successful; browser workflow still in progress at this writing. Physical Android, actual Hugging Face network and abrupt power-loss runs not performed. Remain at Bug/Observation level; do not update Canonical automatically.

## Main integration (2026-10-20)

HSR [PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) merged via squash to `main@fd9dfca282c7fce7806b37d748261337da3bc831`. Exact PR head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2` passed [`tests` #39360131642](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131642), [`seven ASS` #39360131709](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131709) and [`subtitle browser` #39360131588](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131588). Merge-commit CI and deployed / real-device acceptance should be tracked independently. Canonical unchanged.

### Post-merge main CI closure

Exact `main@fd9dfca282c7fce7806b37d748261337da3bc831` succeeded in [`tests` #39360425594](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425594), [`seven ASS` #39360425575](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425575), [`browser evidence` #39360425570](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425570), and [`Pages build/deploy` #39360425088](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425088). Real Android/user legacy MKV and abrupt power-loss field tests are still Pending. Canonical unchanged.
