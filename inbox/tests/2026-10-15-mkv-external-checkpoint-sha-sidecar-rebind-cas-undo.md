# Test · Portable external metadata checkpoint requires current byte rebind and revision-bound inverse

Status: **Test Candidate / Product PR Submitted / exact-head CI Pending**. Not Accepted, not Canonical.
Date: 2026-10-15
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/144
Exact submitted product head: `a305dde5486c068f689d45f340dfdd457e02c5b8`
Depends on PR #143 live one-document authority and parent #142 P0 protection.

## Prior knowledge and distinct gap

Foundry already records `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md`: same filename/size/mtime cannot substitute exact browser File reference for **current-session** metadata editing. `inbox/cases/2026-10-14-mkv-verified-source-delta-export-and-atomic-replay.md` covers source-MKV track/attachment replay based on full-source SHA. Those cases do not cover **multiple external audio/subtitle Files plus optional sidecar** across a session restart, with imported checkpoint JSON, explicit consent and revision-bound inverse.

## Submitted scoped regression gate

New `src/portable-external-project-recovery.js` exports only allowlisted per-external-track metadata, current `File` full SHA-256 and optional subtitle sidecar full SHA-256. JSON neither carries browser File grants, writer rights nor outputs. Imported JSON is untrusted, rigidly parsed and inert. Preparing recovery checks each current File name/size, full bytes digest, exact live `File`/sidecar/format/identity references after every await, the unified immutable ContainerProject identity and revision. Mismatched content, changed File inventory, concurrent edits and malformed schema refuse.

A **separate checkbox + Apply click** dispatches the whole recovered external metadata delta through the actual unified transaction. Undo is valid only against the exact Project object revision resulting from this apply; later edits or File changes invalidate it. This is not a generalized persistent Undo journal.

### Required tests

- Node `tests/portable-external-project-recovery.test.mjs`: successful export/parse/prepare/apply/inverse, altered File byte and sidecar byte, same-looking new File, malicious grant key, unknown field, hash-time field mutation, stale plan, no implicit consent.
- Chromium `scenarioExternalCheckpointRecoveryRealMux`: MP4 + FLAC, export/download JSON, change title, inert import, SHA verify, checkbox approval, apply, undo, second prepare/approve/apply, **real finished MKV**, native independent `ffprobe` reads recovered external audio title.
- PR #143's mixed source/external actual MKV scenario and all legacy P0/Batch/P3 regressions must remain green.

**None of these new exact-head CI or native output verdicts is yet confirmed**. This entry is a pending Test, not proof.

## Dedup / limits

Searched `SHA-256 sidecar recovery explicit consent undo`, `external metadata checkpoint`, `rebind exact File digest user confirmation`, `portable project multi source recovery`. Related exact File identity and source-MKV SHA cases are not duplicate of the **external sidecar + cross-session metadata + consent + CAS undo** test class.

Outside scope: source and external changes combined into one all-or-nothing portable replay; font File regrant; serialized browser handles; durable undo after page refresh; new Chapter/Tag writer. No Canonical promotion.
