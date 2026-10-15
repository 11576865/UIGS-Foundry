# Candidate: Artifact serialization should not automatically repeat full-corpus pixel validation

Status: Candidate
Date: 2026-10-16
Domains: reliability, operations, interface-grammar
Evidence: explicit user workflow correction + source-code inspection + proposed HSR PR changes; exact-head CI and user/device acceptance pending

## Trigger and product observation

In HSR-Voice-Archive-Builder, generating edited `.ass` subtitle artifacts appeared stalled. Code inspection showed `app/subtitles.py::subtitle_render_config()` configured `verify_libass_layout=True` for all export consumers. `subtitle_layout/ass_writer.py::render_ass()` then ran `solve_subtitle_layout(..., ink_validator=...)`, whose callback ultimately invokes FFmpeg/libass pixel probing, potentially more than once per bilingual cue. The job also originally showed 0/1 until full completion.

The user explicitly requested that this repeated full-corpus ink check be removed from final ASS generation and associated with the preceding explicit preview/validation stage instead. An ASS artifact is subtitle metadata and instructions, not an already rasterized full video.

## Candidate principle (not Canonical)

- Separate **geometry / serialization** (line breaking, positioning, event/format validity, overflow detection, atomic file and receipt publication) from **renderer-authoritative pixel proof** (actual font resolution, stroke/shadow/blur bounds, animation samples).
- Do not make heavyweight per-item pixel proof an automatic side effect of every serialization, on-demand export or incremental edit refresh, unless the explicit product contract requires full coverage at that stage.
- Retain accessible, explicit true-render inspection and attach its evidence to a meaningful scope: cue, renderer/config/font identity, sampled time ranges and provenance. A single still-frame preview is not full-corpus or full-temporal certification.
- Do not present success of a lightweight export as proof that all rendered pixels are safe. `artifact current`, `geometric pass`, `sampled real render`, and `full corpus render-verified` are different claims.
- If heavyweight verification is triggered, its progress must reflect actual work, and synchronous request handling must not block status polling or conflict with project output writes.

## HSR implementation evidence

PR [#185](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/185), branch `fix/ass-export-progress-20261016`, implements an artifact-only `replace(cfg, verify_libass_layout=False)` in both full derived and ASS-only regeneration while keeping the explicit `render_ass_preview_png` `verify_libass_layout=True`. It also restores the original bounded ink-probe cache and updates progress copy. A targeted unit test checks that exported rendering does not invoke `validate_real_ink`; CI and real user runtime acceptance are **Pending**.

## Risk and evidence boundary

Removing export-time actual-ink checks can allow font-dependent visual overflow that a geometric approximation misses. This is an explicit trade-off, **not** evidence that the earlier stage has proven every exported subtitle. Any stronger preflight gate needs an independently scoped validation receipt and renderer/font/style identity. This candidate does not recommend disabling authentic preview or changing SafeArea's meaning.

## Deduplication / related existing records

- `inbox/bugs/2026-10-12-hsr-estimated-text-box-is-not-rendered-safe-area.md` establishes the critical distinction between estimated bounds and actual libass ink. That bug remains valid; this candidate narrows *when* expensive validation runs, not what constitutes rendered proof.
- `inbox/candidates/2026-10-02-long-job-stage-observability-and-completion-handoff.md` covers progress and handoff, but not artifact serialization versus renderer proof.
- `inbox/candidates/2026-10-03-phase-specific-performance-telemetry-must-exclude-validation-time.md` distinguishes stage timing, but not redundant stage execution.

This is one HSR workflow observation and source patch. **No Canonical promotion**.
