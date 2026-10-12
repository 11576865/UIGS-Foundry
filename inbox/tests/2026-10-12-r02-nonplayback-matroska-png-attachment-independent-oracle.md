# Test: R-02 non-playback Matroska — single PNG attachment, zero Tracks/Cluster, independent reader+byte oracle

Date: 2026-10-12
Status: Test / **one passing independent-tool research fixture**, not Canonical or production writer certification
Project: `11576865/MKV-Fast-Muxer`
Product PR: https://github.com/11576865/MKV-Fast-Muxer/pull/88
Product merged commit: `fee72462c687181348f7f1f2e181816c1dc8d30d`
Exact PR head: `c267e639ef6058ceb1c1ca0f7401ba8a24af794f`
Verified workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38237809185
R-02 experiment artifact: `r02-png-only-matroska-experiment` (artifact ID `11741029185`, attached to run; time-limited retention)
Reference specification: RFC 9559 §§4.5, 6.1 and 21.

## Hypothesis and scope

The container domain is permitted to **model** a target with exactly one PNG AttachedFile, zero Tracks, zero Cluster, and no video surrogate. Current video-rooted FFmpeg mux execution is a **different** capability from the format's top-level structure. RFC 9559 §6.1 says Info is the sole REQUIRED Segment top-level element while a *playable* Matroska requires Tracks and Cluster; this is a normative starting condition, not a guarantee that a particular fixture satisfies every EBML constraint.

## Reproducible independent oracle

1. `scripts/r02-attachment-only-experiment.mjs` writes a deterministic **test-only** EBML Header + Segment(Info, Attachments) document containing a valid one-pixel PNG `pixel.png` as AttachedFile FileData, FileMediaType `image/png`, FileUID 42. It deliberately adds **no** video, audio, subtitle, Tracks or Cluster elements.
2. Independently run `mkvmerge -J` (different software from the fixture writer). Require exactly 0 tracks and 1 attachment with the requested file name and media type.
3. Extract attachment using `mkvextract attachments` and compare extracted bytes with the original PNG via SHA-256/content equality. Do not treat a copied MIME string as a byte integrity check.
4. Run `ffprobe` separately. A reader returning EOF for a non-playing/no-track container is recorded as a compatibility observation; it is **not** automatically classified as a broken EBML structure.
5. Save machine-readable `r02-attachment-only-report.json` even if MKVToolNix fails. CI runs this experiment `continue-on-error: true`; **green workflow status alone does not certify R-02**. The JSON verdict is the scoped oracle.

## Observed exact-head result

- GitHub workflow `38237809185`: **254/254** Node unit tests pass, Vite Build pass, full Chromium Browser E2E passes.
- Experiment step completed successfully, logging:
  `result=INDEPENDENT_READER_AND_BYTES_MATCH`;
  `reader.mkvmerge=parsed`;
  `reader.mkvextract=extracted`;
  `reader.ffprobe=rejected-or-no-media`.
- Independent audit artifact was uploaded. These observations establish **one validly extracted test-only sample** and demonstrate why reader/playability and format-domain representation must not be conflated.

## Non-claims / future falsification

- No production browser attachment-only writer, GUI operation or generalized attachment extractor is proven.
- Not a formal standards conformance suite, not multiple-independent-reader certification, not portable player support.
- No proof that arbitrary Chapters, Tags, unknown EBML elements, UID target relationships, or changing an existing MKV are preserved.
- Follow-up: inspect additional independent parser/validator, document full schema constraints, test a production-compatible writer with arbitrary attachment bytes/size/name/MIME and no invented media, then validate roundtrip and filename conventions. Keep the writer capability explicitly unsupported until those gates pass.

## Existing-knowledge dedup

Extends the scope/standards distinction already recorded in:
`inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`
and
`inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md`.

It is a **Test-level evidence record**, not a promotion or rewrite of either Observation and not a change to any UIGS Canonical rule.

## P2 source reader follow-up — 2026-10-12 (Pending exact-head CI)

