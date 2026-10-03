# Candidate: Editing UI should distinguish requested boundaries from execution-realizable boundaries

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, media-processing, reliability

## Summary

When an editing operation cannot realize an arbitrary user-requested boundary without changing the operation semantics, the UI should preserve both values:

- the **requested boundary**: what the user selected;
- the **execution-realizable boundary**: what the chosen operation can actually honor.

Do not silently replace one with the other, and do not render the requested marker as though it were already executable.

## Observed media case

For stream-copy / lossless video trim, the requested IN point may fall between decodable random-access points. The current implementation resolves the actual start to the previous video keyframe rather than re-encoding.

A timeline that shows only the requested IN marker makes the operation appear frame-exact even though execution will start earlier.

Quick-Automatic-Hardsub-Encoder PR #36 therefore presents:

- the user's requested IN marker;
- video keyframe distribution as a distinct lane;
- the actual lossless start as a separate marker;
- the requested-to-actual time delta;
- previous/next keyframe navigation;
- an explicit “align IN to keyframe” action.

OUT remains a requested boundary and is not falsely presented as requiring keyframe snap.

## Candidate rule

For constrained editing operations:

1. Keep user intent and execution feasibility as separate state.
2. Visualize the constraint source when it is useful for decision-making.
3. Preview the execution-realizable result before execution when possible.
4. Offer an explicit alignment/snap action, rather than silently mutating the user's requested value.
5. Revalidate the constraint in the execution backend; UI preview is not execution authority.
6. Do not leak this constraint into modes where it does not apply. Re-encoding modes may retain frame-accurate requested boundaries even when stream-copy mode cannot.

The same structure may apply outside media editing where a requested value is quantized or constrained by the execution substrate.

## Evidence

Source project: `11576865/Quick-Automatic-Hardsub-Encoder`

Implementation:
- PR #36, merged as `7d2c72506544f8353b7de23ee9caec0da5bd5868`;
- Web FFprobe keyframe scan;
- Windows Native FFprobe keyframe scan;
- Android Native FFprobe keyframe scan;
- timeline ruler, keyframe lane, requested IN, actual lossless start and delta;
- execution backends independently revalidate the previous keyframe.

Automated evidence:
- keyframe extraction unit test;
- cross-backend keyframe timeline wiring test;
- real FFmpeg integration already exercises `-skip_frame nokey` and packet-identical stream-copy output;
- Playwright smoke verifies requested 8:20 -> actual 8:00 -> explicit snap;
- UIGS invariant `MEDIA.COPY.KEYFRAME.TIMELINE_SEMANTICS`;
- Windows smoke, Android compile, frontend tests and UIGS Evidence Coverage passed on the PR head.

Visual evidence:
- CI captures the analyzed mobile copy timeline with keyframe lane and requested/actual markers.

PR #40, merged as `09b67ee4ed774fa258365e9aee2717e23855efca`, strengthens the same pattern with source-frame evidence:
- scrubbing the timeline decodes and displays the source frame at the current cursor;
- Copy mode displays the requested-IN frame and the execution-realizable keyframe-IN frame side by side;
- the two visual values remain separate from the execution authority; the backend still independently resolves the keyframe at run time;
- Web, Windows Native and Android Native expose the same frame-preview semantic path;
- real FFmpeg integration verifies source-frame extraction at distinct timestamps;
- Playwright exercises the cursor preview and requested-vs-actual boundary inspector;
- UIGS invariant `MEDIA.TIMELINE.SOURCE_FRAME_PREVIEW` binds source, test and workflow evidence.

This is stronger evidence for “preview the execution-realizable result before execution” but is still one product implementation, so it does not justify Canonical promotion.

## Scope / non-claims

This does not imply that all stream-copy endpoints must be keyframes, nor that every codec/container has identical seek semantics. It captures the product rule: the UI must expose the actual constraint used by the execution path instead of implying precision the operation cannot provide.

This is a Candidate only. It is not Canonical.
