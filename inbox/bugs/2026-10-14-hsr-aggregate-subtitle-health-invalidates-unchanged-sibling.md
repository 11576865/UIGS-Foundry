# Bug: aggregate subtitle health falsely expires an unchanged sibling artifact

Date: 2026-10-14
Project: `11576865/HSR-Voice-Archive-Builder`
Status: Fixed in direct-main checkpoints; CI outcome not independently confirmed
Area: independent deliverables, provenance receipts, MKV freshness, UI status

## Symptom and reproduction

The existing `read_subtitle_export_health()` returned only an aggregate `state` and `artifacts_current` for the pair of exported SRT and ASS files. If a previously certified `HSR_Voice_Archive.ass` is modified, aggregate `state=stale`; the MKV dashboard previously calculated `srt_current` using that aggregate state. Consequently the unchanged, hash-matching `HSR_Voice_Archive.srt` was also incorrectly marked stale. Symmetrically, a tampered SRT should not negate a separately unchanged ASS file's own content identity.

The combined `HSR_Voice_Archive_Bundle.mkv` **must** still be stale and cannot be regenerated until both required subtitle exports are current. An independently valid SRT or ASS is not a substitute for both.

## Bounded repair

- `app/subtitle_export_status.py`: add `srt_current` and `ass_current` computed independently from each file's hash against the persisted successful export receipt and the unchanged source-input hash set. The aggregate `artifacts_current` remains fail-closed and requires all promised outputs. Pending/failed/invalid or missing receipts cannot assert either output current.
- `app/archive_bundle_lifecycle.py`: read those individual flags into `prerequisites`, retain strict `subtitles_current`/MKV current checks and source-replacement behavior.
- Regression tests `tests/test_subtitle_export_status.py` and `tests/test_archive_bundle_delivery_contract.py`: ASS-only change leaves SRT current while MKV stale; SRT-only change leaves ASS current; SRT-only export without ASS remains an independent usable product, not MKV-ready.

Product main commits: `c7ba1f78f28b64c3a7fb19cc27f652269d149699`, `32893a20e1470f02cffb2d4a0df006b3b4ee671a`, `f1fc0a20558ee88ea77a3b3a45180cf75479a682`, `14bbf0dec97dd66de4829cbdd8e5c7f560a52024`, `4c9fc2b0bd96ebfe77af8f907683ecd349ea38ef`.

## Evidence tier and limits

Source inspection confirms original aggregate coupling and the separate-flag fix; regression tests were submitted on main, but **green push-triggered GitHub Actions runs are not available from the connected commit-status endpoint**, so do not report CI passed. No Android physical player verification. The existing product issue #158 still tracks real device and color/performance acceptance.

## Reusable method (observation, not Canonical)

An aggregate health signal for a compound export must **not** be reused as evidence that every independent member of the set is invalid. Publish per-artifact provenance next to aggregate readiness. Combine them only at the delivery operation that actually requires the entire set (here, MKV mux). Maintain old aggregate API semantics for compatibility.

Related to existing HSR Foundry observations about MKV full-regeneration lifecycle and the earlier durable subtitle edit/export gap, but distinct: this defect is a *false invalidation of an unchanged sibling* rather than stale subtitles being incorrectly trusted. One observed defect does not authorize Canonical changes.

## API-level follow-through

HSR main commit `437aae060b3c6059c91e46e9dcbd4f987016ddd5` also makes `project_summary.output_groups.independent_products` expose independent SRT/ASS `current`, `freshness` and `used_in_bundle`, while the lossless FLAC mother track is labelled `ready_for_bundle` for cheap presence preflight but `freshness=unverified` (no claim of independent FFprobe attestation). Corresponding tests and docs: `4dac9eee0d00e91384ceffe78bc7af0d564b7cec`, `a0e6df7a8eb735e223dc9c3c7b85453de9a669fa`.

The principal invariant is now visible on both the HTML output cards and the structured project API: an independently unchanged subtitle remains current; its changed sibling is stale; a combined MKV demanding both remains stale. Exact-head CI/real-device verification remains a separate evidence tier and has not been asserted as passed.
