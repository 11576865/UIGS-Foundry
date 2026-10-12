# Bug: Browser MKV preserve-all remux drops nested chapter and linked tag (confirmed)

Date: 2026-10-12
Status: Confirmed in one reproducible CI fixture / fix pending
Severity: High — silent semantic data loss from source structures in apparently successful output
Product: `11576865/MKV-Fast-Muxer`
Issue: https://github.com/11576865/MKV-Fast-Muxer/issues/77
Evidence PR: https://github.com/11576865/MKV-Fast-Muxer/pull/76
Reproduced CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38194692640
Existing related case: `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`
Duplicate search: nested chapters missing; chapter targeted tags dropped; ChapterUID remux; preserve-all chapters in Foundry/bugs — no matching confirmed bug found.

## Reproduction

1. Create a 2-second media input, author Matroska **using mkvmerge** with a parent ChapterAtom `510010` and nested child ChapterAtom `510011`, chapter display language `eng`, and EditionUID `510001`. Add one binary attachment.
2. Inject custom `P0_NESTED_CHAPTER_KEEP` tag via `mkvpropedit --tags all:...`, targeting ChapterUID `510011`; add independent global `P0_GLOBAL_KEEP` tag. `mkvmerge --global-tags` must **not** be used for this, since it strips Targets.
3. Self-check authoring with `mkvextract` chapter and tag XML to ensure the actual input carries hierarchy, targeted tag and UID; this check succeeded in CI.
4. Import only this MKV in the real browser soft-mux UI, select no new edits, use default preserve-all mode, and produce output.
5. Independently run the P0 `--deep` comparator using `ffprobe`, `mkvmerge`, `mkvextract` and normalized XML.

## Observed output

- Parent chapter UID `510010` remains, nested child chapter `510011` **vanishes**.
- Source EditionUID `510001` is no longer present in output.
- Parent chapter display language changes `eng` → `und`.
- Chapter-targeted tag `P0_NESTED_CHAPTER_KEEP` → ChapterUID `510011` **vanishes**.
- The global tag `P0_GLOBAL_KEEP` **survives**.
- Browser mux produced a file and did not report these semantic losses as a blocking error.
- CI comparator reported `DIFFERENCE_DETECTED` for `chapterHierarchy` and `p0MarkedTags`; Browser E2E finished RED **on purpose**.
- Earlier P0 test of a simpler FFmpeg-authored MKV passed `CHECKED_FIELDS_MATCH`, demonstrating why that green is insufficient.

## Scope and hazard

This is proof of data loss for a **specific, independently authored** MKV structure and current browser mux execution path, not proof of universal Matroska/FFmpeg failure or complete EBML preservation coverage. Nested chapters may be flattened while a flat ffprobe chapter list looks plausible; metadata targets may consequently be lost.

The unsafe product-level generalization would be: `preserveAllSourceStreams` / append-only mux success implies all Chapters/Tags/EBML references are preserved. It does not for this fixture.

## Required guard and verification

- Treat source MKV semantic structure as distinct from recognized streams. Before allowing a modification, detect whether unsupported nested/targeted metadata could be lost (or limit the operation to a backend proven to preserve the structure).
- If safe preservation cannot be proven, **block** the modification or disclose a constrained/degraded *new* output requiring explicit acceptance; never overwrite the original.
- Test independent backend strategy (Matroska-specific tools/metadata-only edits where appropriate) rather than assuming more FFmpeg flags solve the loss.
- Preserve the authored fixture, complete independent audit JSON and red CI history; report non-coverage and mark unknown.
- Re-run legacy subtitle, font and batch regression alongside any proposed guard.

Status: Product fix not implemented. No general cross-project Canonical change authorized; this record is a concrete Bug with attached reproduction evidence.


## Independent-backend control — important limitation on attribution

Control workflow https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38195156550 ran a plain `mkvmerge` remux of the *same self-checked source*. The exact same deep oracle reported **no `chapterHierarchy` difference**, but **did report loss of `P0_NESTED_CHAPTER_KEEP` linked to ChapterUID `510011`**. The global `P0_GLOBAL_KEEP` survived.

