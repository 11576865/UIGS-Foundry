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
