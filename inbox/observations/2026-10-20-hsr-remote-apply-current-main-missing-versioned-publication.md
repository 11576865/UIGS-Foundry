# Observation — HSR current main lacks earlier guarded remote-update publication

Date: 2026-10-20
Level: **Observation / current-main code verified; crash reproduction pending**
Project: `11576865/HSR-Voice-Archive-Builder`
Exact main: `dea5411312ed3e819864f1915f4f2008f938cba3`

## Fresh authority check
Both current [FastAPI Apply code](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/server.py#L1710-L1780) and [Termux Lite Apply code](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/lite_server.py#L1510-L1560) delete `.generated/combined_audio` with `shutil.rmtree(combined)` **before** replacing it with a new staging directory. They update CSV/index/config in subsequent steps. Failure between deletion, directory replacement and config/index update can leave an incomplete generation, or remove the only remaining combined-audio copy.

PR #133 is listed as merged and its changed files included `app/remote_update_guard.py`, `app/remote_update_publication.py`, `app/remote_update_publish.py`. However, current-main recursive Git tree does not contain those three files, `combined_audio_versions`, or `incremental_revisions`; current `server.py`/`lite_server.py` instead expose destructive replacement. This is a **current-main evidence divergence** from older merged-PR/Foundry accounts, not proof of the specific historical cause. Issue [#176](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/176) already tracks controlled semantic re-landing of unported remote-update clusters.

## Test gate
Inject failure (a) after existing directory deletion but before staging move; (b) after move but before CSV/index/config publication; (c) during cancellation/restart. Assert old source and active project config remain usable, index rows resolve to exactly one present WAV/member, and a successful replacement publishes only after verification. Prefer versioned immutable staging + commit/fencing/rollback rather than copying an old branch wholesale.

## Dedup
Prior `inbox/observations/2026-10-11-hsr-remote-apply-preflight-not-transactional.md` documented repair in PR #133. This new observation specifically records the **2026-10-20 current-main divergence** and does not override historical PR evidence or assert observed user data loss. No Canonical change.

## Repair checkpoint — PR #195 (2026-10-20)

Both FastAPI and Termux Lite Apply now publish unique `.generated/combined_audio_versions/<generation>` source trees and versioned incremental index files, and never remove the previous active combined directory before the configuration switch. Shared `app/remote_apply_generation.py` provides a tested fail-safe rename boundary. Tests inject directory-publish failure and verify original audio survives; comprehensive PR #133 journal/rollback semantics and cross-process locks remain outside this patch.

Patch: [HSR PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) branch `fix/hsr-archive-publish-safety-20261020`. Exact tested head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2`: Python 3.11/3.12/3.13, Termux Lite surface, real libass and seven ASS workflow successful; browser workflow still in progress at this writing. Physical Android, actual Hugging Face network and abrupt power-loss runs not performed. Remain at Bug/Observation level; do not update Canonical automatically.

## Main integration (2026-10-20)

HSR [PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) merged via squash to `main@fd9dfca282c7fce7806b37d748261337da3bc831`. Exact PR head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2` passed [`tests` #39360131642](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131642), [`seven ASS` #39360131709](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131709) and [`subtitle browser` #39360131588](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131588). Merge-commit CI and deployed / real-device acceptance should be tracked independently. Canonical unchanged.

### Post-merge main CI closure

Exact `main@fd9dfca282c7fce7806b37d748261337da3bc831` succeeded in [`tests` #39360425594](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425594), [`seven ASS` #39360425575](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425575), [`browser evidence` #39360425570](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425570), and [`Pages build/deploy` #39360425088](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360425088). Real Android/user legacy MKV and abrupt power-loss field tests are still Pending. Canonical unchanged.
