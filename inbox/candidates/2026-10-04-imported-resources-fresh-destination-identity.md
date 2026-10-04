# Candidate: Imported resources need fresh destination identity while source provenance stays separately verifiable

Status: **Candidate / implementation-backed engineering observation**
Date: 2026-10-04
Project evidence: `11576865/ASS-Workbench-Android` PR #117

## Observation

Importing a resource from one structured artifact into another is not the same operation as replacing an existing destination resource.

The external source resource already has an identity inside its own artifact, but copying that identity directly into the destination can collide with destination identities, while reusing an identity freed by deletion can make post-write verification misclassify an import as a replacement.

The first external Matroska Track import implementation exposed a reusable separation between **source provenance identity** and **destination resource identity**.

## Candidate rule

For cross-artifact resource import:

1. Preserve source provenance separately from destination identity.
2. Resolve and revalidate the exact source resource at execution time using the strongest available source identity; if the source artifact changed identity between planning and execution, fail closed.
3. Allocate a fresh destination identity according to the destination format's identity rules. Do not copy a potentially colliding source identity into the destination.
4. Do not recycle an identity removed earlier in the same destination transaction for an unrelated import.
5. Preserve all surviving destination resource identities and relative ordering unless renumber/reorder is itself an explicit mutation.
6. If copied metadata contains references targeted to the source resource identity, retarget only the references that semantically belong to the imported resource. Do not automatically import unrelated artifact-level metadata or sibling resources.
7. Post-write verification should distinguish:
   - survivor preservation;
   - replacement identity preservation;
   - removal absence;
   - import as a genuinely fresh destination identity;
   - source-provenance evidence used to resolve the imported payload.
8. Default/selection semantics that can change downstream behavior should use an explicit import policy rather than silently inheriting a source artifact's local selection priority.

## Implementation evidence

PR #117 implements this for Matroska Track import:

- source TrackNumber identifies the selected source Track and source TrackUID is revalidated at save time when available;
- destination TrackNumber / TrackUID are allocated above the original destination identity range;
- removed destination identities are not recycled;
- source track-targeted Tags are retargeted to the new destination TrackUID;
- source Chapters, Attachments, global Tags and unrelated Tracks are intentionally not imported;
- new imported Tracks are non-Default by default to avoid silently stealing player auto-selection;
- output is re-scanned to prove survivor identity plus fresh imported identity.

Regression coverage includes non-contiguous destination TrackNumbers, source UID drift, duplicate import rejection, full destination track-set replacement and ASS replacement + external Track import in one remux.

## Evidence boundary

This is implementation-backed in one Matroska editor. Other formats may use different identity domains, reference graphs, or mandatory renumbering rules.

Do not promote to Canonical from this evidence alone.