Product [Draft PR #89](https://github.com/11576865/MKV-Fast-Muxer/pull/89) at initial head `f0c54d1fa1ebffbb42c0b72cae9b950b3634ebe2` adds a session-reference-scoped SourceAsset identity and bounded `Blob.slice` / raw-EBML attachment inspector. The reader observes generic FileName, FileMediaType, FileUID and FileData byte ranges, retains no source File objects in immutable report projections, does not load full FileData during inventory, fails closed on incomplete/unknown-sized child structures, and opens an attachment only as an explicitly requested Blob view. `projectAttachmentCopyTarget` maps selected observed attachment metadata into a separate *non-executable* output draft; no production writer or copy-preservation guarantee was added.

New R-02 crosscheck reads the **same test-only sample** already independently examined with `mkvmerge`/`mkvextract`, and will compare this reader's chosen PNG Blob view hash against the independent extracted PNG hash. The crosscheck remains **non-gating research** and uploads its own JSON verdict; the browser and Node suites remain gating. At intake, the current PR head is queued/running; no new passing result is yet claimed. Any green CI without `MODEL_AND_INDEPENDENT_ATTACHMENT_BYTES_MATCH` is insufficient to promote this crosscheck to verified evidence.

Threat boundary: arbitrary attachment names and MIME are **untrusted metadata**. This P2 API exposes no filesystem save or execution action, and no automatic preview; downstream UI must sanitize/collision-check before exporting and must not take MIME at face value. Existing untrusted attachment Case remains the acceptance reference. No UIGS Canonical promotion.

## 2026-10-12 R-02-W candidate writer experiment submitted (Pending independent verification)

New product [Draft PR #93](https://github.com/11576865/MKV-Fast-Muxer/pull/93), latest initial implementation head `21350cd8e0818d230897a55fceec34e6908e0f86`, introduces an **independent implementation** from the earlier constant R-02 fixture: a session-bound, immutable `PNG_ONLY_PLAN_SCHEMA` authorizes one source PNG Blob in a WeakMap keyed by the genuine plan object, and a research-only EBML Blob writer creates Segment Info + exactly one PNG AttachedFile with zero Tracks/Cluster. It checks an eight-byte PNG prefix but does **not** claim full PNG safety, bytes hash before output, portable source identity, general Matroska write support, or browser UI enablement.

The new script `scripts/r02-candidate-writer-independent-audit.mjs` writes a candidate-produced Matroska, then *separately* runs `mkvmerge -J` to confirm exactly zero media tracks and one PNG attachment and `mkvextract` to prove original/extracted byte equivalence. The separate raw-EBML model reader also re-inspects the **same** candidate-produced file and compares extracted bytes. New non-gating artifact `r02-candidate-jobplan-writer-audit` contains JSON plus exact output and extracted PNG. **The required verdict is `CANDIDATE_WRITER_INDEPENDENT_ZERO_TRACK_AND_PNG_BYTES_MATCH`; workflow green on its own is not proof.** At Foundry intake, exact-head Node/Vite/Chromium CI and independent verdict are Pending.

This is an extension of the existing R-02 Test, not a standalone assertion of broad writer conformance. R-02's original research fixture, production browser FFmpeg writer constraints, and red #77 complex ChapterUID-targeted Tag remux behavior retain their separate statuses. No Canonical promotion.

## R-02-W independent candidate-writer proof verified — 2026-10-12

Product [PR #93](https://github.com/11576865/MKV-Fast-Muxer/pull/93), exact head `21350cd8e0818d230897a55fceec34e6908e0f86`, passed **288/288 Node**, Vite build, full real Chromium E2E (including old mux/batch and R-02 browser extraction), and BOTH separate R-02 and R-02-W independent steps in [workflow 38248987337](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38248987337). The **new candidate-writer-produced** output audit logged exact result `CANDIDATE_WRITER_INDEPENDENT_ZERO_TRACK_AND_PNG_BYTES_MATCH` with `mkvmerge=parsed`, `mkvextract=extracted`, `modelReader=inspected`. Candidate writer artifacts and JSON uploaded as `r02-candidate-jobplan-writer-audit`. Squash merged into main as `a2823e5c1f0d07c9913d3f7cbfd002832490af30`.

This upgrades only the **scoped, create-new, one-PNG zero-Tracks/Cluster, 16 MiB-limited JobPlan/EBML writer candidate experiment** from Pending to independently verified for this exact sample. It remains **not wired to product UI** and does not certify full Matroska conformance across samples, audio-only, multi-attachment, malformed input, unknown elements, ChapterUID/Tag preservation, general writer compatibility, player support or arbitrary browsers/devices. PNG prefix matching is not full-image/malware validation. Existing FFmpeg video-rooted and #77 technical preservation risks remain unchanged.

Reusable knowledge is the *bounded independent provenance* separation: test-only fixture authoring, a second candidate authoring implementation, and independent external extraction must not be conflated merely because outputs resemble each other. Preserve the green CI log plus the named JSON oracle; don't promote Canonical from one fixture.

## R-02 browser-produced output implementation submitted — 2026-10-12 (Pending exact-head E2E)

Product [Draft PR #94](https://github.com/11576865/MKV-Fast-Muxer/pull/94), initial head `e3ef0b4a26ce6dbf1e21abd7d986ef0865cbf790`, adds a **deliberately experimental** two-stage browser tool for creating exactly one PNG AttachedFile inside a *new* zero-Tracks/zero-Cluster Matroska. It uses the previously verified PR #93 session-bound immutable JobPlan and candidate EBML/Blob writer; it never invokes or edits the video-rooted FFmpeg/Wasm or legacy batch engine. The first user action prepares an output and invokes the **project reader** on its Blob, checks exactly one PNG/UID1 and no Tracks/Cluster, and compares original/extracted FileData with browser WebCrypto SHA-256. Only then does a second explicit button request an opaque Blob download. Changing the selected File clears the prepared output; a fake PDF-prefix file named `.png` must be denied.

A real Chromium E2E scenario saves the **actual browser-produced output**, not only a Node-produced candidate or constant EBML fixture, and passes that file to independently authored `mkvmerge -J` and `mkvextract`; it must report zero tracks, one PNG, exact extracted bytes and machine JSON `BROWSER_WRITER_INDEPENDENT_ZERO_TRACK_AND_PNG_BYTES_MATCH`. A separate upload artifact `r02-browser-png-only-candidate-audit` preserves the MKV, extracted PNG and JSON. **At intake these outcomes are Pending**, and old E2E+P0 and preexisting R-02/W evidence remain mandatory. New nonplaying output is still experimental: no broad certification, general container write support, multi-file/Chapter/Tag editing, disk overwrite control or device compatibility claim. Do not alter UIGS Canonical based on a single scenario.

## Actual browser-produced nonplaying Matroska independent audit verified — 2026-10-12

Product [PR #94](https://github.com/11576865/MKV-Fast-Muxer/pull/94), exact head `e3ef0b4a26ce6dbf1e21abd7d986ef0865cbf790`, passed **288/288 Node**, Vite Build, all Chromium Browser E2E, and previous R-02 fixture/new candidate independent steps in [workflow 38250198625](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38250198625). Chromium logs confirm `P2 R-02 browser-produced candidate independently extracted bytes PASS` and `All browser E2E scenarios PASS`. The **actual downloaded browser output** was parsed by external `mkvmerge -J` (zero Tracks and one `pixel.png` `image/png` of the expected size); `mkvextract` recovered bytes equal to the originating PNG. A misleading PDF-prefix source named as PNG was refused. Evidence artifact `r02-browser-png-only-candidate-audit` (artifact ID `11746858373`) contains the downloaded MKV, independently extracted PNG, and JSON `BROWSER_WRITER_INDEPENDENT_ZERO_TRACK_AND_PNG_BYTES_MATCH`. PR squash merged as `main@268b08e1ec406eb09dc92835b594d6f7db1acd99`.

The user-facing operation is deliberately labeled **experimental**, with separate Generate+Verify and Download user actions, browser-local reader inspection and SHA-256 attachment equality before enabling download. Its scope remains only **one PNG, new Matroska, zero media tracks, <=16 MiB**, not a universal Matroska writer, established full standards conformance or player compatibility. In particular, no edited existing Matroska semantics, nested Chapter/Tag UID relation preservation (#77), multi-attachment CRUD, arbitrary MIME/malware proof, durable output ownership or cross-device performance was validated. Do not promote Canonical based on this one fixture; future wider proofs must be filed separately.

## Generic multi-attachment create-only follow-up — 2026-10-12 (Pending independent external oracle)

Product [Draft PR #95](https://github.com/11576865/MKV-Fast-Muxer/pull/95), initial head `af71cf3461b868c4b13efa895557bf27fcd69540`, proposes a **separate experimental** multi-attachment-only authoring path. Unlike the already proven one-PNG R-02-W/R-02-browser paths, this writer accepts **2–8 distinct, non-empty File/Blob inputs** with explicit syntactically checked but untrusted MIME; caps at 16 MiB/item and 32 MiB/plan; freezes a plain `JobPlan` while binding actual File objects in a private session WeakMap; allocates distinct new Segment-local FileUIDs 1–N. Original→safe filename changes and collision suffixes require explicit `approveFilenameAdjustments`, not silent renaming. It creates a **new, zero Tracks/Cluster Segment**, never edits an existing MKV or replaces the FFmpeg/Batch executor, and returns `CREATED_AWAITING_INDEPENDENT_AUDIT`.

The separately-authored `scripts/p2-multi-attachment-independent-audit.mjs` must test an actual candidate-produced MKV with **two different payloads** (PNG and `text/plain` license) using `mkvmerge -J` (zero tracks, two correct attachments) and `mkvextract` (both original-byte/SHA-256 matches). The preexisting separately-authored raw-EBML reader must inspect this **same output**, require FileUIDs 1 and 2, zero Cluster/Tracks, and agree with external extracted hashes. Separate non-gating CI artifact `p2-generic-multi-attachment-writer-research` should contain source/observed hashes, MKV and independent extractions; the only passing research verdict is `MULTI_ATTACHMENT_WRITER_INDEPENDENT_UIDS_AND_BYTES_MATCH`. **At this intake the new exact-head CI and external-tool results are Pending.**

A successful candidate would remain evidence only for this bounded create-new no-media scenario, **not** production general attachment CRUD, universal Matroska validity, unknown-element/Chapter/Tag UID relation preservation (#77), executable-attachment safety, full payload MIME verification, browser UI or player/device interoperability. Update this Test record if/when exact-head results arrive; do not promote Canonical from one pair of fixtures.

## Generic two-attachment candidate verified; browser multi-file creation submitted — 2026-10-12

Product [PR #95](https://github.com/11576865/MKV-Fast-Muxer/pull/95), exact head `af71cf3461b868c4b13efa895557bf27fcd69540`, passed **296/296 Node**, Vite Build and entire real Chromium E2E in [workflow 38251770437](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38251770437). The separate candidate-writer experiment **itself** logged `MULTI_ATTACHMENT_WRITER_INDEPENDENT_UIDS_AND_BYTES_MATCH` after independent `mkvmerge -J`, `mkvextract` of both PNG and text/license bytes, and an independent project-reader check of distinct FileUID 1 and 2, zero Tracks/Cluster and SHA-256. Previous R-02 and R-02-W oracles remained green. PR #95 squash merged as `main@cf1e220ebfda74dbbf1e82bb221334d9e7d44a78`. Verified scope: new no-media Matroska with two different attached files, distinct UIDs and exact bytes, under plan caps 2–8 attachments, 16 MiB each, 32 MiB total; NOT broad-sample, worst-case or product UI verification.

New [Draft PR #96](https://github.com/11576865/MKV-Fast-Muxer/pull/96), head `03f2d6f57dbf014b92df1a2b9ab0e4f84decf32c`, proposes the next separately scoped **browser user-review and real output** experiment: visible per-file original/written names, untrusted editable MIME/size, explicit privacy/rename confirmation, invalidation on source or MIME change, plan-local independent reader and per-attachment SHA-256 checks before manual download. Real Chromium E2E will submit two files, save actual user-facing MKV, use independent `mkvmerge`/`mkvextract` to check both bytes and record `BROWSER_MULTI_ATTACHMENT_INDEPENDENT_UIDS_AND_BYTES_MATCH`. At intake, **#96 exact-head Node/Vite/Chromium CI and external report are Pending**. The new writer is still marked experimental and never edits/remuxes existing source Matroska or establishes ChapterUID/Tag preservation, malware safety, or arbitrary content MIME authenticity. No Canonical promotion.

## P2-M browser multi-attachment creation independently verified — 2026-10-12

Product [PR #96](https://github.com/11576865/MKV-Fast-Muxer/pull/96), exact head `03f2d6f57dbf014b92df1a2b9ab0e4f84decf32c`, passed **296/296 Node**, Vite Build, full real Chromium E2E and all existing R-02/R-02-W/P2-M independent tests in [workflow 38253090685](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38253090685). Browser scenario explicitly logged `P2-M browser multi-attachment byte audit + review invalidation PASS`, then `All browser E2E scenarios PASS`; new candidate research itself logged `MULTI_ATTACHMENT_WRITER_INDEPENDENT_UIDS_AND_BYTES_MATCH`. The workflow uploaded actual Chromium-created output MKV, both independently extracted generic attachments and a machine JSON report `BROWSER_MULTI_ATTACHMENT_INDEPENDENT_UIDS_AND_BYTES_MATCH` as artifact `p2-browser-multi-attachment-independent-audit` ID `11748753102`. PR #96 squash merged into `main@9c414517e97e0fc7c14a926dc5b0dc9c3e08aeb4`.

**Bounded verified operation:** experimental new-container creation from two separately selected files (a PNG and an actual license text resource), with explicit review of names/MIME/bytes and sensitive-content disclosure, local project-reader per-attachment SHA-256 before manual download, and independently observed browser-downloaded MKV with zero media tracks and exact external PNG/text FileData extraction. MIME editing invalidates approval/output; case-collision name changes are surfaced, and one-file selection is refused on the multi-attachment route. **Not verified:** every 2–8 input combination, full 16 MiB/device resource budget, malicious payload handling, actual destination overwrite prevention, multiple Chapter/Tag/unknown EBML preservation, arbitrary player interoperability, persistent JobPlan recovery. The new writer remains an experimental *create-new* path; no Canonical promotion.
