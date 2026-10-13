# Candidate: Media workbench should present the composed output object, not duplicate input/probe stages

Date: 2026-10-11
Status: **Candidate / product review verified in existing screenshots / new implementation unverified**
Product: `11576865/MKV-Fast-Muxer`
Product design issue: https://github.com/11576865/MKV-Fast-Muxer/issues/75
Related legacy architecture: https://github.com/11576865/MKV-Fast-Muxer/issues/68
Related PR hold: https://github.com/11576865/MKV-Fast-Muxer/pull/74

## Observation grounded in real UI evidence

The user repeatedly rejected explanation-heavy and then card-heavy renditions of the soft-mux interface. The content-first importer and high-coverage browser mux tests were not the problem in themselves. CJK-correct screenshots from PR #74 ([Chromium run 38132508666](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38132508666), artifact 11699228516) showed:

- 1440px: one subtitle appears under `source.mkv`'s nested stream list, again in the central `当前对象` form, and again in the tall right-column planned MKV track list. The main action is present, but the layout portrays three representations as separate stages and keeps a large populated-state dropzone.
- 390px: an import/card tree, selected-object editing form, preview, full output plan and batch disclosure are stretched across many vertical screens. Replacing the scroll with four exclusive file/edit/output/batch tabs does not automatically solve the issue: those tabs partition one output-composition task into separate destinations, creating mode switches for one property edit.
- The later PR #74 mobile projection was not independently visually verified; [latest run 38134061521](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38134061521) had 203/203 Node tests passing, but real Chromium E2E failed a source/inspector geometric ownership assertion. Do not claim a completed redesign.

### A new distinction

**Content-first ingestion is an internal identity/classification contract, not the main interaction model.** The primary user object for a muxing tool is the prospective **output container composition**: which video, audio, subtitle, chapter and font/attachment items will be in the resulting MKV, and what changes are to be applied.

Model source-file provenance and immutable codec/stream identity separately from the *single authoritative* output-track selection and metadata state. Different UI projections may show source provenance or final output order without instantiating independent editable copies of the same track.

This refines the older `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` rather than replacing it: classification-after-import remains correct; presentation-after-import should be composition-first. It also refines `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md`: a visibly named mux button does not compensate for structurally duplicated track views.

## Proposed UX contract (not yet tested)

- **Empty state:** one obvious add-file/folder/drop affordance; **populated state:** collapse the prominent dropzone to a small Add Resources control.
- **Main view:** output track collection with per-row keep/remove/order and recognizable language/title/default/forced state. Source files are an origin label or secondary browser, not a second track editor.
- **Context:** one selected stream inspector, with relevant preview only when previewable ASS/SSA is selected; font or attachments have their own fields when chosen. No always-empty preview for audio and video tasks.
- **Output:** nearby MKV filename, change summary and important compatibility/warning status, with an always-reachable mux action. Show the detailed plan/FFprobe audit on demand, not as a competing repeated full track inventory.
- **Mobile:** track-list navigation plus contextual editor sheet and persistent export command; do not require four top-level tabs for one job. Preserve draft field state and focus/scroll across viewport changes.
- **Batch:** its own task mode and queue, not an extra several-screen disclosure beneath single-job controls. Reuse recognition/executor safety rather than cloning UI state.

## Engineering and evidence boundaries

Retain video/audio `stream copy`, MKV-only output, safe append-only source defaults, content-sniff evidence, unsupported/mismatch diagnostics, renderer-limited on-demand preview, ambiguous batch match refusal, cancellation, output collision checks, and post-mux FFprobe audit. Output-composition rows are a **view projection** from existing owned task/source models, not a second authoritative FFmpeg plan.

Validation must include actual single- and mixed-source MKVs, subtitles/fonts, renamed input, original audio/attachments/chapters, stream ordering/default/forced edits, real mux and post-export audit, plus 320px/390px/900px/1180px/1440px/1600px browser accessibility/overflow/focus/visual evidence. Do not treat source-regex matches or 203/203 Node results as geometric or usability proof.

### Source and competing explanations

