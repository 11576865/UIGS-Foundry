# Observation: HSR subtitle-request closure differs from branch implementation and delivered main

Status: Observation / requirement-to-delivery audit, not Canonical
Date: 2026-10-13
Domains: UI, subtitle effects, media preview, engineering process, stacked PR integration
Source: `11576865/HSR-Voice-Archive-Builder`

## User-stated task boundary (current conversation)

The user describes three desired changes: remove the duplicated subtitle layout boundary, split out a subtitle effects workbench, and add video preview for judging animated effects. This is a current user report, not a reconstructed verbatim earlier specification; do not infer that no other directions were authorized in unseen conversations.

## Repository observations

1. PR #132 was merged directly to main at `88cbadd80229720c88f85903fa3924e6a4fac2a3`. Its work is a much wider subtitle studio: cue editing, non-destructive display timing, interactive event timeline, WAV audition/waveform, export evidence, concurrency protection and Chromium/libass tests.
2. PR #133 was merged into feature branch `feat/subtitle-style-workbench-evidence-v15`, not main. PR #134 was merged into feature branch `feat/hsr-archive-audit-karaoke-v1`, not main. GitHub reports all three as `merged=true`, but that metadata alone does not prove #133/#134 content is in main.
3. At inspected main HEAD `88cbadd80229720c88f85903fa3924e6a4fac2a3`, `docs/subtitle-layout-safety-ratio.md` is absent. It exists at #134's feature head. `compare_commits(main, #134 feature head)` reports `status=diverged`, `ahead_by=180`, `behind_by=3`; therefore the #134 implementation has not been integrated as current-main authority.
4. PR #134 narrows “duplicated boundaries” to one layout `SafeArea`, suppressed diagnostic boxes, and zero additional ASS Style margins for explicitly positioned bilingual text. This still retains the safe area and central gap; it is not a wholesale abolition of all geometry constraints.
5. Current-main UI inventory exposes `HSR.WORKSPACE.LAYOUT` and inspector sections rather than a separate subtitle-effects workbench. The current v15 workbench document expressly characterizes itself as one editing surface, not a separate tab/product.
6. Current-main preview consists of browser geometry and on-demand FFmpeg/libass rendered still frames. PR #132's scope explicitly excludes render-backed video playback. #134's timestamp and sampled-interval rendered-ink checks explicitly do not constitute continuous video playback.

## Requirement-to-acceptance gap

The reusable issue is not that these additional features are intrinsically wrong. It is that capability completion must be checked against the user's original *interaction-level request*, the actual current-main code and the requested runtime/media evidence, not against number of commits, green CI, merged labels or visually adjacent substitutes.

A single FFmpeg/libass PNG is renderer evidence, not video playback. Effects controls inside a style Inspector are not automatically an independent effects workbench. Removing redundant ASS margins while preserving one layout SafeArea is a narrower interpretation of “remove duplicate boundary” and needs acceptance against the user's intended meaning.

## Actionable follow-up (not performed by this observation)

- Make a three-row acceptance ledger with explicit semantics and user approval.
- Inspect branch ancestry and integrate only the wanted verified delta onto current main; do not force-reset a divergent branch.
- For video: require actual user-supplied moving media, playback/scrub with audio-time identity, ASS composited at the selected instant, and field verification; do not substitute browser bounding boxes or synthetic black-frame renders.
- Do not promote this single case into Canonical.

## Deduplication

