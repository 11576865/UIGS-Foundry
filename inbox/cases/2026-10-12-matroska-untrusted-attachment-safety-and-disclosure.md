# Case: Untrusted Matroska attachments — extract safety, semantic identity and disclosure

Date: 2026-10-12
Status: Case / candidate acceptance contract, not executed or validated
Origin: risk-oriented reassessment of `11576865/MKV-Fast-Muxer` after scope expansion to arbitrary attachments
Dedup: searched Foundry for attachment security, untrusted attachment and path traversal; no directly matching Matroska-specific case identified.
Existing related design:
- `inbox/candidates/2026-10-04-container-attachment-mutation-type-agnostic.md`
- `inbox/cases/2026-10-04-matroska-generic-attachment-cover-image-acceptance.md`
- `inbox/observations/2026-10-12-mkv-tool-scope-correction-and-ecosystem-baseline.md`

## Normative basis

RFC 9559 §26 explicitly identifies malicious or executable payloads stored in `Attachments`, inaccurate attachment media types, malicious Chapter Codecs, decoder/parsing attacks, and resource-denial risks. Readers extracting or consuming attachments SHOULD verify expected data or avoid using it. https://www.rfc-editor.org/rfc/rfc9559#section-26

§5.1.6 declares `FileData` an opaque binary payload; `FileName` and `FileMediaType` are metadata and must not be blindly trusted as proof of safe content.

## Threat model / candidate tests

A browser-local Matroska inspector/author should safely open untrusted source files and never require executing extracted attachments:
1. Attachment filename is `../private.txt`, absolute path, Windows drive path, control characters, Unicode lookalike, reserved basename, or duplicate path. Export is confined to a user-selected destination or direct download with sanitized, collision-safe filename; report the original name separately.
2. Declared `image/png`, `font/ttf`, or `text/plain` differs from actual file signature. UI distinguishes declared metadata from observed content; preview/parse only with verified appropriate parser, with explicit unknown state when uncertain.
3. Attached font/image contains corrupt, oversized, or exploit-oriented payloads; preview and font inspection execute with bounded memory/work and meaningful timeout/cancel. Decode failures do not corrupt the composition or silently discard source resources.
4. A source container includes a huge attachment or extreme attachment counts; importing should not allocate all payloads merely to list filenames, and should display size / limits accurately.
5. Attachment includes private document, software executable, license text, or media resource. The UI permits general binary attachment if otherwise valid but highlights inclusion on output review and never implies encryption/confidentiality.
6. An extracted file has same name as an existing destination file, or save fails halfway. Default behavior does not overwrite without an explicit decision, and reports partial and failed writes.
7. Standalone attachment with no media tracks is treated as non-playable even when structurally valid; structural writer support and conventional file extension must be independently tested.
8. Audit extract->reimport compares raw `FileData` bytes with trustworthy checksums when an exact-copy claim is made; no hash alone proves playback compatibility.

No code execution, codec exploit, or denial-of-service penetration test is claimed here. These are proposed adversarial fixtures, not a guarantee any real browser execution environment is secure. Do not auto-promote to Canonical.

## 2026-10-12 implementation provenance — export policy only (Pending exact-head CI)

