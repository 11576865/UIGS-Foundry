# Case: HSR focused workspace usability follow-up (PR #153)

Date: 2026-10-13
Level: Case / implementation and test proposal (not Canonical)
Product: `11576865/HSR-Voice-Archive-Builder`
Source PR: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/153
Source head at intake: `c4d2b45a92856d9d5325b59206ae2251360746f2`
Status: Draft / exact-head CI pending; physical touch-device validation pending.

## Concrete report and root-scope distinction

The user reported repeated browser page scrolling, accidental parameter changes while scrolling, hard-to-discover project font import, and uninformative media preview. Recent mainline implementations already provide project TTF/OTF/TTC upload, FFmpeg/libass effect video, optional word alignment, and a complete MKV with FLAC/ASS/attached fonts. Capability presence is not evidence that a user can readily find, manipulate and validate it.

Earlier HSR draft PR #149 proposed an optional fullscreen Layout/Effects viewport but diverged from main. Rebuilding that UI behavior on current main avoids discarding subsequent background-image and archive-MKV fixes.

## Proposed implemented behavior in #153

- Layout and Effects open in a bounded, fixed-viewport editor by default rather than leaving the browser document as the main scroll surface. Escape or an explicit top action exits; within the focus viewport, task-local buttons reuse the existing `showWorkspace` logic.
- Coarse-pointer range controls are locked by default for scroll safety. The original Inspector lock is extended to the timeline range control and a single touch pointerup/pointercancel re-locks the active adjustment. The lock control resides at the top rather than below many scrollable controls.
- One visible `导入字体` shortcut routes to the existing project-scoped font importer. It does not create a second font store.
- When switching Layout QA to Effects, keyboard focus moves to a visible task control, not a hidden primary nav button under the focused overlay.
- Source/Chromium regressions cover desktop 1600×900, tablet 768×1024, mobile 390×844, real browser UI geometry, Escape, task switch, font importer disclosure and coarse pointer lock semantics.

## Evidence boundary

Code submitted in Draft PR #153. At intake the two workflow runs were started/queued; success must be checked at exact head. The browser tests use fixture media, and CI cannot prove every Android browser's real touch gesture or all device-specific viewport behavior. No effect renderer, word alignment, FLAC, ASS, MKV or font file storage backend was changed here.

## Reuse and deduplication

This case extends the existing HSR observation `inbox/observations/2026-10-13-hsr-subtitle-requirement-to-mainline-preview-gap.md` (which records user requirement versus implementation and the first user feedback). It does not duplicate its broad product assessment. It focuses on a concrete testable implementation where a task viewport, gesture arming and recovery action must be demonstrated together. Related MKV UI discoverability Candidate and CSS authority Candidate remain unchanged.

No Canonical promotion is justified by a single project or pending workflow.

## Exact-head automated verification follow-up (2026-10-13)

PR #153 commit `a61d64f1025de7b0869d6453bd29b25c1bc9ef00` passed:
- Python/Termux workflow: https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38375165253
- Chromium UI / actual libass / archive MKV workflow: https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38375165418

Before success, first Chromium failure was an obsolete assertion locating the *global* Layout/Effects nav above the fullscreen editor; it was corrected to assert the actual visible focused task nav. A later production-CSP Chromium test tried clicking a global nav element covered by the focused stage, correctly timing out. It was changed to click the visible in-workbench task switch rather than bypassing hit-testing. Both failures demonstrate test/interaction alignment, not a media codec defect.

Tests included real FFmpeg/libass and complex archival bundle checks, but this does not constitute physical Android swipe behavior, accessibility study or long-term user acceptance. Remains Draft/Unmerged pending design and device review. The Canonical system is unchanged.


## User-facing effect-feedback and alignment-onboarding follow-up (2026-10-13)

Branch: `fix/hsr-viewport-and-gesture-workbench-20261013`, PR #153, tested head `e4cbb271e4b38302a4832dee164d54a3cd18344f`.

The user reported an inert effects preview and unclear Karaoke prerequisite file. Inspection showed the real preview already generates encoded video, but its primary status and missing Word-Level Alignment controls were buried in the scrolling Inspector or collapsed advanced detail. The new change reuses the existing controls/IDs and backend, surfacing alignment diagnostic/generation/JSON import directly in Effects rather than cloning state; it also displays progress at the stage with distinct preparing / FFmpeg encoding / browser decoding / decoder-confirmed ready / stale / failure states. Audio/subtitle/MKV encoders are unchanged.

Source and Chromium regressions assert one owner for each alignment control, visible generation and upload, disabled local generate when WhisperX unavailable, decoded success rather than HTTP success, and automatic stale-state presentation after background changes. Exact-head green evidence:
- Python/Termux: https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38385948013
- Chromium and real FFmpeg/libass / MKV: https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38385947838

**Reusable bounded observation:** A media button's backend completion and a file import's existence do not prove *task-local operation comprehension*. Provenance/phase and prerequisites must be accessible at the affected canvas/action without declaring a playable artifact before browser decoding or fabricating missing timing. Reuse the existing case; no Canonical promotion. Still pending: physical Android UI/device review and merge of PR #153.


## Mainline integration and superseded draft resolution

PR [#153](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/153) was promoted from Draft and squash-merged **directly into main** as `5af422cd3fd4c7c2857cd62a13a3cd5b614ea660`. GitHub postmerge metadata: `merged=true`; comparing the merge SHA to `main` returned `identical`. Production HTML on main contains the visible Karaoke control group. Source exact-head Python/Termux and real Chromium/libass/MKV suites were green before merge.

Older optional-focus PR [#149](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/149) remained a divergent Draft, then was closed **without merge** as superseded. No orphaned alternative focus workflow is being treated as authoritative. The implementation now delivered is the default viewport-first task surface with project font import and honest effects/Karaoke status.

**Evidence boundary remains:** automated browser viewports and real media tests are not physical Android-device validation. User-reported improvement is not yet confirmed by new user field observation. Do not promote Canonical.
