# Web realization: UIGS.COMPOSITION.PREVIEW_INSPECTOR_SPLIT

Status: reference recipe derived from HSR Voice Archive Builder.

## Wide layout

Use a primary flexible canvas plus a bounded inspector rather than two equal columns.

A validated production example asserts:

```css
grid-template-columns: minmax(0,1fr) clamp(390px,26vw,460px);
```

The inspector may use `position: sticky` on sufficiently wide pointer/fine layouts. Keep it in normal grid flow; sticky is a presentation behavior, not a new semantic owner.

## Narrow layout

The production contract explicitly switches the inspector back to static positioning and full width on mobile/coarse-pointer layouts.

Required properties:
- primary preview remains the dominant visual surface on wide screens;
- inspector controls stay grouped and reachable;
- advanced controls use disclosure instead of a permanently tall parameter wall;
- control IDs/semantic identity do not change just because presentation changes;
- mobile fallback restores a single-column flow rather than squeezing the desktop split.

Production evidence: HSR-Voice-Archive-Builder `app/static/index.html` and `tests/test_progress_ui.py`.
