# Test: QHE guided integer budget feasibility and verified output streams

Status: **Pending CI / implementation submitted**  
Date: 2026-10-11  
Source project: `11576865/Quick-Automatic-Hardsub-Encoder`  
PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/89  
Head: `b6feb839a10e22f669eae39ec7e0078976f57668`

## Contract under test

1. A Guided target-size budget that cannot accommodate the current estimated audio, container reserve, and minimum executable video bitrate must be refused before FFmpeg, with an actionable numeric explanation. A feasible but low-quality target must not be called mathematically impossible.
2. A Guided Windows Native output must not become completed/exportable based only on a readable video header. Validate one video stream, requested audio count (if supplied), positive/near-expected duration, and a stream-copy packet scan. The strict container byte ceiling remains an independent final acceptance gate.
3. Two actual source audio tracks are retained by a software two-pass `audio=copy` job, including the strict under-ceiling path.

## Submitted test paths

- `src/guided-size-policy.test.mjs`: 1-byte-below/at feasibility boundary, audio bitrate sensitivity, fixed vs percentage reserve, invalid inputs.
- `scripts/check-guided-budget-native.ps1`: real Windows FFmpeg/localhost Bridge, synthetic FFV1 video + two PCM audio tracks, software two-pass and strict byte ceiling, existing staged-file oversize tamper/export refusal checks.
- `windows/native-bridge.ps1`: terminal stream/duration/packet guard before completed state.

## Evidence and limits

This intake was recorded at **branch/PR submission**. CI was not polled after submission. Nothing here is a claim that Windows runtime validation passed or that the full long-form hardware matrix completed. The packet scan checks demux/packet integrity, **not** full decode, cryptographic content integrity, picture quality, or post-export reopen. Physical device/long-media coverage remains FIELD-PENDING in QHE issue #77.

Related existing Candidates:
- `inbox/candidates/2026-10-03-impossible-target-budgets-must-explain-the-constraining-component.md`
- `inbox/candidates/2026-10-03-cross-boundary-invariant-coverage.md`

Do not promote to Canonical from this checkpoint.
