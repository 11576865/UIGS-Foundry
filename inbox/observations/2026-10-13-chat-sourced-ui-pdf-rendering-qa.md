# Observation: Chat-sourced UI PDF requires render-level artifact verification

Date: 2026-10-13
Status: Observation; confirmed production-artifact defect and local correction; not a UIGS Canonical rule
Context: a 27-page chat-sourced product-design PDF for MKV-Fast-Muxer, generated as HTML/WeasyPrint, with landscape desktop/tablet mockup plates and embedded SVG icon grammar.

## Actual defects discovered on visual review

1. In the batch queue mockup, dynamic values such as `EP{i+1:02}.mkv`, `{1 if i...}`, and `{badge(...)}` were visibly printed instead of example job values. Root cause: part of a Python-generated row template became a plain string after concatenation, so only the first fragment was an f-string and subsequent braces were left literal. The original PDF compiled and text flowed inside page bounds; machine checks would not detect the semantic display defect.
2. In the icon grammar figure, icon tiles rendered without glyphs. The SVG paths and shapes existed in generated HTML, but stroke color was provided only via CSS inheritance (`stroke:currentColor`), which the chosen HTML→PDF rendering pipeline did not display as expected. Explicit SVG `stroke` attributes corrected the PDF.
3. An early icon proposal reused a question-mark circle for both 'unknown' and 'help', contradicting the project's own icon-semantics contract. A distinct dash-circle unknown shape resolved the mockup inconsistency.

All three were corrected in the final generated PDF. After regeneration, PDF text extraction confirmed interpolated EP01–EP07 names and no raw template placeholders; rendered pages showed actual icon glyphs. The 27-page final PDF had no extracted text bounding boxes outside page coordinates. This confirms these specific issues were fixed, not that all UI/visual aspects have passed user acceptance.

## Reusable engineering lesson

- Trace source attribution separately from implementation claims. A report that derives from a conversation may quote earlier assistant claims, but it must not promote those claims into current repository/standard evidence without a separate live verification step.
- Validate rendered figures visually, not merely successful PDF generation, file size or text extraction.
- Check for raw generation tokens, unresolved curly-brace templates, icon loss, CJK font fallback, long-line wrapping and page clipping.
- Require a representative set of rendered pages that includes each visual archetype (dense task matrix, icon legend, light settings, dark workspace, help panel, responsive comparison).
- Semantic consistency is part of rendering QA: 'unknown' status must not use the same icon as the help trigger even if the code renders it perfectly.
- The final artifact can be ready only after recomposing the HTML, regenerating the PDF and re-inspecting corrected pages.

## Evidence limits

This observation is about an artifact-generation workflow, not the actual released MKV-Fast-Muxer UI. The finished PDF contains design proposals and cannot stand in for an interactive browser test. No Canonical promotion or default design-policy mutation is proposed.

Related existing Foundry records: `inbox/candidates/2026-10-02-automated-production-visual-evidence.md`, `inbox/observations/2026-10-11-browser-ui-screenshot-cjk-font-coverage.md`, `inbox/candidates/2026-10-12-single-source-contextual-help-and-settings-scopes.md`.
