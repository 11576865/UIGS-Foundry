# Test: QHE WU05 independent completed-cut output clock receipt

Date: 2026-10-14
Status: PENDING exact-head Windows Native real B-frame run; Chromium plus model hosted run PASSED at earlier head 233efb
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Windows run: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38567583986
Chromium/model run: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38566621375
Owner report: R19 §06 pp6–7 and R24 §09 pp12–13; B09/A04; independent full-report denominator unchanged.

## Delivered code under test

The completed Windows Native Stream Copy trim can be inspected with an optional, read-only localhost endpoint. Bounded real FFprobe queries observe output-clock first decoded video presentation (best_effort_timestamp_time), first video packet PTS/DTS, and first packet PTS/DTS for each output audio stream. The frontend binds the receipt to completed job ID, byte size and execution-seek identity, displays separate source requested IN/OUT versus *output* presentation clock and includes the observation in the existing JSON report. Failure cannot invalidate an otherwise verified, still-saveable artifact.

## Falsifiable test conditions

- Existing model and real Chromium test checks a deliberate wrong-job response fails without blocking save, a correct receipt appears, is exported with copiedPacketRange:null and sourceMappingVerified:false, and source changes hide stale inspection.
- Actual Windows hosted test generates H.264 with B frames and AAC, uses the official schema-v4 compiler to create Stream Copy Trim, executes it in real localhost Bridge, obtains actual completed artifact's timeline receipt, independently FFprobes the staged output frame and compares the first decoded presentation.
- Output PTS/DTS versus input/source timeline and copiedPacketRange source packet hash mapping are intentionally unverified; bounded first-packet observation cannot close VFR/B-frame full alignment or last-output-frame acceptance.

## Early diagnostic

Initial real Windows run 38567204535 successfully generated B-frame source and compiled the official task but failed at HTTP transport because PowerShell 5.1 re-read the UTF-8 formal JSON with default ANSI encoding, corrupting Chinese compatibility messages. Corrected by posting original JSON bytes at QHE commit e848e186512bfd782dbd31edff7d8fe1930fa7cb. This is a test-harness transport issue, not proof of a video encoder defect. Real exact-head result is pending.

No Canonical promotion. Distinct from prior QHE trim-copy cost-only audit and keyframe-prediction-only Candidate: this is an actual completed output presentation/packet time observation.