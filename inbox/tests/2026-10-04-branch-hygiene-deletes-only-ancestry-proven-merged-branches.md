# Test: Branch hygiene deletes only ancestry-proven fully merged branches

Status: test
Date: 2026-10-04
Domains: engineering-process, git, branch-hygiene, CI

## Purpose

Verify an automated branch-cleanup workflow cannot satisfy a branch-count target by deleting branches that still contain unique work.

## Preconditions

The repository has a default branch, one or more non-default branches, and GitHub API access with permission to read pull requests/branches and delete refs.

## Contract

A branch is eligible for automatic deletion only when all of the following are true:

1. it is not the default branch;
2. it is not protected;
3. it is not the head of an open pull request;
4. it is not an explicitly retained long-lived branch class such as release/integration/maintenance;
5. GitHub compare from default branch to candidate reports `ahead_by == 0`.

If compare fails or returns an unclassifiable result, retain the branch.

If `ahead_by > 0`, retain the branch even when it appears semantically superseded, squash-merged, old, or redundant. Semantic supersession requires a separate reconciliation step.

## Budget signal

After the safe sweep, count remaining open-PR or unique-work branches. If the count exceeds the working budget, report the debt but do not delete unique commits to force compliance.

## Expected result

- ancestry-proven merged branches are deleted;
- unique, protected, open-PR, long-lived, and unclassifiable branches remain;
- branch-budget excess is visible as a warning rather than converted into destructive cleanup.

## Evidence

The workflow pattern was submitted on 2026-10-04 to six project repositories:
ASS-Workbench-Android #119, Quick-Automatic-Hardsub-Encoder #62, MKV-Fast-Muxer #62, HSR-Voice-Archive-Builder #130, Character-Voice-Service #12, and Character-Voice-Reader #9.

Validation evidence: the workflow PRs merged successfully in ASS-Workbench-Android, Quick-Automatic-Hardsub-Encoder, MKV-Fast-Muxer, HSR-Voice-Archive-Builder, Character-Voice-Service, and Character-Voice-Reader. First-run sweeps reduced observed branch counts without deleting unique-work branches: Quick 61→33, MKV 60→35, HSR approximately 132→82, and ASS 129→69 after its workflow landed. Foundry adopted the same workflow directly on main and reduced from 9→5 branches. These counts are operational evidence, not a claim that all remaining branches are still needed.

No Canonical promotion.


## 2026-10-05 semantic reconciliation evidence

A follow-up cross-repository audit exercised the contract's `ahead_by > 0` boundary rather than treating Git uniqueness as proof of missing product work.

Confirmed examples:

- Character-Voice-Service PR #9 remains many commits ahead of its old base, but current main already contains the stronger post-Reader EngineAdapter/engine-registry/IndexTTS architecture through PR #11 and later work.
- MKV-Fast-Muxer PR #25 remains Git-unique, while current main already contains canonical/Open Graph/Twitter/WebApplication metadata plus robots/sitemap and regression coverage.
- MKV-Fast-Muxer PR #26 remains Git-unique, while current main already contains the evolved mobile/tablet layout authority and browser E2E coverage.
- HSR-Voice-Archive-Builder PR #38 was superseded semantically by merged PR #68's center-outward bilingual ASS engine.
- HSR PR #56 was superseded by merged PR #57's responsive subtitle-editor layout.
- HSR PR #77 was superseded by merged PR #78's voice-gap-aware fade/motion engine.

The closed PR threads were annotated with the semantic successor/equivalence evidence.

This reinforces the test boundary: `ahead_by > 0` means automated deletion must stop, but it does **not** mean the branch should automatically be re-landed. A human/agent reconciliation must determine whether the semantic capability is absent, already represented by a successor, or intentionally obsolete.

No Canonical promotion.
