# Candidate: Shared product shells must keep the active execution runtime visible

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, runtime-state, cross-platform, user-trust
Evidence type: user-visible ambiguity plus implemented runtime-state presentation

## Summary

Different execution backends may legitimately share one product UI, but semantic parity does not imply that runtime identity should disappear.

When Web/WASM, a localhost native bridge and a mobile native service have materially different execution limits, file access, accelerators or failure modes, the active runtime should remain visible in persistent application chrome.

An introductory paragraph or a backend detail buried in diagnostics is insufficient if the rest of the interface is visually indistinguishable.

## Observed case

Quick-Automatic-Hardsub-Encoder intentionally shares the same media workbench across Web, Windows Native and Android Native. Users still need to know which executor currently owns the task because the backends differ in:

- file selection and size constraints;
- system FFmpeg/FFprobe vs WebAssembly/FFmpegKit;
- NVENC availability;
- Native job persistence and local Bridge lifecycle.

Before PR #41, Windows Native could look almost identical to Web apart from title/introductory copy. PR #41 now establishes a persistent runtime identity layer:

- the workbench title and kicker name the runtime;
- the header status names Web/WASM, Windows Native or Android Native;
- a persistent runtime banner explains the execution substrate;
- semantic `body[data-runtime-backend]` state drives runtime-specific chrome;
- Windows Native uses a distinct engine accent while retaining the same business workflow.

The Playwright smoke verifies both the Web label and a simulated Windows Native page across refresh, and captures a Windows Native visual artifact.

## Candidate rule

For a shared UI spanning materially different runtimes:

- share task semantics and workflow where possible;
- expose runtime identity as persistent state, not a transient onboarding message;
- place the identity in stable chrome visible before deep diagnostics;
- describe only differences that materially affect execution or user expectations;
- avoid forking the entire business UI merely to make runtime identity visible;
- expose a semantic runtime state to CSS/tests so presentation cannot drift independently from actual backend selection;
- include at least one visual/behavioral test for each materially distinct runtime presentation.

## Relationship to existing UIGS knowledge

This is compatible with the existing experimental-presentation capability-asymmetry Candidate: semantic parity can remain mandatory while presentation details differ where capabilities or operating context differ.

This Candidate is specifically about preserving user-visible execution identity inside a shared shell.

This is a Candidate only. It is not Canonical.
