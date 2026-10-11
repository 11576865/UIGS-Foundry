# Bug: HSR layout "Safe Area OK" checks estimated text boxes, not rendered ink

Date: 2026-10-12
Status: Confirmed source-code design/validation gap; no production fix in this intake
Product: 11576865/HSR-Voice-Archive-Builder
Branch reviewed: feat/hsr-archive-audit-karaoke-v1
Head reviewed: 741ea4daa56a0944f8926de364a58223cb8af704
Kind: Bug / UI-geometry semantics / false-positive validation

## User observation
The visible screenshot of the Subtitle Style Workbench at 127.0.0.1:8765 shows a green dashed outer "Safe Area" and multiple blue/purple rectangles around text. The user expected the Safe Area to be the final permissible envelope of actually *rendered visible glyph pixels*. If there is both a "safe region for the text box" and another implicit safety margin within that text box, those must not become two independent effective safe areas.

## Verified implementation facts
- `subtitle_layout/safe_area.py` defines a **single explicit** SafeArea rectangle (defaults 3% left/right, 5% top/bottom); there are not two independent SafeArea objects in the inspected solver.
- `subtitle_layout/preview.py::_line_info` computes each line's `bbox` from `measure_text_width` and `measure_line_height`; this is an **estimated layout rectangle**, not a pixel/ink bbox of FFmpeg/libass.
- `subtitle_layout/layout_solver.py` passes estimated lines through `check_bilingual_collision_with_reason`. `subtitle_layout/collision.py` tests estimated width and block extents against `SafeArea`, but does not test true stroke/shadow/blur/card/animated visible effect extents. Its horizontal check even measures width without passing the resolved font path.
- `app/static/index.html::renderPreviewCanvasSvg` draws the Safe Area green dashed rectangle and separate line `bbox` blue/purple dashed rectangles; it emits “✓ 正常 OK” based on estimated `layout.failed`, not verified rendered-pixel coverage.
- `subtitle_layout/ass_writer.py` separately sets ASS margins and uses `\\pos` / animation tags; presence of Style margins alone is **not proof** of double application, because explicit positioning can supersede them. Avoid claiming a definite two-margin numerical bug without a rendered reproduction.
- The 60%/40% primary/Chinese split in `layout_solver.py` and `preview.py` is hard-coded; this is a separate configurable-ratio issue, not a second Safe Area.

## Why this is a bug
The UI labels geometric estimation as safety clearance. Real glyph pixels and effects can extend beyond estimated rectangles. Hence `layout.failed == False` does **not** imply the libass output's visible ink is contained within the Safe Area. This is a code-derived false-certification risk, not yet a real-world clipping reproduction.

## Acceptance recommendation
1. Keep ONE authoritative Safe Area in 1920x1080 final-render coordinates, bounding actual visible subtitle pixels/effects (use a documented alpha/perceptual threshold for blur/glow), including relevant temporal frames.
2. Keep per-line layout/text boxes as computed, read-only diagnostic overlays, hidden by default and never labeled “another safe zone” or offered as competing drag handles.
3. Distinguish estimated layout status from **verified libass rendered safe-area status**. Until the authoritative check exists, label the green pass “几何估算通过；最终渲染待验证”.
4. Use a pixel-mask-based FFmpeg/libass frame check over representative or all relevant time states, with tests involving bold descenders/ascenders, CJK, outline, shadow, blur, kinetic motion and line wrapping. Do not use `measure_line_height=font_size*1.25` as evidence of exact ink.
5. Check safe-area overshoot independently of valid central separation/gaps; expose the 60/40 split as a user preset/parameter in a separate UI change.
6. Prove browser diagnostic and final ASS output agree on the *meaning* of Safe Area, rather than forcing the glyph to remain inside an artificial second inset.

## Deduplication
Related HSR case `inbox/cases/2026-10-10-hsr-subtitle-preview-evidence-and-async-save.md` covers asynchronous preview provenance, but not the geometry/visible-ink distinction. Existing experimental `domains/reliability/test-patterns/TEST.RENDERED_EFFECT_DIFFERENTIAL.json` concerns verifying actual rendered effects and may support future testing; it does not already specify this Safe Area contract. Distinct Bug intake, not a Canonical amendment.

Evidence level: source inspection and user screenshot, **not** instrumented libass pixel reproducer. Status Pending fix; Canonical unchanged.


