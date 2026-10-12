# Bug: Windows PowerShell sends Unicode formal Media Task JSON as string, Native Bridge parse fails

Date: 2026-10-13 (Asia/Shanghai)
Status: **Fixed at CI caller; regression tested by real full Native job**
Lifecycle: validation-pending
QHE source: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104 (draft/unmerged)
Scope: transport in Windows CI; do NOT infer a browser client production bug without separate proof
Evidence: first full-job CI `38283951323` failed; follow-up `38284134399` passed after UTF-8 bytes fix

## Reproduction / failure

The **same real native source** and its 12 paired CQ x264/x265 windows and 2 actual x265 VBR windows succeeded. `build-manual-adopted-native-request.mjs` accepted real VBR receipts, performed the atomic form transaction and compiled a valid HEVC+copy-audio task v4. But the new test harness sent its **pretty-printed JSON including a non-ASCII Chinese FLAC compatibility warning** to `POST /api/encode` using Windows PowerShell `Invoke-RestMethod -Body $requestJson` as a string.

`windows/native-bridge.ps1::Read-HttpRequest` determines body size from HTTP Content-Length, reads that exact number of **bytes** and decodes UTF-8. On that Windows runner the string-body encoding/length did not agree with Bridge's UTF-8 interpretation. The Bridge's `ConvertFrom-Json` threw `Invalid array passed in, ',' expected. (1069)` before reaching FFmpeg. The HTTP request was rejected, despite all prior short samples being valid.

This is a **transport/protocol encoding mismatch in the CI harness**, not evidence that HEVC, audio copy or Native formal encoding was broken. The earlier short-sample requests used ASCII-only compact PowerShell-generated JSON and did not expose this boundary.

## Remedy

Use `$requestBytes=[Text.Encoding]::UTF8.GetBytes($requestJson)`, then `Invoke-RestMethod -Method Post -ContentType 'application/json; charset=utf-8' -Body $requestBytes`. Body byte length and actual UTF-8 contents now agree with Bridge's decoder. The exact real 5s formal Windows Native job successfully encoded HEVC, preserved 235/235 copied FLAC packet payload SHA256, verified 60 frames/5 seconds, 358516 output bytes, full source-reference SSIM 0.999738, in follow-up run `38284134399`.

Do **not** silently remove Unicode-compatible warning strings from the formal task to work around the problem; keep full source/task semantic data and fix its actual transport encoding.

## Follow-up / scope

The actual browser client network transport has **not** been proven defective by this incident: different runtimes can send UTF-8 correctly. Test any other PowerShell/CLI clients carrying non-ASCII Media Task JSON. Separate the evidence: correct encoding at the caller, strict Content-Length and UTF-8 decoding at server, successful schema acceptance and actual encoding. This one case belongs in Bug/Test, **not Canonical** without dedup across other projects.
