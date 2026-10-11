# Case: Render an existing MKV's ASS subtitle using only retained in-container resources

Date: 2026-10-12
Status: Case / proposed acceptance contract / not implemented in MKV-Fast-Muxer
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
