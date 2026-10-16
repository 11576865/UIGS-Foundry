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

## Bounded accuracy gate (2026-10-16)

Run `python tools/check_code_atlas_accuracy.py --output /tmp/code-atlas-accuracy.json`.
CI now checks manually specified known edges and *forbidden* false edges, including
dotted-import lookalikes, module basename collisions, and parameter/local/module
shadowing. It also checks three real Foundry code anchors in complete checkouts.

This is an intentionally narrow falsification probe: passing does **not** prove
whole-project recall, dynamic behavior, or correctness on other languages.
A passing result must report the actual counts, failures, and whether real
repository fixtures were available. Uncovered paths remain unknown.

Known unrelated blocker: the general Validate Foundry workflow can fail
because older `inbox/bugs/` records lack required `Lifecycle:` metadata.
Code Atlas validation is separate; do not manufacture lifecycle states just
to turn CI green.

## Opt-in runtime call evidence (Python, experimental)

The browser does **not** execute repository code. Runtime evidence requires
a separate, explicit operator invocation. The traced Python entrypoint runs
with its normal effects, so select a safe test or read-only check. For example:

```bash
python tools/code_atlas_trace.py \
  --root . --repo 11576865/UIGS-Foundry \
  --script tools/test_epistemic_graph.py \
  --output /tmp/uigs-atlas-runtime.json

python tools/code_atlas.py \
  --runtime-trace /tmp/uigs-atlas-runtime.json \
  --export-html /tmp/UIGS_Code_Atlas_with_runtime.html

# Or inspect interactively:
python tools/code_atlas.py --runtime-trace /tmp/uigs-atlas-runtime.json --serve
```

Observed Python-to-Python `call` events are attached only when both endpoint
symbols exist in the static AST index. `python_profile_observed` is displayed
as a visually distinct runtime relationship; AST declarations and inferred
call edges remain separate. Unmatched observed calls are counted and sampled
under `runtime_trace`, not invented as resolved edges.

Safety / correctness rules:

- Trace and source graph must match both repository identity and commit SHA.
  Two unanchored local snapshots may be combined, but are marked `anchored:
  false`, not treated as reproducible commit-pinned evidence.
- No tracing is initiated by the Web UI. The script explicitly supplied via
  `--script` must be inside `--root`; arbitrary script arguments are passed
  after `--`. No subprocess, C-extension, prior-thread, or full asynchronous
  coverage is claimed.
- An event limit is enforced, and truncation is reported. Running the traced
  script may change files or external state exactly as running it normally
  would. Use test fixtures first.
- The collector observes, but does not independently certify itself. Static
  indexing, runtime collection, and tests are distinct evidence channels.


## Correlated explicit operations (experimental)

Code Atlas can now correlate **explicitly instrumented** operation boundaries with real
Python profile calls. Import the opt-in annotation API in a **safe test script**:

```python
from code_atlas_causality import operation, mark

with operation("Save draft"):
    mark("action", "save clicked")
    # Call test functions here.
    mark("state_write", "draft updated", subject="subtitle:draft")
```

This is an *annotation*, not proof that the named state changed. Capture explicitly:

```bash
python tools/code_atlas_trace.py --root . --repo 11576865/UIGS-Foundry --script tools/code_atlas_causality_demo.py --output /tmp/uigs-operations.json
python tools/code_atlas.py --runtime-trace /tmp/uigs-operations.json --export-html /tmp/uigs-operations.html
```

The safe in-repository demo observes one exact call inside an annotated operation.
Select its function node in the exported browser to see operation events alongside
the observed call. When there are no annotations, the operation panel stays hidden.

- Operation IDs and parent IDs track nested spans. Asyncio child tasks inherit
  the operation context by default. Threads do not inherit it automatically.
- State and side-effect annotations are manually emitted claims; do not interpret
  them as independently observed writes, complete side-effect capture, or full
  causal proof. Python function calls are actual profile observations.
- No code is ever run by the browser, and tracing requires an explicit CLI
  entrypoint. All execution side effects remain the operator's responsibility.
- Annotations are capped at 2,000 events (or a lower profile limit) with an
  explicit truncated flag. An incomplete operation tail must not be represented
  as a successful operation completion.
- Static/runtime matching continues to require the same repository and revision;
  unanchored operation evidence is labeled as such.
- The experiment does not yet track JavaScript, Kotlin, external processes,
  actual property writes, lock ownership, distributed traces, or race causation.

## Bounded before-and-after state probe (experimental)

Inside an explicit operation, use `observe_state(subject, read_state)` around a safe action. The supplied probe reads a selected JSON-serializable value twice and emits only `state_delta` with `changed`, `unchanged`, or `unknown`. Neither raw values nor probe exception messages are written to evidence. Each snapshot is limited to 64 KiB; errors and excess size fail closed as `unknown`. The probe reader itself must be side-effect-free and deterministic.

This is an independently computed comparison of two selected probe outputs, **not** proof of causation or full state correctness. The browser inspector labels these readings separately from unverified `state_write` annotations. Browser automation in the current execution environment was blocked by Chromium navigation policy; end-to-end browser acceptance remains Pending.
