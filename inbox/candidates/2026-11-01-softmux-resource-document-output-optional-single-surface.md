# Candidate — Content-first Matroska workbench: optional output, no implicit primary MKV, explicit membership and preview provenance

Date: 2026-11-01
Status: **Candidate / UX-domain hypothesis, user scenarios but no UI or runtime acceptance**
Product: `11576865/MKV-Fast-Muxer`
Owner input: mixed-file and multiple-MKV drag, unused/wrongly imported assets, no-MKV creation, source vs target preview, independent choice among multiple subtitles; the owner explicitly asks whether a “主件 + 待加入” scheme is valid and whether a simpler single surface exists.

## Problem, not a decided UI

The previously proposed “one source MKV as principal + other files as awaiting addition” rule fails with multiple MKVs, unattached or never-used imports, source-only inspection, and no-source Matroska creation. “Every imported file goes into an output draft” also wrongly equates import with inclusion/export. Content-first classification, selected object, composition authority, and eventual export are different axes.

## Candidate model

- **Resource inventory**: all imported external File objects and scanned source-container resources, with stable identity and provenance. Import is observation/access, never a persistent output membership grant.
- **Active document view**: one focused source MKV or an unsaved prospective Matroska composition, selected for inspection without implying any write. Multiple MKVs remain independent, inspectable sources; source focus must not silently assign “primary output”.
- **Optional target plan**: immutable-source, mutable-intent draft made on an explicit composition/export operation or unobtrusively presented as an *unsaved candidate* for file-only creation. No output is required for inspection. The main surface may project either the active source or target without duplicating writable state.
- **Per-target per-object membership**: imported/available, proposed included, deliberately excluded from output, or unsupported/uncertain. “Unused” is not a file error and does not mean removed from the workspace. A source MKV may contribute only selected tracks/attachments. One resource may have different roles across multiple output plans. Distinguish `remove from imported session`, `exclude from this output`, `remove source member from proposed output`, and `delete physical file` (not allowed).
- **Contextual preview**: each ASS file (including unselected alternatives) can be examined separately with its own source identity; selecting a subtitle/track changes preview content, not output membership. A subtitle without video can preview against a neutral/test canvas within supported renderer limits. Preview of source, simulated planned composition, and independently examined real exported output must be labeled distinctly; a composition display does not prove output was generated.
- **Multiple MKVs**: opening each for inspection is the default, no auto-merge, auto-concatenation, or first-MKV-as-master writer authority. If the user requests combination, identify a destination plan and selected object contributions; if many outputs are intended, make separate output plans / a batch matrix. Source-to-output mapping must be explicit when ambiguous.
- **No MKV**: show an empty virtual target document or a candidate newly constructed composition; classify ordinary media into supported tracks and unrelated files into attachments only under a transparent rule. File inclusion is draft and cancelable. A no-track attachments-only output is non-playback Matroska as distinct from an encoded still video.
- **Single-surface proposal (not a 3-workspace mandate)**: a central current-document/target composition tree, contextual selected-object inspector + preview, small collapsible source inventory/unused resources tray and clear action/save area. For existing MKV unedited inspections, no mandatory “create project”/output setup. For target edits, show source vs proposed differences. No input-before-type questionnaire or multi-step mode gate.

## Falsifiable interaction scenarios

1. Drop one existing MKV only, browse internal tracks/font/chapters, close without export. No output plan or file write is forced.
2. Drop MKV A + MKV B. Both inspectable, none implicitly merged or reclassified as “added extras”. After explicit selection, add exactly one subtitle track or attachment from B to target based on A, retaining independent source identities. Reject unverified unsafe writes.
3. Drop MKV + three ASS. Preview each independently; only one selected for output; others remain in source inventory without error indicators. Changes to preview selection must never silently change included subtitle track.
4. Drop MP4+ASS+TTF+PNG. Create a candidate Matroska with known track/attachment roles, preserve original subtitle/font workflow; show output intent separately from source truth.
5. Drop PNG+PDF only; show previewable selected asset and draft non-playback Matroska membership; on explicit export, produce a valid Matroska, then independently extract PNG and PDF and compare hashes.
6. Drop wrong file. `Remove import` releases session reference (if no active dependent operation); `Exclude from output` leaves asset in inventory; removing an original source track from output never changes original source bytes; Undo restores plan intent.
7. Drop 2 MKVs plus episode subtitles; distinguish inspect independently, one combined output, or N separate outputs without prematurely forcing these choices at import time.
8. Source preview vs plan preview vs generated output audit report show unambiguous evidence labels; no fake “final MKV preview” for unrendered composition.

## Dedupe / supporting prior Foundry material

- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` establishes imported identity vs task role and ambiguous source selection; this candidate adds *no mandatory primary*, per-target membership, unused-resource semantics, and optional export.
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` establishes composition-focused presentation and avoidance of duplicate three-panel object views; this candidate explicitly allows *source-only inspection without prospective output* and tests multi-MKV semantics.
- `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md` establishes A/B/C/D as non-peer UI destinations; this candidate formalizes source/document/target relations and evidence labels for multiple subtitles/target preview.
- `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` already separates multi-source single output versus multi-output batch.

These are preexisting **research Candidates**, not approved UI. Product `src/output-composition.js` remains a read-only projection over legacy state as of `main@36f71dc9ae80a4e0b463de51d2f3aa2edae64c02`; neither a general no-video writer nor actual one-surface UX is proven by this entry.

## Next evaluation

Paper/prototype test against all eight scenarios, particularly the four distinct remove/exclude operations and subtitle source/plan preview identity. Then implement a bounded vertical task using current handlers and real Chromium artifacts, measuring mistaken auto-inclusion, accidental source reassignment, navigation/focus loss, and operator understanding. Do not replace existing user-approved scopes or automatically modify Canonical from an untested proposal.

**Pending:** owner selection of view/role semantics; UI implementation, real-device proof and runtime acceptance.
