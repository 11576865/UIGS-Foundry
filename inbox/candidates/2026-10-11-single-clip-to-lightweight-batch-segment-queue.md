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
