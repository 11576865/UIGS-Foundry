# Observation: CI setup must validate the Python API actually used by media fixtures

Date: 2026-10-11
Status: **Observed CI setup defect, repair submitted; latest E2E Pending**
Source: https://github.com/11576865/MKV-Fast-Muxer/pull/73
Failed workflow: https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38120088550

## Direct observation

To reduce repeated Playwright Chromium downloads in the PR #73 UI E2E
workflow, the runner was changed to prefer its installed Google Chrome
using the test's existing `E2E_BROWSER_EXECUTABLE` path and provision
missing FFmpeg/font tools only if necessary.

The revised setup **correctly detected** `/usr/bin/google-chrome` and
successfully completed apt installation of `ffmpeg` and
`python3-fonttools`. The setup step nevertheless failed with exit code
1 at its final `command -v pyftsubset` check: the command was absent.
No Node/browser product tests ran in that workflow.

The actual repository fixture generator
`tests/e2e/generate-fixtures.sh` imports
`from fontTools.ttLib import TTCollection, TTFont` through a
configurable `E2E_PYTHON`. It does **not** invoke `pyftsubset`.

## Repair

Validate `/usr/bin/python3 -c 'from fontTools.ttLib import TTFont,
TTCollection'` as the dependency contract, and set
`E2E_PYTHON=/usr/bin/python3` for the real fixture process. Retain the
existing `google-chrome` / `chromium` fast path and Playwright install
fallback. A Node regression asserts the workflow checks the module
rather than an unused binary.

Source head when recorded: `3fc63dcf5725d4c0cd10a466158710460b0ccdc1`.
Corrected Chromium/FFmpeg/actual media-E2E CI was **Pending**; do not
represent setup checks, source assertions, or a Pages build as proof of
successful browser mux.

## Reusable distinction

Use the **same interpreter, library import and executable** in dependency
preflight that the subsequent test actually runs. An unrelated CLI
availability check can reject an otherwise capable environment,
particularly when distribution and pip packaging expose different
entrypoints. This is a single-repository observed bug, not a change to
Canonical UIGS reliability policy.
