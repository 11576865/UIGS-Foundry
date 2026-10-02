# Cross-project Knowledge Inventory — 2026-10-02

Status: first-pass inventory  
Scope: ASS-Workbench-Android, Character-Voice-Service, MKV-Fast-Muxer, Quick-Automatic-Hardsub-Encoder, HSR-Voice-Archive-Builder

This is a **knowledge inventory**, not a claim that every item is already Canonical.

## Promoted into structured experimental/candidate records

### ASS-Workbench-Android
- GitHub Actions artifact-storage guardrail with machine enforcement.
- Renderer-risk adversarial corpus and bounded-work preflight.
- Existing documents also expose device-test fixtures, renderer validation matrices, UI audits, migration checklists, and hardening reports for later ingestion.

### Character-Voice-Service
- System Graph: integration by stable identity, ownership, dependency and lifecycle rather than filesystem co-location.
- Runtime environment isolation: per-engine environments, explicit absolute executable paths, registry/supervisor ownership, GPU exclusivity, and refusal to kill unowned conflicts.

### MKV-Fast-Muxer
- Actionable error taxonomy separates raw evidence, stable failure category, cause, recovery action, and whether output may still be saved.
- Additional future harvest targets: browser E2E, storage/quota behavior, container-preservation regressions, encoding/metadata failures.

### Quick-Automatic-Hardsub-Encoder
- Candidate architecture: shared Web control plane with Windows/Android native execution backends and runtime capability probing.
- Additional future harvest targets: Native Bridge lifecycle, Windows smoke workflows, NVENC runtime-probe failures, cancellation and long-task ownership.

### HSR-Voice-Archive-Builder
- Paid API pre-execution budget guard: heuristic estimate before request, authoritative actual usage after request, reusable completed checkpoints, provider-specific pricing semantics.
- Additional future harvest targets: translation checkpoint/recovery, alignment failures, report-generation and archive-build accounting.

## Cross-project families already visible

1. **Budget guard before expensive work**
   - GitHub Actions storage/retention.
   - Paid API token/USD spending.
   - Parser/preflight work budgets.
   These are distinct mechanisms but share a higher-level family: expensive or attacker-controlled work should have an executable guard before cost is incurred.

2. **Authority must match the real execution path**
   - Native renderer/encoder/runtime results outrank static declarations.
   - Runtime registries and generation revisions make execution identity traceable.

3. **Policy-as-code**
   - A written policy becomes substantially stronger when CI can fail on violations.

4. **Failure knowledge should be operational**
   - Stable error category + evidence + recovery action is more reusable than raw logs alone.

## Not yet harvested

- Multi-agent/worktree coordination: known from development discussions but not yet located as an authoritative repository artifact in this pass.
- Full Bug Museum migration.
- Historical CI red-reason corpus.
- UI screenshots/recordings/golden baselines.
- Generic extraction of all HARDENING / POLICY / DESIGN / ROADMAP / RELEASE documents.

These remain future intake work; absence here must not be interpreted as absence from the source projects.
