# Test · Browser-local checkpoint shelf must never become revived media or execution authority

Date: 2026-10-26
Status: **Test / Pending exact-head product CI / Not Canonical**.
Product: [11576865/MKV-Fast-Muxer PR #204](https://github.com/11576865/MKV-Fast-Muxer/pull/204), softmux 0.1032 candidate.

## Deduplication and specific new gap

Foundry already records `inbox/tests/2026-10-15-mkv-external-checkpoint-sha-sidecar-rebind-cas-undo.md` for portable JSON and complete external-file/sidecar SHA rebind; `inbox/candidates/2026-10-15-mkv-single-live-project-cross-owner-transaction-guard.md` for cross-owner transactions; and `inbox/candidates/2026-10-04-browser-storage-namespace-lazy-copy-forward.md` for a **different product** migrating existing IndexedDB namespaces and preventing deletion resurrection. Those are not a test for explicitly storing *inert dual-domain, user-authored project metadata* in a first-party origin and safely revisiting it after reload. No new migration/lazy-copy-forward rule is inferred.

## Proposed S09 regression gate

Product PR #204 reuses the already-validated `softmux-workspace-recovery-bundle-v1` serializer to save only versioned JSON plus source label and timestamp in new origin-scoped IndexedDB `softmux-workspace-metadata-checkpoints-v1`. Saving is explicitly user initiated and requires a byte-verified source SHA-256. External audio/subtitle/sidecar digests are computed via the existing authoritative path; a hard limit of eight records requires deliberate user cleanup rather than implicit eviction. The local shelf exposes Save/List/Load/Delete inside the production '工程草稿 · 核验与恢复' progressive disclosure.

After refresh, load must only stage independent source/external review drafts. It must not reconstruct `File`, media `Blob`, browser `FileSystem*Handle`, directory authority, generated MKV, a verified source grant, previous explicit confirmation, an executable mux, or durable undo. Actual selected source and external/sidecar files must be selected again, hashed and explicitly approved for the scoped restore before the real mux plan can change. A deletion removes the origin record but must not modify accepted live project metadata or source bytes.

Acceptance evidence required: Node negative tests for malformed nested JSON, missing digest, forged storage fields/scope, budget and IndexedDB unavailability; a **real Chromium IndexedDB-backed** test that directly inspects persisted record keys/no native `File` or `Blob`, reloads the page, confirms no browser File grants and no automatic mux, loads the saved metadata, reselects authentic media, verifies SHA and user consent, deletes the record without changing an accepted plan, and independently verifies a truly finished MKV by native ffprobe. This must be distinguished from in-memory mocked storage or a broad assertion about physical durability.

Failure/counterexample boundaries: browser private mode and storage eviction can erase the shelf; an IndexedDB quota denial must not fabricate 'saved'; local storage does not confer user-owned portable backups. The existing downloadable combined JSON remains the durable manual alternative. Fully editable Chapter/Tag graphs, font File reauthorization and media re-import do not become supported merely because a checkpoint is locally stored.

**State at intake:** Product PR #204 initially red due to a Node negative-case fixture constructing an invalid `createContainerProject` source rather than tampering a valid JSON; corrected at head `5be73092a0692441698a7db141b9836bc411e400`. Exact-head full Node, Chromium and S12 workflow verdicts are **Pending**. This Test does not modify any Canonical rule.

## 2026-10-26 actual production-disclosure accessibility regression (Pending exact-head CI)

Product PR #204 Code Review identified that on page refresh the production UI deliberately recreates `#sf14Recovery` as a **closed** progressive disclosure. The new Chromium storage test initially attempted to operate a present but hidden IndexedDB shelf after reload. Corrected product head `a8f89a3b611c30b579b5a516456dd405dd2a63c1` explicitly opens `#sf14Recovery > summary`, verifies that it is expanded, then uses visible save-list-load/delete actions. This is a test navigation defect, not evidence of failed IndexedDB persistence. It is already related to Foundry PR #55's recovery-disclosure observation, so **no second Candidate** was created.

Precise corrected product head's full Chromium and S12 CI remained in progress at this update; do not promote this Test to accepted, nor infer stable user storage or tablet acceptance merely from Node green.