## 2026-10-12 continuation: mitigations submitted for review (not verified production fix)

HSR PR [#134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134) is stacked on #133 → #132 and now proposes a source implementation at branch `feat/hsr-layout-safety-ratio-karaoke-preview` (initial commit `5ed706eae6f2f14921b5faee5bdbd1ef010ec4d0`, follow-up badge correction `6cdf8abb0e20cbe8a3f4f6ec546d8c0e702b66db`).

- Defines a configurable `primary_region_ratio` (default 0.60) with project persistence, preview/export parity and UI slider, instead of the formerly hard-coded split.
- The geometry diagnostic boxes and central-gap helper are off by default, while the single explicit SafeArea remains visible. The green pass explicitly says “几何估算通过 · 像素待验证” rather than claiming final pixel safety.
- For explicitly positioned CHS/Primary `\\pos` events, ASS style MarginL/Right/V are set to zero to avoid potentially compounding layout SafeArea and style margins; original intake correctly did **not** establish that both had been applied, so the new change must be verified against libass output rather than described as a confirmed defect fix. Archive HUD retains margins.
- Collision-width checks now use the font path resolved for line breaking. A time scrubber can request a real FFmpeg/libass frame at the selected percentage without creating a second editor/state model.

**Status:** mitigation code submitted in Draft PR, exact-head CI / libass pixel-mask validation / target-device acceptance pending. The core Bug about comparing actual rendered ink against the true SafeArea over effect-relevant time remains **OPEN**. No Canonical promotion or new duplicate Candidate. Existing HSR async-preview Case is related but remains separately recorded.


## 2026-10-12 follow-up: sampled rendered-ink validation submitted

HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134) now includes commits `9e30e3f257879e522a83ba7b97c5e94ca2df1852` and `440c1bab4b7704ac3c5ba41b36c88bc875977a73`. The FastAPI/Termux Lite action `/api/subtitle-layout/inspect-rendered-ink` renders the same unsaved ASS trial at the requested fractional timestamp on black and white backgrounds and estimates the actual visible-pixel bounding box with a documented RGB contrast threshold 16. It compares against the single SafeArea and reports single-frame evidence separately from geometric validity. UI clears stale evidence when the trial payload changes.

The original geometry bug is **partially mitigated, not closed**. The current method is a *single-time sample*, not a complete scan of Karaoke/kinetic states. Effects fainter than the threshold may be missed. Fully clipped offscreen glyph geometry cannot be reconstructed from the framebuffer, and final media configuration/device/font differences remain independent. No exact-head CI result or field pixel acceptance is inferred. Future work: bounded temporal sampling/full relevant timeline validation, explicit coverage reporting, and final saved-artifact identity. No Canonical promotion.


## 2026-10-12 continuation: bounded temporal sampling submitted in PR #134

HSR [PR #134](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/134), exact-head `577b2c0bdf27a3ff6a6dfcb109307b7f52901905`, adds an opt-in, budget-capped **dynamic-interval sampling** route and UI action alongside the existing single-frame ink inspection. The production code constructs deterministic candidate instants from 0 and end, a midpoint, distributed times, kinetic fade/soft-entry events, and valid karaoke word boundaries; it selects at most eight instants by default (server max 12) and consumes only the first 500 valid source alignment entries when computing candidate events. One actual synthesized ASS is reused while each selected timestamp is rendered on black and white backgrounds and compared against the single explicit SafeArea.

Validation responses declare `scope=bounded_sampled_timestamps_only` and `full_interval_verified=false`, per-frame ink boxes and observed violations, `candidate_count`, `omitted_candidate_count`, and `max_unsampled_gap_seconds`. `sampled_no_violation` cannot be promoted to all-time safety; `no_visible_evidence` is separately inconclusive. Exceptions fail the check rather than publish partial success. The browser invalidates stale results on edits. FastAPI offloads the expensive operation to a threadpool; browser abort does not cancel already-running FFmpeg subprocesses on the server.

**Source evidence:** implementation/test/workflow committed. New exact-head GitHub Actions [tests](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38171331084) and [real libass/browser](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38171331071) jobs were started, status **pending** at intake. The earlier head's unit failure was traced to an outdated exact JS timestamp string assertion and updated in this commit; do not claim the new tests pass until CI completes. No real Android field acceptance or exhaustive dynamic duration proof. The Bug remains **OPEN (partially mitigated)**. Canonical remains unchanged.
