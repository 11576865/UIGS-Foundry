# Candidate: Separate imported asset identity from its task role in content-first media workbenches

Status: **Candidate / implementation under Draft PR CI**  
Date: 2026-10-10  
Domains: information architecture, media ingest, UX-dataflow contracts, source selection, container/track navigation

## Observation

Product: `11576865/MKV-Fast-Muxer`  
User direction: The initial UI refresh only changed icon labels but retained four separate **Video / Subtitle / Font / Audio** upload gates. The user rejected that architecture: a workbench capable of recognizing multiple actual input content types must not require users to choose a type before importing. The earlier UI-only Draft PR #67 was closed without merge.

The existing code uses distinct DOM File inputs (`videoInput`, `subInput`, `fontInput`, `audioInput`) with real change handlers for mux execution, subtitle/family inspection and source MKV track scanning. These represent **execution roles**, but the visible UI was using them as **ingress categories**. A new content-first intake can unify import without assuming that content identity alone defines source/append roles.

## Proposed principle

**Asset identity is discovered; role is assigned.** Keep them distinct:
- One import surface for files, folder selection or file drag/drop; preserve an auditable inventory of *every* input, including unrecognized bytes.
- First classify by inspected content/signature, not filename extension or MIME claim. Distinguish recognized headers from internal stream evidence; a recognized MP4 `ftyp` or Matroska EBML header does not establish a video stream.
- Choose the primary video-bearing container explicitly if more than one is present. A single candidate can be tentatively selected, but `ffprobe` still validates actual streams before the video mux path accepts it.
- Standalone recognized subtitle/font/audio assets may be mapped to existing role adapters; classify undecidable inputs as `UNSUPPORTED` or `UNVERIFIED`, not silently dropped.
- Source-container tracks, attachments, chapters and metadata belong conceptually *under the container object*, not as four separate files to upload.
- Keep user-edited metadata and audit paths owned by stable domain objects, not input-widget lifetimes.
- The UI affordance change alone is insufficient: replace the implicit source+added-subtitle precondition so a source-only MKV remux can be represented, while maintaining actual video-stream verification.

## Engineering proposal and current evidence

Issue: https://github.com/11576865/MKV-Fast-Muxer/issues/68  
Draft PR: https://github.com/11576865/MKV-Fast-Muxer/pull/69  
Initial head: `896019e97fca2b8a87d7fc52cde749ed69156850`

PR #69 adds `src/asset-intake.js` (bounded content-signature classifier and explicit source-role resolution), a unified resource inventory in `index.html`, and `src/main.js` wiring through the existing input-event adapters. It preserves the existing source-MKV scan and post-mux audit. The classifier's role claims are explicitly weaker than mux/codec support claims. A single-source-only MKV remux path is enabled without mandatory new subtitles.

Local source-derived V8 results: **8/8** classification/role checks and **6/6** UI source checks passed; full Node CI, Chromium E2E, actual viewport screenshots and manual UX acceptance **not yet proven**. New browser scenarios exercise mixed-content import with real mux, unsupported asset gating/removal, multiple-container ambiguity and source-only MKV remux. PR is Draft; do not claim production deployment or tested visual appearance.

## Deduplication and evidence boundaries

Foundry search for `content-first intake`, `unified asset inventory`, `role after classification`, `import slot category` found no identical intake/role UX case. Existing `2026-10-05-media-import-capability-stages-must-not-collapse.md` already distinguishes parseability, decoding, stream-copy and execution readiness. The new candidate specifically addresses **user-facing import categories vs post-recognition task roles**, a separate information-architecture boundary. `2026-10-02-media-format-support-is-a-compatibility-relation.md` covers compatibility evidence, not the import-gate UX constraint.

The new importer is deliberately incomplete: signatures are bounded, file identity is not equivalent to complete byte hashing, and the internal legacy role input adapters remain. Do not infer arbitrary format support or guarantee that all media containers can serve every role. Keep Candidate-only; no Canonical update based on one draft implementation.


## Verified PR #69 CI evidence

Source PR head: `896019e97fca2b8a87d7fc52cde749ed69156850` (Draft / not merged).  
GitHub Pages **build succeeded**; Chromium Browser E2E workflow `37982837913` **completed successfully**, running the full **163/163 Node tests** (0 failures) followed by real Chromium scenarios. The job log explicitly contains `Unified content-first intake mux PASS` and `Source ambiguity and MKV-only remux PASS`. Review threads and reviews were empty at verification; PR remains Draft and `main` remains at `d5669c6d9bb6ebdd6843ee8c7f651902c80c4d08`.

