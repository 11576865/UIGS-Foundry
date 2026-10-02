# Web realization: UIGS.WORKSPACE.STICKY_SUPPORTING_PANE

Status: reference recipe

Keep the pane in normal layout flow and make the pane sticky rather than turning it into an unrelated fixed overlay.

```css
.workspace {
  display: grid;
  grid-template-columns: minmax(0, 1fr) clamp(270px, 27vw, 340px);
  gap: 14px;
  align-items: start;
}
.supporting-pane {
  position: sticky;
  top: 10px;
  max-height: calc(100dvh - 20px);
  overflow-y: auto;
  overflow-x: hidden;
}
@media (max-width: 899px) {
  .supporting-pane {
    position: static;
    max-height: none;
    overflow: visible;
  }
}
```

Sticky positioning does not create backdrop blur. A glass variant requires a translucent surface plus `backdrop-filter` and a readable fallback.

Required tests: main-content scroll, pane overflow, narrow fallback, viewport-height reduction, ancestor overflow/transform, touch scrolling, horizontal overflow, and no-blur fallback.
