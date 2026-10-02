# Candidate / Bug: Git tree replacement hazard when base tree identity is unresolved

Status: **Candidate / recovered engineering bug**
Date: 2026-10-02

## Incident

While constructing a merge commit through GitHub Git Data APIs, the caller misread a commit response shape and obtained an undefined base-tree SHA. `create_tree` then proceeded without the intended base tree and produced a tree containing only the explicitly supplied entries. Moving the feature branch ref to a commit using that tree would effectively replace the repository tree with a tiny partial tree.

The error was detected immediately by verifying the branch tree and compare result. The branch was recovered by:
1. reading the authoritative feature-head Git commit through the Git commit endpoint;
2. obtaining its real tree SHA;
3. rebuilding the merge tree from that base plus the intended main-side file blobs;
4. creating a correct two-parent merge commit;
5. force-moving the feature ref to the corrected commit;
6. verifying `behind = 0` and the expected changed-file set.

## Follow-up incident

A second branch-sync incident showed a related but distinct hazard: even with a valid feature base tree and a correct two-parent merge commit, reconstructing the merge tree by overlaying only the *latest* main-side delta can still silently omit files introduced by an earlier main merge that never existed in the feature tree.

The candidate merge correctly reported `behind = 0`, yet the full compare against the target main head showed an unexpected deletion of `docs/UI-EXPERIMENT-240-LEDGER.md`. The branch ref was corrected immediately by restoring the missing main file and re-verifying that the full changed-file set contained only intended feature changes.

This demonstrates that ancestry correctness (`behind = 0`) is necessary but not sufficient. The full compare must also be inspected for unexpected removals or modifications before or immediately after moving the ref.

## Reusable rule

Before any Git Data API operation that can move a public branch ref:

- treat `base_tree_sha` as a required invariant even if the API schema marks it optional;
- assert the resolved tree SHA is non-empty and belongs to the expected parent commit;
- construct the candidate commit before moving the branch ref;
- inspect the resulting tree/diff or compare result;
- reject any candidate whose full compare against the target base contains unexpected removals/modifications, even when `behind = 0`;
- only then update the ref;
- after the ref move, re-read the branch head and compare against its base.

An omitted `base_tree_sha` is not a benign default when the intent is an incremental tree update; it changes the operation into construction from scratch.

## Stronger safe sequence

`resolve parent commit -> verify parent tree -> create tree -> create commit -> full compare against exact target base -> validate changed-file allowlist -> update ref -> re-read/compare branch`

Where possible, prefer a native merge/update-branch API over manual Git Data composition.

## Evidence boundary

This is one recovered incident using the GitHub Git Data workflow. It should not be promoted to Canonical solely from this occurrence, but it is high-value regression knowledge because the failure mode can make a branch appear to delete nearly the entire repository.

Do not promote to Canonical from this incident alone.
