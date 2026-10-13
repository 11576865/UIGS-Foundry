# Test: MKV ContainerProject imported draft provenance, diff and writer authority refusal

Date: 2026-10-13
Status: **PASS — exact PR head, named artifact and independently green post-merge main CI**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/121
Baseline: `main@31af804e5f60ec0da0f8dccf70e11e2551b7e591`
PR head at registration: `b99597fc88d650eeb858bc5bd791e6c664b93bf7`

## Work and acceptance boundary

A follow-up to the delivered *export-only* five-step preview [PR #120](https://github.com/11576865/MKV-Fast-Muxer/pull/120). New strict `container-project-v1` JSON import is bounded to 1 MiB, rejects extra keys/file handles/forged writer authorization, passes semantic object typing/references through the existing immutable domain constructor and renders a read-only comparison against **current** visible source/object projection.

Even if projected source IDs and object IDs are exactly the same, the status is only `display-identity-only`: file name/size/mtime is not evidence of source byte equality. The parser cannot revive file handles, verified attachments, saved artifacts, runtime execution permission or previous editor commits. New/removed object counts and import rejection are visible in the live workbench. Chromium must export the real project JSON then reimport it in an actual visible control, reject a `writerStatus:verified` injection, and prove current source and output stay unchanged.

## Dedup

- `inbox/tests/2026-10-13-mkv-five-step-integrated-preview-real-browser.md`: previous PASS covered JSON **export**, portable BatchRecipe and viewport evidence, not project re-import and live object-diff display.
- `inbox/candidates/2026-10-04-container-inventory-stable-identity-diff.md`: existing general object-ID diff principle; no new Canonical rule required.
- `inbox/candidates/2026-10-05-media-import-capability-stages-must-not-collapse.md`: imported representation is not write authority.
- `inbox/candidates/2026-10-02-shallow-magic-vs-structural-file-identity.md`: superficial identity checks cannot certify file content.

## Limitations

This is a **non-authorizing detached draft review**; it is not automatic edit-intent replay, true source cryptographic verification, full repository serialization with protected binary blobs, a transactionally writable `ContainerProject` or safe generic EBML writer. Do not promote Canonical from a single product test. Maintain explicit Pending if CI or Foundry write cannot be completed.


## Verified PR-head delivery

- Tested PR #121 exact head `b99597fc88d650eeb858bc5bd791e6c664b93bf7`, base `main@31af804e5f60ec0da0f8dccf70e11e2551b7e591`.
- [Node/build 38418128223](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38418128223): **PASS 450/450 tests and production build**.
- [Full Chromium E2E 38418128226](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38418128226): **PASS**, named five-step export-import scenario and legacy P0 safety/P3 dynamic ASS render scenarios all passed. Tests actually downloaded project JSON from browser and re-imported, then rejected forged `writerStatus:verified` without mutating `FileList` or starting mux.
- Named `five-step-container-recipe-workbench-evidence` artifact ID **11824899451** independently downloaded and examined: 2 JSON files and 3 PNG viewport screenshots 1440×900, 1024×768, 390×844. Actual project JSON is a `base.mp4` header-only one-object draft with `authorization=requires-relink` and `execution=requires-fresh-source-authorization`; no byte-hash authorization. Screenshots visually confirm import/review text (desktop and phone inspected).
- Squash-merged PR #121 to `main@3ec608648b57de6231ae253a561cb9bc82f31d7f`. No Canonical promotion; post-merge checks tracked separately.

## Independent main CI closure

Exact squash-merged `main@3ec608648b57de6231ae253a561cb9bc82f31d7f` re-verified independently after PR merge:

- [Main Node/build/Pages 38418982702](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38418982702): **PASS**.
- [Main full Chromium E2E 38418982574](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38418982574): **PASS**, logs explicitly contain project export/import scenario, P0/P1 unsafe source fail-closed and P3 four-frame dynamic ASS verdict, as well as `All browser E2E scenarios PASS`.
- Final status **PASS**, constrained to a detached nonauthorizing project comparison and schema validation. Full editable domain authority, file byte-hash binding, generic EBML safe writer and user-file execution remain outside this test. No Canonical promotion.

## 2026-10-14 P1 bounded source byte proof — PENDING exact CI evidence

PR: https://github.com/11576865/MKV-Fast-Muxer/pull/122
Baseline: `main@3ec608648b57de6231ae253a561cb9bc82f31d7f`
Current candidate head: `4d0ce26e3751fd18e1718a27a079d24d9b068ab5`
Status: **PASS exact PR head, artifact inspected and independently green post-merge main CI**

This extends the existing project's *import and drift review* Test instead of duplicating the Test or creating a new Canonical rule.

- Bounded whole-source SHA-256 committed in optional `sources[].sha256` of detached `ContainerProject v1`; WebCrypto must read all selected bytes, refuse files larger than **64 MiB before allocation**, and validate exact File continuity after awaiting hash.
- Previously exported v1 drafts without this optional digest remain legal imports but cannot claim source byte evidence. Typed parser rejects malformed SHA or hidden source grants.
- Explicit real UI button computes the current chosen File digest on request and compares with imported JSON; valid match yields only `digest-matches-draft` **without** `executionAuthorized` or `changesApplied`, while a same-name/file-identity draft with changed checksum fails.
- Hash match proves **relative to an untrusted/user-editable JSON claim**, not authorship, trust in edited object intents or permission to write MKV. It is not a digital signature, a live editable unified domain, continuous streamed multi-gigabyte hashing or a real container writer.
- Candidate unit tests require WebCrypto full hash vs independent Node hash, tampered file, too-large refusal before file read, no-digest old import, strict SHA format and zero runtime authorization. Browser E2E requires independent Node SHA of actual `base.mp4` match to exported JSON, valid explicit re-hash, forged SHA mismatch and preservation of prior P0/P2/P3 safety gates.

Related Candidate `inbox/candidates/2026-10-02-shallow-magic-vs-structural-file-identity.md` already separates display identity from actual bytes. Do not duplicate or promote Canonical based on one implementation.

### PR #122 exact-head acceptance

- Accepted PR head `4d0ce26e3751fd18e1718a27a079d24d9b068ab5`: [Node/build 38428630256](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38428630256) **PASS 457/457**; [full Chromium 38428630328](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38428630328) **PASS**, including user-explicit source SHA-256 match and same-source tampered-JSON digest mismatch, existing P0/P1 unsafe-source refusal and P3 multi-timepoint delivered libass rendering.
- Named artifact `five-step-container-recipe-workbench-evidence` **ID 11829154330** downloaded, extracted and JSON manually reviewed; 5 entries. Actual detached `base.mp4` draft declares `sources[0].sha256 = a78a0c371584ab404b90c9b7d9b6807550506cedcad8b991013a2cda859f520c`, `authorization=requires-relink`, `execution=requires-fresh-source-authorization`. It has only a header-only `other` object; no claim full track inspection. E2E independently checks source digest against Node digest of the actual fixture bytes. Three PNGs 1440/1024/390 were reviewed, showing visible entry and non-executable draft warnings.
- PR #122 merged via squash to `main@7e1274a70748810463129051e99529dbb1b62fa3`; **independent main build and Chromium CI verified PASS**.
- Scope remains full-file bounded WebCrypto ≤64MiB, untrusted editable JSON comparison, not a signed provenance proof, not an actual media-writing domain owner. No Canonical promotion.

### PR #122 independent main CI closure

Squash merged `main@7e1274a70748810463129051e99529dbb1b62fa3` independently verified after merge:
- [Main Node/build and Pages deployment 38429854419](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38429854419): **PASS**.
- [Main complete Chromium E2E 38429854426](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38429854426): **PASS**, logs contain named five-step source SHA browser scenario, P0/P1 structural-safety refusal, P3 four-frame dynamic ASS evidence, and final `All browser E2E scenarios PASS`; zero workflow errors.

Status confirmed **PASS** for one bounded, detached, nonauthorizing complete-file SHA-256 equality check. No broader browser stream hashing, full writer, editor-intent replay, device or Canonical claim. No further Pending item.
