# Observation — HSR full-build rollback scope ends before final MKV publication

Date: 2026-10-20
Level: **Observation / source-confirmed; fault-injection and physical-device acceptance pending**
Project: `11576865/HSR-Voice-Archive-Builder`
Reviewed exact main: `dea5411312ed3e819864f1915f4f2008f938cba3`

## Source evidence
- [`app/pipeline.py#L1561`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/pipeline.py#L1561): `with preserve_published_archive(out_dir, state_dir)` wraps manifest/FLAC/SRT/ASS/report work.
- [`app/pipeline.py#L1948-L1989`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/pipeline.py#L1948-L1989): the final complete `ArchiveBundleExporter.export(...)` and `seal_complete_delivery(out_dir)` run **after** the context manager exits.
- [`app/publishing.py`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/dea5411312ed3e819864f1915f4f2008f938cba3/app/publishing.py): rollback restores some generated files only when an exception crosses its active scope. Its archive list also does not include `archive_bundle_receipt.json`.
- `tests/test_archive_publication.py` checks encoder/final-stage errors within the protected phase; no seen injected failure at the **post-context full MKV** stage.

## Failure hypothesis for regression
1. Start with an existing sealed complete MKV and matching voice clock/receipt.
2. Change an audio timeline input and run a complete rebuild.
3. New manifest, FLAC, ASS/SRT, build_report and final stage record successfully publish during the protected phase.
4. Inject an exception in `ArchiveBundleExporter.export()` (e.g. FFmpeg failure), after the rollback context has ended.
5. The previous MKV bytes remain on disk, but newly written manifest/output sources and old bundle receipt refer to different generations. `require_bound_voice_timeline` may reject playback from the retained old MKV.

This is **not** evidence of a user-visible occurrence yet; the incomplete transaction envelope follows from exact-current-main control flow.

## Proposed test and repair
Add a deterministic source+receipt+manifest snapshot assertion for failure injected after source phase but before final MKV replacement, and another after MKV replace but before sealing. Implement a unified publish generation or an explicit rollback boundary around the final stage, preserving source/media/receipt coherence. Do not overwrite old verified media merely to make a test pass.

## Dedup
Existing `inbox/bugs/2026-10-13-hsr-mkv-stale-ass-and-output-writer-race.md` concerns stale source and same-project writer checks at mux admission/publication. This observation concerns **full project-build rollback scope** and distinct failures after the earlier protected stage. No Canonical change.

## Repair checkpoint — PR #195 (2026-10-20)

Full build now keeps `ArchiveBundleExporter.export` and `seal_complete_delivery` inside `preserve_published_archive`, and the rollback list includes `archive_bundle_receipt.json` and `subtitle_export_receipt.json`. A new real-FFmpeg regression in `tests/test_archive_publication.py` injects a final-MKV export failure and asserts byte-identical old manifest, MKV, both receipts, build report and checkpoint, with no leftover build marker.

Patch: [HSR PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) branch `fix/hsr-archive-publish-safety-20261020`. Exact tested head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2`: Python 3.11/3.12/3.13, Termux Lite surface, real libass and seven ASS workflow successful; browser workflow still in progress at this writing. Physical Android, actual Hugging Face network and abrupt power-loss runs not performed. Remain at Bug/Observation level; do not update Canonical automatically.

## Main integration (2026-10-20)

HSR [PR #195](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/195) merged via squash to `main@fd9dfca282c7fce7806b37d748261337da3bc831`. Exact PR head `cdc07676b98fef2c01b04e5b0528ead2cdf7a8f2` passed [`tests` #39360131642](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131642), [`seven ASS` #39360131709](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131709) and [`subtitle browser` #39360131588](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39360131588). Merge-commit CI and deployed / real-device acceptance should be tracked independently. Canonical unchanged.
