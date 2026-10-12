# Candidate: Diagnostic curves must not be represented as an optimized decision frontier

Status: Candidate
Date: 2026-10-10
Domain: product semantics, optimization UX, engineering evidence

## Context
A review of Quick-Automatic-Hardsub-Encoder after PRs #67–#72 found that its Windows Native manual-transcode workflow now produces real measured quality-search traces and a single-configuration rate-distortion curve. The broader user goal was a time-budgeted Compression Decision Engine that could compare competing codec/resolution branches and produce a justified recommendation at a selected target size.

These are different evidence and decision contracts:
- diagnostic exploration: what was measured for the selected configuration and sampled scenes;
- single-branch estimation: an interpolation within observed bitrate bounds;
- cross-branch decision frontier: the best supported candidate across relevant alternative configurations, with uncertainty and cost explicitly accounted for.

## Candidate rule
Do not promote a diagnostic curve or single-branch fitted line to the semantics of a globally optimal decision frontier.

A decision-facing surface should declare:
1. candidate space actually explored;
2. evidence modality (measured CQ/CRF output, inferred target-size, true final-encode verification);
3. uncovered candidate families and sample regimes;
4. sampling/calibration time already paid and remaining budget;
5. whether the selected configuration is a recommendation, a provisional local winner, or merely a user-inspected alternative;
6. rate-control-mode changes between measurement and execution, which invalidate any implication that the same quality is guaranteed.

## Evidence
- Quick-Automatic-Hardsub-Encoder PR #67: measured exploration and efficiency curves for current Windows Native encoder/preset, explicit caveat that selecting target bitrate differs from CQ measurement.
- PR #68: quick/balanced/thorough fixed sampling profiles; long-video safeguards but no value-of-information stopping rule.
- PR #69: UI differentiates measured points, fitted curves, observed dispersion, and local knee.
- PRs #70–#72: stale-evidence and chart-validity corrections.

## Verification boundary
The review is based on current-main code and PR metadata, not a field test on the user's actual machine. This is a Candidate, not a Canonical rule.

## Scope and user-intent review (2026-10-10)

The user explicitly challenged the introduction of two separately exposed “exploration” and “efficiency” charts in Quick-Automatic-Hardsub-Encoder: they had requested a target-size/quality decision curve and eventual cross-resolution/codec comparisons, not necessarily two manual-transcode diagnostic charts. Available historical discussion supports the original draggable target-size/quality decision surface and cross-branch optimization intent; it does **not** establish an explicit request for the two separately named diagnostic surfaces. Absence of a located authorization record should be reported as an evidence gap, not proof that none ever existed.

Reusable scope-review observation:
- Distinguish a user-requested *decision abstraction* from an engineering-chosen *diagnostic presentation*. The fact that search traces and single-branch measurements exist does not authorize elevating each internal representation into a prominent user workflow.
- For each new primary UI surface, retain a concrete chain: source user task or explicit approval -> decision/operation enabled -> necessary user interaction -> implementation and validation evidence. Technical usefulness, CI success, and merged PR status do not themselves establish demand.
- Investigate less intrusive realizations first: preserve accurate measured evidence and optional diagnostics, but favor concise actionable recommendations and progressive disclosure when detailed search traces are not needed for the primary task.
- Evaluate opportunity cost against unresolved higher-priority user constraints: bounded calibration time, representative sampling, and cross-configuration upper-envelope decision-making.
- Do not infer that the user's objection requests code deletion or reversal of all rate-distortion modeling. Scope disposition remains a product decision, not a completed change.

Evidence: user feedback during a 2026-10-10 project-status reassessment; recorded original October 3 user intent; QHE main `2eeaab388851008a72c653aaf9f0f14560262b76`, particularly `src/transcode-calibration-panel.js` and PRs #67–#72. This extension remains **Candidate** and does not alter any Canonical rule.

## Explicit single-curve direction and implementation (2026-10-10)

The user explicitly requested that the exploration curve be merged or removed because the compression workflow should present only one curve. The chosen implementation removes the standalone exploration plots in **both** the manual transcode panel and the guided hard-sub quality panel, while retaining actual CQ/CRF sampling, measurement provenance, and progress/target status. Manual transcode retains one interactive target-size/SSIM frontier; individually tested CQ/CRF settings and adoption controls are available in a collapsed details section under the graph.

- QHE PR: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/73
- Branch: `fix/single-measured-compression-curve`
- Commit: `7b4f635d97e45422717a27d5c3c975f70ad95319`
- State at submission: PR open; CI pending; not merged; no hardware/device acceptance.
- Reusable boundary: a diagnostic search trace may remain operationally essential without occupying a primary user-facing visualization. Preserve the underlying observations and parameter-selection affordances when collapsing the diagnostic surface.
- This is one product-specific disposition and does not automatically prescribe a single curve for every application.

