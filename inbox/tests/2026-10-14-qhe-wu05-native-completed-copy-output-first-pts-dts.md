# Test: QHE WU05 independent completed-cut output clock receipt

Date: 2026-10-14
Status: PASS — exact-head Windows hosted B-frame output receipt and Chromium/model at e848e; subsequent start-clock warning CI pending
QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Windows PASS: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38567583986
Chromium/model latest PASS at e848e: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38567583926
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
## 2026-10-14 real Windows acceptance result

Actual Windows FFmpeg 9.0.2 produced H.264 B-frame/AAC source and used QHE shared schema-v4 to compile and execute Stream Copy Trim through localhost Native Bridge. The read-only endpoint returned the job-bound first decoded video PTS, first encoded video packet PTS/DTS, and first audio packet PTS. Independent FFprobe of the private completed MKV verified its first decoded frame matches the receipt:

- requested source cut IN/OUT: 2.400–4.800 s;
- actual first decoded presentation in OUTPUT clock: 2.000 s;
- first output video packet PTS/DTS: 2.083 / 2.000 s;
- first output audio packet PTS: 0.005 s;
- actual completed artifact: 58,863 bytes;
- copiedPacketRange remains null, source mapping and full A/V sync explicitly unverified.

Real Windows run `38567583986` SUCCESS; it followed a test-harness-only error at `38567204535` where PowerShell 5.1 default ANSI Get-Content corrupted the Node-produced UTF-8 JSON formal task. Sending the original UTF-8 JSON bytes fixed transport. This is a bounded B09/A04 product capability, not total A04 closure or universal B-frame/VFR success.
