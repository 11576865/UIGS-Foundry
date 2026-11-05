# Case: Render an existing MKV's ASS subtitle using only retained in-container resources

Date: 2026-10-12
Status: Case / partially implemented and scoped real-output evidence verified; broader proposed matrix remains incomplete
Product: `11576865/MKV-Fast-Muxer`
Evidence base: main merge commit `7781a4f410a9c6edb9a1f3d056091e6ace333cc4`
Related UIGS records:
- `inbox/candidates/2026-10-02-shared-libass-not-identical-player-output.md`
- `inbox/candidates/2026-10-04-container-compatibility-detection-wraps-mutations.md`
- `inbox/candidates/2026-10-04-container-attachment-mutation-type-agnostic.md`
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`

## Source-backed gap

The product's `src/main.js` `syncPreviewControls()` and `refreshSubtitlePreview()` select subtitles from `selectedSubtitleTracks()`, which resolves newly imported subtitle files. The preview loads `selectedFonts()` from the external font input into a `fontsdir`. It extracts a video frame from the chosen source, then composites the external ASS/SSA with libass. It does not extract and select an existing ASS/SSA track plus original font attachments from the input MKV, and it does not enforce an isolated font environment containing only the resources planned for the output. Therefore this preview is evidence about an external subtitle-plus-font setup, not a self-contained verification of a source or proposed output MKV.

The source scan does enumerate source subtitle/attachment streams, but `buildContainerTreeModel` is a projection of scan state, not a rendered-resource dependency closure. This is a bounded capability gap, not proof that the existing preview path is broken.

## Proposed test/acceptance

1. Prepare a deterministic source MKV containing video, an internal ASS subtitle track, and attached TTF or OTC font resources. Do not supply an external ASS or font file.
2. Select the source MKV, scan it, pick its internal ASS track and request a preview. The test should extract the selected subtitle and resolve the proposed output's retained font attachments, then render via libass with system/external font fallback explicitly disabled or accounted for and reported.
3. Provide positive frames for normal style, inline `\\fn`, weight/italic, `\\r` reset, `\\t` transitions, and non-Latin glyphs. Record provenance for every font face actually used.
4. Negative variant: remove the only required font attachment in the planned output; verify that the user sees a dependency failure or explicit fallback, not an unqualified 'renders correctly' result.
5. Negative variant: source internal ASS is removed or replaced; the preview must use the actual prospective output selection, not stale source state or a silently retained external input.
6. Export the MKV, re-open the output file in an isolated renderer, verify actual subtitle/font attachment identities and compare representative frames. Keep `writer compatibility`, `libass render correctness` and `target player appearance` as separate evidence categories.
7. Neither previewing nor cancellation changes the source. The final output's attachment/subtitle inventory and unchanged streams are audited independently.

## Engineering principle under test

A self-contained render check must close its dependency set over the *proposed output container*, not a convenient global resource directory. A preview's visual success cannot establish that a self-contained artifact will render without the fonts accidentally available on the tester's OS or loaded as external project inputs.

## Evidence level and limits

Source inspection of exact main code, and a proposed test case. No isolated actual MKV acceptance run was performed for this case. Do not claim runtime reproduction or mark implemented. No Canonical promotion.


## 2026-11-05: S03 bounded real Chromium/native render evidence — earlier implementation gap narrowed

**Intake/dedup:** Update this existing Case because its original `not implemented` scope is now stale. Do not reinterpret the original proposed seven-part full contract as automatically approved or fully satisfied. Related font subset grapheme/cmap defect is already tracked and closed separately in `inbox/bugs/2026-11-03-font-subset-prunes-canonical-composition-cmap.md`; no duplicate Bug or Canonical record created.

**Exact actual evidence:** [Softmux full Browser E2E #41973241938](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41973241938), source code head `a38696a61822f67a55f2a0ebf7cce1cc77f6b9d7`, completed **SUCCESS**. Its dedicated S03 collection/CFF native-shaping job, units/build, and actual Chromium browser suite succeeded and uploaded six independently inspected archives:
- `13391185006`: four actual MKV outputs with two-face TTC/OTC (byte-preserved, no unauthorized collection subsetting) and CFF OTF single/batch subsets. Deterministic original and subset render PNG pixel equality with independent native libass reference; changed-font negative PNGs are distinct. Native font-face and HarfBuzz shaping vectors (including Arabic, ligature and multistage combining accents) were checked. **Source archive itself marks `previewFaceIdentityVerified:false`**: it does NOT prove exactly which face the browser preview used.
- `13390504606`: real `preserve` / `subset` / `force` font strategies and an intentional missing-dependency warning case. Native outputs and extracted font SHA-256 match receipts. Positive PNG pixel equivalence holds; negative case records two warnings and `pixelEquivalenceVerified:false` rather than suppressing a failure.
- `13390459389` and `13390952838`: independent libass actual final ASS+font one-frame proof and four distinct fractional-time dynamic ASS samples. Source vs demuxed-final exact-pixel checks pass; direct-MKV frames are high but not exact-SSIM matches. Altered/blank image controls distinguish false positives.
- `13391310491` and `13391365035`: true input MKV embedded ASS+font inspection/preview and another MKV using selected source ASS+font, with actual output source-byte identity/provenance in tested run and independently inspected final frame + attachment evidence.

**Independent reviewer work:** Downloaded all 6 ZIPs, locally recalculated SHA-256 for every included mode's final MKV, delivered standalone font where packaged, and documented PNGs; `ffprobe` opened each supplied actual MKV and identified expected video/audio/ASS/attachment types. Positive image comparisons were pixel-exact; negative images differ. No original source fonts/video for every mode were included to permit a second external input rehash. Reinspection receipt SHA-256: `3dac8e39130502fdae74d85e70ec3ec1c33fcf1227a44b5b3ae282037b4d3368`.

**Release ledger:** Docs-only [PR #247](https://github.com/11576865/MKV-Fast-Muxer/pull/247) merged to `main@74d2cbdda77f77aa127a3b7ac50ca58fc109bc2e`, records this S03 `SCOPED_PASS_NOT_1_0_ACCEPTANCE`, artifact IDs, exact tested code head and **unresolved preview font-face provenance** in existing `docs/softmux-1.0-release-evidence.json`. Formal `status:UNASSESSED`, release candidate null, contract owner approval pending. No product feature code was modified by the documentation reconciliation.

**Unmet/unknown relative to the original Case:** There is no independent browser preview exact-face proof for each TTC/OTC face; the original matrix's every `\\fn`, `\\r`, `\\t`, source track removal/fallback, arbitrary glyph/style/font, real physical devices and cross-player requirement have not been certified as a whole. These are *bounded evidence/scope gaps*, not observed new product defects. Continue to distinguish independent native result rendering, browser preview, and actual target player behavior; do not promote Case to Canonical.
