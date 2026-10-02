# Candidate: Resolve mid-flight duplicate work by narrowing to a single authoritative PR

Status: candidate
Date: 2026-10-02
Domains: operations, reliability

## Summary

In multi-agent repository work, duplicate scope can appear after a task has already started. The correct response is not to let both branches continue until merge time.

When a narrower, purpose-built PR appears for the same change:
1. re-check repository state before the next write;
2. identify the single authoritative PR for that scope;
3. remove the duplicate change from the broader branch if it has not shipped;
4. keep the broader branch focused on its original responsibility;
5. record the ownership decision in the shared coordination index.

This reduces duplicate CI, conflicting review evidence, and accidental double-merges.

## Evidence

ASS-Workbench-Android PR #62 (UI Contract Slice A) temporarily added Edge Bookmark coverage to the cross-presentation invariant test after Edge Bookmark entered main.

A separate PR #69 was then detected whose sole purpose was exactly that Edge Bookmark invariant coverage. #62 immediately reverted its duplicate test change and restored its four-file Contract scope, while #69 remained authoritative for the gate update.

No product behavior was lost; the two workstreams were separated before either merged.

## Candidate rule

For shared repositories:
- treat open PRs and recently created branches as dynamic coordination state;
- re-scan them before significant writes, not only at task start;
- if duplicate scope is detected, prefer the narrower or more established authoritative implementation;
- revert unmerged duplicate edits rather than carrying equivalent changes in two PRs;
- document the authority handoff so other agents do not recreate the duplicate.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- broad PR: `#62`
- narrow authoritative PR: `#69`
- duplicate-add commit on #62: `083a712778f814da4fa4fb2120eb833d71825fa0`
- duplicate-removal commit on #62: `1f759d3778f50784f2eb8edaf6ef026bdab16388`
- evidence level: directly observed multi-agent repository coordination

This is a Candidate only. It is not Canonical.
