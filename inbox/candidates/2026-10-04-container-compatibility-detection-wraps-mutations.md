# Candidate: Compatibility and detection should wrap container mutations, not be replaced by them

Status: **Candidate / architecture integration observation**
Date: 2026-10-04

## Observation

When a media workflow evolves from a video-centric soft-mux tool into a generic container editor, existing compatibility, capability-detection, diagnostics, and post-output verification work should not be discarded or rewritten as feature-specific checks.

The broader resource model makes these layers more important because a planned mutation may be structurally valid in the container while unsupported by the current writer, poorly supported by downstream players, or semantically risky for a renderer.

## Candidate rule

Model the editing pipeline as distinct evidence stages:

1. **Observed facts / detection** — what the source container, runtime, renderer, ABI, tracks, attachments, chapters, tags, and resources actually expose.
2. **Capability / compatibility evaluation** — what the current toolchain and selected target profile are known to support for a proposed mutation, with explicit supported / warning / unsupported / unknown states.
3. **Planned mutation** — the requested container changes, without claiming success before execution.
4. **Execution** — perform the remux/edit through the authoritative writer/container path.
5. **Verified output** — re-open the produced artifact and compare expected changes plus preservation invariants.

Compatibility should be target-aware rather than one global boolean. Container legality, local writer capability, renderer behavior, and downstream player behavior are separate dimensions.

Existing QC, Compatibility, and Diagnostics may share a presentation surface, but they should retain distinct semantics:
- QC: content correctness / repairable authoring problems;
- Compatibility: target-environment interoperability risk;
- Diagnostics: actual runtime/tool/renderer state.

## Example

For a PNG cover image:
- Matroska attachment storage may be supported;
- the local writer may support generic attachment insertion;
- the produced file can be verified to contain `image/png`;
- whether a particular player displays that attachment as cover art remains a separate downstream-compatibility fact and may be unknown.

## Evidence boundary

This candidate integrates existing ASS-Workbench reliability principles with the new generic container mutation direction. It is not a claim that every compatibility dimension is already implemented.

Do not promote to Canonical from this observation alone.
