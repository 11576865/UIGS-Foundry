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
