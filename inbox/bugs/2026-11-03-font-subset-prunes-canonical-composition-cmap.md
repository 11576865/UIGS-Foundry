# Bug · font subset prunes canonical composition candidates after character deduplication

Date: 2026-11-03
Status: **Product fix locally verified; exact-head full CI pending; no Canonical change**
Product: `11576865/MKV-Fast-Muxer`, development0.1047.0
Durable product implementation/evidence: `fd637f6f53055bf56f3ba7e4fb9270f7b18cb264` ([PR #227](https://github.com/11576865/MKV-Fast-Muxer/pull/227)), branch `test/softmux-s03-collections-shaping-20261103`.

## Deduplication and scope

Bounded searches for `font subset normalization` and `subset whitespace` found no same-mechanism record. Existing structural font identity/format support candidates concern classifying a real font, not retaining canonical cmap candidates during subsetting. This Bug records one actually reproduced shaping defect and its tested repair; it does not establish a universal font-normalization rule or promote Canonical.

## Actual failure

A genuine uniquely named CFF OpenType font, derived from installed DejaVu outlines with genuine GDEF/GSUB/GPOS, was subset by the actual browser pipeline and attached to a real MKV. Container, exact delivered font payload and authored ASS event checks passed. Independent native HarfBuzz shaped `a`+U+0301 in the original font through precomposed U+00E1, while the subset had pruned that cmap candidate: the sample `á AV` changed from4glyphs to5 with a separate zero-advance mark. Native libass output differed by89pixels in the accent region; Latin ligature and Arabic metrics already matched, so retaining layout tables alone was insufficient.

An unrelated first-fixture `AngleStyle` typo caused style-audit unavailability and was corrected before GREEN; no product failure is inferred from that harness error. The canonical defect is independently bound to native font shaping/cmap behavior and preserved in product `docs/evidence/s03-canonical-subset-red-20261103.json`.

## Mechanism and bounded repair

The repertoire was deduplicated into code points before the subsetter was invoked, losing authored sequence information needed to retain canonical composition candidates. `analyzeAssFontUsage` now expands canonical decompositions and intermediate composition candidates within actual graphemes before deduplication; non-text override boundaries do not hide candidates. A cached composition table is derived once from the runtime Unicode normalizer over a fixed scalar range, avoiding quadratic growing-prefix normalization. Raw authored ASS/diagnostic characters remain unchanged, drawing/Comment content is excluded, and compatibility normalization NFKC/NFKD is deliberately not used. The shared analysis serves both single and frozen-batch subsetting.

## Verification

- Two focused tests were RED before repair;7focused tests GREEN after the review correction, including canonical decomposition, dedup ordering, non-text override boundaries and compatibility/drawing/comment exclusions.
- Four actual Chromium/Wasm outputs passed independent extraction/fontTools/systemHarfBuzz/libass checks: TTC two-face passthrough, actual CFF OTC two-face passthrough, standalone OTF subset, frozen-batch OTF subset.
- Both collections retain complete original SHA and real Regular/Bold selected PostScript identities; subset requests honestly return `font-collection` passthrough.
-30native shaping vectors retain clusters/advances/offsets; full/reference and extracted final pixels equal; missing Bold, deleted layout tables, wrong text and blank controls differ.
-859Node tests/build passed. Correct isolated four-mode PASS receipt: product `docs/evidence/s03-collections-shaping-green-20261103.json`.

Preview proof is actual PNG availability, not claimed preview face/pixel equivalence (external preview uses error log level). Final artifact face identity/rendering is independently checked. This does not prove arbitrary fonts/scripts, physical devices, all players, general collection subsetting or formal S03 acceptance. Product CI and subsequent integration remain separate lifecycle states.


## Independent review correction: endpoint normalization was insufficient

The earlier `9e4fec9` proposal retained final NFC and NFD endpoints only. Independent review used the actual hb-subset-wasm and native HarfBuzz to show that `a`+U+0302+U+0301 still requires intermediate `â` before reaching `ấ`: the endpoint-only subset produced3glyphs instead of1, with two separately positioned marks, despite no `.notdef`. An override/style run ending after circumflex also lost its1glyph composition. This undercuts the earlier endpoint-only repair, not merely its test count.

One bounded fix pass added two failing regressions for intermediate/multi-stage marks, overrides, Hangul intermediates and grapheme separation. The corrected implementation conservatively retains canonical candidates whose decomposition components occur inside the same actual grapheme; compatibility forms remain excluded. All7focused tests,859full tests/build and four actual browser/native outputs passed. The expanded30native vectors include the multi-stage example and a non-composing intervening mark; source/reference and extracted final pixels match, negative controls differ. A fixed runtime Unicode scan was50ms in the observed local Node environment (not a tablet performance promise). Exact-head fullCI for PR227 remains pending; no Canonical or formal/device acceptance promotion.
