# Candidate: Orthogonal product dimensions should not become competing navigation destinations

Date: 2026-10-12
Status: Candidate / user design-review insight plus cross-project architectural hypothesis; not an implemented or validated UI
Primary product: `11576865/MKV-Fast-Muxer`
Related domains: ASS authoring, professional media workspaces, object-centered interfaces
Related prior records:
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`
- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md`
- `inbox/candidates/2026-10-03-adaptive-layout-semantic-context-reentry.md`
- `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`

## New distinction from design discussion

Four plausible product directions were initially classified as peer modules:

A: ASS/font subtitle delivery;
B: Matroska container composition;
C: output correctness and compatibility verification;
D: source-container inspection/extraction.

The user noted that they are compatible but conceptually different in *every* respect. Analysis yields a narrower, falsifiable candidate:

- B is **domain object and edit authority** (one composed Matroska document).
- D is **observation capability** (source/inventory/provenance).
- C is **cross-cutting evidence and assurance**, applied before and after edits.
- A is **task-specific workflow/recipe** assembled from B/D/C; not a separate backing document or exclusive top-level app section.

Rendering these dimensions as four exclusive pages or independent mutable models forces unnecessary context switches and duplicate source/track representations. A UI should instead bind an active resource identity to relevant inspection, modification, and verification commands, while recipes provide guided entry without spawning a second state authority.

## Suggested representation contract

- One authoritative container composition; one selected semantic resource; one modification log.
- Persistent composed-object navigation on desktop-size layouts, secondary source provenance, contextual inspector, and continuous compact verification status.
- Select item -> context actions and information without navigating A/B/C/D as destinations.
- Allow focused mobile/narrow-screen re-projections without serially stacking every workspace pane into an indefinitely scrolling document.
- Treat viewport presentation (desktop/tablet/narrow) and execution capability (browser/Wasm/native) as independent axes. A narrow viewport must not be mistaken for missing codec support or vice versa.
- For very narrow viewports, preserve core inspection and task access; complex editing may use an explicit focused inspector. Zoom is not a substitute for providing a readable and keyboard/touch-accessible fallback.
- Avoid describing all this as proven UX quality without actual 1440/1280/1024/768/390 widths, zoom, focus and screen-reader acceptance. W3C WCAG Understanding SC 1.4.10 allows focused two-dimensional interfaces such as data tables and toolbars to retain necessary spatial relationships while reflowing surrounding content. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html

## Source observations and evidence boundaries

- Product `src/output-composition.js` at main `7781a4f410a9c6edb9a1f3d056091e6ace333cc4` is already a display projection over legacy tracked state, not a general container authority.
- Existing Foundry composition-first Candidate documented three duplicated visible representations, long phone vertical stacks and non-accepted four-tab navigation.
- User's current review explicitly rejects long scrolling, excessive prose, vague iconography/colour, oversized actions, and degraded narrow-screen stacking.
- Matroska official format spec distinguishes tracks/attachments/chapters/tags and font attachments, so these must not be flattened into a single undifferentiated file list. https://www.rfc-editor.org/rfc/rfc9559

This records a proposed *cross-project classification and layout principle*, not visual validation, Canonical status, or a completed product direction. The user has not approved any implementation from this discussion.
