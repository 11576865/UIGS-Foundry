# Candidate: Complete product-block delivery rather than PR-count optimization

Date: 2026-10-14
Status: Candidate / explicit user execution preference and project-grounded observation
Source project: 11576865/MKV-Fast-Muxer

## Trigger

The user explicitly rejected the perceived slow, fragmented approach to MKV-Fast-Muxer: “太慢了，太碎了，大步板块推进”.

At the repository snapshot, main had merged source-asset work through PR #132, while PR #133 was still proving external-resource live domain ownership, and overlapping PRs #134 and #135 were both implementing substantial Batch Recipe v2 / per-episode review and frozen execution behavior. Three separately active PRs spanning overlapping UI, pairing, editor-domain and batch-execution surfaces increase merge and validation burden. This is an integration risk, not proof that all three implementations are wrong.

## Proposed reusable principle (not Canonical)

For a user-facing capability that crosses domain state, UI, execution, artifact and verification, choose a **coherent functional block** as the delivery and acceptance unit. Internal commits and durable checkpoints may remain small for recovery, but should not be misrepresented as separate product milestones. Prioritize merged, user-observable end-to-end outcomes over the number of PRs, tests or commits.

For the current project, the next useful block is *verified reusable batch delivery*: external asset editing authority + reviewed per-output Batch Recipe v2 + current-File rebind + frozen JobPlan + real two-output mux + independent ffprobe/result audits. Treat #134/#135 as overlapping alternatives to reconcile semantically onto the authoritative #133 / main tree; do not blindly merge both or overwrite newer repairs.

Acceptance for a block: actual user task works end-to-end; source/domain authority is unambiguous; old capabilities preserved; stale input/plan cannot impersonate the current task; output independently examined; automated CI and any device evidence separately labeled; commit/branch is durable. The block is *not* complete merely because each constituent module has unit tests.

## Boundaries

- Do not bypass the P0 #77 complex Matroska nested Chapter / targeted Tag / AttachmentUID protection to make a large block look complete.
- Do not conflate a large feature block with one unreviewable giant commit; durable recovery checkpoints still apply.
- Continue following Canonical governance/AGENT-EXECUTION.md for bounded interactive turns, pending asynchronous CI and no unbounded polling.
- User-specific delivery granularity is not evidence of universal productivity or the correct PR size across all projects.
- No Canonical promotion on this single observation. No code or PR merge is implied by this Candidate.

## Deduplication

Searched Foundry for coherent feature batches, vertical slices, micro-PRs, integrated delivery and PR-branch boundaries. Related existing records: Canonical governance/AGENT-EXECUTION.md (durable bounded work); Candidate 2026-10-04-reintegrate-stale-branches-as-semantic-deltas (semantic merge); Candidate 2026-10-13-user-mainline-direct-commits-for-live-feedback (publication preference); Candidate 2026-10-12-legacy-capability-migration-and-document-plan-batch-queue (legacy/batch preservation). None directly records this user's block-level outcome/anti-fragmentation directive. This record complements rather than supersedes them.

## Follow-up verification

Observe whether reconciling the existing P1/P3-B branches into one accepted batch workflow reduces duplicate integration, without hiding CI failures, relaxing scope evidence, or regressing safety.
