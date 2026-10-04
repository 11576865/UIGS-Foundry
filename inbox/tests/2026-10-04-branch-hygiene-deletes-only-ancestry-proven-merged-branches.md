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

Validation is pending repository CI and first-run sweep evidence.

No Canonical promotion.
