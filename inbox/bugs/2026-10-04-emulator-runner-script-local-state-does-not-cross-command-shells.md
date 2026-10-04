# Bug: Emulator-runner script commands cannot assume shell-local variables survive command boundaries

Date: 2026-10-04
Status: Bug
Domains: CI, Android emulator, shell execution, workflow reliability

## Symptom

Quick-Automatic-Hardsub-Encoder PR #61 completed its Android instrumentation test successfully, then failed while collecting exported Stream Plan v4 outputs.

The workflow used a runner action script containing separate lines:

- assign `pack=...`;
- assign `outputs=...`;
- later run `mkdir -p "$outputs"`.

The action executed those lines as separate `/usr/bin/sh -c` commands. The shell-local assignments therefore did not exist in the later command, and CI failed with:

`mkdir: cannot create directory ‘’: No such file or directory`

This failure occurred after the emulator test itself had passed.

## Fix

Revision `91aed5d1140ed7a7b1ad0e2c4655cc8498d82c31` removes cross-command shell-local state from the emulator-runner script:

- stable environment variables such as `RUNNER_TEMP` are referenced directly;
- the output-copy `while` compound command is kept on one command line;
- verifier paths are explicit instead of depending on prior shell assignments.

## Reusable rule

When a CI action accepts a "script" string but internally executes commands one-by-one, do not assume ordinary multiline-shell scope.

Before relying on local variables, shell functions, `cd`, `set -e`, traps, or other process-local state:

1. verify whether the action runs the block in one shell process;
2. if not, use stable environment variables / absolute paths directly;
3. keep stateful compound shell logic in one command invocation or move it to a checked-in script;
4. distinguish post-test evidence-collection failures from product/emulator test failures.

## Provenance

- project: `11576865/Quick-Automatic-Hardsub-Encoder`
- PR: #61
- failing workflow: Android Stream Plan v4 emulator runtime acceptance #6
- instrumentation result before workflow failure: BUILD SUCCESSFUL, 1/1 Android test completed
- repair revision: `91aed5d1140ed7a7b1ad0e2c4655cc8498d82c31`
- deduplication: searched Foundry for emulator-runner command-shell / lost shell-local variable guidance; no direct duplicate found

This Bug record is evidence. It is not Canonical.


## Verification

- repaired workflow run: Android Stream Plan v4 emulator runtime acceptance #7 — success
- companion checks: Compile Android media tasks #105 — success; UIGS Evidence Coverage #148 — success
- project PR #61 merged as `abbe9f436ebc9e60942b5a04eaa4c197f02d5762`

The failure is therefore confirmed as workflow command-shell scoping rather than a Stream Plan v4 runtime acceptance failure.
