# Bug · S12 cross-workflow concurrency collision cancels research matrix without verdict

Date: 2026-10-21
Status: **Scoped CI scheduling bug resolved: exact-head five-case research matrix executed; no Canonical change**
Product: `11576865/MKV-Fast-Muxer`
Clean current-main research PR: https://github.com/11576865/MKV-Fast-Muxer/pull/173

## Deduplication
- Related but distinct from `inbox/tests/2026-10-21-softmux-s12-genuine-large-mkv-wasm-envelope-pending.md` which owns the actual test and media geometry; this Bug records the *CI schedule/coordination mechanism*, not a separate media acceptance result.
- Existing branch-boundary/async CI practice concerns when to validate a PR after submitting it; it does not establish independence of two Actions workflow concurrency groups. Search found no exact existing cross-workflow concurrency collision Bug.
- Do not promote a single repository observation into Canonical.

## Actual reproducible incident
- Historical experimental PR #170 remained based on old `main@0.1025` despite product main advancing through 0.1027. GitHub [PR #170](https://github.com/11576865/MKV-Fast-Muxer/pull/170) reported `mergeable=false` and comparison main→head had 29 ahead / 2 behind commits including stale production files. Its newest five-case matrix `9adf653f25d9c274818f543db16274d7e07cb827` exposed no discoverable PR workflow run; this absence was correctly recorded as **no verdict**, not acceptance.
- To isolate this from merge conflicts, created clean [PR #173](https://github.com/11576865/MKV-Fast-Muxer/pull/173) on current `main@585f4e8e8473e09d0a4c7fa63d66368d9a9f9870`, containing only actual fixture generator, E2E, and research Actions workflow. GitHub subsequently confirmed this PR `mergeable=true`, compare main→head was exactly 3 changed research/test files.
- Its first Actions [research workflow #39609218661](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39609218661) scheduled all 5 genuine attachment-count matrix jobs, but **all 5 were cancelled before testing**, not failed in FFmpeg/Chromium. The same PR also activated production `S12 scoped real large media acceptance` workflow [#39609218697](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39609218697).
- Root cause confirmed by comparing the two checked-in workflow files: **both configured identical global Actions concurrency group** `s12-real-envelope-${{ github.ref }}-${{ github.event_name }}` and both `cancel-in-progress: true`. Because the concurrency key lacks workflow identity, a different workflow for the same PR ref cancels the research group. GitHub's cancelled jobs reveal no memory or functionality outcome.
- Proposed isolated fix on PR #173 branch commit `ff2b232de811f3100ba9720e6e6c9761b30a79c9`: change **only** research workflow's group to `s12-attachment-cardinality-${{ github.workflow }}-${{ github.ref }}-${{ github.event_name }}`. This prevents collision with the existing production positive acceptance group while retaining legitimate same-workflow supersession for newer heads.
- **Next exact-head CI Pending** at this writing. Do not mark corrected workflow as actually effective until scheduled five-case tests are seen and either complete or present true engine failures.

## Reusable lesson
CI concurrency groups are repository-scoped identifiers, not automatically scoped by workflow name. When independent workflows share a ref and `cancel-in-progress: true`, accidental key reuse can suppress an entire class of evidence. Use distinct workflow identity in groups, distinguish cancelled/never-scheduled from test red, and retain exact SHA/runner evidence for outcomes. This is a scoped Observation/Bug and does not amend Canonical standards.

## Resolution verified

- Moved research workflow concurrency group to `s12-attachment-cardinality-${{ github.workflow }}-${{ github.ref }}-${{ github.event_name }}`, so it cannot collide with production positive workflow's `s12-real-envelope-${{ github.ref }}-${{ github.event_name }}`.
- Created clean [PR #174](https://github.com/11576865/MKV-Fast-Muxer/pull/174), exact head `ff2b232de811f3100ba9720e6e6c9761b30a79c9`, based on main `0.1027`. Superseded #173 closed, #170 preserved as historical research.
- Corrected [CI #39610097982](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39610097982): **all five matrix jobs really ran and finished** (two actual MKV+SHA PASS, three actual OOM red); concurrent scoped [CI #39610097976](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39610097976) completed **SUCCESS** without canceling research. The red research jobs are real product runtime failures, no longer cross-workflow cancellation.
- Resolution scope is Actions scheduling isolation, not a fix to large original Matroska attachment memory pressure. Canonical remains unchanged. Exact native media outcomes belong to the existing S12 Test, not this Bug.
