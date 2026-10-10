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


## Phase 5 — physically separated source navigator, editor inspector, output rail; native task jumping

**2026-10-10, verified Draft PR #69 head `0a4ab6a47d15ada7ce71fe7f9e66874853ddad2c`.**
GitHub Actions Chromium E2E [run #38026390328](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38026390328) succeeded with **173/173 Node tests** and all browser mux scenarios passing. Pages build [run #38026390445](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38026390445) succeeded on the same head. Artifact [#11660360915](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38026390328/artifacts/11660360915) includes **4 real Chromium screenshots**: 1440×900 and 390×844 actual viewport captures, plus both full workspace captures, all generated from non-user synthetic MKV fixtures.

The previous phase compacted each stream into an index row but still kept the active stream editor **inside the import card**. That violated interaction ownership despite less vertical height. Phase 5 physically moved the selected-stream inspector into the central editor column (`#assetInspectorHost`), leaving the source inventory/stream index in the left zone and the preflight/execute/audit rail on the right. Wide fine-pointer desktop now uses a three-purpose grid; smaller viewports stack rather than collapse or remount domain controls. Original compatibility/bulk editor stays callable explicitly, not in the default UI.

**Critical event ownership:** moving an actual DOM editor out of `#assetInventory` required explicit rebinding of delegated `change`, `input`, `toggle` and track-move `click` handlers to the new host, while source selection remains in the inventory. Both projections still mutate the same `trackState`. Re-rendering the navigator after selection initially destroyed the focused button, so the handler now restores focus by stable stream identity to the reconstructed element. Browser E2E checks Enter-based selection **and continued focus**. Active track title and attachment name changes update the source index label without re-mounting the live text field, preserving caret continuity.

**Actual viewport finding:** the first whole-page and 1440px viewport screenshots showed that the long source-copy/preflight plan displaced the icon-only export action below the visible part of the output rail. Output DOM was reorganized as **summary → execution readiness/status and visibly labeled primary/secondary actions → detailed plan**, not merely reordered by CSS, preserving keyboard/reading order. At below 1440px, sticky native section anchor links (资源/编辑/输出/批量) and focusable heading targets allow users to bypass long source inventories. The 390px browser scenario verifies that choosing 输出 places the main MKV action inside the visible viewport. The resulting 1440px viewport screenshot visibly places the primary MKV action near the top of the output rail, and phone screenshot shows native nav without horizontal clipping.

**Evidence boundaries:** The 173/173 Node suite, Browser E2E and synthetic screenshots demonstrate preserved real MKV output audit and correct browser geometry/interaction. They do not establish actual human task completion time, assistive-technology usability or finished industrial design. The phone remains a vertically long task; batch is still a separate expanded secondary workflow and not unified with source ingest. PR #69 remains Draft/open/unmerged; this is **Candidate evidence only**, not Canonical.

**Deduplication:** this extends the existing content-first asset identity / role / inspector Candidate rather than creating a duplicate. Related Candidate about stable stream identity is `inbox/candidates/2026-10-04-container-inventory-stable-identity-diff.md`. Foundry searches for `event delegation DOM relocation inspector`, `live editor moved event handlers parent`, `keyboard focus remount selected item`, `source editor output separate columns` found no identical focused case. The learning is specifically to keep **task-role ownership, DOM event ownership, and focus ownership** aligned when splitting a complex interface into distinct workbench regions.


## Phase 6 — explicit CSS ownership and viewport-aware native task navigation (2026-10-10)

Source: MKV-Fast-Muxer **Draft PR #69**, verified head `ec4ec2ed103a3db4d83fe3aa17f5b8c20e4070ca`. Browser E2E [run #38027820697](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38027820697) succeeded with **177/177 Node tests**, all Chromium mux/E2E tests passing (including mobile task-jump active semantics and unchanged FFmpeg/MKV output checks). Pages [run #38027820648](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38027820648) passed on the same head. Four synthetic-fixture screenshots published as [artifact #11660956495](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38027820697/artifacts/11660956495).

The prior workbench's terminal CSS overrides were a single **~369-line patch stack at the end of a 6,238-line stylesheet**. Phase 6 extracted this suffix into `src/workbench.css`, declared the workbench stylesheet as the authority for compact stream navigation, active inspector, output actions, three-zone/stacked geometry and task jumps, and imported it **after** `src/style.css` from `src/main.js`. This is a scoped ownership refactor, **not** a claim that the remaining ~5,868-line global stylesheet has been completely normalized.

**Visual equivalence check:** downloaded this exact head's Chromium artifact, unzipped four screenshots, and compared RGBA pixels against the previous green workbench head's four comparable screenshots using Pillow `ImageChops.difference().getbbox()`. All **four image pairs had exactly identical decoded pixels**: desktop 1440×900 viewport and 1404×1430 full-workspace; phone 390×844 viewport and 366×2699 full-workspace. PNG file byte hashes differ in two pairs despite pixel identity; use decoded pixels, not file hash, for equivalence. This is strong but limited evidence for the four captured fixture states, not a proof for all breakpoints, browsers, live media or interactions.

The native 资源 / 编辑 / 输出 / 批量 anchor bar now reflects the active viewport section using `aria-current="location"`; the app does not intercept the hash navigation, steal keyboard focus, or rebuild editor DOM. The initial Chromium E2E revealed that **the sticky navigation's geometric cutoff was not the same as the browser's fragment scroll landing position**: clicking 输出 then keyboard-activating 编辑 successfully updated the URL hash but the active marker reverted. The corrected projection favors a matching URL fragment when its actual heading is near the top of the visible viewport, then restores geometry ownership after the user scrolls away. A targeted unit test exercises this distinction and listener cleanup; real browser E2E confirms native pointer and keyboard task jumps.

Reusable Candidate: a component style authority can be extracted without functional/UI regression **if cascade order is explicitly preserved and visual snapshots compare decoded pixels**. In fragment navigation, URL location, sticky visual occlusion, scroll-margin, current-section semantics and focus movement are distinct concerns. Preserve native navigation and independently project `aria-current`, with view geometry and bounded hash-target precedence rather than forcing a custom router. This is additional evidence for the existing Candidate, **not** a Canonical promotion.

Foundry dedup queries covered `CSS cascade authority workbench separate stylesheet`, `responsive css last-write wins architecture`, `task navigation aria-current scroll position`, `navigation current section scroll anchor focus`, and `UI stylesheet split preserve cascade`; no more specific existing CSS-ownership/anchor-state record was identified. Remaining: CSS authority cleanup beyond this suffix, accessibility with assistive tech, mobile task-length reduction, and batch-ingest integration. PR #69 remains Draft/open/unmerged.


## Phase 7 — unified batch ingest without implicit role guessing

Draft PR #69 expands the existing *content identity versus task role* distinction from single MKV jobs into **batch intake**. The original batch UI required separate VIDEO/SUB/FONT file and folder gates. New UI presents one mixed file/folder/drop entry with every imported file shown in an auditable inventory. The same bounded content-header classifier from `src/asset-intake.js` routes *all* container candidates to the existing batch video preflight, recognized subtitles to the existing matching and IDX/SUB checks, and fonts to the existing batch font pipeline.

**Important capability boundary:** a recognized container header does not prove it contains video; existing `identifyBatchVideos` remains authoritative. Standalone audio, unknown or unreadable inputs are retained in the visible inventory as **unsupported for the current batch mux plan** and block execution until removed. Even an identified container rejected by actual batch video preflight now blocks execution in the unified path rather than disappearing from work. The unified batch path also does **not** inherit hidden single-task font selections. Existing legacy category inputs remain explicitly disclosed for compatibility; choosing them switches out of unified mode instead of mixing stale hidden adapter files.

The implementation reuses existing batch picker `FileList` adapter events under a guard and invokes the pairing plan once after role synchronization. It explicitly advances the pairing generation when new file bytes begin classification to stop an earlier async result from re-enabling execution. The visible batch region overrides the legacy three-column *upload-gate* grid; the old three-column cluster layout remains only inside the advanced compatibility disclosure.

**Evidence at initial record:** 3/3 source-derived UI tests and JavaScript syntax checks passed; the first full Chromium E2E and screenshot check (1440px desktop, 390px phone with real fixture assets) were running at initial entry. The browser scenario must prove unknown audio blocks start, removal allows a real MKV mux with subtitle + font, downloaded MKV streams pass ffprobe, legacy picker switching clears the old unified context, and mobile grid has no horizontal overflow. Do **not** assert full browser acceptance until latest-head CI completes.

Reusable distinction: **“unified intake” does not mean “all media types are executable in every task mode.”** Keep format identity and per-workflow role compatibility separate, and expose rejection rather than treating nonmatching assets as silent no-ops. No Canonical change and no MP4 output implementation.


### Phase 7 latest-head evidence — verified

Draft PR #69 **head `59add37a9765ebf823a24aa2fe3f14b7e82b7608`**, GitHub Chromium run [`38051694757`](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38051694757) **completed successfully**: **182/182 Node tests, 0 failures, all browser E2E scenarios pass**, including the new content-first batch import scenario, incompatible audio blocking/removal, real downloaded MKV probe with video+subtitle+font attachment, and explicit isolation from the legacy categorized picker. Pages run `38051694767` succeeded. The browser suite also passes a desktop **inter-workbench non-overlap** geometry assertion and 390px no-horizontal-overflow assertion. Screenshot artifact `11669673885` contains six actual fixture-backed UI images.

The corresponding desktop and phone batch screenshots were downloaded and actually inspected. Desktop `mkv-container-tree-batch-desktop-1440.png` shows one full-width mixed intake, video/subtitle/font rows, separately controlled batch settings/plan and start; the prior sticky single-task output overlay is absent. Phone `mkv-container-tree-batch-phone-390.png` shows readable rows stacked into a single column, rather than clipped three-way category slots. These observations do not prove human accessibility or optimize task duration.

The earlier failed run `38051094510` already passed the real batch mux and output audit but its test incorrectly demanded a formed pairing after explicitly clearing the legacy subtitle input. The corrected regression first verifies old adapter inputs are cleared, asserts no executable job without matched subtitles, then supplies a matching legacy subtitle and verifies the old plan reactivates. This is a **test contract correction**, not a relaxation of the application's pairing safety rules.

Status remains **Candidate only**; no Canonical changes. PR #69 remains Draft/unmerged; standalone audio append in the batch workflow is explicitly unsupported, and all container headers still require authoritative probing.


### Phase 8 — keyboard focus continuity when asset-list DOM is replaced

In PR #69, single-job and batch inventories replace their entire row DOM when removing a classified file. The old focused Remove button is destroyed, and without explicit restoration keyboard users can be returned to the document rather than a meaningful next action. A change to the active main-source radio also replaces the old focused control. This issue is distinct from the existing selected **track-inspector** focus restoration: it concerns **imported-asset action controls**, including the newly unified batch workflow.

The implementation now shares `src/inventory-focus.js`: after executing the real adapter and plan synchronization, it locates the surviving resource at the same row index (or last surviving), or the import dropzone when the inventory becomes empty. Main-source selection instead locates its radio by stable content identity. It applies `focus({preventScroll:true})` and never mutates task roles itself. Four direct unit tests passed in a source-derived V8 check. The latest Chromium scenario adds keyboard Enter for single/batch deletion and Space for source selection, checking `document.activeElement` **after the UI rerender**, not merely button labels.

Deduplication searches for `inventory removal focus restoration`, `keyboard focus after deleting resource list item`, `dynamic file inventory focus update`, `focus restore after DOM recreation` found no independent matching Candidate. This extends the existing shared-domain-inventory Candidate rather than creating a new Canonical principle. **Full latest-head CI is pending at the time this update was authored**; successful E2E evidence must be attached separately before upgrading its status.


**Phase 8 verified evidence (latest Draft head `9596b2606f77a4dd2ee1a5e62f54f9873799dfa4`):** GitHub Actions [Chromium run #38060726820](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38060726820) **completed success** with **186/186 Node tests, zero failures, all Browser E2E scenarios PASS**. The browser suite explicitly performs Enter-triggered removal of the last unsupported resource in both the single and batch inventories, verifies focus moves to the neighboring surviving item, and Space-triggered radio source selection with focus restored by stable asset key. Pages run #38060726823 succeeded on the same head. Artifact #11672494573 carries fixture-backed interface screenshots (not newly inspected in this phase).

This upgrades the preceding focus-continuity proposal from source-derived checks to **tested keyboard behavior in real Chromium**; it does not prove screen-reader announcements, assistive-tech compatibility or human usability. Draft PR remains unmerged; no Canonical change.
