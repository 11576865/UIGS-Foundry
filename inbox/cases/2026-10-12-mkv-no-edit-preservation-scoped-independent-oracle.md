# Case: Matroska no-edit browser remux requires scoped independent preservation evidence

Date: 2026-10-12
Status: Case / test and code submitted on Draft PR, full CI pending
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/76
Branch: `test/p0-preservation-baseline-20261012`
Initial baseline: `main@7781a4f410a9c6edb9a1f3d056091e6ace333cc4`
Related:
- `inbox/candidates/2026-10-03-preserve-all-must-cover-full-source-domain.md`
- `inbox/candidates/2026-10-02-persistable-semantic-roundtrip-verification.md`
- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md`
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`

## Context / why this case is new

An unchanged input MKV can be re-muxed by browser FFmpeg Wasm into a playable MKV while dropping metadata, attachments, chapters or relationships not inspected by the tool itself. A “no-op remux” is not bytewise no-op. Before general-purpose editing, implement a *negative-preservation oracle* which can falsify an unsupported preserve-all claim.

Draft PR #76 adds `scripts/p0-compare-roundtrip.mjs` and `tests/p0-preservation-audit.test.mjs`, plus a browser real-output E2E scenario against the existing font+note+chapter test MKV. The oracle uses independent `mkvmerge -J` / `mkvextract` to enumerate and extract attachments then hashes their *actual bytes*, and `ffprobe` to compare media types/codecs, applicable flags and titles/languages, chapter start/end/titles and selected global metadata. Failing differences yield a nonzero exit and a machine-readable JSON artifact. Tool failures are reported as CHECK_UNAVAILABLE, not success.

**Explicit coverage limit:** passing checked fields does not mean all EBML is retained. The current fixture itself was generated with FFmpeg and does not stress independent muxers, unknown EBML elements, nested Chapter/Tag targets, UID references, CodecPrivate, packet timestamp identity, playback rendering or player compatibility. Those remain separate P0 tasks. Do not merge or claim full preservation merely because this scoped fixture is green.

## Execution observation (at intake)

At earlier PR head `8cec099537d4d70769274e76f6b7ed23c0cc807c`, both Pages and browser workflows reached Unit tests and failed the same preexisting source-shape assertion in `tests/composition-workspace.test.mjs`: it expected only `roles.needsSourceChoice || roles.unknown.length` while current production `src/main.js` additionally preserves an actively focused source radio using `|| focusedSourceRadio`. The production code was not modified by P0. PR head `7291eb587a309c62a0a82407251a34c45fd24d13` updates the stale regex to match the additional focus-preservation behavior. Pages workflow for that head has passed; Chromium Browser E2E is **in progress** at intake. This is not evidence that the new browser remux oracle has executed successfully yet.

## Proposed cross-project takeaway (Candidate-level only)

A roundtrip test must:
- use the *actual production writer/executor*, not an unrelated CLI simulation, for the system under test;
- independently re-read the resulting artifact;
- compare safety-relevant object facts and extracted payload digests;
- provide explicit `notChecked` coverage and avoid equating scoped success with full preservation;
- keep tool-unavailable and semantic-difference states separate from pass;
- preserve a failing fixture and machine-readable output so a failure changes capability claims instead of being explained away.

This case records a concrete local engineering experiment and pending checks. It is not a generalized UIGS Canonical standard.


## Continued P0 execution: basic green, independent hard corpus in CI

Verified from workflow logs at commit `7291eb587a309c62a0a82407251a34c45fd24d13` (run `38192821478`): Node tests 220/220; existing Browser E2E PASS; `P0 preservation comparison: CHECKED_FIELDS_MATCH` for the FFmpeg-authored unedited input with 2 attachments/chapters. Thus **scoped basic preservation was actually verified** but not all Matroska semantics.

Draft PR #76 now also adds:
- `tests/e2e/generate-independent-matroska-fixture.sh`, independently authoring nested Chapters and a generic attachment with mkvmerge;
- `mkvpropedit --tags all:<file>` injecting an explicit custom `ChapterUID` target, followed by independent extraction and self-checks;
- `scripts/p0-summarize-ebml-xml.py` and `scripts/p0-compare-roundtrip.mjs --deep` to compare hierarchical chapters and scoped `P0_*` tag targets;
- additional isolated unit tests and a real Chromium output test writing `p0-independent-audit.json`.

**Fixture-design observation:** authoritative MKVToolNix docs state that `mkvmerge --global-tags` deliberately removes `Targets` (therefore is not a suitable way to author a chapter-targeted test). Modern `mkvextract` syntax uses explicit XML output paths for chapters/tags. A self-check must independently verify that the fixture actually contains the intended hard structure before any application roundtrip; otherwise a green or red result could be about the fixture generator rather than the product.

