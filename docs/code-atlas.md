# Code Atlas — read-only source observer (experimental)

Code Atlas is a browser interface over automatically generated **Python AST facts**. It is part of UIGS observability, not a second policy system and not an AI-generated architecture poster.

## Start

From a full local checkout of UIGS-Foundry:

```bash
python tools/code_atlas.py --serve
# open http://127.0.0.1:8765
```

To export the graph without the browser:

```bash
python tools/code_atlas.py --output /tmp/uigs-code-atlas.json
```

To generate a single standalone HTML file that opens without a server (including on another device):

```bash
python tools/code_atlas.py --export-html /tmp/UIGS_Code_Atlas.html
```

A standalone HTML includes one pinned graph snapshot; regenerate after source changes. A CI artifact is downloadable from Code Atlas Source Observation workflow runs.

To inspect another local Python repository, pass `--root /path/to/checkout --repo owner/name`. Run it against UIGS-Foundry itself first. Nothing is pushed and the server exposes only `/`, `/index.html`, and `/api/graph`, binding to `127.0.0.1` by default.

## What the graph says

- `file` / `function` nodes: syntax definitions from parsed `.py` files.
- `declares` / `imports` / `calls` edges: *static* AST syntax, with a direct file and line pointer.
- Calls through reflection, callbacks, unknown dispatch, reassigned symbols, other languages, and external services are **not** proven. `unresolved_call_sites` counts conservatively unresolved syntactic calls. Static edges are **not runtime evidence**.
- Source links are only emitted when the index is tied to a 40-character Git commit SHA; use a clean or recorded checkout for reproducible reviews. Uncommitted changes are not represented by the commit URL; rerun after committing.
- The UI deliberately limits displayed nodes while search covers the complete local index. A missing visible edge is not proof of independence.

## Falsification gate

1. Index the tool itself. Its own `index()`, `serve()` and test symbols must be discoverable.
2. Check an imported call across files (e.g. `generate_validation_missions.generate -> evaluate_epistemic_graph.evaluate`) against exact source.
3. Deliberately shadow an imported function name and verify that the graph **does not** claim a call to the imported function.
4. Introduce syntactically invalid Python and verify an explicit parse error, not a fabricated empty graph.
5. Run `python -m unittest discover -s tools -p test_code_atlas.py -v` and test the served browser manually.

**Status:** Python-only experimental slice. No claim of general cross-language understanding, race detection, causal proof, complete coverage, or independent self-certification. Product repository code and CI remain authoritative. UIGS Foundry's Claim/Evidence process is the governance layer; this graph is only a derived read model.