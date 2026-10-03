# Observation: Integration harnesses must reproduce executor staging semantics before interpreting platform failures

Status: observation
Date: 2026-10-03
Domains: testing, ffmpeg, windows, staging
Evidence type: failed acceptance harness corrected against production executor behavior

## Observation

The first Windows run of Quick-Automatic-Hardsub-Encoder's AV1+ALAC acceptance test failed in the ASS filter because the test harness substituted absolute Windows paths directly into an FFmpeg filter graph:

`ass=C:\...\subtitle.ass:fontsdir=C:\...`

FFmpeg filter syntax treated the drive-colon/backslashes as filter syntax and rejected the graph.

That failure did not reproduce the product's Windows Native execution path. The real executor stages `subtitle.ass` and `fonts` inside a per-job working directory and substitutes relative names into the validated filter graph.

After the harness was changed to run FFmpeg with the job directory as `cwd` and use the same relative asset names as production, the identical AV1+ALAC acceptance passed on Windows.

## Reusable implication

A cross-platform integration test should mimic the production executor's staging, working-directory and argument-escaping boundary before a platform-specific failure is classified as a product bug.

Otherwise the test can manufacture a portability defect that the production path deliberately avoids.

This is an Observation only. It is not Canonical.
