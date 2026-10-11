# Candidate: lightweight multi-range queue for repeated Stream Copy cutting

Date: 2026-10-11
Status: **Design proposal / not implemented / not user-approved**
Origin: QHE Studio v3 follow-up conversation on whether one video can yield multiple clips without making the workflow complex.
Project: `11576865/Quick-Automatic-Hardsub-Encoder`
Scope: Interaction/design option only; no product code change or test evidence.

## Problem and bounded proposed approach

Current QHE Stream Copy is oriented around one IN/OUT interval per execution. The same source video can be cut repeatedly into independently saved clips without reimporting the source. For occasional two-cut use, that path is adequate. For multiple repeated cuts, manual changes plus separate exports become repetitive.

Proposed **optional** improvement: preserve the one-clip path and add a lightweight queue:
1. Set IN/OUT and choose `加入片段`.
2. Show a short list of interval items, with edit/delete, duration, and predictable filenames.
3. `导出全部` produces **separate files** for each interval; never silently concatenates them.

A compact `剪下一段` continuation after save is the smaller first step if batch demand is low. Avoid multitrack editing, composite timelines, unnecessary project documents, and additional work modes until actual task evidence supports them.

## Important semantics

Stream Copy may snap its actual cut-in to a keyframe preceding the requested IN time; each queued item should expose requested vs actual cut-in where probe/verification allows it. Do not label keyframe-limited copy as frame-exact cutting. Existing independent audio/video timing and output verification rules remain authoritative. No automatic transcoding may be hidden behind a claimed lossless action.

## UIGS intake

Search for `multi segment batch export clip queue`, `multi range stream copy UX`, `无损剪切 片段 队列`, and `batch clip intervals timeline` did not return a direct duplicate; adjacent intake metadata candidate was unrelated. This is a **single conversational design proposal**, not observed usability evidence or a Canonical requirement. Do not promote to Canonical without usage observation, interaction design review, implementation and browser/native acceptance.


## Product implementation checkpoint — QHE PR #99

2026-10-11: Proposal advanced to **implemented on an open product PR, but not accepted/merged**. QHE PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/99, code checkpoint `4267293a7f814c91ec354053eca40d57a109b4a7`, bookkeeping `ae2bd9e16557028021bd7980d5ba53f109cc79b9`. Still a Candidate, not a Canonical rule.

Actual production implementation now includes the optional Stream Copy range queue in `src/media-workspace.js`: add/load/remove/clear IN/OUT ranges; source identity invalidation; per-clip independent compileTask schema-v4 calls; unique output names; sequential execution through the existing Web/Native executor; waiting for **jobId-matched Native export result** (not merely an export request) before proceeding to the next clip; refusal of mismatched full-range audio/subtitle stream policies and unsaved prior result override; stop and retry semantics. `src/clip-queue.js` provides bounded pure range parsing and filenames. CSS `src/media-workspace-ui.css` owns its visual presentation.

Acceptance strategy: Node `src/clip-queue.test.mjs` plus Playwright source readiness, Copy-only queue, duplicate rejection, two range plans, unique filenames, Native result acknowledgment fence. Existing one-clip flow preserved by design. Latest-head frontend/Windows/UIGS CI, screenshots and physical Android SAF / Native dialog acceptance **Pending External Validation**; no product quality claim until evidence. External screens/FFmpeg GPU remain separate.

Reusability hypothesis: model repeated sub-ranges as independent sequential tasks, preserve source identity, and explicitly fence asynchronous export confirmation between tasks. This is not sufficient for Canonical promotion without repeat observations and field acceptance.


### First CI regression and test-contract repair

PR #99 first post-checkpoint Frontend run `38140978460` failed in `src/studio-v3.test.mjs` before Playwright because the existing source contract required the `mediaInfoListener` declaration to contain exactly the original three functions. The implementation had correctly added `clearClipQueueOnSourceChange()` and `syncClipQueue()` to the same listener. The source test was too brittle; browser/runtime acceptance was **not reached**.

