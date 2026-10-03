# Candidate: Post-operation visual verification should map source/output evidence by timeline time, not frame index

Date: 2026-10-03
Status: Candidate
Scope: media verification / VFR / transcode quality comparison

## Observation

A source frame and an encoded output frame cannot safely be paired by "frame N" when the operation may involve VFR input, CFR conversion, frame-rate changes, trim offsets, or other timestamp rewriting.

In Quick-Automatic-Hardsub-Encoder, post-transcode verification instead maps a selected output timestamp onto the source timeline using the verified actual start of the completed task. Source and output frames are then decoded independently through the authoritative FFmpeg paths.

## Candidate principle

For post-operation visual comparison:

- make output time the user-facing inspection coordinate;
- derive source time from the completed task's authoritative actual start plus output time;
- do not use nominal frame number as the cross-file authority;
- retain the extracted source/output timestamps with the evidence;
- invalidate previously extracted visual evidence when the inspection timestamp changes.

This prevents a comparison UI from presenting stale or semantically misaligned frames as if they were a valid quality A/B pair.

## Limits

- Time mapping alone does not solve deliberate spatial transforms such as crop, scale or rotation; those must be disclosed or normalized separately.
- Hard-sub verification needs a rendered reference (source + authoritative subtitle renderer), not the raw source frame, because subtitles are an intentional difference.
- Decoder seek semantics still determine which decoded frame represents a requested timestamp.

Do not promote to Canonical from this single implementation.
