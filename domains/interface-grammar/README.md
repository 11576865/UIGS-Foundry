# Interface Grammar

This domain contains the reusable User Interface Grammar System.

A human or agent should be able to resolve:

**natural-language intent -> Pattern ID -> platform realization -> expected effect -> validation contract -> known failures**

- `registry/` — semantic identity, intent, anatomy, aliases, constraints.
- `realizations/` — concrete platform recipes.
- `showcases/` — reference demos, recordings, and visual baselines.
- `validation/` — behavior contracts, visual regression, accessibility, performance.
- `evidence/` — production cases, screenshots, recordings, source references.
- `compatibility/` — capability matrices and fallbacks.

A Pattern defines what the UI means. A Realization defines how a platform implements it. A Showcase demonstrates the expected effect. Validation proves properties. Do not collapse these layers.
