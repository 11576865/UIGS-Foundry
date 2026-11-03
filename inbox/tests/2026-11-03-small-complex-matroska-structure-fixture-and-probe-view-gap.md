# Test — Compact real Matroska structure fixture versus stream-probe projection

Date: 2026-11-03
Status: **Observed local synthetic fixture / FFmpeg and independent EBML traversal; native MKVToolNix readback pending**
Scope: Softmux / Matroska general test methodology, not product feature acceptance.
Fixture: conversation artifact `Matroska_复杂结构学习样本_20秒.mkv`, size **1,047,610 bytes**, SHA-256 `568d0815c2900bc05772b2e9590ffe8191de63117e2b8f937475334c7e2e2a6e`. Local-only file; not committed or asserted as a permanent GitHub test fixture.

## Why this is new evidence
A learning request asked for *structurally complex, not large*, MKV. Constructed a genuine 20-second Matroska file from synthetic images, English offline text-to-speech and tone audio, styled ASS, SRT and WebVTT, four different MIME attachments, and appended standard EBML Chapters/Tags while preserving old clusters, Cues and source SeekHead offsets. A second SeekHead in existing Void was added for the new top-level elements. RFC 9559 and matroska.org schema permit multiple Tags and SeekHead elements and Chapters after Clusters; one Chapters master holds multiple EditionEntry and recursive ChapterAtom.

Exact audited structure: 8 actual Matroska `TrackEntry` objects (H.264 + VP9, AAC + Opus + FLAC, ASS + SubRip + WebVTT), 4 `AttachedFile` entries (PNG/SVG/JSON/TXT), 2 `EditionEntry` (one default, one alternate), 8 `ChapterAtom` (three nested children), and nonzero actual UID-targeted tags referencing TrackUID, ChapterUID, EditionUID and Attachment FileUID, plus a nested SimpleTag. All targets were matched to source element UIDs and all 4 extracted FileData contents hash-matched original attachments. SeekHead positions resolved to correct element ID and the Segment size was contiguous after appending. Both video/audio routes decoded for scoped 2-second runs via local FFmpeg 7.1.5; FFprobe decoded container metadata and first default edition's three top-level chapters.

**Parser/representation discrepancy, not necessarily corruption:** `ffprobe -show_entries stream` lists the PNG attachment as an additional synthetic `video/png` stream (typically `attached_pic`), despite the EBML container actually containing only **two video TrackEntries**. A plain FFprobe chapter listing returned only 3 top-level default-edition chapters rather than all 8 recursive ChapterAtoms across two editions. Therefore stream probe row count and chapter list count cannot be used as independent oracles for complete Matroska raw object cardinality/relations.

## Proposed future reusable test
1. Assert EBML raw TrackEntry counts/type and attachments separately from FFprobe's synthetic attached pictures.
2. Assert each recursive ChapterUID across Editions and TagChapterUID references, not just `-show_chapters` flat rows.
3. Check target UIDs as uint64 losslessly; do not use JS float comparison for > 2^53.
4. Re-mux a copy under test and require semantic invariants across raw chapters/editions, target Tags and attachments, not only playable media or codec names.
5. Use **independent native MKVToolNix `mkvmerge -J` / `mkvextract chapters` / `mkvextract tags`** to validate the exact compact fixture before promoting this to a durable CI oracle. At present, MKVToolNix not installed in local environment, so no independent native result exists. Also real hardware/player acceptance not measured.
6. Do not overgeneralize: this is a pedagogical synthetic case, not a large-file performance fixture, complete RFC conformance certification or a test of original font attachment round-trips.

Related historical Foundry family: `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md` for no-op remux preservation losses, `inbox/bugs/2026-10-12-mkvmerge-json-uint64-uid-precision-loss.md` for JS UID parse risks, `inbox/cases/2026-10-14-mkv-nonterminal-attachments-native-seekhead-relay.md` for index relocation. This test adds **small content-rich fixture construction and probe projection discrepancy**, not a duplicate of those cases. No Canonical promoted.
