# Candidate: Archive exact reviewed squash-merged PR heads before deleting Git-unique branch refs

Status: **Candidate / product implementation in PR #72; deletion evidence pending**
Date: 2026-10-11
Source repository: `11576865/MKV-Fast-Muxer`
Source PR: https://github.com/11576865/MKV-Fast-Muxer/pull/72

## Context and distinction

`MKV-Fast-Muxer` had 39 remote branch refs following integration of PRs
#63, #66, #69, #70. Thirty-three old heads matched the immutable
`head.ref` and `head.sha` of GitHub pull requests that were already
merged into main. Because most used **squash merge**, all 33 nevertheless
reported `ahead_by > 0` under `compare(main...branch)`.

Existing UIGS test
`inbox/tests/2026-10-04-branch-hygiene-deletes-only-ancestry-proven-merged-branches.md`
correctly prohibits their **general automatic deletion**. This Candidate
does not modify that Test or weaken its ancestry-only sweep.

## Proposed reviewed one-time exception

When a user expressly requests old branch-count reduction, treat the
cleanup as a separate archival/reconciliation operation, not an automatic
consequence of `merged == true`:

1. Explicitly list each reviewed branch name, exact original head SHA, PR
   number and merge commit SHA in a frozen allowlist.
2. At execution, verify branch protection, unchanged head SHA, original
   same-repo PR identity, merged status, and merge-commit ancestry on main.
3. Exclude any currently open PR head/base and long-lived branch classes.
4. Before changing a ref, create and verify a persistent lightweight Git
   archive tag pointing to **that exact original SHA**.
5. Recheck source ref and PR-use constraints, and delete with Git
   `--force-with-lease=refs/heads/name:expectedSHA`.
6. Confirm branch-ref absence before counting it removed; preserve the
   archive tag for recovery. Fail closed on mismatch, API uncertainty or
   lease rejection. Retain unreviewed branches.
7. Keep the general ancestry-based cleanup policy unchanged.

The pattern preserves object reachability while reducing *branch* refs. It
is not a reason to destroy branch work whose PR identity or semantic
successor has not been established.

## Evidence boundary

Source implementation:
- `docs/branch-archive-allowlist-2026-10-11.json`
- `scripts/archive_reviewed_merged_branches.py`
- `scripts/test_archive_reviewed_merged_branches.py`
- `.github/workflows/archive-reviewed-merged-branches.yml`

PR-unit job was successful at the time of this intake. Local Git
transport experiment verified a lease-protected deletion accepts an
unchanged ref and rejects a moved one. Full GitHub remote archival
and deletion are **not yet claimed** and require later explicit evidence
(backup refs, workflow result, and post-run branch inventory).

Status remains **Candidate**. Single-repository engineering evidence is
insufficient for Canonical promotion.
