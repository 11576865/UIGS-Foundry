# Candidate: Long-running task UIs must make stage, progress, and completion handoff explicit

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, operations, reliability
Evidence type: direct user workflow observation

## Summary

A long-running operation is not usable merely because it can be started, runs in the background, and eventually reports success.

The UI must preserve a legible task model across three moments:

1. **Before start** — the user can understand the chosen intent/preset without having to interpret the raw execution command.
2. **While running** — the UI exposes enough observable progress to answer "is it still working, how far along is it, and what is happening now?"
3. **After verified completion** — the next required user action is promoted in place and clearly distinguishes "verified temporary artifact" from "saved/published final artifact."

## Evidence

In Quick-Automatic-Hardsub-Encoder on Windows Native, a real user workflow on 2026-10-02 showed all three failure modes in one task:

- the encoding parameter stage remained difficult to understand despite the intended preset/intent redesign;
- while encoding, the visible state was essentially `encoding • 实际起点 0.000 秒` plus a progress bar, without enough readable progress context for the user to judge advancement;
- after processing completed and the artifact was reported as verified, the user had difficulty locating the `保存成品` action;
- the subsequent save/publish attempt failed in the Windows Native layer with PowerShell reporting that no `op_Subtraction` overload with two arguments could be found.

The encode/verification result and the final save/publish result were therefore different states and must not be collapsed into one generic "completed" state.

## Candidate rule

For long-running user tasks:

- before start, make the selected user intent and effective plan understandable without requiring raw command-line interpretation;
- raw FFmpeg / shell command text belongs to diagnostics or an explicitly expanded technical view, not the primary decision surface;
- while running, show a compact but sufficient progress model: current stage, progress fraction or processed/total media time when available, elapsed time, processing speed when meaningful, and cancellation state;
- never fabricate ETA when evidence is insufficient;
- after verify-then-publish workflows, distinguish at least:
  - processing;
  - processed / verifying;
  - verified but not yet published/saved;
  - published/saved;
  - publish/save failed while verified staging remains recoverable (when true);
- when only one next action is required after completion, promote it as the primary contextual action instead of leaving it in the previous multi-action toolbar;
- a publish/save failure after successful processing must not force a re-encode unless the staged artifact is actually invalid or unavailable;
- post-completion errors must be shown next to the completion/publish action, with technical detail available separately.

## Scope

Applies to encoding, rendering, export, build, deployment, model inference, archive generation, and similar multi-stage long-running tasks.

## Provenance

- source project: `Quick-Automatic-Hardsub-Encoder`
- source: direct user screenshots and workflow report, 2026-10-02
- evidence level: direct user-observed usability failure plus visible runtime error
- related existing Foundry patterns: `REL.SINGLE_OWNER_LONG_JOB`, `REL.VERIFY_THEN_PUBLISH`

This is a Candidate only. It is not Canonical.