This is an update to the existing Candidate, not a new duplicate or Canonical promotion.

## Follow-up implementation: single curve plus evidence integrity (2026-10-10)

The user requested continued implementation. QHE PR #73 now has a second commit `a98d291ad53e12e9dad557595214bead555d17b7`: the existing single-curve design remains while completed sample measurements are reusable across decision-only threshold/audio-budget changes. Live sampling still rejects changed run identities; source/encoder/sample-profile changes remain incompatible. Pure tests, browser lifecycle regression, and documentation were extended. PR remains open; latest-head CI pending.

This concretizes the distinction between a primary decision surface and internal diagnostics; it does **not** establish a global upper envelope or measured VBR equivalence. No Canonical promotion.

## Single-curve baseline merged; next decision module pending (2026-10-10)
QHE PR #73 is **merged** into main after Frontend, Windows and UIGS evidence CI passed. Merge SHA: `7b6cddfe766a9a0f70fd67442bf14170cd9438e8`. Its single-curve interaction and strict raw calibration evidence are now the mainline baseline, not merely a proposed PR.

The next multi-codec envelope and VBR validation implementation is tracked separately at https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/74 and was **unmerged, CI/device acceptance pending** at this checkpoint. No Canonical promotion.


## 2026-10-12 Manual comparable-evidence contract PR #104: actual isolated implementation checkpoint

QHE owner requested continuation after delivery of the 18-page architecture/decision report and draft PR #103. A second **independent draft** [QHE PR #104](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104) was created from QHE main `de8bfb476b7f35b952db88bcaf5b4d2c9ed44d38`, proposal head `8b5c437809aae3c22524f261c4c9811467737105`. It does not depend on #103.

What exists (CODE + CI; **not** Manual UI or physical FFmpeg proof):
- `src/manual-transcode-comparison.js` adds a **session-only read-only** `createManualTranscodeComparison` contract. Candidates must identify the same source token, runtime/build token, direct source-SSIM reference protocol, no-filter processing, selected video stream, trim interval, original/reference dimensions, versioned sample plan and exactly paired windows.
- Every CQ trial must supply at least two distinct valid bitrate points with measured SSIM/duration/bitrate on **all shared sample windows**. Synthetic tests cover rejection of missing, shifted, wrong-duration, invalid-numeric samples and summary values that do not match raw window averages/minima.
- A complete candidate set reuses QHE's existing `fitRateDistortionModel` and `createMultiBranchFrontier`; the upper envelope is confined to common measured output-budget ranges. Output size planning requires an explicit audio-budget evidence kind, not an unknown copied-audio budget silently treated as zero.
- The result returns `sessionOnly=true`, `adoptionRequiresNativeVbrVerification=true`: CQ comparison does **not** authorize automatic encoder changes or promise formal VBR/final-size equivalence.
- `src/manual-transcode-comparison.test.mjs` is wired into `.github/workflows/test-frontend.yml`; documentation `docs/manual-transcode-comparison-evidence.md` distinguishes test fixtures and next-stage acceptance.

Exactly scoped proof: QHE Test frontend GitHub Actions run `38263407888` **success** and UIGS Evidence Coverage run `38263407783` **success** for exact proposal head. The model is tested with synthetic protocol/evidence only, not actual multiple real NVENC/x264/x265 samples, and its source/runtime tokens are assertions rather than cryptographic content verification.

User impact: PR #104 does not modify the Manual interface, source-video FFmpeg execution, the Guided ASS estimator, lossless Stream Copy or the task v4 schema. The already installed Manual single-branch curve continues to work unchanged. PR #104 remains **draft/unmerged**; owner review and real/native comparison acceptance pending.

Reusable boundary: **rate-distortion model code reuse is not comparable measurement reuse**. The cross-branch optimizer should receive *paired, protocol-versioned, same-reference evidence*; it must not repair mismatched evidence by chart interpolation or presenting convenient codec labels. This is an extended Candidate, not Canonical or a claim of existing cross-backend parity.


## 2026-10-12 native provenance receipt follow-up: PR #104 exact-head CI, not cross-codec acceptance

