# Case: QHE 51-head ancestry reconciliation exposes long-lived UIGS outbox deletion hazard

Date: 2026-10-15
Status: **Integration verified / outbox restored; next real scheduled sweep protection pending validation**
Project: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder
Historical base main: `e3ba785d72784497cce24b9154f8d2cd0124466c`
All-head convergence: [PR #111](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/111)
Correction: [PR #112](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/112)
Restored main: `2dda8c59772218c88689a5bea1252e015a0b2ab1`
Review record: `docs/full-remote-branch-ancestry-reconciliation-2026-10-15.md`

## Grounded facts

User explicitly requested **all GitHub remote branches** merged into `main`, without keeping individual legacy PRs as independent feature bases. The initial inventory contained 52 remote branch refs: `main` + 51 non-main heads. Of the 51, 42 heads mapped to earlier merged product PRs, seven closed-but-unmerged PRs were superseded by merged #41/#60/#61, and two non-product refs were `uigs-outbox` (durable intake packets) and `feat/qhe-theory-v1-10round-20261015` (non-authoritative design checkpoint). Two branches with heads beyond their merged PR SHA were checked: the UI probe/source summary functionality already existed on latest main, and the Android font branch had no extra file patch versus its original PR head.

Because prior PRs had been mostly squash merged, 51 heads remained divergent from `main` at the Git ancestry level although their relevant product capabilities had been merged or superseded. To preserve the latest product implementation, seven sequential **ours-style multi-parent commits** were constructed (first-parent chain from `e3ba785d`, 8/8/8/8/8/8/3 historical parents). The exact 51 SHAs were independently verified as distinct additional parents, zero omissions, identical tree across all seven commit objects; the only worktree change was the 51-row historical audit document. [PR #111](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/111) merged as `b78749fc307d1becf7295aaff31aa7bc30a48381`.

Important: **ancestry-only merge is not semantic source replay**. Old outbox packet files, replaced product code and obsolete speculative designs were not copied into main. This is valid for historical reconciliation only after verifying workstream supersession, not a universal merging strategy for unresolved feature branches. R19/R24 B01–B25/A01–A10 remain separate product acceptance obligations.

## Observed retention defect and correction

Immediately after #111, branch inventory dropped from 52 initial refs to **one `main` ref**, through [Branch hygiene run #38739519121](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38739519121), which correctly deletes ancestry-proven legacy heads. This also removed `uigs-outbox`, however, a special-purpose long-lived packet transport branch. Inspection of `.github/workflows/branch-hygiene.yml` showed it exempted `maintenance/*`, `integration/*`, release refs etc., but not `uigs-outbox`. Automatically treating `uigs-outbox` as a disposable product feature branch would interrupt UIGS intake.

[PR #112](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/112) added an explicit `uigs-outbox` exemption and merged as `2dda8c59772218c88689a5bea1252e015a0b2ab1`. Its exact PR-head UIGS Evidence Coverage check passed; main's subsequent Branch hygiene [run #38740291845](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38740291845) and UIGS Evidence Coverage succeeded. **That hygiene sweep happened before the outbox ref was re-created**, so it cannot independently establish future retention. The original outbox commit `8ea7b86ec1a1c5f2d3218c063f68a1f19fd06b8f` was still reachable as main ancestry and the branch was **successfully recreated at this exact SHA**. Subsequent GitHub branch GET verified `main`, the temporary fix PR head, and `uigs-outbox` were present; other old product refs remained gone.

## Reusable guardrails and open verification

- A Git `ours` ancestry reconciliation can make **all** historical refs eligible for an automatic ancestry-only branch deletion sweep, even when their feature content is not replayed. Inventory exemptions before the merge, not after it.
- Protected/long-lived infrastructure refs need explicit whitelists, not merely a conceptual comment calling them “not product”.
- Archive exact source SHAs and PR mapping first. Preserve actual code behavior and test contracts, do not mistake Git ancestry for production feature acceptance.
- Recovery from deletion is possible if the exact commit SHA remains reachable; restore the ref **after fixing the cleanup guard** or it can be deleted again.
- **PENDING TEST:** observe the next actual Branch hygiene sweep that runs while `uigs-outbox` exists and verify `retained>=1`, exact ref unchanged or naturally advanced, and no removal. Do not claim that test already passed.

## Deduplication

Foundry already has `inbox/tests/2026-10-04-branch-hygiene-deletes-only-ancestry-proven-merged-branches.md`, `inbox/candidates/2026-10-11-squash-merged-branch-tags-before-ref-pruning.md`, and `inbox/candidates/2026-10-04-active-work-branch-budget-and-cleanup.md`. These establish safe deletion and explicit archive practice, but do not capture this observed **all-head multi-parent ancestry→unexpected evidence transport deletion→repair** failure. Case is a single-repository observation; no Canonical promotion.

## Final tail reconciliation — 2026-10-15

The hygiene-fix PR #112 had been **squash merged**, leaving its new source branch at `e7a2ec02c7de32912eeb65719442f9a672829ba5` with 1 historical commit outside `main`. To fulfill the owner's literal all-ref ancestry requirement, a **non-force two-parent, no-tree-change** merge commit was created with current main `2dda8c59772218c88689a5bea1252e015a0b2ab1` first parent and the fix branch head second parent. Final main: **`ad90cb172700e2c182d6697b4b27d9b5d91083c1`**. GitHub compare confirmed both remaining non-main refs, `uigs-outbox` and the hygiene-fix branch, have **0 commits unique relative to final main**. The final source diff from the pre-convergence main has exactly 2 files: this QHE repo's 51-head audit Markdown and the `uigs-outbox` exemption in the hygiene YAML. No product source changed.

At final GET, QHE had **3 refs** (main, preserved `uigs-outbox`, and already merged fix ref), **0 open PRs**. Existing branch-hygiene may delete the redundant fix ref at its next sweep. The outbox should remain due the explicit exclusion; **next sweep with the outbox actually present is still pending independent runtime confirmation**.
