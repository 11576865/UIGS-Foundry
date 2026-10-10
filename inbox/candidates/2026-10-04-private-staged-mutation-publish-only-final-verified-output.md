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


## QHE size-ceiling publication test checkpoint — PR #86 (2026-10-10)

A **second project** provides a distinct implementation context for private staging and publish-only-after-verification. QHE PR #86, merged as `7774777b36d57ea8c31f484dad7e8ba6573e70e4`, runs explicitly selected two-pass software H.264 on the real Windows Native Bridge. Pass one creates only private encoder statistics and a null output; pass two produces the staged Matroska. A user-selected **strict** ceiling rejects the *actual completed container bytes* if greater than the declared limit: the job becomes failed, staged output is removed and the existing export operation refuses to publish anything. A Windows synthetic Native API test proved a **1,024-byte strict failure** and a **5,000,000-byte strict success** (73,585-byte output).

This reinforces the Candidate's *private intermediate / only verified final publication* transaction boundary. It is a bounded software CI example, not user GPU/multi-hour/export-dialog field acceptance. The existing Candidate rule is unchanged, not promoted to Canonical. Separate Test: `inbox/tests/2026-10-10-guided-native-two-pass-verified-byte-ceiling.md`.
