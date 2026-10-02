# UI Showcases and Golden Baselines

A semantic Pattern is incomplete as visual reference material when it has no observable implementation result.

Evidence levels are intentionally distinct:

1. **Reference Demo** — executable mechanism/interaction example. It does not claim product pixel identity.
2. **Production Evidence / Interaction Recording** — a real product state with repository/state provenance.
3. **Visual Baseline** — declared viewport/theme/state reference suitable for visual regression.

A Showcase does not replace semantic or behavioral contracts. It demonstrates expected realization.

`coverage.json` reports these evidence levels separately. Reference-demo coverage must never be presented as production-evidence or golden-baseline coverage.