Some current failure may be an incorrect CSS breakpoint or an outdated E2E expectation; the observed duplicate presentation problem is independent of which one caused the latest E2E geometry failure. The user has not approved the new proposed design through interaction. This Candidate must not be promoted to Canonical without successful implemented evidence and user acceptance.

Research context (not a mandate to copy): MKVToolNix GUI associates source files, tracks and mux options with project configurations; LosslessCut exposes an accessible Tracks editing entry and export overview. Their interaction constraints differ from browser-local FFmpeg and ASS preview.

No Canonical promotion.


### 2026-10-12 implementation integration checkpoint

Product PR #74 now contains a bounded, **submitted but not yet browser-verified** implementation of the composition-first Candidate:
- A pure projection `src/output-composition.js` (13+ Node safety cases in product CI previously exercised) becomes a visible `#outputCompositionPanel` containing one output-row collection. It derives from the existing scanned stream and edited track state, external subtitle/audio state and selected fonts. IDs are stable; removed tracks remain inspectable and do not count toward output.
- Row selection routes back to the existing source stream inspector, external subtitle/audio metadata controls or font controls, rather than creating new writable state. The populated-state dropzone collapses; the full source/tree/recognition evidence remains in native `#sourceFilesDetails`, which auto-opens for unrecognized input or ambiguous main source. Full mux-plan rows are behind another explicit `<details>`, while important plan warnings remain independently visible.
- Phone source/editor work areas get buttons that call the existing `#muxBtn` and mirror its disabled state. This reduces mandatory source→edit→output tab hopping but is **not yet equivalent to the proposed single-screen contextual editor sheet**, so visual acceptance is open.
- Product source and browser assertions were added for output projection, external audio/subtitle navigation, original inspector identity and secondary-source disclosures. The exact-head CI and new CJK screenshots are **Pending**, so no claim of UI acceptance or shipped behavior follows.

Observed prior product CI failure: a desktop test measured `#assetInspectorHost` while the editor was hidden before selecting an output object (zero rectangle); the assertion has been moved after explicit selection. This only resolves an outdated test precondition; it does not prove actual geometry until the new browser run succeeds.

This adds implementation evidence under the existing Candidate and **does not change Canonical**.


## Round 4/5 container-source observations and actual-output audit inspector (2026-10-13; Pending exact-head CI)

Product [PR #107](https://github.com/11576865/MKV-Fast-Muxer/pull/107), branch `feat/round4-container-evidence-and-audit-workspace`.

The primary composition surface now receives a **source-scoped, read-only** projection of ffprobe flat chapters, global tags and other/data streams. It does not add these as editable target tracks or assert preservation of unobserved EBML/UID links. An output-evidence inspector renders data from the actual generated MKV's JSON report: SHA-256, ffprobe audit status/issues, real output name and counts, and a source/plan freshness check. It distinguishes generated output from persisted output and explicitly disclaims unknown EBML/UID preservation. The read-only status is deliberately separate from `ContainerDocument`'s editable target collection.

Unit tests and an existing real-browser E2E were extended to check source evidence and compare the workbench's displayed SHA-256 with a downloaded report. At this Intake, exact-head browser CI is **Pending**, so acceptance is not asserted.

The testable reusable insight is a claim-boundary split: source observations, planned mutations, measured output, independent audit and persistence are different evidence states. This refines this Candidate and is **not** a new Canonical norm.


## Round 4/5 exact-head evidence and merge (2026-10-13)

Product [PR #107](https://github.com/11576865/MKV-Fast-Muxer/pull/107), tested head `beec8e5339915a2240db15c6e79308381316bcb7`, merged `main@7fcf01841ff7d5169db48019db0ec762d63a4c7b`. [Node/build workflow 38340867580](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38340867580) **success**; [full Chromium E2E workflow 38340867583](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38340867583) **success**. E2E asserts actual ffprobe-observed chapter/tag source rows and hashes from the generated MKV report displayed in the UI; this is not physical-device acceptance or blanket EBML retention evidence.

Product evidence remains a read-only source observation projection and actual artifact audit status. Draft freshness is based on the source key + currently displayed `buildMuxPlan` projection equality, *not* a cryptographic source identity or universal execution-proof revision. No Canonical promotion.
