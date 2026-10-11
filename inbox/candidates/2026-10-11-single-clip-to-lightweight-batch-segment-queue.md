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
