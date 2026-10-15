# Agent protocol

## 最高指导：用户授权边界（适用于所有项目、每次执行）

> 有什么疑问直接问我，千万千万千万千万千万千万千万不要不经过我允许就擅自改动。

**优先级：最高，覆盖与之冲突的默认工程习惯。** 用户已明确列出的修改即为该限定范围内的授权，不需要反复询问；除此之外，任何 UI、行为、数据、文件、测试、配置、工作流或工程范围的改动都不可擅自添加、删除或扩大。有真正影响实施的歧义，应先询问用户，而非自行决策。

**执行前逐项核对：** 当前任务获授权的对象与精确范围；哪些现有功能和界面明确要求不得触碰；写入目标是否经用户指定或由指令直接确定；是否存在未经请求的独立分支、PR、合并、发布、顺带重构或自动规范提升。独立分支/PR 不得仅凭惯例擅自创建。若需越界，必须先取得新授权。本次对话中每一次执行都必须重新检查本条。

**HSR 本轮边界：** 删除的是排版模式里的字幕时间轴 UI，不是底层字幕时间轴、数据或导出功能；特效工作台 UI 不得改动。快速字幕预览与实际 ASS 渲染须作为不同来源与证据等级保留。自动保存不得把旧设置覆盖新编辑。

---

This repository is a knowledge-control plane, not a dumping ground.

## Execution safety — highest priority

Interactive agent sessions are disposable workers. Repositories, commits, branches, pull requests, task-state records, and other persisted artifacts are the durable state.

1. **Persist useful work early and incrementally.** Do not keep the only copy of meaningful progress in conversation memory, hidden reasoning, a temporary worktree, or an unpushed local state.
2. **Use bounded work units.** Broad goals such as "continue improving the project" must be converted into one coherent work unit with an explicit durable checkpoint before the next unit begins.
3. **Checkpoint before crossing failure domains.** Before long CI, emulator/device tests, renders, deployments, cross-repository work, or other asynchronous/external operations, commit and push the coherent work completed so far whenever it is safe to do so.
4. **A pushed commit / branch / PR is the default execution boundary.** Once the requested coherent work unit is durably submitted and no immediately actionable failure is already known, mark the agent work complete and return control to the user.
5. **External validation does not keep the turn alive.** Pending CI, builds, emulator runs, native probes, renders, deployments, reviews, Foundry collection/triage, or promotion processing are reported as Pending and do not block Agent Execution Complete.
6. **Do not poll open-endedly.** After starting or locating an external job, perform at most one immediate status read unless the user explicitly requested synchronous waiting. If it is still queued/running, report Pending and stop.
7. **Bound repair generations.** If an already-visible failure is directly caused by the current work unit, one immediate repair generation may be performed. After re-pushing the repair, do not wait for the next validation generation; report it Pending and stop.
8. **Make interrupted work resumable from repository state alone.** For work expected to span more than one coherent unit, maintain a durable task state following `governance/AGENT-EXECUTION.md` and `schemas/agent-task-state.schema.json`.
9. **Resume before rediscovering.** On a continuation request, read the durable task state, branch/PR, and latest durable commit first. Do not reconstruct project progress primarily from conversational memory.
10. **UIGS Intake is bounded post-processing.** Intake may classify and persist reusable knowledge, but it must not reopen the primary product task, wait for Foundry CI, chase downstream automation, or silently expand into another unbounded workstream.
11. **Foundry processing is asynchronous by default.** Product-side agents may emit/update a bounded intake record or mark it Pending. Collection, triage, proposal generation, reporting, validation, and Canonical promotion are separate lifecycles.
12. **Never claim external completion without evidence.** Distinguish Agent Execution Complete, Pending External Validation, External Validation Complete, and Project Complete.

These rules take precedence over lower-level intake, reporting, validation, and workflow instructions whenever continuing those activities would risk losing already-completed work or keeping an interactive turn alive without a bounded purpose.

## Epistemic protocol

1. Treat `governance/EPISTEMIC-MODEL.md` as the semantic source of truth for reusable knowledge.
2. Do not equate maturity with current truth or current authority.
3. Before using high-impact reusable knowledge, respect scope, assumptions, computed effective authority, epistemic state, and evidence freshness.
4. A Canonical Claim that is effectively quarantined must not be used as default guidance.
5. New contradictory or undercutting evidence must challenge the existing Claim; do not merely append a new contradictory document.
6. Preserve evidence lineage. Do not count copied/adopted implementations as independent confirmation when they share an upstream origin.
7. When a dependency is invalidated, propagate review debt only to Claims that actually depend on it.
8. Permanent demotion/deprecation/supersession requires a durable Knowledge Change record.
9. Prefer revising/narrowing a Claim over deleting history.
10. Before inventing a new foundational governance mechanism, perform prior-art mapping against `governance/PRIOR-ART.md`.

## Knowledge-control protocol

1. After substantial software/UI/testing/engineering work, perform a UIGS Intake Check.
2. Determine whether the new information is reusable beyond the immediate task.
3. Search existing registry and inbox records before creating a new one.
4. Record provenance and evidence level.
5. Prefer updating an existing family over creating a duplicate.
6. A single observation may create Observation, Candidate, Case, Bug, Test, Lesson, Claim, Evidence, or implementation reference.
7. Do not silently promote a rule to Canonical; follow `governance/PROMOTION.md`.
8. Product repositories remain authoritative for executable implementation.
9. If a Foundry write cannot be completed, report it as **Pending**; never imply success.
10. For UI work resolve: natural-language intent -> Pattern ID -> platform realization -> expected effect -> validation contract -> known failures.


## Synchronous liveness guard

**Bound synchronous action chains.** Durable checkpointing and bounded polling are not sufficient by themselves. Prefer one coherent work package, batch related remote mutations, and hand off before entering a second independent subsystem or migration phase. A broad goal describes the desired end architecture, not permission for an unbounded turn.