At this update, newer E2E `38194692640` is running after correction of an invalid XML test string. Do not misread the older green result as proving this independent corpus passes. All design knowledge stays Case/Candidate, not Canonical.

References: https://mkvtoolnix.download/doc/mkvmerge.html and https://mkvtoolnix.download/doc/mkvextract.html and https://mkvtoolnix.download/doc/mkvpropedit.html


## Positive control: TrackUID-targeted tag semantic preservation (2026-10-12)

Product PR #83: https://github.com/11576865/MKV-Fast-Muxer/pull/83
Browser CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38202212178
Merged test-only commit: `096d3a52b3e828175e9430b2ac41761765335ba3`

An independent MKVToolNix fixture with **flat** chapters and one genuine `P0_TRACK_RELATION` custom Tag targeting the actual video `TrackUID` was authored using the UID read via `mkvmerge -J` with Python 64-bit integer safety, and self-checked by `mkvextract`. The actual browser FFmpeg/Wasm no-requested-edit mux path displays its ordinary `UNVERIFIED_REFERENCES` warning and generates output.

`scripts/p0-audit-track-tag-relations.py` resolves the source and output `TagTrackUID` references to a **logical track identity** (type, codec, ordinal), rather than comparing raw UID numbers, which are legitimately reassignable by container writers. It also rejects a missing Tag and an unresolved/dangling target. At source PR head `c75a68a0b7a614436ec06164f4fa8fec397f3b35`, **228/228 Node tests**, full Chromium E2E PASS and `P0 track-tag semantic relation: CHECKED_RELATIONS_MATCH`; machine-readable `p0-trackuid-target-relation-audit` artifact uploaded.

Interpretation: one **positive control** for correctly linked user-defined TrackUID metadata in a simple independent Matroska source. It does **not** support a blanket TrackUID guarantee, nor negate verified nested ChapterUID-target loss from #77/#76. It supports separating confirmed harmful structures from common-but-not-generally-verified metadata instead of globally forbidding all UID targets. Generalizable methodological insight: independent roundtrip oracles should test **referential semantics** and logical target resolution, rather than false failures from mutable surrogate IDs.

This supplements an existing Case, avoids duplicate Candidate creation, and does not update UIGS Canonical.

**Production branch evidence:** After test-only PR #83 merged, `main@096d3a52b3e828175e9430b2ac41761765335ba3` Browser E2E run https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38202515829 passed **228/228 Node tests** and complete Chromium E2E, again reporting `CHECKED_RELATIONS_MATCH` for the fixture-controlled P0 video TrackUID relation. Pages deployed successfully at https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38202515792. The original targeted ChapterUID preservation bug remains open in Issue #77.

## Candidate-output protected raw EBML contract — 2026-10-12 (Pending external oracle)

