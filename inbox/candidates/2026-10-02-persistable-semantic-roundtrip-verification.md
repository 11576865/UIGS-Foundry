# Candidate: Persistable-semantic round-trip verification

Status: candidate
Date: 2026-10-02
Domains: reliability, architecture

## Summary

For file formats that normalize or quantize values during serialization, round-trip safety checks should compare the semantics the format can actually persist, not the raw in-memory representation.

A serializer may legitimately turn two different in-memory representations into the same persisted representation. Treating those differences as corruption creates false-negative save gates and can block recovery or safe-save paths.

## Evidence

ASS-Workbench-Android stabilization integration #59 exposed two concrete cases:

- ASS timestamps persist centiseconds, while editor state can carry millisecond precision. A strict before/after comparison incorrectly rejected valid values such as non-10-ms-aligned timestamps after ASS serialization.
- Empty Style/Event Format lists mean “use the standard default format” in memory, while writing and parsing makes the same default format explicit. Literal list comparison incorrectly reported this as a format change.

The verifier was corrected to canonicalize these persistence-equivalent representations before comparison while retaining strict checks for custom columns, opaque payload, unknown sections, styles, and events.

## Candidate rule

Before using round-trip equivalence as a save/recovery/release gate:

1. Define the persisted semantic domain of the format.
2. Canonicalize representationally equivalent values into that domain.
3. Compare strict semantics after canonicalization.
4. Do not use canonicalization to hide genuinely lossy fields or custom extensions.
5. Add regression tests for every discovered normalization boundary.

## Provenance

- source repository: `11576865/ASS-Workbench-Android`
- pull request: `#59`
- merge commit: `6b6cc6a7c9e4378b0ecb4809ab3eb910920e7da1`
- verifier normalization commits: `5741386abf06ee095cd0d35297437d3437daa89a`, `924b117caf53555ea879a55162286fd250f719d8`
- evidence level: CI-validated unit and emulator regression evidence on PR head `6a8c8ca9d360f81c2bedf9beefe5bba82ffbb740`

This is a Candidate only. It is not Canonical and requires cross-project corroboration before promotion.
