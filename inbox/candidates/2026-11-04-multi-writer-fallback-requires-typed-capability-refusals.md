# Candidate: Alternate writer fallback requires explicit capability-refusal classification

Date: 2026-11-04
Status: **Candidate / product implementation submitted, full exact-head CI pending**
Domain: Matroska editing, multi-backend routing, error containment, media preservation
Product: `11576865/MKV-Fast-Muxer`, Draft [PR #236](https://github.com/11576865/MKV-Fast-Muxer/pull/236), head `28d527ace9dee5efee1c2605b8ddf21986c2a0b1`
Trigger: user requested actual upstream-informed implementation work rather than further UI convenience features or theoretical reports.

## Grounded observation

The existing product's `src/p2-existing-mkv-writer-router.js` sequentially prepares one of four bounded attachment FileData writers: same-size, adjacent Void, tail resize, nonterminal SeekHead relay. Preparation exceptions that did not match one partial regex of known fatal words were treated as route-capability refusals and permitted fallback. That default could mask an unexpected, unrecognized EBML parser or source-consistency error as an ordinary unsupported geometry case. The observed code flaw is definite; **there is no reported real-file exploit or independently demonstrated silent corruption from that flaw**.

## Tentative reusable rule

For a system with several alternative writers/parsers/execution backends, only **explicitly recognized capability-inapplicability** may authorize trying another backend. Unknown or inconsistent error results must terminate fail-closed rather than be retroactively reclassified as "unsupported geometry". A positive allowlist tied to exact backend failure semantics is safer than an unbounded fallback plus a partial blacklist of generic error keywords.

Do not conflate (a) the writer cannot handle this layout with (b) source facts are contradictory, reference indexes stale, UIDs non-unique, CRC invalid, or parser returned an unexpected error. Reclassification must be covered by negative tests and output readback. This is a **routing safety gate**, not a replacement for mature generalized Matroska editing or an assertion of full preservation.

## Submitted product change and tests

- One private per-route explicit list of expected inapplicability codes; unknown parser/CRC/index/scope errors raise `P2_ROUTE_FATAL_<code>` and retain cause.
- Existing four proven positive routes remain structurally unchanged, no new writer, no new UI, no additional media mutation.
- Unit tests assert recognized geometry fallbacks versus unknown/error-state refusal; existing positive writer fixtures and linked-Tag/unknown-top/invalid-SeekHead negatives remain in test suite.
- Draft PR #236 and exact-head Chromium/native acceptance remain the product source of truth. At entry creation, Browser E2E workflow `41698538275` was still **in progress**; do not claim accepted until observed success.

## Mature-tool context, not copy claim

MKVToolNix 102.0 upstream-source archive exposes `kax_analyzer_c::update_element_result_e` and distinct fast/full parse modes; its `propedit.cpp` selects and validates element updates. 103.0 official manual documents `mkvpropedit` fast/full modes and attachment selection by UID. This supports treating backend errors/selector identity as distinct states. **No MKVToolNix source was copied or integrated**. Full source migration is open and separate from this hardening.
- https://fossies.org/dox/mkvtoolnix-102.0/common_2kax__analyzer_8h_source.html
- https://fossies.org/dox/mkvtoolnix-102.0/propedit_8cpp_source.html
- https://mkvtoolnix.download/doc/mkvpropedit.html

## Deduplication and boundary

Checked existing:
- `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md` covers source-structure preflight; this candidate covers **cross-backend fallback after a backend preparation error**.
- `inbox/observations/2026-10-12-browser-native-capability-envelope-container-workbench.md` distinguishes backend capacity; does not define error-type control flow.
- `inbox/candidates/2026-10-15-upstream-code-reuse-semantic-contract-license-gate.md` covers upstream reuse and licensing, not fallback admissibility.

Single product code and test family, no independently validated broad recurrence rate. Do not promote to Canonical from this Candidate or overwrite the product's existing signed-off user scope. After CI, check whether recognized-fallback tests are still passing before claiming a successful mitigation.
