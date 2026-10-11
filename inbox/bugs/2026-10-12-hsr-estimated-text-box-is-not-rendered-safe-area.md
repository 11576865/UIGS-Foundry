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