Extends rather than replaces existing Foundry knowledge:
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md`
- `inbox/observations/2026-10-04-collapse-stacked-pr-chain-by-retargeting-top.md`
- `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`

Specific new observation: this HSR three-requirement audit reveals both mainline ancestry and semantic substitution (still-frame evidence versus requested moving video, inspector section versus separate workbench).

References:
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/132
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
- https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134
- https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/.uigs/ui-surfaces.json

## Follow-up: concrete duplicate-control ownership and CSS accumulation (2026-10-13)

Source inspected: HSR `main`, commit `88cbadd80229720c88f85903fa3924e6a4fac2a3`, `app/static/index.html`.

- Proofreading workspace has `subFinalEditor` for final Chinese and states that it auto-saves after approximately one second of idle input. Layout workspace has a separate `layoutCueFinalText` editor and explicitly requires `layoutCueSaveBtn`. This is not merely two read-only projections: the same kind of final subtitle text is independently editable through UI with divergent save semantics. A single authoritative final-text write path is preferable, retaining the distinct high-value proofreading context and shared per-cue identity.
- Proofreading has `subListView` / `subSearchQuery`, while layout has `layoutCorpusList` / `layoutCorpusSearch`; both provide project subtitle navigation. The original WAV is available via `subOriginalAudio` and via layout's `layoutCueAudio` with waveform. A shared item-selection/audio resource component or explicit read-only projections can eliminate duplicate business ownership without eliminating purpose-specific affordances.
- Layout's `layoutCueScrubber` and karaoke `prevKaraokePreviewTime` are separate time-position controls that need an explicit shared preview-clock contract; they need not be identical controls, but inconsistent clocks or effects are a risk worth testing.
- The production `index.html` is 8,516 lines / 421,591 characters at inspected main; its CSS contains 945 `!important` uses and repeated layout/workbench selector overrides. This count is a maintainability signal, *not* proof that every override is a defect. A previous HSR #129 explicitly fixed a real old/new CSS layout-authority collision.
- Proposed acceptance structure: one authoritative cue editor and commit path; per-workspace presentation projections; a distinct typography/layout workspace and motion/Karaoke effects workspace sharing one preview/clock/state; preview-render verification separated from actual moving-video playback; output execution remains in Export. Never silently remove existing actions before an ID→owner→destination parity ledger and regression.
- This overlaps the existing Foundry MKV two-editor Candidate `inbox/candidates/2026-10-10-mkv-ui-primary-action-and-editor-discoverability.md` and CSS authority Candidate `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md`. Treat the HSR facts as project-specific corroboration in this existing Observation, not as a new universal rule. Do not auto-promote Canonical.

Suggested validation: user-visible save behavior across Review/Layout, delayed input vs stale backend response, identical export text/sidecar, cross-workspace focus/preview identity, FFmpeg/libass v. browser still-frame mode, actual video playback, and 390px/768px/1600px responsive captures.


## Delivery follow-up: three-pass implementation landed to main (2026-10-13 discussion / UTC merge 2026-10-12)

Product: `11576865/HSR-Voice-Archive-Builder`. User explicitly constrained scope to **three processes only** (deduplication, UI workbench division, actual playable preview and acceptance), to prevent feature creep.

- Implemented PR [#135](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/135), source head `4072b8c43098d26512071b4c6e4054ee7e40ed63`, merged **directly to main** at `5e7fa67a2d3285c611390c1e0651ffcf24f5979e`. Verified subsequent main search and main file fetch.
- Pass 1: Review is the user-facing final Chinese text and original WAV editing/listening owner; Layout projects the selected text as read-only, routes to Review by cue identity; Review draft flush and Layout refresh on navigation. Existing timeline display timing editing remains.
- Pass 2: separate scoped Style and Effects views share a single project/render config/preview. Bilingual explicitly positioned CHS/Primary ASS styles no longer apply redundant Style margins on top of solver SafeArea. Debug boundary overlays default off.
- Pass 3: FFmpeg/libass renders **actual video over a generated black background**, 24fps, max 8s; WebM/VP8 chosen for Chromium where H.264 decoder unavailable, MP4/H.264 otherwise. Browser must decode and allows seeking; stale requests discarded. Backend FastAPI and Termux Lite provide protected API. This does **not** contain a user-provided moving video, source WAV synchronized audio, or physical device acceptance, and must not be described as such.
- Exact-head tests CI [38293666205](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38293666205) `success`; Chromium + libass [38293666354](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38293666354) `success`. The Chromium playback test used independently generated **real VP8 video bytes served by API fixture**; backend FFmpeg/libass actual video encoding/decode-frame difference was tested in a separate job. This scope distinction prevents E2E overclaiming.
- Maintains important explicit non-claims: complete removal of all duplicate code (legacy handlers remain for compatibility), comprehensive CSS refactoring, production multimedia user-supplied video overlay, and field/device sign-off have **not** been proven. Source-level UI deduplication and two-role projection were delivered; this is a bounded implementation, not full architectural rewrite.

Reusable observation: define and prove **user-facing ownership / product acceptance** separately from source-code deduplication and automated rendering evidence. A three-pass stop rule forced main integration and eliminated unbounded feature expansion, while distinguishing actual playable black-background preview from actual source-footage composite.

Deduplication: retain existing `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md`; related records: `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` and `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`. Observation only; **Canonical unchanged**.


## Delivery follow-up: opt-in local moving footage composite (2026-10-13)

Converged directly on main via HSR PR [#136](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/136), exact source head `e3e2ff874260e56ea0295ab631be4cd2cca1a985`, squash merge `b51cf24e11f095329527ca6594af7199054a6002`; post-merge main tip and test file were verified.

User-facing improvement: the previously black-only animated libass proof now has an **optional** user-selected local moving-video input (with source offset and clear-to-black). The same renderer burns animated ASS over a real moving background. UI represents `video-footage` separately from `video` (generated-black) and displays source provenance. This is not a new production export or second subtitle authoring system.

Implementation and limitations: no user-provided path or URL is accepted by the FFmpeg execution plan; the API accepts only up to **4 MiB** of base64-decoded local bytes, checks actual JSON request length at **8 MiB**, and probes the file for a video stream, source-window duration, and maximum **3840×2160** dimensions. Selected start offset is **0–600 s** and preview output **0.5–8 s**, 960×540, 24fps, without audio. Input is held in a temporary directory and deleted after each render. Termux Lite and FastAPI keep their distinct host implementation but share the renderer.

Exact-head CI:
- [38326261385](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38326261385): `success` (Python matrix and Termux Lite).
- [38326261297](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38326261297): `success` (Chromium interactions and actual FFmpeg/libass backend proof).
- Chromium test picks real WebM bytes via a file control and proves browser decode, state provenance, and seeking. API is fixture-backed for this browser test. A **separate backend test** synthesizes a real moving-video source, compares a rendered ASS overlay against a source-only encode, and decodes actual pixel differences. Do not misreport the Chromium test as an integrated actual backend E2E with real user clips.

Observed edge case: A pixel-comparison control test initially supplied both dialogue fields empty to the ASS writer, which correctly rejects dialogue-less output; test repaired by independently generating a no-subtitle FFmpeg control clip using equivalent frame normalization. This is a **test fixture defect**, not an application regression.

Still out of scope: unbounded/full-length footage, audio synchronization, source-time-aware word highlighting beyond the preview-local interval, large uploads, arbitrary codec/device coverage, end-to-end actual backend Chromium playback, real Android-device validation, or final project export.

Reusable project-specific lesson: a video-effect preview has multiple distinct evidence layers—UI provenance, actual source-byte forwarding, decoder usability, and source-vs-overlay rendered pixel proof. Green at any one layer cannot stand in for the rest. Deduplication: attach to this existing HSR Observation and the related subtitle preview Case rather than creating another overlapping Candidate. **Do not promote to UIGS Canonical from this single project.**


## Mainline update: opt-in source audio and live Chromium/libass E2E (2026-10-13)

HSR [PR #137](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/137) merged **directly into main**, exact source head `a24b25889b8b19dfafab6c05492e1edf44a1bd9f`, squash commit `aba42855b32828e12c86b209ff000440e364adc8`. Verified post-merge main tip and the live E2E test file.

Product boundary: extends *existing* Effects workbench, no second editor, no new workbench. Opt-in local source input increases from 4 MiB to **24 MiB** with 36 MiB request-body bound on the preview endpoint only (Lite's other operations retain the 8 MiB request cap). Video output stays **0.5–8s**, source offset **0–600s**, 960×540, 24fps, ephemeral source within the FFmpeg temp dir. This remains Base64 JSON (not an unbounded/streaming full-movie design).

Audio semantics: `include_source_audio` selects the **first audio track of the user-selected video**, if present. It is seeked and clipped in the *same* FFmpeg operation as source picture + libass ASS. MP4 transcodes that audio to AAC; WebM to Opus; opting out or using black input yields silence. This is **not** synchronization with the HSR archive's separate WAV file, nor proof of all audio tracks/encoders/devices.

Exact-head green CI:
- [38328657466](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38328657466) — Python matrix 3.11/3.12/3.13 + Termux Lite, all success.
- [38328657467](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38328657467) — real FFmpeg/libass unit proof, responsive Chromium layout tests and **live browser-to-server media request**.

The newly added `tests/browser_live_preview_e2e.py` runs the real FastAPI application through uvicorn, loads the shipped HTML under **production CSP**, selects real synthetically generated WebM video with an Opus tone, and forwards its video-preview API through Playwright's `route.fetch()` to the **actual backend**. It captures that actual response body (not a mock media fixture), delivers those same bytes to Chromium, confirms FFprobe codec and AV start alignment, actually decodes output audio samples, and checks browser decoded video + seeking. Unrelated project/corpus endpoints retain fixtures; real Android/production user-media coverage remains unproven.

Two newly observed testing pitfalls (not automatically Canonical):
1. The old fixture-only browser suite lacked production Content Security Policy, so `page.wait_for_function` string-expression tests did not catch `unsafe-eval` restrictions. Live test retains CSP and uses `page.evaluate` callable polling, never weakens production policy.
2. Under Playwright `route.continue_()`, the subsequent page response's `Response.body()` was empty in this CI environment even though it had HTTP 200 and real media headers. The test captures original binary using `route.fetch()` and `APIResponse.body()`, then `route.fulfill(response=upstream, body=payload)`. It does not fabricate rendered media; E2E assertions read verified upstream bytes and confirm the same bytes are playable in Chromium.

Deduplication: recorded as a follow-up to this existing HSR Observation, and complementary to `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`; do not generate redundant generalized rules from one app. Canonical unchanged.


## Product follow-up: actual visible UI convergence delivered on main (2026-10-13)

HSR [PR #138](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/138), exact head `070f69fe6932f952baf302d135259d6dc9ce2bd3`, merged **directly to main** at `e19794c57e1e3912e7fe3b0450ced32722909472`. Verified main tip and separately loaded `app/static/hsr-ui-convergence.css`.

Specific initial problem: although PRs #135–#137 added functional renderer and partially scoped Style/Effects, the UI still displayed a second full subtitle navigator/search, disabled text editor, manual trial editor, mixed task tabs deep inside Inspector, and overlapping old CSS. That meant a green renderer CI did not satisfy the original task-level product contract.

Change:
- Layout/Effects navigation promoted above the canvas/Inspector into a top-level task switch; title + Inspector task heading change together.
- Existing corpus explorer is now a **collapsed, inert, explicitly opened batch layout QA surface** for pressure/issue screening and audit. Review retains the primary searchable subtitle list, Layout Effects retains event timeline; QA behavior remains accessible and is not removed.
- Layout's second final-text `textarea` is hidden and its content is displayed as a normal read-only paragraph; the user is directed to the Review-owned save editor. Sample/trial text input is behind a collapsed, clearly non-authoritative disclosure.
- ASS file generation is under a distinct output disclosure instead of competing with the primary style save action.
- Fixed literal `\\n` in legacy CSS and introduced a new separately maintained responsive CSS file after the inline layer as the single new layout authority rather than appending another inline override. It supplies two-column desktop, single-column tablet, responsive mobile **by default**, with legacy 3-column arrangement available when opening QA.
- Actual Chromium tests now screenshot and assert the **default collapsed UI** at 1600px, 768px, and 390px before exercising the advanced QA drawer and former drag/edit flows. Both exact-head [tests run 38342430246](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38342430246) and [Chromium/libass run 38342430289](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38342430289) succeeded.

Boundary: this is a **visible functional de-duplication and coherent task navigation** delivery. Old JS compatibility handlers and some duplicate underlying data fetches remain; it does not prove complete source refactoring or erasure of all existing `!important` rules, full-length video input, archive-WAV mixing, or Android physical-device signoff. These must not be marked complete merely because green UI CI is present.

Reusable test observation, overlapping existing Foundry knowledge `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md` and `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md`: the **default visible task configuration** (not solely all reachable controls) is a necessary UI acceptance target. Hidden-but-accessible specialist diagnostics can preserve functionality while returning primary screen space to the task, but must remain accessible/keyboard navigable; regression must check closed and open states. Case-specific corroboration only, Canonical remains unchanged.


## HSR first-class Effects workspace mainline follow-up (2026-10-13)

Source: [HSR PR #139](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/139), exact head `8c2221ee95650f620711a54ec1701851bede09ba`, squash merged **directly to main** at `ca01ecba6d31c417daf33c635e1ee228dc80d916` (main HEAD and production HTML/capture manifest verified).

New observed correction to PR #138: moving the Layout/Effects local tab pair *above* the Inspector was not enough to fulfill the user's "separate Effects workbench" requirement. The app's primary workspace nav still exposed only "排版", while "特效" was nested in that page. A green UI layout check masked a semantic/navigation ownership gap.

Bounded implementation: the **six-item primary nav** now has separate `排版` and `特效` destinations, removes the second inner task-tab pair, and updates context titles and selected-task evidence. Both destinations project the **same** underlying `#subtitleLayoutPreviewCard` and project/canvas/ASS state. `body.dataset.workspace='layout'` provides compatibility with existing large CSS and layout code; `body.dataset.workspaceTask='effects'` independently names the user task. Switching between these two destinations does not re-fetch the entire subtitle corpus; crossing from Review still invokes its conflict-safe unsaved-text save/refresh path. Layout-only batch QA is not a default Effects control. Updated `.uigs/ui-surfaces.json` to 12 declared surfaces, with Effects visual-capture fixture in `.uigs/ui-visual-capture.json`, and synchronized shell/visual tests.

