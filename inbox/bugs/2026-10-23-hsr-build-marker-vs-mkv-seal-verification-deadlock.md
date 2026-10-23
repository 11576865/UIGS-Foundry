# Bug — HSR build-in-progress marker defeats MKV verification inside protected build

Date: 2026-10-23
Repository: `11576865/HSR-Voice-Archive-Builder`
Confirmed source baseline: `main@2d770d2be1bdb7356dc1f459049eb1d1d0bca71c`
Layer: **Bug / user screenshot + source-backed root cause + fixed product CI evidence**
Status: **SOURCE-FIXED / PR-MERGED / EXACT-MAIN-CI-PENDING / TERMUX-FIELD-PENDING**

## User symptom
User screenshot from mobile Termux Lite browser `127.0.0.1:8765`, project shown as `evanescia`, build reported `ValueError: Cannot discard working files before MKV verification`. Job stack originates at `app/jobs.py` runner → `app/lite_server.py` run / `build_project_v02` → `app/delivery_artifacts.py` `seal_complete_delivery`. The screenshot does not establish that WAV source or encoded MKV bytes are corrupt.

## Confirmed code-level causal path

1. `app/pipeline.py:1561` runs the build within `with preserve_published_archive(out_dir, state_dir), tempfile.TemporaryDirectory(...)`. The last operation of this protected body in complete-delivery mode is `seal_complete_delivery(out_dir)` at `app/pipeline.py:1988`.
2. `app/publishing.py` `preserve_published_archive` does `marker.touch()` before yielding and removes `.build_in_progress` only upon leaving the context manager. The marker therefore remains present **during** sealing.
3. `app/delivery_artifacts.py:199–201` `seal_complete_delivery` calls `bundle_export_status(output)` and throws the exact user-visible error whenever `health["state"] != "current"`. This check runs before marking the receipt sealed or deleting any working files.
4. `app/archive_bundle_lifecycle.py:468–505` `bundle_export_status` identifies `.build_in_progress` as `build_busy`, adds `项目正在构建，完成后再封装` to `blockers`, and converts any otherwise verifiable present bundle to `state="stale"`. Thus the outer build's own safety marker deterministically blocks internal final sealing in the normal complete-build path even if the MKV and receipt had just been published.
5. Related inefficiency: `app/pipeline.py:1970` calls `bundle_export_status(out_dir)["needs_rebuild"]` **inside** the same marked scope; build_busy forces needs_rebuild=True, so the conditional can never certify a currently finished bundle solely because the build owns its own marker. An earlier pre-context fast-return is separate and may bypass work on unchanged inputs, but in-context decision is self-blocking.
6. Exception propagates through `preserve_published_archive`, which attempts to roll back the prior coherent published artifact set. If no previous product existed, the output can appear empty after failure. It would be unjustified to tell the user audio is damaged or to delete the marker/file receipt by hand.

## Original repair requirements (subsequently implemented by PR #203)

- Separate **public availability** (`build_busy` blocks ordinary users/other processes) from **internal final verification** invoked by the same exclusive journal/project output writer. Introduce an explicit narrowly scoped self-owned verification path that ignores **only its own** active build marker while retaining all receipt, source signature, codec and bundle evidence checks. Do not simply bypass `health["state"]` or remove the marker early; doing either would risk deleting unverified working FLAC/SRT/ASS or publishing a mixed artifact.
- Resolve in-context `needs_rebuild` decisions with the same consistent self-owned marker policy. Do not weaken externally exposed `bundle_export_status` or claim running MKV is externally current.
- Regression test: newly generated complete MKV and receipt from the same protected build must seal successfully; public status remains busy during build; injected verification failure leaves sources untouched and rollback recovers previous published artifacts; successful seal deletes only unchanged work files after verification; Termux-lite path is included in CI and physical device retest FIELD-PENDING.
- This was an initial pre-fix requirement; see the completed implementation and exact PR-head CI below. Physical device validation remains pending.

