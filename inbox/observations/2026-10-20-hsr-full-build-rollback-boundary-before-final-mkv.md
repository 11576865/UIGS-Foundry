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
