# Bug — HSR build-in-progress marker defeats MKV verification inside protected build

Date: 2026-10-23
Repository: `11576865/HSR-Voice-Archive-Builder`
Confirmed source baseline: `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`
Layer: **Bug / source-backed reproduction pathway and user screenshot; no product fix yet**
Status: **OPEN / FIX-PENDING** — hardware field observation; not yet verified by dedicated regression test

## User symptom
User screenshot from mobile Termux Lite browser `127.0.0.1:8765`, project shown as `evanescia`, build reported `ValueError: Cannot discard working files before MKV verification`. Job stack originates at `app/jobs.py` runner → `app/lite_server.py` run / `build_project_v02` → `app/delivery_artifacts.py` `seal_complete_delivery`. The screenshot does not establish that WAV source or encoded MKV bytes are corrupt.

## Confirmed code-level causal path

1. `app/pipeline.py:1561` runs the build within `with preserve_published_archive(out_dir, state_dir), tempfile.TemporaryDirectory(...)`. The last operation of this protected body in complete-delivery mode is `seal_complete_delivery(out_dir)` at `app/pipeline.py:1988`.
2. `app/publishing.py` `preserve_published_archive` does `marker.touch()` before yielding and removes `.build_in_progress` only upon leaving the context manager. The marker therefore remains present **during** sealing.
3. `app/delivery_artifacts.py:199–201` `seal_complete_delivery` calls `bundle_export_status(output)` and throws the exact user-visible error whenever `health["state"] != "current"`. This check runs before marking the receipt sealed or deleting any working files.
4. `app/archive_bundle_lifecycle.py:468–505` `bundle_export_status` identifies `.build_in_progress` as `build_busy`, adds `项目正在构建，完成后再封装` to `blockers`, and converts any otherwise verifiable present bundle to `state="stale"`. Thus the outer build's own safety marker deterministically blocks internal final sealing in the normal complete-build path even if the MKV and receipt had just been published.
5. Related inefficiency: `app/pipeline.py:1970` calls `bundle_export_status(out_dir)["needs_rebuild"]` **inside** the same marked scope; build_busy forces needs_rebuild=True, so the conditional can never certify a currently finished bundle solely because the build owns its own marker. An earlier pre-context fast-return is separate and may bypass work on unchanged inputs, but in-context decision is self-blocking.
6. Exception propagates through `preserve_published_archive`, which attempts to roll back the prior coherent published artifact set. If no previous product existed, the output can appear empty after failure. It would be unjustified to tell the user audio is damaged or to delete the marker/file receipt by hand.

## Repair direction / safety contract (proposed, not implemented)

- Separate **public availability** (`build_busy` blocks ordinary users/other processes) from **internal final verification** invoked by the same exclusive journal/project output writer. Introduce an explicit narrowly scoped self-owned verification path that ignores **only its own** active build marker while retaining all receipt, source signature, codec and bundle evidence checks. Do not simply bypass `health["state"]` or remove the marker early; doing either would risk deleting unverified working FLAC/SRT/ASS or publishing a mixed artifact.
- Resolve in-context `needs_rebuild` decisions with the same consistent self-owned marker policy. Do not weaken externally exposed `bundle_export_status` or claim running MKV is externally current.
- Regression test: newly generated complete MKV and receipt from the same protected build must seal successfully; public status remains busy during build; injected verification failure leaves sources untouched and rollback recovers previous published artifacts; successful seal deletes only unchanged work files after verification; Termux-lite path is included in CI and physical device retest FIELD-PENDING.
- Concrete root code path was inspected; dedicated red-to-green CI, PR, and physical device validation have not yet been performed.

## Dedup / promotion
Foundry search for exact error string found `inbox/cases/2026-10-15-hsr-imported-font-double-render-bilingual-share-and-provider-availability.md`, unrelated to this exact marker/seal race; searches for `build_in_progress seal_complete_delivery` and `preserve_published_archive bundle_export_status` returned no specific duplicate. This distinct code-level safety-lifecycle bug is recorded as Bug and left OPEN; no Canonical modification.
