# Test: MKV ContainerProject imported draft provenance, diff and writer authority refusal

Date: 2026-10-13
Status: **PASS at exact PR head + named real-browser artifact; post-merge main CI pending**
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
