# Observation: explicit guided-to-manual task intent handoff

Date: 2026-10-13
Status: Observation / local compiler evidence; hosted browser Pending
Source: QHE PR #105 continuation after 428caf4

Dedup: queried inbox/tests/2026-10-13-qhe-heterogeneous-audio-plan-and-source-owned-ui.md. Same source-owned-plan/UI family; this adds a one-way explicit intent reconstruction, not full bidirectional authority or Canonical promotion.

A guided action labelled CPU parameters reconstructs its codec/quality or budget target, preset, dimensions, audio policy and selected container in the existing manual compiler. Software encoding is explicit; native auto-selection and prior calibration are not declared equivalent. Budget is recalculated through per-stream ledger; copy size tasks still need current source measurement. Prior audio overrides, range and manual transforms are reset using mount defaults. Original artifacts remain previous-owned results. Handoff is idle-only, does not execute or validate automatically, and does not transfer measured quality authorization.

Four new pure compiler regressions cover quality, strict budget/two-pass, unsupported intent and copied-cost refusal. Total local Node 222 pass/7 conditional skips; build passes. Browser real-DOM fixture checks no encode, reset audioPlan/start, unchecked projection and subsequent manual validation; local Chromium unavailable, CI Pending. Physical devices, full two-way domain unification and automatic codec/resolution/preset decisions remain open. Previous Android emulator V4D-06 video-end verification failure is separately recorded, not counted as acceptance.


## WU-01 2026-10-14 follow-up — source-bound compiler guard

QHE PR #105 commit dcecd685c0a8096f2a40957facb8eb76121bd14a adds a narrow test-backed safeguard: commitGuidedCpuHandoff now rejects a precompiled contract if its own sourceKey is not the current expectedSourceIdentity, even if the caller and live source agree. It also rejects source changes during the post-apply authoritative compileTask. Regression tests cover both cases.

A new Draft-eligible hosted Ubuntu FFmpeg/libass integration fixture independently checks the source-bound Guided to Manual CPU task compilation, an actual x264 output, ASS presence, dimensions, full video decode, and whether rendering ASS before bicubic scaling differs from reversing the order. At submission the exact-head hosted workflow was in progress; this is **submitted, not yet verified**. No Chromium handoff UI/Windows Native same-task execution or long user video acceptance is claimed.

This is a follow-up to the same Guided-to-Manual handoff observation, not a separate Canonical rule. Related Candidate: persisted derived evidence must carry all material input dependencies. Scope and confidence remain bounded.
