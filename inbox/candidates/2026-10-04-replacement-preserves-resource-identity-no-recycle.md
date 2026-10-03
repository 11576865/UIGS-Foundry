# Candidate: Replacement mutations should preserve stable resource identity and never recycle removed identity in the same transaction

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #97

## Observation

A generic container editor cannot treat Remove + Add as equivalent to Replace when resources have stable identity. Reusing the identity of a removed resource for a newly added resource also makes post-write diff and verification ambiguous.

The attachment CRUD implementation exposed two distinct requirements:

1. replacing an existing attachment should preserve its stable Attachment/File UID when one exists;
2. newly added attachments must receive identities above the source transaction's original identity range rather than recycling a UID freed by a removal.

## Candidate rule

For transactional resource editors with stable identities:

- represent **Replace** separately from **Remove + Add**;
- preserve the target resource's stable identity across replacement when the format supports it;
- do not recycle an identity removed earlier in the same transaction for an unrelated newly added resource;
- resolve mutation targets by strong identity first; permit weak/name targeting only when it is unambiguous;
- fail closed if one target is simultaneously scheduled for incompatible operations such as Remove and Replace;
- after execution, verify unchanged resources by identity, removals by absence, replacements by preserved identity plus expected new payload metadata, and additions as genuinely new identities.

## Why this matters

Without these constraints, a post-write inventory diff can misclassify a newly added resource as a modification of the removed one, or fail to distinguish replacement from delete-and-recreate. That weakens auditability, undo semantics, and user trust in resource-oriented editors.

## Evidence

PR #97 implements these constraints for Matroska attachments and adds Go, Android bridge, and plan-level regression coverage.

## Evidence boundary

This is implementation-backed in one container editor. Exact identity mechanisms vary by format and resource class; not every format supports stable identity preservation.

Do not promote to Canonical from this evidence alone.
