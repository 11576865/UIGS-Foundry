# Observation — Editable SVG handoff after Figma design-write/upload blockers
Date: 2026-10-14
Status: Observation / local artifact verified; Figma canvas sync **PENDING USER IMPORT**
Product: ASS-Workbench-Android R2 concept UI (NOT Native APK)
Tool chain: Inkscape-generated SVG -> Figma upload_assets intake -> container curl / Figma Plugin API
## Observation
The existing three R2 SVGs (main workbench, per-field origin detail, write review) were present as local source files with vector UI elements and a single embedded raster media reference each. Figma `upload_assets` returned single-use submission URLs but server-side canvas import only occurs after a separate POST to those URLs. Current container POST attempts failed DNS resolution for mcp.figma.com. One read-only `use_figma` call confirmed the previously created Figma design file was empty (page children = 0); a subsequent plugin call hit Starter MCP tool-call limit. Do not represent returned upload URLs or a new blank Figma file as successful design import.

A local recovery build sanitized invalid XML 1.0 control bytes (two in the `origin_detail` SVG), retained named groups and embedded raster references, and created a standalone import package with three SVGs and concise instructions. Each SVG passed strict lxml XML parsing and Inkscape PNG rendering. This proves valid local SVG and import handoff, **not** successful Figma-layer reconstruction or correct text editability after Figma import.

## Reusable intake insight
A design-tool connector's preflight upload URL is not its commit receipt. Preserve exact failure stage and a Pending state; if external upload/post cannot execute or the API is rate-limited, provide a self-contained vector artifact with import instructions and mark the hosted canvas as unsynced. Validate local XML and raster rendering before handoff; do not claim native component editability or pixel-perfect fidelity in the destination design tool until checked there.
## Dedupe / epistemic scope
Foundry searches for 'Figma upload editable SVG external agent quota fallback', 'SVG XML invalid control character Figma import', and 'design tool unavailable use self-contained editable vector artifact pending sync' produced no exact record. This is a single Observational workflow case, not evidence for Canonical.
## Next action
When Figma MCP quotas or upload networking are available, import the validated SVGs to the existing design file https://www.figma.com/design/2EitAXVEgfIQtxr4KrkYRN and verify layer visibility, text and image preservation. Until then: **Pending User Import**.