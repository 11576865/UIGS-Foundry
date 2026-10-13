# Case: Streaming large-file source identity must preserve digest semantics and cancellation boundaries

Date: 2026-10-14  
Status: **Case / product implementation submitted; exact-head PR CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
Work package: [P1 PR #126](https://github.com/11576865/MKV-Fast-Muxer/pull/126)  
Source baseline: merged PR #125, `main@1583570d59234a965c180b22a8fc24707703a24e`

## Trigger and problem

Existing P1 detached `ContainerProject` export used `SubtleCrypto.digest('SHA-256', await file.arrayBuffer())` and imposed a 64 MiB whole-source cap. This prevented ordinary larger videos from obtaining a source-byte commitment needed for verified import and user-confirmed track restoration. Removing the size check without changing the algorithm would allocate potentially multi-gigabyte JavaScript ArrayBuffers in the page.

## Implemented experiment

- Keep small-file WebCrypto and introduce incremental FIPS 180-4 SHA-256 for larger files, one 1 MiB `File.slice()`/ArrayBuffer at a time. It computes **SHA-256 of the concatenated original bytes**, not SHA-256 of separate chunk hashes or an alternative identity scheme. Keep `sources[].sha256` format unchanged.
- Scope the activity: maximum 16 GiB per source, one active local hash operation, byte-based progress, explicit user cancellation, cancellation on source replacement or draft import, no publication of a partial digest, and source ref checks before subsequent export / verification.
- Retain the original authority boundary: even a matching SHA in editable JSON does not prove author, prior edits or permission to execute, and it does not bypass scanned track identity, old-value conflicts or final Matroska output audit.
- Large-media encoding/mux is unchanged. The P2 RAW EBML 64 MiB independent **research** cap is not increased.

## Evidence

- Deterministic FIPS SHA-256 standard vectors pass in isolated V8 function execution (empty, abc, hello, 1,000,000 a).
- Source hashing of a logical **65 MiB + 13 bytes** of literal `a` in 1 MiB chunks yielded `ad363dc06f71afbf51c807994c7719181d60477460cda7feae3bfee72997084a`, independently checked against Python hashlib.
- Submitted Node regressions include >64 MiB fake `File` refusing full `arrayBuffer()`, irregular chunks vs Node crypto, cancellation, size drift, truncated slices, digest persistence/mismatch and strict import.
- Submitted Chromium E2E uses real application input: MP4-prefixed 65 MiB File, user-facing export, JSON SHA-256 vs independent Node `crypto`, reimport and source verification; it must never infer mux or track authority.
- Changed JavaScript syntax parsed successfully. **Exact PR #126 Node/build/Chromium is Pending**; long-media runtime, 16 GiB wall clock, OEM/memory/storage and device acceptance have not been measured.

## Scope and deduplication

- Related P1 Case `inbox/cases/2026-10-14-mkv-verified-source-delta-export-and-atomic-replay.md` documents read-only compare → explicit verified edit mutation; current Case solves the source-identity scalability bottleneck, not duplicate replay logic.
- Do not confuse the new P1 16 GiB bound with the independently justified P2 64 MiB raw Matroska structure research budget.
- General cross-project hypothesis: separate **cryptographic identity semantics** from a particular execution mode/whole-buffer implementation. Keep this as a scoped Case while exact-head CI and wider corroboration are pending; do not promote Canonical from this observation.
