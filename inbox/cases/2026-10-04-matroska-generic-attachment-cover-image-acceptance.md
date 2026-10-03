# Case: Cover image as first real acceptance target for generic Matroska attachments

Date: 2026-10-04
Status: Case / acceptance scenario
Project: ASS-Workbench-Android soft-mux / container workspace

## Scenario

After the soft-mux workflow is generalized from a video-centric model to a container-resource model, the first concrete user acceptance target is to add a personal cover image to an MKV as a generic Matroska attachment.

## Acceptance criteria

- The image is added through the same generic attachment path used by other arbitrary files, not through a one-off cover-only mux implementation.
- The attachment retains a stable filename and MIME type such as image/jpeg or image/png.
- The container inventory shows the image as an attachment/resource and does not misclassify it as a video track.
- The planned mutation is visible before write-back.
- The resulting MKV is remuxed transactionally, re-scanned, and verified to contain the image while preserving unrelated tracks, chapters, tags, and pre-existing attachments.
- Failure or unsupported downstream cover-art display behavior must not be confused with failure to store the attachment itself.

## Evidence boundary

This is a user-driven acceptance case, not a Canonical rule. It validates generic attachment support with one meaningful real-world artifact. It does not require every media player to display the attachment as cover art.

Do not promote to Canonical from this case alone.
