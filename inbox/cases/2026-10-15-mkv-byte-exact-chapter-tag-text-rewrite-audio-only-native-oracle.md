# Case · Exact-width UTF-8 Matroska chapter/tag text patch with unchanged graph and native audio-only oracle

Date: 2026-10-15
Status: **verified integrated exact-head Chromium/native Case; product Draft PR not merged; not Canonical**
Product: [MKV-Fast-Muxer PR #147](https://github.com/11576865/MKV-Fast-Muxer/pull/147)
Integration: [PR #148](https://github.com/11576865/MKV-Fast-Muxer/pull/148)
Exact combined head: `dd709601645a8e5787f2b6e8e22c026823e2981e`
Evidence: [full Node/build/real Chromium GitHub Actions run 38608413912](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38608413912), SUCCESS: **579/579 Node, Vite build and actual E2E with independent native MKVToolNix/ffprobe oracle**. The run logs record `P2 R5 native audio-only chapters/tag output and UID/packet oracle PASS`.

## Initial gap and justified capability boundary

The established complex-Matroska P0 counterexample (#77) prohibits assuming an FFmpeg remux preserves arbitrary nested ChapterAtom and ChapterUID-targeted Tag graphs. Previously the source editor could preserve many protected metadata elements unchanged, but not **edit** Chapters/Tags in the original container.

When the desired change is the payload of exactly one existing Matroska `ChapString` or `TagString`, and replacement UTF-8 has **exactly the same byte length**, an offset-stable patch can replace only the original string bytes. The resulting EBML hierarchy, Segment/master sizes, UID values, SeekHead and Cues offsets and media Cluster packet bytes need not change. This is a distinct operation class, **not a generalized chapter/tag writer**.

## Submitted actual browser implementation

- `src/p2-matroska-inline-metadata-writer.js` uses a bounded whole-source raw EBML inspection and recognizes only explicit Chapter/Edition/ChapterAtom/ChapterDisplay/ChapString and Tags/Tag/SimpleTag/TagString ancestry. Rejects unknown top-level IDs, CRC inside edited hierarchy or at Segment level, unknown-sized Segment, invalid UTF-8, a missing/ambiguous target, length mismatch, no-op, over-budget source, missing explicit review, and fake/reused plans.
- A frozen one-shot plan binds a real immutable browser File in a private WeakMap, checks full source SHA-256 before execution, creates a separate Blob by changing only the identified text bytes, reparses the entire new container and verifies all field identities plus all protected non-target top-level bytes, and directly byte-compares the untouched prefix/suffix against the original. Never overwrites source or calls FFmpeg.
- `src/p2-matroska-inline-metadata-ui.js` and main `index.html` offer real File selection, concrete discovered chapter/tag title, explicit same-byte review, prepare, SHA evidence and manual independent copy download.
- `tests/p2-matroska-inline-metadata-writer.test.mjs` verifies a synthetic Matroska with **no video/track**, nested ChapterAtom and chapter-targeted Tag; chapter and tag byte edits both work, source remains hash identical and all EBML offsets remain stable. Checks adversarial CRC, unknown top-level, unknown size, malformed UTF-8, size increase/shrink, forged or replayed plan.
- `scenarioTracklessMkaRealChapterTagTextEdit` builds a **native independent MKA audio-only source** via `mkvmerge` with nested XML chapters and ChapterUID-targeted tags, reads the actual completed output from the browser, uses native `mkvextract` chapters/tags XML and `ffprobe` packet SHA-256 to prove exact intended metadata text changes and unchanged audio packets/track UIDs. It also checks no video tracks are introduced and source SHA remains unchanged.

This is verified for the **scoped sample and code head**, not every Matroska layout, all players, every language/Unicode encoding, large file budgets, or general metadata writing.

## De-dup / related Foundry knowledge

Search: `same-byte chapter tag string Matroska`, `chapter tag inline editor`, `trackless audio-only chapter tag editing`. No directly matching entry. Related prior Cases:
- `inbox/cases/2026-10-14-mkv-existing-attachment-same-size-filedata-preservation.md`: same-size *attachment FileData* patch, not Chapter/Tag string editing.
- `inbox/cases/2026-10-14-mkv-nonterminal-attachments-native-seekhead-relay.md`: move one Attachments master via relay while preserving original Chapters/Tags.
- `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`: non-video Matroska as product requirement, not native chapter/tag editing.

Reusable rule suggested by this Case: an object-specific writer can be validated by **exact byte span + unchanged EBML geometry + required UID graph unchanged + unrelated byte equality**, even when a general format rewrite is outside the safety envelope. This is a Case, not evidence to amend Canonical from one project path.

## Remaining risks and CI semantics

Exact-head work can be externally verified before PR merge, but a successful Draft PR test is not itself merge or release acceptance. The current modification may still be rejected by strict CRC/unknown-size/unknown hierarchy rules. Chapter insertion, deletion, resizing, timestamp editing, changed UID targets, arbitrary Tag expansion and all unknown layouts remain unsupported. Product P0 issue #77's conventional remux is NOT resolved by this operator. Any promotion must require broader corpus, negative oracle and independent real software results.