Product [Draft PR #90](https://github.com/11576865/MKV-Fast-Muxer/pull/90), head `70cdb199c37fbd197c50667267d0528c9ae3feb9`, implements a **pure, source-reader-independent**, no-write export-name proposal policy. It normalizes untrusted metadata (NFKC), strips path components, replaces control/bidi/unsafe characters, handles reserved Windows device basenames and bounded UTF-8 lengths, and proposes case/Unicode-aware collision suffixes. It keeps the original FileName and declared MIME visible as **unverified metadata**, never trusted MIME/content bytes, direct directory paths or approval to overwrite.

Regression tests are submitted for `../`, Windows paths, fullwidth separators, reserved names, bidi controls, UTF-8-length collisions, exact caller-provided existing names and immutable/no-write status. **No real browser save or filesystem recheck is implemented here**; `destinationRecheckRequired=true`, `overwriteAuthorized=false`, `readyToWrite=false`, `payloadIntegrity=not-checked`. The actual safe save/rename + user approval work remains future, contingent on PR #89's separate Matroska attachment source reader and independently validated R-02 crosscheck.

At intake, exact-head Node/Vite/Chromium CI is **pending**. Update evidence only after tests, and do not promote Canonical from this one implementation.

## Export name policy exact-head verified and merged — 2026-10-12

Product PR [#90](https://github.com/11576865/MKV-Fast-Muxer/pull/90), exact head `70cdb199c37fbd197c50667267d0528c9ae3feb9`, passed **262/262 Node**, Vite Build, full Chromium E2E and the existing scoped R-02 independent fixture experiment in workflow [38241509099](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38241509099). Squash merged as `main@9bd2108938525997911cbff1f83cb3fe86ff2dad`.

**Verified scope:** immutable export *name proposals* for hostile Matroska FileName metadata, including traversal, Unicode normalization, bidi/control characters, reserved device names, UTF-8 limits and conservative collision suggestions. `declaredMimeType` remains untrusted and `overwriteAuthorized=false`. These tests do **not** establish actual browser save, destination race checks, payload digest, secure preview or source-attachment reader integration. Keep this Case partially unmet and do not promote a generic extraction-security guarantee to Canonical.

## P2 actual browser export integration — 2026-10-12 (Pending exact-head E2E)

Product PR [#89](https://github.com/11576865/MKV-Fast-Muxer/pull/89), exact head `e6ad4e67f89f661b2bdce180c887ac1e7abbbb59`, passed **273/273 Node**, Vite Build, full Chromium E2E, and independent R-02 `INDEPENDENT_READER_AND_BYTES_MATCH` + `MODEL_AND_INDEPENDENT_ATTACHMENT_BYTES_MATCH` in [workflow 38242968495](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38242968495). The source reader was merged as `main@f526d96d6f5f929f6b8cdcc3a48f5c50a2013207`. It is a bounded reader, not writer certification or full EBML/UID relationship preservation.

New product Draft [PR #91](https://github.com/11576865/MKV-Fast-Muxer/pull/91), head `92c8d9624d988fc7340c4f7b25f97448a0f0a76b`, integrates #89's inspected attachment Blob view and #90's safe proposed filename into an **explicit user-button browser download** workflow without touching legacy video/MKV writer inputs. It uses opaque `application/octet-stream` Blob URLs, visible original-name and declared-MIME distrust, generation/File-reference checks for stale scans and deferred URL revocation. New real-browser E2E will compare a downloaded generic attachment byte-for-byte with `notes.txt` independently attached by MKVToolNix, and verify malformed-source and delayed stale-source denial.

**Evidence status: Pending exact-head Node/Vite/Chromium.** Safe download invocation does not establish actual persistence to an arbitrary directory, filesystem overwrite prevention, independently verified content type, untrusted payload safety or general semantic container preservation. MIME/path spoofing and destination conflict threat cases remain relevant. No Canonical promotion.

## P2 actual browser generic attachment export verified — 2026-10-12

Product [PR #91](https://github.com/11576865/MKV-Fast-Muxer/pull/91), exact head `92c8d9624d988fc7340c4f7b25f97448a0f0a76b`, passed **273/273 Node**, Vite Build, full Chromium Browser E2E and R-02 independent/model crosscheck in [workflow 38243844113](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38243844113). Browser logs explicitly report `P2 independently-authored attachment browser extraction PASS` and `P2 source-switch async inspection rejection PASS`. The real downloaded attachment bytes from an independently `mkvmerge`-authored fixture match source `notes.txt`; swapping to malformed source removes export actions and a delayed read cannot resurrect stale entries. PR merged as `main@8c3de2e86173693b936009c3210d4a4ee30eb6ab`.

**Verified bounded behavior:** independent source chooser handles generic attached resources without video-rooted FFmpeg input; raw source name/MIME are displayed as untrusted metadata; safe proposed download names are used; downloads originate only from a direct user button click and get opaque `application/octet-stream` Blob views, with later URL revocation. This is browser **download initiation with verified E2E saved fixture bytes**, not general destination transaction/overwrite prevention, actual content-type validation, malware/executable safety or user-file filesystem write. The independent R-02 non-playing sample remains **test-only writer proof**; a production attachment-only writer remains absent. Full Chapter/Tag UID relation preservation and independently observed #77 remux semantic loss remain outside this slice. No Canonical promotion.

## P2 prefix evidence and declared MIME contradiction — 2026-10-12 (Pending exact-head E2E)

Product [Draft PR #92](https://github.com/11576865/MKV-Fast-Muxer/pull/92), exact initial head `4c74d74253c1ae3812ecb4463bd30f6ff682c13d`, implements a bounded, opt-in **64-byte** attachment FileData-prefix observation. It detects a deliberately small known-signature set (PNG/JPEG/GIF/PDF/ZIP/TTF/OTF/WOFF/WOFF2 and preliminary MZ) and only declares `prefix-mismatch` when a recognized signature contradicts a source-declared MIME. Unknown short/text content remains `unknown`, not automatically suspect or corrupted. Even matching prefixes explicitly retain `contentVerified=false` and `safeToOpen=unverified`. Real FileData is **not** scanned upon merely opening the Matroska inventory; browser users must deliberately click “检查签名” on an attachment. UI uses textContent and retains separate original untrusted metadata and safe proposed export filename.

New deterministic browser fixture shares the R-02 **test-only** EBML encoder with the existing independent MKVToolNix oracle, verifies a zero-Track/zero-Cluster PNG-only Matroska source through browser import and saved-download byte equality, then falsely declares the same PNG FileData as `application/pdf` and requires a visible `image/png` mismatch warning. Node and Vite gates passed on the pending head; full Chromium and independent R-02 evidence not yet accepted at intake.

This is **prefix classification only**, not a trustworthy MIME detector, parser vulnerability defense, malware scan, complete image/font decode, full bytes hash, or safe-preview authorization. No product no-media writer, destination filesystem overwrite control, or Chapter/Tag retention fix is introduced. This extends the existing Case with one narrowly scoped testable hypothesis; no Canonical promotion.