A single bounded repair `bf9db1e877aa005378f134f2c57f2e8e63b104cb` replaces that exact-function-body regular expression with a contract that still requires `syncTaskActions()`, source invalidation and clip list refresh, but does not prohibit new correct work. Latest repair-head CI, actual export behavior and screenshot review remain **Pending External Validation**. No merge and no Canonical promotion.


### Browser queue evidence and Native CI trigger expansion

PR #99: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/99. Implementation fix `a635c66fcec2df58baeabff419492a00d0b6bf49` addressed a real Playwright test-isolate `previousRuns` scope error by explicitly passing the value into `page.evaluate`, and reserved batch ownership **before** asynchronous media preparation to prevent duplicate starts or mode switching during Native preparation. Frontend/Playwright workflow `38141977192` and UIGS `38141977202` completed **success** on that exact head. The smoke covered distinct Stream Copy clip ranges and output filenames, plus waiting for first Native export result before next task.

Actual browser capture artifact `11702799151` from `38141977192` was downloaded and visually examined, including `media-workspace-copy-segment-queue-390.png` (390px wide). It shows two queued intervals `0:00 → 2:05` and `2:10 → 2:15`, each with duration and controls, followed by a single `导出全部` action. No horizontal queue overflow apparent in the evidence; this is **browser** visual evidence, not an Android device acceptance.

Windows local smoke was not originally triggered by changes to `src/media-workspace.js`/`src/clip-queue.js`, even though batch logic interacts with Native export. Head `4bcd835d762ac9d18a38f5eea6884a8fc803bb23` expands Windows smoke path filters and UIGS visual capture dependency to cover those modules. **That latest head's** Frontend, Windows smoke and UIGS runs must all complete successfully before PR merge. Visual validation and prior-head green CI must not be represented as latest-head completion. Physical Windows/Android Native save-dialog field validation is still Pending. No Canonical change.


### Accepted product implementation — PR #99 merged

2026-10-11: **Product-side CI/browser acceptance completed**, but physical Native field acceptance remains pending. QHE PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/99 was merged as `6a7820560caf0eaac11b11c53f384718625f7015` from exact head `4bcd835d762ac9d18a38f5eea6884a8fc803bb23`; QHE task checkpoint `2c4ee1db6513a9778a6a4b08228cc9b93088b910` closes the previous engineering Pending entries.

Exact final feature head successfully completed Frontend/Playwright `38142116055`, Windows local smoke `38142116010`, and UIGS Evidence Coverage `38142116077`. The prior green Frontend head `a635c66fcec2df58baeabff419492a00d0b6bf49` produced the actual 390px two-segment queue screenshot, archive artifact `11702799151`, which was extracted and reviewed. The final-head delta adds Windows path triggers and visual capture dependencies; it does not alter the queue UI or backend execution. The actual browser workflow verifies two distinct compiled copy-only ranges, distinct filenames, and serial Native export acknowledgement blocking the second job.

Boundaries: the browser-based Native export test uses a simulated event and **does not** establish physical Windows Native save-dialog or Android SAF batch export success; field acceptance is **Pending**. Actual keyframe-cut correctness across long videos and real GPU/HDR/VFR also remain pending. The implementation is now merged, but this **Candidate** is *not* promoted to Canonical from one product experience. Update only after additional observations/evidence.


### In-place queued clip edit (QHE PR #101)

2026-10-12. Intake result: **new source-backed UX defect / bounded product fix committed / latest-head CI Pending**. QHE PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/101, source head `dbfad1bc0c7f841fe794ff2920da92eaad770dc2`.

The original multi-clip queue displayed a `载入` control that copied a row's IN/OUT into the live inputs. However the primary button remained `加入片段`, which unconditionally appended a new row. This meant users could not edit an existing unsaved row in place despite the apparent row-edit affordance. The issue was confirmed by reading the real source and browser test flow; it is not a physical device observation.

