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

## Observed completed product-block delivery — 2026-10-14

The project reconciled overlapping #133/#134/#135 work into one integrated **PR #134** and merged to `main` as [8155280](https://github.com/11576865/MKV-Fast-Muxer/commit/815528027048e05d0d39660a1c21199d84dcd4d9). The final exact-head [CI 38524496562](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38524496562) succeeded on Node, build and full real Chromium. A previous run independently confirmed two actual outputs and final audit, and the final head repeated the full browser suite. PR #133 and #135 were closed unmerged and documented as superseded; unlike a mechanical merge, the alternate JSON schema from #135 was **not** advertised as supported. Source-resource authority, per-output metadata, explicit Recipe v2 review, frozen queue and real MKV production were accepted as one coherent user-facing unit.

This is a single project-specific observed instance, not controlled evidence that block-level PR strategy always reduces delivery time. A concrete caveat: attempts to rush through the sequence exposed multiple failed exact-head Chromium runs before the actual `EXTERNAL_DOMAIN_INVENTORY_CHANGED` fault was diagnosed and corrected. Keep CI failure localization and fail-closed behavior even when the requested milestone is broad. Next P0/P2 structural writer remains separately gated. Candidate remains **non-Canonical**.

## ASS recurrence and integrated source response — 2026-10-23

The same user explicitly rejected the ASS delivery cadence: “你在逗我吗，全是小修小改”. The visible work had delivered separate task-tab, Raw-dock, inspector-tab and regression-driver increments; those source checkpoints did not establish full-page visual acceptance. This is a recurrence of the existing user-specific granularity preference, not independent controlled evidence about productivity.

In response, ASS PR #149 now batches the permanent wide task rail, Figma-scaled page columns, shared canonical/draft text presentation, responsive inspector QC/Raw review and strict 1440×900/1024×768 compositor capture gates into one page-level source package: [020e207](https://github.com/11576865/ASS-Workbench-Android/commit/020e20761b024b64502c8ea582c163db86aa2ca9). Product rationale and explicit gaps: [integrated-page note](https://github.com/11576865/ASS-Workbench-Android/blob/020e20761b024b64502c8ea582c163db86aa2ca9/docs/FIXED-V11-INTEGRATED-PAGE-2026-10-23.md).

Evidence level: explicit user feedback + submitted product source + 22 local Python validator/extractor tests. Android build, device regressions, actual target-size screenshots and Figma parity for this package are Pending. No claim of improved elapsed time, completed integrated UI acceptance, bilingual semantics, main merge or Canonical promotion. Durable small checkpoints remain compatible with a coherent product milestone; they are not the milestone themselves.
