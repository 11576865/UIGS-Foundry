# Bug: Playwright in-memory file injection prevents large-source browser E2E from reaching production logic

Date: 2026-10-14  
Status: **repair submitted, exact-head rerun Pending**  
Product: `11576865/MKV-Fast-Muxer` PR [#126](https://github.com/11576865/MKV-Fast-Muxer/pull/126)  
First failed run: [Browser E2E #38450948443](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38450948443), job `115481383133`

## Failure evidence

The first PR #126 run completed Node tests and Vite build successfully, but full Chromium test exited during `scenarioStreamedSourceDigestBrowser` before hashing its 65 MiB input. The GitHub Actions log reported: `Error: Cannot set buffer larger than 50Mb, please write it to a file and pass its path instead.`

The E2E scenario created a 65 MiB `Buffer` and passed it through `page.setInputFiles('#videoInput', { name, mimeType, buffer })`. That API path has a 50 MB in-memory buffer limit. A failing browser job therefore provided **no evidence that production incremental SHA-256 or its UI flow was defective**.

## Repair

Write the same test bytes to `.e2e/output/large-source.mp4` first using `fs.writeFile`, then call `page.setInputFiles('#videoInput', largeSourcePath)`. Independently derive the expected SHA-256 with Node `crypto`; keep browser export/import, source byte identity and lack of implicit mux assertions. E2E JS syntax and fixture path transformation were locally inspected after this change.

The repair is committed to PR #126 at `1ce5fc4f6647a18436282d47faa70e5ebf093cd5`. The durable task-state update follows on the same branch. **New exact-head Chromium CI remains Pending** and must not be represented as passing.

## Reusable learning / dedup

When testing file sizes larger than ordinary browser automation fixture budgets, distinguish a transport/fixture admission failure from a product path failure. Use on-disk or streamed fixtures rather than test-harness in-memory file injection where the harness has explicit buffer caps. Assert that the intended product operation was actually reached before declaring feature coverage.

This is scoped as a Bug rather than a Canonical rule. Foundry already holds `governance/AGENT-EXECUTION.md` describing bounded repair generations and asynchronous CI; this record adds a concrete test-fixture failure mode, not another copy of that policy.
