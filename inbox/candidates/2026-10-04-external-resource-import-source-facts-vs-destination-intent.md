# Candidate: External resource import should separate source observation from destination intent

Status: **Candidate / implementation-backed interaction and engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #115

## Observation

Importing a resource from another container is not the same operation as cloning that source container's local preferences.

A source track carries two kinds of information:

- **resource facts** required to preserve the encoded resource itself, such as codec/private data, track kind and payload;
- **source-context preferences / metadata**, such as Name, Language, Default and Forced, whose meaning may change when the resource enters a different destination container.

The first multi-track import workflow exposed a recurring UI and mutation problem: blindly copying every source flag makes source-local selection preferences become destination intent without an explicit user decision.

## Candidate rule

For cross-container or cross-document resource import:

1. **Inspect before planning.** Scan the source and present importable resources before creating destination mutations.
2. **Select a resource explicitly.** Import one or more concrete source resources, not the source container implicitly.
3. **Preserve payload-defining facts.** Codec, codec-private data and selected payload follow the resource unless conversion is an explicit operation.
4. **Allocate destination identity.** Do not reuse source identity as destination identity when the destination owns its own identity namespace.
5. **Treat source defaults as evidence, not destination intent.** Values such as Default, preferred role, visibility, activation or selection state should not silently become destination defaults.
6. **Expose destination metadata before commit.** Let the user confirm or edit destination-facing name/language/flags in the import flow.
7. **Do not silently import adjacent resources.** Source attachments, chapters, global tags and unselected tracks require separate explicit policy or mutations.
8. **Warn about known dependencies.** If a selected subtitle resource comes from a source with attachments, report that those attachments are not automatically copied and may contain required fonts/resources.
9. **Keep important actions visible, disclose secondary choices progressively.** A visible Add/Import entry may lead to source inspection and per-resource configuration without permanently expanding every row with all possible actions.

## Implementation evidence

PR #115 implements this for Matroska Track import:

- Android SAF source picker;
- source Track scan before mutation creation;
- per-Track chooser and destination metadata dialog;
- source Default is not inherited by default;
- selected Track codec/payload is preserved;
- a fresh destination TrackNumber / TrackUID is allocated;
- source global metadata and unrelated resources are not imported;
- source Track-targeted tags are retargeted to the new destination TrackUID;
- subtitle imports warn when the source contains Attachments;
- the tablet Container Inventory groups resources and moves secondary row actions behind an overflow menu while keeping Add Track / Add Attachment / Save visible.

## Evidence boundary

This is implementation-backed in one Matroska editor. It does not prescribe which metadata fields every format should treat as source facts versus destination intent.

Do not promote to Canonical from this evidence alone.
