# Bug: HSR MKV exporter accepted stale ASS and concurrent output writers

Date: 2026-10-13
Status: **Fixed in source main; exact-head automated verification green; physical device and arbitrary real-world media pending**
Lifecycle: regression-verified
Project: `11576865/HSR-Voice-Archive-Builder`
Repair: [PR #154](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/154)
Tested head: `62d4ddaab64e6d2e262da3304e4632748dd99e8d`
Merged main: `f78c2794c309b01ff01d5ed7aab4bf036a9333af`

## Observed defect and risk boundary

The project's existing `app/subtitle_export_status.py` already records checksum-bound `subtitle_export_receipt.json`: source manifest, human text/timing overrides, and ASS/SRT outputs. However, both the full FastAPI MKV route and Termux lite route accepted merely existing `continuous.flac` + `HSR_Voice_Archive.ass`. That let a stale or externally modified ASS be bundled into a newly created "verified" MKV. There was a classic check-versus-publication race: authoritative subtitles could change after a job was queued or while FFmpeg muxed.

`ArchiveBundleExporter.validate()` checked one video/audio/subtitle stream and FLAC/ASS codecs but did not check video was the specified H.264 or matched expected resolution, and counted font attachments without confirming each filename/MIME. A symlinked project font directory could result in no attachments rather than an explicit error.

The job scheduler serialized build jobs only. Same-project MKV exports, ASS, black-video, build and remote-apply operations could run concurrently, competing for authoritative output files. This is a source-verified race condition; no user report of actual overwritten files is asserted.

## Implemented mitigation

- `require_current_bundle_subtitles()` reuses the project's *existing* receipt validation rather than a new parallel provenance layer. Both API adapters reject missing/stale/unverified/non-ASS receipts before queuing a job; the MKV writer also rechecks at execution start and immediately before atomic publication.
- Output integrity validation now verifies H.264 video codec and dimensions, each font filename and MIME type, duplicated attachments and exact project font name membership. Symlinked font asset directories fail closed.
- `app/jobs.py` now serializes output-writing jobs **per project**, retaining unrelated-project concurrency; build-global single-flight semantics remain.
- FFmpeg remains FLAC stream-copy + selectable ASS soft subtitles + existing video background; old successfully validated MKV is preserved when any new check fails.
- Legacy projects without a valid subtitle export receipt must regenerate ASS/SRT before the next complete MKV export. A file existing alone is not sufficient to certify current content.

## Regression evidence

- [Python/Termux workflow 38388064657](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38388064657): success
- [Chromium plus real FFmpeg/libass/MKV workflow 38388064667](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38388064667): success
- New real FFmpeg tests construct a known-good MKV, then assert stale receipt, modified override between validation and replace, and mismatched video codec are rejected. Tests assert the original output bytes remain unchanged. Font symlinks/attachment identity and full/lite API gates have coverage. Held background job tests prove same-project output-writer rejection, other-project independence, and retry after completion.
- GitHub main comparison after squash merge returned `identical` at the cited merge commit.

## Reusable knowledge and boundaries

A container's successful mux and superficially correct stream inventory cannot prove it corresponds to **current authoritative project state**. Verify provenance at task admission *and publication*, and serialize writers sharing an output identity. Keep separate evidence for stream structure, decoded/raster quality, physical player compatibility and real source packages. No AAC or multi-subtitle enhancement was delivered by this bug fix.

Related historical sources: `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`, `inbox/bugs/2026-10-11-hsr-source-revision-loses-human-override-and-accepts-stale-editor.md`, `inbox/candidates/2026-10-09-mkv-batch-heuristic-pairing-and-output-identity-gates.md`. This record is a concrete new MKV publication-boundary defect, not a duplicate of editor-draft conflict handling. No automatic Canonical change.


## Continuation — embedded ASS payload equality, not only stream inventory (2026-10-16)

A new user-facing report disclosed a distinct *publication-chain* failure: after edited ASS regeneration, the loose `HSR_Voice_Archive.ass` changed but the delivered complete MKV still exposed the old subtitle. In the HSR source at PR #185, the explicit `/api/output/ass` job formerly marked success after creating loose ASS alone, and automatic style refresh separately regenerated that loose file; MKV rebuild was contingent on a best-effort later follow-up. Existing FFprobe-based checks verified only stream count, codec type and provenance receipts, not the **embedded text/style/event payload** itself. The previous PR #154 source receipt safety remains necessary but does not establish the new content equivalence claim.

**Proposed HSR repair (not yet regression-verified):** [PR #185](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/185) now routes manual and auto ASS regeneration through one serialized complete-MKV publishing job in `app/auto_delivery.py`. Before replacing the previous MKV, `app/archive_bundle_exporter.py` demuxes its staged `0:s:0` ASS track using FFmpeg stream copy and compares all `Style:` and `Dialogue:` rows (including timestamps and override tags) with the latest source ASS. Mismatch fails without replacing the prior artifact. FastAPI/Termux Lite and browser polling share job completion semantics; tests include a revised real FFmpeg fixture that updates the subtitle, confirms new embedded text, and injects a mismatch to assert old MKV preservation.

**Evidence boundary:** HSR latest CI and physical Termux/device acceptance are still pending. The proposed comparison normalizes row ordering and ASS header metadata; it is an exact multiset of style/event rows, **not** a byte-exact container proof, renderer raster quality proof or player compatibility result. Keep the earlier 2026-10-13 regression-verified status scoped to its original PR #154 only; this continuation is **Pending External Validation**. Canonical unchanged.

## Continuation — 2026-11-10 Termux embedded ASS false-mismatch report (Pending Field/CI)

**Source:** User supplied two Android/Termux screenshots of ArchiveBundleExporter._verify_embedded_ass() raising at archive_bundle_exporter.py:145, called by export() at line 367, with the error "MKV 内的 ASS 字幕文本、时间、样式或特效与最新生成的 ASS 不一致；拒绝覆盖旧 MKV". This proves the **staged new MKV failed the equality gate**, not that the previously published MKV was itself wrong. The on-device loose ASS, demuxed temporary MKV and full diff were not collected; the precise user-file mismatch field is **unconfirmed**.

**Reproducible narrower finding:** In a local real-FFmpeg round trip, a valid ASS timestamp with one centisecond digit (such as "0:00:00.1") is serialized as "0:00:00.01"; zero-padded numeric margins are also persistence-equivalent. Raw Style/Dialogue row equality can therefore reject equivalent events. This complements "inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md", not independent proof of this user's exact root cause.

**Bounded product patch:** [HSR PR #221](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/221), head cde83875ff9337a2ca042788d5eae15e790a381b, stream-copies the existing ASS stream rather than invoking a redundant ASS encoder, canonicalizes event times into exact centiseconds and integer layer/margins while retaining actor/style/effect/text/override tags and event multiplicity, and reports first changed category/index and style/event counts if verification still fails. Reject-before-atomic-replace remains. Real FFmpeg mux/readback and negative text-mismatch regressions added.

**Status:** Implementation submitted to review, **Pending External Validation** (exact-head CI and real Android/Termux field rerun not verified). Do not claim the user's archive fixed without a successful device run. No Canonical promotion. A repeated failure should capture the new first-difference category and counts, then distinguish actual missing/altered events from representation-only normalization.

**Merge/CI update — 2026-11-10:** HSR PR #221 merged by squash into `main@9a9c1e74d63f869ec1991f892be6f1482b907ad9`, after all six reported PR-head GitHub Actions workflows completed successfully (tests, seven ASS, browser evidence, Windows, legacy interop, concurrent journal). Post-merge source readback confirms semantic signature normalization and reject-with-detail remain present. Physical Termux rerun on the user's original archive remains **Pending Field Validation**; this update does not establish that the original mismatch was format-only.

## 2026-11-10 continuation — >10h FFmpeg ASS-text conversion clamping

**Latest field report:** After PR #221 and #222 were merged, the user's real Termux build failed at ASS verification with 4 styles on both sides and 9990 Dialogue events on both sides. The comparator's first differing sorted event is #3521. Its actual fields/timestamps are not visible, so the device-specific root cause remains unconfirmed.

**Independently reproduced real-FFmpeg issue:** A local FFmpeg 7.1.5 trial with 4 styles, 9990 events, and a timeline longer than ten hours retains the exact native Matroska packet time for event 10:00:00.00 (pts=36000000, time_base=1/1000), while re-exporting through FFmpeg's ASS-text muxer clamps both Start and End to 9:59:59.99. Style and event counts remain unchanged. The pre-existing verifier was comparing this potentially lossy intermediate ASS text, not the MKV's own packet timestamps. This identifies a reproducible causal mechanism, but not yet proof that the specific device's event #3521 crosses the same threshold.

**Bounded correction submitted:** HSR [PR #223](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/223), head 6e7cfa5ef5b7f86bc77b8aa5dd32f9d05608a499, replaces ASS-text demux verification with native FFprobe ASS packet + codec-private style inspection: exact rational PTS/duration centiseconds, exact text/override/style/actor/effect semantics, preserved event multiplicity and ReadOrder guard. Existing refusal to publish corrupt replacements remains. Real 9990-event >10h mux/test and tamper tests included.

**Status:** Local reproduction and product patch done; first read of six PR workflows showed them in progress. CI final and physical Termux field acceptance **Pending External Validation**. No Canonical promotion and no claim that device failure is fixed.

## PR #223 merge and verification update — 2026-11-10

GitHub PR [#223](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/223) completed all six PR-head GitHub Actions workflows successfully, including the seven ASS requirements suite and real media test. Squash-merged to HSR main at `8b5d5aa6a1dad5e49f486c634c8940d539559379`.

Independent post-merge readback verifies production `app/archive_bundle_exporter.py` calls `assert_native_ass_matches(self.ffprobe, mkv, expected)` instead of exporting the embedded ASS stream through the lossy textual `-f ass` path. The native packet verifier and the 9990-event >10h regression test also exist on main. The checks still compare native timing, style, event payload, effects and multiplicity; they do not relax the reject-before-publish guard.

Evidence tier: merged production code + all six PR-head CI workflows passed. **Device acceptance Pending**: the user has not yet provided a successful updated Termux rebuild of the original 9990-event project, so the exact reported field failure cannot be marked closed. No Canonical promotion.
