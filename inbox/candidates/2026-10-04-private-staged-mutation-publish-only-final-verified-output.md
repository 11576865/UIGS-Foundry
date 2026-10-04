# Candidate: Compose incompatible mutation engines through private stages; publish only the final verified artifact

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #109

## Observation

Two valid mutations may require different specialised streaming/write paths and therefore cannot always be executed safely in one writer pass. Forcing them into one generalized path can destroy invariants that the specialised path exists to protect.

ASS Workbench encountered this when combining:

- same-slot ASS replacement, which injects regenerated subtitle blocks through a specialised path; and
- external Track import, which merges blocks from several container sources through a k-way streaming path.

The product composes them as private cache-local stages instead of publishing the first stage.

## Candidate rule

When a single user transaction contains mutations implemented by incompatible or independently validated transformation engines:

1. Preserve one **user transaction / plan** even if execution requires several internal stages.
2. Each intermediate artifact is **private implementation state**, not a user-visible saved result.
3. Later stages consume the previous stage's actual output rather than reconstructing an assumed state.
4. Only the final artifact is eligible for publication to the user-selected destination.
5. Run end-to-end verification against the original plan on the final artifact; success of an intermediate stage is not sufficient.
6. If any later stage or final verification fails, do not publish the intermediate artifact as though the transaction succeeded.
7. Keep staging local/ephemeral when possible so internal composition does not create extra user-facing files or identities.

## Implementation evidence

PR #109 uses this rule when dirty ASS replacement and external Track import coexist:

1. write an internal cache `ass-stage.mkv` with the specialised ASS replacement path;
2. import external tracks from that actual staged container into the final cache artifact;
3. re-scan and verify the final artifact against Track, Attachment, Chapter, ASS, and identity invariants;
4. only then copy the final artifact to the user's destination URI.

When no specialised ASS replacement is needed, Track import remains a one-pass remux.

## Evidence boundary

This is one implementation pattern, not a requirement to use filesystem staging. An in-memory pipeline, transactional database, object store, or streaming graph may provide the same semantic boundary.

Do not promote to Canonical from this evidence alone.