In QHE draft [PR #104](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/104), latest tested head `d163ef4be15c8e77dafc5cd02f0eb46848ba04f6`, Windows `Invoke-Sample` acquired an **optional** `nativeEvidence` receipt on exact, source-SSIM, no-subtitle samples. `windows/manual-sample-evidence.ps1` identifies source and FFmpeg runtime from full file path, size and LastWriteTimeUtc; runtime token also includes the FFmpeg version banner. Samples snapshot both source and runtime before and after encoding; changed stat token rejects the receipt. CQ and VBR use distinct method IDs, preventing evidence-mode conflation. The JS `admitManualNativeCqSample()` rejects missing or mismatched native tokens, reference/filter protocols, codec/encoder/preset, timing window, encoding quality and invalid SSIM/packet bytes. Current Manual single-branch operational flow is unchanged: the verifier is future infrastructure, not a shipped GUI decision flow.

**Identity caveat:** `stat-sha256:...` is SHA-256 over file metadata, *not* full media/FFmpeg executable content hash and *not* proof of decoded-frame equality. It is a scoped accidental-staleness guard and should never be shown as a content-integrity guarantee.

**CI precise result:** on `d163ef4be15c8e77dafc5cd02f0eb46848ba04f6`: Test frontend `38266242799` **success**; Windows local smoke `38266242696` **success**; Windows Stream Plan v4 acceptance `38266242680` **success**; UIGS Evidence Coverage `38266242659` **success**. Windows smoke creates a *real* FFmpeg input, checks the receipt's source/runtime stamps, distinguishes CQ and VBR, modifies the source and asserts the pre-sample evidence can no longer be accepted. The previous failed Windows runs were traced to a new test placed before FFmpeg installation, then an inherited PowerShell external-process exit code; those were corrected in the exact-head green version. Preserve that failure/fix record rather than silently report first-run green.

**Not proven:** running two distinct actual codec encoders through the bridge, collecting same-window full native quality observations, correctly republishing a Manual multi-branch curve, physical NVIDIA hardware performance, long-video field behavior, end-to-end immutable file identity, or any real-user UI screenshots. No merge, product declaration or Canonical change. Follow up by connecting real native sample receipts to an actual versioned per-candidate registry and corresponding matched-window field acceptance.


## 2026-10-12 real dual-software-encoder Bridge acceptance (PR #104)

The evidence boundary has advanced beyond synthetic JS model fixtures. QHE's independent `Windows Manual paired codec acceptance` runs an actual localhost Windows Native Bridge against a generated FFV1 synthetic video, with two software encoders (`libx264`, `libx265`), three actual CQ/CRF settings (18/28/40), and two paired 1.5-second windows (0.25 s and 3.0 s); 12 native calls in all. Each native SSIM/packet-byte result is admitted via `admitManualNativeCqSample`, summarized only after complete paired measurements, and evaluated by the real `createManualTranscodeComparison`/upper envelope engine. No fake SSIM or mock codec paths are used.

Exact proposal head `3f1b4fbc1d6a2c02c269f920a9db92adf04a9c52`, hosted Windows run `38268364465` **PASS**. Observed per-sample SSIM approximately `0.93529..0.99828`; common measured/projection byte budget approximately `39986..149237`, for that **specific synthetic source**. Fitted upper-envelope selection at midpoint reported `h264-x264` in this fixture, not any general H.264 superiority. The earlier paired run `38268001729` also succeeded.

What is **not established**: actual Manual multi-branch UI state/history, bounded on-demand per-encoder scheduling on a user-selected film, active cancellation, final VBR-mode adoption and full output, NVENC/GPU, AV1, HDR/VFR, user-device equivalence, or general bitrate-quality codec ranking. Current local receipt identity is stat-based, not content cryptography.

The proposal also encountered an unrelated hosted Windows CI fault: Chocolatey FFmpeg feed HTTP 504 caused missing `ffmpeg`, while an unguarded setup command let the domain test appear at fault. A bounded three-attempt installer exit-code guard was added to both Windows workflows. Separate Bug: `inbox/bugs/2026-10-12-windows-ci-ffmpeg-chocolatey-504-unchecked-install.md`. Distinct real-native Test: `inbox/tests/2026-10-12-qhe-native-bridge-paired-x264-x265-comparison.md`. Keep this a Candidate; no merge or Canonical promotion purely on passing CI.


## 2026-10-12 session-scoped candidate evidence registry now implemented/tested — QHE PR #104

Draft QHE PR #104 head `694dc6bfb05596fb40accfa36140c305a2b9ba30` now contains `src/manual-transcode-session.js`. The new session is an **experimental read-only, bounded paired-candidate evidence authority** with frozen source/reference/runtime/time window protocol; it is not yet connected to the consumer Manual UI. Individual Native CQ observations are keyed by candidate + CRF + source window. Only a *complete set of windows* creates a fit-eligible R–D point; previous fully complete quality settings survive a cancelled exploration while the partial point is discarded. **Stale/incompatible native provenance invalidates all completed session evidence**, not just the arriving sample. Per-session candidate count, quality settings, sample count and measured encode seconds are bounded. Cooperative stop checks happen both before invoking Native and after its return; stopping does not claim actual FFmpeg interruption. Read-only `compare` passes only complete, eligible branches to the existing common-domain upper envelope; the original one-branch Manual calibrator is unchanged.

Exact-head GitHub CI **five green**: Test frontend `38270515303`, Windows Manual paired codec acceptance `38270515270` (12 actual Windows x264/x265 source-backed FFmpeg samples routed through the new session), Windows local smoke `38270515272`, Windows Stream Plan v4 acceptance `38270515300`, UIGS Evidence Coverage `38270515280`.

New deduplicated Test: `inbox/tests/2026-10-12-qhe-manual-candidate-session-atomicity-and-cancellation.md`. This advances measured data provenance and incomplete-sample atomicity but does **not** establish user-visible multicodec Manual UI, codec auto-adoption, duration/quality guarantee, physical GPU or long-film field acceptance. Remains a draft PR and Candidate, not Canonical.


## 2026-10-13 optional Manual x264/x265 consumer UI experiment in draft PR #104

QHE `src/manual-transcode-compare-ui.js` is now opt-in mounted beside the *existing* single-codec Manual calibrator: two native software codecs, two matched windows, three CQ settings, at most 12 samples on the intentionally restricted SDR yuv420p/no-transform Windows v:0 path. Data originates from the real source-backed Native CQ receipts and the versioned session registry. The same `#taskEfficiencyChart` is a **single-mode or multi-branch upper-envelope view**, never two competing chart state owners; details expose each fitted alternative at the **same video-only estimated budget** (copied audio/container are not included). The app still has no automatic codec/bitrate handoff: the existing exact configuration VBR check remains required before any formal bitrate adoption.

Real browser interaction regression with mocked Native transport: `scripts/check-curve-design.cjs` uses Chromium to check one chart, candidate table, keyboard/touch-size layout at 1280 and 390px, single/compare mode-specific controls, no auto-adoption, safe pixel-format rejection and evidence retention for threshold-only changes. See distinct Test `inbox/tests/2026-10-13-qhe-manual-comparison-one-chart-browser-and-native-separation.md`. Windows Native paired real FFmpeg integration remains separately tested. Both browser UI and Windows paired tests succeeded at `ca7c9261d1e6065e8357aa39149ddbe3a4790670`. Other exact-head CI must be checked individually before a whole-PR success declaration.

Independent screenshot review of a previous iteration found an extra *test fixture chart* still visible above the Manual workbench and single-encoder VBR controls left visible in compare view. Browser fixture and CSS were corrected rather than portraying the two-graph screenshot as product acceptance. Additionally, the original vertical axis legend `平均样本 SSIM` could falsely imply an arithmetic mean despite worst-window/fit-based samples. It was changed to `短样拟合 SSIM` and protected by a test. No observed actual video encode regression is claimed from these UI defects.

**Do not promote** to Canonical: client Native/real film field acceptance, AV1/GPU, subtitle-affecting reference and final VBR codec switch, actual saved output/size and long-form compatibility are all still open. Draft PR #104 not merged.


## 2026-10-13 QHE Manual selected-branch VBR check now implemented but formal adoption deferred

Draft QHE PR #104 head `c2f3cbf638aa30caf540aadd468bf5a8c8113bdd` adds a separate explicit Native bitrate-mode confirmation gate for the selected candidate from the existing one-chart CQ envelope. It is an **execution-mode bridge**, not automatic codec adoption: same-source/reference Native `windows-native-exact-vbr-v1` receipts, exact encoder/preset, disabled multipass, requested rate and every paired source window must match; SSIM minimum is checked against the user threshold. Repeating the curve's CQ interpolation or treating CQ receipts as VBR evidence is rejected.

A passing result remains a **short-window attestation**. It does not set formal codec/bitrate, prove full-length quality or output bytes. The GUI's status and graph readout now share one selected-budget/candidate/threshold-bounded VBR result. Independent image review caught and resolved a contradictory “VBR passed” versus “not verified” display. User interaction (keyboard moving volume budget, changing SSIM threshold, changing source) invalidates the prior current selection's VBR pass.

Exact-head CI **all five success**: Windows real Native paired x264/x265 CQ plus x264 VBR (`38278213526`), frontend/browser (`38278213258`), Windows smoke (`38278213254`), Windows v4 (`38278213362`), UIGS coverage (`38278213284`). True VBR path exercised two real FFmpeg windows at 600kbps on one 5-second FFV1 synthetic source. For full evidence/modeled vs real distinction see `inbox/tests/2026-10-13-qhe-manual-native-vbr-gate-and-readout-consistency.md`.

Remaining Candidate question: define atomic `codec + encoder + preset + rateMode + targetVideoBitrate` owner-approved handoff with task recompile, Native revalidation and stale-evidence invalidation, *then* independently verify a formal encoded output. Do not silently merge, auto-adopt, or modify Canonical from this CI or browser fixture alone.