This upgrades the evidence from source-derived checks to a **green real browser execution/mux audit** of the first intake slice. It does **not** establish completed real-user visual acceptance, fully general codec/container support, audio-only MP4 classification, or source-container track tree presentation in the import list. Do not treat the green CI as a license to declare the whole issue solved or to promote the Candidate to Canonical.


## Phase 2 — live MKV source-container tree and verified CI

Implementation head: `0e16632d422dd2ea6550f6bce558cbe7df766910`, Draft PR #69. The imported MKV source row now expands after the real source scan into nested sections for source video/audio/subtitle/data streams, attachments, chapters and selected global metadata. The editable audio/subtitle track and attachment inputs write **the same trackState objects** already used by the original MKV editor, with no duplicated independent data model. Import inventory remains the entry point; unverified non-source containers receive no imaginary track tree.

Evidence: source projection unit checks **5/5 passed**; latest GitHub Actions Node suite **168/168 passed**; Chromium run `37984257203` **succeeded**, including actual MKV artifact probes after in-tree audio keep/remove, title, Forced changes and original attachment rename/remove, plus Chapters retention. The browser also validated post-export task state preservation and mobile 390px tree visibility after viewport reflow. Pages build succeeded.

The initial E2E attempt `37983860309` failed after export because legacy mux success cleared hidden file adapters and `trackState` while the persistent imported-asset inventory remained visible. This was a real cross-lifecycle defect, not a mere responsive test flake; root cause/fix recorded separately in `inbox/bugs/2026-10-10-mkv-unified-intake-post-export-lifetime-desync.md`, now fixed on PR #69 and verified by latest E2E.

Limits remain: the old source editor is still a secondary presentation; order and advanced flags are not duplicated into the tree. Only already-verified MKV main-source internals render as editable tree; generic container streams, multi-container role composition, batch unification and screenshot/human visual acceptance remain future work. PR is still **Draft/unmerged**; do not promote to Canonical.


## Phase 3 — ordered edits, advanced flags, and real viewport observation (2026-10-10)

Source PR #69 head `c6354abaea9d598342ce75cca57640f80f8722df` passed GitHub Actions Chromium workflow `38022985204` with **169/169 Node tests (zero failed), full Browser E2E PASS**, and Pages build success. The E2E specifically produced and inspected a real MKV after in-tree reorder of two audio streams and mutation of source `original`, `comment` and subtitle `hearing_impaired` dispositions. The browser also checked legacy editor ↔ tree reverse synchronization, and advanced-disclosure state retention across DOM list updates. The new tree is a view over the existing `trackState`, and no new independent edit state was created.

Workflow artifact ID `11658369977`, `mkv-ui-container-tree-viewports`, contains the **populated source-tree** screenshots at 1440px desktop and 390px phone, generated from synthetic media fixtures. Visual inspection of both images found the tree and controls legible enough to locate and operate, but also uncovered two UX defects **not captured by prior source checks**:
1. The imported source row still said `需进一步验证` despite a successful real MKV internal stream scan. This conflated the earlier file-header identity stage with the later container-content verification stage.
2. The phone screenshot used very small text for track properties/flags, increasing reading effort despite no horizontal overflow.

A follow-up branch revision advanced the selected scanned source label to `内部结构已扫描` only when the matching `trackState.fileKey` exists, increased the control/metadata text scale under mobile CSS, and added a browser assertion for the truthful post-scan label. **Final follow-up CI and updated screenshot review are still pending** as of this note. None of these screenshots are a substitute for real-user usability testing.

Reusable candidate: **content identity, probe verification and task-role readiness are independent claims and should be reflected as distinct UI states**; user-entered metadata should have one canonical domain owner across multiple projections; two-way synchronization should not remount the active text input or collapse advanced disclosures. Ordering is both a UI presentation property and an output-mapping operation, therefore output `ffprobe` is necessary evidence, not merely the reordered DOM.

Related Foundry Candidate: `2026-10-04-container-inventory-stable-identity-diff.md` already covers stable identities and before/after verification in another media editor. Do not duplicate or promote either Candidate to Canonical solely on the present PR.


## Phase 3 final green validation