Product fix: unsaved rows now show `编辑`; the selected row is visually marked, the primary action becomes `更新片段`, and explicit `取消编辑` leaves the original unchanged. Modifying a row replaces the same interval and restores `queued` state, with duplicate detection excluding only that row. Delete/clear/source-change and Copy mode exit invalidate selection safely. During a pending edit, `导出全部` is disabled. Already exported rows show `复用` and can only create an additional independent clip; their saved output status is immutable. Screen-reader button accessible labels identify row indices. Browser regression verifies the updated first range reaches the actual compiler and that cancelling another edit and reusing a saved interval preserve the original row state.

**Validation pending on exact PR #101 head**: Frontend/Playwright, Windows local smoke, UIGS and actual 390px screenshot. This Candidate is not a Canonical rule. Physical Android SAF/Windows Native UI export dialog field validation remains separately pending; no new device evidence.


### PR #101 exact-head acceptance and merge closure

2026-10-12: QHE's **in-place queued-clip editing** repair (previous Pending) is now verified and merged. Product PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/101 exact source head `dbfad1bc0c7f841fe794ff2920da92eaad770dc2` passed Frontend/Playwright `38159643466`, Windows local smoke `38159643480` and UIGS Evidence Coverage `38159643511`. Merge commit `7dd5e12791a5dc27b2706c68f663da1b7abe988a`, QHE main checkpoint `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`.

The actual 390px Chromium queue screenshot, `media-workspace-copy-segment-queue-390.png` in artifact `11709509544`, was extracted and reviewed. The first requested interval changed **in-place** from 0:00–2:05 to 0:00–2:04, the second remained 2:10–2:15, and the list stayed at two rows. Playwright additionally established edit cancellation preserved original row data, the revised IN/OUT reaches the compiled copy task, exported rows remain immutable when ranges are re-used, and prior Native mocked-save failure/retry did not re-encode.

The product repair is accepted at exact-head **browser+CI level**. It does **not** demonstrate physical Windows Native or Android SAF file-dialog behavior, keyframe-boundary accuracy across real videos, or long-form GPU/HDR/VFR field tests. Those remain FIELD-PENDING. This is still a **Candidate** / source-backed Case-level insight, not an automatically promoted Canonical requirement.


### PR #102 observed phone queue reachability

Date: 2026-10-12. Status: **Browser-observed layout problem; targeted product correction committed, CI Pending**. Product PR https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/102, source head `3df7c7cccba494ace858a31f4d97847d9e350111`.

The prior, actually captured PR #101 390px tall Chromium screenshot `media-workspace-copy-segment-queue-390.png` (artifact `11709509544`) showed IN/OUT at the very top of the workbench and the queued clip list below the expanded audio waveform, keyframe preview and two separate frame images, approximately 1,500+ vertical pixels away. For the task “set range → add a second/third clip”, that long control-to-result distance introduces repeated scrolling and hides the batch concept even though the feature itself passes all previous automated function tests. This is a **separate UI placement / task proximity defect**, not another task-engine bug.

Bounded design change: reparent the *same* queue panel beside IN/OUT (ahead of the optional advanced timeline), preserving all original buttons/event ownership and single-clip path; increase visible queue buttons to minimum 44px and add real Chromium geometry tests for 390px mode plus 320px/24px-root-font (150% root scaling) with horizontal overflow and button hit-target checks. The test captures a new 320px queue screenshot. The 24px root simulation cannot substitute for physical Android OS scaling, touch, accessibility, or SAF export acceptance.

Latest-head Frontend/Playwright, Windows smoke, UIGS CI and actual changed screenshot **Pending External Validation**; do not merge if red. This is a Candidate/Case-level example of reducing interaction distance between a primary input and its task action, not a new Canonical rule.
