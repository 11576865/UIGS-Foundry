# Interface Grammar Compositions

A Pattern answers a reusable UI question. A **Composition Recipe** describes how several Patterns may be combined without collapsing their state ownership or semantics.

Composition is not a new maturity shortcut. A recipe may be Experimental while its member Patterns have different evidence levels.

The resolver returns:

- matched Patterns;
- matching Recipes;
- required/recommended/optional member coverage;
- platform realization references;
- Showcase evidence;
- known missing evidence.

It must not infer that two Pattern IDs are compatible merely because both match the same sentence. Explicit relation/recipe data carries composition semantics.