Therefore:
- Browser FFmpeg/Wasm writer: confirmed nested chapter/edition/language mutation **and** targeted-tag loss.
- Plain MKVToolNix mkvmerge writer: nested chapter retained, targeted-tag lost.
- Neither is yet a proven all-structure preservation solution for this source.

The first browser red was not merely a broken fixture; the independent writer control both supports the distinct nested-chapter loss and reveals an additional cross-writer problem with ChapterUID-targeted tag retention. Avoid concluding that switching to MKVToolNix alone fixes the tag-target relation. The control step is non-gating to allow Browser E2E to run and independently fail with its own red semantic oracle; both JSON evidence files are retained. No Canonical promotion or production fix.

Source product Issue #77 comment documents this refinement.


## Partial mitigation deployed (2026-10-12)

A bounded read-only preflight hazard detector has been merged from PR #78 into main at `9c49af8b32bc0b0926a07dfc1bad700627d60787`, with head-specific Node 226/226 and Chromium E2E PASS. It blocks the independently reproduced nested chapter and chapter-targeted-tag source **before** output in both single and mixed batch workflows. It explicitly warns, without claiming preservation, for otherwise common TrackUID/AttachmentUID-targeted Tags; the initial broad hard-block caused a legacy E2E regression and was corrected.

**Bug remains unresolved**: the actual browser FFmpeg/Wasm remux engine still loses nested chapters and UID-targeted tag semantics on that source when executed without guard, as proven by evidence PR #76. The merged safety check is a prevention barrier for recognized inputs, NOT a writer fix, nor proof of complete EBML preservation. Source issue #77 must remain open.


## Product copy review — 2026-10-12

Tracking issue: https://github.com/11576865/MKV-Fast-Muxer/issues/80

Despite the confirmed chapter/tag source-semantic loss and only partial safety preflight, `README.md` still promises `完整保留原容器结构，仅追加` for ordinary MKV; `src/main.js` still says `完整保留并追加` / `保留 Chapters 与 metadata` and runtime `正在无损封装 MKV`. Those messages do not distinguish media stream copy from EBML container-semantic preservation. This is a confirmed user-facing claim/technical-capability mismatch, not proof of a new data-loss mechanism. Keep it with the existing Bug as a terminology/claim scope issue; independently update code and documentation with narrow, source-supported behavior and regression tests.

Source issue #77 remains open after partial preflight; this is not Canonical policy change.


## Verified #80 copy correction (2026-10-12)

Product Issue #80: https://github.com/11576865/MKV-Fast-Muxer/issues/80 (closed)
Product PR #82: https://github.com/11576865/MKV-Fast-Muxer/pull/82 (merged)
Commit: `c01e7411e83ab85d64b7e924d55a82fde6c6a2ea`
Integrated pre-merge Chromium CI: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38200883249

The product formerly exposed `完整保留原容器结构，仅追加`, `正在无损封装 MKV`, and Chapter/metadata output-plan assertions as though `-map 0` / `-c copy` guaranteed complete EBML semantic preservation. In independent #77 evidence this was false. PR #82 changed UI, runtime and README copy to distinguish stream-copy/remux from UID/Chapter/Tag preservation, linked the source-data loss and preflight limitation, and added a static regression check against these absolute promises. The integrated #79 + #80 branch passed **227/227** Node tests and complete Chromium E2E including batch preflight snapshot and cancellation.

This is verified correction of **misleading product claims**, not a writer or serializer fix. Original #77 remains OPEN and independent red source evidence remains intact. No Canonical change authorized.


### Final integrated-main confirmation — 2026-10-12

Main `c01e7411e83ab85d64b7e924d55a82fde6c6a2ea` GitHub Actions [Chromium E2E](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38201136018) passed 227/227 Node tests and full browser scenarios, including delayed source-preflight stale-plan and cancellation tests; main [Pages deploy](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38201136026) passed. Thus #80's accurate copy is integrated with #79's transactional batch-start change and verified on the final merged commit. Product #77 (original Matroska chapter/tag loss under ordinary remux) remains OPEN. No Canonical change.
