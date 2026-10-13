# Test/Observation: bounded codec × preset candidate set

Date: 2026-10-13
Source: QHE PR #105 continuation after a954ba6
Status: local compiler and actual FFmpeg tasks passed; hosted comparison UI Pending

Dedup: queried inbox/tests/2026-10-13-qhe-heterogeneous-audio-plan-and-source-owned-ui.md. Existing source-owned intent/evidence family retained; this narrow test adds preset combinations, not universal optimization or a Canonical rule.

Optional Windows manual comparison offers legacy x264/x265 medium (12 short samples) or finite x264/x265 × medium/fast (24). Both use unchanged two-window, three-CRF, source SDR yuv420p protocol and existing reported encode-time budget. Each branch has a unique codec/encoder/preset identity. Candidate policy change invalidates old session and VBR authorization. Candidate lookup during verification and adoption comes from the session's actual frozen set, avoiding a fixed two-codec catalog. One chart, common evidence domain, no automatic task change; VBR verification and explicit adopt remain required.

Local two new tests failed before implementation; after: Node 225 pass/8 conditional skips, Vite build pass. A real FFmpeg regression compiles all four plans, independently checks codec/160x90/24 frames, and fully decodes each output. This verifies basic encoder/preset execution, not actual Native four-branch quality measurement. Real-DOM browser fixture covers four branches, policy invalidation, VBR review and adopted fast preset without automatic adoption; CI Pending, local Chromium absent. Finite source-size candidates only; resolution/AV1/VVC/GPU joint comparison remains unsupported. No global-optimum, subjective-quality or physical-device claim.

Previous head a954ba6 all nine workflows passed; Android previous V4D-06 timing failure did not recur in 38355738585, but its root cause is unresolved, so no claim of a fixed intermittent defect.