Exact-head green evidence:
- [tests run 38343976722](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38343976722): Python 3.11/3.12/3.13, Termux Lite all success
- [Chromium/libass run 38343976711](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38343976711): desktop, tablet, mobile mode routing, no second corpus fetch during Layout-to-Effects switch, original timeline and real browser/FFmpeg preview regressions all success.

The initial failing CI was an obsolete app-shell snapshot expecting five primary tabs, plus a missing new Effects entry in the UI capture manifest. A later Chromium test incorrectly expected a Layout-only batch-QA button inside Effects. These were corrected by proving intended behavior, not by removing the product-level separation. No blanket CSS rewrite and no separate Effects data model.

**Remaining known debt**: Review and Layout can still make distinct server data queries when arriving from another workspace; compatibility-only hidden cue editing/audio event handlers remain; broad historic inline CSS overrides and physical Android usability are unverified. This is a product-navigation and same-task refetch reduction, **not** wholesale source-code/data-fetch de-duplication. Candidate/general principle overlaps `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md`; do not create a redundant new Candidate or alter Canonical based only on HSR.


## HSR PR #140: gated Review navigation and optimistic-lock ownership (2026-10-13)

Source [HSR PR #140](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/140), exact source head `95e1734f823f5934f6368b958246c1f4a9e59539`, merged directly into main as `dd5fe10ab476a724f68679bc29a05ad65b5027f6`. Verified main tip and regression file.

Defect: Review was the user-facing authority for `final_chs` but its writer sent only `{id,final_chs}` (missing server-side optimistic-concurrency preconditions). The hidden, duplicated Layout writer had the stronger preconditions. Moreover, switching Review -> Layout/Effects changed the visible workspace **before** awaiting the pending text save, so a failure could leave the user viewing stale subtitle effects with an unsaved draft in Review.

Bounded fix:
- Dirty Review -> Layout/Effects transition remains on Review until save is confirmed and that cue has no newer dirty edits. Any failure prevents visible navigation and preserves the draft. Navigation-generation checks prevent an earlier async completion from hijacking a later user choice. Leaving the shared layout canvas also invalidates an earlier corpus request generation.
- Review now sends the prior baseline (`expected_final_chs`), source member (`expected_source_member_id`), and project root (`expected_project_root`) to the existing server's conflict guard. It captures target project identity before an asynchronously serialized write, checks identity again after response, and reports stale edit conflicts without silently overwriting them.
- The legacy Layout text editor's hidden input/save hotkeys are disconnected and its direct helper refuses read-only/disabled DOM. Distinct subtitle *display timing* editing and the waveform remain supported.
- Existing code compatibility handlers are not entirely removed; this is a runtime ownership enforcement plus correct authoritative persistence, not a whole-module deletion.

Evidence on exact head: [tests 38345986268](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38345986268) and [Chromium/libass 38345986337](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38345986337), both success. New production-source Node regression in `tests/test_hsr_navigation_save_gate.py` checks save-first, save failure, stale navigation and request invalidation. Legacy duplicate-editor tests were updated to assert *read-only* projection and no duplicated text POST, rather than preserving outdated expectations.

Reusable observation (dedup with `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md` and `inbox/bugs/2026-10-10-hsr-durable-subtitle-edit-versus-export-refresh-failure.md`): single visual editing ownership is insufficient if the authoritative writer lacks the conflict checks previously found on the secondary editor; save-first navigation must be measured independently of view-switch animations. No automatic UIGS Canonical promotion.


## HSR mainline follow-up: project-scoped cross-workspace subtitle corpus snapshot (2026-10-13)

Source [HSR PR #141](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/141), exact source head `3ea4bfa887cac97d64751828bff702d0092791a9`, squash merged **to main** at `326a87add0779aa94ae89477ddcbcb8577a2f925`; main HEAD and new test checked after merge.

Problem: `fillProject` initiates a Review list request, and Review → Layout initiated another `GET /subtitles?selector=all`. More seriously, an older Review response did not verify project identity or request generation before replacing the current list.

Fix scope: immutable copied, **12-second** candidate snapshot of a clean `selector=all` Review response. On Review → Layout/Effects it is reused only when its project identity, generation, age, and no dirty drafts pass checks; a filtered Review request invalidates it. User-requested explicit Layout refresh does not rely on the snapshot. Successful Review text saves and Layout display-timing saves invalidate it. Project switches invalidate both the snapshot and stale Review requests; stale HTTP failures are not rendered on the new project's UI. The preview and independent timing/word-alignment fetch paths remain.

Exact-head CI success:
- [tests 38347636287](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38347636287): Python 3.11 / 3.12 / 3.13 and Termux Lite
- [Chromium/libass 38347636232](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38347636232): real Chromium UI requests with corpus/API fixture, actual FFmpeg/libass regression
- Chromium counted **1** full-list request for clean Review → Layout, and **3 total** for initial clean Review, later filtered Review, then new unfiltered Layout read. The corpus/backend response is fixture-backed for this request count; it is **not** end-to-end external multi-session freshness evidence.
- `tests/test_hsr_shared_subtitle_corpus.py` tests project separation, dirty-draft rejection, TTL, copy isolation and mutation invalidation against extracted production source.

Observed regression-test integration pitfall: older timing/timeline Node suites extracted only JS beginning at `let layoutStressSample` and omitted the newly shared invalidation helper, producing misleading timing-save failures. Tests now include the complete relevant production helper. Browser network event test also needs to wait for HTTP **response** rather than just the emitted request before asserting handler request counts.

Known limitations: this is **bounded read reduction** for a valid clean snapshot, not one physical canonical corpus store. Searches, explicit refresh, changed subtitles, expired snapshots, and some other workspace paths still fetch. Cross-session updates within the 12-second window may not be shown immediately, though edits use server optimistic-concurrency guards. Broad historic CSS overrides and Android physical-device usability remain unverified.

Dedup: retain this existing HSR Observation rather than promoting a new Candidate; related `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md` and the prior UI CSS authority candidate. Do not alter UIGS Canonical based on one app.


## HSR task-boundary regression: Layout-only QA must close on Effects navigation (2026-10-13)

HSR [PR #142](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/142) exact tested head `07f4e7430970067dab089364aebf49992d769476`, squash merged to main as `24e9db70e65339122cb4bd04a11618e3f0e6a09d`; production HTML/CSS and main tip verified after merge.

Observed UI defect: after promoting Effects into a first-class destination, the old layout-only optional batch QA rail still remained visible in Effects if the user first opened it in Layout. An earlier Chromium regression had explicitly **expected** this leak, even though the Layout toolbar was hidden. This is concrete evidence that a green screenshot/geometry suite may fossilize an incorrect task-boundary behavior when UI responsibilities change.

Bounded fix: entering Effects now closes the optional QA drawer and synchronizes `aria-hidden`, `inert`, `aria-expanded` and `audit-open`; keyboard focus located within the rail moves to the visible Effects primary navigation item rather than being stranded inside a hidden control. A scoped CSS fallback prevents the layout-only QA rail from being painted in `data-studio-mode="effects"`. Returning to Layout keeps the drawer closed until explicitly opened. Navigation accent CSS now uses semantic `data-workspace-target` rather than fragile positional `nth-child` styling, and unused nested `.hsr-studio-tabs` styles were removed.

Evidence on exact head: [Python/Termux suite 38349516459](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38349516459) and [responsive Chromium + libass 38349516465](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38349516465), both success. Browser tests examine desktop, tablet, mobile states, actual QA opening in Layout then closing in Effects, accessible state transitions, restored two-column/stacked viewport, and programmatic keyboard-focus recovery. Media playback regressions remain green.

Reusable observation, deduplicated with existing `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md`: when a specialist subtool becomes task-scoped, tests must verify **absence** of the tool in other tasks, not merely its availability somewhere in the app; hidden panes must atomically transition visual state, focusability, and ARIA state. This single HSR observation does not justify automatic UIGS Canonical changes. Still unverified: Android physical-device usability and comprehensive historical CSS/source code removal.


## HSR PR #143: source-level retirement of hidden duplicate subtitle/audio controls (2026-10-13)

Source: [HSR PR #143](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/143), exact reviewed head `934eeb20ba48eace490d92424e34b1867c830222`, merged to `main` as `260f9a1431f2035b666794d37948a6c2ef72c2d3`. Verified postmerge HEAD, checked-in regression and actual production HTML: exactly **one `<audio>`** (`#subOriginalAudio` in Review); retired `layoutCueAudio`, `layoutCueFinalText`, `layoutCueScrubber`, `saveLayoutCueText`, and `layoutCueWaveform` source markers absent.

Problem: Earlier HSR PRs had only hidden the second Layout editor, original WAV player and per-cue scrubber. The Layout module continued to retain a complete abandoned text writer, independent audio fetch/waveform/decoder with AbortController and object URLs, leftover click/key listeners, a parallel preview position, legacy CSS specificity overrides, and a `beforeunload` warning for invisible text drafts. Visually hiding the controls did not fully establish single-owner behavior.

Change: Actually delete the abandoned second Layout text/audio/scrubber DOM and corresponding JS implementation and obsolete scoped CSS. Preserve the **Review-owned** `final_chs` writer, selected original WAV loader and validation, plus the **Layout/Effects-owned** read-only text projection, persisted subtitle display timing, pointer/keyboard time editing, Karaoke preview time slider and real playable effect rendering. Effects' visible `#prevKaraokePreviewTime` drives the playhead; `layoutCueState` becomes a projection of persisted text rather than a second draft store. Removes a stale warning about drafts that could no longer be edited.

Evidence for exact PR head:
- [Python 3.11/3.12/3.13 + Termux Lite 38353418708](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38353418708): success.
- [Chromium desktop/tablet/mobile and actual FFmpeg/libass 38353418689](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38353418689): success.
- Revised `tests/test_subtitle_cue_audio_waveform.py` proves the production **Review** WAV loader validates a WAV signature, avoids redundant object URLs for the same selection and revokes the URL on release. Browser checks absence of the old duplicate DOM and exactly one audio element while exercising timeline and effect playback. The initial failing unit test misquoted the source fixture's timeline start/end (`8,10` rather than `5,9`), repaired without production rollback.

Evidence boundary: this retires a specific abandoned duplicate subsystem; it is **not** proof that all historical inline CSS, all unused JS, all cross-workspace API loads, full-length movie preview or physical Android UI problems are fixed. The existing CSS authority Candidate and HSR Cases already cover the broader reuse principle: when designating a single visible owner, source-level duplicate listeners and persistence paths may still exist; acceptance should prove negative DOM/handler absence as well as surviving owner behavior. Append to this Observation rather than create redundant Canonical changes.


## HSR mobile QA double-toggle elimination and focus handoff (2026-10-13)

HSR [PR #144](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/144), source head `7ca54b8fd6590485dd8e8a8c01c75b3d6f520cf0`, merged directly to main at `75f27f3866b41ddde73ed20ed8c22f2a1367ba44` (verified main tip, production HTML).

Root cause: mobile batch Layout QA retained a legacy inner `layoutCorpusMobileToggleBtn` controlling `.is-open` independently from the new single top-level `layoutAuditDrawerToggle`, which already controlled `.audit-open`, `inert`, `aria-hidden`, `aria-expanded` and the visual availability of the rail. The old mobile CSS could hide the rail's search/list/footer under an expanded parent. The inner button therefore represented **duplicate UI state ownership**, not additional product functionality.

Fix: remove the inner mobile expand button, its event listener and the dead responsive CSS that hid QA content according to that inner toggle. All viewports now use the single outer Layout-only batch-QA disclosure. On switching to Effects, the programmatic transition moves focus to the visible `studioEffectsTab` when focus is either inside the QA rail **or on the soon-to-be-hidden QA opener**. Existing project, timing, libass, and media behavior is preserved.

Evidence, exact PR head:
- [tests 38354549750](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38354549750): full Python 3.11/3.12/3.13 and Termux Lite, success.
- [browser + libass 38354549720](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38354549720): Chromium desktop/tablet/mobile interaction and real FFmpeg/libass tests, success. Browser checks opening shows actual QA search, list, and refresh controls at mobile widths; the duplicate toggle is absent; expanded rail is not inert; closing/switching restores ARIA/inert state and visible focus.
- Two earlier test assertions still expected the removed secondary toggle; they were updated to assert **the sole intended disclosure contract** rather than reinstating the duplicate.

The reusable observation overlaps the existing CSS authority/navigation Candidate: when migrating from nested responsive disclosures to a single task-level drawer, remove the obsolete inner state owner and its dependent CSS, not merely hide its control. The visible screen alone does not prove accessible open/close state; test actual focus and `inert` / `aria-hidden` consistency across task changes. **Case-specific corroboration, no automatic Canonical change.**

Boundary: this does not remove the broader legacy inline CSS, solve entire media preview constraints, or constitute physical Android-device acceptance.


## HSR PR #145: CSS layout authority must include the legacy state boundary (2026-10-13)

Source: [HSR PR #145](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/145), exact tested head `019aa1e4923435326e7f69a76bcef0310130e6c4`, squash merged **to main** at `580295045781f602d38a6aa78099eed19387eb4d`. Verified post-merge main tip and final CSS.

Observed defect: simply removing six `!important` grid-placement declarations from `app/static/hsr-ui-convergence.css` made Chromium's 1600px desktop Effects timeline narrower than the existing >400px acceptance requirement. The underlying old inline CSS still imposed a forced three-column grid even when the batch QA rail was collapsed. This confirms that downstream CSS cleanup is ineffective while earlier rules retain unconditional authority.

Fix: restrict legacy multi-column desktop/tablet/mobile layout rules to `.preview-workbench.audit-open` (the explicit QA-open state) and remove competing forced default widths from relevant base/media rules. The final separately loaded CSS governs the **default QA-closed** two-column desktop or single-column tablet layout without those six forced `!important` grid declarations; the explicit QA-open arrangement remains independently reachable. Existing hidden/inert rail safety rules remain enforced. UI tests were updated only where they asserted obsolete literal CSS tokens, not to lower geometric thresholds.

Evidence on exact head:
- [Python/Termux run 38356350753](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38356350753) success, 3.11/3.12/3.13 + Termux Lite
- [Chromium/libass run 38356350609](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38356350609) success, desktop/touch-size geometry, QA interaction and real media regressions.
- Prior failed [Chromium run 38355777244](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38355777244) demonstrated the insufficient-width regression; the failure was **not** ignored.

Reusable observation, overlapping the existing `inbox/candidates/2026-10-10-ui-css-authority-and-native-task-navigation.md`: removing `!important` from downstream CSS does not transfer layout authority if upstream declarations remain forced and improperly scoped to a closed/open UI state. The safe remediation is to scope old ownership to the state that actually needs it, then verify both states with computed browser geometry. One project occurrence is not sufficient for Canonical promotion. Remaining historic inline CSS debt, full UI refactor and Android physical-device verification are not completed.


## HSR PR #151: actual editable-track archival MKV, not black video with external subtitles (2026-10-13)

User-originated product connection: HSR Voice Archive Builder's continuous FLAC and ASS rendering artifacts can be composed as one Matroska deliverable, paralleling the softmux product's *container first* model. The previous `BlackVideoExporter` deliberately produced only H.264 black track + FLAC and reported `subtitles_embedded: false`; it was not a complete subtitle artifact.

Source [HSR PR #151](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/151) exact PR head `e05057ad3fe1bd437e6cbc942ebdb21d281f3efe`, squash merged to **main** at `3673349d03a129ca98e4012d1b9186790c91f778`, main tip verified.

Delivered distinct `HSR_Voice_Archive_Bundle.mkv` (old Black MKV remains):
- Project `continuous.flac` mapped directly and copied as FLAC audio stream
- Actual separately selectable `HSR_Voice_Archive.ass` subtitle stream, `-c:s ass`, **not hardburned**
- Actual H.264 background video track, user-defined #RRGGBB, or ephemeral bounded PNG/JPEG/WebP picture with scale/pad
- Explicit user choice to attach SFNT project-imported TTF/OTF/TTC files as Matroska attachments with MIME. Attachments are from the project's validated `subtitle_fonts` only; default player behavior is not guaranteed across devices, font redistribution rights stay with user
- Dedicated FastAPI + Termux Lite job routes, project-root guard, 8 MiB body boundary, max 4 MiB image payload, FFprobe dimensions bound, temp/atomic publication
- FFprobe acceptance **before publication** requires exactly one video, FLAC audio, ASS subtitle, specified attachment count and MIME, duration bounded to original audio; status and new finished-output card accessible in UI
- Rebuilding `continuous.flac` invalidates previous complete MKV; build rollback preserves previously published bundle
- Background picture is a real decoded video image, not CSS-only stage paint; user's original request for long-form effects-encoded footage is a separate unimplemented capability

Exact-head success:
- [Python 3.11/3.12/3.13 + Termux Lite workflow #38368898712](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38368898712)
- [Chromium/layout/libass + real MKV FFmpeg/FFprobe workflow #38368898708](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38368898708)
- New `tests/test_archive_bundle_exporter.py`: generate real 1.6-second FLAC+ASS+optional installed DejaVu font, verify Matroska stream codecs/attachment count/duration, and independently FFmpeg-decode center video pixel from uploaded red PNG background.

Scope / non-claims: This outputs a still background video (1 fps by default) with selectable dynamic ASS subtitles. It does not provide all-project hardburn of effect animations, multi-audio-language tracks, or chapter metadata. Physical Android/multiple media player attachment-font compatibility is not established. Font import, word-alignment controls and viewport/touch-slider fixes preexisted this PR and should not be falsely credited to it.

Intake duplication: Existing `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` covers MKV as composition; `inbox/candidates/2026-10-02-media-format-support-is-a-compatibility-relation.md` covers format semantics. Add case-specific independent evidence here rather than duplicate Candidate or automatically change Canonical. Generalizable constraint: a container-export UI must distinguish *hardburn* from *soft subtitle tracks*, validate stream types and attachment MIME independently, and preserve source artifacts and publication atomicity.


## HSR mainline PR #152: user background image becomes genuine dynamic ASS video source (2026-10-13)

Source: [HSR PR #152](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/152), exact test head `1f14e8e2ab5f8d6b2a8563e392bbfc4aeb434bc9`, merged to main `b7a5e6581bd1cd6be80366ac86a77dd9cc900b48` (main tip and renderer verified after merge).

Problem clarified via current main: previous HSR releases had project font import, mobile touch-slider pointer locks, viewport scroll panes, word-alignment JSON and local generation, and a full MKV output bundler. Those features should not be reimplemented as if missing. But the *user-provided still image* was limited to browser geometry staging and already supported in MKV export: the **actual short FFmpeg/libass playable effects preview** accepted only color or local motion video. UI also described video results as black/silent even when a nonblack solid color or source audio was selected.

Implemented:
- Effects can upload PNG, JPEG or WebP up to **4 MiB** as an alternative source for a genuine 0.5–8 s video preview. Local video takes precedence, else user image, else solid color.
- Reused the MKV bundler's bounded base64/magic validation, then FFprobe image dimensions (16–3840 by 16–2160), FFmpeg image loop at 24 fps, aspect-preserving scale+pad, real libass ASS overlays; input temporary and not copied into project storage. Both FastAPI and Termux Lite implement the same source/provenance contract. Source video and background image are mutually exclusive inside renderer.
- Browser validates returned `X-HSR-Preview-Background: background-image` where applicable, identifies real playable output, and avoids the former blanket claims of black backgrounds or always-silent video.
- New real FFmpeg test synthesizes PNG, renders MP4 with libass, FFprobes video dimensions/duration and decodes RGB to verify a colorful image-backed result. Additional direct renderer/API and checked-out Chromium UI tests cover source selection and exclusion.

Exact-head green evidence:
- [Python 3.11/3.12/3.13 + Termux Lite #38370835603](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38370835603)
- [Chromium / real FastAPI-libass and actual image FFmpeg proof #38370835538](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38370835538)

Reusable observation: **a selected preview background in DOM/CSS is not evidence that exported or renderer-produced media contains that source**. Test the actual container's decoded pixels, API source provenance, and frontend data path as separate obligations. This is additive to existing HSR Observation / preview case; not a new candidate and does not modify Canonical. Physical Android and long-form media processing remain unverified.


## 2026-10-14 HSR full-branch audit and draft resolution (Observation, not acceptance)

- Current HSR branch inventory at [`.uigs/tasks/hsr-branches-20261014.json`](https://github.com/11576865/HSR-Voice-Archive-Builder/blob/main/.uigs/tasks/hsr-branches-20261014.json) records **109 remote refs**. Every one of the **108 non-main refs** returned Git `diverged` relative to the audited main `6e370850`. This topology is **not a count of missing features** because prior PRs were re-landed, squash-merged, or targeted another feature branch.
- Audit chain `feat/hsr-layout-safety-ratio-karaoke-preview` (180 ahead / 85 behind main) is a direct ancestor of `feat/hsr-archive-audit-karaoke-v1` (181 ahead / 85 behind). The latter still contains substantive modules absent from main (`archive_audit.py`, `ass_coverage_batches.py`, `ass_coverage_lock.py`, `ass_export_sampling.py`). A separate overlapping `feat/subtitle-style-workbench-evidence-v15` had 155 ahead / 85 behind. This is **pending integration**, not grounds to claim feature completion or delete refs. [Draft PR #159](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/159) makes the cluster visible; at creation GitHub reported `mergeable=false`.
- [Draft PR #150](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/150) was closed **unmerged and superseded**, because current main already has 16 MiB PNG/JPEG/WebP real image-backed FFmpeg/libass preview instead of the draft's older 6 MiB PNG/JPEG path. A distinct real-video-image regression, evidence state and clear control were re-landed in `c657027`, `a6d525`, `3b9fe86`. The new exact-head CI remains Pending; closure does not imply final production acceptance.
- Scope boundary: `uigs-outbox` is an operational ref and `v0.*` branches are historical provenance, not default source for forced merges. Real Android player/font/banding/long-duration validation remains [Issue #158](https://github.com/11576865/HSR-Voice-Archive-Builder/issues/158) FIELD-PENDING.

Deduplication: existing Foundry Candidates `2026-10-04-replay-stale-feature-branch-as-semantic-delta.md`, `2026-10-04-rebuild-stale-feature-on-current-main.md`, and branch hygiene Tests already capture the general rule. This is **product-specific Observation evidence only**, not a new generic Candidate, new Canonical rule, or a claim all 109 branches are complete.
