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
