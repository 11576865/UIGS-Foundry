# Candidate · Same-byte metadata leaf editing can preserve an existing binary container graph without a general writer

Date: 2026-10-15
Status: **Candidate / Product implementation submitted / exact-head integrated CI Pending** (not Canonical)
Project: [MKV-Fast-Muxer PR #147](https://github.com/11576865/MKV-Fast-Muxer/pull/147)
Submitted precise head: `37c4996b34e459eaf4e0de3b9df05458f9f2260a`
Main-targeted integrated gate: [PR #148](https://github.com/11576865/MKV-Fast-Muxer/pull/148)

## Proposed scoped technique

Where an existing complete finite Matroska Segment contains a supported known UTF-8 leaf `Chapters/EditionEntry/ChapterAtom/ChapterDisplay/ChapString` or `Tags/Tag/SimpleTag/TagString`, modifying **exactly one value with identical UTF-8 byte length** can form a real edited output Blob without touching EBML size/ID fields, Segment geometry, chapter/track/attachment UIDs, SeekHead/Cues pointers or media Cluster packet bytes.

This is stronger than a read-only mock editing interface, but far narrower than arbitrary Chapter/Tag object mutation or general EBML structural writer. Reject unknown top-level structure, source/source-size drift, unknown-sized Segment, CRC-bearing relevant ancestors, malformed UTF-8 and unequal byte length. Original source must remain untouched. Plan is one-shot and bound to the source File bytes rather than authorizing JSON or broad writer rights.

## Submitted independent test boundary

- `src/p2-matroska-inline-metadata-writer.js`: inspect real chapters/tags tree, select existing literal field, validate old value and same byte length, produce only new copy, then re-inspect all metadata field paths, top-level offsets and unchanged byte commitments; directly byte-compare the entire source/output outside the selected payload; source SHA rechecked.
- `src/p2-matroska-inline-metadata-ui.js`: existing field selection, reviewed replacement, local output evidence, manual download.
- `tests/p2-matroska-inline-metadata-writer.test.mjs`: synthetic nested chapter and targeted tag in a **trackless Matroska** positive/negative matrix, no assumed video root.
- Browser `scenarioTracklessMkaRealChapterTagTextEdit`: MKVToolNix writes real audio-only `.mka` with a nested ChapterUID-linked Tag, browser actually edits TagString then ChapString and downloads the independent copy. Native `mkvmerge`, `mkvextract` and `ffprobe -show_packets -show_data_hash sha256` check precise two textual changes, unchanged ChapterUID target, unchanged original audio packet stream and no video tracks.
- Exact PR-head workflow and native output verdict **not yet observed** at intake. Do not call this Case Accepted.

## Boundaries and dedup

- This is not an arbitrary length-changing text editor, a CRC recomputation writer, an arbitrary add/remove/move Chapters/Tag writer, nor a general no-video container *creator*; PNG-only and multi-attachment-only candidate creation already exist separately.
- Search `ChapString TagString same byte length editor`, `Matroska chapter tag text in-place rewrite`, `metadata byte exact nonvideo mka`, `CRC ancestors text leaf patch`. Existing `inbox/cases/2026-10-14-mkv-existing-attachment-same-size-filedata-preservation.md` establishes a similar **same-length FileData** technique but not byte-exact *chapter/tag semantic text* edits in an audio-only container. Existing `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md` covers the general preflight concern; this Candidate is a narrower testable implementation.
- Single observation cannot amend Canonical; promotion would require exact-head CI/native results, independent malformed/CRC corpus and review of the supported Matroska text subtree subset.