Latest PR #69 head: `1b579263d0a2d8393064f67ef27e9041c4a09a9a`, **Draft / open / unmerged**. GitHub Pages build run `38023534209` and Chromium E2E `38023534205` **completed successfully**. Browser job ran **169/169 Node tests**, **0 failures**, and logged `MKV container-tree order and advanced flags PASS`, `Scenario 19 PASS` (ten sequential tasks), and `All browser E2E scenarios PASS`. Artifacts: `mkv-ui-container-tree-viewports`, ID `11659630835`, two real populated container-tree screenshots at 1440px desktop and 390px phone. Output ffprobe validated audio track ordering, titles and advanced stream dispositions.

The previous visual review caught the distinction between recognized container header and scanned internal stream information: once the selected MKV has a matching completed `trackState`, the label now says `内部结构已扫描`, not `需进一步验证`. A new E2E assertion checks that transition. Desktop and phone screenshots after the correction were viewed, and phone tree text/fields were enlarged without a new observed horizontal overflow. This is limited **two-viewport evidence**, not a usability-study signoff or universal responsive guarantee.

CI history was not uniformly green: an intermediate run `38023294968` passed source-tree output tests but failed the existing ten-sequential test because it edited metadata before current subtitle/font preflight finished, capturing a stale/default subtitle title. Updating the test to await **current input identity and enabled current mux action** before editing fixed this testing race; the green latest run confirms it. The semantic readiness rule was already known in `inbox/candidates/2026-10-02-batch-execution-async-preflight-readiness-race.md`, so no redundant new Candidate was created.

Remaining: clean removal of the redundant legacy editor once full editing parity and alternate import sources are supported; true exploratory keyboard/touch visual review across more viewports; stream inventory for non-main-source containers; unified batch ingestion. No MP4 output scope, Canonical promotion, or merge of PR #69.


## Phase 4 — compact index + single-object inspector after user rejection of repeated form rows

Source PR #69 head `de1d8af62d917ddc5a07fe008cb547ec129a067e`, remains **Draft/open/unmerged**. The user rejected the prior large expansion-based container UI as lacking coherent interaction architecture. Actual screenshots showed every audio/subtitle track rendered as a repeated full form with language, title, default/forced, reorder and advanced flags, creating many long stacked rows and overlong phone scrolling.

Implementation converts the verified source MKV entry into a **compact grouped stream index** plus **one selected-object detail inspector**. Selection is keyed by stream type/index, not visual row order; an individual stream selection renders a single editable panel backed by the existing `trackState`. On wide desktop the source list and inspector are side by side; below 1100 CSS pixels they stack. The old source editor is removed from the default duplicated presentation but remains reachable on explicit source focus or 'traditional batch tools' disclosure, preserving uncommon operations and tests. Source content mutation logic, mux planner, FFmpeg, attached font and output audit are not changed.

GitHub Actions: `38024627091` **Chromium E2E success** with **169/169 Node tests**, including actual MKV output checks after inspector selection, audio rearrangement, disposition flags, attachment rename/removal and legacy editor bidirectional synchronization; Pages `38024627134` **success**. Both screenshot viewports published as `mkv-ui-container-tree-viewports`, artifact `11660147368`. Real images were inspected. At the same crop width and comparable synthetic multi-track content, the phone screenshot reduced from `366×1614` to `366×1309` pixels (305 pixels / ~19% lower), desktop from `1050×839` to `1050×763` pixels (~9% lower). These are **only image-height comparisons**, not measured human efficiency or accessibility guarantees.

Candidate learning: in editing workflows, a detected-object **inventory** and an active-object **inspector** perform different tasks. Repeating every editable property for each inventory row collapses browsing into a vertical wall of forms. Preserve item identity and one domain state while projecting compact many-item navigation and a single intentional editing surface; retain specialized/bulk tools behind explicit mode or disclosure. E2E should include actual destination artifact semantics and real viewport evidence.

Foundry dedup search `single selected detail inspector track list compact`, `master detail source container inventory`, `progressive disclosure one active editor`, `object inspector form per row duplication` found no identical record; this is recorded as an amendment to the existing content-first candidate, not as a duplicate or Canonical promotion.

Remaining: full app shell composition beyond the import section, tablet/coarse-pointer experience, genuinely independent usability and keyboard testing, eliminating old editor dependency after parity, importing/probing non-primary containers, and shared batch ingest. **Neither passing CI nor shorter screenshots alone establishes a finished modern interface.**