Product [Draft PR #100](https://github.com/11576865/MKV-Fast-Muxer/pull/100), first exact head `cc4f06a53a955fe3e1e6424452dd1436fe448a25`, adds a **read-only bounded** source→candidate comparison of every complete raw Segment top-level child element, including Tracks, Cluster, Chapters, Tags, SeekHead, Cues, unknown EBML, and AttachedFiles. It uses 256-KiB WebCrypto SHA256 chunk commitments with explicit length (a deterministic *tree commitment*, not whole-file SHA256), max 64 MiB per research source, and immutable per-ID/range/ordinal summaries. Changing a protected non-Attachment element reports `BLOCKED_PROTECTED_BYTES_CHANGED`; changing only FileData is `BLOCKED_UNREQUESTED_ATTACHMENT_DELTA` unless an explicit edit is declared, after which it remains `ATTACHMENT_DELTA_NEEDS_REFERENCES_OFFSETS_AND_WRITER_PROOF`. **Every comparison has `approvedToWrite=false` and no output writer.**

The independent oracle reuses the **real MKVToolNix+mkvpropedit-authored nested ChapterUID-targeted source** from unresolved #77, verifies its source XML with `mkvextract`, compares a true byte-identical copy, separate in-memory changed Chapter and Tag markers and a changed generic attachment payload, requires each change correctly classified, and checks source MKV SHA-256 remains unchanged. Required machine verdict is `INDEPENDENT_COMPLEX_MKV_RAW_PROTECTION_DIFFERENCES_DETECTED`. CI research is non-gating, so the exact-head result and JSON are **Pending** at this intake. This is deliberately a necessary-only safeguard for a possible future restricted raw-copy writer class, not full Matroska semantic equivalence, referential UID integrity, offset/CRC correctness, or an existing-MKV authoring authorization. Ordinary semantically valid rewrites may fail strict byte equality. No Canonical promotion and no claim #77 is fixed.

## P2-PC source→candidate protected raw EBML comparison independently verified — 2026-10-12

Product [PR #100](https://github.com/11576865/MKV-Fast-Muxer/pull/100), exact head `b1e21b5ff5dc1513af1577e4347900427dc73661`, passed **328/328 Node**, Vite and complete real Chromium E2E in [workflow 38272145160](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38272145160). The separately run non-gating oracle on the independently MKVToolNix+mkvpropedit-authored source with nested ChapterUID-targeted metadata explicitly emitted `INDEPENDENT_COMPLEX_MKV_RAW_PROTECTION_DIFFERENCES_DETECTED` with `error:null`. It compared byte-identical original vs cloned source and three distinct in-memory mutations (nested Chapter, ChapterUID-targeted Tag, generic Attachment FileData), detected the protected Chapter/Tag differences individually, and left the original MKV SHA-256 unchanged. The final revision also rejects uncommitted valid pre-Segment Void elements rather than reporting false complete coverage. PR squash merged into `main@2240ccb94bd6a2221a33956d85b7cc2f5b4f3a89`.

The scoped reusable evidence: bounded **source/candidate** raw EBML element commitments (all top-level protected objects + Attachments) can distinguish requested and unrequested raw data changes, while requiring `approvedToWrite:false` even when all inspected bytes match. The 64 MiB/256 KiB source-scan budget is *research-only* and the report's hash is a fixed-chunk SHA256 tree commitment, not ordinary whole-file SHA256. The comparator is deliberately too strict to certify legitimate semantically equivalent Matroska reserializations; it **does not** validate SeekHead/Cues offsets, CRCs, any arbitrary UID retargeting, media packet/timing semantics, storage transactions or a real existing-MKV writer. Known writer-level #77 chapter/tag loss remains open. This is Case/Test evidence; **no Canonical promotion**.

## Strict existing-MKV append-only AttachedFile candidate — 2026-10-12 (Pending external audit)

Product [Draft PR #101](https://github.com/11576865/MKV-Fast-Muxer/pull/101), head initially `1daa860edd3f9133a3972dec0e10209c787f5efd`, investigates an **isolated new writer class** for a small existing Matroska with original Tracks and Cluster, **no existing Attachments**, a known-length Segment header whose size VINT can hold the added element **without changing header width**, no Segment CRC-32, unknown top-level/preamble EBML or unproven Tag target inventory. Critically it refuses **any source TagAttachmentUID target, including orphaned targets**, so adding FileUID 1 cannot silently change referential semantics by resolving a previously missing attached resource.

It constructs an experimental **new** candidate Blob from the untouched original EBML/Segment child bytes, a same-width Segment size change and an appended `Attachments / AttachedFile` master at Segment end. Merged #100's separate byte contract must confirm every original protected Cluster/Track/Chapter/Tag/Info/Cues/Seek element remains byte-committed unchanged; its result still says `ATTACHMENT_DELTA_NEEDS_REFERENCES_OFFSETS_AND_WRITER_PROOF` with **no write authorization**. Input and new FileData sources are bound only to an authentic frozen plan via a private WeakMap; filenames and MIME remain untrusted, output never automatically downloads or replaces source.

The independent audit (Pending) creates a separate **MKVToolNix+mkvpropedit-authored attachment-free source** containing nested ChapterAtom and ChapterUID-targeted Tag, invokes this candidate, and demands `mkvmerge -J` parse source+new attachment, `mkvextract` match full chapter/tag XML and every compressed track's extracted bytes against source, and recover the appended text exactly, with source SHA-256 unchanged. Required machine result: `INDEPENDENT_APPEND_ONLY_EXISTING_MKV_TAG_CHAPTER_MEDIA_AND_ATTACHMENT_MATCH`. Exact-head Node/Vite/full Chromium and the non-gating external source oracle remain **Pending**. No production existing-MKV writer, no general appended-to-existing-Attachments support, no safe delete/replace, no universal SeekHead/Cues or structural validation, and #77 old FFmpeg/Wasm ChapterUID-tag loss remains open. Update this existing Case after evidence; no Canonical promotion.

## Negative control: EOF attachment append not discoverable in external audit — 2026-10-13

Product [PR #101](https://github.com/11576865/MKV-Fast-Muxer/pull/101) initial EOF-appending version at exact head `8ab009b5c1512781da5b216c08ee131a63752097`, [workflow 38274347769](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38274347769), passed **336/336 Node**, Vite and complete Chromium but emitted independent **`INCONCLUSIVE_OR_FAILED`**, code `INDEPENDENT_CANDIDATE_ATTACHMENT_METADATA_MISMATCH`. Artifact `p2-existing-mkv-append-attachment-candidate` ID `11758052884` retains source, candidate and JSON. Direct EBML inspection of those two real files showed an appended `Attachments` master at EOF after Tags and an original `SeekHead` with no Attachments entry. `ffprobe` enumerated only original video/audio streams. The exact reasons for MKVToolNix's missing/incorrect attachment metadata are not yet independently established, but this **demonstrates why “original bytes unchanged + new raw element present” is insufficient evidence of an externally usable existing-MKV modification**. Do not treat green gating CI as approval when a separate research oracle is red.

Revised Draft PR #101 head `de22f9a278b68db7eedfaa09478cd196167d45ac` now consumes a pre-Info reserved top-level `Void` with exact-length `Attachments` + remaining `Void`, preserving all **original non-Void** EBML child bytes and absolute offsets, unchanged Segment/SeekHead header and total output length. It keeps the strict original raw comparator's `BLOCKED_PROTECTED_BYTES_CHANGED` (Void truly changed), adds a separate narrower proof for unchanged non-Void offsets and commitments, and retains all publication/writer capabilities disabled. Missing/insufficient reserve and preexisting AttachmentUID target are refused. **New exact-head CI and independent real MKVToolNix source→candidate result Pending**, not verified. This is Case-level negative evidence and next experiment, not a Canonical rule or full writer proof. P0 #77 remains open.

## Bounded existing-MKV reserved-Void attachment candidate independently verified — 2026-10-13

Product [PR #101](https://github.com/11576865/MKV-Fast-Muxer/pull/101), exact final head `199eac02688abf3423928d529d9d9b72abbb699c`, passed **336/336 Node**, Vite and full Chromium E2E, with explicit successful **non-gating independent** verdict `INDEPENDENT_APPEND_ONLY_EXISTING_MKV_TAG_CHAPTER_MEDIA_AND_ATTACHMENT_MATCH` and `error:null` in [workflow 38283166453](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38283166453). CI artifact `p2-existing-mkv-append-attachment-candidate`, ID `11762097320`, contains actual independently authored source, edited candidate MKV and machine audit JSON. PR #101 squash merged as `main@35de55eae204b19e3e931d03033fa93373f86cef`.

The repaired candidate **does not tail-append physically**. It requires a pre-existing sufficiently large top-level `Void` immediately between `SeekHead` and `Info` and converts some bytes of that *same exact reserved span* into one new `Attachments / AttachedFile` master, leaving a valid residual `Void`. Thus original total MKV byte length, EBML and Segment headers, original SeekHead, and every original **non-Void** element's absolute offset, length and byte commitment remain unchanged. The strict original #100 comparator correctly reports `BLOCKED_PROTECTED_BYTES_CHANGED` because original Void changed; the candidate's separate narrower check verifies no other original element was rewritten. No writer/export privilege results from either comparison.

The **external independent source**, authored by MKVToolNix/mkvpropedit, had video/audio, nested ChapterAtom and real ChapterUID-targeted custom Tag and no original Attachments. `mkvmerge -J` discovered precisely one newly inserted text attachment (`text/plain`, exact 51-byte payload, FileUID 1), unchanged original exact TrackUID/codec. `mkvextract` recovered original and candidate chapter and tag XML equal and new attached FileData byte-identical. The research track-metadata extractor's initially unsupported `mkvextract tracks 0:*.bin` was replaced (not silently dropped) by an **independent FFprobe packet-level SHA256 + PTS/DTS/duration/size check**: all 143 media packet records (48 video + 95 audio) remained identical on real prior candidate; final oracle requires all records equal as well. Original source SHA256 unchanged. Initial EOF append and intermediate raw-track extraction red experiments remain recorded above as negative controls.

**Scope constraint:** only one new attached file to a small (60MiB source, 4MiB attachment) existing MKV with *no original AttachedFiles*, complete TagAttachmentUID graph containing zero targets (including orphans), accepted fixed pre-Info Void, and no unsafe unsupported Segment CRC or unknown top-level elements. No existing-MKV user edit/save action, no generic append, rename, replace or delete, no arbitrary media/format/unknown EBML or playback certification, no destination overwrite transaction. Old FFmpeg/Wasm #77 nested ChapterUID-tag loss remains **unfixed**; this distinct research writer does not repair the old path. No Canonical promotion.

## Existing-Matroska Void layout corpus and execution-time byte provenance — 2026-10-13 (Pending exact-head oracle)

Product [Draft PR #102](https://github.com/11576865/MKV-Fast-Muxer/pull/102), exact head initially `ce12714ceac9be5b8c22cedb8f3d868f0bde442a`, extends independently verified research-only reserved-Void attachment candidate #101. Source/payload identity remains bound to the same genuine immutable JobPlan, but **execution also now re-scans the entire bounded original source including reserved Void**, and requires all original raw byte commitments/header fingerprints unchanged from plan compilation; it separately hashes the newly added Blob FileData at plan and execution. Even a same-length, same-File-object source Void or attached payload byte swap must throw `APPEND_SOURCE_CHANGED_AFTER_PLAN` / `APPEND_ATTACHMENT_CHANGED_AFTER_PLAN`, respectively. This is not a persistent user-session identity guarantee or transaction-time overwrite lock.

Separate real external corpus script `scripts/p2-existing-void-layout-matrix.mjs` independently authors three `mkvmerge+mkvpropedit` source variants (default Cues, `--no-cues`, `--disable-lacing`) with original video/audio and nested ChapterUID-target Tag, creates a reserved-Void replacement candidate for each, and requires independent `mkvmerge -J` exact original TrackUID and attachment inventory, `mkvextract` full chapter/tag XML and added FileData, `ffprobe` per-packet SHA-256/PTS/DTS/duration parity, unchanged source hashes and unchanged output file length/non-Void offsets. It also requires explicit denial on an independently authored source with pre-existing Attachments, and on a derived still-readable same-length source where one pre-Info Void is split into two. Required machine verdict: `P2_VOID_LAYOUT_CORPUS_INDEPENDENT_ROUNDTRIP_AND_REJECTIONS_MATCH`; non-gating artifact `p2-existing-void-layout-independent-matrix`.

**Status at intake:** exact-head Node/Vite/full Chromium and named external matrix result **Pending**. No production existing-MKV editor or wider format certification; old FFmpeg #77 Chapter/Tag loss remains unfixed. This is an existing preservation Case extension rather than a new Canonical rule. A single success on multiple options of the same writer family is not broad cross-writer proof.

## P2-V three-layout existing-MKV reserved Void corpus independently verified — 2026-10-13

Product [PR #102](https://github.com/11576865/MKV-Fast-Muxer/pull/102), exact tested head `8e2512bef015e287da6aca78355e0ae217d6bbff`, passed **338/338 Node**, Vite and full Chromium Browser E2E in [run 38285406375](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38285406375). The **non-gating external oracle** explicitly logged `P2_VOID_LAYOUT_CORPUS_INDEPENDENT_ROUNDTRIP_AND_REJECTIONS_MATCH`, `error:null`, and identified five distinct verdicts: `default-cues`, `no-cues`, and `disable-lacing` were independently MKVToolNix-authored *success* cases; `preexisting-attachments` was an independently authored and *refused* source; `two-preinfo-void-elements` was a derived, independently readable but *refused* pre-Info layout. Artifact `p2-existing-void-layout-independent-matrix` ID `11763077872` retains raw sources, generated candidates and JSON. PR #102 merged as `main@ec65c26f6affd265aeb693b5c066166132b12c91`.

Every positive experiment required `mkvmerge -J` exact original TrackUID/codec and correctly discovered new FileUID=1, FileName/MIME/size; full source→candidate chapter and tag XML equality via `mkvextract`; full original media packet SHA-256, PTS, DTS, duration/size parity via independent `ffprobe`; byte-exact new attachment extraction; unchanged source SHA-256, output file byte length and original **non-Void** element offsets and fingerprints. Unit tests additionally simulate source Void and added FileData byte mutations after a genuine frozen JobPlan is created, and require `APPEND_SOURCE_CHANGED_AFTER_PLAN` / `APPEND_ATTACHMENT_CHANGED_AFTER_PLAN` on execution despite identical source object references and sizes.

The first CI attempt [38285258058](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38285258058) failed at module parse time because JavaScript `String.replace` replacement-string `$&` expansion corrupted the MIME regex; repaired before final head verification and separately recorded under the existing project's Foundry Bug evidence. No product existing-MKV output UI, mutation of original source, generic existing-attachment CRUD or unsupported Seek/Cues/CRC semantics are claimed. Three MKVToolNix variants **do not** amount to broad cross-writer compatibility. The legacy FFmpeg/Wasm P0 #77 ChapterUID-targeted Tag loss remains **unfixed**. No Canonical promotion.

## FFmpeg-native author refusal vs MKVToolNix decoder/seek parity — 2026-10-13 (Pending exact-head oracle)

Product [Draft PR #103](https://github.com/11576865/MKV-Fast-Muxer/pull/103), head initially `58facfc721ccb8996721e5fbc6687e48ba043453`, adds two explicitly distinct external observations: (1) independently **FFmpeg-native Matroska** sources from default `-c copy` and `-reserve_index_space 4096` options are parsed by `mkvmerge -J`, decoded by FFmpeg and individually classified by real top-level EBML layout and pre-Info Void capacity. A 1024-byte resource must be refused by the **narrow reserved-Void writer** with a precise eligibility code when the original slot is insufficient; this must not be called malformed Matroska or global FFmpeg source incompatibility. If either source unexpectedly becomes eligible, demand a separate independent **positive** source/candidate oracle; do not silently expand allowed write capability. (2) Reuse the independently verified three MKVToolNix source/candidate pairs **only if** P2-V's named corpus JSON is green, and require decoded FFmpeg video/audio framehash equality at two concrete seek positions (0.35s/1.25s), plus indexed FFprobe packet/hash/time range comparison for cases with Cues. The no-Cues member gets full-decode equality only and must not count as a seek success.

Required new non-gating machine verdict `CROSS_WRITER_FFMPEG_LAYOUT_REFUSALS_AND_MKVTOOLNIX_DECODER_SEEK_MATCH`, artifact `p2-cross-writer-decode-seek-matrix`. Exact-head Node/Vite/full Chromium and external JSON are **Pending** at intake. No real product existing-MKV writer, no generalized player compatibility, no ChapterUID-tag writer loss fix (#77), no promotion to UIGS Canonical. This extends the preexisting Matroska preservation Case rather than creating a new generalized rule.

## P2-X FFmpeg-native refusal and MKVToolNix source→candidate decoded-seek parity verified — 2026-10-13

Product [PR #103](https://github.com/11576865/MKV-Fast-Muxer/pull/103), exact tested head `58facfc721ccb8996721e5fbc6687e48ba043453`, passed **338/338 Node**, Vite and full Chromium Browser E2E in [workflow 38286995079](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38286995079). The **separate non-gating external research step** explicitly logged `CROSS_WRITER_FFMPEG_LAYOUT_REFUSALS_AND_MKVTOOLNIX_DECODER_SEEK_MATCH`, `error:null`. Artifact `p2-cross-writer-decode-seek-matrix` ID `11763917251` contains the JSON and actual FFmpeg-native MKVs. PR squash merged as `main@f87c2178b573baf6150f0d78c20ebdcec68a87a2`.

The two independently **FFmpeg native Matroska authored** sources (default copy mux and `-reserve_index_space 4096`) were readable by `mkvmerge -J` and decodable with FFmpeg video/audio; both were precisely refused by the small reserved-pre-Info-Void research writer when proposing a 1024-byte generic attachment: `APPEND_VOID_SLOT_CAPACITY_EXCEEDED`. They were **not malformed**; FFmpeg's index-reserve setting did not guarantee sufficient space in the particular pre-Info Void slot this writer needs. This confirms source validity and candidate-writer eligibility are separate dimensions.

For previously independently verified MKVToolNix source/candidate pairs, all three variants maintained full FFprobe packet hash/timing parity and independent full video/audio decoding behavior. The **default-Cues** and **disable-lacing** pairs also matched FFmpeg decoded framehash/count at **0.35s and 1.25s** for video and audio, plus indexed FFprobe seek-window packet hash/timestamp observations. The **no-Cues** pair was deliberately classified full-decode only: **no seek functionality claim**. This is a single decoder/seek test matrix, **not** a broad device/player conformance assertion or production existing-MKV editor approval. Legacy FFmpeg/Wasm no-edit #77 nested ChapterUID-targeted Tag loss remains unfixed. No UIGS Canonical promotion.


## Three-step narrow writer product UI and external browser oracle (2026-10-13; Pending exact-head CI)

Product [PR #110](https://github.com/11576865/MKV-Fast-Muxer/pull/110), branch `feat/three-step-existing-mkv-limited-attachment-workflow`. The independently MKVToolNix-authored reserved-**pre-Info Void** candidate was previously verified in exact product E2E [workflow 38345684462](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38345684462), including named machine verdicts `INDEPENDENT_APPEND_ONLY_EXISTING_MKV_TAG_CHAPTER_MEDIA_AND_ATTACHMENT_MATCH`, `P2_VOID_LAYOUT_CORPUS_INDEPENDENT_ROUNDTRIP_AND_REJECTIONS_MATCH`, and `CROSS_WRITER_FFMPEG_LAYOUT_REFUSALS_AND_MKVTOOLNIX_DECODER_SEEK_MATCH`. These prior fixture results justify implementing a **limited separate opt-in workflow**, not general write authorization.

New implementation under review: reuse the strict plan+candidate EBML writer in a `prepareVerifiedLimitedAppend` orchestrator; budget-check **before** any full-source hash; bind source and payload full SHA before/after; require identical original non-Void raw bytes and EBML offsets, stable Segment/SeekHead and exact output FileData, MIME, UID and filename; create a separate output Blob. A dedicated reviewed source+attachment+MIME/filename UI only enables download after actual candidate self-audit. Changed source/payload/metadata or review revokes preparedness; no standard mux or BatchRunner integration, no source overwrite. User-visible scope remains experimental and narrow.

The new Chromium E2E independently authors a nested-chapter, ChapterUID-targeted Tag source via MKVToolNix/mkvpropedit; exercises review and downloaded output; uses **external** mkvmerge, mkvextract chapter/tag XML, FFprobe packet hashes and physical new attachment extraction. Checks that an existing-attachments source is refused and previous download invalidated. Unit tests cover refusal and size budgets.

Status at intake: exact-head build/Node **success**, full Chromium and external source-output scenario **Pending** at [PR #110](https://github.com/11576865/MKV-Fast-Muxer/pull/110). Never call this a general Matroska writer, universal Chapter/Tag writer fix, source-format-independent behavior or physical-device playback validation. This extends this existing Case; do not promote Canonical from a single product.

## Three-step narrowly eligible writer exact-head production integration verified (2026-10-13)

Product [PR #110](https://github.com/11576865/MKV-Fast-Muxer/pull/110), exact tested head `acf7100839574f4afc40952ce00b5a943b8fed5a`, merged `main@03320d45608d1c3e394df84c2289ade3a253e4a2`.
- [Node tests and build 38347441776](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38347441776): **success**.
- [Full Chromium E2E 38347441773](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38347441773): **success**, exact log line `P2-A opt-in existing MKV independent browser writer PASS` followed by `All browser E2E scenarios PASS`. The new browser scenario independently authored a nested-ChapterUID source via MKVToolNix/mkvpropedit, generated & downloaded a new existing-MKV one-attachment candidate in the UI, compared original/output mkvextract Chapters/Tags XML, extracted FileData, and compared all compressed FFprobe packet/timestamp records. Source with preexisting attachments was denied and stale download disabled.
- The same run's separate P2-A external oracle reported `INDEPENDENT_APPEND_ONLY_EXISTING_MKV_TAG_CHAPTER_MEDIA_AND_ATTACHMENT_MATCH`, `error:null`, and cross-writer/seek matrix `CROSS_WRITER_FFMPEG_LAYOUT_REFUSALS_AND_MKVTOOLNIX_DECODER_SEEK_MATCH`, `error:null`.
- Source hashing is bounded by source/payload size guards *before reads*. UI output is isolated from the FFmpeg/Wasm and BatchRunner paths, source is never overwritten, and all changes require explicit opt-in review.

Precise delivery status: **a usable, opt-in, narrow existing-MKV copy writer class** has reached production main; **general existing-MKV editor, preexisting-attachment CRUD, arbitrary chapter/tag mutation, large source support, unknown EBML and a fully independent FFmpeg media core remain unresolved**. This is not proof that every eligible third-party source works or plays correctly in arbitrary clients.

Deduplicated as extension of this existing Case. No new Canonical rule is inferred.


## Extension: Multiple new attachments in one existing reserved-Void MKV (2026-10-13; CI pending)

Product [PR #111](https://github.com/11576865/MKV-Fast-Muxer/pull/111), head `e96dfdb902918c8b3e23057f563ce613f4134e02`, extends the exact same bounded and externally checked one-attachment eligibility class rather than declaring generalized Matroska write safety:
- Encode one Attachments master containing 1–8 new AttachedFile children, unique FileUIDs 1..N, no pre-existing attachments, no orphan AttachmentUID target links, no unsafe top-level/CRC elements; original pre-Info Void space must fit the entire master plus valid remainder. Source ≤60 MiB, aggregate payload ≤4 MiB.
- Freeze per-file metadata and hashes; refuse unsafe duplicate filename auto-rewriting; after generating the new source-length-preserving MKV Blob, verify every actual attached FileData by unique FileUID, name, declared MIME, size and SHA-256. The actual source and staged files are rehashed before output is exposed.
- The previously opt-in existing-MKV UI now allows 1–8 selected files, lists proposed names/MIME, requires renewed review, preserves legacy single-file fields, and invalidates cached downloads on source/list/options changes.
- Node fixtures test two actual EBML attachments plus budget, duplicate, preexisting attachments, insufficient slot refusals. The real Chromium MKVToolNix-authored tagged/nested chapter scenario now tests two attachments and external mkvmerge/mkvextract/FFprobe packet equivalence, in addition to the previous single-file scenario.

**Status: Submitted, exact-head Node/build and full Chromium/E2E Pending.** Previous PR #110 passing evidence is not a substitute for this new multiple-attachment head. All output is experimental, no general existing-MKV writer, prior attachment CRUD, device playback conformance or full FFmpeg adapter decoupling. Deduplicated as another observation in this existing Case; no Canonical promotion.


## Exact-head verified: two new attachments in one existing MKV reserved-Void output (2026-10-13)

Product [PR #111](https://github.com/11576865/MKV-Fast-Muxer/pull/111) exact validated head `501747687c3c9f83a925213a30ab2c4819b54138`, merged `main@6eb098e7a44a27d84588b9e5faf8835262d876f9`.

- [Node/build workflow 38349722787](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38349722787): **success**, includes 383/383 Node tests and build.
- [Full real Chromium workflow 38349722782](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38349722782): **success**, including the exact log assertions `P2-A opt-in existing MKV independent browser writer PASS` and `All browser E2E scenarios PASS`.
- New true browser scenario uses a MKVToolNix source with nested chapters and targeted tags, selects **two real File objects** in one UI review, creates/downloads an MKV and requires independent external `mkvmerge -J` recognition of **both** actual AttachedFile entries. Both resources are extracted with `mkvextract` and compared byte for byte, source vs output Chapter/Tag XML compares identically, and ordered FFprobe compressed media packets/PTS/DTS/duration/hash compare identically. Original source file size and output equal, original source remains separate.
- Source already containing attachments and missing/insufficient pre-Info Void remain refused. Single attachment workflow continues passing. Duplicate filenames and payload budget refusals have dedicated Node checks.
- First CI failures reflected test-fixture overlap (duplicate filenames triggered before intended preexisting-attachments gate) and double-escaped regex in browser inventory assertion; both corrected **without disabling production safety checks**; only final exact-head green run is accepted.

**Bounded scope:** 1–8 new AttachedFile children inside ONE newly placed Attachments master, no existing attachments, source ≤60 MiB, aggregate new bytes ≤4 MiB, all source headers/non-Void EBML elements and offsets unchanged. No arbitrary Matroska editor, no general existing attachment CRUD, no arbitrary device playback certification, no full FFmpeg media-core decoupling. Case evidence only; no Canonical change.


## Existing-MKV per-AttachedFile metadata editing and plan-freshness (2026-10-13)

Product [PR #115](https://github.com/11576865/MKV-Fast-Muxer/pull/115), head `8719dbc3bfbcf3bc7ac26d18a1de93313a6ba4b7`. Builds on the **already externally verified narrow** existing-MKV 1–8 new attachments / reserved pre-Info Void writer (PR #111) without broadening its capability.

Observation: The original multi-file UI only displayed File.name and File.type, which can be unsafe, conflicting, or incorrect; unlike the single-item path it offered no in-workbench remediation. New product code presents individually editable filename and MIME fields, checks the **same** filename policy as the actual writer (no automatic collision rename), enforces aggregate source limits, and snapshots exact File references plus user-reviewed proposed output metadata. All metadata edits invalidate prior review and the prepared Blob URL. Before a late async result can be published and again before download, the UI compares both the actual current field values and same File identities against the accepted snapshot. The server-independent writer retains its own exact FileData/UID/hash checks.

Node tests validate unsafe/duplicate/case-equivalent output names, invalid MIME, per-item changes, same-metadata source File replacement and byte budgets. Existing Chromium MKVToolNix-authored source scenario additionally tests forbidden duplicate metadata, explicit renamed/MIME-corrected second attachment, revoked old download, and external mkvmerge/mkvextract confirmation of the revised output while Chapter/Tag XML and media packets remain unchanged.

At this Intake: exact-head Node/build [workflow 38365289395](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38365289395) **success**; full Chromium [workflow 38365289426](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38365289426) **Pending**. No claim of external output acceptance until it passes. This is an extension of the existing Case, not a Canonical change.


## PR #115 exact-head per-attachment editor, reviewed draft and independent output (2026-10-13)

Product [PR #115](https://github.com/11576865/MKV-Fast-Muxer/pull/115) exact tested head `76c8840b37c69cff536c2316fc0635af3981694c`, merged `main@15ca805db83e640f867bcbc6e36502d89af25f61`. [Node/build 38366083228](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38366083228) **success**; [full Chromium E2E 38366083221](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38366083221) **success**.

The previously landed 1–8 new-attachment writer now has *per-attachment* filename and MIME field editing in the real UI. The pure draft is bound to exact File objects; invalid MIME, duplicate/case-equivalent/unsafe names, stale metadata, over-budget selections and non-reviewed modifications cannot produce a valid downloadable candidate. Every per-item field change invalidates previous review and prepared Blob. Existing single-attachment operation is still supported. Chromium independently verifies the edited fields and exact FileData with mkvmerge/mkvextract, and preservation of original chapters/tags and media packet hashes.

Do not extrapolate this to general existing Matroska CRUD, large unknown layouts or physical-device playback. This is another corroborated product-specific Case detail, **not Canonical**.
