# Bug · font subset prunes canonical composition candidates after character deduplication

Date: 2026-11-03
Status: **Product fix locally verified; exact-head full CI pending; no Canonical change**
Product: `11576865/MKV-Fast-Muxer`, development0.1047.0
Durable product implementation/evidence: `9e4fec9fa5060f052807c0f629c109e770d1b5cf`, branch `test/softmux-s03-collections-shaping-20261103`.

## Deduplication and scope

Bounded searches for `font subset normalization` and `subset whitespace` found no same-mechanism record. Existing structural font identity/format support candidates concern classifying a real font, not retaining canonical cmap candidates during subsetting. This Bug records one actually reproduced shaping defect and its tested repair; it does not establish a universal font-normalization rule or promote Canonical.

## Actual failure

A genuine uniquely named CFF OpenType font, derived from installed DejaVu outlines with genuine GDEF/GSUB/GPOS, was subset by the actual browser pipeline and attached to a real MKV. Container, exact delivered font payload and authored ASS event checks passed. Independent native HarfBuzz shaped `a`+U+0301 in the original font through precomposed U+00E1, while the subset had pruned that cmap candidate: the sample `á AV` changed from4glyphs to5 with a separate zero-advance mark. Native libass output differed by89pixels in the accent region; Latin ligature and Arabic metrics already matched, so retaining layout tables alone was insufficient.

An unrelated first-fixture `AngleStyle` typo caused style-audit unavailability and was corrected before GREEN; no product failure is inferred from that harness error. The canonical defect is independently bound to native font shaping/cmap behavior and preserved in product `docs/evidence/s03-canonical-subset-red-20261103.json`.

## Mechanism and bounded repair

The repertoire was deduplicated into code points before the subsetter was invoked, losing authored sequence information needed to retain canonical composition candidates. `analyzeAssFontUsage` now unions NFC and NFD code points from visible dialogue before deduplication; non-text override boundaries do not hide candidates. Raw authored ASS/diagnostic characters remain unchanged, drawing/Comment content is excluded, and compatibility normalization NFKC/NFKD is deliberately not used. The shared analysis serves both single and frozen-batch subsetting.

## Verification

- Two focused tests were RED before repair;5focused tests GREEN afterward, including canonical decomposition, dedup ordering, non-text override boundaries and compatibility/drawing/comment exclusions.
- Four actual Chromium/Wasm outputs passed independent extraction/fontTools/systemHarfBuzz/libass checks: TTC two-face passthrough, actual CFF OTC two-face passthrough, standalone OTF subset, frozen-batch OTF subset.
- Both collections retain complete original SHA and real Regular/Bold selected PostScript identities; subset requests honestly return `font-collection` passthrough.
-18native shaping vectors retain clusters/advances/offsets; full/reference and extracted final pixels equal; missing Bold, deleted layout tables, wrong text and blank controls differ.
-857Node tests/build passed. Correct isolated four-mode PASS receipt: product `docs/evidence/s03-collections-shaping-green-20261103.json`.

Preview proof is actual PNG availability, not claimed preview face/pixel equivalence (external preview uses error log level). Final artifact face identity/rendering is independently checked. This does not prove arbitrary fonts/scripts, physical devices, all players, general collection subsetting or formal S03 acceptance. Product CI and subsequent integration remain separate lifecycle states.