## Dedup / promotion
Foundry search for exact error string found `inbox/cases/2026-10-15-hsr-imported-font-double-render-bilingual-share-and-provider-availability.md`, unrelated to this exact marker/seal race; searches for `build_in_progress seal_complete_delivery` and `preserve_published_archive bundle_export_status` returned no specific duplicate. This distinct code-level safety-lifecycle bug is recorded as Bug; source fix has since been merged as PR #203. No Canonical modification.

## 2026-10-23 source fix and PR-head CI evidence

HSR [PR #203](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/203) merged with squash commit `main@6a6410b0181b82e60528fe52f4e807911b430f4d`, after all six exact final PR-head workflows succeeded (`a7de8dfa562330d368bf77b04ef1f25be8d14577`).

- `app/publishing.py`: `preserve_published_archive` records the current protected output path in a ContextVar only during the own build transaction; the token is reset on success, rollback and exception.
- `app/archive_bundle_lifecycle.py`: `bundle_export_status(output, _owned_build=True)` is restricted to the active matching transaction and ignores only its own `.build_in_progress` blocker. Existing MKV artifact checksum, source signatures, subtitle provenance, fonts and publication receipt requirements remain enforced. Ordinary public polling still reports `stale` during construction.
- `app/delivery_artifacts.py`: `seal_complete_delivery` uses the owned exemption **if** an owned build transaction exists, or ordinary verification for historical standalone already-verified MKV exports with **no** marker. A foreign marker continues to block. On non-current input, the exception now includes the health reason. Working files remain untouched until the receipt is authenticated and sealed.
- `app/pipeline.py`: internal `needs_rebuild` decision uses the same scoped exemption so the self-owned marker cannot cause automatic redundant full MKV re-encoding.
- `tests/test_owned_build_mkv_seal.py`: owner-only first seal, public busy, standalone compatibility, no unauthorized exemption, mismatched FLAC provenance refusal with coherent old-output rollback, incomplete receipt preserves working files. `tests/test_archive_bundle_exporter.py`: **actual FFmpeg** 1.6-second FLAC+ASS+SRT → selectable MKV under a live build marker, then authenticated sealing, deletion and state transition. Native Windows suite also runs the transaction tests.
- First draft failed existing unit and seven ASS suites because it required the owned context even for normal standalone calls. This was caught and corrected before merging. Those red drafts are **not** acceptance evidence.

Final exact PR-head green:
[Python 3.11–3.13 / Termux Lite surface / libass `tests` #39893592432](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592432),
[native Windows writer+journal #39893592605](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592605),
[seven ASS #39893592560](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592560),
[prior/current interop #39893592488](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592488),
[sustained process progress #39893592530](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592530),
[browser evidence #39893592537](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893592537).

**Not yet claimed:** exact post-merge mainline CI (initially pending), physical Android/Termux `evanescia` reproduction and updated build success, physical abrupt power loss, or full-size real-world archive completion. This is a source-fixed bug with real-FFmpeg CI, not a declaration that the user's already-running local HSR server automatically received the patch.

**Intake:** one project-specific Bug, deduplicated against older HSR MKV/media cases; no Canonical promotion.

## Exact merged-main CI snapshot (2026-10-23)

GitHub reports HSR `main@6a6410b0181b82e60528fe52f4e807911b430f4d` (PR #203) with these independent push-triggered workflows **success**:
- [Python 3.11–3.13, Termux Lite import surface, real libass #39893799736](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799736)
- [Native Windows project output and journal tests #39893799812](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799812)
- [Browser evidence #39893799928](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799928)
- [Pinned legacy/current code interoperability #39893799772](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799772)
- [Sustained concurrent progress #39893799717](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799717)
- [Pages #39893799572](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799572)

[Seven ASS main push run #39893799783](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39893799783) was still **in_progress** at final snapshot, in the runner's dependency installation step (its exact PR-head counterpart already passed). Do not report an uncompleted check as passed.

The owner was given the normal README-backed Termux update commands (`git pull --ff-only`, restart launcher) with explicit instruction to preserve project data and not delete the safety marker. Real `evanescia` rerun is still FIELD-PENDING. No Canonical promotion.
