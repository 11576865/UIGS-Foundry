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


## 2026-11-01 follow-up: resolve "主件 + 资源库" combinatorial complexity through virtual per-target references

New owner design scenario: all imported inputs go into “资源库”, an MKV may be the open main document or—if no MKV—an automatic proposed output; when A/B/C/D.mkv are present, user may copy selected nested objects of A into the intended outputs based on B, C and D. Owner explicitly questioned where A’s object should live, whether to pre-extract it, whether move should erase A, whether B’s edited copy is another resource, and how to avoid combinatorial interaction complexity. The owner rejects video concatenation as an invented task outside intended scope.

### Refined candidate (owner has not approved)

**UI:** one active document surface with a source/library browser and context inspector. “主件” is reframed as **current open document / virtual output composition**, not a privileged physical original. Model C’s provenance, object membership and optional output underpin model A’s simple UI; they need not appear as three separate pages.

**Data semantics:**
- Keep exactly one imported source identity per original File and its scanned nested items. Do not implicitly extract or reify a Matroska member as a separate uploaded file merely to make it selectable.
- A nested member is referenced by a stable tuple of **source File identity + source container object/track identity + any necessary byte/time/format constraints**. A target draft can hold a *reference intent* to this object, not a duplicated payload. The same source object can be selected for several target documents independently; output bytes are written only at explicit execution.
- Opening B without modifications shows *actual source* B. Editing it produces an in-memory B* plan, displaying inherited B objects plus any selected external sources; the original B File remains unchanged. B* is not a new imported file; after explicit export it creates a distinct MKV artifact (unless a separately approved replacement operation is designed). The exported result does not silently become an input source; importing or using it again requires explicit user action.
- Multiple possible targets can retain separate per-target unsaved plans. One target is active at a time. Selecting/viewing A's member should not silently change B* output membership or create a target plan.
- **No “move” required initially**. Moving bytes/objects between real MKV sources would imply writing two files; present addition to one target and exclusion from another as distinct non-destructive operations, and preserve original file(s).
- **No MKV input**: show an unsaved virtual new Matroska with proposed recognizable contents, each inclusion editable before output; preview is of recognized input or planned composition, not generated final container. No export remains normal.
- **One MKV**: auto-open it for inspection, no output unless changes/export. **Multiple MKVs**: library selection determines which source is opened; importing does not auto-merge. For a cross-source add operation, default destination is currently active B* where unambiguous, otherwise ask to choose explicit target *at the action*.
- Wrongly imported file: removing it from session should not delete disk data; if referenced in any drafts, show dependent target(s) and require a safe decision. Removing a member from B* only edits the plan.
- Subtitle preview: select any standalone or embedded subtitle from source browser and preview independently of inclusion; preview selection never silently toggles output membership.
- Support restriction: referencing an A media track in B* does not prove a legal/common-timebase writer path; unsupported cross-container stream operations must be blocked or labeled unavailable. Attachments-only export remains a separately bounded writer capability.

### Acceptance thought experiments

1. A/B/C/D imported. Open B → no outputs. Choose A nested attachment → Add to current B* → inspect source A unchanged, source B unchanged, B* displays only a *pending* addition, no duplicate extracted A file.
2. Use the same A attachment in C* and D* without spawning duplicated source rows; independently export B*, C*, D* to distinct physical artifacts.
3. Deselect A object from B*, leave it in C*: only B* plan updates; A original and C* untouched.
4. Wrong-file removal with 2 active draft references produces a dependency-aware action (cancel/remove dependent intents); no implicit disk deletion.
5. Switch B* → inspect A → return B*: preserve B* drafts and selection; no automatic inclusion from preview click.
6. Without input MKV, show a provisional draft container from PNG/PDF and only create actual Matroska on explicit export.
7. Cross-container video concat is excluded from these tests: owner explicitly says it is not an expected function.

Deduped against this Candidate's earlier optional-output + per-target membership model, and `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`. This is a refinement, not a second product identity or a Canonical rule. No implementation/UI tests performed; owner-facing interaction and technical cross-container writer envelope remain **Pending validation**.
