# Observation: a demuxer stream projection is not the stored container object kind

Status: observation
Date: 2026-11-03
Domains: media-processing, container-modeling, preservation, independent-output-validation
Maturity: single bounded implementation/fixture family; not Canonical

## Distinct observation

A valid Matroska image AttachedFile is physically FileData, yet FFprobe can expose it as codec_type=video with disposition.attached_pic=1 and filename/mimetype tags. In a native counterexample, remuxing that projection using -map 0 -c copy changed the picture into a Matroska video track: attached_pic became0 and the original AttachedFile identity was lost. Stream Copy did not preserve its object role.

A container workbench must distinguish the physical EBML object from a tool's stream projection before choosing the write operation. Re-labeling a UI row alone is insufficient: exclude the raw image stream from stream mapping and use the actual source FileData when preserving it as an attachment. Unique source-name/MIME binding and bounded actual-byte reads can fail closed rather than guessing identity. This observation concerns Matroska image AttachedFile; it does not redefine ISO BMFF cover-art stream semantics.

## Product implementation and evidence

Softmux https://github.com/11576865/MKV-Fast-Muxer/pull/224; implementation commit 6a8296514fc9d7d5606e1d424b51e3a54ef7e9c8. Product source/tests remain authoritative.

- tests/media-attachment-delivery.test.mjs covers Matroska-only normalization, physical source FileData binding, raw stream negative mapping and ordinary payload rejection on wrong SHA/MIME/name.
- tests/e2e/media-attachments-scenario.mjs generates real browser outputs with retained original PNG, source filename edits/selection, uploaded fonts and ordinary PNG/PDF/explicit opaque JSON, checking independent native payload extraction, complete source/output SHA and media packet PTS/payloads.
- Actual source picture remains FileData after default and selective paths, instead of becoming a movie track. New ordinary payload verification remains separate from font evidence and FFprobe counts.
- Source-image reattachment currently permits <=16MiB each/32MiB total and requires unique physical binding. UID/target-reference/complete EBML or arbitrary player/device preservation is not claimed.
- Local839 Node tests/build and five mixed outputs plus three original-route regression outputs passed. Hosted exact-head CI pending.

## Intake lineage

Searched UIGS-Foundry for attachment/image/attached_pic; no exact prior entry returned. This is one Observation from one fixture/implementation family, not independent multi-project confirmation. It proposes no Canonical change or global capability promotion.
