# Observation: Shallow Git history can make a negative ancestry result inconclusive

Date: 2026-11-05
Status: Observation / reproduced locally / no Canonical change
Product context: [HSR read-only device acceptance, PR #219](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/219).

## Reproduction and result

In a local three-commit chain A → B → C, clone C at depth 1 and fetch A separately at depth 1. Both commit objects exist. Git exits 1 for `merge-base --is-ancestor A C` because the traversal cannot cross the shallow boundary. After fetching full history, the same query exits 0. In a complete checkout, querying C as an ancestor of A exits 1.

For device acceptance, preserve confirmed ancestry, use unknown for an unproven negative in shallow history, and keep acceptance incomplete until sufficient evidence is available. Local real-Git regression reproduced the original false classification and passed after repair. Product push, CI and physical Termux acceptance were pending at intake.

## Deduplication and scope

The existing [HSR jieba Bug](../bugs/2026-10-24-hsr-jieba-posseg-pair-iterable-not-indexable.md) tracks tokenizer adaptation and field acceptance. This Observation concerns the completeness of ancestry evidence and is independently reproducible with Git alone. The [branch-delta Candidate](../candidates/2026-10-04-audit-post-sync-branch-delta.md) concerns content preservation despite valid ancestry. Neither record covers shallow-boundary false negatives.
