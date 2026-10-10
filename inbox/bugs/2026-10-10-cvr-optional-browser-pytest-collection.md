# Bug: Optional browser test discovered by default pytest without its dependency

Date: 2026-10-10
Status: Bug / fixed on product PR branch; final CI pending
Lifecycle: validation-pending
Project: 11576865/Character-Voice-Reader

## Observed failure

The Reader's new real-Chromium IndexedDB test was placed in
`tests/test_offline_browser.py`. Its module-level
`from playwright.sync_api import sync_playwright` made normal
`python -m pytest -q` discover and import the optional browser test, even
though Playwright was intentionally installed only in a separate browser CI
workflow. Reader tests run `38023028473` failed during collection with
`ModuleNotFoundError: No module named 'playwright'`.

The separate dedicated Chromium IndexedDB workflow recorded a success for its
earlier test commit; the error was a **test-collection dependency boundary**,
not evidence of an IndexedDB application failure.

## Repair

CVR [PR #12](https://github.com/11576865/Character-Voice-Reader/pull/12),
repair commit `03b7a7da66cd0ab90bd33cd1f1abbeb70cbed9ec`:

- moves the optional Playwright import into the browser test's explicit
  `main()` entry point;
- renames standalone browser checks away from `test_*` so default pytest
  discovery cannot treat them as fixtures-based tests;
- keeps the explicit browser workflow responsible for installing Playwright and
  running the browser suite.

## Candidate reusable lesson / boundary

When a repository runs lightweight default pytest plus a separate expensive
browser suite, do not make default collection import optional browser
dependencies. Either isolate discovery by filename/directory/configuration
or guard optional imports and test names so only the specialized workflow runs
them. Adding a browser test without preserving the default CI discovery
boundary can make an otherwise healthy product PR red at collection time.

## Evidence

- Actual Reader tests CI failure: https://github.com/11576865/Character-Voice-Reader/actions/runs/38023028473
- Product repair commit as above
- Post-repair Reader and Chromium CI: **Pending** at intake
- Dedup: searched Foundry for pytest, Playwright, optional dependency and test
  discovery equivalents; no direct matching bug record found
- This is a project Bug record, not Canonical guidance or proof of full
  device/browser acceptance.
