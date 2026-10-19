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
