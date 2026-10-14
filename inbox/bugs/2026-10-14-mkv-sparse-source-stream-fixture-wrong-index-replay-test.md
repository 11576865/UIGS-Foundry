# Bug: Sparse source-stream recovery test selected an attachment index as audio

Date: 2026-10-14  
Status: **one bounded test-only repair submitted; new exact-head CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#132](https://github.com/11576865/MKV-Fast-Muxer/pull/132)  
First failed head: `b2a9e32faed85e1174f60aeea592d815d21bd301`  
Node CI failure: [Browser E2E workflow 38507704778](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38507704778), Node test stage (Build/Chromium skipped). Also caused Pages Test stage failure in run `38507704961`.

## Exact evidence

`tests/container-project-restore.test.mjs` created two real source audio tracks with **sparse indices 1 and 6**, plus separate source attachments including `index=4`. The test verifying a portable source-order permutation at line 419 then mistakenly selected:
```js
const second = state.tracks.find(t => t.index === 4);
[first.order, second.order] = [second.order, first.order];
```
`second` was undefined. The node:test log identified `TypeError: Cannot read properties of undefined (reading 'order')` at line 420. This is a test fixture lookup regression **before the actual production source-order export/replay flow executed**, not proof that the implementation was defective. The other newly added source-order rejection and final-commit tests (subtests 196–198) passed.

## Bounded repair and status

Changed the stale test lookup to **index 6**, matching the second actual source audio object; no production logic or general writer safety changed. Commit: `513a0535cf51f7cf231a50f06f9f743d3011786a`.

The new exact-head Node/build/Chromium CI is **Pending**; do not relabel the whole PR green based on this correction alone. Do not automatically retry the entire test suite repeatedly.

## Reusable observation

When a container-test fixture intentionally uses sparse `ffprobe` indices to expose bad assumptions about order versus stream identity, every accessor must match **both stream kind and actual source index**. Avoid hard-coded stale numbers and use explicit fixture selectors/assertions before exercising behavior. Fixture admission errors should be separated from product-path output validation.

This Bug complements existing `inbox/cases/2026-10-14-mkv-verified-source-track-order-permutation-sparse-executor-mapping.md` and is **not** a Canonical policy change.
