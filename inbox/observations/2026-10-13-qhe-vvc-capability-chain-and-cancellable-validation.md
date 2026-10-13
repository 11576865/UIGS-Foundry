# Observation: VVC capability chain and cancellable output validation

Date: 2026-10-13 (Asia/Shanghai)
Status: Observation / implementation + local Node acceptance; Windows/browser runtime Pending
Project: 11576865/Quick-Automatic-Hardsub-Encoder
Source: PR #105 https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/105
Code revision: 87d0ae59d8da6d9e38a93442362c1b651239cf64

## Dedup / family
Existing REL.CAPABILITY_PROVEN_BY_OUTPUT already covers enumerated names versus real output. ARCH.RUNTIME.EXCLUSIVE_RESOURCE_OWNERSHIP covers owned long tasks. This is a scoped implementation observation in those families, not a new Canonical rule. Current Foundry tree was queried before capture; no VVC-specific case found.

## New implementation facts
VVC/libvvenc availability requires a tiny real MKV encode, independent FFprobe codec/pixel-format/frame-count inspection and full FFmpeg decode under bounded probe timeouts. UI accepts only the protocol encode-mkv-decode-v1, Windows runtime availability, QP support and yuv420p10le. The formal output decoder runs as a second owned asynchronous process, with validating status and existing cancellation/exclusivity guards. VVC is excluded from a legacy selector whose acceptance contract is weaker.

QP differs from CRF/CQ: compiler and manual short trials use integer 0..63, preserve endpoint requests, and reject foreign flags/presets. The existing rate-distortion calibration is not implicitly extended to VVC.

## Evidence and limitations
Local Node suite: 190 PASS, 5 conditional skips, 0 failures. Existing real FFmpeg task integration: 3 PASS. Vite build PASS. New QP endpoint and capability regressions observed RED then GREEN. An independent review identified synchronous decoder blocking, wrong trial bounds, and legacy-path leakage; addressed in the proposal.

No local VVC encoding evidence: installed Linux FFmpeg lacks libvvenc. Local Chromium unavailable and download returned an invalid archive. Windows executable argument/lifecycle tests plus actual Bridge QP/bitrate jobs, and browser capability fixtures are committed but Pending CI. UNSUPPORTED must remain distinct from runtime PASS. Physical devices, HDR, Android/Web VVC distribution and external players remain unverified. Inherited PR #104 media evidence is not independent confirmation of VVC.

## UI mapping
Intent: show a manually selected codec only when the current backend can execute and validate it.
Pattern family: UIGS.NAVIGATION.CAPABILITY_CATALOG + REL.CAPABILITY_PROVEN_BY_OUTPUT.
Realization: disabled H.266 option with scoped reason; experimental available state; QP-labelled controls and constrained presets.
Expected effect: no silent encoder fallback or false cross-platform availability.
Validation: src/vvc-capability.test.mjs, src/vvc-task.test.mjs, scripts/check-vvc-ui.cjs, scripts/check-vvc-native.ps1.
Known failures: catalog-only capability, CRF treated as QP, legacy path bypass, blocking validation. No Canonical promotion.


## Required runtime lane follow-up, 2026-10-13 (Observation; hosted Pending)

Prior exact-head green Windows CI still reported actual VVC UNSUPPORTED: libvvenc absent. Add a separate required-runtime lane; generic smoke may report unsupported, dedicated acceptance must fail if runtime absent. Resolve official BtbN FFmpeg release asset and verify published SHA-256 before running isolated binaries; record release/asset/digest/version. This confirms download integrity relative to upstream metadata, not independent upstream trust or floating-latest reproducibility. Exercise QP and bitrate transcode plus ASS hard-sub through real Bridge, followed by independent FFprobe 24-frame VVC/10-bit and full decode, retaining generated MKVs. No user-toolchain mutation or product distribution.

Local fixture tests RED→GREEN, total Node 213 pass/7 conditional skips, build pass, YAML syntax pass. PowerShell/actual encode/mux/decode Pending hosted workflow. Do not promote to runtime PASS or Canonical before reading actual receipt. Same project lineage; physical/long-form/player/subtitle perceptual fidelity unverified.


## Hosted runtime bug and parser repair (2026-10-13)

Workflow 38344020498 verified official asset 633881560 and progressed beyond real VVC short probe/Bridge health; first formal request was refused with FFmpeg encoder does not support -fps_mode. Production global help regex missed optional stream-selector suffixes such as -fps_mode[:<stream_spec>]. Normalization now extracts base flags and is shared with toolchain scoring; compiler/backend whitelist is unchanged. Two regressions execute the actual regex RED->GREEN; .NET helper fixtures added to required CI. Full help/capability/bridge logs retained. Local suite 215 pass/7 skip, build/YAML pass; hosted formal QP/bitrate/ASS task acceptance Pending after one bounded repair. Do not infer three formal task acceptance from short probe success; no Canonical promotion.
