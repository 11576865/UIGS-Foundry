# Source-owned UI Surface Inventory

This layer answers a different question from the Pattern Registry:

- **Pattern Registry:** what reusable UI grammar exists?
- **Surface Inventory:** what concrete UI actually exists in each product, where is it implemented, and what effect does it have?

Each product repository remains authoritative and declares an optional `ui_inventory` pointer in `.uigs/project.json`. The pointed `.uigs/ui-surfaces.json` contains stable concrete Surface IDs, implementation effects, source references, Pattern links, tests and production visual-evidence references.

Foundry periodically reads the adapter and inventory at the same source HEAD and builds a derived cross-project index.

A product without a declared inventory is reported as missing coverage. Foundry does not infer or invent its surfaces.

An empty `visual_evidence` array means the concrete surface is indexed but no product screenshot/recording has yet been registered.
