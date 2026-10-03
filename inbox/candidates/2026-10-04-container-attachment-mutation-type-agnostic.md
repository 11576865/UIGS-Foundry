# Candidate: Container attachment mutation should be type-agnostic

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #91

## Observation

A media-container editor becomes structurally brittle when every attachment class receives a separate write path (for example font-specific append logic, then image-specific logic, then document-specific logic).

Matroska attachments share the same underlying container role even when the UI classifies them as fonts, images, documents, project data, or unknown binary files.

## Candidate rule

For container formats with generic attachment support:

- model the write operation as a type-agnostic **attachment mutation**;
- keep MIME/type classification primarily as metadata, validation, presentation, and downstream-compatibility information;
- do not require a media-track edit merely to add an attachment;
- preserve legacy specialized flows (such as font packaging) as constrained callers of the generic attachment path rather than separate remux implementations;
- keep planned attachments separate from observed inventory until write-back succeeds;
- rebuild/remux transactionally, re-scan the actual output, and verify unrelated tracks, chapters, and pre-existing attachments before publication;
- unknown file types should remain explicit and may use a generic binary MIME type instead of being rejected solely because the application does not understand their payload.

## Implementation evidence

PR #91 adds:

- generic attachment remuxing in the native mkvgo bridge;
- an attachment-only path that does not require selecting or rewriting ASS;
- Android pending-attachment state and arbitrary-file picker;
- cover PNG and arbitrary unknown-extension regression fixtures;
- post-remux inventory verification.

The user-facing first acceptance artifact is a cover image stored as a Matroska attachment.

## Evidence boundary

This is backed by one project implementation and tests, not a cross-project usability result. It does not prescribe how every container format represents attachments and does not claim that downstream media players will display arbitrary attachments or cover art.

Do not promote to Canonical from this evidence alone.
