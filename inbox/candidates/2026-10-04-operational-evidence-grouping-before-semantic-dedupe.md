# Candidate: Group repeated operational evidence before semantic deduplication

Status: candidate
Date: 2026-10-04
Domains: operations, reliability, knowledge-governance, review-workflow
Evidence type: Foundry intake/review pipeline implementation

## Summary

Repeated CI or runtime packets can create review effort proportional to execution count even when many packets share the same operational shape.

Before asking a reviewer to inspect every packet independently, a knowledge system may group unresolved evidence by conservative operational dimensions such as:

- source repository;
- workflow or execution surface;
- coarse failure category;
- matched classification rules;
- already-related knowledge.

This reduces review repetition while preserving the original packets as immutable evidence.

## Critical boundary

Operational grouping is **not** semantic/root-cause deduplication.

Two failures may share repository, workflow and classifier signals while still have different root causes. Therefore grouping may:

- prioritize review;
- expose recurrence volume;
- select representative samples;
- reduce repeated navigation;

but it must not automatically:

- merge Bug records;
- assert one root cause;
- accept/reject a promotion proposal;
- promote knowledge maturity.

## Reusable rule

Use a two-stage model:

`raw evidence -> conservative operational family -> human/semantic review -> knowledge dedupe`

Do not collapse directly from repeated telemetry into one knowledge claim.

## Evidence

UIGS-Foundry PR #12 adds a generated review queue that groups unresolved `needs-review` CI packets by repository, workflow, red-reason category, matched rules and related knowledge while keeping promotion decisions explicit.

This is a Candidate only. It is not Canonical.
