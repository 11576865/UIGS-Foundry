# Candidate: Import normalization must define the identity of the normalized execution representation

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #122

## Observation

An import adapter may accept a source representation that the destination writer cannot consume directly.

In that case there are at least three distinguishable identities:

1. the external source artifact's raw byte identity;
2. the **normalized execution representation** produced by the import adapter;
3. the fresh destination resource identity allocated when the normalized representation is materialized.

The standalone ASS import implementation exposed a concrete failure mode if these are collapsed. A UTF-16/BOM or otherwise supported text source is decoded and normalized to UTF-8 before it reaches the Matroska writer. Hashing only a transient cache path proves nothing, while describing the normalized hash as a raw-file checksum overstates what was actually pinned.

## Candidate rule

For source-normalizing import pipelines:

1. **Name the identity domain explicitly.** State whether evidence covers raw source bytes, decoded semantics, normalized bytes, or destination identity.
2. **Normalize deterministically before execution evidence is committed.** The same source plus the same adapter policy should produce the same execution representation.
3. **Pin the normalized execution representation before materialization.** Store a digest or equivalent evidence over the exact representation the downstream writer is expected to consume.
4. **Re-read and re-normalize at execution time.** If the source can change between planning and Save/Commit, reproduce the normalization and compare the evidence before writing.
5. **Validate again at the adapter/writer boundary when practical.** Staging paths are transport; they are not identity. The downstream writer should reject staged bytes that do not match the planned normalized evidence.
6. **Allocate destination identity separately.** A normalized source still becomes a new destination resource under destination identity rules.
7. **Verify semantic materialization after writing.** When a semantic round-trip verifier exists, compare the planned normalized source semantics with the actual output resource instead of relying only on metadata/count checks.
8. **Do not imply raw-byte immutability from normalized evidence.** Two byte-distinct source files may intentionally normalize to the same execution representation.

## Implementation evidence

PR #122 applies this to standalone ASS → Matroska Track import:

- Android decodes the selected ASS through `AssTextDecoder`;
- decoded text is normalized to UTF-8;
- SHA-256 is computed over the normalized UTF-8 bytes;
- Save re-reads the SAF URI, repeats decoding/normalization, and rejects normalized-payload drift;
- the native bridge validates the staged UTF-8 bytes against the same SHA-256 before parsing/muxing;
- the destination Track receives fresh TrackNumber / TrackUID;
- post-remux verification finds the actual imported subtitle Track and compares it against the staged normalized source through `AssRoundTripVerifier`.

This deliberately means an encoding-only raw-byte change that decodes to the same normalized ASS can remain equivalent, while a semantic change fails closed.

## Additional implementation evidence

PR #123 extends the same rule from a single ASS source adapter to a second source format, SRT:

- ASS / SSA and SRT now converge into the same deterministic UTF-8 ASS execution representation before the native writer;
- the Matroska writer does not gain an SRT parser or a second subtitle-writing path;
- BOM and line-ending differences that normalize to the same SRT semantics produce the same normalized identity;
- semantic SRT changes produce a different normalized SHA-256;
- the same save-time re-read, normalized evidence check, native bridge validation, fresh destination identity allocation, and post-write semantic verification are reused.

This strengthens the observation that a normalized execution representation can act as the stable contract between multiple source adapters and one downstream writer, reducing format-specific branching below the adapter boundary.

## Evidence boundary

This evidence now covers two text subtitle adapters converging on one execution representation. Binary media normalization, transcoding, lossy canonicalization, color-management transforms, and nondeterministic encoders may require stronger or different equivalence definitions.

Do not promote to Canonical from this evidence alone.
