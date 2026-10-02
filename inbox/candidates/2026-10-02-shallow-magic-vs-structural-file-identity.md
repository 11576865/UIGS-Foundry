# Candidate: Shallow magic detection is a hint, not verified file identity

Status: **Candidate / reusable ingestion-validation pattern**
Date: 2026-10-02
Project evidence: `11576865/MKV-Fast-Muxer`, PR #57

## Observation

Replacing filename-extension checks with content inspection is not sufficient if the new inspection only verifies a few leading magic bytes.

During font identity work, an SFNT-looking signature such as `0x00010000`, `OTTO` or `ttcf` was enough to classify a file as a probable TrueType/OpenType resource, but that shallow evidence does not prove that the internal font tables, collection directory, name table or usable faces are structurally valid.

A file can therefore pass:

```text
filename hint
    ↓
magic/signature check
    ↓
“looks like font”
```

while failing the real parser later.

## Candidate rule

For structured file ingestion:

- treat filename/MIME as hints;
- treat magic/signature recognition as shallow content evidence;
- when the product already has a real structural parser, use successful parsing as the verified identity boundary before enabling downstream capabilities that assume a usable resource;
- keep shallow detection useful for cheap preclassification, but do not promote it to “supported” when malformed structure can still invalidate the file;
- carry parser-derived identity forward so later preview, conversion, batching, MIME assignment and export do not independently fall back to weaker hints;
- regression tests should include files with a valid-looking signature but malformed internal structure.

A useful evidence ladder is:

```text
name/MIME hint
< magic/signature match
< structural parse
< operation-specific real execution
< final output verification
```

## Evidence

PR #57 initially had a font content detector based on SFNT/OpenType signatures. The single-task mux path later called the existing font parser and would still reject malformed fonts, but batch discovery could classify a signature-spoofed file as a supported font before that deeper validation.

The revised implementation adds verified font inspection: it first recognizes the SFNT family, then requires the existing internal font parser to successfully read one or more usable faces before setting `supported=true`. Batch discovery and subsetting consume this verified identity.

## Scope

Applicable to fonts, archives, media containers, document formats, model files, databases, executable/object formats and other structured resources where a short magic prefix is necessary but not sufficient evidence of a usable file.

Do not promote to Canonical from this single project implementation without broader validation.
